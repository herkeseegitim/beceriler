#!/usr/bin/env python3
"""baslangic.html sayfasını kare kare kaydedip dikey MP4 yapar (MIT, Herkese Eğitim).

Kullanım:
  python3 kaydet.py baslangic.html cikti.mp4 [--fps 60] [--sure 24] [--muzik muzik.wav]

Gereken: Python 3, Playwright (Chromium ile), ffmpeg. Ağ çağrısı yapmaz;
sayfa yerel dosyadan açılır. Kareler çıktı dosyasının yanındaki geçici klasöre yazılır."""
import argparse, base64, os, subprocess, sys, tempfile
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("sayfa"); ap.add_argument("cikti")
ap.add_argument("--fps", type=int, default=60)
ap.add_argument("--sure", type=float, default=None, help="saniye; boşsa sayfadaki DURATION")
ap.add_argument("--muzik", default=None)
a = ap.parse_args()

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Playwright yok. Kurulum ornek/NASIL.md içinde (isteğe bağlı adım).")

sayfa = Path(a.sayfa).resolve()
cikti = Path(a.cikti).resolve()
kare_dir = Path(tempfile.mkdtemp(prefix="kareler_", dir=cikti.parent))

with sync_playwright() as p:
    tr = p.chromium.launch()
    pg = tr.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto(sayfa.as_uri() + "?kayit=1")
    sure = a.sure or pg.evaluate("window.DURATION")
    n = int(round(sure * a.fps))
    for i in range(n):
        url = pg.evaluate("t => { render(t); return document.getElementById('c').toDataURL('image/png'); }", i / a.fps)
        (kare_dir / f"f_{i:05d}.png").write_bytes(base64.b64decode(url.split(",", 1)[1]))
        if i % a.fps == 0:
            print(f"{i // a.fps} / {int(sure)} sn", flush=True)
    tr.close()

cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(a.fps), "-i", str(kare_dir / "f_%05d.png")]
if a.muzik:
    cmd += ["-i", a.muzik, "-c:a", "aac", "-b:a", "192k", "-shortest"]
cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", str(cikti)]
subprocess.run(cmd, check=True)
print("Hazır:", cikti)
print("Kareler burada duruyor, işiniz bitince kendiniz silebilirsiniz:", kare_dir)
