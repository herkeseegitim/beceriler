#!/usr/bin/env python3
"""Altyazı dosyası (.srt) denetimi. Yalnız standart kütüphane, ağ çağrısı yok.
Kullanım: python3 -I srt_denetim.py dosya.srt
Yöntem kaynağı: kajisho5/subtitle-skill doğrulama kuralları (MIT olarak bildirilir); kod bu pakete özgüdür."""
import sys

def zt(s):
    h, m, r = s.split(':'); sn, ms = r.split(',')
    return int(h) * 3600 + int(m) * 60 + int(sn) + int(ms) / 1000

def oku(p):
    c = []
    for x in open(p, encoding='utf-8-sig').read().strip().split('\n\n'):
        L = x.strip().split('\n')
        a, e = [zt(t.strip()) for t in L[1].split('-->')]
        c.append((L[0], a, e, L[2:]))
    return c

def denetle(c, cps=17, satir=42, enaz=0.8, ensatir=2):
    bul = []; onc = None
    for i, a, e, L in c:
        d = e - a; n = sum(len(l) for l in L)
        if onc is not None and a < onc: bul.append(f"{i}: önceki altyazıyla çakışıyor ({onc-a:.2f} sn)")
        if len(L) > ensatir: bul.append(f"{i}: {len(L)} satır")
        for l in L:
            if len(l) > satir: bul.append(f"{i}: satır {len(l)} harf (>{satir})")
        if d < enaz: bul.append(f"{i}: {d:.2f} sn ekranda (<{enaz})")
        if d > 0 and n / d > cps: bul.append(f"{i}: okuma hızı {n/d:.1f} harf/sn (>{cps})")
        onc = e
    return bul

c = oku(sys.argv[1]); b = denetle(c)
print(len(c), 'altyazı'); print('\n'.join(b) or 'sorun yok')
