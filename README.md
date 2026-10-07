# SP Telas — site

Site institucional da SP Telas (Hortolândia-SP). Página estática, publicada na Vercel.

- `index.html` — página publicada (gerada, não editar à mão)
- `SP Telas Site.dc.html` + `support.js` — fonte do design (Claude Design)
- `scripts/build.py` — gera o `index.html` a partir do design

```bash
python3 scripts/build.py "SP Telas Site.dc.html" index.html
```
