# Pasta with Claude (30 s, 9:16)

The guy asks Claude (the robot) how to make pasta. Claude gives real steps and roasts him at every one.

- `voice/script.json`: the dialogue (who, mood, text, optional pause). Rendering the script creates `voice/out/`, with the voiced lines, the lip-sync timeline and the caption timings. It is not committed.
- `index.html`: the 3D scene, step cards, captions and end card, all driven by `window.frame(i)`.
- `words.py`: caption phrases and word timings from Whisper. `cues.py`: derives every card, checklist, stamp and sound cue from the spoken words, so editing the script re-times everything. `mix.py`: dialogue, mandolin bed (dips under speech) and UI sounds.
- `render.mjs`: `still 1.2,10.6` for test frames, or `video` for all frames.

To rebuild, run `npm install` here and serve `/home/user` on port 8766. Then:
1. `python voices.py` (from the cast kit) on `voice/script.json`
2. `words.py`, `timeline.py` (cast kit), then `cues.py`
3. `mix.py`
4. `node render.mjs video`
5. Encode with ffmpeg
