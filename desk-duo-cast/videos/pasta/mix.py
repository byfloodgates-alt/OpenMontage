"""Mix: dialogue + procedural mandolin tarantella bed (ducked under speech) + UI sounds. -> out/mix.wav (48 kHz stereo)"""
import json, numpy as np, soundfile as sf
CUES = json.load(open('voice/out/cues.json')); EV = CUES['ev']
SR, TOTAL, END = 48000, CUES['total'], CUES['end']
rng = np.random.default_rng(7)
N = int(SR * TOTAL)
dlg, sr = sf.read('voice/out/dialogue.wav'); assert sr == SR
voice = np.zeros(N); voice[:min(N, len(dlg))] = dlg[:N]

# ---------- music: plucked strings (Karplus-Strong), A minor tarantella, 6/8 feel
def pluck(freq, dur, bright=0.5, amp=1.0):
    n = int(dur * SR); p = int(SR / freq)
    buf = rng.uniform(-1, 1, p) * amp
    out = np.empty(n); idx = 0
    damp = 0.996
    for i in range(n):
        v = buf[idx]; out[i] = v
        buf[idx] = damp * 0.5 * (v + buf[(idx + 1) % p]); idx = (idx + 1) % p
    env = np.exp(-np.linspace(0, dur * 3.2, n))
    return out * env
def note(m): return 440 * 2 ** ((m - 69) / 12)
eighth = 0.15   # 6/8 tarantella feel: six eighths per bar, ~133 bpm dotted-quarter pulse
chords = {  # midi notes (arpeggio pattern root-3rd-5th-octave-5th-3rd)
    'Am': [57, 60, 64, 69, 64, 60], 'Dm': [62, 65, 69, 74, 69, 65], 'E': [56, 59, 64, 68, 64, 59], 'C': [60, 64, 67, 72, 67, 64],
}
prog = ['Am', 'Am', 'Dm', 'Dm', 'E', 'E', 'Am', 'Am', 'C', 'C', 'Dm', 'E']
music = np.zeros(N + SR * 2)
t = 0.4; bar = 0
cache = {}
while t < END - 0.2:
    ch = chords[prog[bar % len(prog)]]
    for j, m in enumerate(ch):
        if t >= END - 0.2: break
        key = m
        if key not in cache: cache[key] = pluck(note(m), 0.9)
        x = cache[key] * (0.9 if j == 0 else 0.6) * (1 + 0.08 * rng.standard_normal())
        i0 = int(t * SR); music[i0:i0 + len(x)] += x
        # bass on the downbeat
        if j == 0:
            kb = ('b', m)
            if kb not in cache: cache[kb] = pluck(note(m - 12), 1.2) * 0.9
            xb = cache[kb]; music[i0:i0 + len(xb)] += xb
        t += eighth
    bar += 1
# final chord at the end card
for m in [45, 57, 60, 64, 69]:
    x = pluck(note(m), 2.0) * 0.8; i0 = int(END * SR); music[i0:i0 + len(x)] += x
music = music[:N]
music /= np.abs(music).max() + 1e-9

# ducking: follow the voice envelope
env = np.abs(voice)
win = int(0.12 * SR); k = np.ones(win) / win
env = np.convolve(env, k, 'same'); env = np.clip(env / (np.percentile(env, 98) + 1e-9), 0, 1)
env = np.convolve(env, np.ones(int(0.3 * SR)) / int(0.3 * SR), 'same')
duck = 1 - 0.65 * np.clip(env * 3, 0, 1)
music *= 0.16 * duck
# fade in, louder on the end card
tt = np.arange(N) / SR
music *= np.clip(tt / 0.6, 0, 1) * np.where(tt > END, 1.9, 1.0)

# ---------- UI sounds
sfx = np.zeros(N)
def put(x, t, g):
    i0 = int(t * SR); x = x[:max(0, N - i0)]; sfx[i0:i0 + len(x)] += x * g
def pop(f=900, d=0.07):
    n = int(d * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * (f + 600 * np.exp(-tt * 60)) * tt) * np.exp(-tt * 45)
def tick(f=1800):
    n = int(0.05 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.5 * tt)) * np.exp(-tt * 90)
def whoosh(d=0.35):
    n = int(d * SR); x = rng.standard_normal(n)
    x = np.convolve(x, np.ones(18) / 18, 'same'); e = np.sin(np.linspace(0, np.pi, n)) ** 2
    return x * e
def thump():
    n = int(0.25 * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * (70 + 80 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14) + 0.3 * rng.standard_normal(n) * np.exp(-tt * 60)
for _, a, _z in CUES['cards'][1:]: put(whoosh(), a - 0.12, 0.35)
for a, c in CUES['rows'].values(): put(pop(), a, 0.22)
for t in [EV['reply'], EV['comeback'], EV['whichsea']]: put(pop(700), t, 0.2)
for a, c in CUES['rows'].values():
    if c is not None: put(tick(), c, 0.16)
for j in range(int((EV['q1'] - EV['q0']) / 0.09)): put(tick(2600 + 300 * (j % 3)), EV['q0'] + j * 0.09, 0.07)   # typing
put(thump(), EV['stamp'] + 0.05, 0.5)                                         # IN TRAINING stamp
for j, f in enumerate([880, 1109, 1319]): put(pop(f, 0.35), EV['heart'] + 0.08 * j, 0.14)   # heart chime
put(whoosh(0.5), END - 0.15, 0.3)

mix = voice * 1.0 + music + sfx
mix = np.stack([mix + 0.02 * np.roll(music, 300), mix + 0.02 * np.roll(music, -300)], 1)
mix /= max(1.0, np.abs(mix).max() / 0.95)
import os; os.makedirs('out', exist_ok=True)
sf.write('out/mix.wav', mix, SR)
print('wrote out/mix.wav', mix.shape[0] / SR, 's')
