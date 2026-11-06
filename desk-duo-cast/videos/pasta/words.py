"""Caption phrases with timings: places lines like timeline.py, times words with Whisper, groups into short phrases."""
import json, os, re, sys
from faster_whisper import WhisperModel
out = 'voice/out'
lines = json.load(open(f'{out}/lines.json'))
m = WhisperModel('base.en', device='cpu', compute_type='int8')
phrases, words = [], []
for i, L in enumerate(lines):
    start = L['start']
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
    words += [{'w': tok, 't0': round(start + a, 3), 't1': round(start + b, 3), 'line': L['id']} for tok, (a, b) in zip(toks, times)]
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
lineTimes = [{'id': L['id'], 'who': L['who'], 't0': L['start'], 't1': round(L['start'] + L['dur'], 3)} for L in lines]
t = lines[-1]['start'] + lines[-1]['dur']
json.dump({'phrases': phrases, 'words': words, 'lines': lineTimes, 'speechEnd': round(t, 3)}, open(f'{out}/captions.json', 'w'), indent=1)
for p in phrases: print(f"{p['t0']:6.2f}-{p['t1']:6.2f} {p['who']:4} {p['text']}")
