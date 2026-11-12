# Herkese Eğitim skills v1

Three free skills for Claude, written in Turkish, for teachers who make short videos or need notes from long recordings. Each skill folder has a short English summary (`README.en.md`).

| Skill | What it does |
|---|---|
| `iki-hal-dugmesi` | A 24-second vertical video format: a small world inside an on/off toggle, one click between two states. Includes working starter code. |
| `eyes-video-kontrol` | Checks a video before delivery: size, loudness, frozen and black frames, safe area, subtitle file. With Eyes installed, also frame sheets, transcript and on-screen text. |
| `uzun-video-isleme` | Turns hours-long webinars, lectures or conference recordings into a Turkish guide document from slides and speech. |

## Install

### Claude Code
Copy each skill folder as it is into your skills folder:

```
~/.claude/skills/iki-hal-dugmesi/
~/.claude/skills/eyes-video-kontrol/
~/.claude/skills/uzun-video-isleme/
```

On Windows the same place is `%USERPROFILE%\.claude\skills\`. For a single project, use `.claude/skills/` inside the project folder. Restart Claude Code.

### claude.ai
Zip each skill separately (the zip holds the skill folder with `SKILL.md` inside), then upload it from the skills section in Settings. Menu names may change between versions. Code execution must be on.

## Requirements

| Skill | Required | Optional |
|---|---|---|
| iki-hal-dugmesi | Python 3, ffmpeg | Playwright with Chromium (to render video) |
| eyes-video-kontrol | Python 3, ffmpeg, ffprobe | Eyes (reported as MIT), whisper.cpp (MIT), ggml-large-v3-turbo-q5_0 model (574,041,195 bytes, whisper.cpp model repository) |
| uzun-video-isleme | Python 3, ffmpeg, ffprobe, Pillow | sherpa-onnx (Apache-2.0), soundfile, sherpa-onnx Whisper base model (GitHub Releases; size on the release page) |

Optional installs download code and models from outside sources. Use a separate virtual environment and look at each step before running it. Check third-party licenses yourself; this package does not include them.

None of these skills publishes or uploads anything on its own; they only delete temporary files they created themselves. The rule when working with Claude: get explicit approval at the time for every step that cannot be undone.

## Example prompts

- "Check this video before delivery: kisa_video.mp4"
- "Does this .srt file have overlaps or reading-speed problems?"
- "Summarise this three-hour webinar and put dated tasks first."
- "Make a two-state toggle video that goes from an empty board to a finished lesson."

## Examples and credits

Product names (ÇizTahta, YazTahta) and colours in the skills are examples from Herkese Eğitim; replace them with your own. Credits are written inside each skill: Eyes (Moritz Kremb), kajisho5/ffmpeg-skill and kajisho5/subtitle-skill (methods only), ClaudeAnimationBase (method only), and the X account Lattice_Node for the toggle idea.

## License

MIT, for code and text. See `LICENSE`. Copyright: Herkese Eğitim.
