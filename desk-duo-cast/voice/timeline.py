"""Turn a voices.py output folder into a lip-sync timeline for the 3D scene.

  ~/lemo-opuscar/.venv/bin/python timeline.py out_dir [fps]

Reads out_dir/lines.json + the wavs, places lines with the same gaps as dialogue.wav,
and writes out_dir/timeline.json: per frame, each character's mouth opening (0..1) and who is speaking.
"""
import sys, os, json, numpy as np, soundfile as sf
out = sys.argv[1]; fps = int(sys.argv[2]) if len(sys.argv) > 2 else 30
lines = json.load(open(os.path.join(out, 'lines.json')))
t, placed = 0.0, []
for i, L in enumerate(lines):
    t += 0.15 if i and lines[i - 1]['who'] == L['who'] else 0.35
    placed.append((t, L)); t += L['dur']
total = t + 0.8
n = int(total * fps)
frames = [{'host': 0.0, 'bot': 0.0, 'speaker': None, 'hostMood': 'calm', 'botMood': 'calm'} for _ in range(n)]
for start, L in placed:
    x, sr = sf.read(os.path.join(out, L['file']))
    hop = sr // fps
    env = np.array([np.sqrt(np.mean(x[k:k + hop] ** 2)) for k in range(0, len(x), hop)])
    env = np.clip((env / (np.percentile(env, 95) + 1e-9)) ** 0.7, 0, 1)
    env = np.convolve(env, [0.25, 0.5, 0.25], 'same')            # soften the flapping
    f0 = int(start * fps)
    for k, v in enumerate(env):
        if f0 + k < n:
            fr = frames[f0 + k]; fr[L['who']] = float(round(v, 3)); fr['speaker'] = L['who']
    # mood holds from this line until the same character speaks again
    for k in range(f0, n): frames[k][L['who'] + 'Mood'] = L.get('mood', 'calm')
json.dump({'fps': fps, 'frames': frames}, open(os.path.join(out, 'timeline.json'), 'w'))
print(f'{n} frames, {total:.2f}s ->', os.path.join(out, 'timeline.json'))
