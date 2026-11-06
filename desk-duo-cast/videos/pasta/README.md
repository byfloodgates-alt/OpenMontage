# Pasta with Claude (30 s, 9:16)

The guy asks Claude (the robot) how to make pasta. Claude gives real steps and roasts him at every one.

- `voice/script.json`: the dialogue (who, mood, text). `voice/out/` holds the voiced lines, the lip-sync timeline and the caption timings.
- `index.html`: the 3D scene, step cards, captions and end card, all driven by `window.frame(i)`.
- `words.py`: caption phrases from Whisper word timings. `mix.py`: dialogue, mandolin bed (dips under speech) and UI sounds.
- `render.mjs`: `still 1.2,10.6` for test frames, or `video` for all frames.

To rebuild, run `npm install` here and serve `/home/user` on port 8766. Then:
1. `python voices.py` (from the cast kit) on `voice/script.json`
2. `words.py`, then `timeline.py` (cast kit)
3. `mix.py`
4. `node render.mjs video`
5. Encode with ffmpeg
