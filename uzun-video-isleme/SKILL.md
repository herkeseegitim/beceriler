---
name: uzun-video-isleme
description: Saatlerce süren video kayıtlarını (canlı yayın, ders, webinar, konferans — elinizdeki ya da kullanıcının yüklediği mp4) izlemeden işleyip Türkçe rehber belgeye dönüştürme becerisi. Kullanıcı bir video dosyası yükleyip "özetle", "önemli konuları çıkar", "konuşmaları çevir", "slaytları oku" dediğinde; video yabancı dilde olduğunda; video 30 dakikadan uzun olduğunda bu beceriyi kullan. Slayt okuma + ses transkripti + çapraz doğrulama boru hattının tamamı burada.
---

# Uzun Video İşleme

Saatlerce süren bir videoyu (çoğu zaman yabancı dilde) izlemeden, içindeki kritik bilgiyi güvenilir biçimde çıkarıp derli toplu bir Türkçe belgeye dönüştürmek için denenmiş bir boru hattı.

## Temel ilke: iki kanal, tek gerçek

Video iki bilgi kanalı taşır ve ikisi birbirini denetler:

1. **Görsel kanal (slaytlar):** sayılar, tarihler, tutarlar, adresler buradan alınır. Ses transkripti ne kadar temiz olursa olsun sayısal bilgi yalnız sesten yazılmaz.
2. **Ses kanalı (konuşmalar):** slaytlarda olmayan yorumlar, taktikler, uyarılar, alıntılar buradan gelir. Whisper base modelinin çıktısı gürültülüdür; anlam çıkarılır, rakam çıkarılmaz.

Belgeye giren her tarih ve tutarın kaynağı slayttır; sözlü bilgiler "konuşmadan" diye işaretlenir. Belirsiz kalan değer belgeye "sesten net çıkmadı" notuyla girer ya da hiç girmez.

## Adım 0: Keşif

```bash
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 VIDEO.mp4
ffprobe -v error -select_streams s -show_entries stream=codec_name -of csv VIDEO.mp4   # gömülü altyazı var mı?
```

Gömülü altyazı varsa önce onu çıkarın (`ffmpeg -i VIDEO.mp4 -map 0:s:0 altyazi.srt`), transkripsiyona girmeyin. Çözünürlüğü not edin: 480p ve üstü slayt okumaya yeter; 240p'de slaytlar okunur ama belgeye gömülecek görüntüler yumuşak olur (kullanıcıya söyleyin).

## Adım 1: Görsel tarama (her zaman önce bu)

1. `scripts/kareler.py` ile videodan düzenli aralıkla kare çekin (kısa videoda 60 sn, 3 saatten uzunda 180–300 sn) ve zaman damgalı kontakt sayfaları (3×4 ızgara) üretin:
   `python3 scripts/kareler.py VIDEO.mp4 180 kareler`
2. Kontakt sayfalarına bakarak oturum/bölüm haritası çıkarın: hangi dakikada hangi konu, nerede mola, nerede slayt yoğun.
3. Önemli anlardan tam çözünürlüklü kare çekin. Konuşmacı ekranın solundaysa slayt bölgesini kırpın:
   `ffmpeg -ss SANIYE -i VIDEO.mp4 -frames:v 1 -q:v 2 -vf "crop=iw*0.70:ih:iw*0.30:0,scale=1250:-1" slayt.jpg`
   Slayt tam ekransa kırpmayın; kırparsanız içerik kaybolur.
4. Slaytları okuyun. Tarih, tutar, adres, e-posta gibi kritik verileri buradan toplayın.

Bu adım tek başına özetin omurgasını verir; sesten önce kullanıcıya ilk özet sunulabilir ve sunulmalıdır. Uzun transkripsiyon sürerken kullanıcı boş beklemesin.

## Adım 2: Ses transkripti (yalnız gereken bölümler)

Tamamını dökmeyin: kullanıcı için değerli bölümleri seçin (açılış konuşması, kritik oturum, soru-cevap).

Kurulum isteğe bağlıdır; her adımdan önce ne indirileceğini, kaynağını, boyutunu ve lisansını söyleyip onay alın. Sistem Python'unu bozmamak için ayrı bir sanal ortam kullanın:

```bash
python3 -m venv sesenv && . sesenv/bin/activate
pip install sherpa-onnx soundfile
wget https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.tar.bz2
tar xf sherpa-onnx-whisper-base.tar.bz2
```

- sherpa-onnx Apache-2.0, Whisper ağırlıkları MIT olarak bildirilir; kullanmadan önce lisansları kontrol edin. Boyutu indirme sayfasında görün.
- Neden bu yol: model GitHub Releases'tan iner; Hugging Face ya da OpenAI sunucularına erişimi kısıtlı ortamlarda da çalışır. Erişiminiz varsa başka bir Whisper kurulumu da olur.
- Hız: int8 base modeli tek CPU çekirdeğinde yaklaşık 3 kat gerçek zamanlı çalışır (1 saat ses ≈ 20 dk). Daha temiz ama yaklaşık 3 kat yavaş isteyen için `-small` modeli aynı adreste.

Transkripsiyonu `scripts/transkript.py` ile yapın. Özellikleri:
- Whisper'ın 30 sn pencere sınırına göre 28 sn'lik parçalar, her satır zaman damgalı.
- **Kaldığı yerden devam eder:** dosyadaki satır sayısını sayar, yazılmış parçaları atlar. Süreç durursa aynı komutla yeniden başlatın; iş kaybolmaz.
- Uzun işi arka planda çalıştırın, örneğin `VID=VIDEO.mp4 LANG_CODE=en nohup python3 scripts/transkript.py > tr.log 2>&1 &`. Çalıştığınız aracın komut süre sınırı varsa bekleme komutlarını o sınırın altında tutun.
- Sessiz ya da bekleme ekranlarında model tek kelimeyi döngüye sokar (aynı sözcüğün satır boyu tekrarı). Bu satırları yok sayın.

## Adım 3: Çeviri ve sentez

- Ham transkript bozuk olacaktır; slayt bağlamıyla birlikte okuyun, anlamı çıkarın, Türkçeye çevirin.
- Konuşmacının slaytta olmayan katkılarını arayın: taktikler ("emin değilseniz önce kaynağa dönün" gibi), tekrarlanan uyarılar, güçlü alıntılar. Bunlar belgenin en değerli kısmıdır.
- Soru-cevap bölümleri ayrı başlıkta özetlenir (soru, cevap).

## Adım 4: Çıktı belgesi

- Kullanıcının diline ve sesine uygun, insan elinden çıkmış gibi yazılmış belge. Belge üretme beceriniz varsa (ör. docx) onu kullanın; PDF gerekiyorsa LibreOffice ile dönüştürün.
- Yapı: **tarihli işler ve yapılacaklar en başta tablo hâlinde**, sonra bölüm bölüm içerik, sonda dürüstlük notu ("konuşma çevirileri otomatik çözümlemeden geçti; tutarlar ve tarihler slaytlardan doğrulandı; önemli kararlar öncesi resmi kaynaktan teyit edin").
- İstenirse önemli slayt kareleri belgeye gömülür, altına çevirisi yazılır.
- Süreç uzunsa ara teslim yapın: önce slayta dayalı özet, transkript bittikçe konuşma çevirileri.

## Bilinen tuzaklar

| Tuzak | Çözüm |
|---|---|
| Arka plan işi araç zaman aşımında duruyor | Kaldığı yerden devam eden betik, aynı komutla yeniden başlatma |
| Model ağırlıkları inmiyor | GitHub Releases'taki sherpa-onnx modelleri |
| Tam ekran slaytı kırpınca içerik gitti | Kırpmadan önce kontakt sayfasından yerleşimi kontrol edin |
| Sessizlikte döngüye giren tek kelime | Tekrarlı tek kelimelik satırları atın |
| Sesten alınan rakam yanlış | Rakamlar yalnız slayttan; şüphede dürüstlük notu |
| Tırnaklı Türkçe metni komut satırında düzenlerken bozulma | Düzenleme betiklerini ayrı dosya olarak yazın |
