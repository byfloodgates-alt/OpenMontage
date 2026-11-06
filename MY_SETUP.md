# My OpenMontage setup

My personal fork of [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage).

## Default style
- **Playbook:** `styles/blocky-game.yaml`. This is a blocky, game-inspired quest look: a quest bar with XP, an original blocky chef avatar, chat-bubble captions, chiptune music and game sound effects. It is original art, with no real game's logos, avatars, fonts or sounds.
- New videos use this style unless I ask for something else.

## Voice
- **Current:** Piper (free, offline). The model is `en_US-ryan-high` with `length_scale` 0.86 and `sentence_silence` 0.12, then pitched up 2 semitones (`rubberband=pitch=1.12246`), with a +3 dB boost at 3 kHz and loudness normalised to -16 LUFS.
- **Later:** this will be replaced with my own recorded or cloned voice (ElevenLabs, Fish Audio or HeyGen). API keys go in the cloud environment settings, never in this repo.

## Saved projects
- `projects/how-to-make-pasta/`: the original illustrated kitchen version.
- `projects/pasta-quest-blocky/`: the blocky game version.

Each project folder contains:
- `hyperframes/index.html`: the composition.
- `hyperframes/assets/`: the fonts, GSAP and the final audio mix.
- `renders/final.mp4`: the finished video.
- `scripts/`: the generator, music and sound-effect scripts, plus the narration text and timings.

## Setting up a new session
1. Install everything with `make setup`.
2. Put `.venv/bin` on `PATH` so OpenMontage can find Piper.
3. Download the Piper voices into `~/.piper/models`. This needs `huggingface.co` and `us.aws.cdn.hf.co` on the environment's allowed hosts:
   - `python -m piper.download_voices en_US-ryan-high`
   - `python -m piper.download_voices en_US-lessac-medium`
4. Re-render a project from its `hyperframes/` folder. First create a local `package.json` with a name other than `hyperframes` (the name must differ or `npx` breaks), then run `npm i gsap@3.14.2` and `npx hyperframes render -o ../renders/final.mp4`.
