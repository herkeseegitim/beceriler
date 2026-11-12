#!/usr/bin/env python3
"""Shorts/Reels teslim kontrolü. Yalnız ffmpeg/ffprobe kullanır, ağ çağrısı yok.
Kullanım: python3 -I teslim_kontrol.py video.mp4
Yöntem kaynağı: kajisho5/ffmpeg-skill check.py (MIT olarak bildirilir); kod bu pakete özgüdür."""
import json, re, subprocess, sys
from fractions import Fraction

p = sys.argv[1]
def run(a): return subprocess.run(a, capture_output=True, text=True)

pr = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", p]).stdout)
v = next(s for s in pr["streams"] if s["codec_type"] == "video")
a = next((s for s in pr["streams"] if s["codec_type"] == "audio"), None)
dur = float(pr["format"]["duration"])
fps = float(Fraction(v["r_frame_rate"]))  # eval yerine Fraction: dosyadaki metin kod gibi çalışmaz

rows = []
def row(ad, ok, deger, hedef): rows.append(("GEÇTİ" if ok else "UYARI", ad, deger, hedef))

row("boyut", (v["width"], v["height"]) == (1080, 1920), f'{v["width"]}x{v["height"]}', "1080x1920")
row("kare/sn", 24 <= fps <= 60, f"{fps:.2f}", "24–60")
row("kodek", v["codec_name"] in ("h264", "hevc") and v.get("pix_fmt") == "yuv420p",
    f'{v["codec_name"]} {v.get("pix_fmt")}', "h264 yuv420p")
row("süre", dur <= 180, f"{dur:.1f} sn", "≤180 (Reels ≤90)")

if a:
    e = run(["ffmpeg", "-hide_banner", "-nostdin", "-i", p, "-vn", "-af",
             "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"]).stderr
    d = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", e, re.S).group(0))
    I, tp = float(d["input_i"]), float(d["input_tp"])
    row("ses yüksekliği", abs(I + 14) <= 2, f"{I:.1f} LUFS", "-14 ±2")
    row("tepe", tp <= -1, f"{tp:.1f} dBTP", "≤ -1")

e = run(["ffmpeg", "-hide_banner", "-nostdin", "-i", p,
         "-vf", "blackdetect=d=0.5:pix_th=0.10,freezedetect=n=0.003:d=2",
         "-af", "silencedetect=n=-50dB:d=0.5", "-f", "null", "-"]).stderr
blk = sum(float(x) for x in re.findall(r"black_duration:([\d.]+)", e))
frz = [float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", e)]
st = re.findall(r"freeze_start: ([\d.]+)", e)
if len(st) > len(frz): frz.append(dur - float(st[-1]))
sil = sum(float(x) for x in re.findall(r"silence_duration: ([\d.]+)", e))
row("siyah", blk / dur <= 0.10, f"{blk:.1f} sn", "≤%10")
row("donuk en uzun", (max(frz) if frz else 0) <= max(3, 0.3 * dur), f"{max(frz) if frz else 0:.1f} sn", "≤ max(3 sn, %30)")
row("sessizlik", sil / dur <= 0.5, f"{sil:.1f} sn", "≤%50")

# Güvenli alan: Shorts alt %18, sağ %12 (Reels alt %20, sağ %12). Orta kareden şeritli görüntü çıkar.
h, w = v["height"], v["width"]
run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{dur/2:.2f}", "-i", p, "-frames:v", "1", "-vf",
     f"drawbox=y={int(h*0.82)}:w=iw:h={int(h*0.18)}:color=red@0.35:t=fill,"
     f"drawbox=x={int(w*0.88)}:w={int(w*0.12)}:h=ih:color=red@0.35:t=fill",
     p.rsplit('.', 1)[0] + "_guvenli_alan.png"])

for r in rows: print(f"{r[0]:6} {r[1]:16} {r[2]:>14}   hedef {r[3]}")
