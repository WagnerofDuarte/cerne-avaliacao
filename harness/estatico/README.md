# Harness estático (H-002)

Um módulo por métrica, cada um com CLI (`python3 -m harness.estatico.<modulo> --repo <repo> --tag <tag>`) e função `analisar(...)`. Todos leem a tag por `git archive` numa **cópia temporária** e nunca gravam no repositório do app.

| Módulo | Métrica |
|---|---|
| `m4_artefatos` | M4 |
| `m6_aderencia` | M6 parte D (tasks, plano × diff, referências inexistentes) |
| `m7_camadas` | M7 (RNF06) + regras estruturais do RF07 e do RF10 (saída à parte, contam na M11) |
| `m8_cobertura` | M8 (lcov temporário, injeção de importa-tudo) |
| `m8b_mutacao` | M8b (mutantes por operador, suíte do agente) |
| `m9_hardcodes` | M9 parte D (hardcodes) |
| `m10_either` | M10 parte D (assinaturas) |
| `m12_complexidade` + `../m12/` | M12 (CLI Dart sobre `package:analyzer`) |
| `m13_regressao` | M13 |
| `m14_decisoes` | M14 seleção (regras.md §1) + checks estáticos |
| `m15_consistencia` | M15 (C1–C4) |

Testes (contra o repositório de calibração montado em pasta temporária):

```bash
export PATH=/root/tools/flutter/bin:/root/tools/dart-sdk/bin:$PATH FLUTTER_ALLOW_ROOT=true   # ajuste ao ambiente
(cd harness/m12 && dart pub get)
python3 -m pytest harness/estatico/tests -q      # ~3 min (flutter test por tag + mutação)
(cd harness/m12 && dart test)
```
