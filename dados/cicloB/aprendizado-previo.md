# Aprendizado prévio do Ciclo A (GATE-X02)

**Autor:** Wagner (pesquisador). **Data:** 25/10/2026.
**Para que serve:** registrar o que o pesquisador aprendeu no Ciclo A e que pode influenciar o Ciclo B. Vira uma subseção de ameaças à validade (ordem fixa A → B, D18). **Escrever com as suas palavras, 2 a 4 linhas por tópico.** Não é para listar números de métrica. As "pistas" abaixo são só lembretes do que ficou registrado no A; apague o que não se aplica e acrescente o que faltar.

A partir daqui: **não abrir `cerne-ciclo-a`** (nem `git log`, nem VS Code) até o `cicloB/final`.

## 1. Backend e ambiente hospedado
*Pistas:* cadastro por e-mail estava desligado no Supabase (D-017); a chave `anon` dos `.env` estava mascarada (D-018); `REPLAY_MODE=replay` e perguntas novas do chat que demoram a responder; o filtro de data só oferece Todo o período, Esta semana e Este mês (D-034); contas do seed não têm perfil, e a conta nova do cadastro tem.

(escreva aqui)

## 2. Dispositivo físico (iPhone)
*Pistas:* o app só abre pelo `flutter run`, em modo debug; erro de *Developer Mode* depois de reiniciar o Mac; Face ID, PIN e 5 minutos em segundo plano exigem espera real; teclado cobrindo modal; microfone e câmera reais; Modo Avião e inatividade de 2 minutos exigem tempo.

(escreva aqui)

## 3. Pacotes e ferramentas
*Pistas:* `whisper_ggml` (modelo grande, Podfile, tempo de build), `share_plus`, build do Xcode, atualização automática do Xcode no meio do A (D-038), `flutter test` e `analyze` limpos que não pegaram defeitos que só apareceram no aparelho.

(escreva aqui)

## 4. O jeito de trabalhar com o agente e com o protocolo
*Pistas:* o que você faria diferente na rotina de sessões (coleta única, nada em segundo plano, sessão descartada precisa de coleta, `PROCESSO:` nas pausas previstas, nada colado), o que ficou mais rápido com a prática, o que ainda dá erro de execução; roteiros da P6 que ajudaram ou atrapalharam (conta vazia, mais de 30 entradas).

(escreva aqui)

## 5. O que pode enviesar o B
*Pistas:* você já conhece o protótipo e o backend, então vai reconhecer cedo defeitos de design e de backend; sabe quais critérios costumam falhar; sabe o que o Spec Kit pergunta e o que o agente costuma decidir sozinho. Escreva em que pontos isso pode favorecer ou atrapalhar o BMAD no B, **sem tentar compensar** (o protocolo manda tratar igual).

(escreva aqui)
