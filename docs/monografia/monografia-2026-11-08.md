<!-- Instantaneo da 'Monografia Inicial - TCC2' (Google Docs 1rw6oi6yfNMk5ppwVjzQOET3mZ13zk6XaVq1lUjbp0Rg) em 08/11/2026, exportado como texto/markdown. A fonte de verdade e o Google Docs. -->

**UNIVERSIDADE FEDERAL DE MINAS GERAIS**

**ESCOLA DE ENGENHARIA**

**CURSO DE ENGENHARIA DE SISTEMAS**

**WAGNER DE OLIVEIRA FERREIRA DUARTE**

**Desenvolvimento orientado por especificação com agentes de IA: estudo de caso comparativo entre GitHub Spec Kit e BMAD-METHOD**

Belo Horizonte

2026

**WAGNER DE OLIVEIRA FERREIRA DUARTE**

**Desenvolvimento orientado por especificação com agentes de IA: estudo de caso comparativo entre GitHub Spec Kit e BMAD-METHOD**

Monografia apresentada ao Curso de Engenharia de Sistemas da Universidade Federal de Minas Gerais como requisito parcial para a obtenção do título de Bacharel em Engenharia de Sistemas.

Orientadora: Profa. Luiza Bernardes Real

Belo Horizonte

2026

# **RESUMO**

Agentes de codificação baseados em modelos de linguagem ampliaram a autonomia do desenvolvimento de software, mas faltam evidências empíricas para escolher entre as metodologias de desenvolvimento orientado por especificação que organizam o trabalho desses agentes. Este trabalho compara duas delas: o GitHub Spec Kit, que conduz um agente único por comandos incrementais, e o BMAD-METHOD, que planeja o produto de forma antecipada e divide o trabalho entre agentes especializados. Em um estudo de caso comparativo, o mesmo desenvolvedor aplicou cada metodologia, em sequência, com o mesmo agente (Claude Code com o modelo Claude Sonnet 5), à construção do mesmo aplicativo móvel de diário pessoal, o Cerne, decomposto em onze unidades de trabalho. O protocolo, o instrumento de medição e o registro de desvios foram definidos antes da execução, e as métricas de processo foram coletadas dos transcritos brutos das sessões. Foram analisadas 274 sessões. O Spec Kit consumiu 25,9 horas de tempo ativo, 4,9 milhões de tokens de saída e o equivalente a US$ 271 em custo; o BMAD-METHOD, 82,7 horas, 9,1 milhões de tokens de saída e o equivalente a US$ 902, isto é, 3,2, 1,9 e 3,3 vezes mais, respectivamente. Na análise pareada por requisito, o BMAD-METHOD exigiu mais tempo em todos os nove pares (teste de Wilcoxon, p exato = 0,004), mas provocou menos intervenções corretivas do pesquisador (16 contra 49), ao custo de mais respostas a pausas previstas pelo próprio processo (279 contra 67). As métricas de produto e a validação do avaliador baseado em modelo de linguagem não foram realizadas nesta versão, por prazo, de modo que o trabalho responde com dados à questão sobre o custo do processo e deixa em aberto a qualidade do produto e a transmissão de decisões entre fases. As contribuições são o protocolo, o instrumento de medição e o registro de 98 desvios, que permitem replicar e completar a avaliação.

**Palavras-chave: desenvolvimento orientado por especificação; agentes de codificação; GitHub Spec Kit; BMAD-METHOD; engenharia de software empírica.**

# **ABSTRACT**

Coding agents based on large language models have increased the autonomy of software development, but there is little empirical evidence for choosing among spec-driven development methodologies that organize the work of these agents. This work compares two of them: GitHub Spec Kit, which drives a single agent through incremental commands, and BMAD-METHOD, which plans the product up front and splits the work among specialized agents. In a comparative case study, the same developer applied each methodology in sequence, with the same agent (Claude Code with the Claude Sonnet 5 model), to build the same mobile journaling app, Cerne, decomposed into eleven work units. The protocol, the measurement instrument and the deviation log were defined before execution, and process metrics were collected from the raw session transcripts. A total of 274 sessions were analyzed. Spec Kit consumed 25.9 hours of active time, 4.9 million output tokens and the equivalent of US$ 271 in cost; BMAD-METHOD consumed 82.7 hours, 9.1 million output tokens and the equivalent of US$ 902, that is, 3.2, 1.9 and 3.3 times more, respectively. In the paired analysis by requirement, BMAD-METHOD required more time in all nine pairs (Wilcoxon signed-rank test, exact p = 0.004), but triggered fewer corrective interventions by the researcher (16 versus 49), at the price of more answers to pauses foreseen by the process itself (279 versus 67). Product metrics and the validation of the language-model evaluator were not carried out in this version because of the deadline, so the study answers the process-cost question with data and leaves product quality and the transmission of decisions across phases open. The contributions are the protocol, the measurement instrument and the log of 98 deviations, which allow the evaluation to be replicated and completed.

**Keywords: spec-driven development; coding agents; GitHub Spec Kit; BMAD-METHOD; empirical software engineering.**

# **LISTA DE QUADROS**

Quadro 1 – Variáveis controladas e graus de liberdade dos ciclos

Quadro 2 – Requisitos funcionais do núcleo comparativo

Quadro 3 – Modos do cache de respostas de IA

Quadro 4 – Atribuição de fases aos comandos e fluxos das metodologias

Quadro 5 – Métricas de processo

Quadro 6 – Métricas de produto

Quadro 7 – Métricas diferenciais

Quadro 8 – Métricas por dimensão da taxonomia de Macedo (2026)

Quadro 9 – Decisões de arquitetura do backend

Quadro 10 – Decisões de protocolo

Quadro 11 – Hashes SHA-256 dos itens congelados

Quadro 12 – Alterações em itens congelados

Quadro 13 – Composição do pacote de entrada

Quadro 14 – Entrega dos prompts de intenção

Quadro 15 – Rubricas do avaliador

Quadro 16 – Escala de severidade dos defeitos

Quadro 17 – Cenários dos critérios de aceite

Quadro 18 – Cenários de falha de rede

Quadro 19 – Métricas e análises não avaliadas nesta versão do estudo

Quadro 20 – Desvios do protocolo, agrupados por natureza

Quadro 21 – Conferências do contexto do agente com o comando /context

# **LISTA DE TABELAS**

Tabela 1 – Fechamento das unidades nos dois ciclos (datas de 2026, horário de Brasília)

Tabela 2 – Métricas de processo por ciclo

Tabela 3 – Tempo ativo, custo, intervenções (M5) e respostas de processo (M5b) por unidade

Tabela 4 – Artefatos de especificação e planejamento (M4) por tipo

Tabela 5 – Tempo de implementação e validação, custo e intervenções por par de requisitos

Tabela 6 – Testes de Wilcoxon por par de requisitos (diferença B menos A)

# **LISTA DE ABREVIATURAS E SIGLAS**

  

|  |  |
| :-: | :-: |
| API | Application Programming Interface |
| BLoC | Business Logic Component |
| BMAD | Breakthrough Method of Agile AI-Driven Development |
| ESPEC | Fase de especificação |
| HTTP | Hypertext Transfer Protocol |
| IA | Inteligência artificial |
| IMPL | Fase de implementação |
| JSON | JavaScript Object Notation |
| LGPD | Lei Geral de Proteção de Dados Pessoais |
| PDF | Portable Document Format |
| PIN | Personal Identification Number |
| PRD | Product Requirements Document (documento de requisitos de produto) |
| QP | Questão de pesquisa |
| RAG | Retrieval-Augmented Generation (geração aumentada por recuperação) |
| RF | Requisito funcional |
| RNF | Requisito não funcional |
| SHA | Secure Hash Algorithm |
| SQL | Structured Query Language |
| UML | Unified Modeling Language |
| VALID | Fase de validação |

  

# **SUMÁRIO**

**1 INTRODUÇÃO**

1.1 Contextualização e motivação

1.2 Problema e questões de pesquisa

1.3 Objetivos

1.3.1 Objetivo geral

1.3.2 Objetivos específicos

1.4 Justificativa e contribuições

1.5 Escopo e delimitações

1.6 Evolução do escopo desde a proposta

1.7 Organização do texto

**2 FUNDAMENTAÇÃO TEÓRICA E TRABALHOS RELACIONADOS**

2.1 Desenvolvimento de software assistido por agentes de IA

2.2 Desenvolvimento orientado por especificação

2.3 GitHub Spec Kit

2.4 BMAD-METHOD

2.5 Taxonomia de processo e comparação documental

2.6 Avaliação empírica de processos com modelos de linguagem

2.7 Fundamentos do veículo experimental

2.8 Síntese e lacuna de pesquisa

**3 MÉTODO DE PESQUISA**

3.1 Caracterização do estudo

3.2 Questões de pesquisa e proposições

3.3 Desenho dos ciclos

3.3.1 Variáveis controladas

3.3.2 Tratamento A: GitHub Spec Kit

3.3.3 Tratamento B: BMAD-METHOD

3.3.4 Unidades de trabalho, ordem e limite de tempo

3.3.5 Regras de interação do pesquisador

3.4 Veículo experimental: o aplicativo Cerne

3.4.1 Visão do produto e requisitos

3.4.2 Protótipo de referência

3.4.3 Backend compartilhado

3.5 Controle do não determinismo da IA do produto

3.6 Instrumento de medição

3.6.1 Princípios e arquitetura

3.6.2 Coleta por sessão

3.6.3 Suíte de avaliação de caixa-preta

3.6.4 Avaliador baseado em modelo de linguagem

3.6.5 Congelamento do protocolo e registro de desvios

3.7 Métricas

3.8 Plano de análise

3.9 Ameaças à validade

**4 RESULTADOS**

4.1 Execução dos ciclos

4.2 Ciclo A: GitHub Spec Kit

4.3 Ciclo B: BMAD-METHOD

4.4 Métricas de processo

4.5 Métricas de produto

4.6 Métricas diferenciais

4.7 Validação do avaliador

4.8 Análise pareada por requisito

**5 DISCUSSÃO**

5.1 Comportamento observado e notas documentais

5.2 Produtividade e confiabilidade

5.3 Perda de contexto e fidelidade de *handoff*

5.4 Lições sobre o próprio instrumento

**6 AVALIAÇÃO DE IMPACTOS**

6.1 Impacto social

6.2 Impacto econômico

6.3 Impacto ambiental

**7 CONCLUSÃO**

7.1 Respostas às questões de pesquisa

7.2 Contribuições

7.3 Limitações

7.4 Trabalhos futuros

**REFERÊNCIAS**

**APÊNDICES**

# **1 INTRODUÇÃO**

## **1.1 Contextualização e motivação**

Agentes de codificação baseados em modelos de linguagem de grande porte deixaram de ser ferramentas de completar código e passaram a executar tarefas inteiras de engenharia de software: ler um repositório, planejar uma mudança, editar arquivos, executar testes e corrigir os próprios erros, com pouca intervenção humana entre um passo e outro. Hassan et al. (2025) chamam essa etapa de engenharia de software agêntica e observam que os agentes passam a receber objetivos complexos, e não apenas pedidos de geração de código. Dados do fornecedor do agente usado neste trabalho indicam a mesma tendência: entre outubro de 2025 e janeiro de 2026, a duração dos turnos mais longos do Claude Code quase dobrou, e, no uso interno da empresa, entre agosto e dezembro de 2025, o número médio de intervenções humanas por sessão caiu de 5,4 para 3,3 (Anthropic, 2026).

Maior autonomia, porém, não se traduz automaticamente em maior produtividade nem em software mais confiável. Em um experimento controlado com 16 desenvolvedores experientes de projetos de código aberto, o uso de ferramentas de IA aumentou em 19% o tempo de conclusão das tarefas, embora os participantes esperassem uma redução de 24% (Becker et al., 2025). Farrag (2026) descreve essa tensão como um paradoxo entre produtividade e confiabilidade: os ganhos de produção individual trazidos pelos assistentes de IA convivem com a piora de indicadores do sistema, como a estabilidade das entregas, a taxa de falha das mudanças, o retrabalho de código e a densidade de defeitos em produção. Entre os mecanismos que o autor aponta estão a perda de contexto entre etapas e os testes gerados pela IA que apenas espelham o código também gerado por ela.

Uma das respostas a esse problema é o desenvolvimento orientado por especificação (spec-driven development), no qual a especificação escrita antes do código passa a ser o artefato central que orienta o agente e contra o qual o resultado é verificado (Böckeler, 2025; Piskala, 2026). Em vez de conduzir o agente por uma sequência de instruções em conversa, o desenvolvedor produz, com a ajuda do próprio agente, documentos de requisitos, planos técnicos e listas de tarefas, e a implementação é gerada a partir deles. Em poucos meses surgiram diversas ferramentas que organizam esse processo, entre as quais o GitHub Spec Kit (GitHub, 2026) e o BMAD-METHOD (BMAD Code Organization, 2026).

As duas ferramentas partem da mesma premissa, mas organizam o processo de modo distinto. O Spec Kit conduz um único agente por uma sequência de comandos que especifica, planeja e implementa uma funcionalidade por vez. O BMAD-METHOD distribui o trabalho entre agentes especializados, que reproduzem os papéis de uma equipe ágil, como analista, gerente de produto, designer de experiência, arquiteto e desenvolvedor, e planeja o produto inteiro antes de iniciar a implementação (BMAD Code Organization, 2026; Hassan et al., 2025). Hoje, a escolha entre elas se apoia na documentação das ferramentas, em relatos de praticantes e em comparações documentais, como a de Macedo (2026), que avalia seis ferramentas a partir de uma taxonomia de processo. Até onde foi possível verificar, não há comparação empírica que aplique as duas metodologias à construção de um mesmo produto, em condições controladas, e meça tanto o custo do processo quanto a qualidade do resultado.

Este trabalho realiza essa comparação. O GitHub Spec Kit e o BMAD-METHOD são aplicados, em sequência, à construção de um mesmo aplicativo móvel, o Cerne, um diário reflexivo com inteligência artificial desenvolvido em Flutter, com o mesmo agente de codificação, o mesmo modelo, o mesmo desenvolvedor e o mesmo backend. O aplicativo é o veículo experimental, e não o objeto de estudo: seus requisitos foram escolhidos por gerarem dados comparáveis entre os dois processos.

## **1.2 Problema e questões de pesquisa**

O problema que motiva o estudo é a falta de evidência empírica para escolher entre metodologias de desenvolvimento orientado por especificação que diferem na forma de organizar o trabalho do agente. A documentação das ferramentas e as análises comparativas existentes descrevem o que cada metodologia promete, como a especificação antecipada, a decomposição em papéis e as etapas de validação, mas não mostram se essas promessas se realizam quando a metodologia é aplicada a um produto real, nem a que custo. Em particular, não se sabe se o planejamento antecipado e a divisão em agentes especializados do BMAD-METHOD transmitem melhor as decisões de projeto até o código do que o planejamento incremental, com um único agente, do Spec Kit, nem quanto tempo, quantos tokens e quanta intervenção humana cada abordagem consome.

A questão principal do estudo é:

QP: Como o GitHub Spec Kit e o BMAD-METHOD se diferenciam, quanto ao processo de desenvolvimento e ao produto resultante, quando aplicados pelo mesmo desenvolvedor, com o mesmo agente de codificação, à construção do mesmo aplicativo?

Ela se desdobra em quatro questões específicas:

  - QP1 (custo do processo): quanto tempo, quantos tokens e quantas intervenções humanas cada metodologia exige, no total e em cada fase do desenvolvimento?
  - QP2 (transmissão de decisões): em que medida as decisões registradas nos artefatos de planejamento de cada metodologia chegam ao código entregue?
  - QP3 (qualidade do produto): como os produtos de cada ciclo se comparam quanto à arquitetura, aos testes, à fidelidade visual, ao tratamento de erros e ao atendimento dos critérios de aceite?
  - QP4 (estabilidade ao longo do ciclo): as convenções e a integridade arquitetural se mantêm à medida que o código cresce, ou se degradam entre os primeiros e os últimos requisitos?

A seção 3.2 relaciona essas questões às dimensões da taxonomia de Macedo (2026), e a seção 3.7 apresenta as métricas que respondem a cada uma delas.

## **1.3 Objetivos**

### *1.3.1 Objetivo geral*

Comparar empiricamente o GitHub Spec Kit e o BMAD-METHOD quanto ao custo do processo de desenvolvimento, à qualidade do produto resultante e à transmissão das decisões de planejamento até o código, por meio de um estudo de caso instrumentado em que as duas metodologias são aplicadas, com o mesmo agente de codificação, à construção do mesmo aplicativo móvel.

### *1.3.2 Objetivos específicos*

Para alcançar o objetivo geral, o trabalho se propõe a:

  - definir e congelar, antes do primeiro ciclo, um protocolo experimental que fixe tudo o que não é a própria metodologia, incluindo agente, modelo, ambiente, pilha técnica, informação de produto e regras de interação do pesquisador com o agente;
  - construir um backend compartilhado e determinístico, com cache de respostas de IA, que elimine o backend e o provedor de IA como fontes de variação entre os ciclos;
  - desenvolver um instrumento de medição invisível ao agente, que colete tempo, tokens e intervenções a cada sessão e avalie o produto por scripts, por uma suíte de avaliação de caixa-preta e por um avaliador baseado em modelo de linguagem, validado por amostragem;
  - executar dois ciclos completos de desenvolvimento, um com cada metodologia, e registrar todos os desvios de protocolo;
  - comparar os ciclos em métricas de processo, de produto e de transmissão de decisões, organizadas pelas dimensões da taxonomia de Macedo (2026);
  - discutir os resultados à luz do paradoxo entre produtividade e confiabilidade (Farrag, 2026) e registrar as lições sobre o próprio instrumento, de modo que o protocolo possa ser replicado.

## **1.4 Justificativa e contribuições**

A justificativa do trabalho tem três componentes. O primeiro é prático. Equipes e desenvolvedores que adotam agentes de codificação precisam decidir como organizar o trabalho do agente, e as metodologias de desenvolvimento orientado por especificação diferem em custo de adoção, número de etapas e quantidade de interação exigida. Uma comparação feita sobre o mesmo produto, com as demais condições fixadas, oferece um ponto de referência que a documentação das ferramentas não oferece.

O segundo componente é científico. Macedo (2026) compara as duas metodologias apenas no plano documental e propõe, como agenda de pesquisa, avaliações orientadas a processo, métricas de contexto e estudos com equipes reais. Farrag (2026) relata um estudo piloto com o Spec Kit em equipes reais, mas sem controle experimental e com parte dos dados obtida por autorrelato. Este trabalho operacionaliza parte dessa agenda, com medidas extraídas de registros, e não de percepção, e oferece uma primeira evidência empírica para uma comparação que, até aqui, foi apenas documental.

O terceiro componente é metodológico. Avaliar metodologias que dependem de modelos de linguagem exige controlar fontes de variação que não existem em estudos tradicionais de engenharia de software: o não determinismo das respostas, a mudança silenciosa dos modelos comerciais, o contexto carregado automaticamente pelo agente e a própria interação do pesquisador com o agente. O protocolo, o backend determinístico e o instrumento de medição construídos aqui, bem como o registro dos problemas encontrados na sua aplicação, podem ser reaproveitados em estudos semelhantes. As contribuições decorrentes desses três componentes são retomadas na seção 7.2.

## **1.5 Escopo e delimitações**

O estudo compara duas metodologias, em versões específicas (GitHub Spec Kit 1.0.10 e BMAD-METHOD 6.11.0), aplicadas por um único agente de codificação (Claude Code, com o modelo Claude Sonnet 5) à construção de um aplicativo para iOS em Flutter. Os dois ciclos são conduzidos pelo mesmo desenvolvedor, que é também o pesquisador, em ordem fixa e sem repetição. Por isso, o trabalho é um estudo de caso instrumentado, e não um experimento controlado, e seus resultados não autorizam generalização estatística (seção 3.1).

A comparação se restringe ao desenvolvimento do aplicativo móvel. O backend foi construído antes dos ciclos, com outra abordagem, e permanece idêntico e congelado nos dois; a interface foi definida em um protótipo também congelado. O núcleo comparado compreende os dez requisitos funcionais descritos na seção 3.4.1 e quatro requisitos não funcionais medidos de forma automatizada. Três funcionalidades presentes no protótipo, os planos de ação, o seletor de persona e os marcadores manuais, ficam fora dos dois ciclos.

O Cerne é tratado como veículo experimental neutro. Embora pertença à categoria dos diários reflexivos, o estudo não avalia efeitos do aplicativo sobre o bem-estar dos usuários, não inclui protocolo de detecção de risco psicológico e não envolve participantes humanos além do próprio pesquisador. Também ficam fora do escopo a avaliação de usabilidade com usuários, o desempenho em produção, outras plataformas além do iOS, outros agentes de codificação e outras metodologias.

## **1.6 Evolução do escopo desde a proposta**

A proposta apresentada na primeira etapa do Trabalho de Conclusão de Curso previa comparar a abordagem RIPER com o GitHub Spec Kit e apresentava o Cerne como um ecossistema de apoio à saúde mental, fundamentado na literatura sobre os efeitos da escrita expressiva. O escopo técnico excluía o processamento de imagens, e o cronograma previa um ciclo de desenvolvimento com cada abordagem entre agosto e setembro de 2026.

Ao longo do planejamento, quatro mudanças redefiniram esse escopo. A primeira foi o par comparado: o BMAD-METHOD passou a ocupar o lugar da RIPER, e o estudo tornou-se a comparação entre duas metodologias de desenvolvimento orientado por especificação com organizações de processo distintas. A RIPER foi reaproveitada na construção do backend compartilhado, fora da comparação. A segunda foi o enquadramento do produto: o Cerne deixou de ser tratado como intervenção de saúde mental e passou a ser um veículo experimental neutro, cujos requisitos foram reorganizados pela capacidade de gerar dados comparáveis. Com isso, a eficácia do diário saiu do escopo, e a fundamentação psicológica passou a servir apenas como contexto do produto (seção 2.7).

A terceira mudança foi o escopo técnico, que passou a incluir o reconhecimento de texto em fotografias de páginas manuscritas (RF02), executado pelo backend por um modelo de linguagem com visão; não há análise de imagens de pessoas. A quarta foi o cronograma: agosto e setembro foram dedicados à construção do backend, do protótipo e do instrumento de medição, e os dois ciclos comparativos começaram depois do congelamento do protocolo, em outubro de 2026.

Todas essas mudanças foram decididas antes do primeiro ciclo e não afetam a comparação. Elas são registradas aqui porque explicam as diferenças entre este texto e os documentos da primeira etapa do trabalho.

## **1.7 Organização do texto**

Além desta introdução, o trabalho está organizado em seis capítulos. O capítulo 2 apresenta a fundamentação teórica: o desenvolvimento assistido por agentes, o desenvolvimento orientado por especificação, as duas metodologias comparadas, a taxonomia de processo usada na análise, os cuidados da avaliação empírica com modelos de linguagem e os fundamentos do aplicativo usado como veículo. O capítulo 3 descreve o método: o enquadramento como estudo de caso, as questões de pesquisa, o desenho dos ciclos, o veículo experimental, o controle do não determinismo, o instrumento de medição, as métricas, o plano de análise e as ameaças à validade. O capítulo 4 apresenta os resultados dos dois ciclos, e o capítulo 5 os discute, incluindo as lições sobre o próprio instrumento. O capítulo 6 avalia os impactos sociais, econômicos e ambientais do trabalho, e o capítulo 7 reúne as conclusões, as contribuições, as limitações e os trabalhos futuros. Os apêndices trazem as decisões de arquitetura do backend, o protocolo e os hashes de congelamento, o pacote de entrada e os prompts, as rubricas do avaliador, os cenários da suíte de avaliação, o registro de desvios e a verificação do contexto do agente.

# **2 FUNDAMENTAÇÃO TEÓRICA E TRABALHOS RELACIONADOS**

## **2.1 Desenvolvimento de software assistido por agentes de IA**

O uso de modelos de linguagem na programação passou, em poucos anos, por duas etapas. Na primeira, os assistentes completavam trechos de código dentro do editor, a partir do contexto imediato do arquivo. O experimento controlado de Peng et al. (2023) é uma das referências mais citadas dessa etapa: desenvolvedores com acesso ao GitHub Copilot concluíram a implementação de um servidor HTTP em JavaScript 55,8% mais rápido do que o grupo de controle. Na segunda etapa, os assistentes passaram a operar como agentes: recebem um objetivo, consultam o repositório, decidem quais arquivos alterar, executam comandos e testes e iteram sobre os próprios resultados.

Hassan et al. (2025) chamam essa etapa de engenharia de software agêntica e propõem uma dualidade para organizá-la. De um lado, a engenharia de software para humanos redefine o papel do desenvolvedor, que passa a se concentrar na intenção, na estratégia e na orientação do agente. De outro, a engenharia de software para agentes busca oferecer um ambiente estruturado e previsível, no qual vários agentes possam operar. As metodologias comparadas neste trabalho pertencem a esse segundo lado: são estruturas de processo que dizem ao agente o que produzir, em que ordem e com quais verificações.

A evidência sobre o efeito desses agentes ainda é mista. Watanabe et al. (2025) analisaram 567 pull requests gerados com o Claude Code em 157 projetos de código aberto e observaram que 83,8% deles foram aceitos, contra 91,0% dos pull requests humanos dos mesmos projetos, e que cerca de 55% dos aceitos foram integrados sem alterações adicionais. Becker et al. (2025), em experimento com desenvolvedores experientes trabalhando em projetos maduros, encontraram o efeito oposto ao esperado: com acesso a ferramentas de IA, as tarefas levaram 19% mais tempo, embora os próprios participantes tenham estimado, ao final, um ganho de 20%. A distância entre percepção e medição é um dos motivos pelos quais este trabalho mede tempo e intervenções a partir dos registros das sessões, e não por autorrelato.

Farrag (2026) organiza essas observações no que chama de paradoxo entre produtividade e confiabilidade. O ganho de velocidade na produção de código convive com problemas que só aparecem depois: código que viola convenções e padrões arquiteturais definidos em arquivos que ficaram fora da janela de contexto do modelo; deriva em fluxos de vários passos, nos quais etapas posteriores contradizem decisões tomadas antes; e validação circular, quando o mesmo agente escreve o código e os testes que deveriam verificá-lo. Taghavi e Bhavani (2026) chamam de cegueira de contexto um caso particular desse problema, em que o agente produz artefatos intermediários coerentes entre si, mas incompatíveis com o repositório real, com referências a APIs, caminhos e convenções que não existem. Essas três classes de problema, a perda de contexto, a erosão arquitetural e a validação circular, orientaram a escolha das métricas de produto e de transmissão de decisões deste estudo (seção 3.7).

## **2.2 Desenvolvimento orientado por especificação**

O desenvolvimento orientado por especificação propõe que a especificação, e não o código, seja o artefato central do desenvolvimento assistido por IA. Piskala (2026) resume a ideia ao afirmar que a especificação declara a intenção e o código a realiza, e descreve um fluxo de quatro fases: especificar o que o software deve fazer, com foco em comportamento e critérios de aceite; planejar como construí-lo, com arquitetura, modelos de dados, interfaces e escolhas tecnológicas; implementar em incrementos pequenos, conferidos contra a especificação e o plano; e validar o resultado por testes automatizados e revisão humana, corrigindo o código ou a especificação quando houver divergência, com a especificação como referência final.

Böckeler (2025) e Piskala (2026) distinguem três níveis de rigor. No primeiro, chamado *spec-first*, uma especificação bem pensada é escrita antes do código e usada para conduzir a tarefa, podendo ser abandonada depois. No segundo, *spec-anchored*, a especificação é mantida depois da tarefa e usada também na evolução e na manutenção do sistema. No terceiro, *spec-as-source*, a especificação é o único artefato editado por pessoas, e o código nunca é alterado manualmente. As duas metodologias comparadas aqui produzem especificações antes da implementação de cada unidade e as mantêm no repositório, mas não regeneram o código a partir delas; situam-se, portanto, entre o primeiro e o segundo nível.

A abordagem tem antecedentes. Böckeler (2025) aproxima o nível *spec-as-source* do desenvolvimento orientado por modelos, em que modelos em UML ou em linguagens textuais específicas alimentavam geradores de código, abordagem que nunca chegou a ser adotada em larga escala em aplicações de negócio. Os modelos de linguagem removem parte das restrições daquele paradigma, porque aceitam especificações em linguagem natural, mas introduzem o não determinismo: a autora observou variação no código gerado várias vezes a partir da mesma especificação. Piskala (2026) acrescenta um limite de outra natureza: passar nos testes derivados da especificação garante apenas que o software corresponde à especificação, e não que esteja correto, já que a própria especificação pode estar errada.

Esses limites têm duas consequências para este estudo. A primeira é que o volume e a forma das especificações produzidas não bastam para avaliar uma metodologia: é preciso verificar se as decisões registradas chegam ao código (métrica M14) e se o código entregue atende aos critérios de aceite segundo uma verificação independente da própria especificação (métrica M11). A segunda é que o não determinismo afeta não apenas o agente medido, mas também qualquer componente de IA do produto, o que motivou o controle descrito na seção 3.5.

## **2.3 GitHub Spec Kit**

O GitHub Spec Kit é um conjunto de ferramentas de código aberto, mantido pelo GitHub, que implementa o desenvolvimento orientado por especificação por meio de comandos executados dentro do agente de codificação (GitHub, 2026). Uma interface de linha de comando prepara o repositório com modelos de documento e scripts auxiliares e instala os comandos no agente escolhido; a partir daí, o desenvolvedor interage com o Spec Kit por comandos de barra (slash commands) no próprio agente (Böckeler, 2025). O princípio declarado pela ferramenta é que a especificação é a fonte da verdade e que o código deve servir à especificação, e não o contrário (GitHub, 2026).

O fluxo parte de uma constituição do projeto, criada pelo comando constitution, que registra princípios tratados como imutáveis e aplicados a toda mudança (Böckeler, 2025). Farrag (2026) classifica esse arquivo como um mecanismo de governança constitucional, o mais abrangente dos mecanismos de governança que propõe e também o de maior custo inicial. Cada funcionalidade percorre, então, uma sequência de comandos que produzem artefatos encadeados: specify gera a especificação funcional, com histórias de usuário e critérios de aceite; plan produz o plano técnico, com arquitetura, modelo de dados e contratos; tasks decompõe o plano em uma lista ordenada de tarefas; e implement executa essas tarefas. Comandos opcionais acrescentam etapas de esclarecimento e verificação: clarify faz perguntas sobre as ambiguidades da especificação; checklist gera listas de verificação da qualidade dos requisitos; analyze confere a consistência e a cobertura entre especificação, plano e tarefas; e converge compara o código implementado com os artefatos e acrescenta às tarefas o trabalho que falta, até declarar a funcionalidade convergida.

Cada comando lê os artefatos produzidos pelos anteriores, o que permite executá-los em sessões separadas do agente sem perda da informação registrada. O Spec Kit não define papéis distintos: o mesmo agente especifica, planeja, implementa e verifica, e o planejamento é feito uma funcionalidade por vez, à medida que o desenvolvimento avança. Na taxonomia de Macedo (2026), discutida na seção 2.5, o Spec Kit recebe nota máxima nas dimensões de especificação e de portabilidade e nota intermediária nas de contexto, papéis, execução e validação; o principal risco apontado pelo autor é a deriva entre os artefatos e a implementação quando a validação é fraca. Taghavi e Bhavani (2026) estudaram esse ponto ao acrescentar ao fluxo do Spec Kit verificações automáticas que conferem se os caminhos, as bibliotecas e as tarefas citados nos planos existem e são viáveis no repositório real.

## **2.4 BMAD-METHOD**

O BMAD-METHOD (*Breakthrough Method of Agile AI-Driven Development*) é uma estrutura de código aberto que organiza o desenvolvimento assistido por IA como o trabalho de uma equipe ágil composta por agentes especializados (BMAD Code Organization, 2026). Hassan et al. (2025) o descrevem como um exemplo de equipe de agentes projetada mais abrangente do que os subagentes do Claude Code, porque leva a metáfora da equipe ao pé da letra: os agentes assumem papéis como os de dono do produto, arquiteto, desenvolvedor e testador, e a decomposição de tarefas com especialização de papéis é apontada como a principal força da metodologia.

Na versão usada neste trabalho, os agentes são acionados por fluxos de trabalho (*skills*) instalados no agente de codificação e organizados em quatro fases (BMAD Code Organization, 2026). Na análise, uma analista de negócios conduz sessões de *brainstorming*, pesquisa de domínio e elaboração do *product brief*. No planejamento, o gerente de produto cria e valida o documento de requisitos de produto (PRD), e a designer de experiência especifica a interface. Na solução, o arquiteto define a arquitetura técnica, o gerente de produto decompõe o PRD em épicos e histórias de usuário, e o planejamento da *sprint* aplica uma verificação de prontidão, que confere a coerência entre os artefatos antes da implementação, e passa a acompanhar o andamento das histórias. Na implementação, o desenvolvedor executa o fluxo de construção, que converte cada história em uma especificação de implementação e gera o código e os testes; seguem-se a revisão de código e a geração de testes de ponta a ponta, e, ao fim de cada épico, a retrospectiva fecha o ciclo.

Duas características distinguem o BMAD-METHOD do Spec Kit. A primeira é o planejamento antecipado: o produto inteiro é analisado, especificado e arquitetado antes do início da implementação, e não uma funcionalidade por vez. A segunda é a transmissão de contexto por documentos encadeados: cada fase produz documentos que servem de contexto para a seguinte, e a implementação parte de histórias derivadas desses documentos, convertidas em especificações focadas no momento da construção (BMAD Code Organization, 2026). Hassan et al. (2025) descrevem esse mecanismo em uma versão anterior da metodologia, na qual um agente Scrum Master fragmentava o trabalho planejado em arquivos de história; na versão 6.11.0, usada neste trabalho, esse papel não existe, e a conversão de cada história em especificação é feita pelo próprio fluxo de construção. Segundo Macedo (2026), essa progressão importa porque impede que o agente de implementação trabalhe apenas a partir de uma instrução curta: a arquitetura informa as histórias, e as histórias informam a implementação. Na taxonomia do autor, o BMAD-METHOD recebe nota máxima nas dimensões de especificação, contexto, papéis e validação e nota intermediária nas de execução e portabilidade; o risco dominante apontado é o custo do processo e a disciplina de uso que ele exige.

## **2.5 Taxonomia de processo e comparação documental**

Macedo (2026) propõe uma taxonomia de processo para as ferramentas que apoiam agentes de desenvolvimento de software e a aplica a seis delas: GitHub Spec Kit, OpenSpec, BMAD-METHOD, Get Shit Done, Spec Kitty e Reversa. A taxonomia tem seis dimensões. A especificação trata de como a ferramenta transforma a intenção humana em artefatos que orientam o agente; o contexto, de como a ferramenta decide o que o agente deve saber antes de agir; os papéis, da especialização, da autoridade e do comportamento esperado de cada agente; a execução, de se a ferramenta apenas orienta o agente ou também aciona ferramentas, edita código, executa testes e interage com interfaces; a validação, dos mecanismos que verificam se o que foi produzido está correto e completo; e a portabilidade, da dependência em relação a um fornecedor, ambiente de desenvolvimento, modelo ou formato específico.

Cada dimensão recebe nota 0, quando ausente ou incipiente, 1, quando parcial, e 2, quando forte ou central no desenho da ferramenta. As notas são atribuídas a partir da documentação oficial, e o próprio autor ressalva que não constituem medição empírica independente. Nessa avaliação, o Spec Kit soma 8 pontos e o BMAD-METHOD, 10. As duas metodologias empatam nas dimensões de especificação e de execução; o BMAD-METHOD é mais forte em contexto, papéis e validação; e o Spec Kit, em portabilidade. Nenhuma das seis ferramentas atinge a nota máxima em todas as dimensões, o que leva o autor a tratar a cobertura completa do processo e a portabilidade como objetivos em tensão.

Duas observações de Macedo (2026) orientam diretamente este estudo. A primeira é que a especificação é a dimensão mais saturada, com quase todas as ferramentas na nota máxima, e, portanto, a que menos as diferencia; por isso, a contagem de artefatos produzidos é tratada aqui como descritiva (seção 3.7). A segunda é que um agente pode passar nos testes e, ainda assim, alterar indevidamente a arquitetura, remover uma restrição de negócio ou ignorar uma decisão de produto, de modo que a avaliação precisa verificar se o caminho percorrido foi auditável, e não apenas se o resultado funciona. A agenda de pesquisa proposta pelo autor inclui avaliações orientadas a processo, métricas de contexto e de ancoragem no repositório e estudos longitudinais com equipes reais. Este trabalho toma as notas documentais como proposições a verificar: se as diferenças que a documentação sugere se realizarem na prática, elas devem aparecer nas métricas associadas a cada dimensão no Quadro 8.

## **2.6 Avaliação empírica de processos com modelos de linguagem**

Estudos empíricos que envolvem modelos de linguagem enfrentam problemas de validade próprios. Baltes et al. (2025) reúnem diretrizes para esse tipo de estudo em engenharia de software, entre as quais declarar o papel do modelo no estudo, reportar o modelo, a versão, a data e todos os parâmetros de configuração, inclusive os valores padrão, que mudam com o tempo, e tratar com cautela o uso de modelos como avaliadores. Quando um modelo de linguagem julga artefatos, seus julgamentos devem ser validados contra avaliação humana, com medida de concordância, e não tomados como verdade.

A medida de concordância adotada neste trabalho é o coeficiente kappa de Cohen (1960), que corrige a proporção de concordância observada entre dois classificadores pela concordância esperada ao acaso. Landis e Koch (1977) propõem faixas de interpretação para o coeficiente, nas quais valores entre 0,61 e 0,80 indicam concordância substancial. Para as edições manuais do pesquisador, adapta-se a escala de Rasnayaka et al. (2024), que, ao estudar o uso de modelos de linguagem por estudantes em um projeto de engenharia de software, classificam o código gerado pelo grau de alteração humana: uso direto, alteração de até 10% das linhas e alteração de mais de 10% das linhas.

Os estudos mais próximos deste trabalho são os de Farrag (2026) e de Taghavi e Bhavani (2026). Farrag (2026) relata um estudo piloto do Spec Kit com 14 engenheiros, em três equipes, ao longo de quatro meses, acompanhando indicadores como o tempo de entrega por funcionalidade e medindo à parte o custo de escrever especificações e planos; o autor declara que o estudo não é controlado e que parte dos dados é de autorrelato. Taghavi e Bhavani (2026) avaliam variantes do fluxo do Spec Kit em tarefas de repositórios reais, tratam cada tarefa como sujeito pareado entre condições, usam como avaliador um modelo diferente do que gera o código, para reduzir o viés de autoavaliação, e classificam as falhas pela causa principal, como falha de validação de artefato, falha nas verificações do repositório ou implementação incompleta. Desses estudos, o presente trabalho herda a separação entre tempo de especificação e tempo de implementação, o pareamento por unidade de trabalho e a classificação das intervenções por causa.

Por fim, estudos que não são experimentos controlados exigem um enquadramento próprio. Runeson e Höst (2009) definem o estudo de caso em engenharia de software como a investigação de um fenômeno contemporâneo em seu contexto real, adequada quando o pesquisador não controla todas as variáveis, e defendem a generalização analítica em lugar da estatística. Verdecchia et al. (2023) criticam a aplicação mecânica, a outros tipos de estudo, dos roteiros de ameaças à validade concebidos para experimentos controlados, como o de Wohlin et al. (2012), e recomendam que as ameaças sejam identificadas desde o desenho, com categorias adequadas ao método. As duas referências fundamentam, respectivamente, o enquadramento metodológico (seção 3.1) e a organização das ameaças à validade (seção 3.9).

## **2.7 Fundamentos do veículo experimental**

O Cerne pertence à categoria dos diários reflexivos, aplicativos em que o usuário registra experiências e emoções. A literatura de psicologia oferece o contexto dessa categoria. Pennebaker (1997) revisa uma década de estudos em que escrever sobre experiências emocionais foi seguido de melhoras em indicadores de saúde física e mental, e associa esse efeito a mudanças nos processos cognitivos e linguísticos durante a escrita. Lieberman et al. (2007) mostram, por ressonância magnética funcional, que nomear emoções em palavras reduz a resposta da amígdala a estímulos negativos. Esses resultados explicam o interesse pela categoria, mas não são objeto deste trabalho, que não avalia efeitos do aplicativo sobre os usuários.

Com os modelos de linguagem, os diários passaram a incorporar assistentes conversacionais. Kim et al. (2024) desenvolveram o MindfulDiary, que conduz conversas diárias com pacientes psiquiátricos e as converte em registros de diário, e o avaliaram em um estudo de campo de quatro semanas com 28 pacientes e cinco psiquiatras. Nepal et al. (2024) integram ao diário dados de sensoriamento comportamental do celular, usados pelo modelo para contextualizar as perguntas de reflexão. Esses trabalhos mostram que o diário com IA é objeto de pesquisa, e não apenas categoria de produto, e oferecem precedentes para as funcionalidades conversacionais do Cerne.

Tecnicamente, a funcionalidade central do Cerne é a conversa com memória, implementada por geração aumentada por recuperação (retrieval-augmented generation, RAG). Nessa técnica, antes de gerar a resposta, o sistema recupera de uma base própria os trechos mais relevantes para a pergunta e os inclui no pedido ao modelo, o que permite respostas apoiadas em informação que o modelo não tem em seus parâmetros (Lewis et al., 2020). No Cerne, essa base é formada pelas entradas do diário do usuário, representadas por vetores numéricos (embeddings) que aproximam textos de significado parecido; a mesma representação sustenta a busca semântica.

Do lado do aplicativo, a pilha técnica fixada nos dois ciclos combina o padrão BLoC (Business Logic Component), que separa a lógica de apresentação da interface por meio de fluxos de eventos e estados, com a Clean Architecture, que organiza o código em camadas concêntricas e exige que as dependências apontem sempre para dentro, em direção às regras de negócio (Martin, 2017). Essa regra de dependência é o que permite medir violações de camada de forma automática: um import da camada de dados ou de apresentação dentro da camada de domínio é, por definição, uma violação. Li et al. (2023) tratam violações de regras arquiteturais como sintomas de erosão da arquitetura e mostram que identificá-las cedo ajuda os desenvolvedores a perceber o problema: em experimento controlado, a apresentação dos sintomas detectados elevou a taxa de detecção dos participantes de 25,9% para 64,7%.

Para a interface, o protótipo segue o padrão dos assistentes conversacionais mais difundidos, com a conversa como tela inicial e o histórico em menu lateral. A escolha apoia-se no princípio de consistência externa: os usuários passam a maior parte do tempo em outros produtos e preferem que um novo funcione como os que já conhecem (Nielsen, 2000), e o uso intuitivo depende da experiência prévia com recursos semelhantes (Blackler; Popovic; Mahar, 2010). A fidelidade do aplicativo a esse protótipo é medida por comparação de capturas de tela, abordagem também usada nas avaliações de geração de código de interface a partir de imagens, como o Design2Code (Si et al., 2025) e o DOne (Huang et al., 2026), que combinam métricas automáticas de similaridade visual com avaliação humana.

## **2.8 Síntese e lacuna de pesquisa**

A literatura revisada permite três constatações. A primeira é que os agentes de codificação já executam tarefas completas de desenvolvimento, mas o ganho de produtividade que prometem convive com perda de contexto entre etapas, erosão arquitetural e validação circular (Farrag, 2026; Taghavi; Bhavani, 2026). A segunda é que o desenvolvimento orientado por especificação é uma resposta a esses problemas, e o Spec Kit e o BMAD-METHOD são duas implementações dessa resposta com organizações de processo distintas: um agente único com planejamento incremental, no primeiro, e agentes especializados com planejamento antecipado, no segundo (Hassan et al., 2025; Macedo, 2026). A terceira é que a comparação existente entre as duas metodologias é documental: as notas de Macedo (2026) descrevem o que a documentação promete, e os estudos empíricos disponíveis tratam de uma metodologia por vez (Farrag, 2026; Taghavi; Bhavani, 2026).

A lacuna que este trabalho procura preencher é, portanto, a ausência de uma comparação empírica entre o GitHub Spec Kit e o BMAD-METHOD aplicados ao mesmo produto, com as demais condições fixadas, que meça ao mesmo tempo o custo do processo, a qualidade do produto e a transmissão das decisões de planejamento até o código. O capítulo 3 descreve como essa comparação foi desenhada.

# **3 MÉTODO DE PESQUISA**

Este capítulo descreve como o estudo foi desenhado e conduzido. A seção 3.1 caracteriza o tipo de pesquisa; a seção 3.2 apresenta as questões que orientam a comparação; as seções 3.3 a 3.5 descrevem os dois ciclos de desenvolvimento, o aplicativo usado como veículo experimental e os mecanismos de controle; as seções 3.6 a 3.8 tratam do instrumento de medição, das métricas e do plano de análise; e a seção 3.9 discute as ameaças à validade.

## **3.1 Caracterização do estudo**

O estudo compara duas metodologias de desenvolvimento orientado por especificação, o GitHub Spec Kit e o BMAD-METHOD, aplicadas por um agente de codificação à construção de um mesmo aplicativo móvel. O objeto da pesquisa são as metodologias, e não o aplicativo: este funciona como veículo experimental neutro, cujos requisitos foram selecionados por gerarem dados comparáveis entre os dois processos.

O mesmo desenvolvedor, que é também o pesquisador, conduz os dois tratamentos em sequência, com ordem fixa e sem repetição. Esse desenho não atende às condições de um experimento controlado: não há aleatorização, não há réplicas independentes e o sujeito experimental é único. Por isso, o trabalho é caracterizado como um **estudo de caso instrumentado**, nos termos de Runeson e Höst (2009), que tratam o estudo de caso como investigação de um fenômeno contemporâneo em seu contexto real, adequada quando o controle total das variáveis não é possível. O caso estudado é o desenvolvimento do aplicativo sob cada metodologia. Dentro dele, cada requisito funcional constitui uma unidade de análise embutida, o que permite comparações pareadas entre os dois ciclos (seção 3.8).

O adjetivo "instrumentado" indica que a coleta de dados não depende de autorrelato. Tempo, consumo de *tokens*, intervenções e propriedades do código são extraídos por *scripts* a partir dos registros das sessões e dos repositórios, e as métricas que exigem julgamento são avaliadas por um modelo de linguagem externo ao experimento, com validação humana (seção 3.6). As definições de todas as medidas foram congeladas antes do primeiro comando do primeiro ciclo.

Desse enquadramento decorrem dois limites que orientam todo o capítulo. Primeiro, os resultados descrevem o comportamento das duas metodologias neste caso, com as versões, o agente e o ambiente aqui fixados, e não autorizam generalização estatística. Segundo, os testes estatísticos previstos têm papel complementar à análise descritiva, já que o estudo de caso busca generalização analítica, e não estatística (Runeson; Höst, 2009).

## **3.2 Questões de pesquisa e proposições**

A questão principal do estudo é:

**QP:** Como o GitHub Spec Kit e o BMAD-METHOD se diferenciam, quanto ao processo de desenvolvimento e ao produto resultante, quando aplicados pelo mesmo desenvolvedor, com o mesmo agente de codificação, à construção do mesmo aplicativo?

Ela se desdobra em quatro questões específicas:

  - **QP1 (custo do processo):** quanto tempo, quantos *tokens* e quantas intervenções humanas cada metodologia exige, no total e em cada fase do desenvolvimento?
  - **QP2 (transmissão de decisões):** em que medida as decisões registradas nos artefatos de planejamento de cada metodologia chegam ao código entregue?
  - **QP3 (qualidade do produto):** como os produtos de cada ciclo se comparam quanto à arquitetura, aos testes, à fidelidade visual, ao tratamento de erros e ao atendimento dos critérios de aceite?
  - **QP4 (estabilidade ao longo do ciclo):** as convenções e a integridade arquitetural se mantêm à medida que o código cresce, ou se degradam entre os primeiros e os últimos requisitos?

O estudo não pré-registra hipóteses direcionais. Em vez disso, parte das proposições estruturais que Macedo (2026) formula ao comparar as duas metodologias a partir da documentação oficial. Naquela análise, o Spec Kit e o BMAD-METHOD recebem a mesma nota nas dimensões de especificação e de execução, mas divergem nas dimensões de contexto, papéis e validação, em que o BMAD-METHOD é avaliado como mais forte. Se essas diferenças documentais se realizarem na prática, espera-se observá-las nas métricas que cada dimensão mobiliza, conforme o Quadro 8 (seção 3.7). O estudo verifica, portanto, se as diferenças que a documentação sugere aparecem no comportamento observado, sem assumir de antemão a direção do efeito.

## **3.3 Desenho dos ciclos**

O desenho compreende dois ciclos de desenvolvimento completos do mesmo aplicativo, cada um conduzido em um repositório próprio, criado vazio. No Ciclo A, o desenvolvimento segue o GitHub Spec Kit; no Ciclo B, o BMAD-METHOD. Tudo o que não é a própria metodologia foi fixado de forma idêntica nos dois ciclos. O princípio que orientou o planejamento foi separar os ciclos na execução, e não no planejamento: todas as regras específicas de cada metodologia, inclusive as do Ciclo B, foram decididas e congeladas antes do início do Ciclo A, para que nada do que fosse observado no primeiro ciclo influenciasse as regras do segundo.

### *3.3.1 Variáveis controladas*

O Quadro 1 lista o que foi fixado e o que cada metodologia pôde escolher livremente.

**Quadro 1** – Variáveis controladas e graus de liberdade dos ciclos

  

|  |  |
| :-: | :-: |
| \*\*Dimensão\*\* | \*\*Valor fixado nos dois ciclos\*\* |
| Agente de codificação | Claude Code 2.1.282, com atualização automática desligada |
| Modelo | claude-sonnet-5, identificador fixo, com nível de esforço de raciocínio high definido na configuração; subagentes forçados para o mesmo modelo; tarefas auxiliares de segundo plano em claude-haiku-4-5-20251001 |
| Superfície de uso | Extensão do Claude Code no VS Code 1.139.1, com anexação automática de contexto desligada antes de cada mensagem |
| Configuração | Um único arquivo settings.json, com o mesmo \*hash\* nos dois ciclos, incluindo a lista de permissões, com a sincronização de recursos da conta do usuário e os conectores da conta desligados |
| Plataforma | iOS, em um único iPhone 16 Pro físico |
| Máquina | MacBook Pro com Apple M1 Pro e 16 GB de memória; macOS 27.0.1, com atualizações automáticas desligadas até o fim do Ciclo B |
| Ferramentas de compilação | Flutter 3.47.5 e Dart 3.13.4, fixados por fvm; Xcode 27.0, atualizado para 27.1 no fim do Ciclo A (seção 3.9) |
| Pilha técnica do aplicativo | flutter\\\_bloc; Clean Architecture em três camadas; fpdart (Either\\\<Failure, T\\\>); mocktail; whisper\\\_ggml para transcrição local; design\\\_tokens.dart como fonte única dos \*tokens\* visuais; convenção de pastas lib/core/ e lib/features/\\\<feature\\\>/{data,domain,presentation}/ |
| Informação de produto | Pacote de entrada idêntico, verificado por \*hash\*, e 14 \*prompts\* de intenção neutros quanto à metodologia |
| Idioma | Inglês nos \*prompts\*, nos documentos do pacote, nos artefatos e no código; português nos textos de interface, reproduzidos do protótipo |
| Backend | Mesmo backend congelado, em ambientes isolados com \*schema\* idêntico |
| Plano de uso do agente | Mesma assinatura nos dois ciclos |
| \*\*Livre para cada metodologia\*\* | Roteamento, cliente HTTP, cache local, injeção de dependência, armazenamento seguro e pacotes de biometria e de gráficos |

  

Fonte: elaborado pelo autor (2026).

A pilha técnica foi fixada para que as métricas de produto pudessem ser calculadas com o mesmo mapa de camadas nos dois ciclos e para que as diferenças observadas não decorressem de escolhas tecnológicas. Os graus de liberdade restantes foram deixados de propósito: é nesse espaço que as metodologias podem divergir, e essa divergência é dado.

Duas decisões sobre a forma de uso do agente merecem registro. A primeira é a superfície: a extensão do VS Code anexa a cada mensagem o arquivo aberto e o trecho selecionado, sem opção de desligamento permanente. Para que esse contexto não chegasse ao agente de forma desigual, o pesquisador fecha todos os editores e desliga a anexação antes de cada mensagem, e o instrumento conta, por sessão, as mensagens que ainda assim chegaram com contexto da IDE. A segunda é a plataforma. O desenho original previa a execução em simulador, mas o teste de ambiente mostrou que o whisper\_ggml, parte da pilha fixa, não compila para o simulador do iOS, limitação documentada do pacote. Os dois ciclos passaram, então, a rodar inteiramente em um aparelho físico.

### *3.3.2 Tratamento A: GitHub Spec Kit*

O Ciclo A usa o GitHub Spec Kit na versão 1.0.10 (GITHUB, 2026), instalada em modo não interativo e sem extensões ou pacotes adicionais. A preparação ocorre uma única vez, com o comando constitution, que recebe o *prompt* de princípios do projeto. Cada unidade de trabalho percorre, em seguida, a sequência completa de comandos, incluindo os opcionais:

specify → clarify → plan → checklist → tasks → analyze → implement → converge

Os comandos implement e converge se repetem em laço até que o converge declare a unidade convergida. A opção por incluir todos os comandos opcionais buscou simetria com o Ciclo B, que também é executado em sua forma completa. O protocolo congelado previa o checklist antes do plan; na primeira unidade, verificou-se que, na versão instalada, o checklist exige o plano como pré-requisito, e a ordem foi ajustada para a indicada pela própria ferramenta, com registro como desvio (Apêndice F).

Cada comando é executado em uma sessão nova do agente. Como o Spec Kit guarda seu estado em arquivos e cada comando lê os artefatos produzidos pelo anterior, a documentação oficial não exige sessão contínua, e essa regra torna os dois ciclos simétricos quanto à forma de transmitir contexto entre fases: nos dois, o contexto passa de uma etapa para a seguinte apenas por meio de artefatos. A consequência metodológica dessa escolha é discutida na seção 3.9.

### *3.3.3 Tratamento B: BMAD-METHOD*

O Ciclo B usa o BMAD-METHOD na versão 6.11.0 (BMAD CODE ORGANIZATION, 2026), com o módulo principal e a trilha padrão para produtos com documento de requisitos e arquitetura. A instalação é feita por parâmetros, sem respostas interativas. O fluxo foi executado de forma completa, em cinco blocos:

1.  **Preparação:** geração do contexto de projeto, que recebe o mesmo *prompt* de princípios usado na constitution do Ciclo A.
2.  **Análise:** *brainstorming*, refinamento da ideia, investigação, documento de perguntas frequentes e *product brief*.
3.  **Planejamento:** criação e validação do documento de requisitos de produto e especificação de experiência do usuário a partir do protótipo congelado, sem alterá-lo.
4.  **Solução:** arquitetura, épicos e histórias, e planejamento da *sprint*, que inclui a verificação de prontidão para implementação.
5.  **Implementação:** para cada história, construção, revisão de código e geração de testes de ponta a ponta; ao fim de cada épico, uma retrospectiva.

Cada fluxo de trabalho é executado em uma sessão nova, como a própria metodologia orienta. Os três primeiros blocos depois da preparação constituem o planejamento global, sem equivalente no Ciclo A, e têm limite próprio de 32 horas de tempo ativo. Recursos de elicitação avançada e de discussão entre agentes simulados, quando oferecidos pela metodologia, são aceitos, e as escolhas feitas pelo pesquisador nesses momentos são registradas.

A diferença central entre os tratamentos fica visível na forma como a informação de produto entra em cada ciclo. No Spec Kit, o pesquisador especifica uma unidade por vez, e o *prompt* de cada requisito entra no comando specify da unidade correspondente. No BMAD-METHOD, todos os *prompts* de requisito entram de uma só vez na criação do documento de requisitos, e a implementação parte das histórias geradas no planejamento. Não se trata de assimetria de informação, pois o documento de requisitos completo está disponível nos dois repositórios desde o início, mas da diferença que se quer observar: planejamento incremental, no Spec Kit, e planejamento antecipado, no BMAD-METHOD.

### *3.3.4 Unidades de trabalho, ordem e limite de tempo*

O trabalho de cada ciclo é dividido em onze unidades: uma fundação (F000), que reúne a estrutura do projeto, os *tokens* visuais, o cliente HTTP, o cadastro e o acesso, a navegação base e o tratamento de sessão expirada, e uma unidade por requisito funcional. A ordem é a mesma nos dois ciclos:

F000 → RF03 → RF01 → RF02 → RF07 → RF06 → RF04 → RF10 → RF08 → RF05 → RF09

Duas posições dessa sequência decorrem de dependências: o RF10 vem depois do RF01 e do RF04, e o RF08 depois do RF04.

Uma unidade é considerada concluída quando quatro condições se verificam ao mesmo tempo: a metodologia declara a unidade pronta (no Spec Kit, o converge reporta convergência; no BMAD-METHOD, a revisão de código aprova a última história da unidade); a análise estática do Flutter não aponta erros; os testes escritos pelo próprio agente passam; e o pesquisador percorre, no aparelho, os critérios de aceite do requisito. Problemas encontrados nessa verificação são tratados em sessões de correção, sempre abertas por uma mensagem que descreve o sintoma, e nunca a solução.

Cada unidade tem um limite de oito horas de tempo ativo em sessão, ou doze horas no caso da fundação, somando todas as sessões, inclusive as de correção. O limite é um teto, e não uma meta. Uma unidade que o atinge é encerrada como não concluída, recebe uma marca própria no repositório e entra na análise com o tempo registrado como valor censurado; o ciclo prossegue normalmente. Durante o Ciclo A, acrescentou-se uma terceira forma de encerramento, válida também para o Ciclo B: o pesquisador pode encerrar como não concluída, antes do limite de tempo, uma unidade cujo critério de aceite continua falhando depois de sucessivas sessões de correção. Nesse caso, o tempo não é tratado como censurado, e a unidade recebe marcação própria na análise.

O Ciclo A foi executado primeiro, por decisão tomada no planejamento (decisão D18), em razão da maior familiaridade do pesquisador com o Spec Kit. Antes do início do Ciclo B, o pesquisador registra por escrito o que aprendeu no Ciclo A e que pode influenciar o segundo ciclo, e deixa de acessar o repositório do Ciclo A até o fim do Ciclo B. Esse registro alimenta a discussão sobre o efeito de ordem na seção 3.9. O atraso acumulado no Ciclo A encurtou o calendário do Ciclo B, sem alterar os limites de tempo ativo de cada unidade.

### *3.3.5 Regras de interação do pesquisador*

Como o pesquisador é também o operador dos dois ciclos, suas mensagens ao agente precisam ser classificadas para que possam ser contadas e comparadas. Cada mensagem pertence a uma de três categorias:

  - **Mensagens neutras**, que não são contadas: confirmações de avanço dadas a pausas que o agente fez por conta própria e a transcrição de mensagens de erro solicitadas pelo agente.
  - **Respostas de processo**, marcadas com o prefixo PROCESSO:: respostas a pausas previstas pela própria metodologia, como as perguntas do clarify no Spec Kit ou as elicitações dos agentes de análise e de produto no BMAD-METHOD. A lista dessas pausas foi congelada para as duas metodologias antes do Ciclo A.
  - **Intervenções**, marcadas com o prefixo INTERVENÇÃO, seguido do tipo e, quando aplicável, da severidade, do nível de edição e da causa. Toda mensagem que não se enquadra nas duas categorias anteriores é uma intervenção.

A separação entre respostas de processo e intervenções evita que o BMAD-METHOD seja penalizado apenas por prever, por desenho, mais pontos de interação. As respostas a perguntas das metodologias seguem uma política fixa: o pesquisador responde apenas com o que está no pacote de entrada, citando a seção; quando o pacote não cobre a pergunta, consulta um registro de respostas já dadas; e, quando nem o registro a cobre, decide na hora e acrescenta a decisão ao registro, para que pergunta equivalente no outro ciclo receba resposta com o mesmo texto. Preferências de gosto recebem sempre a mesma resposta padrão, que devolve a escolha ao critério técnico do agente. Perguntas feitas pelo agente por iniciativa própria, fora das pausas previstas, seguem uma regra complementar: quando apenas pedem confirmação, recebem resposta neutra; quando pedem uma escolha ou uma informação, a resposta é registrada como intervenção do tipo esclarecimento não solicitado e reportada à parte.

A edição manual de código ou de artefatos gerados pelas metodologias é proibida como rotina. Quando inevitável, é registrada como intervenção, com o nível de alteração estimado no momento. Por fim, a primeira mensagem de cada sessão é sempre o comando da metodologia, digitado, seguido do argumento colado; essa forma garante que o agente receba o comando como tal e que o instrumento identifique a fase da sessão.

## **3.4 Veículo experimental: o aplicativo Cerne**

### *3.4.1 Visão do produto e requisitos*

O Cerne é um aplicativo móvel de diário reflexivo com inteligência artificial. O usuário registra entradas por texto, áudio ou fotografia, conversa com um assistente que consulta as entradas anteriores por busca semântica e acompanha resumos de sua evolução ao longo do tempo. As entradas do diário e as mensagens de conversa são separadas: apenas as entradas alimentam a base consultada pelo assistente, e a única ponte entre os dois espaços é a ação explícita de salvar uma mensagem como entrada.

Os requisitos foram organizados pela capacidade de gerar dados comparativos, e não pela completude do produto. O núcleo construído e medido nos dois ciclos tem dez requisitos funcionais, apresentados no Quadro 2, cada um com critérios de aceite verificáveis.

**Quadro 2** – Requisitos funcionais do núcleo comparativo

  

|  |  |
| :-: | :-: |
| \*\*Requisito\*\* | \*\*Descrição resumida\*\* |
| RF01 | Captura multimodal de entradas (texto, áudio e fotografia), todas persistidas no mesmo formato |
| RF02 | Transcrição local de áudio e reconhecimento de texto em imagem, com quatro estados visíveis |
| RF03 | Cofre de acesso por biometria, com PIN como alternativa e nova autenticação após cinco minutos em segundo plano |
| RF04 | Conversa com memória por busca semântica, com resposta transmitida em fluxo e tratamento de queda no meio da resposta |
| RF05 | Exportação de resumo pessoal em PDF, com download dos dados brutos mesmo quando a geração do texto falha |
| RF06 | Busca semântica combinada com filtros de metadados |
| RF07 | Linha do tempo das entradas, com estado que depende de autenticação, sincronização e dados |
| RF08 | Sugestões proativas inseridas na conversa, com isolamento de falha |
| RF09 | Painel de resumos temporais com gráfico e texto narrativo |
| RF10 | Salvamento de uma mensagem do usuário como entrada do diário, sem acoplamento direto entre funcionalidades |

  

Fonte: elaborado pelo autor (2026).

Três funcionalidades presentes no protótipo (planos de ação, seletor de persona e marcadores manuais) foram classificadas como extensões de produto e não recebem implementação em nenhum dos ciclos. Quanto aos requisitos não funcionais, quatro são medidos de forma automatizada: ausência de violações de camada (RNF06), cobertura de testes no domínio de pelo menos 80% (RNF07), fidelidade visual ao protótipo (RNF08) e tratamento consistente de erros de rede (RNF09). Os demais (latência de interface, remoção de dados pessoais identificáveis antes do envio a provedores de IA, retenção zero de dados pelos provedores, isolamento por linha no banco e exclusão completa de conta) são atendidos pelo backend ou tratados como requisitos de higiene, fora da comparação.

### *3.4.2 Protótipo de referência*

A interface do aplicativo foi definida em um protótipo navegável produzido com o Claude Design e congelado antes dos ciclos, com *hash* SHA-256 registrado. O protótipo reúne um catálogo de estados de tela e um painel de *tokens* visuais (cores, tipografia e espaçamentos), que servem de referência única para a métrica de fidelidade visual nos dois ciclos. O padrão de navegação segue o dos assistentes conversacionais mais difundidos, com a conversa como tela inicial e o histórico em menu lateral, em observância ao princípio de consistência externa (Nielsen, 2000; Blackler; Popovic; Mahar, 2010). A escolha também serve ao desenho experimental: um padrão de mercado reduz a chance de que decisões originais de interface se tornem variável entre os ciclos.

### *3.4.3 Backend compartilhado*

O backend foi construído uma única vez, antes dos ciclos e fora da comparação, com a abordagem RIPER, e foi congelado em uma versão marcada no repositório. Os dois ciclos consomem exatamente o mesmo backend, o que restringe a comparação ao desenvolvimento do aplicativo móvel e elimina o backend como fonte de variação.

A infraestrutura usa o Supabase, com PostgreSQL, extensão pgvector, autenticação, armazenamento e isolamento por linha (*Row Level Security*). O contrato expõe 23 *endpoints* e uma taxonomia de 13 códigos de erro, todos no formato { code, message, retryable }. A conversa usa o modelo Claude Sonnet 5; reconhecimento de texto em imagem, detecção de dados pessoais, sugestões, painel e exportação usam o Claude Haiku 4.5; os vetores de busca são gerados pelo modelo voyage-4 da Voyage AI, com 1.024 dimensões. A transcrição de áudio ocorre no próprio aparelho, e o áudio nunca chega ao backend.

O projeto do backend foi documentado em dezoito decisões de arquitetura, identificadas de D1 a D18 (Apêndice A). Três ambientes isolados foram criados: um de desenvolvimento e um para cada ciclo, com *schema* conferido por *hash* antes do início dos ciclos. Defeitos do backend encontrados durante um ciclo não são corrigidos no meio do ciclo; são registrados segundo uma política própria (decisão D16), para que os dois ciclos enfrentem o mesmo backend.

## **3.5 Controle do não determinismo da IA do produto**

Respostas de modelos de linguagem variam entre chamadas idênticas. Se o aplicativo de cada ciclo recebesse respostas diferentes do backend durante a avaliação, parte das diferenças medidas viria do provedor de IA, e não das metodologias. Para eliminar essa fonte de variação, o backend implementa um cache de respostas de IA com reprodução determinística.

O mecanismo depende de três decisões. Os *prompts* são montados no servidor, nunca no aplicativo, com versão fixa (decisão D5); a entrada de cada operação é normalizada em um envelope canônico, com chaves ordenadas; e a chave do cache é o *hash* SHA-256 desse envelope. Assim, duas requisições com o mesmo conteúdo produzem a mesma chave, qualquer que seja a implementação do aplicativo que as enviou. O backend opera em quatro modos, descritos no Quadro 3.

**Quadro 3** – Modos do cache de respostas de IA

  

|  |  |  |
| :-: | :-: | :-: |
| \*\*Modo\*\* | \*\*Comportamento\*\* | \*\*Uso no estudo\*\* |
| off | Sempre chama o provedor, sem usar o cache | Desenvolvimento do backend |
| record | Usa o cache; na ausência de resposta, chama o provedor e grava o resultado | Passada única de gravação na avaliação |
| replay | Idêntico a record | Desenvolvimento dentro dos ciclos |
| replay\\\_strict | Usa o cache; na ausência de resposta, falha com o código REPLAY\\\_MISS | Todas as execuções medidas |

  

Fonte: elaborado pelo autor (2026).

Durante os ciclos, os ambientes operam em replay, porque o desenvolvimento não é medido e o cache dessa fase é descartado. Na avaliação, o procedimento é o seguinte: o ambiente do Ciclo A é restaurado ao estado inicial e a suíte de avaliação é executada uma única vez em modo record; o cache resultante é exportado; os dois ambientes são restaurados e recebem esse mesmo cache; e todas as execuções medidas, nos dois ciclos, ocorrem em replay\_strict. Uma ausência de resposta no cache indica que o aplicativo enviou uma requisição diferente das previstas pela suíte. Esse caso é registrado como achado sobre o aplicativo, e o cenário correspondente é reexecutado com IA ao vivo e assim marcado nos resultados.

A restauração de cada ambiente segue sempre um procedimento de quatro passos: devolver o banco ao estado inicial, reconfigurar o processador de tarefas assíncronas, reimportar o cache congelado, quando existente, e regenerar os vetores das entradas iniciais a partir do próprio cache. Uma restauração parcial apagaria o cache recém-importado e transformaria toda chamada de IA em falha.

O controle se estende ao banco de dados. A busca vetorial usa varredura exata, sem índices aproximados, e toda ordenação termina com desempate pelo identificador. Mesmo os vetores das entradas iniciais passam pelo cache: durante a construção do backend, observou-se que vetores gerados em chamadas distintas para o mesmo texto não eram idênticos, o que alterava a pontuação de similaridade entre ambientes e bastava para quebrar a comparação.

## **3.6 Instrumento de medição**

### *3.6.1 Princípios e arquitetura*

O instrumento de medição foi construído como um repositório próprio, separado dos repositórios dos ciclos, e obedece a seis princípios:

1.  **Invisibilidade para o agente medido:** nada do instrumento entra no contexto do agente durante o desenvolvimento.
2.  **Determinismo sempre que possível:** toda métrica calculável por *script* é calculada por *script*; o modelo de linguagem nunca calcula números.
3.  **Julgamento externo e validado:** as métricas que exigem julgamento são avaliadas por um modelo de outra família, com rubrica congelada, três execuções por item e validação humana por amostra.
4.  **Paridade entre ciclos:** *scripts*, rubricas, *prompts* do avaliador e suíte de avaliação são idênticos nos dois ciclos, com *hash* registrado.
5.  **Pré-registro de definições:** as definições de todas as medidas foram congeladas antes do Ciclo A; o código de avaliação pôde ser construído durante o ciclo, porque é aplicado sobre versões preservadas dos repositórios, igualmente nos dois ciclos.
6.  **Nenhum rastro no repositório medido:** nenhum resultado de medição é gravado no repositório de um ciclo; a avaliação opera sobre cópias temporárias.

O repositório do instrumento contém o protocolo, as definições das métricas, o pacote de entrada, os *prompts* de intenção, os *scripts* de coleta e de avaliação, a suíte de avaliação de caixa-preta, as rubricas do avaliador e os dados coletados. Ele nunca é aberto durante uma sessão de desenvolvimento.

O pesquisador também é mantido cego quanto aos resultados durante a execução. Nenhuma métrica de produto ou diferencial do Ciclo A é calculada ou consultada antes do fim do Ciclo B, e o registro de cada sessão não exibe tempo, *tokens* ou custo, apenas a confirmação do registro e a faixa de consumo do limite de tempo da unidade. Sem essa regra, o pesquisador poderia ajustar o próprio comportamento no segundo ciclo em função dos números do primeiro.

### *3.6.2 Coleta por sessão*

Toda sessão de desenvolvimento termina com um comando de coleta, executado pelo pesquisador. O comando é instalado como *skill* de usuário, fora do repositório do ciclo, e configurado para não ser carregado no contexto do modelo, o que foi verificado antes do início dos ciclos. Ele aciona um *script* que lê o registro completo da sessão (*transcript*) gravado pelo Claude Code, incluindo os registros de subagentes, corta tudo a partir da mensagem de invocação e grava os dados em arquivos tabulares. A telemetria OpenTelemetry fica ativa nos dois ciclos como fonte de conferência: divergências acima da tolerância fixada no protocolo são registradas, e nunca corrigidas manualmente. Sessões interrompidas por limite de uso do plano de assinatura, nas quais o comando não pode ser executado, são coletadas pelo mesmo *script* em modo manual.

Para cada sessão, o *script* registra:

  - *tokens* de entrada, saída, leitura e escrita de cache, separando a parcela dos subagentes;
  - tempo bruto e tempo ativo, em que cada espera pelo pesquisador conta até 30 minutos e o excedente é tratado como pausa;
  - as intervenções e respostas de processo, com seus campos;
  - a fase de cada trecho da sessão;
  - o número de mensagens que chegaram com contexto anexado pela IDE.

A atribuição de fase usa três categorias macro, especificação (ESPEC), implementação (IMPL) e validação (VALID), a partir de uma tabela congelada que associa cada comando do Spec Kit e cada fluxo do BMAD-METHOD a uma fase (Quadro 4). Mensagens sem marcador herdam a fase do marcador anterior. Essa segmentação, inspirada na separação entre tempo de especificação e tempo de implementação usada por Farrag (2026), permite comparar onde cada metodologia concentra seu custo.

**Quadro 4** – Atribuição de fases aos comandos e fluxos das metodologias

  

|  |  |  |
| :-: | :-: | :-: |
| \*\*Fase\*\* | \*\*GitHub Spec Kit\*\* | \*\*BMAD-METHOD\*\* |
| ESPEC | constitution, specify, clarify, plan, tasks | Contexto de projeto, análise, criação do documento de requisitos, experiência do usuário, arquitetura, épicos e histórias, correção de curso |
| IMPL | implement; sessões de correção | Construção de histórias; sessões de correção |
| VALID | checklist, analyze, converge | Validação do documento de requisitos, planejamento da \*sprint\* com verificação de prontidão, revisão de código, testes de ponta a ponta, retrospectivas |

  

Fonte: elaborado pelo autor (2026), a partir do protocolo congelado.

O progresso de cada ciclo é marcado por etiquetas no repositório: estado inicial, metodologia instalada, preparação concluída, planejamento global concluído (apenas no Ciclo B), cada unidade concluída ou incompleta e estado final. As etiquetas permitem reconstruir o código de qualquer unidade e servem de base para as métricas calculadas unidade a unidade.

### *3.6.3 Suíte de avaliação de caixa-preta*

A conformidade funcional não é medida pelos testes que o próprio agente escreveu, porque testes gerados junto com o código tendem a espelhá-lo (Farrag, 2026). Em seu lugar, usa-se uma suíte de avaliação de caixa-preta (*hold-out*), escrita antes do Ciclo A a partir dos critérios de aceite e dos textos visíveis do protótipo, mantida fora dos repositórios dos ciclos e nunca executada durante o desenvolvimento.

A suíte tem três componentes. Fluxos automatizados de interface, escritos com o Maestro, percorrem o aplicativo identificando elementos apenas pelo texto visível e capturam as telas usadas na métrica de fidelidade visual. Um *proxy* de interceptação (mitmproxy) injeta, nas requisições, os cabeçalhos que acionam no backend as falhas simuladas e conta requisições para verificar o intervalo mínimo entre buscas. Consultas SQL verificam o estado do banco, como a ausência de entradas parciais e a idempotência do salvamento a partir da conversa.

O conteúdo da suíte compreende 28 cenários que cobrem os 27 critérios de aceite dos dez requisitos, três deles verificados estaticamente; 15 cenários de falha de rede, que combinam os cinco *endpoints* de escrita com três tipos de falha (tempo esgotado, resposta malformada e ausência de conexão); e a lista de estados de tela avaliados quanto à fidelidade visual. A suíte é executada uma única vez por ciclo, sobre a versão final do aplicativo. Caso sua implementação não esteja validada até a data de corte definida no protocolo, ela é substituída por uma lista de verificação manual roteirizada, com gravação de tela, e a substituição é declarada nos resultados.

### *3.6.4 Avaliador baseado em modelo de linguagem*

Quatro medidas exigem julgamento que não pode ser reduzido a regras: as divergências não documentadas entre plano e código, o espaçamento visual em relação ao protótipo, a implementação das decisões de arquitetura selecionadas e a severidade dos defeitos corrigidos. Para elas, o estudo usa um modelo de linguagem como avaliador, com as salvaguardas que Baltes et al. (2025) recomendam para estudos empíricos com esse tipo de modelo.

O avaliador é o modelo gpt-5.5-2026-04-23, da OpenAI, identificado por versão datada e com parâmetro de esforço de raciocínio fixado em todas as chamadas. A escolha de um fornecedor diferente do agente medido reduz o risco de que o avaliador favoreça código produzido por um modelo da própria família. Taghavi e Bhavani (2026) adotam precaução semelhante ao separar o modelo avaliador do modelo que gera o código, para reduzir o viés de autoavaliação. Cada medida tem rubrica e formato de saída congelados. O avaliador não recebe o nome da metodologia nem o ciclo de origem, e os artefatos são anonimizados antes do envio. Cada item é avaliado três vezes, e o resultado é o voto da maioria.

A confiabilidade do avaliador é verificada por amostragem. Para cada medida, uma amostra de pelo menos 20 itens, somada a todos os itens sem maioria, é classificada às cegas pelo pesquisador, sem acesso ao voto do avaliador nem ao ciclo de origem, e a concordância é calculada pelo coeficiente kappa de Cohen (Cohen, 1960). O limiar adotado é κ ≥ 0,61, que corresponde à faixa de concordância substancial de Landis e Koch (1977). Abaixo desse limiar, a medida passa a ser reportada como exploratória, com o resultado do avaliador acompanhado do resultado humano da amostra. Nenhuma troca de avaliador ou de rubrica é feita depois de conhecidos os dados.

A classificação de severidade dos defeitos segue a ordem inversa: é feita pelo pesquisador no momento da intervenção, numa escala de três níveis, e o avaliador apenas a reclassifica em uma amostra. A classificação humana permanece como dado primário em qualquer caso, o que substitui o revisor externo que a decisão D16 não previa.

### *3.6.5 Congelamento do protocolo e registro de desvios*

As decisões de protocolo, as regras de cada metodologia, o pacote de entrada, os *prompts*, a suíte de avaliação, as rubricas e os *scripts* de coleta foram congelados em 1º de outubro de 2026, antes do primeiro comando do Ciclo A. O congelamento consiste em um arquivo com o *hash* SHA-256 de cada um desses itens e em uma etiqueta no repositório do instrumento. A partir desse ponto, qualquer alteração em um item congelado exige uma entrada prévia no registro de desvios, com o motivo e o efeito esperado sobre as métricas. O código de avaliação, construído durante os ciclos e testado em um repositório de calibração com violações plantadas, recebe congelamento próprio antes do início da avaliação.

O Apêndice B reúne os *hashes* de congelamento, e o registro de desvios é reproduzido integralmente no Apêndice F.

## **3.7 Métricas**

O instrumento define quinze métricas, organizadas em três grupos: de processo, de produto e diferenciais. O Quadro 5 resume as métricas de processo.

**Quadro 5** – Métricas de processo

  

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| \*\*Métrica\*\* | \*\*Definição\*\* | \*\*Mecanismo\*\* | \*\*Unidade\*\* |
| M1 – Tempo de preparação | Tempo de instalação somado ao das sessões de preparação da metodologia | Determinístico | Horas |
| M2 – Tempo do ciclo | Tempo ativo por unidade e total, decomposto por fase; tempo de calendário reportado à parte | Determinístico | Horas |
| M3 – Custo de \*tokens\* | \*Tokens\* por categoria e custo em dólares, calculado por tabela de preços congelada; decomposto por fase | Determinístico | \*Tokens\*; USD |
| M4 – Artefatos gerados | Contagem dos documentos de especificação produzidos, por tipo | Determinístico | Contagem |
| M5 – Intervenções | Intervenções por unidade, tipo, causa e fase; respostas de processo contadas em série separada (M5b) | Determinístico, com classificação humana no momento | Contagem |

  

Fonte: elaborado pelo autor (2026).

A M4 é tratada como descritiva: caracteriza o tratamento aplicado e não recebe interpretação de direção, porque, na análise de Macedo (2026), a especificação é a dimensão mais saturada, com quase todas as ferramentas na nota máxima, e, portanto, a que menos as diferencia, e porque a quantidade de artefatos, por si só, não indica sua qualidade. Na M5, as edições manuais recebem um nível segundo a escala de Rasnayaka et al. (2024): até 10% ou mais de 10% das linhas da mudança corrigida. A causa de cada intervenção é classificada em seis códigos, entre os quais a incompatibilidade com o repositório ou com o backend congelado, o desvio de requisito e a falha em teste ou análise estática.

O Quadro 6 resume as métricas de produto.

**Quadro 6** – Métricas de produto

  

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| \*\*Métrica\*\* | \*\*Definição\*\* | \*\*Mecanismo\*\* | \*\*Meta\*\* |
| M6 – Aderência ao plano | Percentual de tarefas concluídas, cruzamento entre arquivos citados no plano e arquivos alterados, referências a arquivos, pacotes ou elementos do backend inexistentes, e divergências não documentadas | Determinístico e avaliador | — |
| M7 – Violações de camada (RNF06) | \*Imports\* proibidos na camada de domínio, com trajetória por unidade | Determinístico | 0 |
| M8 – Cobertura do domínio (RNF07) | Cobertura de linhas em lib/\\\*\\\*/domain/\\\*\\\* | Determinístico | ≥ 80% |
| M8b – Escore de mutação | Proporção de mutantes do domínio detectados pela suíte do agente, apenas na versão final, se a ferramenta for validada na calibração | Determinístico | — |
| M9 – Fidelidade visual (RNF08) | Escore de 0 a 3 por estado (cor primária, tipografia, espaçamento) e contagem de valores fixos fora dos \*tokens\* | Determinístico e avaliador | 3 por estado; 0 valores fixos |
| M10 – Erros de rede (RNF09) | Assinaturas de repositório no padrão Either e cenários de falha tratados | Determinístico | 0 fora do padrão; 15 de 15 |
| M11 – Critérios de aceite | Critérios atendidos na versão final, por requisito, pela suíte de avaliação | Determinístico | — |
| M12 – Complexidade ciclomática | Média por método no domínio e contagem de métodos acima de 10 | Determinístico | — |
| M13 – Regressão | Percentual de testes do agente que passavam numa unidade e falham na seguinte; testes apagados contados à parte | Determinístico | — |

  

Fonte: elaborado pelo autor (2026).

Algumas escolhas de operacionalização se afastam da especificação original dos requisitos e são registradas como desvios. A M7 e a M12 são calculadas por *scripts* próprios, e não por ferramentas de terceiros: a primeira lê os *imports* de cada arquivo e aplica o mapa de camadas da convenção de pastas; a segunda aplica a regra de McCabe (1976) sobre a árvore sintática do código. A M10 mede os cenários de falha pela suíte de avaliação, e não pelos testes simulados que o próprio agente escreveria. A M8 é interpretada como indicador da disciplina de teste do agente, e não da eficácia da suíte, já que mede apenas linhas executadas por testes que o próprio agente escreveu; a evidência funcional vem da M10 e da M11.

O Quadro 7 apresenta as métricas diferenciais, desenhadas para captar a transmissão de decisões entre fases.

**Quadro 7** – Métricas diferenciais

  

|  |  |  |
| :-: | :-: | :-: |
| \*\*Métrica\*\* | \*\*Definição\*\* | \*\*Mecanismo\*\* |
| M14 – Fidelidade de \*handoff\* | Das dez decisões técnicas selecionadas nos artefatos de planejamento por critério pré-registrado, quantas aparecem corretamente implementadas no código final | Determinístico e avaliador |
| M15 – Consistência de padrões | Quatro convenções pré-registradas, tomando como referência a funcionalidade do RF01, verificadas em cada funcionalidade | Determinístico |

  

Fonte: elaborado pelo autor (2026).

O critério de seleção da M14 privilegia decisões que atravessam fronteiras de fase ou de papel, isto é, definidas no planejamento ou na arquitetura e consumidas na implementação, porque são essas que o construto pretende medir. A M15 compara funcionalidades construídas em momentos distantes do ciclo e testa a previsão de que convenções estabelecidas fora da janela de contexto do agente tendem a ser violadas (Farrag, 2026).

O Quadro 8 relaciona as métricas às seis dimensões da taxonomia de Macedo (2026) e às notas que o autor atribui a cada metodologia com base na documentação oficial.

**Quadro 8** – Métricas por dimensão da taxonomia de Macedo (2026)

  

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| \*\*Dimensão\*\* | \*\*Nota documental do Spec Kit\*\* | \*\*Nota documental do BMAD-METHOD\*\* | \*\*Métricas que observam a dimensão\*\* |
| Especificação | 2 | 2 | M4, M6, M11 |
| Contexto | 1 | 2 | M5 (causa de contexto), M6, M7, M14, M15 |
| Papéis | 1 | 2 | M14; M2 e M3 por fase |
| Execução | 1 | 1 | M2, M3, M5 |
| Validação | 1 | 2 | M5b, M6, M8, M8b, M13 |
| Portabilidade | 2 | 1 | Não medida: o agente é variável controlada |

  

Fonte: elaborado pelo autor (2026), a partir de Macedo (2026).

## **3.8 Plano de análise**

A análise é, antes de tudo, descritiva. Para cada métrica, os dois ciclos são comparados por valores totais, por unidade e, quando aplicável, por fase. Os resultados são organizados pelas dimensões do Quadro 8, o que permite confrontar o comportamento observado com as notas documentais de Macedo (2026), e são interpretados à luz do paradoxo entre produtividade e confiabilidade descrito por Farrag (2026): reduções de tempo só são lidas em conjunto com as métricas de confiabilidade (M6, M11, M13 e M14).

As comparações estatísticas usam o requisito funcional como unidade de pareamento, à semelhança de Taghavi e Bhavani (2026), que tratam cada tarefa como sujeito pareado entre condições. Isso resulta em até dez pares; a fundação e a preparação ficam fora do pareamento. O par principal de cada requisito considera apenas as fases de implementação e de validação. A fase de especificação é comparada no nível do ciclo, somando-se o tempo de especificação de todos os requisitos no Ciclo A e o do planejamento global somado ao de especificação das histórias no Ciclo B. Essa separação é necessária porque o Spec Kit planeja um requisito por vez e o BMAD-METHOD planeja tudo antecipadamente: comparar a especificação requisito a requisito atribuiria ao Spec Kit um custo que, no BMAD-METHOD, está concentrado no planejamento global.

O teste adotado é o de postos sinalizados de Wilcoxon para amostras pareadas (Wilcoxon, 1945), com diferenças nulas tratadas pelo método de Pratt e tamanho de efeito reportado pela correlação bisserial de postos. Unidades que atingiram o limite de tempo entram nos pares com o valor do teto, marcadas como censuradas, e uma análise de sensibilidade repete o teste sem esses pares. Com no máximo dez pares, o poder do teste é baixo, e o valor de p não é o resultado principal. As métricas definidas apenas no nível do ciclo (M1, M4, M14 e M15) recebem tratamento exclusivamente descritivo.

## **3.9 Ameaças à validade**

Verdecchia et al. (2023) observam que a seção de ameaças à validade costuma ser tratada na engenharia de software como formalidade, preenchida ao fim do trabalho com categorias genéricas e pouca reflexão, e defendem que as ameaças sejam consideradas desde o desenho do estudo, com categorização adequada ao tipo de pesquisa. Seguindo essa orientação, as ameaças abaixo foram identificadas e tratadas durante o planejamento e são organizadas pela origem no desenho deste estudo, e não pelo roteiro de Wohlin et al. (2012), concebido para experimentos controlados. Quando pertinente, indica-se a categoria clássica correspondente.

**Ameaças do desenho.** O pesquisador é o único sujeito e opera os dois ciclos, o que impede separar o efeito da metodologia do efeito do operador e limita qualquer generalização (validade externa). A ordem fixa dos ciclos faz com que cada diferença pareada some o efeito da metodologia, o aprendizado do pesquisador sobre o aplicativo e o ambiente, e eventuais mudanças silenciosas de comportamento do modelo comercial ao longo do tempo, componentes que o teste estatístico não separa (validade interna). Para reduzir essa ameaça, o aprendizado prévio é registrado por escrito antes do Ciclo B, o ambiente é conferido na transição entre ciclos e o modelo, a data e a versão da ferramenta são registrados em cada sessão. A diferença de custo em *tokens* entre as metodologias carrega um confundimento estrutural: um fluxo com agentes especializados e mais fases tende a consumir mais *tokens* por construção, de modo que parte da diferença pode refletir a topologia do processo, e não ineficiência. Por isso, a M3 é decomposta por fase e acompanhada de descritores da composição do consumo.

A regra de uma sessão por comando no Spec Kit também altera o contraste previsto inicialmente nos requisitos, que opunha um agente único com contexto contínuo a um fluxo com reinício de contexto entre fases. Como os dois ciclos passaram a transmitir contexto apenas por artefatos, a hipótese correspondente foi reformulada: a M14 mede o quanto os artefatos de cada metodologia carregam as decisões até o código. O contraste entre agente único e agentes especializados permanece, mas o de contexto contínuo deixa de variar entre os ciclos.

No Ciclo B, as etapas de *brainstorming* e de refinamento de ideia solicitam contribuições do pesquisador, e as elicitações avançadas envolvem escolhas livres. Ainda que as respostas se limitem ao pacote de entrada e as escolhas sejam registradas, ideias externas ao pacote podem entrar nos artefatos e alterar o escopo apenas desse ciclo. Além disso, a geração de testes de ponta a ponta acrescenta ao Ciclo B testes que o Ciclo A não tem, com efeito possível sobre a M8 e a M13.

**Ameaças do ambiente.** A extensão do VS Code pode anexar contexto às mensagens; a ameaça é mitigada por procedimento manual e medida pela contagem de mensagens com contexto da IDE. O plano de assinatura impõe limites de uso que podem interromper sessões ou suspender um ciclo por dias, em momentos diferentes de cada ciclo; as interrupções são registradas e contadas. A configuração isolada não bastou, sozinha, para controlar o contexto do agente: antes da primeira sessão medida, verificou-se que o Claude Code sincronizava *skills* e *plugins* da conta do pesquisador e carregava os conectores da conta, e as três fontes foram desligadas por chaves explícitas da configuração, iguais nos dois ciclos. Durante os ciclos, o agente criou por conta própria arquivos de memória automática, carregados nas sessões seguintes; as sessões afetadas são analisadas com e sem esse contexto adicional. O Xcode foi atualizado automaticamente no fim do Ciclo A; como ele só participa da compilação do aplicativo no aparelho, fora das sessões, não se espera efeito sobre as métricas. O prefixo das intervenções é visível ao agente e pode alterar seu comportamento, também de forma simétrica. A troca do simulador pelo aparelho físico alterou as dimensões da tela de 390 × 844 para 402 × 874 pontos em relação aos quadros do protótipo, diferença registrada como desvio e aplicada igualmente aos dois ciclos.

**Ameaças da medição.** A métrica de fidelidade visual depende de um protótipo produzido no próprio projeto, de modo que a precisão das instruções usadas para gerá-lo passa a integrar o instrumento de medição (validade de construto). O avaliador baseado em modelo de linguagem pode errar de forma sistemática; o cegamento, as três execuções e a validação humana mitigam o risco, mas, com amostras de cerca de 20 itens, o intervalo de confiança do kappa é largo. As expressões regulares que detectam referências inexistentes na M6 podem não capturar referências em texto livre. As fronteiras entre fases são aproximadas, porque o agente pode, por exemplo, replanejar durante a implementação; por isso, os totais sem segmentação também são reportados. A M8 mede testes escritos pelo próprio agente, o que configura validação circular; a M8b só a mitiga se a ferramenta de mutação for validada a tempo. Como a suíte de avaliação roda apenas na versão final, perde-se a medida de regressão por uma suíte independente entre unidades, e a M13 depende da suíte do agente. Por fim, a classificação de severidade dos defeitos foi feita sem revisor externo; para reduzir o viés de reconstrução posterior, cada classificação é registrada no momento da intervenção e validada por amostra.

**Ameaças da execução.** O atraso acumulado no Ciclo A levou a um prazo mais curto para o Ciclo B. O tempo ativo, que é o que se mede, não depende do calendário, mas um ritmo mais intenso no segundo ciclo pode aumentar a chance de erros de execução do pesquisador. A regra de encerramento antecipado de unidades, introduzida durante o Ciclo A, depende de um limiar de abandono discricionário, aplicado igualmente aos dois ciclos. Os erros de execução registrados, como prefixos colados em vez de digitados ou respostas com texto diferente do fixado, são tratados por análise de sensibilidade, e nenhum dado bruto é corrigido manualmente. Por fim, uma vez, durante o Ciclo B, valores de tempo, de *tokens* e de custo de duas sessões foram exibidos ao pesquisador por erro do assistente que o apoiava na operação; a exposição foi registrada como desvio, e as regras de parada não dependem desses valores.

**Limites de generalização.** Os resultados se referem a um aplicativo, uma pilha técnica (Flutter em iOS), um agente (Claude Code com Claude Sonnet 5) e versões específicas das duas metodologias, todas sujeitas a mudanças frequentes. Eles caracterizam o comportamento dessas versões neste caso e servem como evidência empírica inicial para uma comparação que, até aqui, foi feita apenas no plano documental (Macedo, 2026).

# **4 RESULTADOS**

## **4.1 Execução dos ciclos**

Os dois ciclos foram executados na ordem prevista (seção 3.3.4): o Ciclo A, com o GitHub Spec Kit 1.0.10, de 7 a 25 de outubro de 2026, e o Ciclo B, com o BMAD-METHOD 6.11.0, de 25 de outubro a 8 de novembro de 2026. Em ambos, o agente foi o Claude Code, versão 2.1.282, com o modelo Claude Sonnet 5, e o aplicativo rodou em um iPhone. O modelo e a versão da ferramenta registrados foram os mesmos em todas as sessões que informam esses campos, e as mensagens com contexto da IDE foram nenhuma no Ciclo A e duas no Ciclo B (D-056). Ao todo, foram medidas 274 sessões de desenvolvimento, 138 no Ciclo A e 136 no Ciclo B.

A Tabela 1 resume o fechamento das unidades. No Ciclo A, dez das onze unidades foram concluídas, e a RF04 foi fechada como incompleta por decisão do pesquisador, porque um critério de aceite continuava falhando (D-026). No Ciclo B, a RF03 foi fechada como incompleta por um critério que dependia de uma lacuna de arquitetura entre o cofre e a sessão (D-061); as outras dez unidades foram concluídas, e a RF02, sem sessões próprias, porque o planejamento antecipado alocou suas funções à RF01.

Tabela 1 – Fechamento das unidades nos dois ciclos (datas de 2026, horário de Brasília)

  

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| \*\*Unidade\*\* | \*\*Requisito\*\* | \*\*Ciclo A\*\* | \*\*Ciclo B\*\* |
| F000 | Fundação do projeto | 11/10, concluída | 03/11, concluída, acima do teto |
| RF03 | Cofre de acesso | 12/10, concluída | 04/11, incompleta, acima do teto |
| RF01 | Captura multimodal | 13/10, concluída | 04/11, concluída, acima do teto |
| RF02 | Transcrição e OCR | 17/10, concluída | 04/11, concluída, sem sessões próprias |
| RF07 | Linha do tempo | 17/10, concluída | 05/11, concluída |
| RF06 | Busca semântica | 19/10, concluída | 05/11, concluída |
| RF04 | Conversa com memória | 20/10, incompleta | 06/11, concluída |
| RF10 | Salvar mensagem como entrada | 22/10, concluída | 06/11, concluída |
| RF08 | Sugestões proativas | 24/10, concluída | 06/11, concluída |
| RF05 | Exportação em PDF | 24/10, concluída | 07/11, concluída, acima do teto |
| RF09 | Painel de resumos | 25/10, concluída | 08/11, concluída, acima do teto |

Fonte: elaborado pelo autor (2026), a partir das tags dos repositórios dos ciclos (dados/cicloA/tags.csv e dados/cicloB/tags.csv). Teto de tempo ativo: 8 horas por unidade, 12 horas na F000.

Algumas ocorrências da execução afetam a interpretação dos resultados e são declaradas aqui; o registro completo está no Apêndice F. Primeiro, cinco unidades do Ciclo B (F000, RF03, RF01, RF05 e RF09) atingiram o teto de tempo e prosseguiram por decisão do pesquisador, em vez de serem encerradas como censuradas, como previa a seção 3.3.4 (D-058, D-060, D-064, D-080 e D-090); a análise principal trata o estado no teto como valor censurado, e a continuação, como sensibilidade. Segundo, a regra de encerramento antecipado, não prevista no protocolo congelado, foi criada durante o Ciclo A e vale para os dois ciclos (D-026). Terceiro, a RF02 do Ciclo B não teve sessões próprias, pois o planejamento antecipado a incorporou à RF01. Quarto, as oito retrospectivas do BMAD-METHOD foram rodadas ao fim do ciclo, em duas sessões (D-092 e D-093). Quinto, oito sessões medidas ficaram sem coleta, duas no Ciclo A e seis no Ciclo B (D-037 e D-094), e suas intervenções ficam fora da leitura principal da M5. Sexto, por decisão registrada em 8 de novembro de 2026, a análise de produto e a validação do avaliador não foram realizadas (D-097; seções 4.5 a 4.7). Nenhum dado bruto foi alterado em nenhum desses casos: as tabelas derivam dos transcritos das sessões.

## **4.2 Ciclo A: GitHub Spec Kit**

O Ciclo A seguiu a sequência de comandos do Spec Kit em cada unidade, com uma sessão por comando e com a ordem do checklist ajustada (D-016). A instalação e a constituição do projeto levaram 0,11 hora de tempo ativo, mas o calendário da preparação se estendeu de 7 a 11 de outubro, porque as conferências de largada encontraram skills, plugins e conectores da conta do pesquisador no contexto do agente e levaram a três reconfigurações, iguais para os dois ciclos (D-009, D-012 e D-013; Apêndice G).

As onze unidades somaram 138 sessões e 25,8 horas de tempo ativo, entre 11 e 25 de outubro. A fundação levou 16 sessões e 3,2 horas, e as unidades seguintes, de 1,5 a 2,9 horas, exceto a RF04, que usou 28 sessões e 5,1 horas e foi a única fechada como incompleta. Na RF04 (conversa com memória e resposta em fluxo), um critério de aceite exigia que, se o fluxo caísse no meio da resposta, a mensagem parcial continuasse visível com indicação de falha, e o critério continuou falhando depois de sessões de correção. O pesquisador decidiu então parar de corrigir e fechar a unidade, o que criou a categoria de encerramento antecipado, depois estendida ao Ciclo B (D-026). Os demais itens da verificação manual da RF04 passaram.

O pesquisador interveio 49 vezes, 45 delas durante a implementação; foram 40 correções, todas por desvio de decisão de produto ou de especificação, e 9 esclarecimentos. As intervenções se concentraram na RF04 (13), na RF09 (7), na F000 (5) e na RF06 (5). Foram registradas 67 respostas a pausas previstas, 35 delas na fase de validação. Duas sessões medidas ficaram sem coleta (D-037), e uma sessão de correção foi aberta fora da configuração do ciclo e não é medida (D-032). A memória automática criada pelo agente em uma sessão medida foi carregada nas seguintes (D-033), e as sessões afetadas são analisadas com e sem esse contexto.

O Ciclo A terminou em 25 de outubro de 2026 (tag cicloA/final), com 138 sessões, 25,9 horas de tempo ativo e custo equivalente de US$ 271,21.

## **4.3 Ciclo B: BMAD-METHOD**

O Ciclo B começou em 25 de outubro de 2026. A instalação por parâmetros e a sessão de contexto do projeto levaram 0,14 hora de tempo ativo, e a preparação foi concluída no mesmo dia. O planejamento global, entre 25 e 26 de outubro, ocupou 11 sessões e 5,4 horas de tempo ativo, muito abaixo do limite de 32 horas previsto, e produziu 31 arquivos: brainstorming, refinamento de ideia, pesquisa, perguntas frequentes (PRFAQ), product brief, requisitos de produto com seus relatórios de validação, especificação de experiência do usuário, arquitetura, épicos e o status da sprint (Tabela 4). A tag cicloB/plan-done foi criada em 26 de outubro.

As onze unidades ocuparam 122 sessões e 75,1 horas de tempo ativo, entre 27 de outubro e 8 de novembro. Cada história foi detalhada e implementada em uma sessão de construção (bmad-build), com a revisão de código e os testes de ponta a ponta em sessões separadas; o ciclo produziu 34 histórias em 8 épicos. A fundação usou 21 sessões e 12,0 horas e passou do teto de 12 horas durante a revisão da história 1.6 (D-058); o pesquisador continuou apenas para fechar a verificação manual, que havia falhado no aparelho por uma versão mínima do iOS exigida por um pacote da pilha fixa.

Quatro outras unidades terminaram acima do teto de 8 horas: RF03 (8,4 horas; D-060), RF01 (11,2 horas; D-064), RF05 (11,2 horas; D-080) e RF09 (8,7 horas; D-090). A RF03 foi fechada como incompleta porque o link “usar e-mail e senha” da tela de biometria continuou ausente, por causa de uma lacuna de arquitetura entre o cofre e a sessão que nenhuma história cobria (D-061). A RF01 absorveu as funções da RF02, que não teve sessões próprias (nota B7), o que explica parte do seu tempo. As outras cinco unidades (RF07, RF06, RF04, RF10 e RF08) ficaram dentro do teto, com 2,5 a 6,8 horas.

O pesquisador interveio 16 vezes (15 nas unidades e uma no planejamento), em 14 correções e 2 esclarecimentos, e respondeu 279 vezes a pausas previstas pelo processo, 147 delas na validação. Das dez unidades com sessões, sete tiveram no máximo uma intervenção, e a RF04, com sete, concentrou quase metade do total.

O Ciclo B concentrou o maior número de desvios de execução do pesquisador, 56 apenas desse ciclo (Apêndice F), em geral respostas com texto diferente do fixado a pausas de revisão. Seis sessões ficaram sem coleta e foram identificadas na conferência de completude (D-094). As oito retrospectivas de épico foram rodadas ao fim do ciclo, em duas sessões, e não ao fim de cada épico (D-092 e D-093); como o método as prevê para informar os épicos seguintes, sua função ficou prejudicada, e seu custo (2,0 horas e US$ 32,36) foi contabilizado à parte, fora das unidades. Em uma ocasião, valores de tempo e de custo de duas sessões foram exibidos ao pesquisador por erro do assistente de apoio à operação (D-045). O ciclo terminou em 8 de novembro de 2026 (tag cicloB/final), com 136 sessões, 82,7 horas de tempo ativo e custo equivalente de US$ 901,86.

## **4.4 Métricas de processo**

Esta seção apresenta as métricas de processo dos dois ciclos, calculadas a partir dos transcritos brutos de 274 sessões medidas (138 no Ciclo A e 136 no Ciclo B). O tempo ativo (M2) segue a regra do protocolo: intervalos que terminam em uma ação do agente contam por inteiro, e as esperas pelo pesquisador contam até 30 minutos cada, com o excedente registrado como pausa. Os tokens (M3) somam o agente principal e os subagentes, e o custo usa a tabela de preços congelada. A M5 conta as intervenções reconhecidas, sem as das sessões que ficaram sem coleta, e a M5b conta as respostas a pausas previstas pela própria metodologia. As tabelas foram geradas por programa a partir das tabelas re-derivadas dos transcritos (D-096), e os totais por ciclo conferem com a soma das unidades. A Tabela 2 resume os dois ciclos.

Tabela 2 – Métricas de processo por ciclo

  

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| \*\*Métrica\*\* | \*\*Ciclo A\*\* | \*\*Ciclo B\*\* | \*\*B/A\*\* |
| M1 – preparação, tempo ativo (h) | 0,11 | 0,14 | 1,3 |
| M1 – calendário, da instalação ao fim da preparação (h) | 101,0 | 3,1 | — |
| M2 – tempo ativo total (h) | 25,9 | 82,7 | 3,2 |
| M2 – tempo ativo nas onze unidades (h) | 25,8 | 75,1 | 2,9 |
| M2 – planejamento global (h) | — | 5,4 | — |
| M2 – retrospectivas (h) | — | 2,0 | — |
| M2 – fase de especificação (h) | 7,6 | 5,5 | 0,7 |
| M2 – fase de implementação (h) | 13,5 | 48,8 | 3,6 |
| M2 – fase de validação (h) | 4,9 | 28,4 | 5,8 |
| Pausa fora do tempo ativo (h) | 23,0 | 38,0 | 1,7 |
| Sessões medidas | 138 | 136 | 1,0 |
| M3 – tokens de saída, agente principal e subagentes | 4.899.491 | 9.124.568 | 1,9 |
| M3 – tokens totais, todas as categorias (milhões) | 814,6 | 2.979,6 | 3,7 |
| M3 – fração da entrada lida do cache | 98,0% | 97,4% | — |
| M3 – custo equivalente (US$) | 271,21 | 901,86 | 3,3 |
| M5 – intervenções, leitura principal | 49 | 16 | 0,3 |
| M5 – intervenções, leitura ampla | 66 | 51 | 0,8 |
| M5b – respostas a pausas previstas pela metodologia | 67 | 279 | 4,2 |

Fonte: elaborado pelo autor (2026), a partir de dados/processo/ciclo.csv. B/A é a razão entre o valor do Ciclo B e o do Ciclo A. A leitura ampla da M5 acrescenta as mensagens livres sem prefixo (interrupções, retomadas e outras).

Preparação (M1). O tempo de preparação foi desprezível nos dois ciclos: 0,11 hora no Spec Kit (instalação e uma sessão de constituição do projeto) e 0,14 hora no BMAD-METHOD (instalação e uma sessão de geração do contexto do projeto). O tempo de calendário entre a instalação e o fim da preparação foi, porém, de 101,0 horas no Ciclo A e de 3,1 horas no Ciclo B, porque a preparação do Ciclo A foi interrompida por reconferências do ambiente, que originaram os desvios D-009 a D-013 (seção 4.2).

Tempo (M2). O Ciclo A somou 25,9 horas de tempo ativo, das quais 25,8 nas onze unidades; o Ciclo B somou 82,7 horas, das quais 75,1 nas unidades, 5,4 no planejamento global e 2,0 nas retrospectivas. O tempo de pausa, que não conta como ativo, foi de 23,0 e 38,0 horas, respectivamente, e o tempo bruto das sessões, de 48,9 e 120,2 horas. Por fase, o Ciclo B consumiu menos tempo de especificação (5,5 horas, quase todas do planejamento global, contra 7,6 horas) e muito mais de implementação (48,8 contra 13,5 horas) e de validação (28,4 contra 4,9 horas). A Tabela 3 detalha o tempo por unidade: o Spec Kit levou de 1,5 a 5,1 horas por unidade, fora a fundação (3,2 horas); o BMAD-METHOD, de 2,5 a 11,2 horas, fora a fundação (12,0 horas), com cinco unidades acima do teto e a RF02 sem sessões.

Tokens e custo (M3). O Ciclo B processou 3,7 vezes mais tokens e custou 3,3 vezes mais: US$ 901,86 contra US$ 271,21. A composição é parecida, com cerca de 98% da entrada vinda de leitura de cache nos dois ciclos, mas a estrutura difere: o Ciclo B usou subagentes, que geraram 0,64 milhão de tokens de saída e responderam por 49% da leitura de cache do ciclo, enquanto no Ciclo A os subagentes quase não foram usados (373 tokens de saída). O custo por unidade variou de US$ 15,6 a US$ 59,5 no Ciclo A e de US$ 36,1 a US$ 123,1 no Ciclo B, fora a fundação; o planejamento global do Ciclo B custou US$ 32,15, e as retrospectivas, US$ 32,36.

Tabela 3 – Tempo ativo, custo, intervenções (M5) e respostas de processo (M5b) por unidade

  

|  |  |  |  |  |  |  |  |  |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| \*\*Unid.\*\* | \*\*Tempo A (h)\*\* | \*\*Tempo B (h)\*\* | \*\*Custo A (US$)\*\* | \*\*Custo B (US$)\*\* | \*\*M5 A\*\* | \*\*M5 B\*\* | \*\*M5b A\*\* | \*\*M5b B\*\* |
| F000 | 3,2 | 12,0† | 23,2 | 117,6 | 5 | 1 | 8 | 45 |
| RF03 | 1,5 | 8,4†‡ | 15,6 | 91,6 | 4 | 2 | 4 | 27 |
| RF01 | 2,9 | 11,2† | 28,7 | 123,1 | 4 | 4 | 7 | 34 |
| RF02 | 1,5 | — | 15,9 | — | 2 | — | 7 | — |
| RF07 | 1,5 | 5,7 | 19,2 | 81,9 | 1 | 0 | 5 | 24 |
| RF06 | 2,4 | 5,1 | 23,4 | 76,9 | 5 | 1 | 6 | 20 |
| RF04 | 5,1‡ | 6,8 | 59,5 | 93,1 | 13 | 7 | 13 | 20 |
| RF10 | 1,7 | 2,5 | 17,5 | 36,1 | 2 | 0 | 2 | 7 |
| RF08 | 1,9 | 3,4 | 19,3 | 37,5 | 4 | 0 | 2 | 5 |
| RF05 | 2,0 | 11,2† | 21,0 | 68,8 | 2 | 0 | 5 | 21 |
| RF09 | 2,1 | 8,7† | 27,4 | 110,0 | 7 | 0 | 8 | 32 |
| Total | 25,8 | 75,1 | 270,8 | 836,6 | 49 | 15 | 67 | 235 |

Fonte: elaborado pelo autor (2026), a partir de dados/processo/rf.csv. † Unidade acima do teto de tempo (8 horas; 12 na F000), continuada pelo Ciclo B por decisão do pesquisador (D-058, D-060, D-064, D-080 e D-090). ‡ Fechada como incompleta (D-026 e D-061). A RF02 do Ciclo B não teve sessões (nota B7). Os totais de M5 e M5b do Ciclo B na Tabela 2 incluem ainda 1 intervenção e 44 respostas de processo do setup, do planejamento global e das retrospectivas.

Intervenções e respostas de processo (M5 e M5b). Na leitura principal, o Ciclo A teve 49 intervenções e o Ciclo B, 16. No Ciclo A, 40 foram correções e 9, esclarecimentos não solicitados; entre as correções, 7 de severidade cosmética (S1), 27 funcionais com contorno (S2) e 6 bloqueantes (S3); 45 intervenções ocorreram na implementação, 3 na validação e 1 na especificação. No Ciclo B, foram 14 correções (nenhuma S1, 11 S2 e 3 S3) e 2 esclarecimentos, 15 na implementação e 1 no planejamento. Pela causa, 40 das 49 intervenções do Ciclo A e 11 das 16 do Ciclo B foram desvios de decisão de produto ou de especificação; as outras três correções do Ciclo B foram uma falha de checagem e duas implementações incompletas, e nenhuma intervenção, em nenhum dos ciclos, decorreu de incompatibilidade com o repositório (causa de contexto). A leitura ampla, que acrescenta interrupções, retomadas e outras mensagens livres sem prefixo, eleva os totais para 66 e 51 e reduz a diferença entre os ciclos; no Ciclo B, 16 interrupções por Esc, 9 retomadas e 9 outras mensagens livres entram nessa leitura, e muitas decorrem de erros de execução do pesquisador declarados no Apêndice F. As respostas a pausas previstas pela metodologia (M5b) foram 67 no Ciclo A e 279 no Ciclo B, 147 delas em fase de validação.

Tabela 4 – Artefatos de especificação e planejamento (M4) por tipo

  

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| \*\*Ciclo\*\* | \*\*Tipo de artefato\*\* | \*\*Fim do planejamento\*\* | \*\*Tag final\*\* |
| A | Constituição do projeto | — | 1 |
| A | Especificações (spec) | — | 11 |
| A | Planos (plan) | — | 11 |
| A | Listas de tarefas (tasks) | — | 11 |
| A | Pesquisa, modelo de dados e quickstart | — | 33 |
| A | Contratos | — | 39 |
| A | Listas de verificação (checklists) | — | 22 |
| A | Total | — | 128 |
| B | Brainstorming | 1 | 1 |
| B | Refinamento de ideia | 2 | 2 |
| B | Pesquisa | 5 | 5 |
| B | PRFAQ | 2 | 2 |
| B | Product brief | 2 | 2 |
| B | Requisitos de produto (PRD) | 6 | 6 |
| B | Relatórios de validação do PRD | 2 | 2 |
| B | Experiência do usuário | 2 | 2 |
| B | Arquitetura | 7 | 7 |
| B | Épicos | 1 | 9 |
| B | Histórias | 0 | 34 |
| B | Status da sprint | 1 | 1 |
| B | Retrospectivas | 0 | 8 |
| B | Outros da implementação | 0 | 2 |
| B | Total | 31 | 83 |

Fonte: elaborado pelo autor (2026), a partir de dados/processo/m4.csv. O Ciclo A não tem planejamento global. No Ciclo B, os arquivos de memória do agente (.memlog.md) ficam fora da contagem.

Artefatos (M4). Na tag final, o Ciclo A tinha 128 arquivos de especificação: uma constituição e, por unidade, uma especificação, um plano e uma lista de tarefas (11 de cada), além de documentos de pesquisa, modelo de dados e quickstart (33), contratos (39) e listas de verificação (22). O Ciclo B tinha 83 arquivos em \_bmad-output: 31 ao fim do planejamento global (entre eles 6 de requisitos de produto, 7 de arquitetura, 5 de pesquisa e 2 de experiência do usuário) e, ao longo das unidades, 34 histórias, 8 retrospectivas, 8 arquivos de épicos e 2 outros (Tabela 4). A M4 mede volume, e não qualidade: o BMAD-METHOD gera mais tipos de artefato por construção, e o Spec Kit gera mais arquivos por unidade.

Quatro ressalvas acompanham esses números. A primeira é que o tempo ativo conta até 30 minutos de espera do pesquisador por pausa; como o BMAD-METHOD prevê mais pausas, parte da diferença de tempo é estrutural ao processo. A segunda é que a topologia de agentes afeta o custo, de modo que o custo em tokens não é comparável como eficiência sem essa ressalva. A terceira é que o Ciclo B teve mais erros de execução do pesquisador, todos declarados (Apêndice F), e as mensagens livres entram apenas na sensibilidade. A quarta é que as diferenças absolutas não indicam qual ciclo é melhor ou pior, porque o produto entregue não foi avaliado (seção 4.5).

## **4.5 Métricas de produto**

As métricas de produto (M6 a M13) dependem do conjunto de avaliação do estudo, descrito na seção 3.6: ferramentas de análise estática, a suíte de caixa-preta executada em aparelho contra um backend instrumentado, o avaliador baseado em modelo de linguagem e as rubricas. O protocolo determina que esse conjunto seja construído e congelado, com hashes registrados, antes de qualquer uso sobre os repositórios finais dos dois ciclos, para que nenhuma escolha de medição seja influenciada pelo resultado que ela produziria (seção 3.6.5). Na data de entrega deste trabalho, o conjunto estava em construção e não havia sido congelado. A regra de cegamento foi mantida: nenhuma métrica de produto foi calculada, e os repositórios finais não foram inspecionados com esse propósito. Os desvios D-095 e D-097 registram a decisão, tomada em 8 de novembro de 2026, de reduzir a Parte IV do estudo às métricas que não dependem do conjunto de avaliação. O Quadro 19 lista o que ficou de fora e o que cada item ainda exige.

Quadro 19 – Métricas e análises não avaliadas nesta versão do estudo

  

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| \*\*Métricas\*\* | \*\*Questão\*\* | \*\*Depende de\*\* | \*\*E\*\*stado na data de entrega |
| M6, M14 | QP2 | Plano de cada unidade, seleção pré-registrada de dez decisões técnicas, avaliador baseado em modelo de linguagem e suas rubricas | Avaliador e rubricas não validados nem congelados. |
| M7, M8, M8b, M10, M12 | QP3 | Ferramentas de análise estática, de cobertura e de mutação, rodadas sobre as tags finais | Em construção, testadas apenas contra um repositório sintético de calibração; não congeladas. A M8b depende ainda de a ferramenta de mutação ser validada. |
| M9 | QP3 | Medidas do protótipo (cor, tipografia e espaçamento) e capturas de tela dos dois aplicativos, com avaliador | Medição do protótipo em construção; avaliador não validado. |
| M11 | QP3 | Suíte de caixa-preta executada em aparelho contra um backend instrumentado | Suíte em construção e não congelada; a execução está prevista só sobre as versões finais, depois do congelamento. |
| M13, M15 | QP4 | Execução da suíte do agente em cada tag de unidade; verificação de quatro convenções em cada funcionalidade | Não executadas; dependem do conjunto de avaliação congelado. |
| Validação do avaliador | — | Amostras de itens julgadas por humano e comparadas com o avaliador por meio do kappa | Não realizada. |

Fonte: elaborado pelo autor (2026), a partir do registro de desvios (D-095 e D-097).

Nenhum número de produto deve ser inferido das métricas de processo da seção 4.4. Os repositórios finais dos dois ciclos (tags cicloA/final e cicloB/final), o protocolo congelado e o conjunto de avaliação, quando concluído e congelado, permitem completar esta seção sem alterar o que foi medido até aqui.

## **4.6 Métricas diferenciais**

A M14 (fidelidade de handoff) e a M15 (consistência de padrões) são as métricas diferenciais, desenhadas para captar a transmissão de decisões entre fases (QP2 e QP4). A M14 exige selecionar, nos artefatos de planejamento de cada metodologia, dez decisões técnicas por um critério pré-registrado e verificar no código final se estão implementadas; a M15 verifica quatro convenções, tomando a RF01 como referência, em cada funcionalidade. As duas exigem o conjunto de avaliação congelado e, no caso da M14, o avaliador; por isso, não foram calculadas, pelos motivos expostos na seção 4.5. A única evidência de processo relacionada à transmissão de decisões é a causa registrada das intervenções do pesquisador, discutida na seção 5.3.

## **4.7 Validação do avaliador**

O avaliador baseado em modelo de linguagem só pode ser usado depois de validado contra julgamentos humanos em amostras pré-definidas, com a concordância medida pelo kappa (seção 3.6.4). Como o avaliador e as rubricas ainda não estavam congelados, essa validação não foi realizada, e nenhum resultado produzido pelo avaliador consta deste trabalho. O intervalo de confiança do kappa, que já se esperava largo por causa do tamanho das amostras (seção 3.9), só poderá ser reportado quando a validação for feita.

## **4.8 Análise pareada por requisito**

A análise pareada usa o requisito funcional como unidade, como previsto na seção 3.8, com três ajustes que a execução tornou necessários (D-098). Primeiro, a RF02 do Ciclo B não teve sessões próprias, porque o planejamento antecipado alocou a transcrição e o reconhecimento de texto em imagem a histórias da RF01; o par da RF01 soma, portanto, as unidades RF01 e RF02 do Ciclo A e as compara com a RF01 do Ciclo B, o que resulta em nove pares, e não dez. Segundo, o tempo do par principal é o das fases de implementação e de validação (IMPL e VALID); como no BMAD-METHOD o detalhamento da história ocorre dentro do laço de construção, o tempo da unidade inteira também é testado. Terceiro, a censura por limite de tempo só está definida para o tempo, e só nele o valor das unidades que passaram do teto é substituído pelo valor do teto (8 horas); as demais métricas usam os valores observados, com sensibilidade sem os quatro pares em que o Ciclo B passou do teto (RF03, RF01, RF05 e RF09). A fundação e a preparação ficam fora do pareamento. A Tabela 5 apresenta os valores por par.

Tabela 5 – Tempo de implementação e validação, custo e intervenções por par de requisitos

  

|  |  |  |  |  |  |  |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| \*\*Par\*\* | \*\*IMPL+VALID A (h)\*\* | \*\*IMPL+VALID B (h)\*\* | \*\*Custo A (US$)\*\* | \*\*Custo B (US$)\*\* | \*\*M5 A\*\* | \*\*M5 B\*\* |
| RF03 | 1,0 | 8,0\\\* (obs. 8,4) | 15,6 | 91,6 | 4 | 2 |
| RF01+RF02 | 3,1 | 8,0\\\* (obs. 11,2) | 44,6 | 123,1 | 6 | 4 |
| RF07 | 0,9 | 5,7 | 19,2 | 81,9 | 1 | 0 |
| RF06 | 1,4 | 5,1 | 23,4 | 76,9 | 5 | 1 |
| RF04 | 4,0 | 6,8 | 59,5 | 93,1 | 13 | 7 |
| RF10 | 1,0 | 2,5 | 17,5 | 36,1 | 2 | 0 |
| RF08 | 1,3 | 3,4 | 19,3 | 37,5 | 4 | 0 |
| RF05 | 1,5 | 8,0\\\* (obs. 11,2) | 21,0 | 68,8 | 2 | 0 |
| RF09 | 1,5 | 8,0\\\* (obs. 8,7) | 27,4 | 110,0 | 7 | 0 |
| Mediana | 1,4 | 6,8 | 21,0 | 81,9 | 4 | 0 |

Fonte: elaborado pelo autor (2026), a partir de dados/processo/rf.csv e dados/processo/pareado\_pares.csv. \* Valor do teto de 8 horas, nas unidades que o Ciclo B continuou além dele; entre parênteses, o valor observado. A RF04 do Ciclo A e a RF03 do Ciclo B foram fechadas como incompletas.

A Tabela 6 apresenta os testes. Em todos os nove pares, o BMAD-METHOD consumiu mais tempo de implementação e validação do que o Spec Kit; a mediana das diferenças foi de 4,9 horas (medianas de 1,4 hora no Spec Kit e de 6,8 horas no BMAD-METHOD), com soma de postos positivos igual a 45 e nenhum posto negativo, p exato bilateral de 0,0039 e correlação bisserial de postos de 1,0. Com nove pares sem empates, 0,0039 é o menor valor de p que o teste pode produzir, de modo que o p indica apenas que a direção da diferença é a mesma em todos os pares, e não mede a sua grandeza. Sem os quatro pares censurados, restam cinco pares, e o menor p possível passa a ser 0,0625: a direção continua a mesma nos cinco, mas o teste não pode, por construção, alcançar o nível de 0,05. A análise com os valores observados, que incluem a continuação além do teto, e a do tempo da unidade inteira produzem o mesmo resultado. A fase de especificação, comparada no nível do ciclo, somou 7,6 horas no Ciclo A e 5,5 horas no Ciclo B.

Tabela 6 – Testes de Wilcoxon por par de requisitos (diferença B menos A)

  

|  |  |  |  |  |  |  |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| \*\*Métrica e tratamento\*\* | \*\*n\*\* | \*\*Mediana A\*\* | \*\*Mediana B\*\* | \*\*B \\\> A\*\* | \*\*p exato\*\* | \*\*r\*\* |
| IMPL+VALID (h), censura no teto (principal) | 9 | 1,41 | 6,84 | 9 | 0,0039 | 1,00 |
| IMPL+VALID (h), sem os pares censurados | 5 | 1,31 | 5,10 | 5 | 0,0625 | 1,00 |
| IMPL+VALID (h), valores observados | 9 | 1,41 | 6,84 | 9 | 0,0039 | 1,00 |
| Unidade inteira (h), censura no teto | 9 | 2,05 | 6,84 | 9 | 0,0039 | 1,00 |
| Unidade inteira (h), valores observados | 9 | 2,05 | 6,84 | 9 | 0,0039 | 1,00 |
| Custo (US$), valores observados | 9 | 21,04 | 81,87 | 9 | 0,0039 | 1,00 |
| Custo (US$), sem os pares censurados | 5 | 19,27 | 76,90 | 5 | 0,0625 | 1,00 |
| Tokens de saída, valores observados | 9 | 377.780 | 750.109 | 7 | 0,0547 | 0,73 |
| M5 intervenções, valores observados | 9 | 4 | 0 | 0 | 0,0039 | \\-1,00 |
| M5 intervenções, sem os pares censurados | 5 | 4 | 0 | 0 | 0,0625 | \\-1,00 |
| M5b respostas de processo, valores observados | 9 | 5 | 21 | 9 | 0,0039 | 1,00 |

Fonte: elaborado pelo autor (2026), a partir de dados/processo/pareado\_testes.csv. Teste de postos sinalizados de Wilcoxon, p exato bilateral por permutação dos sinais, diferenças nulas pelo método de Pratt; B \> A é o número de pares em que o Ciclo B é maior; r é a correlação bisserial de postos.

O custo por unidade tem o mesmo padrão do tempo: maior no BMAD-METHOD em nove dos nove pares, com mediana de US$ 21,04 contra US$ 81,87 e p exato de 0,0039. Os tokens de saída foram maiores no BMAD-METHOD em sete dos nove pares (p exato de 0,0547; correlação bisserial de 0,73), uma diferença menos uniforme que as de tempo e de custo. Parte da distância entre o custo e os tokens de saída vem da leitura de cache: 49% da leitura de cache do Ciclo B ocorreu em subagentes. As intervenções do pesquisador seguem a direção oposta: o Spec Kit teve mais intervenções do que o BMAD-METHOD em todos os nove pares (mediana de 4 contra 0; p exato de 0,0039; correlação de -1,0), ao passo que as respostas a pausas previstas pelo processo (M5b) foram maiores no BMAD-METHOD em todos os pares (mediana de 21 contra 5).

Esses resultados descrevem a direção e a consistência das diferenças entre os pares, e não a sua generalização. Há um único sujeito, uma ordem fixa dos ciclos e nove pares, e o tratamento das unidades que passaram do teto é uma aproximação (seção 7.3).

# **5 DISCUSSÃO**

## **5.1 Comportamento observado e notas documentais**

O Quadro 8 (seção 3.7) relaciona as métricas às dimensões da taxonomia de Macedo (2026) e às notas que o autor atribui às metodologias a partir da documentação oficial. Com as métricas de processo disponíveis, é possível confrontar a execução com cinco das seis dimensões; a portabilidade não foi medida por desenho, e a medida do efeito das demais sobre o produto depende das métricas que não foram avaliadas.

Especificação (nota 2 nos dois). Esperava-se esforço semelhante. O tempo ativo de especificação foi de 7,6 horas no Spec Kit, distribuídas pelas onze unidades, e de 5,5 horas no BMAD-METHOD, concentradas no planejamento global; os valores são do mesmo porte. O volume de artefatos (M4) difere: o Spec Kit terminou com 128 arquivos de planejamento e especificação, em grande parte contratos, documentos de pesquisa, modelo de dados e listas de verificação gerados a cada unidade, e o BMAD-METHOD com 83, dos quais 31 foram produzidos antes da implementação (documento de requisitos, arquitetura, especificação de experiência do usuário, épicos) e 34 são histórias criadas ao longo das unidades. A M4 mede volume, e não qualidade; o resultado mostra apenas que a mesma nota documental convive com formas e quantidades muito diferentes de artefato.

Execução (nota 1 nos dois). Notas iguais não produziram esforço igual: a fase de implementação consumiu 13,5 horas no Spec Kit e 48,8 horas no BMAD-METHOD, e as intervenções do pesquisador nessa fase foram 45 e 15. Parte da diferença é de contabilização, porque no BMAD-METHOD a história é detalhada e implementada no mesmo laço de construção, que inclui uma revisão embutida, ao passo que no Spec Kit a especificação de cada unidade é uma fase própria. Por isso, a comparação mais confiável é a da unidade inteira (Tabela 3).

Contexto, papéis e validação (nota 2 do BMAD-METHOD contra 1 do Spec Kit). São as dimensões em que a documentação prevê vantagem do BMAD-METHOD, e as métricas de processo as tornam visíveis no custo, ainda não no resultado. Quanto aos papéis, os subagentes geraram 0,64 milhão de tokens de saída no Ciclo B e 373 no Ciclo A, o que mostra a divisão do trabalho entre agentes especializados em uso efetivo. Quanto à validação, a fase consumiu 28,4 horas no Ciclo B contra 4,9 horas no Ciclo A, e o Ciclo B exigiu 147 respostas a pausas de validação (revisões de código e geração de testes), contra 35 do Ciclo A. Quanto ao contexto, o indicador de processo da M5, a causa de contexto, não discriminou: foi zero nos dois ciclos, e a transmissão efetiva de contexto fica para a M14.

Em conjunto, as diferenças documentais de contexto, papéis e validação aparecem no comportamento observado como mais planejamento, mais agentes e mais etapas de validação, com maior consumo de tempo e de tokens e menor número de correções pelo pesquisador. Se essas etapas também se traduzem em melhor arquitetura, cobertura de testes e aderência aos critérios de aceite, é o que as métricas de produto devem dizer, e é a parte que esta versão não responde.

## **5.2 Produtividade e confiabilidade**

Farrag (2026) alerta que ganhos de velocidade na produção de código convivem com problemas que só aparecem depois e, por isso, o plano de análise (seção 3.8) exige ler reduções de tempo ao lado das métricas de confiabilidade (M6, M11, M13 e M14). Os dados desta versão contêm apenas o lado da produtividade. Nele, o Spec Kit é mais rápido e mais barato em todos os nove pares de requisitos: o tempo mediano por requisito foi de 2,0 horas, contra 6,8 horas no BMAD-METHOD, e o custo mediano foi de US$ 21,04, contra US$ 81,87 (Tabela 5).

O lado da confiabilidade só pode ser lido por indícios do processo. As intervenções do pesquisador, que registram o que o produto errou a ponto de exigir correção, foram menos frequentes no BMAD-METHOD em todos os nove pares (mediana de 0 contra 4 por requisito; p exato de 0,004) e menos graves: na leitura principal, 3 intervenções bloqueantes (S3) e nenhuma cosmética (S1), contra 6 bloqueantes e 7 cosméticas no Spec Kit. Isso inverte a direção da diferença de custo, mas não equivale a uma medida de confiabilidade. As intervenções registram o que o pesquisador percebeu na verificação manual, que é a mesma nos dois ciclos, e não os defeitos que passaram despercebidos, que as métricas de produto deveriam capturar.

Há ainda dois cuidados de leitura. O primeiro é que parte do custo do BMAD-METHOD é estrutural: o tempo ativo conta até 30 minutos de espera por pausa, e o BMAD-METHOD prevê muito mais pausas (279 respostas de processo, contra 67), de modo que sua diferença em tempo ativo contém tempo de espera que a metodologia exige. O segundo é a topologia do processo: um fluxo com agentes especializados e etapas de revisão consome mais tokens por construção. Os dois cuidados reduzem o peso da comparação como medida de eficiência, mas não mudam a direção da diferença de tempo e de custo, que é a mesma em todos os pares.

## **5.3 Perda de contexto e fidelidade de** ***handoff***

A perda de contexto entre fases é o assunto das questões QP2 e QP4 e das métricas M14 e M15. Como elas não foram avaliadas, esta seção se limita ao que o processo registrou.

Os dois ciclos transmitiram contexto entre fases apenas por artefatos (seção 3.3.2): cada comando do Spec Kit e cada fluxo do BMAD-METHOD rodaram em sessão nova. O Spec Kit repetiu o ciclo de artefatos em cada uma das onze unidades, com planejamento incremental; o BMAD-METHOD produziu seus artefatos de contexto uma vez, antes da implementação, e depois os consultou unidade a unidade. A M5 não registrou nenhuma intervenção por incompatibilidade com o repositório ou com o backend congelado (causa de contexto, a chamada cegueira de contexto) em nenhum dos ciclos, o que indica que, na verificação do pesquisador, nenhuma das duas formas de transmissão produziu falhas evidentes desse tipo.

O indício de processo mais próximo da fidelidade de handoff é a causa de desvio de decisão de produto ou de especificação, que ocorre quando o agente ignora um requisito ou contraria uma decisão registrada. Ela explica 40 das 49 intervenções do Ciclo A e 11 das 16 do Ciclo B. A diferença é compatível com uma transmissão mais fiel das decisões no Ciclo B, em que o protótipo e o pacote de entrada foram incorporados aos documentos de requisitos, de experiência do usuário e de arquitetura antes da implementação. Mas a mesma diferença pode refletir a dificuldade de o agente reproduzir o protótipo no Ciclo A, em que a verificação visual foi a principal fonte de correções, e a M5 não separa as duas explicações. Só a M14 e a avaliação de fidelidade visual, ainda por fazer, separam.

## **5.4 Lições sobre o próprio instrumento**

A execução expôs, além dos resultados, características do instrumento que importam para quem quiser replicar o protocolo.

A primeira diz respeito à coleta. A coleta por sessão, feita por um comando do pesquisador ao fim de cada sessão, produziu lacunas e duplicações (sessões interrompidas, coletas prematuras ou repetidas e oito sessões sem coleta, parte dos 20 desvios do grupo de sessões no Apêndice F) e revelou limites do próprio coletor, como uma coluna de limite de uso que não era confiável e mensagens com contexto da IDE que não eram reconhecidas. A saída adotada foi manter o transcrito bruto como fonte única e re-derivar dele todas as tabelas por um programa testado (D-096). Para uma replicação, a lição é coletar o transcrito bruto e derivar as métricas depois, em vez de depender de uma coleta ao vivo.

A segunda diz respeito ao roteiro de respostas. A política de respostas fixas é o que garante simetria entre os ciclos, mas exige do operador humano uma disciplina de formato ao longo de centenas de pausas: o Ciclo B teve 279 respostas de processo, e 31 dos 98 desvios registrados são respostas com texto diferente do fixado. O erro é previsível quando o volume cresce, e o instrumento o tratou por sensibilidade, mas um roteiro com menos formatos, ou a resposta padrão automatizada, reduziria o risco.

A terceira diz respeito à regra de limite de tempo. A regra de censura no teto não foi seguida em cinco unidades do Ciclo B, porque encerrar a unidade antes de o pesquisador verificar o aplicativo no aparelho deixaria a funcionalidade sem desfecho. Uma replicação deve prever a continuação além do teto como categoria própria, com o estado no teto registrado no momento em que ele é atingido, e não reconstruído depois.

A quarta diz respeito à ordem dos portões do protocolo. O cegamento exige que o conjunto de avaliação de produto seja congelado antes de seu primeiro uso sobre os repositórios finais. Com um único pesquisador e prazo fixo, isso concentrou o trabalho de avaliação ao fim dos ciclos, e a avaliação de produto foi a parte que não coube no prazo. A lição é planejar a construção do conjunto de avaliação em paralelo aos ciclos, sobre materiais que não dependam dos produtos finais, para que o congelamento ocorra logo após o Ciclo B.

Por fim, o registro de desvios mostrou-se parte do instrumento. Ao anotar cada ocorrência com a data, o efeito esperado nas métricas e o tratamento previsto, ele permitiu separar o dado bruto, que não foi alterado, das leituras de sensibilidade, e deu ao leitor os meios de avaliar o peso de cada falha de execução.

# **6 AVALIAÇÃO DE IMPACTOS**

## **6.1 Impacto social**

O impacto social do trabalho decorre mais de seu tema do que de seu produto. Os agentes de codificação estão mudando a forma como o software é produzido e o papel de quem o produz: o desenvolvedor deixa de ser programador e passa a especificador, que redige especificações, avalia as soluções propostas pelos agentes e os orienta (Hassan et al., 2025). Nesse cenário, a forma de organizar o trabalho do agente afeta a qualidade do software que chega às pessoas, a carga de revisão que recai sobre os desenvolvedores e a capacidade de equipes pequenas de construir produtos que antes exigiriam equipes maiores. Uma comparação aberta, com protocolo, instrumento e registro de desvios disponíveis, contribui para que essa escolha seja feita com base em evidência, e não apenas no material de divulgação das ferramentas.

Há também um efeito sobre a formação de engenheiros. Metodologias que tornam explícitos os requisitos, os critérios de aceite e as decisões de arquitetura deixam visível o raciocínio de engenharia que um agente conduzido apenas por conversa tende a esconder. Ao medir quanto desse raciocínio chega ao código, o estudo ajuda a avaliar se essas metodologias podem servir também como apoio ao ensino de engenharia de requisitos e de arquitetura de software, em um momento em que parte do trabalho de programação passa a ser delegada a agentes.

Quanto ao produto, o Cerne lida com dados pessoais sensíveis, os registros de um diário. Embora o aplicativo seja aqui um veículo experimental, sem usuários reais, seu desenho incorporou cuidados de privacidade alinhados aos princípios da Lei Geral de Proteção de Dados Pessoais (Brasil, 2018): detecção e anotação de dados pessoais identificáveis, isolamento por linha no banco de dados, exclusão completa da conta, transcrição de áudio no próprio aparelho e nenhuma imagem armazenada (Apêndice A). O estudo não envolveu participantes humanos além do próprio pesquisador, e todos os dados usados nos testes são fictícios. Um uso real do Cerne exigiria, além disso, cuidados que este trabalho deliberadamente não tratou, como a detecção de situações de risco nas conversas, presente em sistemas de pesquisa da mesma categoria (Kim et al., 2024).

## **6.2 Impacto econômico**

Do ponto de vista econômico, a adoção de uma metodologia de desenvolvimento orientado por especificação envolve um custo fixo de preparação e um custo recorrente por funcionalidade. O primeiro compreende a instalação da ferramenta e a produção dos artefatos iniciais, como a constituição do projeto no Spec Kit ou o planejamento global no BMAD-METHOD; o segundo compreende o tempo do desenvolvedor, o consumo de tokens do agente, as intervenções humanas e o retrabalho de correção. Farrag (2026) propõe tratar esses componentes em conjunto, em um custo total que soma tokens, tempo de autoria das especificações, esforço de verificação e retrabalho, e lembra, com base na economia dos custos de transação, que o uso frequente amortiza os custos fixos de estabelecer a governança e torna economicamente racional um investimento inicial maior. Por isso, a métrica de preparação (M1) é interpretada ao lado do custo recorrente por requisito (M2 e M3).

Dois fatores limitam a leitura dos valores em dólares. O primeiro é a queda acelerada do preço por token, superior a 90% em cerca de três anos, que não implica queda do gasto total, porque fluxos agênticos consomem muito mais tokens por tarefa, e equipes de agentes que trabalham em paralelo podem consumir várias vezes mais do que sessões convencionais (Farrag, 2026). O segundo é a forma de cobrança: os dois ciclos usaram o mesmo plano de assinatura, de custo fixo mensal para o pesquisador, e os valores em dólares são equivalentes calculados por uma tabela de preços congelada no protocolo. O custo em dólares é, portanto, datado; o custo em tokens e em tempo, não.

Os resultados de custo mostram um contraste de ordem de grandeza entre os ciclos. O custo recorrente total (M3), calculado pela tabela de preços congelada, foi de US$ 271,21 no Ciclo A e de US$ 901,86 no Ciclo B, 3,3 vezes maior (Tabela 2). No Ciclo B, US$ 836,55 correspondem às onze unidades, US$ 32,15 ao planejamento global, US$ 32,36 às retrospectivas, rodadas ao fim do ciclo, e US$ 0,80 ao setup. O custo fixo de preparação (M1) foi desprezível nos dois ciclos: 0,11 hora de tempo ativo no Spec Kit e 0,14 hora no BMAD-METHOD. O planejamento global do Ciclo B, que não tem equivalente no Ciclo A, consumiu 5,4 horas de tempo ativo e US$ 32,15, menos de 7% do tempo ativo e menos de 4% do custo do ciclo; o diferencial de custo se forma, portanto, na implementação e na validação das unidades, e não no investimento inicial.

Em tempo do desenvolvedor, o contraste é semelhante: 25,9 horas de tempo ativo no Ciclo A e 82,7 horas no Ciclo B (3,2 vezes), das quais 25,8 e 75,1 horas nas onze unidades. Por requisito, a mediana foi de 2,0 horas e de US$ 21,04 no Spec Kit, contra 6,8 horas e US$ 81,87 no BMAD-METHOD (Tabela 5). Esses números descrevem a execução observada, que inclui cinco unidades do Ciclo B continuadas além do teto de tempo; no estado em que o teto foi atingido, o tempo do Ciclo B seria menor, mas ainda superior ao do Ciclo A (Tabela 6). A leitura econômica completa exige confrontar esses custos com o produto entregue (M6 a M15), o que esta versão do estudo não pôde fazer (seção 4.5). Sem essa contrapartida, os dados indicam o preço do processo, e não a sua relação custo-benefício.

## **6.3 Impacto ambiental**

O impacto ambiental do desenvolvimento com agentes decorre do consumo de energia e de água dos centros de dados que executam os modelos, aproximadamente proporcional à quantidade de processamento de cada inferência. Como os fornecedores não divulgam o consumo por requisição, este trabalho não estima valores absolutos e usa o número de tokens processados, decomposto por fase e por categoria, como indicador relativo entre as duas metodologias. A distinção entre tokens novos e tokens lidos do cache de prompts do fornecedor é relevante nessa leitura, porque a leitura de cache dispensa parte do processamento.

O próprio desenho do estudo reduziu o consumo na etapa de avaliação: o cache de respostas de IA do backend (seção 3.5) faz com que as chamadas de IA do aplicativo sejam executadas uma única vez, na passada de gravação, e reproduzidas a partir do cache em todas as execuções medidas dos dois ciclos, em vez de repetidas a cada execução.

O indicador relativo escolhido, o volume de tokens processados, também ficou mais alto no Ciclo B. Somando o agente principal, os subagentes e todas as categorias de token, o Ciclo A processou 814,6 milhões de tokens e o Ciclo B, 2.979,6 milhões, 3,7 vezes mais (Tabela 2). A maior parte desse volume é leitura do cache de prompts do fornecedor (98,0% da entrada no Ciclo A e 97,4% no Ciclo B), que dispensa parte do processamento; os tokens de saída, que correspondem à geração de texto, foram 4,9 milhões no Ciclo A e 9,1 milhões no Ciclo B (1,9 vez), dos quais 0,64 milhão gerados por subagentes, que praticamente não existem no Ciclo A (373 tokens). Como a topologia do processo afeta o consumo por construção, sobretudo no Ciclo B, em que revisões de código e testes de ponta a ponta usam subagentes, a diferença não deve ser lida como ineficiência isolada (seção 3.9). Sem estimativa de consumo de energia ou de água por requisição, os números indicam apenas a ordem relativa do esforço computacional entre as metodologias.

# **7 CONCLUSÃO**

## **7.1 Respostas às questões de pesquisa**

A questão principal pergunta como o GitHub Spec Kit e o BMAD-METHOD se diferenciam, no processo e no produto. Nesta versão, o estudo oferece uma resposta baseada em dados apenas para a parte de processo; a parte de produto permanece em aberto. Para cada questão específica, o que os dados permitem afirmar é o seguinte.

QP1 (custo do processo). Os dois ciclos construíram o mesmo conjunto de onze unidades com custos muito diferentes. O Spec Kit consumiu 25,9 horas de tempo ativo, 4,9 milhões de tokens de saída e o equivalente a US$ 271; o BMAD-METHOD, 82,7 horas, 9,1 milhões de tokens de saída e o equivalente a US$ 902, isto é, cerca de 3,2, 1,9 e 3,3 vezes mais, respectivamente. A preparação inicial foi desprezível nos dois (cerca de 0,1 hora), e o planejamento global do BMAD-METHOD somou 5,4 horas. Na análise pareada por requisito, o BMAD-METHOD exigiu mais tempo de implementação e validação em todos os nove pares (mediana das diferenças de 4,9 horas; p exato de 0,004; correlação bisserial de postos igual a 1,0), com a ressalva de que o poder do teste é baixo e de que o resultado sem os pares censurados, com cinco pares, tem p exato de 0,0625, que é o menor valor possível com esse número de pares e não chega a 0,05. Por fase, o BMAD-METHOD gastou 48,8 horas em implementação e 28,4 horas em validação, contra 13,5 e 4,9 horas do Spec Kit, e menos tempo de especificação no total do ciclo (5,5 contra 7,6 horas). O quadro se inverte nas intervenções do pesquisador: o Spec Kit exigiu 49, das quais 40 foram correções de diferenças em relação ao protótipo ou ao pacote de entrada, e o BMAD-METHOD exigiu 16; em contrapartida, o BMAD-METHOD exigiu 279 respostas a pausas previstas pelo próprio processo, contra 67 do Spec Kit. Em resumo, o BMAD-METHOD custou mais tempo, tokens e dinheiro por requisito e provocou menos correções não previstas. Essa combinação é compatível com a ideia de que o planejamento antecipado e as revisões por história trocam esforço por menos retrabalho, mas isso é uma hipótese, que só as métricas de produto podem confirmar.

QP2 (transmissão de decisões), QP3 (qualidade do produto) e QP4 (estabilidade ao longo do ciclo) dependem das métricas de produto e diferenciais (M6 a M15), que não foram avaliadas nesta versão por falta de prazo para congelar o conjunto de avaliação antes de usá-lo (seção 4.5). Os dados de processo oferecem apenas indícios indiretos: a causa registrada das intervenções mostra que, no Ciclo A, 40 delas decorreram de diferenças entre o produto e o protótipo ou o pacote de entrada, contra 11 no Ciclo B, o que é compatível com uma transmissão mais fiel das decisões visuais no Ciclo B, mas não a demonstra, porque a medida direta é a M14. Os repositórios finais dos dois ciclos, suas tags e o protocolo de avaliação ficam disponíveis para que a avaliação seja concluída sem alterar o que foi congelado.

## **7.2 Contribuições**

O trabalho oferece contribuições de três naturezas. A primeira é empírica: até onde foi possível verificar, trata-se da primeira comparação entre o GitHub Spec Kit e o BMAD-METHOD aplicados à construção do mesmo produto, com as demais condições fixadas e com medidas extraídas de registros, e não de percepção. Os resultados permitem confrontar com o comportamento observado as notas que a comparação documental de Macedo (2026) atribui às duas metodologias.

A segunda é metodológica. O estudo propõe e documenta um protocolo para comparar metodologias de desenvolvimento com agentes de codificação, que inclui a fixação explícita das variáveis controladas, a separação entre respostas exigidas pela metodologia e intervenções do pesquisador, o congelamento por hash antes do primeiro ciclo e o registro de todos os desvios, com o efeito esperado de cada um sobre as métricas. O instrumento operacionaliza medidas propostas na agenda de pesquisa de Macedo (2026), como a revisão humana exigida pelo processo, as correções por fase, a deriva entre especificação, plano, tarefas, testes e implementação e a estabilidade das decisões.

A terceira é técnica. O backend compartilhado demonstra uma forma de tornar reprodutíveis, entre ambientes e implementações diferentes, as respostas de IA de um produto, por meio de prompts montados no servidor, de um envelope canônico de entrada e de um cache de respostas com modo estrito de reprodução. O instrumento de medição combina coleta a partir dos registros de sessão do agente, uma suíte de avaliação de caixa-preta com injeção de falhas pelo próprio backend e um avaliador baseado em modelo de linguagem com artefatos anonimizados e validação por kappa. Somam-se a isso as lições sobre o próprio instrumento (seção 5.4), que apontam fontes de contexto e de erro pouco discutidas na literatura e que devem ser consideradas em estudos semelhantes.

## **7.3 Limitações**

As limitações do estudo decorrem, em primeiro lugar, do seu desenho. Há um único sujeito, que é também o pesquisador e o operador dos dois ciclos, o que impede separar o efeito da metodologia do efeito do operador. A ordem dos ciclos é fixa, de modo que cada diferença observada combina o efeito da metodologia, o aprendizado do pesquisador e eventuais mudanças silenciosas do modelo ao longo do tempo. Com no máximo dez pares de requisitos, os testes estatísticos têm baixo poder e papel apenas complementar.

Em segundo lugar, há limitações do instrumento. A fidelidade visual depende de um protótipo produzido no próprio projeto; o avaliador baseado em modelo de linguagem é validado com amostras pequenas, que deixam largo o intervalo de confiança do kappa; a cobertura de testes mede testes escritos pelo próprio agente; e a suíte de avaliação de caixa-preta roda apenas sobre a versão final de cada ciclo. Durante a execução, o contexto do agente incluiu fontes inicialmente não previstas, como a memória automática, e o operador cometeu erros de execução registrados como desvios; ambos são tratados por análise de sensibilidade, mas não podem ser excluídos por completo.

Em terceiro lugar, os resultados valem para um aplicativo, uma pilha técnica, um agente, um modelo e versões específicas de duas metodologias que mudam com frequência. Eles caracterizam o comportamento dessas versões neste caso e devem ser lidos como evidência inicial, e não como conclusão geral sobre as metodologias. A seção 3.9 detalha cada uma dessas ameaças e as medidas adotadas para mitigá-las.

Os resultados acrescentam limitações próprias da execução. A primeira é de abrangência: por falta de prazo, a avaliação de produto (M6 a M15), a validação do avaliador e a análise diferencial não foram realizadas nesta versão do estudo (seções 4.5 a 4.7). O trabalho responde, portanto, com dados à questão sobre o custo do processo (QP1) e apenas de forma indireta às demais, e nenhuma conclusão sobre qual metodologia entrega o melhor produto deve ser extraída dele. A segunda é de tratamento das unidades: a regra de limite de tempo previa que unidades que atingissem o teto fossem encerradas como censuradas, mas cinco unidades do Ciclo B (F000, RF03, RF01, RF05 e RF09) prosseguiram além do teto por decisão do pesquisador, para fechar a verificação manual ou a última história. A análise principal usa o valor do teto como estado censurado e trata a continuação como sensibilidade, o que é uma aproximação. Além disso, a RF04 do Ciclo A e a RF03 do Ciclo B foram fechadas como incompletas, e a RF02 do Ciclo B não teve sessões próprias, porque o planejamento antecipado a incorporou à RF01; por isso, a análise pareada tem nove pares, e não dez.

A terceira limitação é de regularidade da execução. O registro soma 98 desvios do protocolo (Apêndice F), dos quais 31 são respostas do pesquisador com texto diferente do fixado, concentradas no Ciclo B, que tem mais pausas; oito sessões medidas ficaram sem coleta (duas no Ciclo A e seis no Ciclo B) e foram excluídas da leitura principal da M5; e o tempo ativo conta até 30 minutos de espera do pesquisador por pausa, de modo que parte da diferença de tempo entre os ciclos é estrutural, porque o BMAD-METHOD prevê mais pausas. Os valores em dólares são equivalentes calculados por uma tabela datada. Por fim, a ordem fixa dos ciclos continua confundida com o aprendizado do pesquisador, que favoreceria o Ciclo B, e com o ritmo mais intenso e a pressão de calendário do segundo ciclo (D-021 e D-055), que podem ter aumentado os erros de execução.

## **7.4 Trabalhos futuros**

A extensão mais direta deste trabalho é a replicação com vários desenvolvedores e ordem contrabalançada, com metade dos participantes começando por cada metodologia. Esse desenho permitiria separar o efeito da metodologia do efeito de ordem e do efeito do operador, que aqui permanecem confundidos, e daria aos testes estatísticos o poder que dez pares não oferecem.

Duas medidas consideradas e não adotadas nesta versão do instrumento podem ser acrescentadas. A primeira é a estimativa prévia de esforço por requisito, registrada fora do contexto do agente, que permitiria medir a distância entre a percepção e o tempo efetivamente gasto, na linha de Becker et al. (2025). A segunda é a estabilidade das decisões na métrica de fidelidade de handoff: a partir do histórico dos artefatos de planejamento, seria possível distinguir uma decisão alterada de forma documentada de uma decisão perdida na transmissão, o que daria quatro desfechos à M14 em vez de três. O escore de mutação (M8b), se não puder ser aplicado nesta edição, também é candidato natural.

O estudo pode ainda ser ampliado em três direções. A primeira é variar o agente de codificação, o que permitiria medir a dimensão de portabilidade, mantida aqui como variável controlada. A segunda é incluir outras ferramentas da taxonomia de Macedo (2026), como o OpenSpec e o Spec Kitty, e outras pilhas técnicas. A terceira é avaliar a evolução do produto depois dos ciclos: as funcionalidades de extensão deixadas de fora, como os planos de ação, o seletor de persona e os marcadores manuais, poderiam ser implementadas como pedidos de mudança, para medir como cada metodologia absorve alterações de escopo em um código já existente e se os artefatos mantidos no repositório de fato apoiam a manutenção, como propõe o nível *spec-anchored* do desenvolvimento orientado por especificação (Böckeler, 2025).

# **REFERÊNCIAS**

ANTHROPIC. **Measuring AI agent autonomy in practice**. \[*S. l.*\]: Anthropic, 18 fev. 2026. Disponível em: https://www.anthropic.com/research/measuring-agent-autonomy. Acesso em: 28 out. 2026.

BALTES, S. *et al*. **Guidelines for empirical studies in software engineering involving large language models**. \[*S. l.*\]: arXiv, 2025. Disponível em: <https://arxiv.org/abs/2508.15503>. Acesso em: 22 out. 2026.

BECKER, J.; RUSH, N.; BARNES, E.; REIN, D. **Measuring the impact of early-2025 AI on experienced open-source developer productivity**. \[*S. l.*\]: arXiv, 2025. Disponível em: <https://arxiv.org/abs/2507.09089>. Acesso em: 28 out. 2026.

BLACKLER, A.; POPOVIC, V.; MAHAR, D. Investigating users' intuitive interaction with complex artefacts. **Applied Ergonomics**, \[*s. l.*\], v. 41, n. 1, p. 72-92, 2010.

BMAD CODE ORGANIZATION. **BMAD-METHOD**. \[*S. l.*\]: GitHub, 2026. Disponível em: <https://github.com/bmad-code-org/BMAD-METHOD>. Acesso em: 22 out. 2026.

BÖCKELER, B. **Understanding spec-driven-development**: Kiro, spec-kit, and Tessl. \[*S. l.*\]: martinfowler.com, 15 out. 2025. Disponível em: <https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html>. Acesso em: 28 out. 2026.

BRASIL. **Lei nº 13.709, de 14 de agosto de 2018**. Lei Geral de Proteção de Dados Pessoais (LGPD). Diário Oficial da União: seção 1, Brasília, DF, 15 ago. 2018.

COHEN, J. A coefficient of agreement for nominal scales. **Educational and Psychological Measurement**, \[*s. l.*\], v. 20, n. 1, p. 37-46, 1960.

FARRAG, S. E. **The productivity-reliability paradox**: specification-driven governance for AI-augmented software development. \[*S. l.*\]: arXiv, 2026. Disponível em: <https://arxiv.org/abs/2605.01160>. Acesso em: 22 out. 2026.

GITHUB. **Spec Kit**. \[*S. l.*\]: GitHub, 2026. Disponível em: <https://github.com/github/spec-kit>. Acesso em: 22 out. 2026.

HASSAN, A. E.; LI, H.; LIN, D.; ADAMS, B.; CHEN, T.-H.; KASHIWA, Y.; QIU, D. **Agentic software engineering**: foundational pillars and a research roadmap. \[*S. l.*\]: arXiv, 2025. Disponível em: <https://arxiv.org/abs/2509.06216>. Acesso em: 28 out. 2026.

HUANG, X. *et al*. **DOne**: decoupling structure and rendering for high-fidelity design-to-code generation. \[*S. l.*\]: arXiv, 2026. Disponível em: <https://arxiv.org/abs/2604.01226>. Acesso em: 28 out. 2026.

KIM, T. *et al*. MindfulDiary: harnessing large language model to support psychiatric patients' journaling. *In*: CHI CONFERENCE ON HUMAN FACTORS IN COMPUTING SYSTEMS, 2024, Honolulu. **Proceedings** \[...\]. New York: ACM, 2024.

LANDIS, J. R.; KOCH, G. G. The measurement of observer agreement for categorical data. **Biometrics**, \[*s. l.*\], v. 33, n. 1, p. 159-174, 1977.

LEWIS, P. *et al*. Retrieval-augmented generation for knowledge-intensive NLP tasks. *In*: ADVANCES IN NEURAL INFORMATION PROCESSING SYSTEMS, 33., 2020. **Proceedings** \[...\]. \[*S. l.*\]: Curran Associates, 2020. p. 9459-9474.

LI, R.; LIANG, P.; AVGERIOU, P.; WANG, Y. **Towards automated identification of violation symptoms of architecture erosion**. \[*S. l.*\]: arXiv, 2023. Versão 6. Disponível em: https://arxiv.org/abs/2306.08616v6. Acesso em: 28 out. 2026.

LIEBERMAN, M. D.; EISENBERGER, N. I.; CROCKETT, M. J.; TOM, S. M.; PFEIFER, J. H.; WAY, B. M. Putting feelings into words: affect labeling disrupts amygdala activity in response to affective stimuli. **Psychological Science**, \[*s. l.*\], v. 18, n. 5, p. 421-428, 2007.

MACEDO, S. O. de. **From prompt to process**: a process taxonomy and comparative assessment of frameworks supporting AI software development agents. \[*S. l.*\]: arXiv, 2026. Disponível em: <https://arxiv.org/abs/2606.04967>. Acesso em: 22 out. 2026.

MARTIN, R. C. **Clean architecture**: a craftsman's guide to software structure and design. Boston: Prentice Hall, 2017.

McCABE, T. J. A complexity measure. **IEEE Transactions on Software Engineering**, \[*s. l.*\], v. SE-2, n. 4, p. 308-320, 1976.

NEPAL, S. *et al*. Contextual AI journaling: integrating LLM and time series behavioral sensing technology to promote self-reflection and well-being using the MindScape app. *In*: EXTENDED ABSTRACTS OF THE CHI CONFERENCE ON HUMAN FACTORS IN COMPUTING SYSTEMS, 2024, Honolulu. **Proceedings** \[...\]. New York: ACM, 2024.

NIELSEN, J. **End of web design**. \[*S. l.*\]: Nielsen Norman Group, 2000. Disponível em: <https://www.nngroup.com/articles/end-of-web-design/>. Acesso em: 22 out. 2026.

PENG, S.; KALLIAMVAKOU, E.; CIHON, P.; DEMIRER, M. **The impact of AI on developer productivity**: evidence from GitHub Copilot. \[*S. l.*\]: arXiv, 2023. Disponível em: <https://arxiv.org/abs/2302.06590>. Acesso em: 28 out. 2026.

PENNEBAKER, J. W. Writing about emotional experiences as a therapeutic process. **Psychological Science**, \[*s. l.*\], v. 8, n. 3, p. 162-166, 1997.

PISKALA, D. B. **Spec-driven development**: from code to contract in the age of AI coding assistants. \[*S. l.*\]: arXiv, 2026. Disponível em: <https://arxiv.org/abs/2602.00180>. Acesso em: 28 out. 2026.

RASNAYAKA, S.; WANG, G.; SHARIFFDEEN, R.; IYER, G. N. An empirical study on usage and perceptions of LLMs in a software engineering project. *In*: INTERNATIONAL WORKSHOP ON LARGE LANGUAGE MODELS FOR CODE, 1., 2024, Lisboa. **Proceedings** \[...\]. New York: ACM, 2024.

RUNESON, P.; HÖST, M. Guidelines for conducting and reporting case study research in software engineering. **Empirical Software Engineering**, \[*s. l.*\], v. 14, n. 2, p. 131-164, 2009.

SI, C.; ZHANG, Y.; LI, R.; YANG, Z.; LIU, R.; YANG, D. Design2Code: benchmarking multimodal code generation for automated front-end engineering. *In*: CONFERENCE OF THE NATIONS OF THE AMERICAS CHAPTER OF THE ASSOCIATION FOR COMPUTATIONAL LINGUISTICS, 2025, Albuquerque. **Proceedings** \[...\]. \[*S. l.*\]: ACL, 2025. p. 3956-3974.

TAGHAVI, P.; BHAVANI, S. **Spec Kit agents**: context-grounded agentic workflows. \[*S. l.*\]: arXiv, 2026. Disponível em: <https://arxiv.org/abs/2604.05278>. Acesso em: 22 out. 2026.

VERDECCHIA, R.; ENGSTRÖM, E.; LAGO, P.; RUNESON, P.; SONG, Q. Threats to validity in software engineering research: a critical reflection. **Information and Software Technology**, \[*s. l.*\], v. 164, art. 107329, 2023.

WATANABE, M.; LI, H.; KASHIWA, Y.; REID, B.; IIDA, H.; HASSAN, A. E. **On the use of agentic coding**: an empirical study of pull requests on GitHub. \[*S. l.*\]: arXiv, 2025. Disponível em: <https://arxiv.org/abs/2509.14745>. Acesso em: 28 out. 2026.

WILCOXON, F. Individual comparisons by ranking methods. **Biometrics Bulletin**, \[*s. l.*\], v. 1, n. 6, p. 80-83, 1945.

WOHLIN, C.; RUNESON, P.; HÖST, M.; OHLSSON, M. C.; REGNELL, B.; WESSLÉN, A. **Experimentation in software engineering**. Berlin: Springer, 2012.

# **APÊNDICE A – DECISÕES DE ARQUITETURA DO BACKEND (D1 A D18)**

O backend do Cerne foi projetado a partir de dezoito decisões de arquitetura, fechadas antes de sua construção e não reabertas durante os ciclos. O Quadro 9 resume cada uma delas. A pergunta que orientou todas as decisões foi o que manteria o comportamento do backend idêntico para os dois ciclos, o que explica a ênfase em garantias impostas pelo banco de dados e em mecanismos de determinismo.

Quadro 9 – Decisões de arquitetura do backend

  

|  |  |
| :-: | :-: |
| \*\*Decisão\*\* | \*\*Síntese\*\* |
| D1 – Autenticação nativa | Autenticação pelo serviço nativo do Supabase; o único \*endpoint\* próprio é o de sessão. A biometria é responsabilidade exclusiva do aplicativo, sem \*endpoint\* no servidor. |
| D2 – Endpoints escritos à mão | 23 funções com um ponto de entrada único, que padroniza validação, formato de erro, cache de respostas e injeção de falhas. O acesso direto do aplicativo ao banco fica desabilitado. |
| D3 – Dados pessoais anotados | O texto original é preservado, e os trechos com dados pessoais identificáveis são anotados por posição, com detecção por modelo de linguagem e saída estruturada. A falha da verificação não significa que algo foi encontrado. |
| D4 – Salvamento idempotente | Um índice único parcial garante que salvar duas vezes a mesma mensagem da conversa crie uma única entrada; a repetição devolve sucesso com a entrada existente, e não erro. |
| D5 – Prompts no servidor | O aplicativo envia apenas o texto digitado; histórico, entradas recuperadas, persona e instruções são montados no servidor, com versão fixa. Sem isso, o cache de respostas teria acerto próximo de zero entre ciclos. |
| D6 – Injeção de falhas | Um cabeçalho de teste, protegido por chave e ignorado em silêncio sem ela, força tempo esgotado, resposta malformada, queda de conexão, falha só da IA, atraso ou limite de taxa em cinco \*endpoints\* de escrita. |
| D7 – Isolamento no banco | \*Row Level Security\* ativada e forçada em toda tabela com dono. O papel administrativo é usado apenas no processamento de filas. Recurso de outro usuário responde “não encontrado”, nunca “proibido”. |
| D8 – Modelo de \*embeddings\* | voyage-4, com 1.024 dimensões e tipos de entrada distintos para documentos e consultas; o modelo e a dimensão são gravados em cada linha. |
| D9 – Sincronização derivada | Arquitetura sem escrita local: o servidor expõe marcas de atualização, e o selo de sincronização, com três estados, é derivado no aplicativo. |
| D10 – Sugestão única | Regra de unicidade por sessão, tipo e chave do gatilho: o aplicativo decide quando disparar, e o banco garante que o disparo ocorra uma única vez. |
| D11 – Exportação com dois estados | Os estados do processamento e da narrativa são independentes; o \*download\* dos dados brutos é liberado sem esperar a narrativa. |
| D12 – Streaming com formato fixo | Sequência fixa de eventos na conversa: mensagem criada, entradas recuperadas, trechos de texto e conclusão ou erro. |
| D13 – Tarefas no banco | Fila e agendamento por extensões do PostgreSQL, sem infraestrutura adicional e sem variação de ambiente entre ciclos. |
| D14 – Três ambientes | Desenvolvimento, Ciclo A e Ciclo B, com as mesmas migrações e os mesmos dados iniciais, e estrutura conferida antes de cada ciclo. |
| D15 – Nova tentativa da conversa | Endpoint dedicado regenera a resposta sem duplicar a pergunta; como a entrada é a mesma, a nova tentativa é servida pelo cache, sem custo e de forma determinística. |
| D16 – Defeitos após o congelamento | Defeitos não bloqueantes são apenas registrados; bloqueantes são corrigidos nos três ambientes, com registro; um bloqueante descoberto no Ciclo B torna a métrica afetada não comparável. |
| D17 – Nenhuma imagem armazenada | A imagem enviada para reconhecimento de texto é processada em memória; guarda-se apenas o seu \*hash\*, usado como chave de cache. |
| D18 – Ordem dos ciclos | Spec Kit primeiro, para que o aprendizado, que favorece o segundo ciclo, e a familiaridade prévia, que favorece o Spec Kit, atuem em direções opostas. A medida atenua, mas não elimina, o efeito de ordem. |

  

Fonte: elaborado pelo autor (2026), a partir da documentação do backend.

# **APÊNDICE B – PROTOCOLO E** ***HASHES*** **DE CONGELAMENTO**

O protocolo experimental reúne as decisões que fixam a condução dos ciclos. As decisões P1 a P14, tomadas antes do Ciclo A, estão resumidas no Quadro 10; as regras específicas de cada metodologia constam da seção 3.3, e as regras de interação do pesquisador, da seção 3.3.5.

Quadro 10 – Decisões de protocolo

  

|  |  |
| :-: | :-: |
| \*\*Decisão\*\* | \*\*Conteúdo\*\* |
| P1 – Modelo | claude-sonnet-5, por identificador fixo no arquivo de configuração; apelidos de modelo proibidos; versão do Claude Code travada. |
| P1b – Raciocínio | Esforço high fixado por variável de ambiente e pensamento estendido sempre ligado; comandos que mudam modelo ou esforço são proibidos nas sessões medidas. |
| P1c – Subagentes | Subagentes forçados para o mesmo modelo; tarefas auxiliares de segundo plano em claude-haiku-4-5-20251001. |
| P2 – Superfície | Extensão do Claude Code no VS Code, com editores fechados e anexação de contexto desligada antes de cada mensagem. |
| P3 – Permissões | Lista de permissões idêntica nos dois ciclos; pedidos aprovados uma vez por ocorrência; negar uma permissão é intervenção. |
| P4 – Sessões | Uma sessão por comando do Spec Kit ou por fluxo do BMAD-METHOD; correções em sessão nova, aberta por intervenção; limpeza manual do contexto proibida. |
| P5 – Edição manual | Proibida como rotina; quando inevitável, registrada como intervenção, com nível de alteração. |
| P5b – Mensagens neutras | Apenas confirmações a pausas espontâneas do agente e transcrição de erros pedidos por ele. |
| P5c – Tempo ativo | Cada espera pelo pesquisador conta até 30 minutos; o excedente é pausa. |
| P6 – Unidade concluída | Metodologia declara a unidade pronta, análise estática sem erros, testes do agente passando e critérios de aceite percorridos no aparelho. |
| P7 – Limite de tempo | 8 horas de tempo ativo por requisito e 12 horas na fundação; unidade que atinge o limite é encerrada como incompleta, com tempo censurado. |
| P8 – Pilha técnica | Conforme o Quadro 1, com os graus de liberdade ali indicados. |
| P9 – Granularidade e ordem | Uma unidade por requisito, precedida da fundação, na ordem da seção 3.3.4. |
| P10 – Telas de extensão | Não são construídas; a tentativa de construí-las gera uma intervenção de redirecionamento. |
| P11 – Plataforma | iOS, inicialmente em simulador; revisada antes dos ciclos para um único iPhone 16 Pro físico. |
| P12 – Idioma | Inglês nos \*prompts\*, no pacote, nos artefatos e no código; português nos textos de interface e nos marcadores das mensagens. |
| P13 – Cobrança | Mesmo plano de assinatura nos dois ciclos; sessão interrompida por limite de uso é coletada em modo manual; custo em dólares pela tabela de preços congelada. |
| P14 – Cronograma | Preparação e congelamento até 30/09/2026, Ciclo A a partir de 01/10/2026 e Ciclo B em seguida; prazos revistos durante a execução, com registro como desvio. |

  

Fonte: elaborado pelo autor (2026), a partir do protocolo congelado.

O congelamento, em 1º de outubro de 2026, consistiu no cálculo do hash SHA-256 de cada item do instrumento e na criação de uma etiqueta no repositório. Para um diretório, cada arquivo é listado com o caminho relativo ao diretório, a lista é ordenada por caminho e o hash combinado é o SHA-256 dessa listagem. O Quadro 11 apresenta os hashes vigentes; os hashes de cada arquivo constam do repositório do instrumento.

Quadro 11 – Hashes SHA-256 dos itens congelados

  

|  |  |
| :-: | :-: |
| \*\*Item\*\* | \*\*SHA-256\*\* |
| Definições das métricas | e028c992a49b59873b339b6aea76e55ec6391b344e93062677c1b0acd4fc3152 |
| Protocolo | 3a167adc2ba81e196c07181528395cbcc6ec80e0778a12e56212bf11009af50a |
| Regras concretas das métricas | b4cbfcfc2a54704d4058b9aa98469d18643910ed720135bb12c1475095b2d20d |
| Tabela de preços | 51dfa7cc099e21e2ed149315b85c81432a7c96894c12e7bf2c127634b776e274 |
| Pacote de entrada (15 arquivos) | 9e0c4b829a9149daae597d6ae4c232b3648ace94c60dac454c5ca56f0510c2d5 |
| Protótipo de referência | 61032a92f082044f979cc52f65ae2d6cb461f0420f2bd9bc676f6115185d2fff |
| Protótipo derivado (no pacote) | aa8263b221d110a599f58877935152eba2fe5802a5b272c04d16ee84864cae0b |
| Prompts de intenção (14 arquivos)\\\* | 71af323b4c5ced78966ddc02a6fa7e8949efc4022894af997cc5cfb95c7d8150 |
| Suíte de avaliação (6 arquivos) | 079032dd05abc90323c64942c67eac3614a124c7cb134a62fbc6bc19c17a81ca |
| Rubricas do avaliador (5 arquivos) | afb84d62b0323765ea8c9a44fa9e1615ee41c52834c2546bf059002c58b856ab |
| Skill de coleta | 34c2059566966940604d763079d940947e244f522d2c92c51bbdd5873e34b345 |
| Scripts de coleta e auxiliares\\\* | dd0e55edfbfded2840562a215f62cd6eef71b7736e59986f6500fd301e4f7d4e |
| Configuração do agente\\\* | 0112786e12fbe0917221c8d09f17f9f4b9c022d5ef811b9123b9fb9b0a62f393 |

  

Fonte: elaborado pelo autor (2026). \* Valor vigente após os desvios listados no Quadro 12.

Três itens congelados foram alterados depois do congelamento, sempre com entrada prévia no registro de desvios. As alterações estão no Quadro 12.

Quadro 12 – Alterações em itens congelados

  

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| \*\*Item\*\* | \*\*Desvio\*\* | \*\*Alteração\*\* | \*\*Hash anterior → vigente\*\* |
| Prompts | D-001 | Correção do cabeçalho de autorização no \*prompt\* de princípios, antes da primeira sessão | a97753fd… → 71af323b… |
| Scripts | D-004 | Novo \*script\* de faixa do limite de tempo do planejamento global do Ciclo B | 137b234a… → caaf0170… |
| Scripts | D-014 | Fase lida pela forma de invocação dos comandos | caaf0170… → 3da29380… |
| Scripts | D-015 | Respostas dadas pelo painel de perguntas do agente | 3da29380… → 86e48501… |
| Scripts | D-024 | Cálculo do tempo ativo após o fim do turno do agente | 86e48501… → e11ed378… |
| Scripts | D-049 | Registro sintético de limite de uso do plano | e11ed378… → dd0e55ed… |
| Configuração | D-009 | Tema visual acrescentado pelo próprio agente | fdb46287… → db5d321b… |
| Configuração | D-012 | Sincronização de \*skills\* e \*plugins\* da conta desligada | db5d321b… → 3904700b… |
| Configuração | D-013 | Conectores da conta desligados | 3904700b… → 0112786e… |

  

Fonte: elaborado pelo autor (2026), a partir do registro de desvios.

# **APÊNDICE C – PACOTE DE ENTRADA E** ***PROMPTS*** **DE INTENÇÃO**

Toda a informação de produto chegou aos dois ciclos por dois canais idênticos: o pacote de entrada, copiado para a pasta docs/input/ de cada repositório antes do primeiro comando, e os 14 prompts de intenção, mantidos fora dos repositórios e colados na conversa segundo uma tabela de entrega congelada. O Quadro 13 descreve o pacote.

Quadro 13 – Composição do pacote de entrada

  

|  |  |
| :-: | :-: |
| \*\*Item\*\* | \*\*Conteúdo\*\* |
| requirements.md | Tradução neutra, para o inglês, dos requisitos reconciliados: requisitos funcionais e não funcionais, telas, \*endpoints\*, ordem de entrega e restrições técnicas. |
| prototype/ | Cópia derivada do protótipo congelado, com a menção ao estudo neutralizada, e um extrato com os \*tokens\* visuais e a lista de estados de tela. |
| backend/ | Documentação de \*handoff\* do \*backend\*, traduzida e neutralizada: contrato OpenAPI, taxonomia de erros, mapa de estados da exportação, semântica do selo de sincronização e defeitos conhecidos. |
| backend/fixtures/ | Um áudio, duas imagens para reconhecimento de texto, a transcrição esperada e três textos semeados para a busca. |
| Fora do pacote | Textos usados pela suíte de avaliação, política de defeitos, roteiro de validação do \*backend\*, testes de contrato e credenciais. |

  

Fonte: elaborado pelo autor (2026), a partir do protocolo congelado.

Os prompts foram escritos em inglês e sem referência a nenhuma das metodologias. O Quadro 14 mostra onde cada um entrou em cada ciclo. A diferença entre as colunas é de método, e não de informação: o documento de requisitos completo está nos dois repositórios desde o início.

Quadro 14 – Entrega dos prompts de intenção

  

|  |  |  |
| :-: | :-: | :-: |
| \*\*Prompt\*\* | \*\*Ciclo A – GitHub Spec Kit\*\* | \*\*Ciclo B – BMAD-METHOD\*\* |
| P-SETUP (princípios) | Argumento do comando constitution | Regras do fluxo de contexto de projeto, na preparação |
| P-GLOBAL (visão do produto) | Anexado ao \*prompt\* da fundação, no primeiro specify | Argumento do \*brainstorming\*, primeiro fluxo da análise |
| P-F000 e P-RF01 a P-RF10 | Argumento do specify de cada unidade, um por vez, na ordem de entrega | Todos de uma vez, na ordem de entrega, como entrada da criação do PRD |
| P-TECH (instrução técnica) | Argumento do plan de cada unidade | Primeira mensagem do fluxo de arquitetura, uma única vez |
| Demais comandos e fluxos | Sem argumento | Sem argumento além do que o próprio fluxo pede |

  

Fonte: elaborado pelo autor (2026), a partir do protocolo congelado.

Reproduzem-se a seguir, na íntegra, o prompt de princípios, o de visão do produto, o de instrução técnica e, como exemplo dos prompts de unidade, o do RF06. Os demais seguem a mesma estrutura do último: objetivo da unidade, referências às seções do pacote, endpoints, material de teste, dependências e restrições.

\# P-SETUP — Project principles

  

Use the principles below as the governing rules for all work in this repository.

  

\#\# Product and sources

  

\- This repository builds \*\*Cerne\*\*, a mobile reflective-journaling app with an AI assistant.

\- The product input is in \`docs/input/\`:

  - \`requirements.md\` — functional and quality requirements, screens, API, delivery order and technical constraints;

  - \`prototype/\` — the frozen visual prototype and its extract (visual tokens, list of states);

  - \`backend/\` — documentation of the existing backend: API, error taxonomy, screen-state map, sync-badge semantics and fixtures.

\- These documents are the source of truth for the product. Where they are silent, make a reasonable technical decision.

  

\#\# Fixed technical stack

  

\- Flutter and Dart at the version pinned for this repository (fvm).

\- State management: \`flutter\_bloc\`.

\- Clean Architecture, three layers per feature.

\- Error handling: \`fpdart\`; repositories return \`Either\<Failure, T\>\`.

\- Test doubles: \`mocktail\`.

\- On-device speech-to-text: \`whisper\_ggml\`. Audio never goes to the backend.

\- Visual tokens: \`lib/core/design\_tokens.dart\` is the single source of colors, typography, spacing and radii.

\- Platform: iOS.

\- Backend: already built and frozen. The app consumes its API as documented in \`docs/input/backend/\`. All AI features, including semantic search, are provided by the backend. Configuration and credentials come from a \`.env\` file at the project root, with exactly two variables: \`FUNCTIONS\_BASE\_URL\` and \`SUPABASE\_ANON\_KEY\`. Every call to \`{FUNCTIONS\_BASE\_URL}/\<function\>\` carries the header \`apikey: \<SUPABASE\_ANON\_KEY\>\`. The \`Authorization: Bearer\` header carries \`SUPABASE\_ANON\_KEY\` on the operations that need no user session (sign-up, login, refresh) and the user's access token on every operation marked \`bearerAuth\` in \`docs/input/backend/api/openapi.yaml\`.

\- Everything else — routing, HTTP client, local cache, dependency injection, secure storage, biometrics, charts — is your choice.

  

\#\# Folder convention

  

\`\`\`

lib/

  core/

  features/

    \<feature\>/

      data/

      domain/

      presentation/

\`\`\`

  

\#\# Quality

  

\- Meet the quality requirements RNF01–RNF09 in \`docs/input/requirements.md\`.

\- The domain layer follows RNF06.

  

\#\# User interface

  

\- The UI is faithful to the prototype in \`docs/input/prototype/\`.

\- UI text is in \*\*Portuguese\*\*, exactly as written in the prototype.

\- Code identifiers, comments and project documentation are in English.

  

\#\# Scope

  

\- Implement the functional requirements in the delivery order given in \`docs/input/requirements.md\`.

\- Extension features (section 2 of \`requirements.md\`) are not implemented. A menu entry may exist as a placeholder.

  

\#\# Do not

  

\- Change the backend, its API contract or its configuration.

\- Call AI providers directly from the app.

\- Write visual values (colors, font sizes, spacing, radii) outside \`design\_tokens.dart\`.

\- Implement extension features.

\- Commit \`.env\` or any credential.

\- Edit the files in \`docs/input/\`.

\# P-GLOBAL — Product vision

  

\*\*Cerne\*\* is a mobile reflective-journaling app with an AI assistant. The user records their day by text, audio or photo; a conversational agent consults those records through semantic search to answer with context and to offer proactive insights. The app also keeps a timeline of all records, lets the user search and filter them, exports a personal summary and shows an evolution dashboard. Access is protected by biometrics or PIN.

  

\#\# Scope

  

The functional requirements RF01–RF10 in \`docs/input/requirements.md\`, section 1:

\- RF01 — Multimodal capture (text / audio / photo)

\- RF02 — Speech-to-text / OCR processing

\- RF03 — Biometric authentication vault

\- RF04 — Interactive chat with memory (RAG)

\- RF05 — Personal summary export

\- RF06 — Semantic search / filter over journal entries

\- RF07 — Multi-source history (timeline)

\- RF08 — Proactive insights (mechanism)

\- RF09 — Temporal summaries / dashboard

\- RF10 — Save a chat message as an entry

  

Plus the quality requirements RNF01–RNF09 (sections 3 and 4) and a foundation unit (F000). Delivery order: section 12.

  

\#\# Out of scope

  

The extension features of section 2 (manual tags, action plans, persona): no functional implementation; a menu entry may exist as a placeholder. The backend already exists and is not changed.

  

\#\# Where everything is

  

\- \`docs/input/requirements.md\` — requirements, screens, endpoints, delivery order, technical constraints.

\- \`docs/input/prototype/\` — the visual prototype (\`cerne-prototype.html\`) and its extract.

\- \`docs/input/backend/\` — API contract and backend documentation.

  

\#\# Do not

  

\- Build extension features.

\- Change the backend.

\- Add features that are not in \`requirements.md\`.

\# P-TECH — Technical instruction

  

Follow the technical constraints in \`docs/input/requirements.md\` and the architecture already in place in the project.

\# P-RF06 — Semantic search / filter

  

Let the user find entries by meaning and narrow them with filters, on the My Records screen.

  

\- Requirement and acceptance criteria: \`docs/input/requirements.md\`, section 1, RF06; parameter: section 10.

\- Prototype states: search bar of "Tela 4 — Meus Registros", "Tela 4 — Sheet de filtro", "Tela 4 — Filtros ativos" (prototype extract, section 2.4, including the note on categories).

\- Backend: \`GET /entries/search\`, \`GET /entries\`.

\- Test material: \`docs/input/backend/fixtures/seeded-search-entries.md\`.

\- Depends on: RF07.

  

\#\# Do not

  

\- Implement features of later units.

\- Build extension features (requirements, section 2).

\- Change the backend.

# **APÊNDICE D – RUBRICAS DO AVALIADOR**

O avaliador baseado em modelo de linguagem (seção 3.6.4) aplica quatro rubricas, resumidas no Quadro 15. Cada rubrica tem definições, prompt, formato de saída em JSON, regra de maioria entre as três execuções e um exemplo sintético, aplicado à mão pelo pesquisador antes do congelamento para conferir que a rubrica leva à saída esperada.

Quadro 15 – Rubricas do avaliador

  

|  |  |  |
| :-: | :-: | :-: |
| \*\*Rubrica\*\* | \*\*Item avaliado e entrada\*\* | \*\*Saída\*\* |
| M6 – Divergências entre plano e código | Uma unidade: plano da unidade e \*diff\* do código entre a etiqueta anterior e a da unidade | Lista de divergências, cada uma com indicação de documentação no plano, causa (ctx, chk, inc, prd, amb ou out) e evidência |
| M9 – Espaçamento | Um estado de tela: quadro do protótipo e captura do aplicativo, na mesma escala | Espaçamento adequado ou não; desvios acima de 4 pontos, por região da tela |
| M14 – Fidelidade de \*handoff\* | Uma decisão: texto da decisão, árvore de lib/ e trechos do código final que contêm os termos da decisão | Implementada, parcialmente implementada ou não implementada, com evidência |
| D16 – Severidade | Uma intervenção de correção: sintoma descrito e critério de aceite relacionado, sem a severidade dada pelo pesquisador | S1, S2 ou S3, com justificativa |

  

Fonte: elaborado pelo autor (2026), a partir das rubricas congeladas.

Antes de qualquer envio, o material é anonimizado: o rótulo do ciclo é trocado por um código aleatório fixado por item; diretórios e arquivos que identificam a metodologia recebem nomes neutros, com o mesmo mapeamento aplicado aos caminhos citados no texto; termos que identificam as ferramentas, nomes de persona e cabeçalhos de modelo de documento são removidos por expressões regulares; e o nome da metodologia, o ciclo, as etiquetas e as datas nunca são enviados. Uma resposta fora do formato é repetida uma vez e, se falhar de novo, o item vai para a amostra humana, assim como todo item sem maioria.

A escala de severidade da D16, usada pelo pesquisador no momento da intervenção e pelo avaliador na validação, está no Quadro 16.

Quadro 16 – Escala de severidade dos defeitos

  

|  |  |
| :-: | :-: |
| \*\*Nível\*\* | \*\*Definição\*\* |
| S1 – Cosmético | Detalhe visual ou de texto; nenhum critério de aceite afetado. |
| S2 – Funcional com contorno | Um critério de aceite ou requisito falha em parte, mas o fluxo é utilizável ou há contorno razoável. |
| S3 – Bloqueante | Um critério de aceite fica impossível de cumprir, ou há falha do aplicativo ou perda de dados do usuário. |

  

Fonte: elaborado pelo autor (2026).

Como exemplo, reproduz-se o prompt da rubrica da M14, na versão congelada.

You check whether a technical DECISION from a design document was implemented in the CODE.

  

Answer "yes" if the code does what the decision says, where it says.

Answer "partial" if the decision is followed in some of the applicable code but not in all of it,

or only partly.

Answer "no" if the code does not follow the decision, or does the opposite.

Judge only this decision. Cite evidence as file:line. If you cannot find the relevant code in the

material given, answer "no" and say so in the justification.

  

Answer only with JSON matching the schema.

  

DECISION:

\<\<\<DECISION\>\>\>

  

FILE TREE:

\<\<\<TREE\>\>\>

  

FILES:

\<\<\<FILES\>\>\>

# **APÊNDICE E – CENÁRIOS DA SUÍTE DE AVALIAÇÃO**

A suíte de avaliação de caixa-preta (seção 3.6.3) roda uma única vez por ciclo, sobre a versão final do aplicativo, com o backend em modo de reprodução estrita. O banco é restaurado e populado uma vez, antes da suíte, com três contas de teste: uma com 34 entradas, três conversas e quatro marcadores, uma com uma entrada e uma vazia. Os elementos da interface são identificados pelo texto visível do protótipo, e elementos sem texto, pela posição relativa no quadro. Um proxy acrescenta a todas as requisições o cabeçalho de teste e um instante fixo, registra cada chamada e injeta falhas apenas onde o cenário manda.

Os cenários rodam em três blocos, porque as chamadas de IA cuja chave de cache depende de identificadores do banco precisam vir antes de qualquer criação de entrada na conta principal: o primeiro bloco usa a conta principal sem escrita; o segundo, as contas com uma e com nenhuma entrada; e o terceiro, a conta principal com escrita. Três cenários são estruturais e são verificados por análise estática do código final. O Quadro 17 lista os 28 cenários, que cobrem os 27 critérios de aceite dos dez requisitos.

Quadro 17 – Cenários dos critérios de aceite

  

|  |  |  |
| :-: | :-: | :-: |
| \*\*Cenário\*\* | \*\*Verificação\*\* | \*\*Natureza\*\* |
| H01-1 | Entradas por texto, áudio e foto são gravadas no mesmo formato | Comportamental |
| H01-2 | Cancelar a captura no meio não cria entrada | Comportamental |
| H02-1 | A transcrição mostra os estados de gravação, processamento, texto transcrito e erro; o reconhecimento de imagem ilegível mostra erro com nova tentativa | Comportamental |
| H03-1 | A falha da biometria oferece o PIN, sem bloquear o usuário | Comportamental |
| H03-2 | Depois de 5 minutos em segundo plano, o aplicativo exige nova autenticação | Comportamental |
| H04-1 | A conversa mostra os estados de resposta em fluxo, completa e com erro | Comportamental |
| H04-2 | A queda no meio do fluxo mantém a resposta parcial com indicação de falha, e a nova tentativa não duplica a pergunta | Comportamental |
| H05-1 | A exportação de um período sem entradas mostra estado de erro tratado | Comportamental |
| H05-2 | A falha da narrativa ainda permite baixar os dados brutos | Comportamental |
| H06-1 | A busca exibe todas as entradas relacionadas devolvidas pelo \*backend\* | Comportamental |
| H06-2 | Digitação rápida gera uma única consulta, depois de 300 ms | Comportamental |
| H06-3 | Depois da reconexão, a lista local corresponde ao servidor, sem duplicatas | Comportamental |
| H06-4 | Dois filtros combinados restringem a lista com E lógico | Comportamental |
| H06-5 | Limpar os filtros restaura a lista completa sem reiniciar a tela | Comportamental |
| H07-1 | Sessão expirada leva a novo acesso, sem falha e sem perder a posição da lista | Comportamental |
| H07-2 | O selo de sincronização não depende do estado de autenticação | Estrutural |
| H07-3 | Nenhum BLoC importa outro BLoC | Estrutural |
| H08-1 | O gatilho de cinco mensagens dispara a sugestão uma única vez | Comportamental |
| H08-2 | O gatilho de 2 minutos de inatividade dispara a sugestão uma única vez | Comportamental |
| H08-3 | A falha da sugestão não afeta a conversa | Comportamental |
| H08-4 | Descartar a sugestão não altera a conversa nem a posição da tela | Comportamental |
| H09-1 | O painel funciona com zero, uma e mais de 30 entradas | Comportamental |
| H09-2 | A agregação é recalculada depois de uma nova entrada | Comportamental |
| H09-3 | Narrativa muito longa ou vazia não quebra a interface | Comportamental |
| H10-1 | A conversa não importa a camada de dados da funcionalidade de entradas | Estrutural |
| H10-2 | Salvar duas vezes a mesma mensagem não duplica a entrada | Comportamental |
| H10-3 | A falha ao salvar mantém a conversa utilizável e permite nova tentativa | Comportamental |
| H10-4 | Só as mensagens do usuário têm o botão de salvar | Comportamental |

  

Fonte: elaborado pelo autor (2026), a partir da suíte congelada. O número do cenário indica o requisito (H01 = RF01).

Os 15 cenários de falha de rede combinam os cinco endpoints de escrita com três tipos de falha: tempo esgotado, resposta malformada e ausência de conexão. A falha é acionada por cabeçalho e executada pelo próprio backend, que a registra, o que permite conferir que cada uma foi de fato injetada. Um cenário é considerado tratado quando quatro condições valem ao mesmo tempo: o aplicativo não quebra; um estado de erro aparece na tela da ação, exceto na sugestão proativa, cuja falha não deve ser exibida ao usuário; nada do que o usuário digitou, gravou ou escolheu se perde; e, removida a falha, a mesma ação funciona sem reiniciar o aplicativo. O Quadro 18 resume os cenários.

Quadro 18 – Cenários de falha de rede

  

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| \*\*Cenários\*\* | \*\*Endpoint\*\* | \*\*Ação\*\* | \*\*Estado esperado\*\* |
| F01–F03 | entries-create | Salvar uma entrada de texto | Modal aberto, texto preservado e erro com nova tentativa |
| F04–F06 | chat-messages-send | Enviar uma mensagem | Mensagem preservada e indicação de falha com nova tentativa, ou aviso de ausência de conexão |
| F07–F09 | media-ocr | Reconhecer o texto de uma imagem | Estado de erro do reconhecimento, com nova tentativa |
| F10–F12 | export-summary-create | Pedir a exportação | Folha de exportação em estado de erro, sem PDF vazio |
| F13–F15 | chat-insight-create | Gatilho de sugestão por inatividade | Nenhum erro visível; a conversa continua funcionando |

  

Fonte: elaborado pelo autor (2026), a partir da suíte congelada. Em cada grupo, os três cenários correspondem a tempo esgotado, resposta malformada e ausência de conexão.

# **APÊNDICE F – REGISTRO DE DESVIOS**

O registro de desvios acompanha o protocolo congelado (seção 3.6.5): cada ocorrência que se afastou do que o protocolo previa foi anotada no momento em que foi percebida, com data, escopo, descrição, causa, arquivos afetados, efeito sobre as métricas e ameaça à validade correspondente, e nenhum dado bruto foi corrigido. Ao fim do Ciclo B o registro tinha 98 desvios, numerados de D-001 a D-098: 12 referentes apenas ao Ciclo A, 56 apenas ao Ciclo B, 29 aos dois ciclos e um à Parte IV do estudo. O registro completo, com todos os campos, está no arquivo docs/desvios.md do repositório do experimento. O Quadro 20 os agrupa pela natureza e indica como cada grupo foi tratado na análise.

Quadro 20 – Desvios do protocolo, agrupados por natureza

  

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| \*\*Grupo\*\* | \*\*Desvios\*\* | \*\*n\*\* | \*\*Natureza\*\* e tratamento |
| Ambiente e configuração do contexto | D-009 a D-013, D-017, D-018, D-038, D-040 | 9 | Skills, plugins e conectores da conta que entravam no contexto do agente; atualizações automáticas do sistema e do Xcode; backend hospedado e chave de acesso; configuração de um ciclo usada em outro projeto. As chaves de configuração foram desligadas por igual nos dois ciclos e conferidas com /context (Apêndice G). |
| Texto do protocolo e procedimentos | D-001 a D-008, D-014, D-016, D-019, D-020, D-023, D-025, D-034 | 15 | Correções de texto, interpretações de lacunas e regras acrescentadas durante a execução (ordem das sessões do Spec Kit, tratamento de diferenças de tela, roteiros de verificação manual, correção repetida). Aplicadas igualmente aos dois ciclos quando a regra era comum. |
| Instrumento de coleta | D-015, D-024, D-044, D-049, D-054, D-056, D-096 | 7 | Falhas e limitações do coletor (faixa de timebox indevida, coluna de limite de uso não confiável, modo manual, contexto da IDE) corrigidas no código, com testes. Os transcritos brutos ficaram intactos, e as tabelas foram re-derivadas deles (D-096). |
| Sessões interrompidas, repetidas, paralelas ou sem coleta | D-028, D-031, D-032, D-035 a D-037, D-047, D-053, D-057, D-059, D-065, D-069, D-071 a D-075, D-077, D-081, D-094 | 20 | Cortes por limite de uso, reinícios do computador, coletas repetidas ou prematuras, sessões abertas fora da configuração, mensagens livres sem prefixo e seis sessões medidas sem coleta no Ciclo B. As mensagens livres entram só na leitura ampla da M5, e as sessões sem coleta ficam fora da leitura principal. |
| Respostas fora do texto fixado | D-022, D-027, D-029, D-030, D-039, D-041, D-043, D-046, D-048, D-050 a D-052, D-062, D-063, D-066 a D-068, D-070, D-076, D-078, D-079, D-082 a D-089, D-091, D-093 | 31 | Respostas do pesquisador a perguntas e painéis do agente com texto diferente do fixado no roteiro, ou sem o prefixo previsto. Concentram-se no Ciclo B, que tem muito mais pausas de confirmação. Tratadas por sensibilidade da M5 e da M5b; nenhum dado bruto foi alterado. |
| Memória automática do agente | D-033, D-042 | 2 | Arquivos de memória criados pelo próprio agente numa sessão medida e carregados nas seguintes, um caso em cada ciclo. As sessões afetadas são analisadas com e sem esse contexto. |
| Exposição de números ao pesquisador | D-045 | 1 | Valores de tempo, tokens e custo de duas sessões do Ciclo B foram exibidos ao pesquisador por erro do assistente de apoio. As regras de parada não dependem desses valores. |
| Calendário, limite de tempo e retrospectivas | D-021, D-026, D-055, D-058, D-060, D-061, D-064, D-080, D-090, D-092 | 10 | Novo prazo do Ciclo B; regra de encerramento antecipado; cinco continuações de unidade além do teto de tempo por decisão do pesquisador (F000, RF03, RF01, RF05 e RF09); RF03 fechada como incompleta; retrospectivas do BMAD rodadas ao fim do ciclo. O estado no teto é tratado como censura, e a continuação, como sensibilidade. |
| Escopo da análise e trilha do harness | D-095, D-097, D-098 | 3 | Corte da suíte de caixa-preta adiado e Parte IV reduzida por prazo: só as métricas de processo e de artefatos foram calculadas (seções 4.1 a 4.8); a análise pareada adaptou o plano de análise (D-098). |

Fonte: elaborado pelo autor (2026), a partir do registro docs/desvios.md do repositório do experimento.

Os desvios mais relevantes para a leitura dos resultados são os do grupo de calendário e limite de tempo, porque afetam o tratamento estatístico da M2, e os de sessões sem coleta, porque afetam a contagem da M5. Os demais alteram a composição de uma sessão ou de uma resposta e foram tratados por sensibilidade. A seção 4.1 retoma os que afetam a interpretação dos resultados.

# **APÊNDICE G – VERIFICAÇÃO DO CONTEXTO DO AGENTE**

Este apêndice reúne as conferências do contexto do agente feitas por meio do comando /context do Claude Code, que lista as categorias de contexto carregadas em uma sessão (instruções do sistema, ferramentas, skills, mensagens e espaço livre). Elas verificaram, antes de cada ciclo, que nenhuma skill, plugin, conector ou memória da conta do pesquisador entrava no contexto do agente e que a skill de coleta de sessão ficava fora dele. As capturas de tela originais estão no repositório do experimento, na pasta dados/evidencias/; o Quadro 21 registra o que cada conferência mostrou.

Quadro 21 – Conferências do contexto do agente com o comando /context

  

|  |  |  |  |
| :-: | :-: | :-: | :-: |
| \*\*Conferência\*\* | \*\*Data\*\* | \*\*O que o /context mostrou\*\* | \*\*Captura (dados/evidencias/)\*\* |
| GATE-C20: skill de coleta fora do contexto (ensaio, Ciclos A e B) | 01/10/2026 | A skill coletar-sessao não aparece em nenhuma categoria nas duas configurações, por desenho (campo disable-model-invocation da própria skill). Skills pessoais da conta ainda apareciam, achado tratado na D-009. | gate-c20-ciclo-a.png; gate-c20-ciclo-b.png |
| GATE-A02: largada do Ciclo A | 07/10/2026 | Modelo claude-sonnet-5, somente skills speckit-\\\*, nenhuma skill da conta, skill de coleta ausente. | gate-a02-ciclo-a.png |
| GATE-A02b: após a D-012 | 08/10 e 11/10/2026 | Modelo claude-sonnet-5 e ausência de CLAUDE.md; pastas de skills e plugins sincronizados da conta ausentes no disco. A categoria MCP tools mostrava 634 tokens (conectores da conta), o que originou a D-013. | gate-a02b-pos-d012-ciclo-a.png |
| GATE-A02c: após a D-013 | 11/10/2026 | Categoria MCP tools zerada; skills em cerca de 2,8 mil tokens; sem memória nem CLAUDE.md; configurações dos dois ciclos idênticas (mesmo hash). | gate-a02c-ciclo-a.png |
| GATE-B02: largada do Ciclo B | 25/10/2026 | Modelo claude-sonnet-5 e nenhuma categoria de MCP tools. As 49 skills bmad-\\\* foram conferidas por listagem do disco, porque o painel não lista skills por nome; sem skills ou plugins sincronizados. | gate-b02-ciclo-b.png |

Fonte: elaborado pelo autor (2026), a partir do registro de conferências do experimento (plano de ciclos) e das capturas de tela em dados/evidencias/ do repositório.

Os autores das ferramentas e do agente podem alterar, entre versões, o que é carregado por padrão em uma sessão. Por isso, as conferências acima foram repetidas toda vez que um achado mudou a configuração, e o conjunto de chaves resultante (D-009, D-012 e D-013) é o mesmo nos dois ciclos. As conferências mostram o estado do contexto no início da sessão; o que o agente criou depois, como os arquivos de memória automática encontrados no Ciclo A (D-033) e no Ciclo B (D-042), é tratado por análise de sensibilidade e declarado nas ameaças à validade (seção 3.9).