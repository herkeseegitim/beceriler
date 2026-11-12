# eyes-video-kontrol (Video check with Eyes)

Lets Claude "watch" a video before delivery: frame sheets, a timestamped transcript, on-screen text and scene changes via Eyes, plus two small checks that work on their own:

- `scripts/teslim_kontrol.py`: size, frame rate, codec, duration, loudness (-14 LUFS, true peak -1 dBTP), black frames, freezes, silence, and a safe-area preview image for Shorts/Reels. Uses only ffmpeg/ffprobe, no network.
- `scripts/srt_denetim.py`: subtitle file check (line length, max two lines, overlaps, minimum 0.8 s on screen, reading speed 17 chars/s for Turkish). Standard library only.

The skill also gives a three-distance review method (contact sheet, strip, contact crop) and a pre-delivery checklist.

Requirements: ffmpeg and ffprobe, Python 3. Optional: Eyes (github.com/moritzkremb/claude-eyes, reported as MIT, check the license), whisper.cpp (MIT), the ggml-large-v3-turbo-q5_0 model (574,041,195 bytes, from the whisper.cpp model repository on Hugging Face; check the license). Every install step is optional and needs explicit approval at the time.

Method credits: kajisho5/ffmpeg-skill and kajisho5/subtitle-skill (reported as MIT, methods only), ClaudeAnimationBase review loop (method only, check the license). The scripts here are original.

License: MIT, see LICENSE in the package root.
