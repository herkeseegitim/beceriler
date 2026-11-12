#!/usr/bin/env python3
"""Videodan düzenli kare çekip zaman damgalı kontakt sayfaları üretir.
Kullanım: python3 kareler.py VIDEO.mp4 [aralik_saniye] [cikti_klasoru]
Gereken: ffmpeg, ffprobe, Pillow. Ağ çağrısı yok. Lisans: MIT (Herkese Eğitim)."""
import subprocess, sys, os, glob
from PIL import Image, ImageDraw

vid = sys.argv[1]
step = int(sys.argv[2]) if len(sys.argv) > 2 else 180
out = sys.argv[3] if len(sys.argv) > 3 else "frames"
os.makedirs(out, exist_ok=True); os.makedirs(out + "_sheets", exist_ok=True)

dur = float(subprocess.check_output(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "csv=p=0", vid]).strip())
for t in range(0, int(dur), step):
    subprocess.run(["ffmpeg", "-ss", str(t), "-i", vid, "-frames:v", "1",
                    "-q:v", "3", f"{out}/f_{t:06d}.jpg", "-y", "-loglevel", "error"])

files = sorted(glob.glob(f"{out}/*.jpg"))
cols, rows, tw, th = 3, 4, 427, 240
for si in range(0, len(files), cols * rows):
    batch = files[si:si + cols * rows]
    sheet = Image.new("RGB", (cols * tw, rows * (th + 20)), "black")
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(batch):
        img = Image.open(f).resize((tw, th))
        x, y = (i % cols) * tw, (i // cols) * (th + 20)
        sheet.paste(img, (x, y + 20))
        sec = int(os.path.basename(f)[2:8])
        d.text((x + 5, y + 2), f"{sec//3600}:{(sec%3600)//60:02d}", fill="yellow")
    sheet.save(f"{out}_sheets/s_{si//(cols*rows):02d}.jpg", quality=80)
print(f"{len(files)} kare, {len(glob.glob(out+'_sheets/*.jpg'))} kontakt sayfası -> {out}_sheets/")
