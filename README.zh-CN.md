<div align="center">

<img src="assets/readme/ras-pipeline.svg" alt="RAS 从请求和证据到报告输出的流程" width="920">

# RAS — Report Anything Skill

### 将请求和证据转化为人们真正愿意阅读的报告。

六套视觉主题 · 16 种可复用模板 · 从同一个规范模型生成 DOCX、PDF 和可选的可编辑 PPTX

[English](README.md) ·
<a href="README.zh-CN.md">简体中文</a> ·
<a href="README.zh-TW.md">繁體中文</a> ·
<a href="README.ja.md">日本語</a>

![输出](https://img.shields.io/badge/输出-DOCX%20%2B%20PDF%20%2B%20可选%20PPTX-117A8B?style=flat-square)
![主题](https://img.shields.io/badge/主题-6-117A8B?style=flat-square)
![测试](https://img.shields.io/badge/测试-19%20passing-027A48?style=flat-square)

</div>

## RAS 是什么

RAS 将用户请求和可用证据整理成结构化报告项目。它会选择合适的报告形状，保留来源和引用关系，解析视觉主题，并在交付前检查输出质量。

RAS 支持 DOCX 和 PDF 核心输出，也可以在主机具备 Node.js 与 Artifact Tool 运行环境时生成可编辑的 PPTX 演示文稿伴侣。

## 主要能力

- 16 种报告类型：执行摘要、决策备忘录、研究综述、深度分析、对比评估、商业论证、路线图、KPI、审计、风险、技术报告、事故复盘、SOP 等。
- 6 套视觉主题：`minimal`、`editorial`、`data-forward`、`institutional`、`technical`、`narrative`。
- 自动内容规划：从请求推断 `quick`、`standard` 或 `deep`，并为每个章节生成页数、字数和幻灯片目标。
- 证据模型：来源台账、声明记录、稳定引用标记、假设、限制和证据缺口。
- 多格式渲染：DOCX、PDF，以及可选的可编辑 PPTX。PPTX 中的图表和表格保持原生可编辑。

## 输出格式

| 格式 | 支持情况 | 运行环境 |
| --- | --- | --- |
| DOCX | 核心输出 | Python 和 `python-docx` |
| PDF | 核心输出 | Python 和 ReportLab |
| PPTX | 可选的可编辑伴侣 | 主机 Node.js 和 Artifact Tool |

## 安装

```bash
git clone https://github.com/CharlesArea/ras.git
cd ras
python -m pip install -e ".[render]"
```

主机侧技能说明位于 [`skills/ras/SKILL.md`](skills/ras/SKILL.md)。Codex 和 Claude 插件清单位于 [`.codex-plugin`](.codex-plugin/plugin.json) 和 [`.claude-plugin`](.claude-plugin/plugin.json)。

## 快速开始

初始化一个报告项目：

```bash
ras-report init reports/my-report \
  --request "Create an evidence-grounded decision memo from these notes" \
  --archetype decision-memo
```

RAS 会从普通语言中推断内容深度：

```bash
ras-report init reports/economy-deep-dive \
  --request "Create a detailed comparison of the economy before and after COVID" \
  --depth deep --research web --pages 15
```

可用深度为 `quick`、`standard` 和 `deep`。使用以下命令查看已解析的计划：

```bash
ras-report plan reports/economy-deep-dive/manifest.yaml
```

编辑生成的 `manifest.yaml`、`sources.yaml` 和 Markdown 章节，然后执行：

```bash
ras-report validate reports/my-report/manifest.yaml
ras-report build reports/my-report/manifest.yaml --formats docx,pdf,pptx
ras-report qa reports/my-report/manifest.yaml
```

默认研究模式使用用户提供的材料。只有明确使用 `--research web` 或在请求中明确要求在线研究时，才会授权外部研究。

## 可复用模板

模板是一组可编辑、可恢复的章节起始结构，而不是固定版式：

```bash
ras-report template list
ras-report init reports/board-decision --template decision-memo \
  --request "Compare the options and recommend a path for the board"
```

使用 `ras-report template inspect <template>` 查看具体章节蓝图。

## 示例和展示

仓库中的示例包含决策备忘录、战略路线图、事故复盘、KPI 报告和技术架构报告。README 的英文版包含完整的 DOCX/PDF/PPTX 展示图：

- [`examples/decision-memo`](examples/decision-memo)
- [`examples/strategy-roadmap`](examples/strategy-roadmap)
- [`examples/incident-postmortem`](examples/incident-postmortem)
- [`reports/covid-economy-comparison`](reports/covid-economy-comparison)

## 证据和质量

用户提供的材料是主要证据。每个来源应在 `sources.yaml` 中拥有稳定 ID，报告章节使用 `[S1]` 等标记引用来源。RAS 会检查来源引用、声明支持、未解析占位符、视觉说明文字、替代文本、路径安全和跨格式章节一致性。

## 开发

```bash
python -m unittest discover -s tests -v
python -m pip install -e ".[render]"
```

当前版本的范围是有证据依据的 DOCX、PDF 报告、可选的可编辑 PPTX、可复用模板和轻量内容规划。Web 报告、电子表格附录和协作编辑不在当前渲染器范围内。

## 许可证

请参阅 [`LICENSE`](LICENSE)。
