<div align="center">

<img src="assets/readme/ras-pipeline.svg" alt="Pipeline do RAS, da solicitação e evidências até o relatório" width="100%">

# RAS — Report Anything Skill

### Transforme uma solicitação e suas evidências em um relatório que as pessoas realmente querem ler.

Seis temas visuais · Dezesseis templates reutilizáveis · DOCX + PDF + PPTX editável opcional a partir de um modelo canônico

[English](README.md) ·
<a href="README.zh-CN.md">简体中文</a> ·
<a href="README.zh-TW.md">繁體中文</a> ·
<a href="README.ja.md">日本語</a> ·
<a href="README.ko.md">한국어</a> ·
<a href="README.es.md">Español</a> ·
<a href="README.fr.md">Français</a> ·
<a href="README.de.md">Deutsch</a> ·
<a href="README.pt-BR.md">Português (Brasil)</a> ·
<a href="README.ru.md">Русский</a>

![Saídas](https://img.shields.io/badge/saídas-DOCX%20%2B%20PDF%20%2B%20PPTX%20opcional-117A8B?style=flat-square)
![Temas](https://img.shields.io/badge/temas-6-117A8B?style=flat-square)
![Testes](https://img.shields.io/badge/testes-19%20passing-027A48?style=flat-square)

</div>

## Por que RAS

A maioria das automações de relatórios para no texto. O RAS trata o relatório como um artefato projetado e auditável: escolhe a forma de comunicação, mantém o caminho das evidências visível, resolve um sistema visual, renderiza DOCX e PDF a partir do mesmo modelo canônico, adiciona opcionalmente um PPTX editável e verifica as saídas antes da entrega.

Peça o resultado em linguagem natural:

> “Compare as opções para o conselho e recomende um caminho.”

> “Crie uma revisão de KPI com um gráfico de tendência claro.”

> “Transforme esta pesquisa em uma síntese baseada em evidências.”

> “Explique o incidente, a causa raiz, o impacto e as ações corretivas.”

O RAS transforma a solicitação em um projeto estruturado com blocos Markdown independentes, registro de fontes, contrato visual e recibo de qualidade.

### Documentação localizada

Leia o projeto em [简体中文](README.zh-CN.md), [繁體中文](README.zh-TW.md), [日本語](README.ja.md), [한국어](README.ko.md), [Español](README.es.md), [Français](README.fr.md), [Deutsch](README.de.md), [Português (Brasil)](README.pt-BR.md) ou [Русский](README.ru.md). O RAS também preserva texto Unicode nos blocos e aceita fontes CJK de fallback configuráveis.

## Veja em ação

Estas prévias são renderizadas a partir dos exemplos e fixtures de aceitação deste repositório.

<table>
  <tr>
    <td width="50%"><img src="assets/readme/kpi-dashboard.png" alt="Relatório de KPI orientado a dados com gráfico de tendência"></td>
    <td width="50%"><img src="assets/readme/technical-blueprint.png" alt="Relatório técnico com diagrama de arquitetura original"></td>
  </tr>
  <tr>
    <td align="center"><sub>Revisão de KPI orientada a dados</sub></td>
    <td align="center"><sub>Relatório de arquitetura técnica</sub></td>
  </tr>
</table>

<table>
  <tr>
    <td width="50%"><img src="assets/readme/editorial-brief.png" alt="Brief executivo editorial com paleta de papel quente"></td>
    <td width="50%"><img src="assets/readme/ras-growth-chart.png" alt="Gráfico de comparação do crescimento global em um relatório RAS"></td>
  </tr>
  <tr>
    <td align="center"><sub>Brief executivo editorial</sub></td>
    <td align="center"><sub>Comparação analítica com gráfico</sub></td>
  </tr>
</table>

### Companheiros PPTX editáveis

O renderizador de apresentações adapta o mesmo pacote de relatório para um deck widescreen editável. Os gráficos continuam como gráficos nativos do PowerPoint, o registro de fontes continua como tabela editável e as referências completas e o texto dos blocos ficam nas notas do apresentador.

<table>
  <tr>
    <td width="33%"><img src="assets/readme/economy-deck-cover.png" alt="Capa PPTX editável do relatório da economia global"></td>
    <td width="33%"><img src="assets/readme/economy-deck-chart.png" alt="Slide com gráfico de crescimento nativo"></td>
    <td width="33%"><img src="assets/readme/economy-deck-sources.png" alt="Slide editável do registro de fontes"></td>
  </tr>
  <tr>
    <td align="center"><sub>Capa do deck</sub></td>
    <td align="center"><sub>Slide com gráfico nativo</sub></td>
    <td align="center"><sub>Registro de fontes editável</sub></td>
  </tr>
</table>

## Instalar no Codex

O RAS é distribuído como um plugin versionado do Codex. Adicione o marketplace da versão estável `v0.1.0`:

```bash
codex plugin marketplace add CharlesArea/ras --ref v0.1.0
codex plugin add ras@ras-marketplace
```

Depois, inicie uma nova conversa no Codex e peça para usar `$ras`. Pelo navegador de plugins, inicie `codex`, execute `/plugins`, abra **RAS — Report Anything Skill** e escolha **Install plugin**. Siga a configuração para instalar o ambiente de renderização Python.

```text
Use $ras to turn these notes into an evidence-grounded decision memo and
deliver DOCX, PDF, and an editable PPTX companion.
```

Atualmente, o Codex instala skills compartilhadas com `codex plugin add`, e não com `codex skill install`. Os comandos acima fixam a versão testada; omita `--ref v0.1.0` para usar o estado mais recente do marketplace.

### Baixar ou instalar manualmente

Baixe o código empacotado em [GitHub Releases](https://github.com/CharlesArea/ras/releases/latest) ou instale a mesma versão fixada para desenvolvimento local:

```bash
git clone --branch v0.1.0 https://github.com/CharlesArea/ras.git
cd ras
python -m pip install -e ".[render]"
```

Python 3.11 ou mais recente é necessário. O manifesto portátil está em [`plugin.json`](plugin.json), o catálogo do marketplace em [`marketplace.json`](.agents/plugins/marketplace.json), e os manifestos compatíveis com [Codex](.codex-plugin/plugin.json) e [Claude](.claude-plugin/plugin.json) também estão incluídos.

## Início rápido

Inicialize um projeto de relatório:

```bash
ras-report init reports/my-report \
  --request "Create an evidence-grounded decision memo from these notes" \
  --archetype decision-memo
```

A profundidade é inferida da linguagem natural; você pode substituir profundidade, modo de pesquisa e número de páginas:

```bash
ras-report init reports/economy-deep-dive \
  --request "Create a detailed comparison of the economy before and after COVID" \
  --depth deep --research web --pages 15
```

Os perfis disponíveis são `quick`, `standard` e `deep`. Consulte o plano resolvido com:

```bash
ras-report plan reports/economy-deep-dive/manifest.yaml
```

Edite `manifest.yaml`, `sources.yaml` e os blocos Markdown; depois valide, faça o build e execute QA:

```bash
ras-report validate reports/my-report/manifest.yaml
ras-report build reports/my-report/manifest.yaml --formats docx,pdf,pptx
ras-report qa reports/my-report/manifest.yaml
```

DOCX e PDF são as saídas principais. PPTX é um companheiro editável opcional e requer o Node.js do host e o ambiente Artifact Tool.

### Formatos de saída

| Formato | Suporte | Runtime |
| --- | --- | --- |
| DOCX | Saída principal | Python com `python-docx` |
| PDF | Saída principal | Python com ReportLab |
| PPTX | Companheiro editável opcional | Node.js do host e Artifact Tool |

### Estrutura de um projeto

```text
reports/my-report/
├── manifest.yaml       # solicitação, estilo, blocos, saídas e recibo QA
├── sources.yaml        # procedência e suporte das afirmações
├── blocks/*.md         # unidades independentes e retomáveis
├── assets/             # recursos visuais fornecidos ou gerados
├── build/              # modelo canônico e visuais intermediários
├── qa/                 # recibos e imagens das páginas renderizadas
└── dist/               # DOCX, PDF e PPTX opcional finais
```

## O que ele produz

O RAS atende relatórios que precisam de estrutura, julgamento e rastreabilidade:

| Intenção | Útil para |
| --- | --- |
| Brief executivo | Resumos para a liderança e revisões concisas |
| Memorando de decisão | Opções, trade-offs, recomendações e próximos passos |
| Síntese de pesquisa | Descobertas baseadas em várias fontes |
| Análise profunda | Tendências, causas, implicações e interpretação |
| Avaliação comparativa | Comparações antes/depois, de opções, fornecedores ou políticas |
| Proposta e roadmap | Casos de negócio, estratégias, planos e marcos |
| KPI e status | Métricas, gráficos, progresso e cadência operacional |
| Auditoria, risco e compliance | Controles, lacunas de evidência, achados e mitigações |
| Relatório técnico | Arquitetura, sistemas, incidentes e investigações |
| SOP e estudo de caso | Procedimentos repetíveis e exemplos documentados |

O roteador oferece dezesseis arquétipos, com substituições explícitas quando a solicitação já define a forma.

### Templates reutilizáveis

Templates são conjuntos de blocos editáveis e retomáveis, não layouts bloqueados:

| Família | Formas incluídas |
| --- | --- |
| Decisão e comparação | Memorando de decisão, avaliação comparativa, proposta/caso de negócio |
| Pesquisa e análise | Síntese de pesquisa, análise profunda, investigação/causa raiz |
| Cadência operacional | Status/progresso, performance/KPI, roadmap estratégico |
| Risco e assurance | Auditoria, compliance/risco, postmortem |
| Técnico e processual | Arquitetura técnica, política/SOP, estudo de caso |

Veja o blueprint exato com `ras-report template inspect <template>`.

### Planejamento leve de conteúdo

Cada pacote registra automaticamente um plano com faixa de páginas, faixa de palavras, objetivo de slides e orçamento de palavras por seção. “Análise detalhada” seleciona deep; “brief conciso” seleciona quick. Assim o host pode ampliar contexto, evidências, implicações e limitações sem criar preenchimento sem suporte.

## Como funciona

1. **Roteia a solicitação:** resolve arquétipo, público, tom, nível de evidência, geometria, estilo visual, densidade e ênfase.
2. **Planeja o conteúdo:** resolve profundidade, páginas, orçamentos e modo de pesquisa. Pesquisa externa exige `web` ou um pedido claro.
3. **Constrói blocos independentes:** cada bloco tem ID estável, objetivo, status, fontes, orçamento de layout e contrato visual opcional.
4. **Resolve um sistema de design:** tema, tokens de marca, componentes, tipografia, paleta de gráficos, linguagem de diagramas, espaçamento e ritmo de página são definidos antes do render.
5. **Renderiza e verifica:** DOCX e PDF usam o mesmo modelo; PPTX mantém gráficos nativos, tabelas editáveis e referências nas notas. QA verifica estrutura, paridade, acessibilidade, legibilidade e integridade das páginas.

## Sistema de design

Os temas mudam hierarquia, capa, painéis semânticos, tabelas, gráficos, diagramas, tipografia, espaçamento e composição, não apenas as cores.

| Tema | Personalidade | Melhor para |
| --- | --- | --- |
| `minimal` | Calmo e compacto | Relatórios curtos e sóbrios |
| `editorial` | Quente e narrativo | Briefs executivos e histórias |
| `data-forward` | Nítido e orientado a métricas | KPIs, comparações e dashboards |
| `institutional` | Formal e estruturado | Políticas, auditorias e compliance |
| `technical` | Preciso como um blueprint | Arquitetura e operações |
| `narrative` | Expressivo e ritmado | Estudos de caso e sínteses longas |

`.ras/brand.yaml` pode sobrepor cores, fontes, espaçamento, tokens, paletas e tokens de diagramas. Markdown suporta **negrito**, *itálico* e `code` de forma consistente.

## Modelo de evidências

O material fornecido pelo usuário é a evidência principal. Pesquisa externa só é usada quando solicitada ou autorizada claramente. O registro de fontes preserva a procedência e os blocos citam com marcadores estáveis como `[S1]`.

```yaml
sources:
  - id: S1
    title: Official source title
    publisher: Publisher
    url: https://example.com/source
    publication_date: "2026-01-01"
```

A validação verifica referências, suporte das afirmações, captions e texto alternativo, caminhos seguros e placeholders não resolvidos.

## Visuais e acessibilidade

Gráficos aceitam especificações `bar`, `line` e `pie` com rótulos, valores, captions e texto alternativo. Diagramas usam uma pequena gramática semântica e geram ativos SVG e PNG originais. Visuais informativos recebem caption visível, texto alternativo, metadados de imagem no DOCX e um ativo determinístico no modelo de build.

## Exemplos e fixtures

- [`examples/executive-brief`](examples/executive-brief) — revisão gerencial editorial
- [`examples/kpi-report`](examples/kpi-report) — relatório de gráficos orientado a dados
- [`examples/technical-report`](examples/technical-report) — relatório técnico com diagrama
- [`examples/decision-memo`](examples/decision-memo) — template com opções e recomendação
- [`examples/strategy-roadmap`](examples/strategy-roadmap) — prioridades, marcos e medidas
- [`examples/incident-postmortem`](examples/incident-postmortem) — linha do tempo e ações corretivas
- [`fixtures/traditional-chinese`](fixtures/traditional-chinese) — fixture de aceitação de renderização CJK
- [`fixtures/insufficient-evidence`](fixtures/insufficient-evidence) — comportamento para evidência insuficiente
- [`reports/covid-economy-comparison`](reports/covid-economy-comparison) — pacote de comparação global com fontes

Os diretórios gerados `build/`, `qa/` e `dist/` são ignorados para manter os pacotes de origem revisáveis e reproduzíveis.

## Desenvolvimento

```bash
python -m unittest discover -s tests -v
```

Passagem completa de aceitação:

```bash
python -m unittest discover -s tests -v
ras-report validate examples/executive-brief/manifest.yaml
ras-report build examples/executive-brief/manifest.yaml --formats docx,pdf,pptx
ras-report qa examples/executive-brief/manifest.yaml
```

As dependências opcionais de renderização estão declaradas em [`pyproject.toml`](pyproject.toml):

```bash
python -m pip install -e ".[render]"
```

## Escopo

O RAS v1 concentra-se em relatórios DOCX e PDF baseados em evidências, companheiros PPTX editáveis opcionais, templates reutilizáveis e planejamento leve de conteúdo. Relatórios web, anexos de planilhas e fluxos de edição colaborativa ficam fora do contrato atual do renderizador.

## Licença

Consulte [`LICENSE`](LICENSE).
