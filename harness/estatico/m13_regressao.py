"""M13 — taxa de regressao (suite do proprio agente).

Entrada: resultado de testes por tag ({id: 'success'|'failure'|'error'|'skipped'}), obtido com
`flutter test --reporter json` numa COPIA temporaria da tag (nada e gravado no repo do app).
ID do teste = '<arquivo>::<nome completo>'.

- regressao: passava na tag anterior e falha agora;
- apagado: passava na anterior e nao existe mais (conta na M13; coluna propria M13_apagados);
- M13 = (regressoes + apagados) / aprovados_anterior; M13_sem_apagados = regressoes / aprovados_anterior;
  M13_seguranca = 1 - M13. Skipped atual conta como 'nao falhou' (nao e regressao).
"""
from __future__ import annotations

import argparse

from .common import dump, run_flutter_tests_json, tag_copy

OK = "success"


def comparar(anterior: dict, atual: dict):
    aprov = sorted(t for t, r in anterior.items() if r == OK)
    reg = sorted(t for t in aprov if t in atual and atual[t] in ("failure", "error"))
    apag = sorted(t for t in aprov if t not in atual)
    n = len(aprov)
    f = lambda x: round(x / n, 6) if n else None
    return {"aprovados_anterior": n, "regressoes": reg, "apagados": apag,
            "M13": f(len(reg) + len(apag)), "M13_sem_apagados": f(len(reg)),
            "M13_apagados": len(apag), "M13_seguranca": (None if not n else round(1 - (len(reg) + len(apag)) / n, 6)),
            "aprovados_atual": sorted(t for t, r in atual.items() if r == OK)}


def rodar_tag(repo, tag):
    with tag_copy(repo, tag) as root:
        _, res = run_flutter_tests_json(root)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--prev-tag", required=True)
    ap.add_argument("--tag", required=True)
    a = ap.parse_args()
    dump(comparar(rodar_tag(a.repo, a.prev_tag), rodar_tag(a.repo, a.tag)))


if __name__ == "__main__":
    main()
