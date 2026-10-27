"""Testes unitários do coletar_sessao.py (C-016), sobre quatro transcripts
sintéticos (critério do plano): sem intervenção; com 3 intervenções de
tipos diferentes; com compactação no meio; com um subagente cujos tokens
estão em arquivo separado. Roda com: pytest scripts/tests/

Não usa nenhum transcript real de ciclo — tudo construído aqui, só com os
nomes de campo confirmados contra uma sessão real (ver docstring de
coletar_sessao.py e protocolo.md §11).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import coletar_sessao as cs  # noqa: E402


def _ts(i: int) -> str:
    # timestamps crescentes, 1 min de diferença, dentro do mesmo cap de pausa (30 min)
    return f"2026-10-01T10:{i:02d}:00.000Z"


def _user(i: int, text: str, human: bool = True) -> dict:
    return {
        "type": "user",
        "timestamp": _ts(i),
        "uuid": f"u{i}",
        "message": {"role": "user", "content": [{"type": "text", "text": text}]},
        "origin": {"kind": "human" if human else "assistant"},
    }


def _assistant(i: int, msg_id: str, text: str = "ok", tokens_in: int = 10, tokens_out: int = 5, model: str = "claude-sonnet-5") -> dict:
    return {
        "type": "assistant",
        "timestamp": _ts(i),
        "uuid": f"a{i}",
        "message": {
            "id": msg_id,
            "model": model,
            "role": "assistant",
            "content": [{"type": "text", "text": text}],
            "usage": {
                "input_tokens": tokens_in,
                "output_tokens": tokens_out,
                "cache_read_input_tokens": 0,
                "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0},
            },
        },
    }


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


@pytest.fixture
def dados_dir(tmp_path: Path) -> Path:
    return tmp_path / "dados" / "a"


# ---------------------------------------------------------------------------
# 1. Sem intervenção
# ---------------------------------------------------------------------------


def test_sem_intervencao(tmp_path: Path, dados_dir: Path):
    main = tmp_path / "proj" / "sess1.jsonl"
    records = [
        _user(0, "oi"),
        _assistant(1, "msg_1", "olá"),
        _user(2, "/coletar-sessao RF01"),  # mensagem de invocação, deve ser cortada
    ]
    _write_jsonl(main, records)

    resultado = cs.coletar(ciclo="a", id_rf="RF01", mode="skill", transcript_path=main, dados_dir=dados_dir)

    assert resultado.n_intervencoes == 0
    assert resultado.n_processo == 0
    assert resultado.n_avisos == 0

    with (dados_dir / "sessoes.csv").open() as f:
        import csv

        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["tokens_input"] == "10"
    assert rows[0]["tokens_output"] == "5"
    assert rows[0]["sessao_id"] == "sess1"


def test_corte_exclui_mensagem_de_invocacao(tmp_path: Path, dados_dir: Path):
    main = tmp_path / "proj" / "sess_corte.jsonl"
    records = [
        _user(0, "oi"),
        _assistant(1, "msg_1"),
        _user(2, "/coletar-sessao RF01"),  # invocação
        _assistant(3, "msg_2", tokens_in=999, tokens_out=999),  # nunca deveria existir de verdade, mas testa o corte
    ]
    _write_jsonl(main, records)

    cs.coletar(ciclo="a", id_rf="RF01", mode="skill", transcript_path=main, dados_dir=dados_dir)

    import csv

    with (dados_dir / "sessoes.csv").open() as f:
        rows = list(csv.DictReader(f))
    # tokens da msg_2 (pós-invocação) não podem ter sido somados
    assert rows[0]["tokens_input"] == "10"
    assert rows[0]["tokens_output"] == "5"


# ---------------------------------------------------------------------------
# 2. Três intervenções de tipos diferentes
# ---------------------------------------------------------------------------


def test_tres_intervencoes_tipos_diferentes(tmp_path: Path, dados_dir: Path):
    main = tmp_path / "proj" / "sess2.jsonl"
    records = [
        _user(0, "INTERVENÇÃO [redirecionamento|prd]: volte para a §2 dos requisitos"),
        _assistant(1, "msg_1"),
        _user(2, "INTERVENÇÃO [correção|S2|ctx]: o endpoint está errado"),
        _assistant(3, "msg_2"),
        _user(4, "INTERVENÇÃO [permissão negada]: não autorizo"),
        _assistant(5, "msg_3"),
        _user(6, "/coletar-sessao RF02"),
    ]
    _write_jsonl(main, records)

    resultado = cs.coletar(ciclo="a", id_rf="RF02", mode="skill", transcript_path=main, dados_dir=dados_dir)
    assert resultado.n_intervencoes == 3
    assert resultado.n_avisos == 0

    import csv

    with (dados_dir / "intervencoes.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 3
    assert rows[0]["tipo"] == "redirecionamento"
    assert rows[0]["causa"] == "prd"
    assert rows[1]["tipo"] == "correção"
    assert rows[1]["severidade"] == "S2"
    assert rows[1]["causa"] == "ctx"
    assert rows[2]["tipo"] == "permissão negada"
    assert rows[2]["causa"] == ""


def test_intervencao_sem_causa_obrigatoria_gera_aviso(tmp_path: Path, dados_dir: Path):
    main = tmp_path / "proj" / "sess2b.jsonl"
    records = [
        _user(0, "INTERVENÇÃO [correção|S1]: faltou a causa"),
        _assistant(1, "msg_1"),
        _user(2, "/coletar-sessao RF02"),
    ]
    _write_jsonl(main, records)

    resultado = cs.coletar(ciclo="a", id_rf="RF02", mode="skill", transcript_path=main, dados_dir=dados_dir)
    assert resultado.n_intervencoes == 0
    assert resultado.n_avisos == 1


def test_processo_reconhecido(tmp_path: Path, dados_dir: Path):
    main = tmp_path / "proj" / "sess_proc.jsonl"
    records = [
        {
            "type": "system",
            "subtype": "local_command",
            "timestamp": _ts(0),
            "commandRun": {"command": "speckit-specify", "args": ""},
        },
        _user(1, "PROCESSO: sim, siga com essa ambiguidade resolvida assim"),
        _assistant(2, "msg_1"),
        _user(3, "/coletar-sessao RF03"),
    ]
    _write_jsonl(main, records)

    resultado = cs.coletar(ciclo="a", id_rf="RF03", mode="skill", transcript_path=main, dados_dir=dados_dir)
    assert resultado.n_processo == 1

    import csv

    with (dados_dir / "revisoes_processo.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["gatilho"] == "speckit-specify"
    assert rows[0]["fase"] == "ESPEC"


def _slash_str(i: int, nome: str, args: str = "") -> dict:
    """Slash command expandido, forma real confirmada em ensaio (D-014):
    mensagem humana com `content` em string e `<command-name>`."""
    return {
        "type": "user",
        "timestamp": _ts(i),
        "uuid": f"u{i}",
        "message": {
            "role": "user",
            "content": f"<command-message>{nome}</command-message>\n<command-name>/{nome}</command-name>"
            + (f"\n<command-args>{args}</command-args>" if args else ""),
        },
        "origin": {"kind": "human"},
    }


def test_fase_detectada_por_command_name_na_mensagem_humana(tmp_path: Path, dados_dir: Path):
    main = tmp_path / "proj" / "sess_cmd.jsonl"
    records = [
        _slash_str(0, "speckit-implement", "# argumento colado"),
        _assistant(1, "msg_1"),
        _user(2, "PROCESSO: yes"),
        _assistant(3, "msg_2"),
        _user(4, "/coletar-sessao RF03"),
    ]
    _write_jsonl(main, records)

    resultado = cs.coletar(ciclo="a", id_rf="RF03", mode="skill", transcript_path=main, dados_dir=dados_dir)
    assert resultado.n_processo == 1

    import csv

    with (dados_dir / "segmentos.csv").open() as f:
        segs = list(csv.DictReader(f))
    assert {(r["fase"], r["marcador_origem"]) for r in segs} == {("IMPL", "speckit-implement")}
    with (dados_dir / "revisoes_processo.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["gatilho"] == "speckit-implement"


def test_extract_slash_command_formas():
    assert cs.extract_slash_command(_slash_str(0, "speckit-plan")) == "speckit-plan"
    em_bloco = _user(0, "<command-message>x</command-message>\n<command-name>/speckit-tasks</command-name>")
    assert cs.extract_slash_command(em_bloco) == "speckit-tasks"
    # mensagem inteira colada nao e expandida pela extensao: nao reconhece
    colada = _user(0, '\n\n<pasted_content id="4057">\n/speckit-constitution # P-SETUP')
    assert cs.extract_slash_command(colada) is None
    # texto do agente (origin != human) que cita um comando nao conta
    assert cs.extract_slash_command(_user(0, "<command-name>/speckit-plan</command-name>", human=False)) is None


def _ask_answer(i: int, answer: str, pergunta: str = "Which option?") -> dict:
    """Resposta pelo painel de perguntas do agente (`AskUserQuestion`), forma
    real confirmada em sessão real (D-015): registro `user` sem origin humana,
    `toolUseResult` com `questions` e `answers`."""
    return {
        "type": "user",
        "timestamp": _ts(i),
        "uuid": f"u{i}",
        "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_x", "content": f'User has answered your questions: "{pergunta}"="{answer}".'}]},
        "toolUseResult": {"questions": [{"question": pergunta, "options": []}], "answers": {pergunta: answer}},
    }


def test_resposta_do_painel_com_processo_e_reconhecida(tmp_path: Path, dados_dir: Path):
    main = tmp_path / "proj" / "sess_ask.jsonl"
    records = [
        _slash_str(0, "speckit-clarify"),
        _assistant(1, "msg_1"),
        _ask_answer(2, "PROCESSO: Use your technical judgment, following the input package."),
        _assistant(3, "msg_2"),
        _ask_answer(4, "Generic HTTP interceptor"),  # clique em opcao: sem prefixo, nao conta
        _assistant(5, "msg_3"),
        _user(6, "/coletar-sessao F000"),
    ]
    _write_jsonl(main, records)

    resultado = cs.coletar(ciclo="a", id_rf="F000", mode="skill", transcript_path=main, dados_dir=dados_dir)
    assert resultado.n_processo == 1
    assert resultado.n_intervencoes == 0

    import csv

    with (dados_dir / "revisoes_processo.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["gatilho"] == "speckit-clarify"
    assert rows[0]["fase"] == "ESPEC"


def test_resposta_do_painel_com_intervencao_e_reconhecida(tmp_path: Path, dados_dir: Path):
    main = tmp_path / "proj" / "sess_ask2.jsonl"
    records = [
        _slash_str(0, "speckit-implement"),
        _assistant(1, "msg_1"),
        _ask_answer(2, "INTERVENÇÃO [redirecionamento|prd]: Section 2 says extension screens are out of scope."),
        _assistant(3, "msg_2"),
        _user(4, "/coletar-sessao F000"),
    ]
    _write_jsonl(main, records)
    resultado = cs.coletar(ciclo="a", id_rf="F000", mode="skill", transcript_path=main, dados_dir=dados_dir)
    assert resultado.n_intervencoes == 1


def test_ask_user_answers_formas():
    assert cs.ask_user_answers(_ask_answer(0, "x")) == ["x"]
    assert cs.ask_user_answers(_user(0, "oi")) is None  # mensagem humana nao e resposta de painel
    assert cs.ask_user_answers(_assistant(0, "m")) is None
    assert cs.is_researcher_record(_ask_answer(0, "x")) is True
    multi = _ask_answer(0, "a")
    multi["toolUseResult"]["answers"] = {"q1": ["a", "b"], "q2": "c"}
    assert cs.ask_user_answers(multi) == ["a, b", "c"]


def test_espera_pela_resposta_do_painel_tem_teto_de_pausa(tmp_path: Path):
    # a resposta chega 40 min depois da pergunta: 30 min contam, 10 vao para pausa_s
    base = _ask_answer(0, "x")
    base["timestamp"] = "2026-10-01T11:40:00.000Z"
    ant = _assistant(0, "m1")
    ant["timestamp"] = "2026-10-01T11:00:00.000Z"
    tempos = cs.compute_tempos([ant, base])
    assert tempos.pausa_s == 10 * 60
    assert tempos.duracao_s == 30 * 60


def _at(rec: dict, ts: str) -> dict:
    rec["timestamp"] = ts
    return rec


def _fim_de_turno(ts: str) -> dict:
    r = _at(_assistant(0, "mfim"), ts)
    r["message"]["stop_reason"] = "end_turn"
    return r


def test_espera_longa_depois_do_fim_do_turno_com_registro_de_sistema_tem_teto(tmp_path: Path):
    # D-024: o agente termina o turno; a conversa fica aberta horas; ao voltar o
    # pesquisador, o primeiro registro gravado é de sistema (`queue-operation`),
    # não uma mensagem humana. A espera é do pesquisador: conta 30 min, o resto é pausa_s.
    fim = _fim_de_turno("2026-10-17T20:00:00.000Z")
    fila = {"type": "queue-operation", "operation": "enqueue", "timestamp": "2026-10-18T08:00:00.000Z"}
    fila2 = {"type": "queue-operation", "operation": "dequeue", "timestamp": "2026-10-18T08:00:01.000Z"}
    tempos = cs.compute_tempos([fim, fila, fila2])
    assert tempos.duracao_s == 30 * 60 + 1
    assert tempos.pausa_s == 12 * 3600 - 30 * 60


def test_resultado_de_ferramenta_demorado_conta_inteiro(tmp_path: Path):
    # o agente espera uma ferramenta (testes, build) por 40 min: é trabalho dele, conta inteiro
    uso = _at(_assistant(0, "m1"), "2026-10-17T20:00:00.000Z")
    uso["message"]["stop_reason"] = "tool_use"
    resultado = {"type": "user", "timestamp": "2026-10-17T20:40:00.000Z", "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "t1", "content": "ok"}]}}
    tempos = cs.compute_tempos([uso, resultado])
    assert tempos.duracao_s == 40 * 60
    assert tempos.pausa_s == 0


def test_retempos_so_altera_duracao_e_pausa(tmp_path: Path, dados_dir: Path):
    # sessão antiga coletada com a regra anterior: duracao_s inflado pela espera
    main = tmp_path / "proj" / "sessX.jsonl"
    fim = _fim_de_turno("2026-10-17T20:00:00.000Z")
    inicio = _at(_user(0, "/speckit-plan"), "2026-10-17T19:50:00.000Z")
    fila = {"type": "queue-operation", "operation": "enqueue", "timestamp": "2026-10-18T08:00:00.000Z"}
    coleta = _at(_user(1, "/coletar-sessao RF06"), "2026-10-18T08:00:02.000Z")
    _write_jsonl(main, [inicio, fim, fila, coleta])
    bruto = dados_dir / "brutos" / "sessX.jsonl"
    bruto.parent.mkdir(parents=True, exist_ok=True)
    bruto.write_text(main.read_text(encoding="utf-8"), encoding="utf-8")
    campos = cs.CSV_FIELDS["sessoes.csv"]
    linha = {c: "" for c in campos}
    linha.update({"ciclo": "a", "id_rf": "RF06", "sessao_id": "sessX", "tipo_sessao": "desenvolvimento",
                  "modo_coleta": "skill", "motivo_fim": "normal", "duracao_s": 12 * 3600, "pausa_s": 0, "n_processo": 2})
    cs.append_csv(dados_dir / "sessoes.csv", campos, linha)

    situacao, faixas = cs.retempos(ciclo="a", dados_dir=dados_dir)
    assert situacao == [("sessX", "RF06", "tempo corrigido")]
    assert faixas["RF06"] == "abaixo de 50%"
    import csv as _csv
    with (dados_dir / "sessoes.csv").open(newline="", encoding="utf-8") as f:
        row = next(_csv.DictReader(f))
    assert int(row["duracao_s"]) == 10 * 60 + 30 * 60  # 10 min de trabalho + teto de 30 min da espera
    assert int(row["pausa_s"]) == 12 * 3600 - 30 * 60
    assert row["n_processo"] == "2"
    # 2ª rodada: nada muda
    assert cs.retempos(ciclo="a", dados_dir=dados_dir)[0] == [("sessX", "RF06", "inalterada")]


# ---------------------------------------------------------------------------
# D-049: registro sintético de limite de uso
# ---------------------------------------------------------------------------

_TEXTO_LIMITE = "You've hit your session limit \u00b7 resets 12:30pm (America/Sao_Paulo)"


def _limite(ts: str, texto: str = _TEXTO_LIMITE) -> dict:
    return {
        "type": "assistant",
        "timestamp": ts,
        "isApiErrorMessage": True,
        "message": {
            "id": "synth1",
            "model": "<synthetic>",
            "role": "assistant",
            "content": [{"type": "text", "text": texto}],
            "usage": {"input_tokens": 0, "output_tokens": 0},
        },
    }


def test_registro_sintetico_nao_entra_nos_modelos():
    uso = cs.accumulate_usage([_assistant(0, "m1"), _limite("2026-10-01T10:05:00.000Z")])
    assert uso.modelos == {"claude-sonnet-5"}


def test_limite_de_uso_e_reconhecido_e_o_reinicio_lido_no_fuso_do_texto():
    rec = _limite("2026-10-27T15:21:41.000Z")
    assert cs.is_limit_message(rec)
    assert cs.agent_turn_ended(rec)
    assert cs.limit_reset_ts(rec).isoformat() == "2026-10-27T15:30:00+00:00"  # 12:30 em Sao Paulo
    # reinício "no dia seguinte": 23h50 locais, reinício à 1:00am
    noite = _limite("2026-10-28T02:50:00.000Z", "You've hit your session limit \u00b7 resets 1am (America/Sao_Paulo)")
    assert cs.limit_reset_ts(noite).isoformat() == "2026-10-28T04:00:00+00:00"
    # mensagem sintética que não fala de limite, ou texto sem horário legível
    assert not cs.is_limit_message(_limite("2026-10-27T15:21:41.000Z", "Request timed out"))
    assert cs.limit_reset_ts(_limite("2026-10-27T15:21:41.000Z", "You've hit your session limit")) is None


def test_espera_pelo_reinicio_do_limite_sai_do_tempo_ativo():
    # limite às 12h21 locais (15:21Z), reinício às 12h30; o pesquisador volta às 13h20 (16:20Z):
    # 8 min 19 s de limite; dos 50 min 40 s restantes, 30 contam e 20 min 40 s vão para pausa_s
    antes = _at(_assistant(0, "m1"), "2026-10-27T15:20:41.000Z")
    limite = _limite("2026-10-27T15:21:41.000Z")
    fila = {"type": "queue-operation", "operation": "enqueue", "timestamp": "2026-10-27T16:20:40.000Z"}
    tempos = cs.compute_tempos([antes, limite, fila])
    assert tempos.rate_limit_s == 8 * 60 + 19
    assert tempos.duracao_s == 60 + 30 * 60
    assert tempos.pausa_s == 50 * 60 + 40 - 30 * 60
    assert tempos.duracao_bruta_s == 3599


def test_limite_sem_horario_legivel_tira_a_espera_inteira():
    antes = _at(_assistant(0, "m1"), "2026-10-27T15:20:41.000Z")
    limite = _limite("2026-10-27T15:21:41.000Z", "You've hit your session limit")
    fila = {"type": "queue-operation", "operation": "enqueue", "timestamp": "2026-10-27T16:21:41.000Z"}
    tempos = cs.compute_tempos([antes, limite, fila])
    assert tempos.rate_limit_s == 3600
    assert tempos.duracao_s == 60
    assert tempos.pausa_s == 0


def test_sem_limite_de_uso_rate_limit_s_e_zero_mesmo_com_texto_parecido():
    # D-044: código do app com "RATE_LIMITED" não é espera por limite de uso
    antes = _at(_assistant(0, "m1", text="retry on RATE_LIMITED and rate limit codes"), "2026-10-27T10:00:00.000Z")
    depois = _at(_assistant(1, "m2", text="done"), "2026-10-27T10:30:00.000Z")
    tempos = cs.compute_tempos([antes, depois])
    assert tempos.rate_limit_s == 0
    assert tempos.duracao_s == 30 * 60


def test_retempos_corrige_custo_e_modelo_de_linha_synthetic(tmp_path: Path, dados_dir: Path):
    sid = "sessS"
    inicio = _at(_user(0, "/bmad-code-review"), "2026-10-27T15:06:51.000Z")
    ag = _at(_assistant(1, "m1", tokens_in=100, tokens_out=50), "2026-10-27T15:20:41.000Z")
    limite = _limite("2026-10-27T15:21:41.000Z")
    fila = {"type": "queue-operation", "operation": "enqueue", "timestamp": "2026-10-27T16:20:40.000Z"}
    coleta = _at(_user(2, "/coletar-sessao F000"), "2026-10-27T16:43:54.000Z")
    bruto = dados_dir / "brutos" / f"{sid}.jsonl"
    _write_jsonl(bruto, [inicio, ag, limite, fila, coleta])
    sub = _assistant(3, "s1", tokens_in=10, tokens_out=5)
    sub["sessionId"] = sid
    sub_limite = _limite("2026-10-27T15:21:18.000Z")
    sub_limite["sessionId"] = sid
    outro = _assistant(4, "o1", tokens_in=999, tokens_out=999)
    outro["sessionId"] = "outra-sessao"
    _write_jsonl(dados_dir / "brutos" / "agent-aaa.jsonl", [sub, sub_limite])
    _write_jsonl(dados_dir / "brutos" / "agent-bbb.jsonl", [outro])
    campos = cs.CSV_FIELDS["sessoes.csv"]
    linha = {c: "" for c in campos}
    linha.update({"ciclo": "b", "id_rf": "F000", "sessao_id": sid, "tipo_sessao": "desenvolvimento",
                  "modo_coleta": "skill", "motivo_fim": "normal", "duracao_s": 5400, "pausa_s": 0,
                  "rate_limit_s": 0, "custo_usd": 0.0, "modelo": "<synthetic>"})
    cs.append_csv(dados_dir / "sessoes.csv", campos, linha)

    situacao, _ = cs.retempos(ciclo="b", dados_dir=dados_dir)
    assert situacao == [(sid, "F000", "tempo, custo e modelo corrigidos")]
    import csv as _csv
    with (dados_dir / "sessoes.csv").open(newline="", encoding="utf-8") as f:
        row = next(_csv.DictReader(f))
    assert row["modelo"] == "claude-sonnet-5"
    assert float(row["custo_usd"]) > 0
    assert int(row["rate_limit_s"]) == 8 * 60 + 19
    assert int(row["pausa_s"]) == 50 * 60 + 40 - 30 * 60
    # só o subagente da própria sessão entra no custo
    precos = cs.load_precos()["claude-sonnet-5"]
    esperado = (100 + 10) * precos["input"] + (50 + 5) * precos["output"]
    assert float(row["custo_usd"]) == pytest.approx(esperado, abs=1e-6)
    # 2ª rodada: o modelo já não é <synthetic>, nada muda
    assert cs.retempos(ciclo="b", dados_dir=dados_dir)[0] == [(sid, "F000", "inalterada")]


# ---------------------------------------------------------------------------
# 3. Compactação no meio
# ---------------------------------------------------------------------------


def test_compactacao_no_meio(tmp_path: Path, dados_dir: Path):
    main = tmp_path / "proj" / "sess3.jsonl"
    records = [
        _user(0, "oi"),
        _assistant(1, "msg_1"),
        {
            "type": "system",
            "subtype": "compact_boundary",
            "timestamp": _ts(2),
            "compactMetadata": {"triggerType": "auto", "preCompactionTokens": 1000, "postCompactionTokens": 100},
        },
        _user(3, "continuando"),
        _assistant(4, "msg_2"),
        _user(5, "/coletar-sessao RF04"),
    ]
    _write_jsonl(main, records)

    resultado = cs.coletar(ciclo="a", id_rf="RF04", mode="skill", transcript_path=main, dados_dir=dados_dir)

    import csv

    with (dados_dir / "sessoes.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["n_compactacoes"] == "1"
    # a compactação não pode ter quebrado a soma dos tokens das duas respostas
    assert rows[0]["tokens_input"] == "20"
    assert rows[0]["tokens_output"] == "10"


# ---------------------------------------------------------------------------
# 4. Subagente com tokens em arquivo separado
# ---------------------------------------------------------------------------


def test_subagente_arquivo_separado(tmp_path: Path, dados_dir: Path):
    session_id = "sess4"
    main = tmp_path / "proj" / f"{session_id}.jsonl"
    records = [
        _user(0, "rode uma busca"),
        _assistant(1, "msg_1", tokens_in=10, tokens_out=5),
        _user(2, "/coletar-sessao RF05"),
    ]
    _write_jsonl(main, records)

    sub_path = tmp_path / "proj" / session_id / "subagents" / "workflows" / "run1" / "agent-1.jsonl"
    sub_records = [
        _assistant(1, "sub_msg_1", tokens_in=100, tokens_out=50, model="claude-sonnet-5"),
    ]
    _write_jsonl(sub_path, sub_records)

    resultado = cs.coletar(ciclo="a", id_rf="RF05", mode="skill", transcript_path=main, dados_dir=dados_dir)
    assert resultado is not None

    import csv

    with (dados_dir / "sessoes.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["tokens_input"] == "10"
    assert rows[0]["tokens_output"] == "5"
    # soma do subagente entra nas colunas sub_* (nunca misturada com o principal)
    assert rows[0]["sub_tokens_input"] == "100"
    assert rows[0]["sub_tokens_output"] == "50"

    # o JSONL do subagente também é copiado para dados/<ciclo>/brutos/
    assert (dados_dir / "brutos" / "agent-1.jsonl").exists()
    assert (dados_dir / "brutos" / f"{session_id}.jsonl").exists()


def test_subagente_modelo_diferente_do_esperado_eh_detectavel(tmp_path: Path, dados_dir: Path):
    """P1c exige claude-sonnet-5 nos subagentes; o script precisa deixar o
    modelo visível (não resolve isto por conta própria, só expõe o dado) —
    GATE-C21 confere isto contra uma sessão real."""
    session_id = "sess5"
    main = tmp_path / "proj" / f"{session_id}.jsonl"
    _write_jsonl(main, [_user(0, "oi"), _assistant(1, "msg_1"), _user(2, "/coletar-sessao RF06")])

    sub_path = tmp_path / "proj" / session_id / "subagents" / "workflows" / "run1" / "agent-1.jsonl"
    _write_jsonl(sub_path, [_assistant(1, "sub_msg_1", model="claude-opus-5-5")])

    sub_transcripts = cs.find_subagent_transcripts(main)
    assert len(sub_transcripts) == 1
    sub_records = cs.load_jsonl(sub_transcripts[0])
    sub_usage = cs.accumulate_usage(sub_records)
    assert sub_usage.modelos == {"claude-opus-5-5"}  # != claude-sonnet-5 -> ameaça do P1c, a registrar à mão


# ---------------------------------------------------------------------------
# Contexto de IDE (P2)
# ---------------------------------------------------------------------------


def test_contexto_ide_detectado_e_removido_do_texto():
    rec = _user(0, "<ide_selection>The user selected lines 1 to 3 from /x.md:\n...\n</ide_selection>oi")
    assert cs.has_ide_context(rec)
    assert cs.human_message_text(rec) == "oi"


def test_mensagem_sem_contexto_ide_nao_e_marcada():
    rec = _user(0, "oi")
    assert not cs.has_ide_context(rec)


# ---------------------------------------------------------------------------
# Os três modos (skill / hook / manual) — critério do C-016
# ---------------------------------------------------------------------------


def test_modo_hook_usa_sessao_inteira_sem_cortar_invocacao(tmp_path: Path, dados_dir: Path):
    """No modo hook não há mensagem de invocação da skill para cortar — a
    sessão é usada inteira, corte = última mensagem (SessionEnd)."""
    main = tmp_path / "proj" / "sess_hook.jsonl"
    records = [_user(0, "oi"), _assistant(1, "msg_1", tokens_in=10, tokens_out=5)]
    _write_jsonl(main, records)

    resultado = cs.coletar(ciclo="b", id_rf="RF07", mode="hook", transcript_path=main, dados_dir=dados_dir)
    assert resultado.n_intervencoes == 0

    import csv

    with (dados_dir / "sessoes.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["modo_coleta"] == "hook"
    assert rows[0]["tokens_input"] == "10"


def test_modo_manual_registra_motivo_fim(tmp_path: Path, dados_dir: Path):
    main = tmp_path / "proj" / "sess_manual.jsonl"
    records = [_user(0, "oi"), _assistant(1, "msg_1")]
    _write_jsonl(main, records)

    cs.coletar(
        ciclo="b", id_rf="RF08", mode="manual", motivo_fim="limite_uso",
        transcript_path=main, dados_dir=dados_dir,
    )

    import csv

    with (dados_dir / "sessoes.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["modo_coleta"] == "manual"
    assert rows[0]["motivo_fim"] == "limite_uso"
