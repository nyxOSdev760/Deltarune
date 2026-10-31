"""Tiny chiptune synth: square / triangle / noise voices with hard little
envelopes, mixed into one mono track, written as 16-bit WAV."""
import wave
import numpy as np

SR = 44100
NOTE = {n: i for i, n in enumerate("C C# D D# E F F# G G# A A# B".split())}


def hz(name):
    """'C5', 'F#3' -> frequency."""
    pitch, octave = name[:-1], int(name[-1])
    midi = 12 * (octave + 1) + NOTE[pitch]
    return 440.0 * 2 ** ((midi - 69) / 12)


def _t(dur):
    return np.arange(int(SR * dur)) / SR


def env(n, attack=0.004, release=0.04, decay=None):
    e = np.ones(n, dtype=np.float32)
    a, r = int(SR * attack), int(SR * release)
    if a:
        e[:a] = np.linspace(0, 1, a)
    if r and r < n:
        e[-r:] *= np.linspace(1, 0, r)
    if decay:
        e *= np.exp(-np.arange(n) / (SR * decay))
    return e


def square(f, dur, duty=0.5, vol=0.2, slide_to=None, vibrato=0.0):
    t = _t(dur)
    freq = np.full_like(t, f) if slide_to is None else np.linspace(f, slide_to, len(t))
    if vibrato:
        freq = freq * (1 + vibrato * np.sin(2 * np.pi * 6 * t))
    phase = np.cumsum(freq) / SR
    w = np.where((phase % 1.0) < duty, 1.0, -1.0)
    return (w * vol).astype(np.float32)


def tri(f, dur, vol=0.25, slide_to=None):
    t = _t(dur)
    freq = np.full_like(t, f) if slide_to is None else np.linspace(f, slide_to, len(t))
    phase = np.cumsum(freq) / SR
    return ((4 * np.abs((phase % 1.0) - 0.5) - 1) * vol).astype(np.float32)


def sine(f, dur, vol=0.2, vibrato=0.0, slide_to=None):
    t = _t(dur)
    freq = np.full_like(t, f) if slide_to is None else np.linspace(f, slide_to, len(t))
    if vibrato:
        freq = freq * (1 + vibrato * np.sin(2 * np.pi * 5.5 * t))
    return (np.sin(2 * np.pi * np.cumsum(freq) / SR) * vol).astype(np.float32)


def noise(dur, vol=0.2, seed=0, lowpass=None):
    rnd = np.random.default_rng(seed)
    x = rnd.uniform(-1, 1, int(SR * dur)).astype(np.float32)
    if lowpass:
        a = np.exp(-2 * np.pi * lowpass / SR)
        y = np.empty_like(x)
        acc = 0.0
        for i, v in enumerate(x):
            acc = a * acc + (1 - a) * v
            y[i] = acc
        x = y / (np.abs(y).max() + 1e-9)
    return x * vol


class Track:
    def __init__(self, seconds):
        self.buf = np.zeros(int(SR * seconds) + SR, dtype=np.float32)
        self.seconds = seconds

    def add(self, t, samples, e=None):
        if e is None:
            e = env(len(samples))
        i = int(t * SR)
        if i >= len(self.buf):
            return
        s = samples * e
        j = min(len(self.buf), i + len(s))
        self.buf[i:j] += s[: j - i]

    def write(self, path):
        x = self.buf[: int(SR * self.seconds)]
        peak = np.abs(x).max()
        if peak > 0.95:
            x = x * (0.95 / peak)
        pcm = (x * 32767).astype("<i2")
        with wave.open(path, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(pcm.tobytes())
