#!/usr/bin/env python3
"""coletar_sessao.py (C-016) — parser do transcript JSONL do Claude Code.

Implementa M1, M2, M3, M5, M5b do `Metricas_e_Skills_Ciclos.md` v1.0 (ver §8
para o esquema exato de cada CSV). Lê o(s) transcript(s) de uma sessão,
corta no ponto certo (conforme o modo), segmenta por fase (`protocolo.md`
§4.4), extrai intervenções e respostas PROCESSO, soma tokens/tempo/custo, e
grava em `dados/<ciclo>/{sessoes,segmentos,intervencoes,revisoes_processo,
avisos_coleta}.csv`.

FORMATO DO JSONL: a documentação oficial do Claude Code avisa que o formato
interno "muda entre versões" (não há schema público estável). Os campos
usados aqui foram confirmados contra uma sessão real, versão 2.1.282
(01/10/2026) — ver `protocolo.md` §11 — não contra documentação oficial.
Qualquer atualização do Claude Code travado exige reconferir isto.

PONTOS AINDA NÃO CONFIRMADOS EMPIRICAMENTE (a verificar no GATE-C21, que já
prevê provocar um subagente de propósito para isso):
  - Caminho exato dos transcripts de subagentes (ver `find_subagent_transcripts`).
  - Formato do evento de compactação (`subtype: compact_boundary`) — baseado
    em relatos de comunidade, não em um evento real observado nesta sessão.
  - Espera por limite de uso (`rate_limit_s`): a partir do D-049 vem do registro
    sintético de erro de API (`<synthetic>`) que o Claude Code grava quando o
    limite é atingido; sem esse registro, grava 0 (nunca inventa).
Nenhum desses pontos derruba o script: na ausência de confirmação, cada um
degrada para 0/vazio e grava um aviso em stderr, nunca interrompe a coleta.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

try:  # D-049: horário de reinício do limite de uso; sem zoneinfo/tzdata, a espera inteira vai para rate_limit_s
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # Python < 3.9
    ZoneInfo = None  # type: ignore[assignment,misc]

    class ZoneInfoNotFoundError(Exception):  # type: ignore[no-redef]
        pass

# ---------------------------------------------------------------------------
# Constantes congeladas (protocolo.md / Metricas_e_Skills_Ciclos.md)
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
PRECOS_MD = REPO_ROOT / "harness" / "precos.md"

# protocolo.md §4.4 — tabela comando/workflow -> fase
PHASE_TABLE: dict[str, str] = {
    # Spec Kit
    "speckit-constitution": "ESPEC",
    "speckit-specify": "ESPEC",
    "speckit-clarify": "ESPEC",
    "speckit-checklist": "VALID",
    "speckit-plan": "ESPEC",
    "speckit-tasks": "ESPEC",
    "speckit-analyze": "VALID",
    "speckit-implement": "IMPL",
    "speckit-converge": "VALID",
    # BMAD
    "bmad-project-context": "ESPEC",
    "bmad-brainstorming": "ESPEC",
    "bmad-forge-idea": "ESPEC",
    "bmad-deep-recon": "ESPEC",
    "bmad-prfaq": "ESPEC",
    "bmad-product-brief": "ESPEC",
    "bmad-prd": "ESPEC",  # pode ser VALID (validar) - ver note_bmad_prd_mode
    "bmad-ux": "ESPEC",
    "bmad-architecture": "ESPEC",
    "bmad-create-epics-and-stories": "ESPEC",
    "bmad-sprint-planning": "VALID",
    "bmad-correct-course": "ESPEC",
    "bmad-build": "IMPL",
    "bmad-code-review": "VALID",
    "bmad-qa-generate-e2e-tests": "VALID",
    "bmad-retrospective": "VALID",
}

# Tipos de intervenção e seus campos obrigatórios (Metricas_e_Skills_Ciclos.md §8 / protocolo.md §1.3)
TIPOS_INTERVENCAO = {
    "redirecionamento",
    "correção",
    "edição manual",
    "permissão negada",
    "interrupção",
    "esclarecimento não solicitado",
}
CAUSAS_VALIDAS = {"ctx", "chk", "inc", "prd", "amb", "out"}
SEVERIDADES_VALIDAS = {"S1", "S2", "S3"}
NIVEIS_VALIDOS = {"N1", "N2"}
TIPOS_COM_CAUSA_OBRIGATORIA = {"redirecionamento", "correção", "edição manual"}

INTERVENCAO_RE = re.compile(r"^INTERVEN[ÇC][ÃA]O\s*\[([^\]]*)\]:", re.UNICODE)
PROCESSO_RE = re.compile(r"^PROCESSO:\s*(.*)", re.UNICODE | re.DOTALL)
IDE_SELECTION_RE = re.compile(r"^\s*<ide_selection>", re.UNICODE)

# P7 — timebox (protocolo.md)
TIMEBOX_SECONDS = {"F000": 12 * 3600}
TIMEBOX_SECONDS_DEFAULT = 8 * 3600

# P5c — esperas pelo pesquisador limitadas a 30 min cada; excedente -> pausa_s
PAUSE_CAP_S = 30 * 60

# Tolerância de div_otel acima da qual div_otel_alerta = True.
# Escolha própria do script (sem valor frozen em protocolo.md) — 2%,
# pendente de validação/ajuste pelo Wagner antes do GATE-C21.
OTEL_TOLERANCE = 0.02

MOTIVOS_FIM = {"normal", "limite_uso", "falha"}

# dados/ usa o nome completo do ciclo (cicloA/cicloB, não a/b) — convenção
# já em uso no repositório (dados/cicloA/, dados/cicloB/ já existem).
DADOS_SUBDIR = {"a": "cicloA", "b": "cicloB"}


def dados_dir_default(ciclo: str) -> Path:
    return REPO_ROOT / "dados" / DADOS_SUBDIR[ciclo]


# ---------------------------------------------------------------------------
# Leitura de preços (harness/precos.md) — nunca duplicado à mão
# ---------------------------------------------------------------------------


def load_precos(path: Path = PRECOS_MD) -> dict[str, dict[str, float]]:
    """Faz parsing da tabela markdown de harness/precos.md.

    Retorna {modelo: {input, output, cache_5m, cache_1h, cache_read}} em
    USD por token (já dividido por 1e6).
    """
    text = path.read_text(encoding="utf-8")
    precos: dict[str, dict[str, float]] = {}
    for line in text.splitlines():
        m = re.match(
            r"\|\s*`([^`]+)`\s*\|[^|]*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|",
            line,
        )
        if not m:
            continue
        modelo = m.group(1)
        vals = [float(m.group(i).replace(",", ".")) for i in range(2, 7)]
        precos[modelo] = {
            "input": vals[0] / 1_000_000,
            "output": vals[1] / 1_000_000,
            "cache_5m": vals[2] / 1_000_000,
            "cache_1h": vals[3] / 1_000_000,
            "cache_read": vals[4] / 1_000_000,
        }
    if not precos:
        raise RuntimeError(f"Nenhum preço lido de {path} — tabela mudou de formato?")
    return precos


# ---------------------------------------------------------------------------
# Localização e leitura do(s) transcript(s)
# ---------------------------------------------------------------------------


def slugify_project_dir(cwd: str) -> str:
    """Reproduz a convenção observada: cwd -> nome de diretório em ~/.claude/projects.

    Caracteres não alfanuméricos -> '-'. (Achado real, 01/10/2026: não há
    confirmação oficial do limite de 200 caracteres + hash citado por
    ferramentas de comunidade; não implementado aqui porque nenhum caminho
    deste projeto chega perto desse tamanho. Se um caminho muito longo vier
    a ser usado, revisar.)
    """
    return re.sub(r"[^A-Za-z0-9]", "-", cwd)


def find_claude_dir() -> Path:
    cfg = os.environ.get("CLAUDE_CONFIG_DIR")
    if cfg:
        return Path(cfg).expanduser()
    return Path.home() / ".claude"


def find_latest_transcript(cwd: str | None = None) -> Path:
    """Acha o .jsonl mais recente do projeto atual (modo skill)."""
    cwd = cwd or os.getcwd()
    claude_dir = find_claude_dir()
    project_dir = claude_dir / "projects" / slugify_project_dir(cwd)
    if not project_dir.is_dir():
        raise FileNotFoundError(f"Diretório de projeto não encontrado: {project_dir}")
    candidates = sorted(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    if not candidates:
        raise FileNotFoundError(f"Nenhum .jsonl em {project_dir}")
    return candidates[-1]


def find_subagent_transcripts(main_path: Path) -> list[Path]:
    """Acha transcripts de subagentes da mesma sessão.

    NÃO CONFIRMADO EMPIRICAMENTE (ver docstring do módulo) — caminho
    esperado por relato de comunidade: <project_dir>/<session_id>/subagents/
    workflows/<run>/agent-*.jsonl, como um diretório irmão do próprio
    arquivo .jsonl principal. Se não existir, degrada para lista vazia e
    avisa em stderr; GATE-C21 confirma/corrige isto com um subagente real.
    """
    session_id = main_path.stem
    session_dir = main_path.parent / session_id
    subagents_root = session_dir / "subagents"
    if not subagents_root.is_dir():
        print(
            f"[coletar_sessao] aviso: diretório de subagentes não encontrado em {subagents_root} "
            "(esperado só se a sessão não usou nenhum subagente, ou se o caminho real difere do "
            "documentado — confirmar no GATE-C21).",
            file=sys.stderr,
        )
        return []
    return sorted(subagents_root.rglob("*.jsonl"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(
                    f"[coletar_sessao] aviso: linha {lineno} de {path} não é JSON válido ({e}) — ignorada.",
                    file=sys.stderr,
                )
    return records


def parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


# ---------------------------------------------------------------------------
# Corte (modo skill / hook / manual)
# ---------------------------------------------------------------------------


def is_human_user_record(rec: dict[str, Any]) -> bool:
    if rec.get("type") != "user":
        return False
    origin = rec.get("origin") or {}
    return origin.get("kind") == "human"


def ask_user_answers(rec: dict[str, Any]) -> list[str] | None:
    """Respostas do pesquisador dadas pelo painel de perguntas do agente
    (ferramenta `AskUserQuestion`). O transcript as grava como registro
    `user` sem `origin.kind: human`, com `toolUseResult` = {questions,
    answers} (confirmado em sessão real, 11/10/2026, desvio D-015). Devolve
    a lista de textos respondidos, ou None se o registro não é uma resposta
    desse painel. Opção clicada vem como o rótulo da opção (sem prefixo);
    resposta escrita em *Other* vem como o texto digitado."""
    if rec.get("type") != "user" or is_human_user_record(rec):
        return None
    tur = rec.get("toolUseResult")
    if not isinstance(tur, dict) or "questions" not in tur or "answers" not in tur:
        return None
    answers = tur["answers"]
    if isinstance(answers, dict):
        vals = list(answers.values())
    elif isinstance(answers, list):
        vals = answers
    else:
        return None
    out: list[str] = []
    for v in vals:
        if isinstance(v, list):
            v = ", ".join(str(x) for x in v)
        out.append(str(v))
    return out


def is_researcher_record(rec: dict[str, Any]) -> bool:
    """Mensagem humana ou resposta do pesquisador pelo painel do agente."""
    return is_human_user_record(rec) or ask_user_answers(rec) is not None


def is_assistant_record(rec: dict[str, Any]) -> bool:
    return rec.get("type") == "assistant"


# D-049: registro sintético que o Claude Code grava quando o limite de uso do
# plano é atingido (`model: "<synthetic>"`, `isApiErrorMessage: true`, texto
# "You've hit your session limit · resets 12:30pm (America/Sao_Paulo)").
SYNTHETIC_MODEL = "<synthetic>"
_RESET_RE = re.compile(r"resets\s+(\d{1,2})(?::(\d{2}))?\s*([ap]m)\s*\(([A-Za-z_/+\-]+)\)", re.IGNORECASE)


def is_synthetic_record(rec: dict[str, Any]) -> bool:
    return is_assistant_record(rec) and (rec.get("message") or {}).get("model") == SYNTHETIC_MODEL


def _record_text(rec: dict[str, Any]) -> str:
    content = (rec.get("message") or {}).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def is_limit_message(rec: dict[str, Any]) -> bool:
    """D-049: mensagem sintética de erro de API que fala de limite de uso."""
    return is_synthetic_record(rec) and bool(rec.get("isApiErrorMessage")) and "limit" in _record_text(rec).lower()


def limit_reset_ts(rec: dict[str, Any]) -> datetime | None:
    """Horário de reinício do limite, lido de "resets <hora> (<fuso>)", na
    primeira ocorrência depois do registro. None se o texto não puder ser lido."""
    m = _RESET_RE.search(_record_text(rec))
    if not m or not rec.get("timestamp") or ZoneInfo is None:
        return None
    hora, minuto, ampm, nome_fuso = int(m.group(1)), int(m.group(2) or 0), m.group(3).lower(), m.group(4)
    if not 1 <= hora <= 12 or minuto > 59:
        return None
    try:
        fuso = ZoneInfo(nome_fuso)
    except (ZoneInfoNotFoundError, ValueError):
        return None
    ref = parse_ts(rec["timestamp"]).astimezone(fuso)
    candidato = ref.replace(hour=hora % 12 + (12 if ampm == "pm" else 0), minute=minuto, second=0, microsecond=0)
    if candidato < ref:
        candidato += timedelta(days=1)
    return candidato.astimezone(timezone.utc)


def agent_turn_ended(rec: dict[str, Any]) -> bool:
    """O agente terminou o turno (`stop_reason: end_turn`) ou foi cortado pelo
    limite de uso (D-049): daí em diante o transcript espera pelo pesquisador,
    até a próxima ação do agente ou mensagem humana (D-024)."""
    return is_assistant_record(rec) and (
        (rec.get("message") or {}).get("stop_reason") == "end_turn" or is_limit_message(rec)
    )


def cut_records(records: list[dict[str, Any]], mode: str) -> tuple[list[dict[str, Any]], str | None]:
    """Corta a lista de registros conforme o modo.

    Retorna (registros_cortados, timestamp_do_corte). No modo `skill`, o
    corte exclui a mensagem de invocação (a última mensagem humana da
    sessão, que contém o `/coletar-sessao <ID>`) e tudo depois dela. Nos
    modos `hook`/`manual`, usa a sessão inteira (corte = última mensagem).
    """
    if mode == "skill":
        human_idxs = [i for i, r in enumerate(records) if is_human_user_record(r)]
        if not human_idxs:
            return records, None
        cut_idx = human_idxs[-1]
        cut_ts = records[cut_idx].get("timestamp")
        return records[:cut_idx], cut_ts
    # hook / manual: usa tudo; corte = timestamp do último registro com timestamp
    for r in reversed(records):
        if r.get("timestamp"):
            return records, r["timestamp"]
    return records, None


# ---------------------------------------------------------------------------
# Fases (segmentação) — protocolo.md §4.4
# ---------------------------------------------------------------------------


@dataclass
class Segmento:
    fase: str
    marcador_origem: str
    inicio: str
    fim: str | None = None
    tokens_input: int = 0
    tokens_output: int = 0
    cache_read: int = 0
    cache_write: int = 0
    sub_tokens_input: int = 0
    sub_tokens_output: int = 0
    sub_cache_read: int = 0
    sub_cache_write: int = 0
    excluido_rate_limit: bool = False


COMMAND_NAME_RE = re.compile(r"<command-name>\s*/?([^<\s]+?)\s*</command-name>", re.UNICODE)


def extract_slash_command(rec: dict[str, Any]) -> str | None:
    """Extrai o nome do comando/skill invocado.

    Forma real (confirmada em ensaio de 11/10/2026, desvio D-014): um slash
    command expandido pela extensão aparece como mensagem humana cujo
    conteúdo traz `<command-name>/nome</command-name>`. A forma
    `system/local_command` (protocolo.md §11.1) nunca apareceu em sessão
    real; fica como reserva. Mensagem inteira colada (`<pasted_content>`)
    não é expandida e não é reconhecida aqui, de propósito."""
    if rec.get("type") == "system" and rec.get("subtype") == "local_command":
        return (rec.get("commandRun") or {}).get("command")
    if is_human_user_record(rec):
        content = (rec.get("message") or {}).get("content")
        texts: list[str] = []
        if isinstance(content, str):
            texts = [content]
        elif isinstance(content, list):
            texts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
        for t in texts:
            m = COMMAND_NAME_RE.search(t)
            if m:
                return m.group(1)
    return None


def segment_by_phase(records: list[dict[str, Any]]) -> list[tuple[dict[str, Any], str, str]]:
    """Para cada registro, devolve (registro, fase, marcador_origem).

    Mensagens sem marcador herdam a fase/marcador do marcador anterior
    (protocolo.md §4.4). Sem marcador algum ainda visto: fase "SETUP"
    (fora da tabela — cobre a sessão A1/B1 antes do primeiro comando
    reconhecido; não é um valor do protocolo, é um default deste script).
    """
    out = []
    fase_atual = "SETUP"
    marcador_atual = "(nenhum)"
    for rec in records:
        cmd = extract_slash_command(rec)
        if cmd and cmd in PHASE_TABLE:
            fase_atual = PHASE_TABLE[cmd]
            marcador_atual = cmd
        out.append((rec, fase_atual, marcador_atual))
    return out


# ---------------------------------------------------------------------------
# Tokens e custo
# ---------------------------------------------------------------------------


@dataclass
class UsoAcumulado:
    tokens_input: int = 0
    tokens_output: int = 0
    cache_read: int = 0
    cache_write_5m: int = 0
    cache_write_1h: int = 0
    modelos: set[str] = field(default_factory=set)

    @property
    def cache_write(self) -> int:
        return self.cache_write_5m + self.cache_write_1h


def accumulate_usage(records: Iterable[dict[str, Any]]) -> UsoAcumulado:
    """Soma usage por mensagem única (dedup por message.id — uma resposta da
    API pode aparecer em mais de uma linha do JSONL, uma por bloco de
    conteúdo; sem dedup, tokens seriam contados em dobro)."""
    acc = UsoAcumulado()
    seen_msg_ids: set[str] = set()
    for rec in records:
        if not is_assistant_record(rec) or is_synthetic_record(rec):
            continue
        msg = rec.get("message") or {}
        msg_id = msg.get("id")
        if msg_id and msg_id in seen_msg_ids:
            continue
        if msg_id:
            seen_msg_ids.add(msg_id)
        usage = msg.get("usage") or {}
        if not usage:
            continue
        acc.tokens_input += usage.get("input_tokens", 0) or 0
        acc.tokens_output += usage.get("output_tokens", 0) or 0
        acc.cache_read += usage.get("cache_read_input_tokens", 0) or 0
        cache_creation = usage.get("cache_creation") or {}
        acc.cache_write_1h += cache_creation.get("ephemeral_1h_input_tokens", 0) or 0
        acc.cache_write_5m += cache_creation.get("ephemeral_5m_input_tokens", 0) or 0
        if not cache_creation and usage.get("cache_creation_input_tokens"):
            # Achado documentado em harness/precos.md regra 2: se o transcript não
            # separar 5min/1h, tudo entra como 5min (aproximação registrada).
            acc.cache_write_5m += usage.get("cache_creation_input_tokens", 0) or 0
        model = msg.get("model")
        if model:
            acc.modelos.add(model)
    return acc


def compute_custo_usd(principal: UsoAcumulado, subagentes: UsoAcumulado, precos: dict[str, dict[str, float]]) -> float:
    """Regra M3 (harness/precos.md): soma por modelo. Como cada UsoAcumulado
    não separa tokens por modelo internamente quando há mais de um modelo na
    mesma sessão (ex.: Sonnet 5 no agente principal + Haiku para tarefas de
    fundo), este cálculo assume um único modelo dominante por acumulador —
    suficiente para o desenho do protocolo (P1/P1c: modelo fixo do agente
    principal e dos subagentes é sempre claude-sonnet-5). Se uma sessão
    real misturar modelos de forma relevante dentro do mesmo acumulador,
    revisar antes do Ciclo A."""
    total = 0.0
    for acc in (principal, subagentes):
        if not acc.modelos:
            continue
        # usa o primeiro modelo observado; ver nota acima
        modelo = sorted(acc.modelos)[0]
        p = precos.get(modelo)
        if not p:
            print(f"[coletar_sessao] aviso: modelo '{modelo}' sem preço em harness/precos.md — custo não somado.", file=sys.stderr)
            continue
        total += acc.tokens_input * p["input"]
        total += acc.tokens_output * p["output"]
        total += acc.cache_read * p["cache_read"]
        total += acc.cache_write_5m * p["cache_5m"]
        total += acc.cache_write_1h * p["cache_1h"]
    return round(total, 6)


# ---------------------------------------------------------------------------
# Tempo ativo / bruto / pausa (P5c)
# ---------------------------------------------------------------------------


@dataclass
class Tempos:
    duracao_s: int = 0
    duracao_bruta_s: int = 0
    pausa_s: int = 0
    rate_limit_s: int = 0


def compute_tempos(records: list[dict[str, Any]]) -> Tempos:
    """P5c: intervalos que terminam em ação do agente contam inteiros;
    esperas pelo pesquisador (terminam em mensagem humana, ou em registro de
    sistema depois que o agente terminou o turno) contam até 30 min cada,
    excedente em pausa_s. D-049: depois de uma mensagem de limite de uso, a
    espera até o reinício informado sai do tempo ativo e da pausa e vai para
    `rate_limit_s`; o que sobra até o pesquisador voltar segue a regra acima."""
    timestamped = [r for r in records if r.get("timestamp")]
    if len(timestamped) < 2:
        return Tempos()
    inicio = parse_ts(timestamped[0]["timestamp"])
    fim = parse_ts(timestamped[-1]["timestamp"])
    duracao_bruta_s = int((fim - inicio).total_seconds())

    duracao_s = 0
    pausa_s = 0
    rate_limit_s = 0
    aguardando_pesquisador = agent_turn_ended(timestamped[0])  # agente terminou o turno e ainda não houve nova ação
    for prev, cur in zip(timestamped, timestamped[1:]):
        delta = (parse_ts(cur["timestamp"]) - parse_ts(prev["timestamp"])).total_seconds()
        if delta > 0 and is_limit_message(prev):
            reinicio = limit_reset_ts(prev)
            limite = delta if reinicio is None else min(delta, max(0.0, (reinicio - parse_ts(prev["timestamp"])).total_seconds()))
            rate_limit_s += limite
            delta -= limite
        if delta > 0:
            if is_assistant_record(cur):
                # intervalo termina em ação do agente -> conta inteiro
                duracao_s += delta
            elif is_researcher_record(cur) or aguardando_pesquisador:
                # intervalo termina em mensagem (ou resposta de painel) do
                # pesquisador -> cap de 30 min. Também vale para o registro de
                # sistema (`queue-operation`, `attachment`...) gravado quando o
                # pesquisador volta de uma espera: a espera segue sendo dele (D-024)
                counted = min(delta, PAUSE_CAP_S)
                duracao_s += counted
                pausa_s += max(0, delta - PAUSE_CAP_S)
            else:
                # eventos de sistema/attachment no meio de um trabalho do agente
                # (resultado de ferramenta etc.): conta no tempo ativo
                duracao_s += delta
        if is_assistant_record(cur):
            aguardando_pesquisador = agent_turn_ended(cur)
        elif cur.get("type") == "user":
            aguardando_pesquisador = False

    return Tempos(
        duracao_s=int(duracao_s),
        duracao_bruta_s=duracao_bruta_s,
        pausa_s=int(pausa_s),
        rate_limit_s=int(rate_limit_s),
    )


def count_compactacoes(records: list[dict[str, Any]]) -> int:
    """NÃO CONFIRMADO empiricamente contra um evento real (ver docstring do
    módulo) — formato por relato de comunidade."""
    return sum(1 for r in records if r.get("type") == "system" and r.get("subtype") == "compact_boundary")


# ---------------------------------------------------------------------------
# Contexto de IDE injetado (P2)
# ---------------------------------------------------------------------------


def has_ide_context(rec: dict[str, Any]) -> bool:
    if not is_human_user_record(rec):
        return False
    content = (rec.get("message") or {}).get("content")
    if isinstance(content, str):
        return bool(IDE_SELECTION_RE.search(content))
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                if IDE_SELECTION_RE.search(block.get("text", "")):
                    return True
    return False


def human_message_text(rec: dict[str, Any]) -> str:
    """Texto da mensagem humana, com o bloco <ide_selection> removido (ele
    não faz parte do que o pesquisador escreveu)."""
    content = (rec.get("message") or {}).get("content")
    parts = []
    if isinstance(content, str):
        parts = [content]
    elif isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
    text = "\n".join(parts)
    text = re.sub(r"<ide_selection>.*?</ide_selection>", "", text, flags=re.DOTALL).strip()
    return text


# ---------------------------------------------------------------------------
# Intervenções e PROCESSO
# ---------------------------------------------------------------------------


@dataclass
class Intervencao:
    timestamp: str
    fase: str
    tipo: str
    severidade: str | None
    nivel: str | None
    causa: str | None
    texto: str


@dataclass
class RevisaoProcesso:
    timestamp: str
    fase: str
    gatilho: str
    texto: str


@dataclass
class Aviso:
    timestamp: str
    linha: str


def parse_intervencao_fields(tipo_campos: str) -> tuple[str, str | None, str | None, str | None] | None:
    """Faz parsing de `tipo|campo1|campo2` (dentro dos colchetes). Devolve
    (tipo, severidade, nivel, causa) ou None se o tipo não é reconhecido."""
    parts = [p.strip() for p in tipo_campos.split("|")]
    tipo = parts[0]
    if tipo not in TIPOS_INTERVENCAO:
        return None
    resto = parts[1:]
    severidade = nivel = causa = None
    for campo in resto:
        if campo in SEVERIDADES_VALIDAS:
            severidade = campo
        elif campo in NIVEIS_VALIDOS:
            nivel = campo
        elif campo in CAUSAS_VALIDAS:
            causa = campo
    return tipo, severidade, nivel, causa


def extract_intervencoes_e_processo(
    segmented: list[tuple[dict[str, Any], str, str]]
) -> tuple[list[Intervencao], list[RevisaoProcesso], list[Aviso]]:
    intervencoes: list[Intervencao] = []
    processos: list[RevisaoProcesso] = []
    avisos: list[Aviso] = []

    itens: list[tuple[dict[str, Any], str, str, str]] = []
    for rec, fase, marcador in segmented:
        if is_human_user_record(rec):
            textos = [human_message_text(rec)]
        else:
            textos = ask_user_answers(rec) or []
        for t in textos:
            itens.append((rec, fase, marcador, t.strip()))

    for rec, fase, marcador, text in itens:
        if not text:
            continue
        ts = rec.get("timestamp", "")

        m_int = INTERVENCAO_RE.match(text)
        if m_int:
            parsed = parse_intervencao_fields(m_int.group(1))
            if parsed is None:
                avisos.append(Aviso(timestamp=ts, linha=text[:200]))
                continue
            tipo, severidade, nivel, causa = parsed
            if tipo in TIPOS_COM_CAUSA_OBRIGATORIA and causa is None:
                avisos.append(Aviso(timestamp=ts, linha=text[:200]))
                continue
            corpo = text[m_int.end():].strip()
            intervencoes.append(
                Intervencao(
                    timestamp=ts,
                    fase=fase,
                    tipo=tipo,
                    severidade=severidade,
                    nivel=nivel,
                    causa=causa,
                    texto=corpo[:200],
                )
            )
            continue

        m_proc = PROCESSO_RE.match(text)
        if m_proc:
            # gatilho = o comando/skill ativo no momento da resposta (marcador
            # de fase) — interpretação mecânica deste script para uma coluna
            # que o protocolo não define como extraída por script; conferir
            # com o Wagner se bate com a intenção antes do GATE-C21.
            processos.append(
                RevisaoProcesso(timestamp=ts, fase=fase, gatilho=marcador, texto=m_proc.group(1).strip()[:200])
            )
            continue

        if text.upper().startswith("INTERVEN") or text.upper().startswith("PROCESSO"):
            # começa com algo parecido mas não bateu nenhum regex -> prefixo malformado
            avisos.append(Aviso(timestamp=ts, linha=text[:200]))

    return intervencoes, processos, avisos


# ---------------------------------------------------------------------------
# OpenTelemetry (conferência, GATE-C03 item 1 / item 7)
# ---------------------------------------------------------------------------


def read_otel_tokens(otel_output_path: Path, inicio: str | None, fim: str | None) -> int | None:
    """Soma tokens do output.jsonl do otelcol-contrib dentro da janela da
    sessão. Best-effort: se o arquivo não existir ou não tiver métricas de
    token reconhecíveis, devolve None (div_otel fica vazio, nunca 0 por
    suposição)."""
    if not otel_output_path.is_file():
        return None
    if not inicio or not fim:
        return None
    t0 = parse_ts(inicio)
    t1 = parse_ts(fim)
    total = 0
    found_any = False
    with otel_output_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            # Formato exato do exportador `file` do otelcol-contrib para métricas
            # OTLP não foi conferido linha a linha nesta sessão (pendência:
            # confirmar no GATE-C21 contra uma sessão real com OTel ligado).
            # Navegação best-effort pela estrutura padrão resourceMetrics/...
            for rm in d.get("resourceMetrics", []):
                for sm in rm.get("scopeMetrics", []):
                    for metric in sm.get("metrics", []):
                        name = metric.get("name", "")
                        if "token" not in name.lower():
                            continue
                        for dp in metric.get("sum", {}).get("dataPoints", []) or metric.get("gauge", {}).get("dataPoints", []):
                            ts_unix_nano = dp.get("timeUnixNano")
                            if ts_unix_nano is None:
                                continue
                            ts_dt = datetime.fromtimestamp(int(ts_unix_nano) / 1e9, tz=timezone.utc)
                            if t0 <= ts_dt <= t1:
                                total += int(dp.get("asInt", dp.get("asDouble", 0)))
                                found_any = True
    return total if found_any else None


# ---------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------

CSV_FIELDS = {
    "sessoes.csv": [
        "ciclo", "id_rf", "sessao_id", "tipo_sessao", "modo_coleta", "motivo_fim",
        "inicio", "corte", "duracao_s", "duracao_bruta_s", "pausa_s", "rate_limit_s",
        "tokens_input", "tokens_output", "cache_read", "cache_write",
        "sub_tokens_input", "sub_tokens_output", "sub_cache_read", "sub_cache_write",
        "custo_usd", "n_intervencoes", "n_processo", "n_avisos", "n_compactacoes",
        "n_msgs_contexto_ide", "div_otel", "div_otel_alerta", "modelo",
        "versao_claude_code", "config_raciocinio",
    ],
    "segmentos.csv": [
        "ciclo", "id_rf", "sessao_id", "fase", "marcador_origem", "inicio", "fim",
        "duracao_s", "tokens_input", "tokens_output", "cache_read", "cache_write",
        "sub_tokens_input", "sub_tokens_output", "sub_cache_read", "sub_cache_write",
        "excluido_rate_limit",
    ],
    "intervencoes.csv": [
        "ciclo", "id_rf", "sessao_id", "fase", "timestamp", "tipo", "severidade",
        "nivel", "causa", "texto",
    ],
    "revisoes_processo.csv": [
        "ciclo", "id_rf", "sessao_id", "fase", "timestamp", "gatilho", "texto",
    ],
    "avisos_coleta.csv": [
        "ciclo", "id_rf", "sessao_id", "timestamp", "linha",
    ],
    "tags.csv": [
        "ciclo", "tag", "tipo", "id_rf", "commit", "data",
    ],
}


def append_csv(path: Path, fieldnames: list[str], row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if is_new:
            writer.writeheader()
        writer.writerow(row)


# ---------------------------------------------------------------------------
# Timebox (P7)
# ---------------------------------------------------------------------------


def timebox_faixa(id_rf: str, segundos_acumulados: int) -> str:
    limite = TIMEBOX_SECONDS.get(id_rf, TIMEBOX_SECONDS_DEFAULT)
    pct = segundos_acumulados / limite if limite else 0
    if pct >= 1.0:
        return "atingido"
    if pct > 0.8:
        return "acima de 80%"
    if pct >= 0.5:
        return "50-80%"
    return "abaixo de 50%"


def soma_duracao_anterior(sessoes_csv: Path, ciclo: str, id_rf: str) -> int:
    if not sessoes_csv.exists():
        return 0
    total = 0
    with sessoes_csv.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("ciclo") == ciclo and row.get("id_rf") == id_rf:
                try:
                    total += int(row.get("duracao_s") or 0)
                except ValueError:
                    pass
    return total


# ---------------------------------------------------------------------------
# Orquestração principal
# ---------------------------------------------------------------------------


@dataclass
class ResultadoColeta:
    n_intervencoes: int
    n_processo: int
    n_avisos: int
    timebox_faixa: str
    div_otel_alerta: bool


def coletar(
    *,
    ciclo: str,
    id_rf: str,
    mode: str,
    motivo_fim: str = "normal",
    transcript_path: Path | None = None,
    dados_dir: Path | None = None,
    otel_output_path: Path | None = None,
    versao_claude_code: str | None = None,
    config_raciocinio: str | None = None,
    tipo_sessao: str = "desenvolvimento",
) -> ResultadoColeta:
    if motivo_fim not in MOTIVOS_FIM:
        raise ValueError(f"motivo_fim inválido: {motivo_fim}")

    dados_dir = dados_dir or dados_dir_default(ciclo)
    main_path = transcript_path or find_latest_transcript()
    all_records = load_jsonl(main_path)
    records, corte_ts = cut_records(all_records, mode)

    timestamped = [r for r in records if r.get("timestamp")]
    inicio_ts = timestamped[0]["timestamp"] if timestamped else None

    segmented = segment_by_phase(records)

    principal_usage = accumulate_usage(records)
    tempos = compute_tempos(records)
    n_compactacoes = count_compactacoes(records)
    n_msgs_contexto_ide = sum(1 for r in records if has_ide_context(r))

    sub_paths = find_subagent_transcripts(main_path)
    sub_records: list[dict[str, Any]] = []
    for p in sub_paths:
        sub_records.extend(load_jsonl(p))
    sub_usage = accumulate_usage(sub_records)

    precos = load_precos()
    custo_usd = compute_custo_usd(principal_usage, sub_usage, precos)

    intervencoes, processos, avisos = extract_intervencoes_e_processo(segmented)

    modelo = sorted(principal_usage.modelos)[0] if principal_usage.modelos else ""

    otel_tokens = None
    if otel_output_path:
        otel_tokens = read_otel_tokens(otel_output_path, inicio_ts, corte_ts)
    jsonl_total_tokens = (
        principal_usage.tokens_input
        + principal_usage.tokens_output
        + principal_usage.cache_read
        + principal_usage.cache_write
        + sub_usage.tokens_input
        + sub_usage.tokens_output
        + sub_usage.cache_read
        + sub_usage.cache_write
    )
    div_otel = None
    div_otel_alerta = False
    if otel_tokens is not None and jsonl_total_tokens:
        div_otel = round(abs(jsonl_total_tokens - otel_tokens) / jsonl_total_tokens, 4)
        div_otel_alerta = div_otel > OTEL_TOLERANCE

    sessao_id = main_path.stem
    modo_coleta = "manual" if mode == "manual" else ("hook" if mode == "hook" else "skill")
    if tipo_sessao == "instalacao":
        modo_coleta = "script"

    sessoes_csv = dados_dir / "sessoes.csv"
    acumulado_anterior = soma_duracao_anterior(sessoes_csv, ciclo, id_rf)
    faixa = timebox_faixa(id_rf, acumulado_anterior + tempos.duracao_s)

    row_sessao = {
        "ciclo": ciclo,
        "id_rf": id_rf,
        "sessao_id": sessao_id,
        "tipo_sessao": tipo_sessao,
        "modo_coleta": modo_coleta,
        "motivo_fim": motivo_fim,
        "inicio": inicio_ts or "",
        "corte": corte_ts or "",
        "duracao_s": tempos.duracao_s,
        "duracao_bruta_s": tempos.duracao_bruta_s,
        "pausa_s": tempos.pausa_s,
        "rate_limit_s": tempos.rate_limit_s,
        "tokens_input": principal_usage.tokens_input,
        "tokens_output": principal_usage.tokens_output,
        "cache_read": principal_usage.cache_read,
        "cache_write": principal_usage.cache_write,
        "sub_tokens_input": sub_usage.tokens_input,
        "sub_tokens_output": sub_usage.tokens_output,
        "sub_cache_read": sub_usage.cache_read,
        "sub_cache_write": sub_usage.cache_write,
        "custo_usd": custo_usd,
        "n_intervencoes": len(intervencoes),
        "n_processo": len(processos),
        "n_avisos": len(avisos),
        "n_compactacoes": n_compactacoes,
        "n_msgs_contexto_ide": n_msgs_contexto_ide,
        "div_otel": div_otel if div_otel is not None else "",
        "div_otel_alerta": div_otel_alerta,
        "modelo": modelo,
        "versao_claude_code": versao_claude_code or "",
        "config_raciocinio": config_raciocinio or "",
    }
    append_csv(sessoes_csv, CSV_FIELDS["sessoes.csv"], row_sessao)

    # segmentos.csv: um segmento por intervalo contíguo de mesma fase
    seg_csv = dados_dir / "segmentos.csv"
    if segmented:
        cur_fase, cur_marcador = segmented[0][1], segmented[0][2]
        seg_start_idx = 0
        for i in range(1, len(segmented) + 1):
            fim_de_segmento = i == len(segmented) or segmented[i][1] != cur_fase or segmented[i][2] != cur_marcador
            if fim_de_segmento:
                bloco = [segmented[j][0] for j in range(seg_start_idx, i)]
                ts_bloco = [r["timestamp"] for r in bloco if r.get("timestamp")]
                seg_usage = accumulate_usage(bloco)
                append_csv(
                    seg_csv,
                    CSV_FIELDS["segmentos.csv"],
                    {
                        "ciclo": ciclo,
                        "id_rf": id_rf,
                        "sessao_id": sessao_id,
                        "fase": cur_fase,
                        "marcador_origem": cur_marcador,
                        "inicio": ts_bloco[0] if ts_bloco else "",
                        "fim": ts_bloco[-1] if ts_bloco else "",
                        "duracao_s": (
                            int((parse_ts(ts_bloco[-1]) - parse_ts(ts_bloco[0])).total_seconds())
                            if len(ts_bloco) >= 2
                            else 0
                        ),
                        "tokens_input": seg_usage.tokens_input,
                        "tokens_output": seg_usage.tokens_output,
                        "cache_read": seg_usage.cache_read,
                        "cache_write": seg_usage.cache_write,
                        # Tokens de subagente por segmento: não discriminados por
                        # fase nesta primeira versão (os transcripts de
                        # subagente não carregam o marcador de fase da sessão
                        # principal) — ficam 0 aqui e inteiros em sessoes.csv.
                        "sub_tokens_input": 0,
                        "sub_tokens_output": 0,
                        "sub_cache_read": 0,
                        "sub_cache_write": 0,
                        "excluido_rate_limit": False,
                    },
                )
                if i < len(segmented):
                    cur_fase, cur_marcador = segmented[i][1], segmented[i][2]
                    seg_start_idx = i

    for it in intervencoes:
        append_csv(
            dados_dir / "intervencoes.csv",
            CSV_FIELDS["intervencoes.csv"],
            {
                "ciclo": ciclo, "id_rf": id_rf, "sessao_id": sessao_id, "fase": it.fase,
                "timestamp": it.timestamp, "tipo": it.tipo, "severidade": it.severidade or "",
                "nivel": it.nivel or "", "causa": it.causa or "", "texto": it.texto,
            },
        )
    for pr in processos:
        append_csv(
            dados_dir / "revisoes_processo.csv",
            CSV_FIELDS["revisoes_processo.csv"],
            {
                "ciclo": ciclo, "id_rf": id_rf, "sessao_id": sessao_id, "fase": pr.fase,
                "timestamp": pr.timestamp, "gatilho": pr.gatilho, "texto": pr.texto,
            },
        )
    for av in avisos:
        append_csv(
            dados_dir / "avisos_coleta.csv",
            CSV_FIELDS["avisos_coleta.csv"],
            {"ciclo": ciclo, "id_rf": id_rf, "sessao_id": sessao_id, "timestamp": av.timestamp, "linha": av.linha},
        )

    # Copia o(s) JSONL para dados/<ciclo>/brutos/
    brutos_dir = dados_dir / "brutos"
    brutos_dir.mkdir(parents=True, exist_ok=True)
    for p in [main_path] + sub_paths:
        dest = brutos_dir / p.name
        dest.write_bytes(p.read_bytes())

    return ResultadoColeta(
        n_intervencoes=len(intervencoes),
        n_processo=len(processos),
        n_avisos=len(avisos),
        timebox_faixa=faixa,
        div_otel_alerta=div_otel_alerta,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def retempos(*, ciclo: str, dados_dir: Path | None = None, aplicar: bool = True) -> tuple[list[tuple[str, str, str]], dict[str, str]]:
    """D-024/D-049: recalcula `duracao_s`, `pausa_s` e `rate_limit_s` de cada
    sessão de `sessoes.csv` a partir do transcript bruto guardado em `brutos/`,
    com a regra vigente de `compute_tempos`. Nas linhas com `modelo`
    `<synthetic>` (D-049) recalcula também `custo_usd` e `modelo` (subagentes
    achados em `brutos/agent-*.jsonl` pelo `sessionId`). Só essas colunas
    mudam, e só nas linhas em que o valor muda. Devolve (sessões com situação,
    faixa de timebox por unidade), sem expor tempos nem custos."""
    dados_dir = dados_dir or dados_dir_default(ciclo)
    sessoes_csv = dados_dir / "sessoes.csv"
    with sessoes_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    situacao: list[tuple[str, str, str]] = []
    mudou_algum = False
    for row in rows:
        if row.get("ciclo") != ciclo:
            continue
        sessao_id, id_rf, modo = row["sessao_id"], row["id_rf"], row.get("modo_coleta", "")
        bruto = dados_dir / "brutos" / f"{sessao_id}.jsonl"
        if modo not in {"skill", "hook", "manual"} or not bruto.exists():
            situacao.append((sessao_id, id_rf, "sem transcript bruto ou não recalculável"))
            continue
        records, _ = cut_records(load_jsonl(bruto), modo)
        t = compute_tempos(records)
        novos: dict[str, Any] = {"duracao_s": t.duracao_s, "pausa_s": t.pausa_s, "rate_limit_s": t.rate_limit_s}
        tempo_mudou = any(int(row.get(c) or 0) != v for c, v in novos.items())
        custo_mudou = False
        if row.get("modelo") == SYNTHETIC_MODEL:
            principal = accumulate_usage(records)
            sub_records = [
                r
                for p in sorted((dados_dir / "brutos").glob("agent-*.jsonl"))
                for r in load_jsonl(p)
                if r.get("sessionId") == sessao_id
            ]
            custo = compute_custo_usd(principal, accumulate_usage(sub_records), load_precos())
            modelo = sorted(principal.modelos)[0] if principal.modelos else ""
            custo_mudou = True
            novos.update({"custo_usd": custo, "modelo": modelo})
        if not tempo_mudou and not custo_mudou:
            situacao.append((sessao_id, id_rf, "inalterada"))
            continue
        row.update({c: v for c, v in novos.items() if c in row})
        mudou_algum = True
        situacao.append((sessao_id, id_rf, "tempo corrigido" if not custo_mudou else "tempo, custo e modelo corrigidos"))

    if aplicar and mudou_algum:
        with sessoes_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    acumulado: dict[str, int] = {}
    for row in rows:
        if row.get("ciclo") == ciclo:
            acumulado[row["id_rf"]] = acumulado.get(row["id_rf"], 0) + int(row.get("duracao_s") or 0)
    faixas = {id_rf: timebox_faixa(id_rf, seg) for id_rf, seg in acumulado.items()}
    return situacao, faixas


def ids_rf_validos() -> set[str]:
    return {"SETUP", "PLAN", "F000"} | {f"RF{i:02d}" for i in range(1, 11)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)

    p_skill = sub.add_parser("skill", help="modo normal, invocado como /coletar-sessao <ID>")
    p_skill.add_argument("id_rf", choices=sorted(ids_rf_validos()))
    p_skill.add_argument("--ciclo", required=True, choices=["a", "b"])

    p_hook = sub.add_parser("hook", help="modo hook SessionEnd, lê JSON do stdin")
    p_hook.add_argument("id_rf", choices=sorted(ids_rf_validos()))
    p_hook.add_argument("--ciclo", required=True, choices=["a", "b"])

    p_manual = sub.add_parser("manual", help="sessão cortada por limite de uso ou falha")
    p_manual.add_argument("id_rf", choices=sorted(ids_rf_validos()))
    p_manual.add_argument("--ciclo", required=True, choices=["a", "b"])
    p_manual.add_argument("--session-id", required=True)
    p_manual.add_argument("--motivo-fim", required=True, choices=["limite_uso", "falha"])

    p_retempos = sub.add_parser("retempos", help="recalcula duracao_s/pausa_s/rate_limit_s (e custo/modelo das linhas <synthetic>) de sessoes.csv a partir de brutos/ (D-024, D-049)")
    p_retempos.add_argument("--ciclo", required=True, choices=["a", "b"])
    p_retempos.add_argument("--dry-run", action="store_true", help="só mostra quais sessões mudariam")

    for p in (p_skill, p_hook, p_manual):
        p.add_argument("--versao-claude-code", default=None)
        p.add_argument("--config-raciocinio", default=None)
        p.add_argument("--otel-output", default=None, type=Path)

    args = parser.parse_args(argv)

    if args.mode == "retempos":
        situacao, faixas = retempos(ciclo=args.ciclo, aplicar=not args.dry_run)
        for sessao_id, id_rf, sit in situacao:
            print(f"{id_rf} {sessao_id[:8]}: {sit}")
        for id_rf, faixa in sorted(faixas.items()):
            print(f"Timebox {id_rf}: {faixa}.")
        if args.dry_run:
            print("(dry-run: nada foi gravado)")
        return 0

    transcript_path = None
    motivo_fim = "normal"
    if args.mode == "hook":
        hook_input = json.load(sys.stdin)
        transcript_path = Path(hook_input["transcript_path"])
    elif args.mode == "manual":
        transcript_path = find_latest_transcript()  # ajustar se --session-id apontar outro projeto
        motivo_fim = args.motivo_fim

    resultado = coletar(
        ciclo=args.ciclo,
        id_rf=args.id_rf,
        mode=args.mode,
        motivo_fim=motivo_fim,
        transcript_path=transcript_path,
        otel_output_path=args.otel_output,
        versao_claude_code=args.versao_claude_code,
        config_raciocinio=args.config_raciocinio,
    )

    # protocolo.md / Metricas_e_Skills_Ciclos.md §4.1 — nunca exibir tokens/tempo/custo
    print(f"Registrado. Intervenções reconhecidas: {resultado.n_intervencoes}.")
    print(f"Respostas PROCESSO reconhecidas: {resultado.n_processo}.")
    if resultado.n_avisos:
        print(f"Avisos (prefixo mal formado): {resultado.n_avisos}.")
    print(f"Timebox da unidade: {resultado.timebox_faixa}.")
    if resultado.div_otel_alerta:
        print("Aviso: divergência com o OpenTelemetry acima da tolerância — ver protocolo.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
