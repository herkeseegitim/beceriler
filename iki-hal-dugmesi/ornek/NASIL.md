# Başlangıç kodu nasıl kullanılır

1. `baslangic.html` dosyasını tarayıcıda açın. 24 saniyelik döngü önizlemesi oynar.
2. Dosyanın başındaki `AYAR` bölümünde başlık satırlarını, çağrı cümlesini, `{yazar}` ve `{kurum}` alanlarını, renkleri ve tık anını değiştirin.
3. `dunyaCiz(t, m)` fonksiyonunu kendi dünyanızla değiştirin. `m` 0 iken ilk hâl, 1 iken ikinci hâldir; arada şafak renkleri kullanılır. Dünya 240×125 piksellik küçük bir tuvale çizilir, düğmeye ×4 büyütülerek yerleşir.
4. Düğme çerçevesine, cam topuza, imlece ve başlık geçişine dokunmayın; biçimin tanınırlığı bunlardan gelir.
5. Videoya çevirmek için:

```
python3 kaydet.py baslangic.html iki_hal.mp4
python3 kaydet.py baslangic.html iki_hal.mp4 --muzik muzik.wav   # müzikle
python3 kaydet.py baslangic.html deneme.mp4 --fps 10              # hızlı deneme
```

Gerekenler: Python 3, ffmpeg, Playwright ve Chromium. Playwright'ı bir sanal ortama kurun; kurulum isteğe bağlıdır, yapmadan önce onay verin:

```
python3 -m venv ortam && . ortam/bin/activate
pip install playwright && playwright install chromium
```

Müziğin hakları sizde olmalı. Tık sesi isterseniz kendi kaydınızı ya da lisansı uygun bir sesi 8,0 sn'ye yerleştirin.
