#!/usr/bin/env python3
"""M6-J, analise de sensibilidade (D-112): repete o julgamento das unidades cujo prompt passou de 700 mil caracteres,
sem a lista "ADDED LINES WITH NEW-FILE LINE NUMBERS" que o harness anexa ao diff (ela dobra o tamanho do prompt).
Mesmo juiz, mesma rubrica, tres execucoes e voto da maioria; resultados em dados/produto/sensibilidade-m6/, sem tocar nos originais.
Uso: python3 scripts/m6_sensibilidade.py"""
import hashlib
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness.avaliador import anonimizar, julgar, julgar_rf  # noqa: E402
from harness.avaliador.cliente import ClienteClaude  # noqa: E402
from harness.produto.julgar_lote import LIMITE_DIFF, VAZAMENTO  # noqa: E402
from harness.produto.rodar import CICLOS, arquivos_b, tag_de  # noqa: E402

SAIDA = ROOT / "dados" / "produto" / "sensibilidade-m6"
MARCA = "\nADDED LINES WITH NEW-FILE LINE NUMBERS:"
ALVOS = [("a", "RF04")] + [("b", u) for u in ("F000", "RF03", "RF01", "RF07", "RF06", "RF04", "RF05", "RF09")]


def item(ciclo, uid, cliente):
    c = CICLOS[ciclo]
    idx = [u for u, _, _ in c["unidades"]].index(uid)
    _, tg, pasta = c["unidades"][idx]
    tag = tag_de(c, tg)
    prev = tag_de(c, c["base"] if idx == 0 else c["unidades"][idx - 1][1])
    arquivos = arquivos_b(c, uid, tag) if c["metodologia"] == "bmad" else None
    plano, diff = julgar_rf.montar_entrada(c["repo"], tag, prev, pasta or "", arquivos=arquivos)
    assert MARCA in diff
    diff = diff.split(MARCA)[0]
    trunc = len(diff) > LIMITE_DIFF
    if trunc:
        diff = diff[:LIMITE_DIFF] + "\n\n[... diff truncated by the harness at %d characters ...]" % LIMITE_DIFF
    prompt = julgar.preencher("M6", PLAN=plano, DIFF=diff)
    h = hashlib.sha256(prompt.encode()).hexdigest()
    arq = SAIDA / "julgamentos" / f"m6-{ciclo}-{uid}.jsonl"
    arq.parent.mkdir(parents=True, exist_ok=True)
    if arq.exists():
        arq.unlink()
    res = julgar.julgar("M6", f"{ciclo.upper()}-{uid}", anonimizar.mapa_para(ciclo.upper(), uid), prompt, h, cliente, arq)
    return {"ciclo": ciclo, "id_rf": uid, "voto": res["voto"], "sem_maioria": res["sem_maioria"], "diff_truncado": trunc,
            "chars_prompt": len(prompt), "vazamentos_no_prompt": len(VAZAMENTO.findall(prompt))}


def main():
    cliente = ClienteClaude("claude-opus-5-5")
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda t: item(t[0], t[1], cliente), ALVOS))
    (SAIDA / "m6-sensibilidade.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(json.dumps({"itens": len(res), "modelos": sorted(cliente.modelos_observados), "chamadas": cliente.chamadas, "custo_usd": round(cliente.custo_usd, 2)}))


if __name__ == "__main__":
    main()
