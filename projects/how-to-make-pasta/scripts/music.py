"""Synthesize a light, upbeat plucked-guitar music bed (deterministic)."""
import sys, wave
import numpy as np

SR = 44100
BPM = 112
BEAT = 60 / BPM
DUR = 31.0
rng = np.random.default_rng(7)
out = np.zeros(int(SR * DUR) + SR)

def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)

def pluck(freq, length=1.2, bright=0.5):
    """Karplus-Strong plucked string."""
    n = int(SR * length)
    period = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, period) * bright + rng.uniform(-1, 1, period) * (1 - bright) * 0.3
    y = np.zeros(n)
    for i in range(n):
        y[i] = buf[i % period]
        buf[i % period] = 0.497 * (buf[i % period] + buf[(i + 1) % period])
    return y

def add(sig, t, gain):
    i = int(t * SR)
    seg = sig[: len(out) - i]
    out[i : i + len(seg)] += seg * gain

# C - G - Am - F  (ukulele-ish voicings)
chords = [
    [60, 64, 67, 72],
    [59, 62, 67, 71],
    [57, 60, 64, 69],
    [57, 60, 65, 69],
]
bass = [36, 43, 45, 41]

# Pre-render a cache of plucks per note
cache = {}
def note(n, bright=0.6, length=1.0):
    key = (n, bright, length)
    if key not in cache:
        cache[key] = pluck(midi(n), length, bright)
    return cache[key]

bar = 4 * BEAT
t = 0.0
k = 0
# strum pattern in eighths: D . D U . U D U
pattern = [(0, 1.0, 1), (1, 0.55, 1), (1.5, 0.5, -1), (2.5, 0.5, -1), (3, 0.75, 1), (3.5, 0.45, -1)]
while t < DUR:
    ch = chords[k % 4]
    for beat, vel, direction in pattern:
        st = t + beat * BEAT
        notes = ch if direction > 0 else list(reversed(ch))
        for j, n in enumerate(notes):
            add(note(n), st + j * 0.012, 0.09 * vel)
    # soft bass on 1 and 3
    add(note(bass[k % 4], 0.3, 1.6), t, 0.22)
    add(note(bass[k % 4] + 7, 0.3, 1.2), t + 2 * BEAT, 0.14)
    # shaker on every eighth
    sh = rng.uniform(-1, 1, int(0.05 * SR)) * np.exp(-np.linspace(0, 8, int(0.05 * SR)))
    sh = np.diff(sh, prepend=0)  # brighten (high-pass)
    for e in range(8):
        add(sh, t + e * BEAT / 2, 0.05 if e % 2 else 0.025)
    t += bar
    k += 1

out = out[: int(SR * DUR)]
# fade in / out
fi, fo = int(0.3 * SR), int(2.0 * SR)
out[:fi] *= np.linspace(0, 1, fi)
out[-fo:] *= np.linspace(1, 0, fo)
out /= np.max(np.abs(out)) + 1e-9
out *= 0.8
pcm = (out * 32767).astype(np.int16)
stereo = np.stack([pcm, pcm], axis=1)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(stereo.tobytes())
print("wrote", sys.argv[1])
