#!/usr/bin/env python3
"""Gera gabarito.md (legivel) a partir de gabarito.json (fonte unica, escrita a mao)."""
import json, pathlib
g = json.loads((pathlib.Path(__file__).parent / "gabarito.json").read_text())
o = ["# Gabarito do repositório de calibração (H-001)", "",
     "Fonte única: `gabarito.json` (escrito à mão; linhas conferidas com `grep -n` nos snapshots). Este arquivo é gerado por `python3 gerar_gabarito_md.py`.",
     "`v1` = unidade anterior (papel de `rf01-done`); `v2` = unidade medida (papel de `final`). Montagem: `./montar-repo.sh <destino>`.", ""]
def tab(rows, cols):
    o.append("| " + " | ".join(cols) + " |"); o.append("|" + "---|" * len(cols))
    for r in rows: o.append("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |")
    o.append("")
o += ["## M4 — artefatos (Spec Kit)", ""]
for v in ("v1", "v2"): o.append(f"- `{v}`: {g['m4'][v]}")
o += ["", "Decoy: `specs/001-entries/notes.txt` (não conta).", "", "## M6 — parte D (unidade v2, anterior v1)", ""]
m6 = g["m6"]
for k in ("m6_tasks", "citados_nao_alterados", "alterados_nao_citados", "inexist_arq", "inexist_pkg", "inexist_backend", "inexist_backend_total"): o.append(f"- `{k}`: {m6[k]}")
o += ["", "## M7 — imports proibidos (RNF06)", ""]
for v in ("v1", "v2"):
    o.append(f"**{v}**"); o.append(""); tab(g["m7"][v], ["arquivo", "linha", "regra"])
o += [f"`M7_novas` em v2: {g['m7']['m7_novas_v2']}", "", "## Regras estruturais (contam na M11)", ""]
for k, rows in g["estruturais"].items():
    o.append(f"**{k}**"); o.append(""); tab(rows, ["arquivo", "linha"])
o += ["## M9 — hardcodes (v1 e v2)", ""]; tab(g["m9_hardcodes"]["v1"], ["arquivo", "linha", "tipo"])
o += ["Decoys que NÃO contam: literais em `core/design_tokens.dart`, em comentário e dentro de string (`entries_page.dart` linhas 6 e 11).", "", "## M10 — assinaturas fora de `Either` (v1 e v2)", ""]; tab(g["m10_assinaturas"]["v1"], ["arquivo", "linha", "metodo"])
o += ["## M12 — complexidade ciclomática à mão (domínio)", "", g["m12"]["_regra"], ""]
tab(g["m12"]["v1"], ["arquivo", "linha", "metodo", "cc"]); o.append(f"Resumo v1: {g['m12']['v1_resumo']}"); o.append("")
tab(g["m12"]["v2_adiciona"], ["arquivo", "linha", "metodo", "cc"]); o.append(f"Resumo v2: {g['m12']['v2_resumo']}"); o.append("")
o += ["## M13 — regressão (v1 → v2)", ""]
m13 = g["m13"]
o += [f"- passa em v1 e falha em v2: {m13['passa_em_v1_falha_em_v2']}", f"- apagado em v2: {m13['apagado_em_v2']}", f"- M13 = {m13['M13']}; sem apagados = {m13['M13_sem_apagados']}; apagados = {m13['M13_apagados']}; segurança = {m13['M13_seguranca']}", ""]
o += ["## M14 — decisões (parte D)", ""]; tab(g["m14"]["decisoes"], ["ordem", "id_principal", "estatica", "esperado"]); o.append(f"Excluídas: {g['m14']['excluidas']}"); o.append("")
o += ["## M15 — consistência (referência `entries`)", "", f"{g['m15']}", ""]
o += ["## M8 / M8b", "", f"- M8: {g['m8']}", f"- M8b: {g['m8b']}", ""]
(pathlib.Path(__file__).parent / "gabarito.md").write_text("\n".join(o))
