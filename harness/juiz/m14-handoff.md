# Rubrica M14 — a decisão do plano está implementada?

**Item:** uma das 8–10 decisões selecionadas pela regra do `C-022` (`harness/regras.md`, seção 1), num ciclo.
**Entrada enviada:** (1) o texto da decisão, anonimizado; (2) a árvore de `lib/` da tag `final`; (3) o conteúdo dos arquivos de `lib/` que contêm ao menos um dos termos-chave da decisão (os identificadores que a regra de seleção exigiu: pacote, classe, caminho), até 60 mil tokens, em ordem de número de ocorrências; se passar do limite, os demais arquivos entram só como caminho.

## Definições
- **sim:** o código faz o que a decisão diz, onde ela diz.
- **parcial:** a decisão aparece em parte do código aplicável e não em outra parte, ou foi aplicada de forma incompleta.
- **não:** o código não segue a decisão, ou faz o contrário.

## Prompt (v1.0)

```text
You check whether a technical DECISION from a design document was implemented in the CODE.

Answer "yes" if the code does what the decision says, where it says.
Answer "partial" if the decision is followed in some of the applicable code but not in all of it,
or only partly.
Answer "no" if the code does not follow the decision, or does the opposite.
Judge only this decision. Cite evidence as file:line. If you cannot find the relevant code in the
material given, answer "no" and say so in the justification.

Answer only with JSON matching the schema.

DECISION:
<<<DECISION>>>

FILE TREE:
<<<TREE>>>

FILES:
<<<FILES>>>
```

## Schema da saída

```json
{"implemented": "yes|partial|no", "evidence": ["lib/…:12"], "justification": "string"}
```

## Regra de maioria
`implemented` = valor com ≥ 2 das 3 execuções; três valores diferentes = sem maioria → amostra humana. **Resultado do ciclo:** decisões com `yes` ÷ decisões selecionadas; `partial` é reportado à parte e não conta como implementada.

## Exemplo sintético
**Decisão:** "Chat and entries communicate only through the use case `SaveMessageAsEntry` in `lib/core/`; the chat feature never imports entries repositories."
**Código:** existe `lib/core/usecases/save_message_as_entry.dart`; `lib/features/chat/presentation/chat_bloc.dart:14` importa `package:app/features/entries/data/entries_repository_impl.dart`.
**Saída esperada:** `{"implemented": "partial", "evidence": ["lib/core/usecases/save_message_as_entry.dart:1", "lib/features/chat/presentation/chat_bloc.dart:14"], "justification": "The use case exists, but the chat BLoC also imports the entries repository directly."}`
