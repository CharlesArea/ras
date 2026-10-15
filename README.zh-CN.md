<div align="center">

<img src="assets/readme/ras-pipeline.svg" alt="RAS 从请求和证据到报告输出的流程" width="100%">

# RAS — Report Anything Skill

### 将请求和证据转化为人们真正愿意阅读的报告。

六套视觉主题 · 16 种可复用模板 · 从同一个规范模型生成 DOCX、PDF 和可选的可编辑 PPTX

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

![输出](https://img.shields.io/badge/输出-DOCX%20%2B%20PDF%20%2B%20可选%20PPTX-117A8B?style=flat-square)
![主题](https://img.shields.io/badge/主题-6-117A8B?style=flat-square)
![测试](https://img.shields.io/badge/测试-19%20passing-027A48?style=flat-square)

</div>

## RAS 是什么

许多报告自动化工具只停留在文字层面。RAS 将报告视为经过设计、可审计的成果：它会选择合适的沟通形式，保留证据链，解析视觉系统，从同一个规范模型生成 DOCX 和 PDF，可选地生成可编辑的 PPTX，并在交付前检查输出。

你可以用自然语言描述结果：

> “比较这些方案，为董事会推荐一条路径。”

> “创建一份带清晰趋势图的 KPI 评审。”

> “把这份研究整理成有证据依据的综合报告。”

> “解释事故、根因、影响和纠正措施。”

RAS 会把请求转化为结构化项目，其中包含独立 Markdown 区块、来源台账、视觉契约和质量收据。

### 本地化文档

你可以阅读[简体中文](README.zh-CN.md)、[繁體中文](README.zh-TW.md)、[日本語](README.ja.md)、[한국어](README.ko.md)、[Español](README.es.md)、[Français](README.fr.md)、[Deutsch](README.de.md)、[Português (Brasil)](README.pt-BR.md) 或 [Русский](README.ru.md) 版本。RAS 也会保留报告区块中的 Unicode 文本，并支持为本地化报告输出配置 CJK 回退字体。

## 实际展示

以下预览来自本仓库中的示例和验收夹具，而不是静态样张。

<table>
  <tr>
    <td width="50%"><img src="assets/readme/kpi-dashboard.png" alt="带趋势图的数据驱动 KPI 报告"></td>
    <td width="50%"><img src="assets/readme/technical-blueprint.png" alt="带原创架构图的技术报告"></td>
  </tr>
  <tr>
    <td align="center"><sub>数据驱动的 KPI 评审</sub></td>
    <td align="center"><sub>技术架构报告</sub></td>
  </tr>
</table>

<table>
  <tr>
    <td width="50%"><img src="assets/readme/editorial-brief.png" alt="暖色纸张配色的编辑风格执行摘要"></td>
    <td width="50%"><img src="assets/readme/ras-growth-chart.png" alt="RAS 报告中的全球增长比较图"></td>
  </tr>
  <tr>
    <td align="center"><sub>编辑风格执行摘要</sub></td>
    <td align="center"><sub>带图表的分析比较</sub></td>
  </tr>
</table>

### 可编辑的 PPTX 伴侣

演示文稿渲染器会将同一个报告项目转换成宽屏、可编辑的幻灯片。经济报告示例保留原生 PowerPoint 增长图表，将来源台账保留为可编辑表格，并把完整来源引用和区块正文放入演讲者备注。

<table>
  <tr>
    <td width="33%"><img src="assets/readme/economy-deck-cover.png" alt="全球经济报告的可编辑 PPTX 封面"></td>
    <td width="33%"><img src="assets/readme/economy-deck-chart.png" alt="经济报告中的原生增长图表幻灯片"></td>
    <td width="33%"><img src="assets/readme/economy-deck-sources.png" alt="可编辑的来源台账幻灯片"></td>
  </tr>
  <tr>
    <td align="center"><sub>演示文稿封面</sub></td>
    <td align="center"><sub>原生图表页</sub></td>
    <td align="center"><sub>可编辑来源台账</sub></td>
  </tr>
</table>

## 在 Codex 中安装

RAS 以带版本的 Codex 插件发布。添加稳定版 `v0.1.0` 的市场：

```bash
codex plugin marketplace add CharlesArea/ras --ref v0.1.0
codex plugin add ras@ras-marketplace
```

然后开始新的 Codex 对话并使用 `$ras`。如果使用插件浏览器，请运行 `codex`，执行 `/plugins`，打开 **RAS — Report Anything Skill** 并选择 **Install plugin**，按提示安装 Python 渲染运行环境后开始新对话。

```text
Use $ras to turn these notes into an evidence-grounded decision memo and
deliver DOCX, PDF, and an editable PPTX companion.
```

Codex 目前使用 `codex plugin add` 安装共享技能，而不是 `codex skill install`。上面的命令固定到经过测试的版本；如需使用默认分支的最新市场状态，可省略 `--ref v0.1.0`。

### 下载或手动安装

可从 [GitHub Releases](https://github.com/CharlesArea/ras/releases/latest) 下载打包源码，或为本地开发安装同一个固定版本：

```bash
git clone --branch v0.1.0 https://github.com/CharlesArea/ras.git
cd ras
python -m pip install -e ".[render]"
```

需要 Python 3.11 或更高版本。可移植插件清单位于 [`plugin.json`](plugin.json)，市场目录位于 [`marketplace.json`](.agents/plugins/marketplace.json)，并包含 [Codex](.codex-plugin/plugin.json) 与 [Claude](.claude-plugin/plugin.json) 兼容清单。

## 快速开始

初始化一个报告项目：

```bash
ras-report init reports/my-report \
  --request "Create an evidence-grounded decision memo from these notes" \
  --archetype decision-memo
```

RAS 会从普通语言中推断内容深度，也可以显式覆盖：

```bash
ras-report init reports/economy-deep-dive \
  --request "Create a detailed comparison of the economy before and after COVID" \
  --depth deep --research web --pages 15
```

可用配置为 `quick`、`standard` 和 `deep`。使用以下命令随时查看解析后的计划：

```bash
ras-report plan reports/economy-deep-dive/manifest.yaml
```

编辑生成的 `manifest.yaml`、`sources.yaml` 和 Markdown 区块，然后执行验证、构建和质量检查：

```bash
ras-report validate reports/my-report/manifest.yaml
ras-report build reports/my-report/manifest.yaml --formats docx,pdf,pptx
ras-report qa reports/my-report/manifest.yaml
```

DOCX 和 PDF 是核心输出，可通过 Python 渲染依赖运行。PPTX 是可选的可编辑伴侣，需要主机提供内置 Node.js 和 Artifact Tool 运行环境。

### 输出目标

| 格式 | 支持情况 | 运行环境 |
| --- | --- | --- |
| DOCX | 核心输出 | Python 与 `python-docx` |
| PDF | 核心输出 | Python 与 ReportLab |
| PPTX | 可选的可编辑伴侣 | 主机 Node.js 与 Artifact Tool |

也可以从可复用模板目录生成更完整的项目：

```bash
ras-report template list
ras-report init reports/board-decision --template decision-memo \
  --request "Compare the options and recommend a path for the board"
```

使用以下命令探索视觉语言：

```bash
ras-report theme list
ras-report theme inspect data-forward
```

<details>
<summary><strong>报告项目包含什么</strong></summary>

```text
reports/my-report/
├── manifest.yaml       # 请求、风格决策、区块、输出、QA 收据
├── sources.yaml        # 来源和声明支持
├── blocks/*.md         # 独立、可恢复的内容单元
├── assets/             # 提供或生成的视觉资产
├── build/              # 规范模型和中间视觉结果
├── qa/                 # 收据和渲染页面图像
└── dist/               # 最终 DOCX、PDF 和可选 PPTX
```

</details>

## RAS 可以制作什么

RAS 适合需要结构、判断和可追溯性的报告：

| 意图 | 适用场景 |
| --- | --- |
| 执行摘要 | 管理层摘要和简洁评审 |
| 决策备忘录 | 方案、权衡、建议和后续行动 |
| 研究综述 | 跨来源的证据型发现 |
| 深度分析 | 趋势、原因、影响和解读 |
| 对比评估 | 前后、方案、供应商或政策比较 |
| 提案与路线图 | 商业论证、战略、计划和里程碑 |
| KPI 与状态评审 | 指标、图表、进展和运营节奏 |
| 审计、风险与合规 | 控制措施、证据缺口、发现和缓解 |
| 技术报告 | 架构、系统、事故和调查 |
| SOP 与案例研究 | 可重复流程和记录型案例 |

路由器提供 16 种报告原型；如果请求已经明确形状，显式覆盖会优先采用。

### 可复用模板

模板是可编辑、可恢复的区块集合，而不是锁定的版式：

| 模板族 | 包含形状 |
| --- | --- |
| 决策与比较 | 决策备忘录、对比评估、提案/商业论证 |
| 研究与分析 | 研究综述、深度分析、调查/根因分析 |
| 运营节奏 | 状态/进展、绩效/KPI、战略路线图 |
| 风险与保障 | 审计评估、合规/风险、事故复盘 |
| 技术与流程 | 技术架构、政策/SOP、案例研究 |

使用 `ras-report template inspect <template>` 查看准确的区块蓝图。

### 轻量内容规划

每个新项目都会自动记录内容计划，其中包含目标页数范围、字数范围、幻灯片目标以及每节字数预算。“详细分析”会选择 deep，“简洁摘要”会选择 quick。主机可以据此扩展上下文、证据、影响和限制，而不是靠无依据的填充。

## 工作方式

1. **路由请求：** 从请求中解析原型、受众、语气、证据级别、页面形状、视觉风格、密度和强调方式；显式用户选择优先。
2. **规划内容：** 解析深度、目标页面、章节预算和研究模式。外部研究需要显式 `web` 模式或明确的在线研究请求。
3. **构建独立区块：** 每个区块都有稳定 ID、沟通目标、状态、来源引用、版面预算和可选视觉契约，可以单独重新生成。
4. **解析设计系统：** 在渲染前统一解析主题、品牌令牌、语义组件、字体、图表调色板、图示语言、间距和页面节奏。
5. **渲染与验证：** DOCX 和 PDF 来自同一个规范模型；PPTX 让图表保持 PowerPoint 图表、表格保持可编辑表格，并把来源和完整区块文本保留在演讲者备注中。QA 检查结构、章节一致性、可访问性、PDF 可读性和渲染页面完整性。

## 设计系统

主题不只是颜色预设，还会改变层级、封面、语义面板、表格、图表、图示、字体、间距和构图规则。

| 主题 | 个性 | 适用场景 |
| --- | --- | --- |
| `minimal` | 安静、紧凑 | 短小、少装饰的报告 |
| `editorial` | 温暖、叙事化 | 执行摘要和故事型工作 |
| `data-forward` | 清晰、指标导向 | KPI、比较和仪表盘 |
| `institutional` | 正式、结构化 | 政策、审计和合规 |
| `technical` | 像蓝图一样精确 | 架构和运营 |
| `narrative` | 富有表现力、节奏感强 | 案例研究和长篇综合 |

项目级 `.ras/brand.yaml` 可以覆盖品牌颜色、字体、间距、组件令牌、图表调色板和图示令牌。Markdown 的 **粗体**、*斜体* 和 `code` 会在请求的输出格式中保持一致。

## 证据模型

用户提供的材料是主要证据。只有在用户请求或明确授权时才使用外部研究。来源台账记录出处：

```yaml
sources:
  - id: S1
    title: Official source title
    publisher: Publisher
    url: https://example.com/source
    publication_date: "2026-01-01"
```

区块使用稳定标记引用来源：

```markdown
The supported finding is stated here [S1].
```

验证器会检查来源引用、声明支持、必需视觉的说明文字和替代文本、不安全路径，以及是否有未解析的占位符。

## 视觉与可访问性

图表支持带标签、数值、说明和替代文本的 `bar`、`line`、`pie` 规格。图示使用轻量语义语法，生成原始 SVG 和 PNG 资产。

信息型视觉包括：可见说明文字、报告中的替代文本、DOCX 中的嵌入图像元数据，以及构建模型中的确定性资产。内置视觉管线依赖较少：Pillow 和 SVG 基元处理图表与图示，ReportLab 和 python-docx 生成最终文档。

## 示例和夹具

- [`examples/executive-brief`](examples/executive-brief) — 编辑风格的管理层评审
- [`examples/kpi-report`](examples/kpi-report) — 数据驱动的图表报告
- [`examples/technical-report`](examples/technical-report) — 带架构图的技术报告
- [`examples/decision-memo`](examples/decision-memo) — 带选项与建议的可复用模板
- [`examples/strategy-roadmap`](examples/strategy-roadmap) — 优先级、里程碑和衡量指标
- [`examples/incident-postmortem`](examples/incident-postmortem) — 无责事故时间线和纠正措施
- [`fixtures/traditional-chinese`](fixtures/traditional-chinese) — CJK 渲染验收夹具
- [`fixtures/insufficient-evidence`](fixtures/insufficient-evidence) — 证据不足行为夹具
- [`reports/covid-economy-comparison`](reports/covid-economy-comparison) — 有来源的全球前后比较项目

生成的 `build/`、`qa/` 和 `dist/` 目录会被忽略，因此源项目保持可审查且可复现。

## 开发

运行标准库测试：

```bash
python -m unittest discover -s tests -v
```

完整验收：

```bash
python -m unittest discover -s tests -v
ras-report validate examples/executive-brief/manifest.yaml
ras-report build examples/executive-brief/manifest.yaml --formats docx,pdf,pptx
ras-report qa examples/executive-brief/manifest.yaml
```

可选渲染依赖在 [`pyproject.toml`](pyproject.toml) 中声明：

```bash
python -m pip install -e ".[render]"
```

## 范围

RAS v1 聚焦有证据依据的 DOCX 和 PDF 报告、可选的可编辑 PPTX 伴侣、可复用模板和轻量内容规划。Web 报告、电子表格附录和协作编辑流程仍不属于当前渲染器契约。

## 许可证

请参阅 [`LICENSE`](LICENSE)。
