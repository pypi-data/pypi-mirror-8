import numpy as np
import logging
import itertools
import functools
import collections
import time

log = logging.getLogger(__name__)

from . import stream
from . import dsp
from . import sampling
from . import train
from . import common
from . import config
from . import framing
from . import equalizer

modem = dsp.MODEM(config.symbols)

# Plots' size (WIDTH x HEIGHT)
HEIGHT = np.floor(np.sqrt(config.Nfreq))
WIDTH = np.ceil(config.Nfreq / float(HEIGHT))

COHERENCE_THRESHOLD = 0.99

CARRIER_DURATION = sum(train.prefix)
CARRIER_THRESHOLD = int(0.99 * CARRIER_DURATION)
SEARCH_WINDOW = 10  # symbols


def report_carrier(bufs, begin):
    x = np.concatenate(tuple(bufs)[-CARRIER_THRESHOLD:-1])
    Hc = dsp.exp_iwt(-config.Fc, len(x))
    Zc = np.dot(Hc, x) / (0.5*len(x))
    amp = abs(Zc)
    log.info('Carrier detected at ~%.1f ms @ %.1f kHz:'
             ' coherence=%.3f%%, amplitude=%.3f',
             begin * config.Tsym * 1e3 / config.Nsym, config.Fc / 1e3,
             np.abs(dsp.coherence(x, config.Fc)) * 100, amp)
    return amp


def detect(samples, freq):
    counter = 0
    bufs = collections.deque([], maxlen=config.baud)  # 1 second of symbols
    for offset, buf in common.iterate(samples, config.Nsym, enumerate=True):
        bufs.append(buf)

        coeff = dsp.coherence(buf, config.Fc)
        if abs(coeff) > COHERENCE_THRESHOLD:
            counter += 1
        else:
            counter = 0

        if counter == CARRIER_THRESHOLD:
            length = (CARRIER_THRESHOLD - 1) * config.Nsym
            begin = offset - length
            amplitude = report_carrier(bufs, begin=begin)
            break
    else:
        raise ValueError('No carrier detected')

    log.debug('Buffered %d ms of audio', len(bufs))

    bufs = list(bufs)[-CARRIER_THRESHOLD-SEARCH_WINDOW:]
    trailing = list(itertools.islice(samples, SEARCH_WINDOW*config.Nsym))
    bufs.append(np.array(trailing))

    buf = np.concatenate(bufs)
    offset = find_start(buf, CARRIER_DURATION*config.Nsym)
    log.debug('Carrier starts at %.3f ms',
              offset * config.Tsym * 1e3 / config.Nsym)

    return itertools.chain(buf[offset:], samples), amplitude


def find_start(buf, length):
    N = len(buf)
    carrier = dsp.exp_iwt(config.Fc, N)
    z = np.cumsum(buf * carrier)
    z = np.concatenate([[0], z])
    correlations = np.abs(z[length:] - z[:-length])
    return np.argmax(correlations)


class Receiver(object):

    def __init__(self, plt=None):
        self.stats = {}
        self.plt = plt or common.Dummy()

    def _prefix(self, sampler, freq, gain=1.0, skip=5):
        symbols = dsp.Demux(sampler, [freq])
        S = common.take(symbols, len(train.prefix)).squeeze() * gain
        sliced = np.round(np.abs(S))
        self.plt.figure()
        self.plt.subplot(121)
        self._constellation(S, sliced, 'Prefix')

        bits = np.array(sliced, dtype=int)
        self.plt.subplot(122)
        self.plt.plot(np.abs(S))
        self.plt.plot(train.prefix)
        if any(bits != train.prefix):
            raise ValueError('Incorrect prefix')

        log.debug('Prefix OK')

        nonzeros = np.array(train.prefix, dtype=bool)
        pilot_tone = S[nonzeros]
        phase = np.unwrap(np.angle(pilot_tone)) / (2 * np.pi)
        indices = np.arange(len(phase))
        a, b = dsp.linear_regression(indices[skip:-skip], phase[skip:-skip])
        self.plt.figure()
        self.plt.plot(indices, phase, ':')
        self.plt.plot(indices, a * indices + b)

        freq_err = a / (config.Tsym * config.Fc)
        last_phase = a * indices[-1] + b
        log.debug('Current phase on carrier: %.3f', last_phase)

        log.debug('Frequency error: %.2f ppm', freq_err * 1e6)
        self.plt.title('Frequency drift: {:.3f} ppm'.format(freq_err * 1e6))
        return freq_err

    def _train(self, sampler, order, lookahead):
        gain = config.Nfreq
        train_symbols = equalizer.train_symbols(train.equalizer_length)
        train_signal = equalizer.modulator(train_symbols) * gain

        prefix = postfix = train.silence_length * config.Nsym
        signal_length = train.equalizer_length * config.Nsym + prefix + postfix

        signal = sampler.take(signal_length + lookahead)

        coeffs = equalizer.equalize_signal(
            signal=signal[prefix:-postfix],
            expected=train_signal,
            order=order, lookahead=lookahead
        )

        log.debug(
            'Equalization filter: [%s]',
            ', '.join('{:.2f}'.format(c) for c in coeffs)
        )
        equalization_filter = dsp.FIR(h=coeffs)
        equalized = list(equalization_filter(signal))
        equalized = equalized[prefix+lookahead:-postfix+lookahead]

        symbols = equalizer.demodulator(equalized, train.equalizer_length)
        sliced = np.array(symbols).round()
        errors = np.array(sliced - train_symbols, dtype=np.bool)
        error_rate = errors.sum() / errors.size

        errors = np.array(symbols - train_symbols)
        rms = lambda x: (np.mean(np.abs(x) ** 2, axis=0) ** 0.5)

        noise_rms = rms(errors)
        signal_rms = rms(train_symbols)
        SNRs = 20.0 * np.log10(signal_rms / noise_rms)

        self.plt.figure()
        for i, freq, snr in zip(range(config.Nfreq), config.frequencies, SNRs):
            log.debug('%5.1f kHz: SNR = %5.2f dB', freq / 1e3, snr)
            self.plt.subplot(HEIGHT, WIDTH, i+1)
            self._constellation(symbols[:, i], train_symbols[:, i],
                                '$F_c = {} Hz$'.format(freq))

        assert error_rate == 0, error_rate

        return equalization_filter

    def _demodulate(self, sampler, freqs):
        streams = []
        symbol_list = []
        errors = {}

        def error_handler(received, decoded, freq):
            errors.setdefault(freq, []).append(received / decoded)

        symbols = dsp.Demux(sampler, freqs)
        generators = common.split(symbols, n=len(freqs))
        for freq, S in zip(freqs, generators):
            equalized = []
            S = common.icapture(S, result=equalized)
            symbol_list.append(equalized)

            freq_handler = functools.partial(error_handler, freq=freq)
            bits = modem.decode(S, freq_handler)  # list of bit tuples
            streams.append(bits)  # stream per frequency

        self.stats['symbol_list'] = symbol_list
        self.stats['rx_bits'] = 0
        self.stats['rx_start'] = time.time()

        log.info('Starting demodulation: %s', modem)
        for i, block in enumerate(common.izip(streams)):  # block per frequency
            for bits in block:
                self.stats['rx_bits'] = self.stats['rx_bits'] + len(bits)
                yield bits

            if i > 0 and i % config.baud == 0:
                err = np.array([e for v in errors.values() for e in v])
                err = np.mean(np.angle(err))/(2*np.pi) if len(err) else 0
                errors.clear()

                duration = time.time() - self.stats['rx_start']
                sampler.freq -= 0.01 * err / config.Fc
                sampler.offset -= err
                log.debug(
                    'Got  %8.1f kB, realtime: %6.2f%%, drift: %+5.2f ppm',
                    self.stats['rx_bits'] / 8e3,
                    duration * 100.0 / (i*config.Tsym),
                    (1.0 - sampler.freq) * 1e6
                )

    def start(self, signal, freqs, gain=1.0):
        sampler = sampling.Sampler(signal, sampling.Interpolator())

        freq_err = self._prefix(sampler, freq=freqs[0], gain=gain)
        sampler.freq -= freq_err

        filt = self._train(sampler, order=11, lookahead=5)
        sampler.equalizer = lambda x: list(filt(x))

        bitstream = self._demodulate(sampler, freqs)
        self.bitstream = itertools.chain.from_iterable(bitstream)

    def run(self, output):
        data = framing.decode(self.bitstream)
        self.size = 0
        for chunk in common.iterate(data=data, size=256,
                                    truncate=False, func=bytearray):
            output.write(chunk)
            self.size += len(chunk)

    def report(self):
        if self.stats:
            duration = time.time() - self.stats['rx_start']
            audio_time = self.stats['rx_bits'] / float(config.modem_bps)
            log.debug('Demodulated %.3f kB @ %.3f seconds (%.1f%% realtime)',
                      self.stats['rx_bits'] / 8e3, duration,
                      100 * duration / audio_time if audio_time else 0)

            log.info('Received %.3f kB @ %.3f seconds = %.3f kB/s',
                     self.size * 1e-3, duration, self.size * 1e-3 / duration)

            self.plt.figure()
            symbol_list = np.array(self.stats['symbol_list'])
            for i, freq in enumerate(config.frequencies):
                self.plt.subplot(HEIGHT, WIDTH, i+1)
                self._constellation(symbol_list[i], config.symbols,
                                    '$F_c = {} Hz$'.format(freq))
        self.plt.show()

    def _constellation(self, y, symbols, title):
        theta = np.linspace(0, 2*np.pi, 1000)
        y = np.array(y)
        self.plt.plot(y.real, y.imag, '.')
        self.plt.plot(np.cos(theta), np.sin(theta), ':')
        points = np.array(symbols)
        self.plt.plot(points.real, points.imag, '+')
        self.plt.grid('on')
        self.plt.axis('equal')
        self.plt.axis(np.array([-1, 1, -1, 1])*1.1)
        self.plt.title(title)


def main(args):
    reader = stream.Reader(args.input, data_type=common.loads)
    signal = itertools.chain.from_iterable(reader)

    skipped = common.take(signal, args.skip)
    log.debug('Skipping %.3f seconds', len(skipped) / float(config.baud))

    reader.check = common.check_saturation

    receiver = Receiver(plt=args.plot)
    success = False
    try:
        log.info('Waiting for carrier tone: %.1f kHz', config.Fc / 1e3)
        signal, amplitude = detect(signal, config.Fc)
        receiver.start(signal, config.frequencies, gain=1.0/amplitude)
        receiver.run(args.output)
        success = True
    except Exception:
        log.exception('Decoding failed')

    receiver.report()
    return success
