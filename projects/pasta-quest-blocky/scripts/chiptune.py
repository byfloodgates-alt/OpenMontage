"""Original chiptune bed + game SFX track (deterministic). Usage: chiptune.py bed.wav sfx.wav"""
import sys, wave
import numpy as np

SR = 44100
DUR = 30.5
BPM = 132
B = 60 / BPM
rng = np.random.default_rng(3)

def buf():
    return np.zeros(int(SR * DUR) + SR)

def f(n):
    return 440.0 * 2 ** ((n - 69) / 12)

def env(n, a=0.005, r=0.08):
    t = np.arange(n) / SR
    e = np.minimum(1, t / a) * np.exp(-t / r)
    return e

def square(freq, dur, duty=0.5, r=0.12):
    n = int(SR * dur)
    t = np.arange(n) / SR
    s = np.where((t * freq) % 1 < duty, 1.0, -1.0)
    return s * env(n, r=r)

def tri(freq, dur, r=0.25):
    n = int(SR * dur)
    t = np.arange(n) / SR
    s = 2 * np.abs(2 * ((t * freq) % 1) - 1) - 1
    return s * env(n, r=r)

def noise(dur, r=0.03):
    n = int(SR * dur)
    return rng.uniform(-1, 1, n) * env(n, a=0.001, r=r)

def put(track, sig, t, g):
    i = int(t * SR)
    seg = sig[: len(track) - i]
    track[i : i + len(seg)] += seg * g

def write(path, x):
    x = x[: int(SR * DUR)]
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.85
    pcm = (x * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.stack([pcm, pcm], 1).tobytes())

# ---------------- music bed ----------------
bed = buf()
# progression (one bar each): C  Am  F  G
roots = [48, 45, 41, 43]
arps = [[60, 64, 67, 72], [57, 60, 64, 69], [53, 57, 60, 65], [55, 59, 62, 67]]
# original 2-bar lead motifs (scale degrees in C), 8th-note grid; None = rest
lead_a = [72, None, 74, 76, None, 74, 72, 67, 69, None, 72, None, 74, 72, None, None]
lead_b = [76, None, 77, 79, None, 77, 76, 72, 74, None, 71, None, 72, None, None, None]
bar = 4 * B
t, k = 0.0, 0
while t < DUR:
    ch = k % 4
    # bass: root on beats, octave bounce on offbeats
    for b8 in range(8):
        n = roots[ch] + (12 if b8 % 2 else 0)
        put(bed, tri(f(n), B / 2 * 0.95, r=0.12), t + b8 * B / 2, 0.30)
    # 16th arpeggio, quiet
    for s16 in range(16):
        n = arps[ch][s16 % 4]
        put(bed, square(f(n), B / 4 * 0.9, duty=0.25, r=0.05), t + s16 * B / 4, 0.045)
    # lead over 2-bar phrases, starting bar 2 so the hook has room
    if k >= 1:
        phrase = lead_a if (k // 2) % 2 == 0 else lead_b
        half = (k % 2) * 8
        for j in range(8):
            n = phrase[half + j]
            if n is not None:
                put(bed, square(f(n), B / 2 * 0.9, duty=0.5, r=0.16), t + j * B / 2, 0.07)
    # drums: kick 1&3, snare 2&4, hats 8ths
    for b in range(4):
        st = t + b * B
        if b % 2 == 0:
            n = int(SR * 0.12); tt = np.arange(n) / SR
            kick = np.sin(2 * np.pi * (60 + 120 * np.exp(-tt * 40)) * tt) * np.exp(-tt * 18)
            put(bed, kick, st, 0.45)
        else:
            put(bed, noise(0.12, r=0.05), st, 0.18)
    for e in range(8):
        h = np.diff(noise(0.03, r=0.01), prepend=0)
        put(bed, h, t + e * B / 2, 0.10)
    t += bar
    k += 1
fi, fo = int(0.2 * SR), int(1.5 * SR)
bed[:fi] *= np.linspace(0, 1, fi)
end = int(SR * DUR)
bed[end - fo : end] *= np.linspace(1, 0, fo)
write(sys.argv[1], bed)

# ---------------- SFX ----------------
sfx = buf()
S = [0, 3.0, 7.0, 11.2, 15.4, 20.0, 24.2]

def pop(t):
    n = int(SR * 0.09); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * (300 + 900 * tt / 0.09) * tt) * np.exp(-tt * 35)
    put(sfx, s, t, 0.5)

def coin(t):
    put(sfx, square(f(83), 0.07, duty=0.5, r=0.05), t, 0.25)
    put(sfx, square(f(88), 0.35, duty=0.5, r=0.12), t + 0.07, 0.25)

def click(t):
    put(sfx, square(f(76), 0.05, duty=0.25, r=0.02), t, 0.3)
    put(sfx, square(f(84), 0.08, duty=0.25, r=0.04), t + 0.05, 0.3)

def levelup(t):
    for j, n in enumerate([72, 76, 79, 84, 88, 91, 96]):
        put(sfx, square(f(n), 0.12, duty=0.5, r=0.08), t + j * 0.07, 0.22)
    put(sfx, square(f(96), 0.6, duty=0.5, r=0.3), t + 0.5, 0.18)
    put(sfx, square(f(91), 0.6, duty=0.25, r=0.3), t + 0.5, 0.12)

def whoosh(t):
    n = int(SR * 0.25); x = rng.uniform(-1, 1, n)
    e = np.sin(np.linspace(0, np.pi, n))
    put(sfx, np.diff(x, prepend=0) * e, t, 0.12)

pop(0.15)
for i in range(1, 7):
    whoosh(S[i] - 0.1)
    pop(S[i] + 0.15)
# step-complete check + coin when XP pops (near the end of each step's narration)
for i, tc in zip(range(1, 7), [2.9, 2.6, 2.7, 3.2, 2.8, 2.7]):
    click(S[i] + tc)
    coin(S[i] + tc + 0.12)
levelup(27.75)
write(sys.argv[2], sfx)
print("ok")
