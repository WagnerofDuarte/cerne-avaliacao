"""Tabela de cenarios do addon (C-018 manipulacoes, C-019 15 falhas, C-020 estados transitorios).

Cada cenario = lista de regras. Regra: dict com
  fn        funcao-alvo (`x-cerne-function` ou ultimo segmento de /functions/v1/<fn>); '*' = qualquer
  acao      fault | hold | sse_cut | forge_401 | offline_all | rewrite
  valor     fault: timeout|malformed|offline|ai_timeout; hold: segundos; sse_cut: n de eventos token;
            rewrite: {campo: regex_da_chave, valor: texto}
  limite    quantas chamadas-alvo sofrem a acao (padrao 1 = so a primeira apos `arm`); None = todas
  pular     quantas chamadas-alvo deixar passar antes de agir (padrao 0)
ATENCAO: nomes de funcao, formato de SSE e corpos de resposta sao SUPOSICOES a conferir contra o
backend real (cerne-backend nao esta neste checkout). Ver docs/trilha-harness-notas.md.
"""
FALHAS = ("timeout", "malformed", "offline")
_ALVOS = {"entries-create": "F01", "chat-messages-send": "F04", "media-ocr": "F07", "export-summary-create": "F10", "chat-insight-create": "F13"}

CENARIOS = {}
for fn, base in _ALVOS.items():
    n = int(base[1:])
    for i, f in enumerate(FALHAS):
        CENARIOS[f"F{n + i:02d}"] = [{"fn": fn, "acao": "fault", "valor": f, "limite": 1}]

CENARIOS.update({
    # C-018 — manipulacao de trafego ou falhas pontuais
    "H04-1": [{"fn": "chat-messages-send", "acao": "fault", "valor": "ai_timeout", "limite": 1, "pular": 1}],  # a 2a mensagem falha
    "H04-2": [{"fn": "chat-messages-send", "acao": "sse_cut", "valor": 3, "limite": 1}],
    "H05-2": [{"fn": "export-summary-create", "acao": "fault", "valor": "ai_timeout", "limite": 1}],
    "H06-3": [{"fn": "*", "acao": "offline_all", "limite": None}],
    "H07-1": [{"fn": "*", "acao": "forge_401", "limite": None}],
    "H08-3": [{"fn": "chat-insight-create", "acao": "fault", "valor": "ai_timeout", "limite": 1}],
    "H09-3a": [{"fn": "dashboard-narrative-get", "acao": "rewrite", "valor": {"campo": "narrative|text|summary", "valor": "x" * 4000}, "limite": 1}],
    "H09-3b": [{"fn": "dashboard-narrative-get", "acao": "rewrite", "valor": {"campo": "narrative|text|summary", "valor": ""}, "limite": 1}],
    "H10-3": [{"fn": "entries-create", "acao": "fault", "valor": "offline", "limite": 1}],
    "H01-1": [],  # sem manipulacao: so registra
    "H06-2": [],  # so contagem
    # C-020 — estados transitorios / de erro (screenshots da M9)
    "t2foto_processing": [{"fn": "media-ocr", "acao": "hold", "valor": 30, "limite": 1}],
    "t2audio_processing": [{"fn": "media-transcribe", "acao": "hold", "valor": 30, "limite": 1}],
    "home_streaming": [{"fn": "chat-messages-send", "acao": "hold", "valor": 30, "limite": 1}],
    "exp_pending": [{"fn": "export-status-get", "acao": "hold", "valor": 30, "limite": 1}],
    "exp_processing": [{"fn": "export-status-get", "acao": "rewrite", "valor": {"campo": "^status$", "valor": "processing"}, "limite": 1}],
    "exp_error": [{"fn": "export-summary-create", "acao": "fault", "valor": "ai_timeout", "limite": 1}],
    "sessao": [{"fn": "*", "acao": "forge_401", "limite": None}],
    "dashNarrativeError": [{"fn": "dashboard-narrative-get", "acao": "fault", "valor": "ai_timeout", "limite": 1}],
})
