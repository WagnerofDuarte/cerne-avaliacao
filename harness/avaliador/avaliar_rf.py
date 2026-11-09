"""/avaliar-rf — parte estatica por tag, numa COPIA temporaria; grava uma linha em rf.csv (esquema C-002).

Uso: python3 -m harness.avaliador.avaliar_rf --repo <repo> --ciclo A --id-rf RF01 --tag v2 --tag-anterior v1 \
       --unidade-dir specs/001-entries --contrato <pasta com openapi.yaml, error-taxonomy.md, README.md> \
       --saida calibracao/saida [--final --hold-out resultados.json --m8b]
`--final`: so na tag final (M8b, M10_cenarios, M11 a partir de `--hold-out`; o build+Maestro+screenshots ficam no V-002).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from harness.estatico import (m4_artefatos, m6_aderencia, m7_camadas, m8_cobertura, m8b_mutacao, m9_hardcodes, m10_either,
                              m12_complexidade, m13_regressao)
from harness.estatico.common import git, tag_copy, tree_files

from . import csvio


def chave_m7(v):
    return (v["arquivo"], v["regra"], v["import"])


def linha_estatica(repo, ciclo, id_rf, tag, anterior, unidade, contrato, metodologia="speckit", chat="chat", entradas="entries"):
    r = {"ciclo": ciclo, "id_rf": id_rf, "tag": tag, "commit": git(repo, "rev-parse", tag).strip(), "timebox_censurado": tag.endswith("-incompleto")}
    r["M4"] = m4_artefatos.analisar_lista(tree_files(repo, tag), m4_artefatos.SPECKIT if metodologia == "speckit" else m4_artefatos.BMAD_PADRAO)["M4"]["total"]
    if anterior and unidade:
        c = Path(contrato)
        m6 = m6_aderencia.analisar(repo, anterior, tag, unidade, m6_aderencia.carregar_contrato(c / "openapi.yaml", c / "error-taxonomy.md", c / "README.md"))
        r.update({"M6_tasks": m6["M6_tasks"], "M6_citados_nao_alterados": m6["contagens"]["citados_nao_alterados"],
                  "M6_alterados_nao_citados": m6["contagens"]["alterados_nao_citados"], "M6_inexist_arq": m6["contagens"]["inexist_arq"],
                  "M6_inexist_pkg": m6["contagens"]["inexist_pkg"], "M6_inexist_backend": m6["contagens"]["inexist_backend"]})
    with tag_copy(repo, tag) as root:
        m7 = m7_camadas.analisar(root, chat, entradas)
        r["M7"] = m7["M7_total"]
        r["M9_hardcodes"] = m9_hardcodes.analisar(root)["M9_hardcodes"]
        r["M10_assinaturas"] = m10_either.analisar(root)["M10_assinaturas"]
        cc = m12_complexidade.rodar(root)
        r["M12_media"], r["M12_acima"] = cc["M12_media"], cc["M12_acima"]
        r["M8"] = m8_cobertura.medir(root)["M8"]
    if anterior:
        with tag_copy(repo, anterior) as root:
            antes = {chave_m7(v) for v in m7_camadas.analisar(root, chat, entradas)["M7"]}
        r["M7_novas"] = len({chave_m7(v) for v in m7["M7"]} - antes)
        m13 = m13_regressao.comparar(m13_regressao.rodar_tag(repo, anterior), m13_regressao.rodar_tag(repo, tag))
        r.update({k: m13[k] for k in ("M13", "M13_sem_apagados", "M13_apagados", "M13_seguranca")})
    return r, m7


def aplicar_final(r, m7, hold_out, repo, tag):
    """M11 = aprovados/total, incluindo os estruturais H07-3 e H10-1 (do modulo M7) e H07-2 (manual, vem no arquivo)."""
    ho = json.loads(Path(hold_out).read_text()) if hold_out else {}
    aprov = total = 0
    por_rf = ho.get("M11", {})
    for rf, (a, t) in por_rf.items():
        if rf == r["id_rf"]:
            aprov, total = a, t
    r["M11_aprovados"], r["M11_total"] = aprov, total
    r["M11"] = round(aprov / total, 6) if total else ""
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--ciclo", required=True, choices=["A", "B"])
    ap.add_argument("--id-rf", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--tag-anterior")
    ap.add_argument("--unidade-dir")
    ap.add_argument("--contrato")
    ap.add_argument("--metodologia", default="speckit")
    ap.add_argument("--chat-feature", default="chat")
    ap.add_argument("--entries-feature", default="entries")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--hold-out")
    ap.add_argument("--m8b", action="store_true")
    a = ap.parse_args()
    saida = csvio.pasta_saida(a.saida)
    r, m7 = linha_estatica(a.repo, a.ciclo, a.id_rf, a.tag, a.tag_anterior, a.unidade_dir, a.contrato, a.metodologia, a.chat_feature, a.entries_feature)
    if a.final:
        r = aplicar_final(r, m7, a.hold_out, a.repo, a.tag)
    csvio.gravar(saida / "rf.csv", csvio.RF, [r], ("ciclo", "id_rf"))
    if a.final and a.m8b:
        with tag_copy(a.repo, a.tag) as root:
            (saida / f"m8b-{a.ciclo}.json").write_text(json.dumps(m8b_mutacao.medir(root), indent=1, ensure_ascii=False))
    if a.final:
        (saida / f"estruturais-{a.ciclo}.json").write_text(json.dumps({k: m7[k] for k in ("rf07_bloc_importa_bloc", "rf10_chat_importa_entradas")}, indent=1))
    print(json.dumps({"rf.csv": str(saida / "rf.csv"), "linha": r}, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
