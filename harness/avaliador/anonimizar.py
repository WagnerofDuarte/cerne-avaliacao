"""Anonimizacao do material enviado ao avaliador (harness/juiz/README.md, 'Anonimizacao').
Le `harness/juiz/anonimizacao.txt`. Nunca envia o nome da metodologia, do ciclo, da tag nem datas."""
from __future__ import annotations

import hashlib
import random
import re
from pathlib import Path

LISTA = Path(__file__).resolve().parents[1] / "juiz" / "anonimizacao.txt"
DATA_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})?)?\b|\b\d{1,2}/\d{1,2}/\d{4}\b")
TAG_RE = re.compile(r"\bciclo[AB]/[\w.-]+|\bcommit\s+[0-9a-f]{7,40}\b", re.I)


def carregar(caminho=LISTA):
    secs, atual = {"termos": [], "cabecalhos": [], "diretorios": []}, None
    for l in Path(caminho).read_text(encoding="utf-8").splitlines():
        s = l.strip()
        if not s or s.startswith("#"):
            continue
        m = re.fullmatch(r"\[(\w+)\]", s)
        if m:
            atual = m.group(1)
            continue
        if atual == "diretorios":
            a, b = s.split(" => ", 1)
            secs[atual].append((re.compile(a, re.I), b))
        elif atual:
            secs[atual].append(re.compile(s, re.I | re.M))
    return secs


def anonimizar(texto, secs=None):
    secs = secs or carregar()
    for rx, rep in secs["diretorios"]:
        texto = rx.sub(rep, texto)
    for rx in secs["cabecalhos"]:
        texto = rx.sub("", texto)
    for rx in secs["termos"]:
        texto = rx.sub("[REDACTED]", texto)
    texto = TAG_RE.sub("[REDACTED]", texto)
    return DATA_RE.sub("[DATE]", texto)


def anonimizar_caminho(caminho, secs=None):
    return anonimizar(caminho, secs)


def codigo_ciclo(item_id, sal="harness-v1"):
    """Codigo X/Y fixo por item, sem relacao com A/B: derivado de hash do item (nao do ciclo)
    e, por item, os dois ciclos recebem codigos DIFERENTES (o chamador passa ciclo para decidir a ordem)."""
    h = int(hashlib.sha256(f"{sal}:{item_id}".encode()).hexdigest(), 16)
    return ("X", "Y") if h % 2 == 0 else ("Y", "X")   # (codigo de A, codigo de B) para este item


def mapa_para(ciclo, item_id):
    a, b = codigo_ciclo(item_id)
    return a if ciclo == "A" else b
