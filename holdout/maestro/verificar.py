#!/usr/bin/env python3
"""Revisao POR LEITURA dos fluxos Maestro (regra 8: nao ha app para rodar antes da Parte IV).

1. Cobertura: todo cenario de cenarios.md (menos os estruturais), toda falha de rnf09.md e todo estado de
   estados-m9.md tem fluxo e entrada no manifesto `holdout/suite.json`.
2. Sintaxe: cada YAML tem as duas partes (cabecalho `appId` + lista de comandos) e so usa comandos conhecidos.
3. Textos: cada texto de `tapOn`/`assertVisible`/`assertNotVisible` existe no HTML de referencia do prototipo
   (comparacao sem acento/caixa) ou esta na lista de excecoes justificadas abaixo.
Saida: relatorio JSON; codigo 1 se algo ficou sem explicacao.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent

# Texto -> justificativa (nao esta no prototipo, mas esta certo no fluxo)
EXCECOES = {
    "Conversa sobre o dia no trabalho": "nome de sessao SEMEADA no backend (fixtures), nao e texto de tela do prototipo",
    "Conversa sobre o sono": "idem",
    "Escreva uma mensagem...": "placeholder do campo de chat (atributo, nao texto de no); conferir no app",
    "Toque para gravar": "rotulo do botao de gravacao (prototipo mostra o estado; conferir no app)",
    "Buscar nos registros...": "placeholder da busca (atributo)",
}
COMANDOS = {"launchApp", "tapOn", "inputText", "assertVisible", "assertNotVisible", "takeScreenshot", "extendedWaitUntil",
            "runFlow", "runScript", "assertTrue", "pressKey", "hideKeyboard"}


def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip()


def proto_texto():
    raw = (RAIZ / "referencia" / "Cerne - Prototipo Final.html").read_text(encoding="utf-8", errors="replace")
    raw = raw.replace("\\\\u002F", "/").replace("\\u002F", "/").replace("&amp;", "&").replace("&gt;", ">")
    return norm(raw)


def ids_esperados():
    cen = (RAIZ / "cenarios.md").read_text()
    h = re.findall(r"^\*\*(H\d\d-\d)\b", cen, re.M)
    estruturais = {"H07-2", "H07-3", "H10-1"}
    rn = re.findall(r"^\| (F\d\d) \|", (RAIZ / "rnf09.md").read_text(), re.M)
    est = re.findall(r"^\| \d+ \| `(\w+)` \|", (RAIZ / "estados-m9.md").read_text(), re.M)
    return [i for i in h if i not in estruturais], rn, est


def textos_do_fluxo(doc):
    for cmd in doc:
        if isinstance(cmd, dict) and isinstance(cmd.get("runFlow"), dict):
            env = cmd["runFlow"].get("env") or {}
            if "CONVERSA" in env:
                yield env["CONVERSA"]
        if isinstance(cmd, dict):
            for k in ("tapOn", "assertVisible", "assertNotVisible"):
                if k in cmd:
                    v = cmd[k]
                    if isinstance(v, dict):
                        v = v.get("text")
                    if isinstance(v, str):
                        yield v


def verificar():
    rel = {"sem_fluxo": [], "yaml_invalido": [], "texto_fora_do_prototipo": {}, "excecoes_usadas": {}}
    man = json.loads((RAIZ / "suite.json").read_text())
    c, f, e = ids_esperados()
    # H09-1..3 e H09-3a/b: o manifesto usa o id do cenario (H09-3), nao os sub-ids da proxy
    for cid in c:
        if cid not in man["cenarios"]:
            rel["sem_fluxo"].append(cid)
    rel["sem_fluxo"] += [x for x in f if x not in man["falhas"]] + [x for x in e if x not in man["estados"]]
    P = proto_texto()
    for p in sorted(AQUI.glob("*.yaml")) + sorted((AQUI / "_comum").glob("*.yaml")):
        try:
            docs = list(yaml.safe_load_all(p.read_text()))
            assert len(docs) == 2 and "appId" in docs[0] and isinstance(docs[1], list), "estrutura"
            for cmd in docs[1]:
                nome = next(iter(cmd)) if isinstance(cmd, dict) else cmd
                assert nome in COMANDOS, f"comando desconhecido {nome}"
        except Exception as ex:  # noqa: BLE001
            rel["yaml_invalido"].append(f"{p.name}: {ex}")
            continue
        for t in textos_do_fluxo(docs[1]):
            if "${" in t:
                continue
            if norm(t) in P:
                continue
            if t in EXCECOES:
                rel["excecoes_usadas"][t] = EXCECOES[t]
            else:
                rel["texto_fora_do_prototipo"].setdefault(t, []).append(p.name)
    rel["ok"] = not (rel["sem_fluxo"] or rel["yaml_invalido"] or rel["texto_fora_do_prototipo"])
    rel["n_fluxos"] = {"cenarios": len(man["cenarios"]), "falhas": len(man["falhas"]), "estados": len(man["estados"])}
    return rel


if __name__ == "__main__":
    r = verificar()
    print(json.dumps(r, indent=2, ensure_ascii=False))
    sys.exit(0 if r["ok"] else 1)
