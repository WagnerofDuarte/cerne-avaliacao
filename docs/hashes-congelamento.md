# Hashes de congelamento — `protocolo-v1.0`

**Gerado em:** 01/10/2026 (`GATE-C23`)
**Método:** SHA-256 (`sha256sum`). Para um diretório, cada arquivo é listado com o caminho relativo ao próprio diretório (ex.: dentro de `entrada/`, o arquivo aparece como `backend/README.md`, não `entrada/backend/README.md`), ordenado por caminho (`sort`, com separador nulo para nomes com espaço). O "hash combinado" de um diretório é o SHA-256 do texto dessa listagem inteira (`hash<espaço><espaço>caminho`, uma linha por arquivo, `\n` no fim) — não do conteúdo bruto concatenado. `.gitkeep` nunca entra na lista (arquivo vazio, sem conteúdo).

**A partir daqui:** qualquer mudança num arquivo ou diretório listado abaixo exige uma entrada em `docs/desvios.md` **antes** de ser aplicada (regra do `GATE-C23`).

**Achado registrado nesta geração:** o texto original do `GATE-C23` lista "os arquivos de `holdout/` e de `harness/juiz/`", mas não menciona `harness/regras.md` (`C-022`) nem `harness/precos.md` (`C-023`) — que também são definições congeladas da Fase 7. Incluídos aqui por extensão; ver `protocolo.md` §7 (divergências) para o registro formal.

## Documentos do instrumento

| Arquivo | SHA-256 |
|---|---|
| `docs/Metricas_e_Skills_Ciclos.md` | `e028c992a49b59873b339b6aea76e55ec6391b344e93062677c1b0acd4fc3152` |
| `docs/protocolo.md` | `3a167adc2ba81e196c07181528395cbcc6ec80e0778a12e56212bf11009af50a` |
| `harness/regras.md` (`C-022`) | `b4cbfcfc2a54704d4058b9aa98469d18643910ed720135bb12c1475095b2d20d` |
| `harness/precos.md` (`C-023`) | `51dfa7cc099e21e2ed149315b85c81432a7c96894c12e7bf2c127634b776e274` |

## Pacote de entrada (`entrada/`)

**Hash combinado:** `9e0c4b829a9149daae597d6ae4c232b3648ace94c60dac454c5ca56f0510c2d5`

Confere exatamente com os 15 hashes por arquivo já registrados no `GATE-C13` (`protocolo.md` §5.2) — nenhum arquivo mudou desde a revisão de neutralidade.

| Arquivo | SHA-256 |
|---|---|
| `backend/README.md` | `85763596609724f6ffa2342e77f8046fc9f017a006b4c97591fdbff4a3b2a196` |
| `backend/api/openapi.yaml` | `82376248daf57648a46265bacfc9c337eba181f8df940cc65f659d350a925a02` |
| `backend/error-taxonomy.md` | `0c996614fa19930d97e8c56cfdea163b5a78177c18a83a0a8957c7ad00f0f5b0` |
| `backend/export-screen-states.md` | `adff962fb13fb8e099fdeb485b227745513443361449e84e4c460ba40926ba66` |
| `backend/fixtures/README.md` | `b9302d2f886006853ec6daab840d87b2e3f483e29b55f4fcf9f37202d8193203` |
| `backend/fixtures/expected-transcription.md` | `b833ed4f72c0f01354a1c5fcb2dd184408a654073e3ffaa64b8661aa5c18dd8b` |
| `backend/fixtures/media/audio_fixture_01.wav` | `3ff3df21d186a8c2d300788bf53af2e2c70a1480a5941a640b94674a66584e1a` |
| `backend/fixtures/media/ocr_fixture_01.png` | `7ed3068dc0d2381259081a92feab4266867b5a0b89bb87925e0b5ed2025fc31d` |
| `backend/fixtures/media/ocr_fixture_ilegivel.png` | `0ed46c03c60f5428a4f645549a1c90b0256f3e81b609a6978c18f555d8efdbd8` |
| `backend/fixtures/seeded-search-entries.md` | `957971e9a65de24311294a32a8638eb2883bd0407326f11fa29a4517a730e5da` |
| `backend/known-bugs.md` | `042adc95e16e8e224390c20cbd3a3e1dd56b0199e740b848967254ad90232f52` |
| `backend/sync-badge.md` | `5a83f0cc23f383a28fdf8abad93024d7dc74bcbeb8ce7fa4589a29e08211bda8` |
| `prototype/cerne-prototype.html` | `aa8263b221d110a599f58877935152eba2fe5802a5b272c04d16ee84864cae0b` |
| `prototype/prototype-extract.md` | `306004c7789dc1b8f798ea3d5a7a4cce456b7900ac139fdde3b6edcbd1995207` |
| `requirements.md` | `6f7915d16617d60ebbd79195020f65e003a140efa51c4600cb3763ac4973c37b` |

## Prompts de intenção (`prompts/`)

**Hash combinado:** `71af323b4c5ced78966ddc02a6fa7e8949efc4022894af997cc5cfb95c7d8150` — atualizado em 01/10/2026 pelo desvio D-001 (`P-SETUP.md`); no congelamento era `a97753fda0604e8a77443ef6dd913e7ebad22aff9f0e66723be454910bcc5c36`

(Fica fora de `entrada/` por desenho — R27 — e tem hash à parte desde o `GATE-C13`.)

| Arquivo | SHA-256 |
|---|---|
| `P-F000.md` | `6752b0a35e6dcb693dd6fa18eac766d02b1302715cd67813783daaa830be122f` |
| `P-GLOBAL.md` | `469cbd183ba9f7697a96af9961f4ea3c368495442a42b38c2a60273763d746e4` |
| `P-RF01.md` | `292b3fa4a446bbd6b31bf21a921687bdb63d17bf7ef04c911147c3bf78a3081d` |
| `P-RF02.md` | `1b1bf0db79c1957202f1ae8aaf3cba52ba516efcca8f51fecd3ed085d80eb411` |
| `P-RF03.md` | `93c35978c6052dfc5fcb9decab13bf6269335718784ca360d0cf951623bc99d8` |
| `P-RF04.md` | `d467cfbbcc1e8458b29b699b0b7d2beeeb6217dbb6bc0446d84a4326ccbe3a54` |
| `P-RF05.md` | `5aad00284e28c1a5aeef03999ac6fc858a4bad4b8030a2d931d54b57595afde2` |
| `P-RF06.md` | `b0d2f486ac0e601967bf010f3a1d825d9b7bce1475c16c6ccb93bd4053864d59` |
| `P-RF07.md` | `c34326a20e90446b6bae90b306bcac7cb69bf16f5ac632823aea650b2bc7f4c0` |
| `P-RF08.md` | `18df84300a0f937239e1c3a9cd36a4b7d35b8cee092bd9af045c1b3c7f1261c6` |
| `P-RF09.md` | `a09915b1da678b8f7baef994e6991d8e858ee34095afb6966df7d75e2429cf61` |
| `P-RF10.md` | `75acf9b3dd43dbfc261610873a7b0d0d39df605decc4e6e9e70a5a45bfb6a3d0` |
| `P-SETUP.md` | `6c040ea1852cfaccb77c59cd9091435a98695b081de8d4e0f5f2109faecbca65` (D-001; antes `46fa242eb0e5ae205ff05683b2d26777cf5d01406bb12a2868c060d1a14d3971`) |
| `P-TECH.md` | `fc758e40bce6ea498e8ceb79e84591806f605338c681df9c6be4a7256f7f4cba` |

## Suíte hold-out (`holdout/`)

**Hash combinado:** `079032dd05abc90323c64942c67eac3614a124c7cb134a62fbc6bc19c17a81ca`

| Arquivo | SHA-256 |
|---|---|
| `cenarios.md` | `107bc48bed31fb3def0e75e8cd65c49bcdb9d0977151a696b6a8586a16ea926a` |
| `estados-m9.md` | `eba4539e6b5a13e06adc7d36c5ed1ac3fff0cb76c749743547d7485fcdd038b5` |
| `fixtures/textos-instrumento.json` | `545037f708537c481141d37642aacf6d43c0811b06298a6a6950c7c3486d1736` |
| `fixtures/textos.json` | `f65c6f86886fe713dac378345dcebc355451018b33ad41f604df18439eb32fa0` |
| `referencia/Cerne - Prototipo Final.html` | `61032a92f082044f979cc52f65ae2d6cb461f0420f2bd9bc676f6115185d2fff` |
| `rnf09.md` | `d7c14d84e6fdbf6e0e6ce1b060a7680833db51178feb40af383869d07dd84aa9` |

(O HTML de referência é bit a bit idêntico ao do pacote de entrada — mesmo hash `61032a92...` desde o `C-006`.)

## Rubricas do avaliador (`harness/juiz/`)

**Hash combinado:** `afb84d62b0323765ea8c9a44fa9e1615ee41c52834c2546bf059002c58b856ab`

| Arquivo | SHA-256 |
|---|---|
| `README.md` | `c8a8d61be0170107bc0303b44cef7be1b7c22dc7b61b6e8eeec388c68a490e9c` |
| `d16-severidade.md` | `8e8524926389d364e869235b2dedbdd15bc60170638b138b0bdf63990689f5aa` |
| `m14-handoff.md` | `da09e78dda5a717dd88c66d6071f996b7c1b30148bab564f546e7f03b4f337fa` |
| `m6-aderencia.md` | `744ac19ab73f4b3708a2270d3e6b29632782d304d5c10adc3189c1403bc97a0b` |
| `m9-espacamento.md` | `5d1c17828feaeba8dbcd726bb0dd1a7f4e2d6b94994e4fd5f97d8ec9e2fac66a` |

## Skill de coleta e script (`skills/coletar-sessao/`, `scripts/`)

**Skill — hash combinado:** `34c2059566966940604d763079d940947e244f522d2c92c51bbdd5873e34b345`

| Arquivo | SHA-256 |
|---|---|
| `skills/coletar-sessao/SKILL.md` | `87c63d60ef9c48ec958f241e496d109ef872031a45f0ad8cf0c3f510e7407fc5` |

**Scripts (skill + auxiliares) — hash combinado:** `86e48501abc18c300709aa783197c8b70b6aa369017d2b6ba469e15adc83d31e` — atualizado em 11/10/2026 pelo desvio D-015 (respostas do painel `AskUserQuestion`); antes era `3da293809bd9a8c872f64cc7a1338c68a9db9c803a3a4929db252a1697028222` — atualizado em 11/10/2026 pelo desvio D-014 (`coletar_sessao.py` e seu teste: detecção de fase por `<command-name>`); antes era `caaf01702bc56ab4fb6ae81494157cf1a995d58f76f68090483fa090fbc00e7d` (atualizado em 01/10/2026 pelo desvio D-004 (arquivo novo `faixa-plan`; nenhum script existente alterado); no congelamento era `137b234a1be868be5cf32ecb462b4694cf021822e3cb8ecc5e0d42593b1448df`)

| Arquivo | SHA-256 |
|---|---|
| `_ciclo_common.sh` | `96151ff1a7f58d23193838ef4320b250c2c86bac5dd118f5ba7f0ec48b4af469` |
| `_concluir_unidade.sh` | `036f8b138ec8f17a2e2019ae2da21a2688405620233c6b58745316bd689da697` |
| `coletar_sessao.py` | `7ac497d939f795219424705337d287bfaa7b2adece43f7e6253a81e9bb75efd0` (D-015; antes `63ccce8eb422506066813919dd8b80bc9825083aeac875ed0e94ade377959e3a` pelo D-014; no congelamento `5e2e8e09c30829aa2671cb68a754e0ed8e7925c8886fe4b8fa154a84a7f0b195`) |
| `concluir-rf` | `3c63882c4f57ad360ebe84cebd3d759f2634f585e33931ed6deeaca1966ec845` |
| `db-truncate-and-seed.ts` | `a9fea32f2cbc9f02bf4688410bac2419bfd006d9181df01124b36a53fb8159e6` |
| `faixa-plan` | `2424ebb6538c8ae22651bb6d6aefe52d72b20b888726d4a39b87953a53e84637` (novo, D-004) |
| `iniciar-ciclo` | `4420572495a993e0ed8485aad392058d7a374fc05ec57c9e15426d330ed9d1fa` |
| `instalar-metodologia` | `f38011365a7bafa4043b4618c23dbe34d1bcb30770ce27438223d3c1bfd578cf` |
| `registrar_instalacao.py` | `dc13e54c168f25de982bba2814ed68ef6faff40a00f0272146a0c050addf5ee6` |
| `registrar_tag.py` | `be769ab879665a4cd7f03c02691f8b09d06623fe7065b5e829c7b3e30be62948` |
| `replay-mode` | `c843a96417cf318fcdc428b31554b28d79139dd383cdae1279ec11884b22742e` |
| `reset-ambiente` | `64c9d39e25150ab9f15d68d2f781c5c96ee2e78c1c5c832ee46b91da538f14f4` |
| `rf-incompleto` | `25d6d5e8aae8b9f919a62bf4c41e9a04b659d9ee6c5d7e0a9440d9234fcbf2a1` |
| `tests/test_coletar_sessao.py` | `085c352fc38ecc2d7d942b4891d9e1bce2709a918436cf6fc8c5f2f911c4e2d3` (D-015; antes `cc9fca1235728d0431b85db28929c543acca90c20ead1a4bc8592c6598587af8` pelo D-014; no congelamento `8f271bddcf9cf6ffe05f00dec9c91448ecb5ef2be47d6f9ce94dfca18acd5c77`) |

## `settings.json` (Claude Code, `cfg-ciclo-a`/`cfg-ciclo-b`)

**Não versionado neste repositório** — vive em `~/cerne/cfg-ciclo-a/settings.json` e `~/cerne/cfg-ciclo-b/settings.json`, na máquina do Wagner (fora de `cerne-ciclo-a`/`b` também, por desenho do `C-011`/P2). Hash já conferido idêntico nos dois arquivos em 25/09/2026 (`C-012`, `protocolo.md` §6.5):

```
fdb4628757e596db7ea6bc57ec523309bf1c1591ac175f83caa2e07ea8285369
```

**Atualizado em 07/10/2026 (desvio D-009):** o Claude Code acrescentou `"theme": "dark"` aos dois arquivos no primeiro uso (30/09) e reordenou as chaves; conteúdo funcional idêntico, iguais entre si. Hash vigente:

```
db5d321b34ad3a400fcc57bfd219191a3f364cdee9b85ef1a1115e1be62391e2
```

**Atualizado em 08/10/2026 (desvio D-012):** acrescentadas aos dois arquivos as chaves `"syncClaudeAiSkills": false` e `"syncClaudeAiPlugins": false` (única diferença, conferida por `diff` nos dois). Hash vigente, idêntico nos dois:

```
3904700bc5637f05675b73788a72c1bf4a934b1b763ab4ac0aa227bf10405922
```

**Atualizado em 11/10/2026 (desvio D-013):** acrescentada aos dois arquivos a chave `"disableClaudeAiConnectors": true` (única diferença, conferida por `diff` nos dois). Hash vigente, idêntico nos dois:

```
0112786e12fbe0917221c8d09f17f9f4b9c022d5ef811b9123b9fb9b0a62f393
```

Se esse hash mudar numa reconferência futura (ex.: X-002 antes do Ciclo B), é desvio — registrar em `desvios.md`.
