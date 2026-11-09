#!/usr/bin/env python3
"""H-007 — re-derivação dos dados de coleta a partir dos transcritos brutos.

Lê `dados/<ciclo>/brutos/*.jsonl` e grava, em `dados/<ciclo>/rederivado/`,
as tabelas `sessoes.csv`, `segmentos.csv`, `intervencoes.csv`,
`revisoes_processo.csv`, `avisos_coleta.csv` (mesmo esquema do C-002),
mais `mensagens_livres.csv` (sensibilidade da M5) e `auditoria.csv`
(colunas que mudaram em relação aos CSVs originais, SEM valores).

Reaproveita as funções de `scripts/coletar_sessao.py` (congelado, só leitura):
`compute_tempos` (D-024), `accumulate_usage`, `segment_by_phase` (D-014),
`extract_intervencoes_e_processo` (D-015), `has_ide_context`/`human_message_text`
(D-056), `find`/corte do modo `skill`. Acrescenta só as decisões registradas
para a re-derivação:

  D-020 — o prefixo `INTERVENÇÃO [...]`/`PROCESSO:` é reconhecido também dentro
          de bloco `<pasted_content>`.
  D-031, D-035 — uma linha por `sessao_id` (todas as métricas vêm do bruto,
          que é único; a duplicata de coleta some).
  D-037, D-094 — sessões medidas sem coleta entram, com a unidade indicada nos
          desvios, marcadas `origem=sem_coleta`.
  D-014 — comando colado dentro de `<pasted_content>`: o agente chama a
          ferramenta `Skill`, e essa chamada vale como marcador de fase.
  Fase das sessões de correção (plano, §13.4): sessão de unidade (F000, RFxx)
          sem nenhum comando da metodologia fica na fase `IMPL`
          (marcador `(correcao)`), e não em `SETUP`.

Regra 8: a saída no terminal mostra só contagens de arquivos/linhas, PASS/FAIL e
NOMES de colunas alteradas; nunca tokens, tempos ou custos.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def _load_collector():
    spec = importlib.util.spec_from_file_location("coletar_sessao_ro", ROOT / "scripts" / "coletar_sessao.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["coletar_sessao_ro"] = mod
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


col = _load_collector()

SESSOES_FIELDS = col.CSV_FIELDS["sessoes.csv"]
SEGMENTOS_FIELDS = col.CSV_FIELDS["segmentos.csv"] + ["duracao_ativa_s"]
INTERVENCOES_FIELDS = col.CSV_FIELDS["intervencoes.csv"]
PROCESSO_FIELDS = col.CSV_FIELDS["revisoes_processo.csv"]
AVISOS_FIELDS = col.CSV_FIELDS["avisos_coleta.csv"]
LIVRES_FIELDS = ["ciclo", "id_rf", "sessao_id", "fase", "timestamp", "origem_msg", "categoria", "texto"]

# D-037 (Ciclo A, RF04) e D-094 (Ciclo B): sessões medidas sem coleta -> unidade.
SEM_COLETA = {
    "a": {"5256ebbb": "RF04", "a18e05bf": "RF04"},
    "b": {
        "7bbc5346": "RF03",
        "b03f306e": "RF01",
        "52633697": "RF01",
        "6be00999": "RF07",
        "15b67843": "RF04",
        "adf6b331": "RF08",
    },
}

PASTED_RE = re.compile(r"</?pasted_content[^>]*>", re.UNICODE)
INTERRUPT_RE = re.compile(r"^\[Request interrupted by user", re.UNICODE)
CONTINUE_RE = re.compile(r"^(continue|continue\b.*|ask again|try again.*)$", re.IGNORECASE | re.DOTALL)
NEUTRA_RE = re.compile(r"^(y|yes|yeds|yes,? proceed\.?|yes\.?)$", re.IGNORECASE)
COLETAR_RE = re.compile(r"<command-name>\s*/?coletar-sessao\s*</command-name>")


# ---------------------------------------------------------------------------
# D-020: reconhecer o prefixo também dentro de <pasted_content>
# ---------------------------------------------------------------------------
_orig_human_message_text = col.human_message_text


def human_message_text_unwrapped(rec: dict[str, Any]) -> str:
    text = _orig_human_message_text(rec)
    if "<pasted_content" in text:
        text = PASTED_RE.sub("", text).strip()
    return text


def install_unwrap() -> None:
    col.human_message_text = human_message_text_unwrapped


# ---------------------------------------------------------------------------
# Leitura dos dados originais e dos brutos
# ---------------------------------------------------------------------------
def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def index_subagents(brutos: Path) -> dict[str, list[Path]]:
    """`agent-*.jsonl` -> sessão pai (campo `sessionId` do 1º registro)."""
    idx: dict[str, list[Path]] = defaultdict(list)
    for p in sorted(brutos.glob("agent-*.jsonl")):
        with p.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    sid = json.loads(line).get("sessionId")
                except json.JSONDecodeError:
                    continue
                if sid:
                    idx[sid].append(p)
                break
    return idx


def has_command(segmented) -> bool:
    return any(m != "(nenhum)" for _, _, m in segmented)


def skill_tool_name(rec: dict[str, Any]) -> str | None:
    """Nome da skill chamada pelo próprio agente (ferramenta `Skill`)."""
    if rec.get("type") != "assistant":
        return None
    content = (rec.get("message") or {}).get("content")
    if not isinstance(content, list):
        return None
    for b in content:
        if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Skill":
            nome = (b.get("input") or {}).get("skill")
            if isinstance(nome, str):
                return nome.lstrip("/")
    return None


def segment_by_phase_with_skill_tool(records):
    """D-014: quando o comando vai dentro de `<pasted_content>`, a extensão não o
    expande e o AGENTE chama a ferramenta `Skill` por conta própria. Enquanto a
    sessão ainda não tem marcador de fase vindo de `<command-name>`, essa chamada
    vale como marcador (só para skills da tabela de fases)."""
    out = []
    fase, marcador = "SETUP", "(nenhum)"
    for rec in records:
        cmd = col.extract_slash_command(rec)
        if cmd and cmd in col.PHASE_TABLE:
            fase, marcador = col.PHASE_TABLE[cmd], cmd
            origem_cmd = True
        else:
            origem_cmd = False
        if not origem_cmd and marcador == "(nenhum)":
            nome = skill_tool_name(rec)
            if nome and nome in col.PHASE_TABLE:
                fase, marcador = col.PHASE_TABLE[nome], nome
        out.append((rec, fase, marcador))
    return out


def segment_with_correction_phase(records, id_rf: str):
    segmented = segment_by_phase_with_skill_tool(records)
    if id_rf not in ("SETUP", "PLAN") and not has_command(segmented):
        segmented = [(r, "IMPL", "(correcao)") for r, _, _ in segmented]
    return segmented



def active_seconds_by_record(records: list[dict[str, Any]]) -> list[float]:
    """Tempo ativo (P5c, D-024, D-049) atribuído ao registro em que cada intervalo
    TERMINA; replica `compute_tempos` registro a registro. A soma bate com
    `duracao_s` (a diferença é só o arredondamento para inteiro)."""
    ativo = [0.0] * len(records)
    idx = [i for i, r in enumerate(records) if r.get("timestamp")]
    if len(idx) < 2:
        return ativo
    aguardando = col.agent_turn_ended(records[idx[0]])
    for a, b in zip(idx, idx[1:]):
        prev, cur = records[a], records[b]
        delta = (col.parse_ts(cur["timestamp"]) - col.parse_ts(prev["timestamp"])).total_seconds()
        if delta > 0 and col.is_limit_message(prev):
            reinicio = col.limit_reset_ts(prev)
            limite = delta if reinicio is None else min(delta, max(0.0, (reinicio - col.parse_ts(prev["timestamp"])).total_seconds()))
            delta -= limite
        if delta > 0:
            if col.is_assistant_record(cur):
                ativo[b] += delta
            elif col.is_researcher_record(cur) or aguardando:
                ativo[b] += min(delta, col.PAUSE_CAP_S)
            else:
                ativo[b] += delta
        if col.is_assistant_record(cur):
            aguardando = col.agent_turn_ended(cur)
        elif cur.get("type") == "user":
            aguardando = False
    return ativo


# ---------------------------------------------------------------------------
# Mensagens livres (sensibilidade da M5): nada disto vira intervenção
# ---------------------------------------------------------------------------
def categorize_free(text: str) -> str:
    t = text.strip()
    if INTERRUPT_RE.match(t):
        return "interrupcao"
    if NEUTRA_RE.match(t):
        return "neutra"
    if CONTINUE_RE.match(t):
        return "retomada"
    return "outra"


def interrupt_text(rec: dict[str, Any]) -> str | None:
    """`[Request interrupted by user ...]`: o transcrito grava a interrupção (Esc)
    como registro `user` sem `origin.kind: human`."""
    if rec.get("type") != "user":
        return None
    content = (rec.get("message") or {}).get("content")
    texts = [content] if isinstance(content, str) else [
        b.get("text", "") for b in (content or []) if isinstance(b, dict) and b.get("type") == "text"
    ]
    for t in texts:
        if INTERRUPT_RE.match((t or "").strip()):
            return t.strip()
    return None


def free_messages(segmented, ciclo: str, id_rf: str, sessao_id: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for rec, fase, _ in segmented:
        ts = rec.get("timestamp", "")
        it = interrupt_text(rec)
        if it is not None:
            out.append({"ciclo": ciclo, "id_rf": id_rf, "sessao_id": sessao_id, "fase": fase, "timestamp": ts,
                        "origem_msg": "sistema", "categoria": "interrupcao", "texto": it[:120].replace("\n", " ")})
            continue
        if col.is_human_user_record(rec):
            raw = _orig_human_message_text(rec)
            if "<command-name>" in raw or COLETAR_RE.search(raw):
                continue  # invocação de skill, inclusive o /coletar-sessao
            text = human_message_text_unwrapped(rec)
            origem = "humana"
            textos = [text]
        else:
            textos = col.ask_user_answers(rec) or []
            origem = "painel"
        for t in textos:
            t = (t or "").strip()
            if not t:
                continue
            if col.INTERVENCAO_RE.match(t) or col.PROCESSO_RE.match(t):
                continue  # já reconhecida
            if t.upper().startswith("INTERVEN") or t.upper().startswith("PROCESSO"):
                continue  # prefixo malformado: já vai para avisos_coleta
            cat = "painel_sem_prefixo" if origem == "painel" else categorize_free(t)
            out.append(
                {
                    "ciclo": ciclo,
                    "id_rf": id_rf,
                    "sessao_id": sessao_id,
                    "fase": fase,
                    "timestamp": ts,
                    "origem_msg": origem,
                    "categoria": cat,
                    "texto": t[:120].replace("\n", " "),
                }
            )
    return out


# ---------------------------------------------------------------------------
# Re-derivação de uma sessão
# ---------------------------------------------------------------------------
def rederive_session(
    *,
    ciclo: str,
    sessao_id: str,
    id_rf: str,
    main_path: Path,
    sub_paths: list[Path],
    meta: dict[str, str],
    precos: dict[str, dict[str, float]],
    origem: str,
) -> dict[str, Any]:
    all_records = col.load_jsonl(main_path)
    modo = meta.get("modo_coleta", "skill")
    cut_mode = "skill" if modo == "skill" else "manual"
    if origem == "sem_coleta":
        cut_mode = "manual"  # sessão descartada: nenhuma invocação de coleta
    records, corte_ts = col.cut_records(all_records, cut_mode)
    timestamped = [r for r in records if r.get("timestamp")]
    inicio_ts = timestamped[0]["timestamp"] if timestamped else ""

    segmented = segment_with_correction_phase(records, id_rf)
    principal = col.accumulate_usage(records)
    tempos = col.compute_tempos(records)
    sub_records: list[dict[str, Any]] = []
    for p in sub_paths:
        sub_records.extend(col.load_jsonl(p))
    sub = col.accumulate_usage(sub_records)
    custo = col.compute_custo_usd(principal, sub, precos)
    intervs, procs, avisos = col.extract_intervencoes_e_processo(segmented)

    row = {
        "ciclo": ciclo,
        "id_rf": id_rf,
        "sessao_id": sessao_id,
        "tipo_sessao": meta.get("tipo_sessao", "desenvolvimento"),
        "modo_coleta": modo if origem == "coletada" else "sem_coleta",
        "motivo_fim": meta.get("motivo_fim", "normal"),
        "inicio": inicio_ts,
        "corte": corte_ts or "",
        "duracao_s": tempos.duracao_s,
        "duracao_bruta_s": tempos.duracao_bruta_s,
        "pausa_s": tempos.pausa_s,
        "rate_limit_s": tempos.rate_limit_s,
        "tokens_input": principal.tokens_input,
        "tokens_output": principal.tokens_output,
        "cache_read": principal.cache_read,
        "cache_write": principal.cache_write,
        "sub_tokens_input": sub.tokens_input,
        "sub_tokens_output": sub.tokens_output,
        "sub_cache_read": sub.cache_read,
        "sub_cache_write": sub.cache_write,
        "custo_usd": custo,
        "n_intervencoes": len(intervs),
        "n_processo": len(procs),
        "n_avisos": len(avisos),
        "n_compactacoes": col.count_compactacoes(records),
        "n_msgs_contexto_ide": sum(1 for r in records if col.has_ide_context(r)),
        # a telemetria OTel não está nos brutos: copia do registro original
        "div_otel": meta.get("div_otel", ""),
        "div_otel_alerta": meta.get("div_otel_alerta", ""),
        "modelo": sorted(principal.modelos)[0] if principal.modelos else meta.get("modelo", ""),
        "versao_claude_code": meta.get("versao_claude_code", ""),
        "config_raciocinio": meta.get("config_raciocinio", ""),
    }

    segs: list[dict[str, Any]] = []
    ativo_rec = active_seconds_by_record(records)
    if segmented:
        cur_f, cur_m = segmented[0][1], segmented[0][2]
        start = 0
        for i in range(1, len(segmented) + 1):
            if i == len(segmented) or segmented[i][1] != cur_f or segmented[i][2] != cur_m:
                bloco = [segmented[j][0] for j in range(start, i)]
                tsb = [r["timestamp"] for r in bloco if r.get("timestamp")]
                u = col.accumulate_usage(bloco)
                segs.append(
                    {
                        "ciclo": ciclo, "id_rf": id_rf, "sessao_id": sessao_id,
                        "fase": cur_f, "marcador_origem": cur_m,
                        "inicio": tsb[0] if tsb else "", "fim": tsb[-1] if tsb else "",
                        "duracao_s": int((col.parse_ts(tsb[-1]) - col.parse_ts(tsb[0])).total_seconds()) if len(tsb) >= 2 else 0,
                        "tokens_input": u.tokens_input, "tokens_output": u.tokens_output,
                        "cache_read": u.cache_read, "cache_write": u.cache_write,
                        "sub_tokens_input": 0, "sub_tokens_output": 0, "sub_cache_read": 0, "sub_cache_write": 0,
                        "excluido_rate_limit": False,
                        "duracao_ativa_s": round(sum(ativo_rec[start:i]), 3),
                    }
                )
                if i < len(segmented):
                    cur_f, cur_m = segmented[i][1], segmented[i][2]
                    start = i

    base = {"ciclo": ciclo, "id_rf": id_rf, "sessao_id": sessao_id}
    return {
        "sessao": row,
        "segmentos": segs,
        "intervencoes": [
            {**base, "fase": it.fase, "timestamp": it.timestamp, "tipo": it.tipo, "severidade": it.severidade or "",
             "nivel": it.nivel or "", "causa": it.causa or "", "texto": it.texto}
            for it in intervs
        ],
        "processos": [
            {**base, "fase": pr.fase, "timestamp": pr.timestamp, "gatilho": pr.gatilho, "texto": pr.texto}
            for pr in procs
        ],
        "avisos": [{**base, "timestamp": av.timestamp, "linha": av.linha} for av in avisos],
        "livres": free_messages(segmented, ciclo, id_rf, sessao_id),
    }


# ---------------------------------------------------------------------------
# Ciclo inteiro
# ---------------------------------------------------------------------------
def rederive_cycle(ciclo: str, dados_dir: Path, out_dir: Path) -> dict[str, Any]:
    install_unwrap()
    brutos = dados_dir / "brutos"
    precos = col.load_precos()
    orig_rows = read_csv(dados_dir / "sessoes.csv")
    by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in orig_rows:
        by_id[r["sessao_id"]].append(r)
    subs = index_subagents(brutos)
    sem_coleta = SEM_COLETA[ciclo]

    mains = sorted(p for p in brutos.glob("*.jsonl") if not p.name.startswith("agent-"))
    sessoes, segs, intervs, procs, avisos, livres = [], [], [], [], [], []
    problemas: list[str] = []
    for p in mains:
        sid = p.stem
        if sid in by_id:
            meta = by_id[sid][-1]  # D-035: vale a última coleta; o bruto é um só
            id_rf = meta["id_rf"]
            origem = "coletada"
        else:
            unidade = next((u for k, u in sem_coleta.items() if sid.startswith(k)), None)
            if unidade is None:
                problemas.append(f"bruto sem linha e sem unidade conhecida: {sid[:8]}")
                continue
            meta, id_rf, origem = {}, unidade, "sem_coleta"
        res = rederive_session(
            ciclo=ciclo, sessao_id=sid, id_rf=id_rf, main_path=p, sub_paths=subs.get(sid, []),
            meta=meta, precos=precos, origem=origem,
        )
        sessoes.append(res["sessao"]); segs += res["segmentos"]; intervs += res["intervencoes"]
        procs += res["processos"]; avisos += res["avisos"]; livres += res["livres"]
    # linhas originais sem bruto (ex.: instalação: não tem transcrito)
    ids_com_bruto = {p.stem for p in mains}
    for sid, rows in by_id.items():
        if sid not in ids_com_bruto:
            r = rows[-1]
            if r.get("tipo_sessao") != "instalacao":
                problemas.append(f"linha sem bruto (não instalação): {sid[:8]}")
            else:
                sessoes.append({k: r.get(k, "") for k in SESSOES_FIELDS})

    sessoes.sort(key=lambda r: (r["inicio"] or "", r["sessao_id"]))
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "sessoes.csv", SESSOES_FIELDS, sessoes)
    write_csv(out_dir / "segmentos.csv", SEGMENTOS_FIELDS, segs)
    write_csv(out_dir / "intervencoes.csv", INTERVENCOES_FIELDS, intervs)
    write_csv(out_dir / "revisoes_processo.csv", PROCESSO_FIELDS, procs)
    write_csv(out_dir / "avisos_coleta.csv", AVISOS_FIELDS, avisos)
    write_csv(out_dir / "mensagens_livres.csv", LIVRES_FIELDS, livres)

    # auditoria: só NOMES das colunas que mudaram (regra 8)
    aud = []
    for r in sessoes:
        orig = by_id.get(r["sessao_id"])
        if not orig:
            aud.append({"sessao_id": r["sessao_id"], "id_rf": r["id_rf"], "situacao": "sem_linha_original", "colunas_alteradas": ""})
            continue
        o = orig[-1]
        changed = []
        for k in SESSOES_FIELDS:
            a, b = str(r.get(k, "")), str(o.get(k, ""))
            if a == b:
                continue
            try:
                if abs(float(a) - float(b)) < 1e-6:
                    continue
            except ValueError:
                pass
            changed.append(k)
        aud.append(
            {"sessao_id": r["sessao_id"], "id_rf": r["id_rf"],
             "situacao": "duplicada_na_origem" if len(orig) > 1 else "ok",
             "colunas_alteradas": ";".join(changed)}
        )
    write_csv(out_dir / "auditoria.csv", ["sessao_id", "id_rf", "situacao", "colunas_alteradas"], aud)
    return {
        "sessoes": len(sessoes), "segmentos": len(segs), "intervencoes": len(intervs),
        "processos": len(procs), "avisos": len(avisos), "livres": len(livres),
        "problemas": problemas, "auditoria": aud,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ciclo", choices=["a", "b"], required=True)
    ap.add_argument("--dados", type=Path, default=None, help="pasta dados/<ciclo> (padrão: a do repositório)")
    ap.add_argument("--saida", type=Path, default=None, help="pasta de saída (padrão: <dados>/rederivado)")
    args = ap.parse_args(argv)
    dados = args.dados or col.dados_dir_default(args.ciclo)
    saida = args.saida or (dados / "rederivado")
    res = rederive_cycle(args.ciclo, dados, saida)
    print(f"ciclo {args.ciclo}: {res['sessoes']} sessões; {res['segmentos']} segmentos; "
          f"{res['intervencoes']} linhas de intervenção; {res['processos']} de PROCESSO; "
          f"{res['avisos']} avisos; {res['livres']} mensagens livres")
    mudou = [a for a in res["auditoria"] if a["colunas_alteradas"]]
    print(f"auditoria: {len(mudou)} sessões com colunas alteradas em relação ao original (nomes em auditoria.csv)")
    if res["problemas"]:
        print("PROBLEMAS:", *res["problemas"], sep="\n  ")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
