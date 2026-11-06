"""Caption phrases with timings: places lines like timeline.py, times words with Whisper, groups into short phrases."""
import json, os, re, sys
from faster_whisper import WhisperModel
out = 'voice/out'
lines = json.load(open(f'{out}/lines.json'))
m = WhisperModel('base.en', device='cpu', compute_type='int8')
t, phrases = 0.0, []
for i, L in enumerate(lines):
    t += 0.15 if i and lines[i-1]['who'] == L['who'] else 0.35
    start = t; t += L['dur']
    toks = L['text'].split()
    segs, _ = m.transcribe(f"{out}/{L['file']}", word_timestamps=True)
    ws = [w for s in segs for w in (s.words or [])]
    if len(ws) == len(toks):
        times = [(w.start, w.end) for w in ws]
    else:   # spread by character count between first and last recognised word
        a, b = (ws[0].start, ws[-1].end) if ws else (0, L['dur'])
        tot = sum(len(x) + 1 for x in toks); acc = 0; times = []
        for x in toks:
            s0 = a + (b - a) * acc / tot; acc += len(x) + 1; times.append((s0, a + (b - a) * acc / tot))
    # group: whole sentences when <= 5 words, else split into balanced halves (no one-word tails)
    sent, sents = [], []
    for tok, (s0, s1) in zip(toks, times):
        sent.append((tok, s0, s1))
        if re.search(r'[.!?]$', tok): sents.append(sent); sent = []
    if sent: sents.append(sent)
    for sn in sents:
        n = len(sn); k = 1 if n <= 5 else (n + 4) // 5
        size = -(-n // k)
        for j in range(0, n, size):
            cur = sn[j:j + size]
            phrases.append({'who': L['who'], 'line': L['id'], 'text': ' '.join(c[0] for c in cur),
                            't0': round(start + cur[0][1], 3), 't1': round(start + cur[-1][2], 3)})
lineTimes = []
t = 0.0
for i, L in enumerate(lines):
    t += 0.15 if i and lines[i-1]['who'] == L['who'] else 0.35
    lineTimes.append({'id': L['id'], 'who': L['who'], 't0': round(t, 3), 't1': round(t + L['dur'], 3)}); t += L['dur']
json.dump({'phrases': phrases, 'lines': lineTimes, 'speechEnd': round(t, 3)}, open(f'{out}/captions.json', 'w'), indent=1)
for p in phrases: print(f"{p['t0']:6.2f}-{p['t1']:6.2f} {p['who']:4} {p['text']}")
