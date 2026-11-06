"""Derive every visual/sound cue from the spoken words, so a script change re-times the whole video.
Reads voice/out/captions.json, writes voice/out/cues.json (used by index.html and mix.py)."""
import json, re
C = json.load(open('voice/out/captions.json'))
W = C['words']; L = {l['id']: l for l in C['lines']}
norm = lambda s: re.sub(r"[^a-z0-9']", '', s.lower())

def at(phrase, line=None, edge='t0'):
    """Time of the first occurrence of a word sequence (optionally within one line)."""
    toks = [norm(t) for t in phrase.split()]
    ws = [w for w in W if line is None or w['line'] == line]
    for i in range(len(ws) - len(toks) + 1):
        if all(norm(ws[i + j]['w']) == toks[j] for j in range(len(toks))):
            return ws[i][edge] if edge == 't0' else ws[i + len(toks) - 1]['t1']
    raise SystemExit(f'cue not found: "{phrase}" in line {line}')

speech_end = C['speechEnd']
end = round(speech_end + 0.4, 2)
total = round(end + 1.9, 2)
cards = [['c0', 0.0, L['04']['t0'] - 0.3], ['c1', L['04']['t0'] - 0.3, L['06']['t0'] - 0.25],
         ['c2', L['06']['t0'] - 0.25, L['07']['t0'] - 0.2], ['c3', L['07']['t0'] - 0.2, L['09']['t0'] - 0.25],
         ['c4', L['09']['t0'] - 0.25, end]]
rows = {
    'pot': [at('Big pot'), at('Big pot', edge='t1') + 0.3], 'water': [at('of water'), at('of water', edge='t1') + 0.4],
    'salt': [at('Salt it'), at('the sea', '04', 't1')],
    'anysea': [at('Literally'), at('any sea', '06', 't1')], 'pastain': [at('Pasta in'), at('Pasta in', edge='t1')],
    'stir': [at('stir'), at('stir', edge='t1') + 0.2], 'taste': [at('Taste one'), at("don't guess", edge='t1')],
    'cup': [at('Save a cup'), at('pasta water', '08', 't1')], 'butter': [at('Butter'), at('Butter', edge='t1')],
    'parm': [at('parmesan'), at('parmesan', edge='t1')], 'toss': [at('toss it'), at('the pan', edge='t1')],
    'chef': [L['09']['t0'] + 0.1, None],
}
ev = {
    'q0': L['01']['t0'] + 0.1, 'q1': at('pasta', '01', 't1'),          # user question types out
    'reply': L['02']['t0'], 'comeback': L['03']['t0'],                    # chat bubbles
    'whichsea': L['05']['t0'], 'timer': [at('about ten'), at('minutes', '06', 't1') + 0.4],
    'boil': at('Salt it'), 'fill': [at('Big pot'), at('of water', edge='t1') + 0.6],
    'stamp': at('You boiled'), 'heart': at('Proud'),
}
sass = [[0, 0], [L['02']['t0'] + 0.6, 35], [at('the sea', '04', 't1'), 50], [L['06']['t0'] + 0.4, 64],
        [L['10']['t0'] + 0.4, 96], [at('Proud') + 0.2, 12]]
# who reacts when (host faces; robot smiles while teasing, never squints)
react = {
    'host': [[at('four hundred'), L['02']['t1'] + 0.6, {'brows': -0.4, 'browTilt': 1}],
             [L['10']['t0'], at('Proud') - 0.1, {'brows': -0.8, 'smile': -0.4}],
             [at('Proud'), total, {'smile': 1, 'brows': 0.5}]],
    'bot': [[L['03']['t0'], L['03']['t1'] + 0.4, 'happy'], [L['05']['t0'], L['05']['t1'] + 0.3, 'happy'],
            [L['09']['t0'], L['09']['t1'] + 0.2, 'happy'], [at('Proud'), total, 'happy']],
}
json.dump({'total': total, 'end': end, 'speechEnd': speech_end, 'cards': cards, 'rows': rows, 'ev': ev, 'sass': sass, 'react': react},
          open('voice/out/cues.json', 'w'), indent=1)
print(f'total {total}s, end card at {end}s'); [print(f'  {k:8s} {v}') for k, v in rows.items()]; print('  ', ev)
