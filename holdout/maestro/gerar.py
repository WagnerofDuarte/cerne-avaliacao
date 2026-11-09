#!/usr/bin/env python3
"""Gera os fluxos Maestro (um por cenario do C-018, um por falha do C-019 e um por estado do C-020) e o
manifesto `holdout/suite.json`. Os YAML gerados ficam versionados ao lado; a fonte da verdade e este arquivo.

Regras de escrita (cenarios.md §0): elementos identificados por TEXTO VISIVEL DO PROTOTIPO; icones sem texto por
posicao no frame 390x844 (porcentagem, vale para o frame real do aparelho). Onde cenarios.md e prototipo
divergem, o fluxo usa o texto do PROTOTIPO e leva a marca `# DIVERGENCIA`. Fluxos NAO validados em app (regra 8):
so revisados por leitura (ver verificar.py).
"""
from __future__ import annotations

import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
TX = json.loads((RAIZ / "fixtures" / "textos.json").read_text())
TXI = json.loads((RAIZ / "fixtures" / "textos-instrumento.json").read_text())
texto = lambda k: TX[k]["texto"] if k in TX else TXI[k]

# posicoes (x%,y% do frame 390x844), medidas no HTML de referencia com Playwright (±4 px; conferir no aparelho)
PT = {"menu": "7%,8%", "plus": "6%,97%", "enviar": "94%,97%", "download": "93%,8%", "funil": "91%,14%",
      "marcador": "94%,88%", "fechar_modal": "93%,8%"}
S1, S2 = "Conversa sobre o dia no trabalho", "Conversa sobre o sono"   # sessoes semeadas (dado do backend, nao do prototipo)
CONTAS = {"A": "cenario-cheio@cerne.test", "B": "cenario-uma@cerne.test", "C": "cenario-vazio@cerne.test"}

# ----------------------------------------------------------------------------- DSL de passos
tap = lambda t, opt=False: ("tap", t, opt)
pt = lambda n: ("pt", n)
inp = lambda t: ("in", t)
ok = lambda t: ("ok", t)
no = lambda t: ("no", t)
shot = lambda n: ("shot", n)
esp = lambda s: ("esp", s)
arm = lambda c: ("arm", c)
disarm = ("disarm",)
chk = lambda q, marca=False: ("chk", q, marca)
nota = lambda t: ("nota", t)
entrar = lambda c: ("entrar", c)
conversa = lambda n: ("conversa", n)
enviar = lambda t: ("enviar", t)
registros = ("registros",)
bg = lambda s: ("bg", s)


def render(passos):
    out = []
    for p in passos:
        k = p[0]
        if k == "tap":
            out += [f"- tapOn:\n    text: {json.dumps(p[1], ensure_ascii=False)}\n    optional: true"] if p[2] else [f"- tapOn: {json.dumps(p[1], ensure_ascii=False)}"]
        elif k == "pt":
            out.append(f"- tapOn:\n    point: \"{PT[p[1]]}\"   # {p[1]}")
        elif k == "in":
            out.append(f"- inputText: {json.dumps(p[1], ensure_ascii=False)}")
        elif k == "ok":
            out.append(f"- assertVisible: {json.dumps(p[1], ensure_ascii=False)}")
        elif k == "no":
            out.append(f"- assertNotVisible: {json.dumps(p[1], ensure_ascii=False)}")
        elif k == "shot":
            out.append(f"- takeScreenshot: ${{CICLO_ANON}}-{p[1]}")
        elif k == "esp":   # espera em tempo real: espera por algo que nunca aparece, opcional (ver notas)
            out.append(f"- extendedWaitUntil:\n    visible: \"__espera_tempo_real__\"\n    timeout: {int(p[1]) * 1000}\n    optional: true")
        elif k == "arm":
            out.append(f"- runScript:\n    file: ../scripts/proxy.js\n    env: {{ACAO: arm, CENARIO: \"{p[1]}\"}}")
        elif k == "disarm":
            out.append("- runScript:\n    file: ../scripts/proxy.js\n    env: {ACAO: disarm}")
        elif k == "chk":
            if p[2]:
                out.append("- runScript:\n    file: ../scripts/agora.js")
            env = f"{{QUERY: \"{p[1]}\"" + (", MARCA_MS: \"${output.ms}\"" if p[2] else "") + "}"
            out.append(f"- runScript:\n    file: ../scripts/checar.js\n    env: {env}\n- assertTrue: ${{output.ok}}")
        elif k == "nota":
            out.append(f"# {p[1]}")
        elif k == "entrar":
            out.append(f"- runFlow:\n    file: _comum/entrar.yaml\n    env: {{EMAIL: \"{CONTAS[p[1]]}\", SENHA: \"${{SENHA_{p[1]}}}\"}}")
        elif k == "conversa":
            out.append(f"- runFlow:\n    file: _comum/conversa.yaml\n    env: {{CONVERSA: {json.dumps(p[1], ensure_ascii=False)}}}")
        elif k == "enviar":
            out.append(f"- runFlow:\n    file: _comum/enviar.yaml\n    env: {{TEXTO: {json.dumps(p[1], ensure_ascii=False)}}}")
        elif k == "registros":
            out.append("- runFlow: _comum/registros.yaml")
        elif k == "bg":
            out.append(f"- pressKey: Home      # iOS: enviar ao background\n- extendedWaitUntil:\n    visible: \"__espera_tempo_real__\"\n    timeout: {int(p[1]) * 1000}\n    optional: true\n- launchApp")
        else:
            raise ValueError(p)
    return "\n".join(out)


def flow(titulo, passos):
    return f"# {titulo}\nappId: ${{APP_ID}}\n---\n" + render(passos) + "\n"


# ----------------------------------------------------------------------------- C-018: 25 cenarios comportamentais
C018 = {}
C018["H01-1"] = ("RF01", "III", "A", None, ["tres_modalidades"], [
    entrar("A"), pt("plus"), tap("Texto"), inp(texto("entrada_manual_nova")), tap("Salvar"),
    pt("plus"), tap("Áudio"), nota("tocar audio_fixture_01.wav perto do microfone durante a gravacao"), tap("Toque para gravar"), esp(8), tap("Toque para gravar", True),
    ok("Transcrevendo..."), esp(15), tap("Salvar"),
    pt("plus"), tap("Foto"), tap("Galeria"), nota("escolher ocr_fixture_01.png"), ok("Reconhecendo texto..."), esp(15), tap("Salvar")])
C018["H01-2"] = ("RF01", "III", "A", None, ["contagem"], [
    entrar("A"), pt("plus"), tap("Áudio"), tap("Toque para gravar"), esp(3), pt("fechar_modal"), registros])
C018["H02-1"] = ("RF02", "III", "A", None, [], [
    entrar("A"), pt("plus"), tap("Áudio"), tap("Toque para gravar"), nota("cronometro correndo = estado 'gravando'"), esp(2),
    tap("Toque para gravar", True), ok("Transcrevendo..."), esp(15),
    nota("transcrito: texto editavel com a duracao do audio"),
    nota("erro de transcricao: nova gravacao de 2 s de SILENCIO"), ok("Não foi possível transcrever"), ok("Tentar novamente"),
    pt("fechar_modal"), pt("plus"), tap("Foto"), tap("Galeria"), nota("escolher ocr_fixture_ilegivel.png"),
    ok("Reconhecendo texto..."), ok("Não foi possível reconhecer o texto — tente outra foto."), ok("Tentar novamente"),
    nota("DIVERGENCIA: cenarios.md cita o botao 'Salvar só a foto'; esse texto NAO existe no prototipo")])
C018["H03-1"] = ("RF03", "III", "A", None, [], [
    entrar("A"), nota("bloquear o app (fluxo do app) e relancar"), tap("Toque para desbloquear"),
    nota("simular rosto nao reconhecido (aparelho fisico: cobrir a camera)"), ok("Não foi possível reconhecer — digite seu PIN"),
    nota("digitar o PIN cadastrado pelo fluxo do app (passo especifico do app)"), ok("Escreva uma mensagem...")])
C018["H03-2"] = ("RF03", "III", "A", None, [], [
    entrar("A"), ok("Escreva uma mensagem..."), bg(310), ok("Toque para desbloquear"), no("Escreva uma mensagem...")])
C018["H04-1"] = ("RF04", "I", "A", "H04-1", ["log_falha:chat-messages-send:ai_timeout"], [
    entrar("A"), conversa(S1), enviar(texto("sessao1_quinta_mensagem")), nota("(a) streaming: capturas sucessivas; texto cresce"),
    shot("H04-1-streaming"), esp(10), shot("H04-1-completa"), enviar("Mais uma mensagem para provocar a falha"),
    ok("Falha ao gerar resposta — toque para tentar novamente")])
C018["H04-2"] = ("RF04", "I", "A", "H04-2", ["mensagens_usuario"], [
    entrar("A"), conversa(S1), enviar("Mensagem seguinte do roteiro"), esp(5), nota("o proxy encerra o SSE apos o 3o token"),
    ok("Falha ao gerar resposta — toque para tentar novamente"), tap("Falha ao gerar resposta — toque para tentar novamente"),
    chk("regra=contagem&fn=chat-messages-retry&igual=1"), chk("regra=contagem&fn=chat-messages-send&igual=1")])
C018["H05-1"] = ("RF05", "II", "C", None, [], [
    entrar("C"), registros, pt("download"), nota("pedir a exportacao"), ok("Nenhum registro nesse período."), no("Baixar PDF"), no("Baixar dados brutos")])
C018["H05-2"] = ("RF05", "I", "A", "H05-2", ["log_falha:export-summary-create:ai_timeout"], [
    entrar("A"), registros, pt("download"), nota("pedir a exportacao"), esp(10), ok("Baixar dados brutos"), tap("Baixar dados brutos"),
    chk("regra=contagem&fn=export-download-get&igual=1")])
C018["H06-1"] = ("RF06", "I", "A", None, [], [
    entrar("A"), registros, tap("Buscar nos registros..."),
    nota("buscar, um por vez, os 3 termos de seeded-search-entries.md; comparar lista da UI com o corpo de entries-search no log do proxy"),
    chk("regra=contagem&fn=entries-search&min=3")])
C018["H06-2"] = ("RF06", "I", "A", "H06-2", [], [
    entrar("A"), registros, tap("Buscar nos registros..."), nota("digitar 'ansiedade' caractere a caractere com ~50 ms entre teclas"),
    inp("ansiedade"), esp(1), chk("regra=debounce&fn=entries-search&q=ansiedade&gap_ms=300", marca=True)])
C018["H06-3"] = ("RF06", "I", "A", "H06-3", ["contagem"], [
    entrar("A"), registros, shot("H06-3-com-rede"), arm("H06-3"), pt("menu"), tap("Meus Registros"), shot("H06-3-offline-cache"),
    disarm, esp(5), shot("H06-3-reconectado"), nota("nº de cartoes = contagem SQL; nenhuma entrada duplicada")])
C018["H06-4"] = ("RF06", "III", "A", None, ["filtro_fonte_mes"], [
    entrar("A"), registros, pt("funil"), ok("Filtrar registros"), ok("PERÍODO"), tap("Este mês"), ok("TIPO DE ENTRADA"), tap("Áudio"),
    tap("Aplicar"), chk("regra=contagem&fn=entries-search&source=audio&min=1"),
    nota("DIVERGENCIA: cenarios.md cita 'INTERVALO DE DATA'; o prototipo usa 'PERÍODO'")])
C018["H06-5"] = ("RF06", "III", "A", None, ["contagem"], [
    entrar("A"), registros, tap("Limpar filtros"), ok("Buscar nos registros..."), ok("Meus Registros")])
C018["H07-1"] = ("RF07", "I", "A", "H07-1", [], [
    entrar("A"), registros, nota("rolar ate o 15o cartao"), shot("H07-1-antes"), arm("H07-1"), pt("menu"), ok("Sessão expirada"),
    tap("Entrar novamente"), disarm, nota("reautenticar"), shot("H07-1-depois")])
C018["H08-1"] = ("RF08", "I", "A", None, [], [
    entrar("A"), conversa(S1), enviar(texto("sessao1_quinta_mensagem")), esp(10), ok("INSIGHT"),
    chk("regra=contagem&fn=chat-insight-create&igual=1"), nota("reabrir a sessao nao gera nova chamada"), conversa(S2), conversa(S1),
    chk("regra=contagem&fn=chat-insight-create&igual=1")])
C018["H08-2"] = ("RF08", "I", "A", None, [], [
    entrar("A"), conversa(S2), enviar(texto("sessao2_mensagem_1")), enviar(texto("sessao2_mensagem_2")), esp(130),
    chk("regra=contagem&fn=chat-insight-create&igual=1"), esp(120), chk("regra=contagem&fn=chat-insight-create&igual=1")])
C018["H08-3"] = ("RF08", "I", "A", "H08-3", ["log_falha:chat-insight-create:ai_timeout"], [
    entrar("A"), conversa(S1), enviar("Mensagem que dispara novo gatilho"), esp(10), enviar("Outra mensagem depois da falha do insight"),
    esp(10), no("Falha ao gerar resposta — toque para tentar novamente")])
C018["H08-4"] = ("RF08", "I", "A", None, [], [
    entrar("A"), conversa(S1), ok("INSIGHT"), shot("H08-4-antes"), nota("tocar no 'x' do cartao"), tap("Fechar"), no("INSIGHT"), shot("H08-4-depois")])
C018["H09-1"] = ("RF09", "II", "ABC", None, [], [
    entrar("C"), pt("menu"), tap("Configurações"),
    ok("Ainda não há registros suficientes para mostrar sua evolução. Comece a escrever para ver seu gráfico aqui."),
    nota("DIVERGENCIA: cenarios.md cita 'Comece a registrar para ver sua evolução aqui'; o prototipo traz o texto acima"),
    nota("repetir com a conta B (primeiro passo) e com a conta A (gráfico + resumo)"),
    ok("Você deu o primeiro passo. Continue registrando para ver padrões surgirem ao longo do tempo."),
    nota("DIVERGENCIA: cenarios.md cita 'Ainda é cedo pra ver um padrão — volte em alguns dias.'")])
C018["H09-2"] = ("RF09", "II", "B", None, [], [
    entrar("B"), pt("menu"), tap("Configurações"), shot("H09-2-antes"), nota("voltar a Home; criar uma entrada de texto; voltar a Configuracoes"),
    pt("plus"), tap("Texto"), inp(texto("entrada_manual_nova")), tap("Salvar"), pt("menu"), tap("Configurações"),
    chk("regra=contagem&fn=dashboard-aggregate-get&min=2"), shot("H09-2-depois")])
C018["H09-3"] = ("RF09", "II", "B", "H09-3a", [], [
    entrar("B"), arm("H09-3a"), pt("menu"), tap("Configurações"), ok("Sua evolução"), shot("H09-3-texto-longo"),
    arm("H09-3b"), pt("menu"), tap("Meus Registros"), pt("menu"), tap("Configurações"), ok("Sua evolução"), shot("H09-3-texto-vazio")])
C018["H10-2"] = ("RF10", "III", "A", None, ["idempotencia_chat"], [
    entrar("A"), conversa(S1), nota("marcador (bookmark) da mensagem sessao1_quinta_mensagem"), pt("marcador"), esp(5), pt("marcador"),
    chk("regra=contagem&fn=entries-create&max=2")])
C018["H10-3"] = ("RF10", "III", "A", "H10-3", ["log_falha:entries-create:offline"], [
    entrar("A"), conversa(S1), arm("H10-3"), pt("marcador"), esp(3), shot("H10-3-erro"), conversa(S2), conversa(S1),
    disarm, pt("marcador"), esp(5), shot("H10-3-salvo"), chk("regra=contagem&fn=entries-create&min=2")])
C018["H10-4"] = ("RF10", "I", "A", None, [], [
    entrar("A"), conversa(S1), nota("rolar a sessao inteira: todo balao do usuario tem marcador; nenhum balao da IA tem"), shot("H10-4-sessao")])

# ----------------------------------------------------------------------------- C-019: 15 falhas
FALHAS = {}
alvos = [("entries-create", "F01", [pt("plus"), tap("Texto"), inp("texto de teste das falhas"), tap("Salvar")], "Tentar novamente"),
         ("chat-messages-send", "F04", [enviar("mensagem de teste das falhas")], "Não foi possível enviar — toque para tentar novamente"),
         ("media-ocr", "F07", [pt("plus"), tap("Foto"), tap("Galeria"), nota("escolher ocr_fixture_01.png")], "Não foi possível reconhecer o texto — tente outra foto."),
         ("export-summary-create", "F10", [registros, pt("download")], "Tentar novamente")]
for fn, base, passos, esperado in alvos:
    for i, fl in enumerate(("timeout", "malformed", "offline")):
        fid = f"F{int(base[1:]) + i:02d}"
        FALHAS[fid] = (fn, fl, [entrar("A"), arm(fid), *passos, esp(3), ok(esperado), shot(f"{fid}-erro"), disarm,
                                nota("recuperacao: repetir a mesma acao SEM reiniciar o app; condicao 4 do criterio 'tratado'"), tap("Tentar novamente", True), esp(3), shot(f"{fid}-recuperado")])
for i, fl in enumerate(("timeout", "malformed", "offline")):
    fid = f"F{13 + i}"
    FALHAS[fid] = ("chat-insight-create", fl, [entrar("A"), conversa(S2), arm(fid), enviar(texto(f"rnf09_mensagem_{i + 1}")), esp(130),
                                              nota("condicao 2 nao se aplica: NENHUM erro visivel"), no("Não foi possível"), chk("regra=fault_injetado&fn=chat-insight-create"),
                                              disarm, enviar("mensagem depois da falha"), shot(f"{fid}-chat-segue")])

# ----------------------------------------------------------------------------- C-020: 31 estados (id, conta, proxy, passos)
E = {}
def est(i, conta, proxy, *passos): E[i] = (conta, proxy, list(passos))
est("splash", None, None, nota("abrir a frio; capturar no primeiro quadro estavel"), shot("splash"))
est("bio", "A", None, entrar("A"), nota("relancar o app com sessao salva"), ok("Toque para desbloquear"), shot("bio"))
est("login", None, None, nota("primeira abertura sem sessao"), ok("E-mail"), shot("login"))
est("pinInicial", "A", None, tap("Toque para desbloquear"), tap("Usar PIN"), ok("Digite seu PIN"), shot("pinInicial"))
est("pinErro", "A", None, tap("Toque para desbloquear"), nota("simular rosto nao reconhecido"), ok("Não foi possível reconhecer — digite seu PIN"), shot("pinErro"))
est("home", "A", None, conversa(S1), shot("home"))
est("t2texto", "A", None, pt("plus"), tap("Texto"), shot("t2texto"))
est("t2audio_recording", "A", None, pt("plus"), tap("Áudio"), tap("Toque para gravar"), shot("t2audio_recording"))
est("t2audio_processing", "A", "t2audio_processing", pt("plus"), tap("Áudio"), tap("Toque para gravar"), esp(3), tap("Toque para gravar", True), ok("Transcrevendo..."), shot("t2audio_processing"))
est("t2audio_transcribed", "A", None, pt("plus"), tap("Áudio"), tap("Toque para gravar"), esp(8), tap("Toque para gravar", True), esp(15), shot("t2audio_transcribed"))
est("t2audio_error", "A", None, pt("plus"), tap("Áudio"), tap("Toque para gravar"), nota("2 s de silencio"), esp(2), tap("Toque para gravar", True), ok("Não foi possível transcrever"), shot("t2audio_error"))
est("t2foto_idle", "A", None, pt("plus"), tap("Foto"), shot("t2foto_idle"))
est("t2foto_processing", "A", "t2foto_processing", pt("plus"), tap("Foto"), tap("Galeria"), nota("ocr_fixture_01.png"), ok("Reconhecendo texto..."), shot("t2foto_processing"))
est("t2foto_recognized", "A", None, pt("plus"), tap("Foto"), tap("Galeria"), nota("ocr_fixture_01.png"), esp(15), shot("t2foto_recognized"))
est("t2foto_error", "A", None, pt("plus"), tap("Foto"), tap("Galeria"), nota("ocr_fixture_ilegivel.png"), ok("Não foi possível reconhecer o texto — tente outra foto."), shot("t2foto_error"))
est("menu", "A", None, pt("menu"), ok("CONVERSAS"), shot("menu"))
est("sessao", "A", "sessao", pt("menu"), ok("Sessão expirada"), shot("sessao"))
est("registros", "A", None, registros, ok("Meus Registros"), shot("registros"))
est("vazio", "C", None, registros, ok("Nenhum registro ainda"), shot("vazio"))
est("filtro", "A", None, registros, pt("funil"), ok("Filtrar registros"), shot("filtro"))
est("filtrosAtivos", "A", None, registros, pt("funil"), tap("Áudio"), tap("Aplicar"), ok("Limpar filtros"), shot("filtrosAtivos"))
est("exp_pending", "A", "exp_pending", registros, pt("download"), ok("Preparando exportação..."), shot("exp_pending"))
est("exp_processing", "A", "exp_processing", registros, pt("download"), ok("Gerando resumo com IA..."), shot("exp_processing"))
est("exp_done", "A", None, registros, pt("download"), esp(15), ok("Resumo pronto"), shot("exp_done"))
est("exp_error", "A", "exp_error", registros, pt("download"), esp(10), ok("Baixar dados brutos"), shot("exp_error"))
est("exp_empty", "C", None, registros, pt("download"), ok("Nenhum registro nesse período."), shot("exp_empty"))
est("config", "A", None, pt("menu"), tap("Configurações"), ok("Sua evolução"), shot("config"))
est("dashZero", "C", None, pt("menu"), tap("Configurações"), shot("dashZero"))
est("dashUma", "B", None, pt("menu"), tap("Configurações"), shot("dashUma"))
est("dashNarrativeError", "A", "dashNarrativeError", pt("menu"), tap("Configurações"), ok("Não foi possível gerar o balanço agora"), shot("dashNarrativeError"))
est("excluir", "A", None, pt("menu"), tap("Configurações"), tap("Apagar conta"), ok("Apagar sua conta?"), shot("excluir"))


def main():
    manifesto = {"_nota": "Gerado por holdout/maestro/gerar.py. ordem dos blocos: I, II, III (cenarios.md §0); estruturais fora (analise estatica).",
                 "cenarios": {}, "falhas": {}, "estados": {}, "estruturais": ["H07-2", "H07-3", "H10-1"]}
    for cid, (rf, bloco, conta, proxy, sql, passos) in C018.items():
        (AQUI / f"{cid}.yaml").write_text(flow(f"{cid} ({rf}) — bloco {bloco}, conta {conta}", passos))
        manifesto["cenarios"][cid] = {"rf": rf, "bloco": bloco, "conta": conta, "flow": f"maestro/{cid}.yaml", "proxy": proxy, "sql": sql}
    for fid, (fn, fl, passos) in FALHAS.items():
        (AQUI / f"{fid}.yaml").write_text(flow(f"{fid} — {fn} / {fl} (rnf09.md)", passos))
        manifesto["falhas"][fid] = {"fn": fn, "falha": fl, "flow": f"maestro/{fid}.yaml", "proxy": fid, "sql": ["log_falha:%s:%s" % (fn, fl)] + (["contagem"] if fn == "entries-create" else [])}
    for sid, (conta, proxy, passos) in E.items():
        pre = [] if sid in ("splash", "login") or conta is None else ([] if passos and passos[0][0] == "entrar" else [])
        corpo = ([entrar(conta)] if conta and not any(p[0] == "entrar" for p in passos) and sid not in ("pinInicial", "pinErro") else []) + \
                ([arm(proxy)] if proxy else []) + passos + ([disarm] if proxy else [])
        (AQUI / f"M9-{sid}.yaml").write_text(flow(f"estado M9 `{sid}` (estados-m9.md, conta {conta or '—'})", corpo))
        manifesto["estados"][sid] = {"conta": conta, "flow": f"maestro/M9-{sid}.yaml", "proxy": proxy}
    (RAIZ / "suite.json").write_text(json.dumps(manifesto, indent=2, ensure_ascii=False) + "\n")
    print(len(C018), len(FALHAS), len(E))


if __name__ == "__main__":
    main()
