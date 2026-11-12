# uzun-video-isleme (Long video processing)

Turns hours-long recordings (live streams, lectures, orientation sessions, webinars, conferences), often in a foreign language, into a clear Turkish guide document without watching them end to end.

The rule is two channels, one truth: numbers, dates, amounts and addresses come only from the slides; the audio adds comments, tips, warnings and quotes. Anything uncertain is marked or left out.

Steps: probe the file and pull embedded subtitles if present; take frames at a fixed interval and build timestamped contact sheets (`scripts/kareler.py`); read the slides; transcribe only the sections that matter with sherpa-onnx and the Whisper base model (`scripts/transkript.py`, resumable, 28-second chunks); translate and synthesise; write the document with dated tasks first and an honesty note at the end.

Requirements: ffmpeg and ffprobe, Python 3, Pillow. For transcription (optional, install in a virtual environment after approval): sherpa-onnx (Apache-2.0), soundfile, and the sherpa-onnx Whisper base model from the sherpa-onnx GitHub releases (Whisper weights reported as MIT; check the licenses and the download size on the release page).

License: MIT, see LICENSE in the package root.
