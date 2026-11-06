"""Original dark-electronic bed + transition FX for the Floodgates promo (deterministic).
Usage: music.py bed.wav fx.wav"""
import sys, wave
import numpy as np

SR = 44100
DUR = 30.5
BPM = 100
B = 60 / BPM
rng = np.random.default_rng(11)
S = [0, 4.2, 9.2, 14.6, 18.6, 22.4]
GATE_OPEN = 1.5

def buf():
    return np.zeros((int(SR * DUR) + SR, 2))

def f(n):
    return 440.0 * 2 ** ((n - 69) / 12)

def put(tr, sig, t, g, pan=0.0):
    i = int(t * SR)
    if sig.ndim == 1:
        sig = np.stack([sig * (1 - max(0, pan)), sig * (1 + min(0, pan))], 1)
    seg = sig[: len(tr) - i]
    tr[i : i + len(seg)] += seg * g

def lowpass(x, a):
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += a * (x[i] - acc); y[i] = acc
    return y

def write(path, x):
    x = x[: int(SR * DUR)]
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.85
    pcm = (x * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())

def saw_pad(notes, dur):
    n = int(SR * dur); t = np.arange(n) / SR
    out = np.zeros(n)
    for note in notes:
        for det in (-0.08, 0.0, 0.08):
            fr = f(note + det)
            out += 2 * ((t * fr) % 1) - 1
    e = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.6)
    return lowpass(out * e / (len(notes) * 3), 0.06)

bed = buf()
chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
roots = [33, 29, 36, 31]
bar = 4 * B
# pads (chords change every bar)
t, k = 0.0, 0
while t < DUR:
    pad = saw_pad(chords[k % 4], bar + 0.6)
    put(bed, pad, t, 0.5, pan=-0.2)
    put(bed, pad, t + 0.01, 0.5, pan=0.2)
    t += bar; k += 1

# rhythm section starts when the gates open
t0 = GATE_OPEN
nb = int((DUR - t0) / (B / 2))
for j in range(nb):
    st = t0 + j * B / 2
    ch = int((st) / bar) % 4
    # pulsing sub bass on 8ths
    n = int(SR * B / 2 * 0.9); tt = np.arange(n) / SR
    sub = np.sin(2 * np.pi * f(roots[ch]) * tt) * np.exp(-tt * 6)
    put(bed, sub, st, 0.55)
    # hats
    h = np.diff(rng.uniform(-1, 1, int(0.03 * SR)) * np.exp(-np.linspace(0, 9, int(0.03 * SR))), prepend=0)
    put(bed, h, st + B / 4, 0.12, pan=0.3)
    if j % 2 == 0:  # kick on beats
        n = int(SR * 0.18); tt = np.arange(n) / SR
        kick = np.sin(2 * np.pi * (45 + 110 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14)
        put(bed, kick, st, 0.8)
    if j % 4 == 2:  # clap on 2 and 4
        c = rng.uniform(-1, 1, int(0.12 * SR)) * np.exp(-np.linspace(0, 10, int(0.12 * SR)))
        put(bed, lowpass(c, 0.5), st, 0.25)
# sparkly pluck arp from scene 2 onward
arp = [69, 72, 76, 79, 76, 72]
j = 0; st = S[1]
while st < DUR - 1:
    ch = int(st / bar) % 4
    base = chords[ch]
    note = [base[0] + 12, base[1] + 12, base[2] + 12, base[0] + 24][j % 4]
    n = int(SR * 0.25); tt = np.arange(n) / SR
    pl = (np.sin(2 * np.pi * f(note) * tt) + 0.3 * np.sin(4 * np.pi * f(note) * tt)) * np.exp(-tt * 12)
    put(bed, pl, st, 0.12, pan=0.4 if j % 2 else -0.4)
    st += B / 2; j += 1
fo = int(1.5 * SR); end = int(SR * DUR)
bed[end - fo : end] *= np.linspace(1, 0, fo)[:, None]
write(sys.argv[1], bed)

# ---------- FX ----------
fx = buf()
def riser(t_end, dur):
    n = int(SR * dur); x = rng.uniform(-1, 1, n)
    y = np.zeros(n); acc = 0.0
    for i in range(n):
        a = 0.02 + 0.5 * (i / n) ** 2
        acc += a * (x[i] - acc); y[i] = acc
    put(fx, y * np.linspace(0, 1, n) ** 2, t_end - dur, 0.5)
def impact(t):
    n = int(SR * 1.2); tt = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (38 + 60 * np.exp(-tt * 8)) * tt) * np.exp(-tt * 3)
    noise = lowpass(rng.uniform(-1, 1, n), 0.2) * np.exp(-tt * 5)
    put(fx, boom + 0.5 * noise, t, 0.9)
def whoosh(t):
    n = int(SR * 0.45); x = rng.uniform(-1, 1, n)
    e = np.sin(np.linspace(0, np.pi, n)) ** 2
    put(fx, lowpass(x, 0.25) * e, t - 0.2, 0.45)
def ping(t):
    n = int(SR * 0.6); tt = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f(88) * tt) + 0.5 * np.sin(2 * np.pi * f(95) * tt)) * np.exp(-tt * 6)
    put(fx, s, t, 0.25)

riser(GATE_OPEN, 1.2)
impact(GATE_OPEN)
for s in S[1:]:
    whoosh(s)
ping(S[4] + 0.6); ping(S[4] + 1.0)
riser(S[5] + 0.1, 0.8); impact(S[5] + 0.1)
write(sys.argv[2], fx)
print("ok")
