# Rubrica M9 (espaçamento) — fidelidade de espaçamento ao protótipo

**Item:** um dos 31 estados de `holdout/estados-m9.md`, num ciclo.
**Entrada enviada:** duas imagens do mesmo estado, no mesmo tamanho lógico (390 × 844 pt, exportadas na mesma escala): **REFERENCE** (frame do protótipo congelado) e **CANDIDATE** (screenshot do app na tag `final`). Sem nome de ciclo; a ordem das imagens é sempre REFERENCE e depois CANDIDATE.
**Escopo:** só espaçamento — margens, paddings, distância entre elementos e alinhamento. Cor e tipografia são medidas por outro mecanismo (D); conteúdo (textos do usuário, datas, quantidades) não é critério.

## Tolerância (instrumento)
Diferença de até **±4 dp** num espaçamento equivalente não é desvio. Na escala @3x, 4 dp = 12 px. O avaliador recebe a escala.

## Prompt (v1.0)

```text
You compare the SPACING of two screenshots of the same app screen state.
Image 1 is the REFERENCE design. Image 2 is the CANDIDATE implementation.
Both are 390 x 844 points, exported at scale <<<SCALE>>>x (1 point = <<<SCALE>>> pixels).

Judge ONLY spacing: outer margins, inner paddings, gaps between elements, and alignment.
Ignore colors, fonts, and content (user text, dates, counts, which items are listed).
A difference of up to 4 points in an equivalent spacing is acceptable.

For each major region present in the REFERENCE (header, main content, list items or cards,
bottom bar or composer, sheets or dialogs), compare it with the CANDIDATE.
Report each spacing deviation larger than 4 points. If a region is missing in the CANDIDATE,
report it as a deviation of that region.

spacing_ok is true only if there is no deviation. Answer only with JSON matching the schema.
```

## Schema da saída

```json
{
  "spacing_ok": true,
  "deviations": [
    {"region": "string", "reference_pt": 16, "candidate_pt": 28, "note": "string"}
  ]
}
```

## Regra de maioria
`spacing_ok` = valor que aparece em ≥ 2 das 3 execuções (sempre há maioria num booleano). A lista de desvios é registrada, mas não pontua. **Resultado:** `espacamento_ok` em `estados_m9.csv`.

## Exemplo sintético
**REFERENCE:** cartões de lista com margem lateral de 16 pt e 8 pt entre cartões. **CANDIDATE:** mesma lista com margem lateral de 16 pt e 20 pt entre cartões; cabeçalho idêntico.
**Saída esperada:** `{"spacing_ok": false, "deviations": [{"region": "list items or cards", "reference_pt": 8, "candidate_pt": 20, "note": "gap between cards"}]}`
