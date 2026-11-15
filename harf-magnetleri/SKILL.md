---
name: "harf-magnetleri"
description: "Bir sitenin sosyal medya ve iletişim bağlantılarını buzdolabı magneti gibi duran, parmakla ya da fareyle sürüklenebilen harf magnetlerine çevirir; tek parça HTML, internetsiz çalışır. Alt bilgi, bağlantı sayfası ya da 'bizi bulun' bölümü istendiğinde kullanılır."
---

# Harf magnetleri

Sıradan simge sırası yerine renkli, yuvarlak, hafif eğik harf magnetleri: YT, IG, FB, in… Fare üstüne gelince magnet kalkar, tutup sürükleyince yerinden oynar, kısa bir tıkla bağlantı açılır. Ziyaretçi bir an durup oynar. Alt bilgiye küçük bir canlılık katar.

Bu beceri tasarımı ve çalışan kodu verir. Hangi hesapların, hangi renklerle konacağı kullanıcınındır.

## 1. Bilgileri toplayın
Kullanıcıdan şunları alın. Eksik olanı sorun, uydurmayın.

| Alan | Ne | Örnek |
|---|---|---|
| Hesaplar | Her biri için ad, adres (https://), harf | YouTube, https://www.youtube.com/@ornekkanal, YT |
| Renk (`renk`) | Her magnet için #RRGGBB. Verilmezse beceri hazır paletten sırayla verir | #D9322B |
| Harf rengi (`yazi`) | İsteğe bağlı. Verilmezse magnet rengine göre koyu ya da açık seçilir | #FFFFFF |
| Liste adı (`baslik`) | İsteğe bağlı. Ekranda görünmez, ekran okuyucu okur | Sosyal medya |
| Zemin (`zemin`) | Magnetlerin duracağı alt bilginin rengi | #2A2420 |
| Not (`not`) | Magnetlerin altındaki küçük satır. Hiç yazılmazsa "Magnetleri sürükleyebilirsiniz." çıkar, boş metin ("") verilirse satır çıkmaz | Magnetleri sürükleyebilirsiniz. |
| Sitenin CSP'si | Sitede satır içi betik ya da stil kapalı mı | Bilmiyorsa sayfanın `<head>` bölümüne birlikte bakın |

Harf seçerken:
- 1–3 karakter. Platformun bilinen kısaltması (YT, IG, FB, TT, X, in, GH) ya da adın ilk harfi.
- Platform logosu, simgesi ya da logonun yazı biçimi kullanılmaz. Yalnız düz harf. Renk de logonun birebir kopyası olmak zorunda değil. Sitenin kendi paletine uyan renkler daha iyi durur.
- 12'den fazla magnet koymayın, kalabalıkta okunmaz. Az ve gerçekten kullanılan hesaplar.

## 2. Üretin
`ornek/magnet.py` betiği bir JSON dosyasından magnetleri üretir. Örnek dosya: `ornek/hesaplar.json`.

```
python3 ornek/magnet.py hesaplar.json -o cikti/
```

Çıktı:
- `parca.html`: stil, liste ve betik tek parça. Sitenin alt bilgisine olduğu gibi yapıştırılır.
- `deneme.html`: parçanın boş bir sayfanın altında nasıl durduğunu gösteren deneme sayfası.

Sitede satır içi betik ya da stil kapalıysa (sıkı CSP) `--ayri` ekleyin. Betik ayrıca `magnet.css`, `magnet.js` ve yalnız listeyi içeren `parca-ayri.html` yazar. CSS `<head>` içine, JS sayfa sonuna bağlanır.

Betik şunları denetler, hata varsa durur: adres https:// ile başlıyor mu, harf 1–3 karakter mi, renk biçimi doğru mu. Harf rengi verilmezse magnet rengine göre koyu ya da açık olanı seçer. Harf ile magnet arasındaki karşıtlık oranı 4,5'in altındaysa ya da magnet zeminle neredeyse aynı renkteyse uyarı yazar. Uyarıyı kullanıcıya aynen iletin, renk önerin.

Betik yoksa ya da çalıştırılamıyorsa aynı yapıyı elle kurun: `ul.hm-liste` içinde her magnet için `a.hm-m` ve onun içinde `b` (harf, `aria-hidden="true"`) ile `span` (ad). Stil ve betik `magnet.py` içindeki STIL ve BETIK metinleridir. Onları değiştirmeden kullanın.

## 3. Davranış (değiştirmeyin)
- Her magnet gerçek bir `<a href>` bağlantısıdır. Klavyeyle Tab ile gelinir, Enter ile açılır. Ekran okuyucu harfi değil adı okur.
- Kayma 6 pikselden azsa tık sayılır ve bağlantı açılır. Daha fazla kayarsa magnet sürüklenir ve bağlantı açılmaz.
- Dokunmatik ekranda parmakla sürüklenir. Magnetin üstünden başlayan kaydırma sayfayı kaydırmaz, magnetin dışından kaydırma olağan çalışır.
- Esc sürüklemeyi iptal eder: magnet yerine döner, bırakınca bağlantı açılmaz. Magnetin odakta olması gerekmez. Konum kaydedilmez, sayfa yenilenince magnetler yerine döner. Tarayıcıda hiçbir şey tutulmaz.
- Az hareket isteyen ziyaretçide geçiş animasyonu kapanır. Yüksek karşıtlık kipinde magnetin çevresine kenar çizilir.
- Dış istek yok: yazı tipi sistemden gelir, görsel kullanılmaz.
- Üç harfli magnette yazı biraz küçülür, uzun adlar alt satıra kırılır.
- Bir sayfaya tek parça konur. İki parça konursa renk sınıfları (`.hm-1`…) çakışır.

Çift tıkla yerine döndürme gibi ek bir davranış eklemeyin. Çift tıkın ilk tıkı bağlantıyı açar.

## 4. Siteye koyun ve deneyin
1. `deneme.html`'i tarayıcıda açın. Magnetleri sürükleyin, birine kısa tıklayın, Tab ile dolaşın.
2. Parçayı sitenin alt bilgisine yerleştirin. Alt bilgi koyu renkteyse `span` yazıları açık renk alır (`color: inherit`). Değilse alt bilginin yazı rengini ayarlayın.
3. Sitede üç genişlikte bakın: masaüstü, tablet (768 px), telefon (390 px). Yatay taşma olmamalı.
4. Her bağlantıyı bir kez açıp doğru hesaba gittiğini görün. Yanlış adres en sık hatadır.

Yayına almak kullanıcının işidir. Siteye yükleme, geri alınamayan her adım için o an açık onay alın.

## Örnek
Fikrin çıktığı yer: Herkese Eğitim sitesinin (herkeseegitim.com) alt bilgisi. Orada koyu tahta şeridin üstünde sekiz magnet duruyor, not satırı "Mıknatısları tahtada gezdirebilirsiniz." Renkler ve not o siteye özgüdür. Kendi sitenizinkileri kullanın.

Lisans: MIT, telif Herkese Eğitim. Tam metin bu klasördeki LICENSE dosyasında.
