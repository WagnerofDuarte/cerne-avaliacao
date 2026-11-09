"""Nucleo do avaliador LLM: prompts congelados (lidos de harness/juiz/*.md), 3 execucoes, voto majoritario,
log em julgamentos.jsonl (esquema C-002 + `hash_entrada`). Rubricas e prompts NAO sao reescritos aqui."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

JUIZ = Path(__file__).resolve().parents[1] / "juiz"
RUBRICAS = {"M6": "m6-aderencia.md", "M9": "m9-espacamento.md", "M14": "m14-handoff.md", "D16": "d16-severidade.md"}

SCHEMAS = {
    "M6": ("m6_divergences", {"type": "object", "additionalProperties": False, "required": ["divergences"], "properties": {"divergences": {
        "type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["description", "evidence", "documented", "cause"],
                                   "properties": {"description": {"type": "string"}, "evidence": {"type": "array", "items": {"type": "string"}},
                                                  "documented": {"type": "boolean"}, "cause": {"type": "string", "enum": ["ctx", "chk", "inc", "prd", "amb", "out"]}}}}}}),
    "M9": ("m9_spacing", {"type": "object", "additionalProperties": False, "required": ["spacing_ok", "deviations"], "properties": {
        "spacing_ok": {"type": "boolean"}, "deviations": {"type": "array", "items": {"type": "object", "additionalProperties": False,
            "required": ["region", "reference_pt", "candidate_pt", "note"], "properties": {"region": {"type": "string"}, "reference_pt": {"type": "number"},
            "candidate_pt": {"type": "number"}, "note": {"type": "string"}}}}}}),
    "M14": ("m14_handoff", {"type": "object", "additionalProperties": False, "required": ["implemented", "evidence", "justification"], "properties": {
        "implemented": {"type": "string", "enum": ["yes", "partial", "no"]}, "evidence": {"type": "array", "items": {"type": "string"}}, "justification": {"type": "string"}}}),
    "D16": ("d16_severity", {"type": "object", "additionalProperties": False, "required": ["severity", "justification"], "properties": {
        "severity": {"type": "string", "enum": ["S1", "S2", "S3"]}, "justification": {"type": "string"}}}),
}


def prompt_template(metrica):
    """Primeiro bloco ```text depois de '## Prompt' na rubrica (texto congelado)."""
    t = (JUIZ / RUBRICAS[metrica]).read_text(encoding="utf-8")
    t = t[t.index("## Prompt"):]
    return re.search(r"```text\n(.*?)```", t, re.S).group(1)


def hash_prompt(metrica):
    return hashlib.sha256(prompt_template(metrica).encode()).hexdigest()


def preencher(metrica, **vals):
    p = prompt_template(metrica)
    for k, v in vals.items():
        p = p.replace(f"<<<{k}>>>", str(v))
    return p


def valida(metrica, o):
    try:
        if metrica == "M6":
            return isinstance(o["divergences"], list) and all(
                isinstance(d["description"], str) and isinstance(d["evidence"], list) and isinstance(d["documented"], bool)
                and d["cause"] in ("ctx", "chk", "inc", "prd", "amb", "out") for d in o["divergences"])
        if metrica == "M9":
            return isinstance(o["spacing_ok"], bool) and isinstance(o["deviations"], list)
        if metrica == "M14":
            return o["implemented"] in ("yes", "partial", "no") and isinstance(o["evidence"], list)
        if metrica == "D16":
            return o["severity"] in ("S1", "S2", "S3")
    except (KeyError, TypeError):
        pass
    return False


# ------------------------------------------------------------------------------ votos
def _loc(e):
    m = re.match(r"(.+?):(\d+)(?:-(\d+))?$", e)
    return (m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))) if m else None


def _mesma(a, b):
    """Mesma divergencia: mesmo arquivo e intervalos de linha que se sobrepoem em ate +-10."""
    for ea in a["evidence"]:
        for eb in b["evidence"]:
            la, lb = _loc(ea), _loc(eb)
            if la and lb and la[0] == lb[0] and la[1] - 10 <= lb[2] and lb[1] - 10 <= la[2]:
                return True
    if not a["evidence"] and not b["evidence"]:
        return a["description"].strip().lower() == b["description"].strip().lower()
    return False


def voto_m6(execs):
    """execs: lista de saidas validas (ate 3). -> (resultado, sem_maioria)."""
    grupos = []   # cada grupo: [(indice_da_execucao, divergencia)]
    for i, sai in enumerate(execs):
        for d in sai["divergences"]:
            alvo = next((g for g in grupos if all(j != i for j, _ in g) and any(_mesma(d, x) for _, x in g)), None)
            if alvo is not None:
                alvo.append((i, d))
            else:
                grupos.append([(i, d)])
    itens, empate = [], False
    for g in grupos:
        if len({j for j, _ in g}) < 2:
            continue
        doc, cau = Counter(d["documented"] for _, d in g), Counter(d["cause"] for _, d in g)
        top_doc, top_cau = doc.most_common(2), cau.most_common(2)
        if (len(top_doc) > 1 and top_doc[0][1] == top_doc[1][1]) or (len(top_cau) > 1 and top_cau[0][1] == top_cau[1][1]):
            empate = True
        itens.append({"description": g[0][1]["description"], "evidence": g[0][1]["evidence"], "documented": top_doc[0][0], "cause": top_cau[0][0]})
    return {"divergences": itens, "M6_div_nao_doc": sum(1 for d in itens if not d["documented"])}, empate


def voto_simples(execs, campo):
    c = Counter(e[campo] for e in execs)
    val, n = c.most_common(1)[0]
    return val, n < 2


# ------------------------------------------------------------------------------ execucao
def julgar(metrica, item_id, ciclo_anon, prompt, entrada_hash, cliente, saida_jsonl, imagens=(), n=3, data=None):
    nome, schema = SCHEMAS[metrica]
    execs, brutas = [], []
    for k in range(1, n + 1):
        o, tentativas = None, 0
        while tentativas < 2:
            tentativas += 1
            try:
                cand = cliente.chamar(prompt, nome, schema, imagens=imagens, item_id=item_id)
            except Exception as e:  # noqa: BLE001
                cand = {"_erro": str(e)}
            if valida(metrica, cand):
                o = cand
                break
        brutas.append(o if o is not None else {"_invalida": True})
        if o is not None:
            execs.append(o)
    if len(execs) < 2:
        voto, sem = None, True      # execucao invalida duas vezes -> amostra humana
    elif metrica == "M6":
        voto, sem = voto_m6(execs)
    elif metrica == "M9":
        v, sem = voto_simples(execs, "spacing_ok"); voto = {"spacing_ok": v}
    elif metrica == "M14":
        v, sem = voto_simples(execs, "implemented"); voto = {"implemented": v}
    else:
        v, sem = voto_simples(execs, "severity"); voto = {"severity": v}
    if len(execs) == 3 and metrica in ("M14", "D16") and len({json.dumps(e.get("implemented", e.get("severity"))) for e in execs}) == 3:
        sem = True
    quando = (data or dt.date.today()).isoformat()
    par = cliente.parametros()
    with open(saida_jsonl, "a", encoding="utf-8") as f:
        for k, b in enumerate(brutas, 1):
            f.write(json.dumps({"metrica": metrica, "item_id": item_id, "ciclo_anon": ciclo_anon, "execucao": k, "saida": b, "voto_final": voto,
                                "sem_maioria": sem, "modelo_avaliador": cliente.modelo, "reasoning_effort": cliente.effort, "parametros": par,
                                "data": quando, "hash_prompt": hash_prompt(metrica), "hash_entrada": entrada_hash}, ensure_ascii=False) + "\n")
    return {"voto": voto, "sem_maioria": sem}
