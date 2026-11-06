# Desk Duo cast kit

The two recurring characters for the vertical promo style: **the host** (seated man, teal hoodie) and **the bot** (red screen-faced robot on a desk stand), plus their voices. Use them in every video.

## Characters: `characters.js`
- `createHost(THREE)` and `createBot(THREE, { stand })` return `{ root, update(state) }`. All colours are in `PALETTE`.
- Host state: `talk`, `smile`, `brows`, `browTilt`, `look:[x,y]`, `blink`, `headTurn/Tilt/Nod`, `lean`, `breathe`, `armL/armR: {raise, out, bend}`.
- Bot state: `t`, `talk` (drives the waveform mouth), `mood` (`neutral|happy|squint|wide|sad`), `look`, `blink`, `headTurn/Tilt/Nod`.
- `addWarmLights(THREE, scene)`: the shared warm room lighting.

## Voices: `voice/`
- `cast.json`: the host uses Kokoro `am_puck` and the bot `am_michael` (two of the voices Kokoro rates best). There is no pitch shifting or echo, only light cleanup; moods change the speaking speed.
- To use ElevenLabs instead of the offline voices, set `"engine": "elevenlabs"` in `cast.json`. It needs an API key, either saved for `api.elevenlabs.io` (header `xi-api-key`) in the cloud environment's Network secrets or set as `ELEVENLABS_API_KEY`. Change the voices under each character's `elevenlabs.voice_id`.
- `voices.py script.json out_dir` renders each line and writes `lines.json` and a `dialogue.wav` reel.
- `timeline.py out_dir` builds per-frame lip-sync data.

## Previews
- `node shoot.mjs turnaround|expressions|scene out.png [w h]` renders still sheets.
- `node animate.mjs voice/preview preview.mp4` renders a lip-synced clip.

Run both with `python3 -m http.server 8765` running in this folder, and `NODE_PATH=$(npm root -g)` set.

## Starting again in a new session
1. Install the plugin:
   - `claude plugin marketplace add lemomo-ai/lemo-opuscar`
   - `claude plugin install lemo-opuscar@lemolab`
2. Get the style library and the voice tools: `sh <plugin>/skills/lemo-opuscar/scripts/setup.sh deps voice`. This puts the library in `~/lemo-opuscar`.
3. Run `npm install` in this folder.
4. Ask Claude for a vertical promo with the Desk Duo cast, on your topic, pointing it at this folder.

Notes:
- If a Whisper model download fails behind a proxy, set `HF_HUB_DISABLE_XET=1`.
- The full style-library render pipeline needs ffmpeg 7 or newer. The kit's own scripts work with ffmpeg 6, which has the `rubberband` filter.
