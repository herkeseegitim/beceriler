# Herkese Eğitim beceriler v1

Claude için üç ücretsiz beceri. Video üreten ya da uzun kayıtlardan not çıkaran öğretmenler için hazırlandı.

| Beceri | Ne işe yarar |
|---|---|
| `iki-hal-dugmesi` | Bir açma-kapama düğmesinin içine küçük bir dünya çizip tek tıkla iki hâl arasında geçen 24 saniyelik dikey video biçimi. Çalışan başlangıç kodu içinde. |
| `eyes-video-kontrol` | Videoyu teslimden önce denetler: boyut, ses yüksekliği, donuk ve siyah kare, güvenli alan, altyazı dosyası. Eyes kuruluysa kareler, transkript ve ekran yazısıyla birlikte. |
| `uzun-video-isleme` | Saatlerce süren webinar, ders ya da konferans kaydını izlemeden slayt ve konuşmadan Türkçe rehber belgeye çevirir. |

## Kurulum

### Claude Code
Beceri klasörünü olduğu gibi kendi beceri klasörünüze kopyalayın:

```
~/.claude/skills/iki-hal-dugmesi/
~/.claude/skills/eyes-video-kontrol/
~/.claude/skills/uzun-video-isleme/
```

Windows'ta aynı yer `%USERPROFILE%\.claude\skills\` klasörüdür. Bir projeye özel kullanmak isterseniz proje klasöründeki `.claude/skills/` altına da koyabilirsiniz. Claude Code'u yeniden başlatınca beceriler görünür.

### claude.ai
Her beceriyi ayrı ayrı zip yapın (zip'in içinde beceri klasörü ve onun içinde `SKILL.md` olsun), sonra Ayarlar'daki beceri yükleme bölümünden yükleyin. Menü adları sürüme göre değişebilir. Kod çalıştırma özelliği açık olmalı.

## Gereksinimler

| Beceri | Gereken | İsteğe bağlı |
|---|---|---|
| iki-hal-dugmesi | Python 3, ffmpeg | Playwright ve Chromium (videoya çevirmek için) |
| eyes-video-kontrol | Python 3, ffmpeg, ffprobe | Eyes (MIT olarak bildirilir), whisper.cpp (MIT), ggml-large-v3-turbo-q5_0 modeli (574.041.195 bayt, whisper.cpp model deposundan) |
| uzun-video-isleme | Python 3, ffmpeg, ffprobe, Pillow | sherpa-onnx (Apache-2.0), soundfile, sherpa-onnx Whisper base modeli (GitHub Releases; boyutu indirme sayfasında) |

İsteğe bağlı kurulumlar dış kaynaktan kod ve model indirir. Bunları ayrı bir sanal ortama kurun, her adımdan önce ne indirileceğine bakın. Üçüncü taraf araçların lisanslarını kendiniz kontrol edin; bu paket onları içermez.

Bu becerilerin hiçbiri kendi başına yayın ya da yükleme yapmaz; yalnız kendi ürettikleri geçici dosyaları siler. Claude'la çalışırken kural şu: geri alınamayan her adım için o an açık onay alın.

## Örnek kullanım

- "Şu videoyu teslimden önce kontrol et: kisa_video.mp4"
- "Bu .srt dosyasında okuma hızı ve çakışma var mı?"
- "Bu üç saatlik webinar kaydını özetle, tarihli işleri en başa koy."
- "Boş tahtadan ders anlatılmış tahtaya geçen bir iki hâl düğmesi videosu hazırla."

## Örnekler ve atıf

Beceri metinlerindeki ürün adları (ÇizTahta, YazTahta) ve renkler Herkese Eğitim'den örnektir; kendi adlarınız ve renklerinizle değiştirin.

Atıflar her becerinin içinde yazılı: Eyes (Moritz Kremb), kajisho5/ffmpeg-skill ve kajisho5/subtitle-skill (yalnız yöntem), ClaudeAnimationBase (yalnız yöntem), iki hâl düğmesi fikri için X'teki Lattice_Node hesabı.

## Lisans

MIT. Kod ve metin için geçerlidir. Ayrıntı: `LICENSE`. Telif: Herkese Eğitim.

English: `README.en.md`
