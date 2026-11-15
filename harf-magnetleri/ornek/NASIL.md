# Nasıl kullanılır

1. `hesaplar.json`'u kopyalayın, kendi hesaplarınızı yazın. Her hesap için `harf`, `ad`, `adres` zorunlu, `renk` ve `yazi` isteğe bağlı.
2. Çalıştırın:

   ```
   python3 magnet.py hesaplar.json -o cikti/
   ```

   Ekrana her magnetin rengi ve karşıtlık oranı yazılır. Uyarı varsa o magnetin rengini değiştirin.
3. `cikti/deneme.html`'i tarayıcıda açıp deneyin.
4. `cikti/parca.html`'in içini sitenizin alt bilgisine yapıştırın.

Sitenizde satır içi betik ya da stil kapalıysa (tarayıcı konsolunda "Content Security Policy" hatası görürseniz):

```
python3 magnet.py hesaplar.json -o cikti/ --ayri
```

`magnet.css` dosyasını `<head>` içinde, `magnet.js` dosyasını sayfanın sonunda bağlayın, `parca-ayri.html`'in içini alt bilgiye koyun.

Gereken: Python 3. Başka kurulum yok.

Hazır palet (renk verilmezse sırayla): kırmızı #D9322B, turuncu #F28A1E, sarı #FFC21A, yeşil #2E6E5E, mavi #2F5D8A, kahve #6E5A44, krem #FFF4DE, mor #7A3E8C.
