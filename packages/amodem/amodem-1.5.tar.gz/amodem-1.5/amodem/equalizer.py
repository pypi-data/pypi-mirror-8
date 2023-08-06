import numpy as np
from numpy.linalg import lstsq

from amodem import dsp
from amodem import sampling

import itertools
import random

_constellation = [1, 1j, -1, -1j]


class Equalizer(object):

    def __init__(self, config):
        self.carriers = config.carriers
        self.omegas = 2 * np.pi * np.array(config.frequencies) / config.Fs
        self.Nfreq = config.Nfreq
        self.Nsym = config.Nsym

    def train_symbols(self, length, seed=0):
        r = random.Random(seed)
        choose = lambda: [r.choice(_constellation) for j in range(self.Nfreq)]
        return np.array([choose() for _ in range(length)])

    def modulator(self, symbols):
        gain = 1.0 / len(self.carriers)
        result = []
        for s in symbols:
            result.append(np.dot(s, self.carriers))
        result = np.concatenate(result).real * gain
        assert np.max(np.abs(result)) <= 1
        return result

    def demodulator(self, signal, size):
        signal = itertools.chain(signal, itertools.repeat(0))
        symbols = dsp.Demux(sampler=sampling.Sampler(signal),
                            omegas=self.omegas, Nsym=self.Nsym)
        return np.array(list(itertools.islice(symbols, size)))

    def equalize_symbols(self, signal, symbols, order, lookahead=0):
        assert symbols.shape[1] == self.Nfreq
        length = symbols.shape[0]

        matched = np.array(self.carriers) / (0.5*self.Nsym)
        matched = matched[:, ::-1].transpose().conj()
        signal = np.concatenate([signal, np.zeros(lookahead)])
        y = dsp.lfilter(x=signal, b=matched, a=[1])

        A = []
        b = []

        for j in range(self.Nfreq):
            for i in range(length):
                offset = (i+1)*self.Nsym
                row = y[offset-order:offset+lookahead, j]
                A.append(row)
                b.append(symbols[i, j])

        A = np.array(A)
        b = np.array(b)
        h = lstsq(A, b)[0]
        h = h[::-1].real

        return h

    def equalize_signal(self, signal, expected, order, lookahead=0):
        signal = [np.zeros(order-1), signal, np.zeros(lookahead)]
        signal = np.concatenate(signal)
        length = len(expected)

        A = []
        b = []

        for i in range(length - order):
            offset = order + i
            row = signal[offset-order:offset+lookahead]
            A.append(np.array(row, ndmin=2))
            b.append(expected[i])

        A = np.concatenate(A, axis=0)
        b = np.array(b)
        h = lstsq(A, b)[0]
        h = h[::-1].real
        return h
