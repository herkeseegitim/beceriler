#!/usr/bin/env python3
"""Harf magnetleri üretici.

Kullanım:
    python3 magnet.py hesaplar.json            # parca.html ve deneme.html yazar
    python3 magnet.py hesaplar.json -o cikti/  # başka klasöre
    python3 magnet.py hesaplar.json --ayri     # ayrıca magnet.css, magnet.js, parca-ayri.html

hesaplar.json:
{
  "baslik": "Bizi bulun",                  (isteğe bağlı, ekranda görünmez; liste etiketi)
  "not": "Magnetleri sürükleyebilirsiniz.",   (isteğe bağlı; boş bırakılırsa yazılmaz)
  "zemin": "#2A2420",                      (deneme sayfasının zemini)
  "hesaplar": [
    {"harf": "YT", "ad": "YouTube", "adres": "https://www.youtube.com/@ornek", "renk": "#D9322B", "yazi": "#FFFFFF"},
    ...
  ]
}

Kurallar: adres yalnız https:// ile başlar; harf 1-3 karakter; renk #RRGGBB.
Harf rengi (yazi) verilmezse magnet rengine göre koyu ya da açık olanı seçilir;
oran 4,5'in altındaysa uyarı yazılır (WCAG).
Aynı sayfaya tek parça konur; iki parça konursa .hm-1… renk sınıfları çakışır.
Çıktıda dış istek yok: yazı tipi sistemden, kod ve stil dosyanın içinde.
Sıkı CSP'li sitede (satır içi betik ya da stil kapalı) --ayri kullanın.
"""
import json, os, re, sys, html, argparse

KOYU, ACIK = "#2A1C10", "#FFFFFF"
VARSAYILAN_RENK = ["#D9322B", "#F28A1E", "#FFC21A", "#2E6E5E", "#2F5D8A", "#6E5A44", "#FFF4DE", "#7A3E8C"]


def _parlaklik(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def oran(a, b):
    x, y = sorted((_parlaklik(a), _parlaklik(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)


def hata(m):
    sys.exit("Hata: " + m)


def denetle(v):
    if not isinstance(v.get("hesaplar"), list) or not v["hesaplar"]:
        hata("'hesaplar' listesi boş ya da yok.")
    if len(v["hesaplar"]) > 12:
        hata("En çok 12 magnet. Kalabalık alt bilgide magnetler okunmaz.")
    for k in ("baslik", "not", "zemin"):
        if k in v and not isinstance(v[k], str):
            hata(f"'{k}' metin olmalı.")
    zemin = v.get("zemin", "#2A2420")
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", zemin):
        hata("zemin #RRGGBB olmalı.")
    cikan, uyari = [], []
    for i, h in enumerate(v["hesaplar"]):
        n = f"{i + 1}. hesap"
        if not isinstance(h, dict):
            hata(f"{n}: {{ }} içinde harf, ad, adres olmalı.")
        for k in ("harf", "ad", "adres", "renk", "yazi"):
            if k in h and not isinstance(h[k], str):
                hata(f"{n}: '{k}' metin olmalı.")
        harf = str(h.get("harf", "")).strip()
        ad = str(h.get("ad", "")).strip()
        adres = str(h.get("adres", "")).strip()
        if not 1 <= len(harf) <= 3:
            hata(f"{n}: harf 1-3 karakter olmalı ('{harf}').")
        if not ad:
            hata(f"{n}: 'ad' boş. Ekran okuyucu ve magnetin altındaki yazı bunu kullanır.")
        if not re.fullmatch(r"https://[^\s\"'<>]+", adres):
            hata(f"{n}: adres https:// ile başlamalı, boşluk ve tırnak içermemeli ('{adres}').")
        renk = h.get("renk") or VARSAYILAN_RENK[i % len(VARSAYILAN_RENK)]
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", renk):
            hata(f"{n}: renk #RRGGBB olmalı ('{renk}').")
        yazi = h.get("yazi") or (KOYU if oran(renk, KOYU) >= oran(renk, ACIK) else ACIK)
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", yazi):
            hata(f"{n}: yazi rengi #RRGGBB olmalı ('{yazi}').")
        o = oran(renk, yazi)
        if o < 4.5:
            uyari.append(f"{n} ({harf}): harf ile magnet rengi arasındaki oran {o:.2f}; 4,5 altı zor okunur.")
        if oran(renk, zemin) < 1.5:
            uyari.append(f"{n} ({harf}): magnet zeminle neredeyse aynı renkte; gölgeye rağmen seçilmeyebilir.")
        cikan.append(dict(harf=harf, ad=ad, adres=adres, renk=renk.upper(), yazi=yazi.upper(), oran=round(o, 2)))
    return zemin.upper(), cikan, uyari


STIL = """.hm{--hm-boy:64px;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.hm-liste{display:flex;flex-wrap:wrap;gap:16px 20px;margin:0;padding:0;list-style:none}
.hm-liste li{margin:0;padding:0}
.hm-m{display:flex;flex-direction:column;align-items:center;gap:8px;text-decoration:none;color:inherit;touch-action:none;user-select:none;-webkit-user-select:none;-webkit-touch-callout:none;position:relative;z-index:1;cursor:grab;outline:none}
.hm-m b{width:var(--hm-boy);height:var(--hm-boy);border-radius:50%;display:grid;place-items:center;font-size:calc(var(--hm-boy)*.31);font-weight:800;letter-spacing:-.02em;line-height:1;box-shadow:0 6px 0 rgba(0,0,0,.4),inset 0 -6px 0 rgba(0,0,0,.18),inset 0 5px 0 rgba(255,255,255,.25);transition:transform .2s,box-shadow .2s}
.hm-m span{font-size:14px;opacity:.85;max-width:12ch;text-align:center;overflow-wrap:anywhere}\n.hm-m.hm-uc b{font-size:calc(var(--hm-boy)*.25);letter-spacing:-.04em}
.hm-liste li:nth-child(odd) .hm-m b{transform:rotate(-6deg)}.hm-liste li:nth-child(even) .hm-m b{transform:rotate(5deg)}
.hm-m:hover b,.hm-m:focus-visible b{transform:translateY(-5px) rotate(0);box-shadow:0 11px 0 rgba(0,0,0,.35),inset 0 -6px 0 rgba(0,0,0,.18),inset 0 5px 0 rgba(255,255,255,.25)}
.hm-m:focus-visible b{outline:3px solid #1F6FEB;outline-offset:4px}
.hm-m.hm-tut{z-index:5;cursor:grabbing}
.hm-m.hm-tut b{transform:scale(1.12) rotate(0);box-shadow:0 18px 14px rgba(0,0,0,.45),inset 0 -6px 0 rgba(0,0,0,.18),inset 0 5px 0 rgba(255,255,255,.25)}
.hm-not{margin:12px 0 0;font-size:13px;font-style:italic;opacity:.7}
@media (max-width:600px){.hm{--hm-boy:54px}.hm-liste{gap:14px 16px}}
@media (prefers-reduced-motion:reduce){.hm-m b{transition:none}}
@media (forced-colors:active){.hm-m b{border:2px solid CanvasText}}"""

# Sürükleme: 6 px'ten az kayma tık sayılır; sürüklendiyse bağlantı açılmaz.
# Esc sürüklemeyi iptal eder, magnet yerine döner, bırakınca bağlantı açılmaz (odak gerekmez).
# Konum kaydedilmez; sayfa yenilenince magnetler yerine döner.
BETIK = """(function(){var etkin=null;
document.addEventListener("keydown",function(e){if(e.key==="Escape"&&etkin)etkin();});
document.querySelectorAll(".hm-m").forEach(function(m){var bx,by,dx=0,dy=0,ox=0,oy=0,tut=false,kaydi=false;
function yer(x,y){dx=x;dy=y;m.style.transform=(x||y)?"translate("+x+"px,"+y+"px)":"";}
function bit(){if(!tut)return;tut=false;etkin=null;m.classList.remove("hm-tut");}
function iptal(){yer(ox,oy);bit();kaydi=true;}
m.addEventListener("pointerdown",function(e){if(e.button)return;tut=true;kaydi=false;bx=e.clientX;by=e.clientY;ox=dx;oy=dy;etkin=iptal;try{m.setPointerCapture(e.pointerId);}catch(_){}});
m.addEventListener("pointermove",function(e){if(!tut)return;var x=e.clientX-bx,y=e.clientY-by;if(!kaydi&&Math.hypot(x,y)<6)return;kaydi=true;m.classList.add("hm-tut");yer(ox+x,oy+y);});
m.addEventListener("pointerup",function(){bit();if(kaydi)setTimeout(function(){kaydi=false;},0);});m.addEventListener("pointercancel",function(){if(tut)iptal();});
m.addEventListener("click",function(e){if(kaydi){e.preventDefault();kaydi=false;}});
m.addEventListener("dragstart",function(e){e.preventDefault();});});})();"""


def renk_stili(hesaplar):
    return "\n".join(f'.hm-{i + 1} b{{background:{h["renk"]};color:{h["yazi"]}}}' for i, h in enumerate(hesaplar))


def parca(v, hesaplar, ayri=False):
    E = lambda s: html.escape(s, quote=True)
    baslik = v.get("baslik") or "Sosyal medya"
    li = "\n".join(
        f'<li><a class="hm-m hm-{i + 1}{" hm-uc" if len(h["harf"]) == 3 else ""}" href="{E(h["adres"])}" rel="noopener" draggable="false">'
        f'<b aria-hidden="true">{E(h["harf"])}</b>'
        f'<span>{E(h["ad"])}</span></a></li>' for i, h in enumerate(hesaplar))
    not_ = v.get("not", "Magnetleri sürükleyebilirsiniz.")
    not_html = f'\n<p class="hm-not" aria-hidden="true">{E(not_)}</p>' if not_ else ""
    govde = f'<div class="hm">\n<ul class="hm-liste" aria-label="{E(baslik)}">\n{li}\n</ul>{not_html}\n</div>\n'
    if ayri:
        return ('<!-- harf-magnetleri: başla (magnet.css head içine, magnet.js body sonuna) -->\n'
                + govde + '<!-- harf-magnetleri: bitti -->\n')
    return (f'<!-- harf-magnetleri: başla -->\n<style>\n{STIL}\n{renk_stili(hesaplar)}\n</style>\n'
            + govde + f'<script>\n{BETIK}\n</script>\n<!-- harf-magnetleri: bitti -->\n')


def deneme(v, zemin, p):
    yazi = KOYU if oran(zemin, KOYU) >= oran(zemin, ACIK) else "#FFF4DE"
    return f"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src 'none'; base-uri 'none'; form-action 'none'">
<title>Harf magnetleri</title>
<style>html,body{{margin:0}}body{{min-height:100vh;display:flex;flex-direction:column;justify-content:flex-end;background:#F3EEE4;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}}
.sayfa{{flex:1;padding:40px 24px;color:#3A322C}}footer{{background:{zemin};color:{yazi};padding:40px 24px 48px}}</style></head>
<body><main class="sayfa"><p>Sayfanızın içeriği burada durur. Alt bilgiye bakın.</p></main>
<footer>
{p}</footer></body></html>
"""


def main():
    a = argparse.ArgumentParser(description="Harf magnetleri üretir.")
    a.add_argument("hesaplar")
    a.add_argument("-o", "--cikti", default=".")
    a.add_argument("--ayri", action="store_true", help="stil ve betiği magnet.css ve magnet.js dosyalarına ayır (sıkı CSP'li siteler için)")
    x = a.parse_args()
    try:
        with open(x.hesaplar, encoding="utf-8") as f:
            v = json.load(f)
    except FileNotFoundError:
        hata(f"{x.hesaplar} bulunamadı.")
    except (IsADirectoryError, PermissionError):
        hata(f"{x.hesaplar} bir dosya değil ya da okunamıyor.")
    except UnicodeDecodeError:
        hata(f"{x.hesaplar} UTF-8 değil. Dosyayı UTF-8 olarak kaydedin.")
    except json.JSONDecodeError as e:
        hata(f"{x.hesaplar} okunamadı: {e.lineno}. satır, {e.colno}. sütunda JSON hatası.")
    if not isinstance(v, dict):
        hata("Dosyanın en dışı { } olmalı.")
    zemin, hesaplar, uyari = denetle(v)
    p = parca(v, hesaplar)
    os.makedirs(x.cikti, exist_ok=True)
    if x.ayri:
        with open(os.path.join(x.cikti, "magnet.css"), "w", encoding="utf-8") as f:
            f.write(STIL + "\n" + renk_stili(hesaplar) + "\n")
        with open(os.path.join(x.cikti, "magnet.js"), "w", encoding="utf-8") as f:
            f.write(BETIK + "\n")
        with open(os.path.join(x.cikti, "parca-ayri.html"), "w", encoding="utf-8") as f:
            f.write(parca(v, hesaplar, ayri=True))
    with open(os.path.join(x.cikti, "parca.html"), "w", encoding="utf-8") as f:
        f.write(p)
    with open(os.path.join(x.cikti, "deneme.html"), "w", encoding="utf-8") as f:
        f.write(deneme(v, zemin, p))
    for h in hesaplar:
        print(f'{h["harf"]:>3}  {h["ad"]:<14} {h["renk"]} / {h["yazi"]}  oran {h["oran"]}')
    for u in uyari:
        print("Uyarı:", u)
    print("Yazıldı:", os.path.join(x.cikti, "parca.html"), "ve deneme.html" + (", magnet.css, magnet.js, parca-ayri.html" if x.ayri else ""))


if __name__ == "__main__":
    main()
