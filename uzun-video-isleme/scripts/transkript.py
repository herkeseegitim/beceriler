#!/usr/bin/env python3
"""Kaldığı yerden devam eden bölütlü transkripsiyon: sherpa-onnx + Whisper.
Kullanım:
  1) SEGMENTS listesini düzenleyin: (ad, baslangic_sn, bitis_sn)
  2) Dili LANG_CODE ile verin (tr, en, de, fr ...)
  3) Arka planda başlatın:
     VID="video.mp4" LANG_CODE=en nohup python3 transkript.py > tr.log 2>&1 &
  4) İlerleme: cat progress.log ; wc -l tr_*.txt
  Süreç durursa aynı komutla yeniden başlatın; kaldığı satırdan devam eder."""
import sherpa_onnx, soundfile as sf, subprocess, time, os

VID = os.environ["VID"]
LANG = os.environ.get("LANG_CODE", "tr")
MODEL = os.environ.get("MODEL_DIR", "sherpa-onnx-whisper-base")
PREFIX = MODEL.rstrip("/").split("whisper-")[-1]
SEGMENTS = [
    # ("bolum_adi", baslangic_saniye, bitis_saniye),
    ("ornek", 0, 600),
]

rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=f"{MODEL}/{PREFIX}-encoder.int8.onnx",
    decoder=f"{MODEL}/{PREFIX}-decoder.int8.onnx",
    tokens=f"{MODEL}/{PREFIX}-tokens.txt",
    language=LANG, task="transcribe", num_threads=1)

for name, start, end in SEGMENTS:
    txt = f"tr_{name}.txt"
    done = sum(1 for _ in open(txt, encoding="utf-8")) if os.path.exists(txt) else 0
    wavf = f"seg_{name}.wav"
    if not os.path.exists(wavf) or os.path.getsize(wavf) < (end - start) * 16000 * 2 - 100000:
        subprocess.run(["ffmpeg", "-ss", str(start), "-t", str(end - start), "-i", VID,
                        "-ac", "1", "-ar", "16000", wavf, "-y", "-loglevel", "error"], check=True)
    wav, sr = sf.read(wavf, dtype="float32")
    step = 28 * sr
    with open(txt, "a", encoding="utf-8") as f:
        for ci, i in enumerate(range(0, len(wav), step)):
            if ci < done:
                continue
            chunk = wav[i:i + 29 * sr]
            s = rec.create_stream(); s.accept_waveform(sr, chunk)
            rec.decode_stream(s)
            ts = start + i // sr
            f.write(f"[{ts//3600}:{(ts%3600)//60:02d}:{ts%60:02d}] {s.result.text}\n")
            f.flush()
    # Geçici ses dosyası bu betiğin kendi ürettiği dosyadır; bölüm bitince kaldırılır.
    os.remove(wavf)
    with open("progress.log", "a", encoding="utf-8") as p:
        p.write(f"{name} bitti {time.strftime('%H:%M:%S')}\n")
with open("progress.log", "a", encoding="utf-8") as p:
    p.write("HEPSİ BİTTİ\n")
