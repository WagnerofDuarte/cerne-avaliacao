# Aprendizado prévio do Ciclo A (GATE-X02)

**Autor:** Wagner (pesquisador). **Data:** 25/10/2026.
**Redação:** rascunho escrito pelo assistente, em primeira pessoa e a pedido do pesquisador, **somente com o que está registrado** nas notas e nos desvios do Ciclo A (`plano-ciclos.md`, `desvios.md`); o pesquisador revisa e confirma antes do `GATE-X02` ser marcado.
**Para que serve:** registrar o que o pesquisador aprendeu no Ciclo A e que pode influenciar o Ciclo B. Vira uma subseção de ameaças à validade (ordem fixa A → B, D18). Sem números de métrica.

A partir daqui: **não abrir `cerne-ciclo-a`** (nem `git log`, nem VS Code) até o `cicloB/final`.

## 1. Backend e ambiente hospedado
- Aprendi que o backend hospedado (Supabase) precisa estar pronto antes da primeira sessão: no A, o cadastro por e-mail estava desligado e a chave `anon` dos `.env` estava mascarada, e isso custou sessões de correção da F000 (D-017, D-018). No B conferi tudo no `GATE-X01` (*Confirm email* desligado, hash de schema, réplica, chamada autenticada).
- As contas do seed não têm perfil no backend; a conta criada pelo cadastro do app tem. Por isso desenvolvo e testo só com contas criadas pelo app, nunca com as do seed.
- Com `REPLAY_MODE=replay`, o que já foi perguntado vem do cache e o que é novo vai ao vivo. No A, uma pergunta nova do chat falhou no aparelho mesmo com o backend funcionando (RF04), então sei que defeito de chat ao vivo pode ser do app e não do backend.
- O filtro de data do app só oferece Todo o período, Esta semana e Este mês, e a exportação só envia o período ao backend. Por isso o estado "Período vazio" só aparece numa conta nova sem entradas (D-034).
- O texto gerado pela IA vem com Markdown literal (`**`, `#`); aprendi a anotar e não tratar como defeito do app.

## 2. Dispositivo físico (iPhone)
- O app só abre pelo `flutter run`, em modo debug (regra do iOS 14+); depois de reiniciar o Mac, o iPhone pediu *Developer Mode* mesmo já habilitado, e resolvi destravando o aparelho e abrindo a janela de Devices do Xcode (RF05).
- Muitos critérios dependem de tempo real no aparelho: Face ID e PIN, 5 minutos em segundo plano (RF03), 2 minutos de inatividade e Modo Avião (RF08), sessão expirada (RF07), microfone e câmera reais (RF01), compartilhar o PDF (RF05).
- Defeitos de comportamento só apareceram no iPhone, depois de a suíte do agente passar: gatilho por inatividade em conversa nova (RF08), diálogo de exclusão sem o provedor do bloc, "Sair" caindo na biometria e vazamento de dados entre contas (RF09).
- Estados vazios e de erro precisam de uma conta nova, de conexão cortada ou de uma sessão invalidada; aprendi a preparar isso antes da P6 (conta vazia, mais de 30 entradas criadas pelo modal).

## 3. Pacotes e ferramentas
- Pacotes que pesaram: `whisper_ggml` (modelo grande, `Podfile` novo e tempo de build, RF01/RF02) e `share_plus` (RF05).
- O Xcode se atualizou sozinho no meio do A (24/10, D-038); passei a conferir versões antes de cada ciclo.
- O agente às vezes faz por conta própria o que a P6 reserva a mim: rodar o app num simulador (F000), rodar testes com `--coverage` (RF01, RF05, RF09) ou tentar build (RF04, quando mandei não buildar sozinho). Anoto sem corrigir.
- A suíte do agente passar não significa que o critério foi atendido; a P6 no aparelho continua sendo o árbitro.

## 4. O jeito de trabalhar com o agente e com o protocolo
- Regras que aprendi, por erros de execução meus e do guia, e que valem no B: uma coleta só, no fim, com nada rodando em segundo plano (D-031, D-035); sessão descartada também é sessão medida e precisa de coleta (D-037); respostas às pausas previstas são `PROCESSO:` e nunca intervenção (D-030); mensagens de intervenção e de processo digitadas à mão, nunca coladas (D-020); a pasta de memória do agente conferida depois de cada coleta (D-033).
- Para descrever defeitos de tela uso uma intervenção por tela, qualitativa e sem números de estilo (D-019); para sintoma repetido, uso a frase de investigação (D-025).
- Os erros de execução vieram quando misturei passos ou fiz coisas fora da ordem (coletar antes do fim, abrir sessão sem coletar a anterior); por isso, no B, sigo a ordem do guia passo a passo.
- Os roteiros da P6 que ajudaram foram os que criam o estado antes de testar (conta vazia, entradas suficientes); os que atrapalharam foram os que assumiam um estado que a tela não oferece (D-023, D-034).

## 5. O que pode enviesar o B
- Já conheço o protótipo e o backend, então reconheço cedo diferenças de design e defeitos de backend e sei descrever o sintoma de forma curta e objetiva; isso pode reduzir ou antecipar sessões de correção no B em relação ao A.
- Sei quais critérios costumam falhar (design contra o protótipo, estados vazio, offline e de sessão expirada, tempo real no aparelho) e vou testá-los desde a primeira rodada da P6; no A, vários só apareceram nas rodadas seguintes.
- Conheço as regras de intervenção e coleta; devo cometer menos erros de execução no B do que no A.
- O B tem prazo mais curto (até 04/11, D-021) e ritmo mais alto; isso pode aumentar a chance de erro de execução meu por cansaço ou pressa.
- Conheço o que o Spec Kit pergunta e o que o agente costuma decidir sozinho; não conheço o equivalente do BMAD e vou aprender enquanto uso.
- Não vou tentar compensar nada disso: o protocolo manda tratar os dois ciclos da mesma forma e registrar o que acontecer.
