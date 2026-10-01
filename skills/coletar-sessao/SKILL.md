---
name: coletar-sessao
description: Encerra a coleta de dados da sessão atual para o instrumento do TCC (M1-M5b). Uso interno do protocolo de pesquisa — nunca invocar fora de uma sessão de ciclo (A ou B).
disable-model-invocation: true
---

Você recebeu o argumento `<ID>`, onde `<ID>` é um de: `SETUP`, `PLAN`, `F000`, `RF01`…`RF10`.

Rode exatamente este comando, pelo caminho absoluto (nunca relativo — esta skill roda de dentro do repositório do ciclo, não de `cerne-avaliacao`), substituindo `<ID>` pelo argumento recebido e `<CICLO>` por `a` ou `b` conforme o `CLAUDE_CONFIG_DIR` desta sessão (`cfg-ciclo-a` → `a`; `cfg-ciclo-b` → `b`):

```
python3 /caminho/absoluto/para/cerne-avaliacao/scripts/coletar_sessao.py skill <ID> --ciclo <CICLO> --versao-claude-code "$(claude --version)" --config-raciocinio "$CLAUDE_CODE_EFFORT_LEVEL" --otel-output ~/cerne/otelcol/output.jsonl
```

Exiba ao usuário **exatamente e apenas** a saída do script, sem adicionar nada, sem resumir, sem comentar tokens/tempo/custo (o script nunca imprime isso, mas se por algum motivo a saída contiver algo parecido, não repita nem elabore sobre isso — é uma falha a reportar, não a esconder).

Depois de exibir a saída, a sessão está encerrada para fins de medição. Não envie nenhuma mensagem adicional, não ofereça ajuda, não pergunte nada — esta é a última ação da sessão.
