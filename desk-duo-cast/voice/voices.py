"""Render dialogue in the desk-duo voices.

  ~/lemo-opuscar/.venv/bin/python voices.py script.json out_dir

script.json = [{"id": "01", "who": "host"|"bot", "text": "...", "mood": "calm"}, ...]
  optional per line: "voice" (override the cast voice), "speed", "pitch" (semitones)
Writes out_dir/<id>.wav (48 kHz mono, effects applied), out_dir/lines.json (with durations)
and out_dir/dialogue.wav (all lines in order with natural gaps), for a quick listen.
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
        tts_lines.append({'id': L['id'], 'text': L['text'], 'voice': L.get('voice', c['voice']),
                          'speed': L.get('speed', m['speed'])})
    json.dump(tts_lines, open(os.path.join(raw, 'in.json'), 'w'))
    run([PY, '-I', os.path.join(LIB, 'core/tts/tts.py'), os.path.join(raw, 'in.json'), raw])
    result = []
    for L in script:
        c = cast[L['who']]; m = c['moods'].get(L.get('mood', 'calm'), c['moods']['calm'])
        semis = L.get('pitch', m['pitch'])
        chain = []
        if semis: chain.append(f"rubberband=pitch={2 ** (semis / 12):.5f}:formant=preserved:pitchq=quality")
        chain.append(c['fx'])
        chain.append('loudnorm=I=-16:TP=-1.5:LRA=7')
        dst = os.path.join(out, f"{L['id']}.wav")
        run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(raw, f"{L['id']}.wav"), '-af', ','.join(chain), '-ar', '48000', '-ac', '1', dst])
        dur = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', dst]))
        result.append({**L, 'file': f"{L['id']}.wav", 'dur': round(dur, 3)})
        print(f"{L['id']:>6} {L['who']:4} {L.get('mood', 'calm'):8} {dur:5.2f}s  {L['text']}")
    json.dump(result, open(os.path.join(out, 'lines.json'), 'w'), indent=1)
    # quick-listen reel: 0.35 s between lines, 0.15 s when the same speaker continues
    inputs, parts = [], []
    for i, r in enumerate(result):
        inputs += ['-i', os.path.join(out, r['file'])]
        gap = 0.15 if i and result[i - 1]['who'] == r['who'] else 0.35
        parts.append(f"[{i}]adelay={int(gap * 1000)}:all=1[a{i}]")
    filt = ';'.join(parts) + ';' + ''.join(f"[a{i}]" for i in range(len(result))) + f"concat=n={len(result)}:v=0:a=1[o]"
    run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', filt, '-map', '[o]', os.path.join(out, 'dialogue.wav')])
    print('wrote', os.path.join(out, 'dialogue.wav'))

main()
