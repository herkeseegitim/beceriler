---
name: "iki-hal-dugmesi"
description: "Bir açma-kapama düğmesinin içine küçük bir dünya sığdırıp tek tıkla iki hâl arasında geçen kısa video biçimi; tüm projelerde, projeye göre uyarlanarak."
---

# İki hâl düğmesi

Fikrin kaynağı: X'te Lattice_Node hesabının gündüz/gece tema düğmesi videosu. Kodu ve çizimi alınmadı; biçim kendi sözlerimizle yazıldı, çizim ve kod sıfırdan yapıldı. Siz de kaynak videonun manzarasını, evini ya da karakterini kopyalamayın.

## Biçimin özü
- Sıradan bir arayüz parçası (yuvarlak hatlı açma-kapama düğmesi) içinde yaşayan küçük bir dünya. İzleyici önce "düğme" sanar, sonra içindeki dünyayı görür.
- Düğmenin iki hâli mesajın iki hâlidir. Tek bir tık birinden ötekine geçirir.
- Mesaj iki hâle bölünmüyorsa bu biçim kullanılmaz.

## 1. Projeyi belirleyin ve kurallarını yükleyin
Bu beceri biçimi verir; renk, dil, kapanış ve onay akışı projenizindir. Üretime başlamadan önce projenin marka kurallarını (renkler, logo, dil, kapanış kartı) okuyun. Yoksa sahibinden isteyin.

| Proje | Dünya | Dil | Kapanış |
|---|---|---|---|
| Örnek: Herkese Eğitim (ÇizTahta, YazTahta) | Bir sınıf, bir tahta, bir masa; ürünün kendi nesnesi (cetvel, harf vagonu, kalem) | Türkçe, siz dili | Ürüne özgü kapanış ve çağrı cümlesi ("İndirin, sınıfınızda kullanın.") |
| Sizin projeniz | Projenin en tanınır nesnesi | Projenin dili | Projenin kendi kapanış kartı ({kurum}, {yazar}) |

Örnek palet (Herkese Eğitim): krem #FBF4E8, koyu #231B1B, kırmızı #D62828, turuncu #E8731A. Kendi paletinizi kullanın.

## 2. İki hâli yazın
Tek satırda: "Sol hâl: ____. Sağ hâl: ____. Tık şunu temsil eder: ____."
Örnekler:
- ÇizTahta (örnek): boş tahta, ders anlatılmış tahta; tık = eklentiyi açmak.
- YazTahta (örnek): harfleri karman çorman masa, sıraya dizilmiş cümle.
- Genel: dağınık masa, düzenli masa; gece ve yalnız bir pencere, sabah ve dolu bir sınıf.

İki hâl arasındaki fark bir bakışta görünmeli (ışık, renk, düzen, kalabalık).

## 3. Sahne
- Piksel dünyayı düşük çözünürlükte (ör. 240×125) çizin, tam sayı ölçekle büyütün (×4), `imageSmoothingEnabled = false`.
- İki hâl ayrı paletlerdir; geçişte gökyüzü ve zemin ara bir renkten (şafak gibi) geçer.
- Düğme: yuvarlak köşeli çerçeve (yükseklik 500 için köşe yarıçapı yaklaşık 220), gölgeli kenar, iç gölge.
- Cam topuz: büyütme yok, yalnız kenar parıltısı ve ince vurgu; içerikteki hiçbir öğeyi puslandırmaz. Bir hâlde solda, ötekinde sağda durur, yaylı kayar (yaklaşık 0,6 sn).
- İmleç ekrana girer, topuza gider, basar (topuz %94'e küçülür), bırakır; tık sesi basışta ve bırakışta.
- Başlığın son satırı hâlle birlikte değişir (ör. "Tahta boş" yerine "Ders anlatıldı").
- Koyu-açık geçişte gri ara kare oluşmasın: yazı ve logo ortada kısa söner, yeni renkle döner.

## 4. Zamanlama (120 BPM kalıbı)
- 0–2 sn: ilk hâl; ilk saniyede hareket (ışıklar yanar, nesne kıpırdar).
- 2–6 sn: ilk hâlin sorunu vuruşlarla kurulur.
- 6–8 sn: imleç gelir; tık bir bar başında (ör. 8,0).
- 8–16 sn: ikinci hâl; şaşırtma anı burada.
- 16–24 sn: projenin kapanışı; son akor bitmeden yaklaşık 1,5 sn önce.
- Müzik: hakları sizde olan bir müzik, bar sınırlarında kesilir; tık bir bölüm geçişine denk gelir. Geçişte whoosh sesi yok.

## 5. Üretim ve kontrol
- Yöntem: sayfada `render(t)` fonksiyonu olan bir canvas, Playwright ile her kare için çağırıp görüntü alma, ffmpeg ile H.264 (yuv420p, bt709) videoya çevirme.
- Başlangıç kodu bu klasörde: `ornek/baslangic.html` (dünya, düğme, imleç, başlık ve kapanış) ve `ornek/kaydet.py` (kareleri alır, videoyu yapar). Dünyayı değiştirin, düğme ve imleç kodunu koruyun. Ayrıntı: `ornek/NASIL.md`.
- Kontrol: videoyu teslimden önce `eyes-video-kontrol` becerisiyle ya da kendi kontrol listenizle açın.
- Video hazır olsa bile yayın sizin işinizdir: geri alınamayan her adım için o an açık onay alın.

## Uyarlama sınırları
- Aynı projede biçim sık tekrarlanırsa şaşırtma kaybolur: bir projede üst üste iki videoda kullanılmaz.
- Bir projenin dünyası başka projede kullanılmaz.
- Düğme her zaman sizin çiziminizdir; kaynak videodan hiçbir görsel öğe kopyalanmaz.
