"""H-004 — amostragem de cor em screenshots (M9, parte D).

Compara a cor lida no screenshot com o hex primario do prototipo.
- Com `regiao=(x0,y0,x1,y1)` (pixels): cor modal (RGB exato) da regiao; ok se a distancia
  Delta-E 1976 (CIELAB) ate o alvo for <= `tolerancia` (padrao 4,0, abaixo da diferenca
  perceptivel de ~2,3 a ~5 conforme o observador; fixada aqui e registrada nas notas).
- Sem regiao: fracao de pixels da imagem com Delta-E <= tolerancia; ok se >= `min_fracao`.
Screenshot em PNG (sem perdas). Nada e gravado fora do stdout.
"""
from __future__ import annotations

import argparse
import math
from collections import Counter

from PIL import Image


def hex_para_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _lab(rgb):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(a, b):
    return math.dist(_lab(a), _lab(b))


def analisar(caminho, hex_alvo, regiao=None, tolerancia=4.0, min_fracao=0.02):
    alvo = hex_para_rgb(hex_alvo)
    img = Image.open(caminho).convert("RGB")
    if regiao:
        img = img.crop(regiao)
    px = list(img.get_flattened_data()) if hasattr(img, "get_flattened_data") else list(img.getdata())
    cont = Counter(px)
    moda, n_moda = cont.most_common(1)[0]
    de_moda = delta_e(moda, alvo)
    proximos = sum(n for c, n in cont.items() if delta_e(c, alvo) <= tolerancia)
    fracao = proximos / len(px)
    ok = (de_moda <= tolerancia) if regiao else (fracao >= min_fracao)
    return {"alvo": "#%02X%02X%02X" % alvo, "cor_modal": "#%02X%02X%02X" % moda, "delta_e_modal": round(de_moda, 3),
            "fracao_proxima": round(fracao, 4), "modo": "regiao" if regiao else "imagem", "ok": ok}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("imagem")
    ap.add_argument("--hex", required=True)
    ap.add_argument("--regiao", help="x0,y0,x1,y1")
    ap.add_argument("--tolerancia", type=float, default=4.0)
    a = ap.parse_args()
    reg = tuple(int(x) for x in a.regiao.split(",")) if a.regiao else None
    import json
    print(json.dumps(analisar(a.imagem, a.hex, reg, a.tolerancia), indent=2))


if __name__ == "__main__":
    main()
