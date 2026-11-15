# harf-magnetleri (Letter magnets)

Turns a site's social and contact links into round, slightly tilted letter magnets (YT, IG, FB, in…) that sit like fridge magnets in the footer. Hover lifts a magnet, dragging moves it around, a short click opens the link. One HTML snippet, works offline, no external requests.

Included: `ornek/magnet.py` (builds the snippet from a JSON list of accounts, checks https links, letter length and colour contrast), `ornek/hesaplar.json` (example list with placeholder accounts), `ornek/NASIL.md` (how to use, in Turkish).

Behaviour: every magnet is a real link (keyboard and screen reader friendly, the reader hears the name, not the letters). Moving less than 6 px counts as a click; more than that drags and does not open the link. Works with touch. Escape cancels a drag (the magnet returns and the link does not open). Positions are not saved. Reduced-motion and forced-colours are respected. For sites with a strict Content Security Policy, `--ayri` writes `magnet.css` and `magnet.js` as separate files.

Letters only: no platform logos or logo lettering.

Requirements: Python 3.

The idea comes from the footer of herkeseegitim.com. Colours there are examples; use your own.

License: MIT, copyright Herkese Eğitim. Full text in LICENSE in this folder.
