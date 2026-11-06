"""Render dialogue in the desk-duo voices.

  ~/lemo-opuscar/.venv/bin/python voices.py script.json out_dir

script.json = [{"id": "01", "who": "host"|"bot", "text": "...", "mood": "calm"}, ...]
  optional per line: "voice" (override the cast voice), "speed", "pitch" (semitones)
Writes out_dir/<id>.wav (48 kHz mono, effects applied, level-matched), out_dir/lines.json (with durations and
start times) and out_dir/dialogue.wav (all lines placed at their start times). Optional per line: 'pause' (extra seconds before it),
'say' (spelling sent to the voice when it differs from the caption text, e.g. "Clawd" for Claude).
Cast settings live in cast.json next to this file.
"""
import sys, os, json, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.environ.get('LIB', os.path.expanduser('~/lemo-opuscar'))
PY = os.path.join(LIB, '.venv/bin/python')

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"failed: {' '.join(cmd[:3])}…\n{r.stderr[-1500:]}")
    return r.stdout

def main():
    if len(sys.argv) < 3: print(__doc__); sys.exit(2)
    script, out = json.load(open(sys.argv[1])), sys.argv[2]
    cast = json.load(open(os.path.join(HERE, 'cast.json')))
    os.makedirs(out, exist_ok=True)
    raw = tempfile.mkdtemp(prefix='tts_')
    tts_lines = []
    for L in script:
        c = cast[L['who']]; m = c['moods'].get(L.get('mood', 'calm'), c['moods']['calm'])
        tts_lines.append({'id': L['id'], 'text': L.get('say', L['text']), 'voice': L.get('voice', c['voice']),
                          'speed': L.get('speed', m['speed'])})
    json.dump(tts_lines, open(os.path.join(raw, 'in.json'), 'w'))
    run([PY, '-I', os.path.join(LIB, 'core/tts/tts.py'), os.path.join(raw, 'in.json'), raw])
    import numpy as np, soundfile as sf
    result, t = [], 0.0
    for i, L in enumerate(script):
        c = cast[L['who']]; m = c['moods'].get(L.get('mood', 'calm'), c['moods']['calm'])
        semis = L.get('pitch', m.get('pitch', 0))
        chain = []
        if semis: chain.append(f"rubberband=pitch={2 ** (semis / 12):.5f}:formant=preserved:pitchq=quality")
        if c.get('fx'): chain.append(c['fx'])
        dst = os.path.join(out, f"{L['id']}.wav")
        run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(raw, f"{L['id']}.wav"), *(['-af', ','.join(chain)] if chain else []),
             '-ar', '48000', '-ac', '1', dst])
        # level-match: voiced RMS to -20 dBFS, peaks below -1 dBFS (no dynamic loudness filter on short lines)
        x, sr = sf.read(dst)
        fr = x[: len(x) // 480 * 480].reshape(-1, 480); rms = np.sqrt((fr ** 2).mean(1))
        voiced = rms[rms > rms.max() * 0.1]
        g = 10 ** (-20 / 20) / (np.sqrt((voiced ** 2).mean()) + 1e-9)
        x = x * min(g, 0.89 / (np.abs(x).max() + 1e-9))
        sf.write(dst, x, sr, subtype='PCM_16')
        dur = len(x) / sr
        # timing: 0.3 s between speakers, 0.12 s when the same speaker continues, plus an optional "pause" before the line
        t += (0.12 if i and script[i - 1]['who'] == L['who'] else 0.3) + L.get('pause', 0)
        result.append({**L, 'file': f"{L['id']}.wav", 'dur': round(dur, 3), 'start': round(t, 3)}); t += dur
        print(f"{L['id']:>6} {L['who']:4} {L.get('mood', 'calm'):8} {result[-1]['start']:6.2f}s +{dur:4.2f}s  {L['text']}")
    json.dump(result, open(os.path.join(out, 'lines.json'), 'w'), indent=1)
    reel = np.zeros(int((t + 0.5) * 48000))
    for r in result:
        x, _ = sf.read(os.path.join(out, r['file'])); i0 = int(r['start'] * 48000); reel[i0:i0 + len(x)] += x
    sf.write(os.path.join(out, 'dialogue.wav'), reel, 48000, subtype='PCM_16')
    print('wrote', os.path.join(out, 'dialogue.wav'), f'({t:.2f}s of speech)')

main()
