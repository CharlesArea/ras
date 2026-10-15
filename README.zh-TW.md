<div align="center">

<img src="assets/readme/ras-pipeline.svg" alt="RAS 從請求與證據到報告輸出的流程" width="920">

# RAS — Report Anything Skill

### 將請求與證據轉化為人們真正願意閱讀的報告。

六套視覺主題 · 16 種可重複使用的模板 · 從同一個規範模型生成 DOCX、PDF 與可選的可編輯 PPTX

[English](README.md) ·
<a href="README.zh-CN.md">简体中文</a> ·
<a href="README.zh-TW.md">繁體中文</a> ·
<a href="README.ja.md">日本語</a>

![輸出](https://img.shields.io/badge/輸出-DOCX%20%2B%20PDF%20%2B%20可選%20PPTX-117A8B?style=flat-square)
![主題](https://img.shields.io/badge/主題-6-117A8B?style=flat-square)
![測試](https://img.shields.io/badge/測試-19%20passing-027A48?style=flat-square)

</div>

## RAS 是什麼

RAS 將使用者請求與可用證據整理成結構化報告專案。它會選擇合適的報告形狀，保留來源與引用關係，解析視覺主題，並在交付前檢查輸出品質。

RAS 支援 DOCX 與 PDF 核心輸出，也可以在主機具備 Node.js 與 Artifact Tool 執行環境時生成可編輯的 PPTX 簡報伴侶。

## 主要能力

- 16 種報告類型：執行摘要、決策備忘錄、研究綜述、深度分析、比較評估、商業論證、路線圖、KPI、稽核、風險、技術報告、事故檢討、SOP 等。
- 6 套視覺主題：`minimal`、`editorial`、`data-forward`、`institutional`、`technical`、`narrative`。
- 自動內容規劃：從請求推斷 `quick`、`standard` 或 `deep`，並為每個章節生成頁數、字數與投影片目標。
- 證據模型：來源台帳、聲明紀錄、穩定引用標記、假設、限制與證據缺口。
- 多格式渲染：DOCX、PDF，以及可選的可編輯 PPTX。PPTX 中的圖表與表格保持原生可編輯。

## 輸出格式

| 格式 | 支援情況 | 執行環境 |
| --- | --- | --- |
| DOCX | 核心輸出 | Python 與 `python-docx` |
| PDF | 核心輸出 | Python 與 ReportLab |
| PPTX | 可選的可編輯伴侶 | 主機 Node.js 與 Artifact Tool |

## 安裝

```bash
git clone https://github.com/CharlesArea/ras.git
cd ras
python -m pip install -e ".[render]"
```

主機側技能說明位於 [`skills/ras/SKILL.md`](skills/ras/SKILL.md)。Codex 與 Claude 外掛清單位於 [`.codex-plugin`](.codex-plugin/plugin.json) 與 [`.claude-plugin`](.claude-plugin/plugin.json)。

## 快速開始

初始化一個報告專案：

```bash
ras-report init reports/my-report \
  --request "Create an evidence-grounded decision memo from these notes" \
  --archetype decision-memo
```

RAS 會從一般語言中推斷內容深度：

```bash
ras-report init reports/economy-deep-dive \
  --request "Create a detailed comparison of the economy before and after COVID" \
  --depth deep --research web --pages 15
```

可用深度為 `quick`、`standard` 與 `deep`。使用以下命令查看已解析的計畫：

```bash
ras-report plan reports/economy-deep-dive/manifest.yaml
```

編輯生成的 `manifest.yaml`、`sources.yaml` 與 Markdown 章節，然後執行：

```bash
ras-report validate reports/my-report/manifest.yaml
ras-report build reports/my-report/manifest.yaml --formats docx,pdf,pptx
ras-report qa reports/my-report/manifest.yaml
```

預設研究模式使用使用者提供的材料。只有明確使用 `--research web` 或在請求中明確要求線上研究時，才會授權外部研究。

## 可重複使用的模板

模板是一組可編輯、可恢復的章節起始結構，而不是固定版式：

```bash
ras-report template list
ras-report init reports/board-decision --template decision-memo \
  --request "Compare the options and recommend a path for the board"
```

使用 `ras-report template inspect <template>` 查看具體章節藍圖。

## 範例與展示

倉庫中的範例包含決策備忘錄、策略路線圖、事故檢討、KPI 報告與技術架構報告。README 英文版包含完整的 DOCX/PDF/PPTX 展示圖：

- [`examples/decision-memo`](examples/decision-memo)
- [`examples/strategy-roadmap`](examples/strategy-roadmap)
- [`examples/incident-postmortem`](examples/incident-postmortem)
- [`reports/covid-economy-comparison`](reports/covid-economy-comparison)

## 證據與品質

使用者提供的材料是主要證據。每個來源應在 `sources.yaml` 中擁有穩定 ID，報告章節使用 `[S1]` 等標記引用來源。RAS 會檢查來源引用、聲明支援、未解析佔位符、視覺說明文字、替代文字、路徑安全與跨格式章節一致性。

## 開發

```bash
python -m unittest discover -s tests -v
python -m pip install -e ".[render]"
```

目前版本的範圍是有證據依據的 DOCX、PDF 報告、可選的可編輯 PPTX、可重複使用的模板與輕量內容規劃。Web 報告、電子表格附錄與協作編輯不在目前渲染器範圍內。

## 授權條款

請參閱 [`LICENSE`](LICENSE)。
