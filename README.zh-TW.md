<div align="center">

<img src="assets/readme/ras-pipeline.svg" alt="RAS 從請求與證據到報告輸出的流程" width="100%">

# RAS — Report Anything Skill

### 將請求與證據轉化為人們真正願意閱讀的報告。

適用於 Codex 與 Claude Code 的技能 · 六套視覺主題 · 16 種模板 · DOCX、PDF 與可選的可編輯 PPTX

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

![輸出](https://img.shields.io/badge/輸出-DOCX%20%2B%20PDF%20%2B%20可選%20PPTX-117A8B?style=flat-square)
![主題](https://img.shields.io/badge/主題-6-117A8B?style=flat-square)
![測試](https://img.shields.io/badge/測試-19%20passing-027A48?style=flat-square)

</div>

## RAS 是什麼

許多報告自動化只停留在文字。RAS 將報告視為經過設計且可稽核的成果：選擇適合的溝通形式、保留證據鏈、解析視覺系統、從同一個模型產生 DOCX 與 PDF、可選擇加入可編輯 PPTX，並在交付前檢查輸出。

你可以用自然語言描述想要的結果：

> 「比較這些方案，為董事會推薦一條路徑。」

> 「建立一份帶有清楚趨勢圖的 KPI 檢視。」

> 「把這份研究整理成有證據依據的綜合報告。」

> 「說明事故、根本原因、影響與矯正措施。」

RAS 會將請求轉成結構化專案，其中包含獨立 Markdown 區塊、來源台帳、視覺契約與品質收據。

### 本地化文件

你可以閱讀[简体中文](README.zh-CN.md)、[繁體中文](README.zh-TW.md)、[日本語](README.ja.md)、[한국어](README.ko.md)、[Español](README.es.md)、[Français](README.fr.md)、[Deutsch](README.de.md)、[Português (Brasil)](README.pt-BR.md) 或 [Русский](README.ru.md) 版本。RAS 也會保留報告區塊中的 Unicode 文字，並支援為本地化報告輸出設定 CJK 後備字型。

**開始使用 RAS：**[安裝至 Codex 或 Claude Code](#install-guide)。

## 實際展示

以下預覽取自本儲存庫中的範例與驗收夾具，而不是靜態樣張。

<table>
  <tr>
    <td width="50%"><img src="assets/readme/kpi-dashboard.png" alt="帶有趨勢圖的資料驅動 KPI 報告"></td>
    <td width="50%"><img src="assets/readme/technical-blueprint.png" alt="帶有原創架構圖的技術報告"></td>
  </tr>
  <tr>
    <td align="center"><sub>資料驅動 KPI 檢視</sub></td>
    <td align="center"><sub>技術架構報告</sub></td>
  </tr>
</table>

<table>
  <tr>
    <td width="50%"><img src="assets/readme/editorial-brief.png" alt="暖色紙張配色的編輯風格執行摘要"></td>
    <td width="50%"><img src="assets/readme/ras-growth-chart.png" alt="RAS 報告中的全球成長比較圖"></td>
  </tr>
  <tr>
    <td align="center"><sub>編輯風格執行摘要</sub></td>
    <td align="center"><sub>帶圖表的分析比較</sub></td>
  </tr>
</table>

### 可編輯的 PPTX 伴侶

簡報渲染器會將同一個報告專案轉成寬螢幕、可編輯的投影片。經濟報告範例保留原生 PowerPoint 成長圖表，將來源台帳保留為可編輯表格，並把完整來源引用與區塊正文放入講者備註。

<table>
  <tr>
    <td width="33%"><img src="assets/readme/economy-deck-cover.png" alt="全球經濟報告的可編輯 PPTX 封面"></td>
    <td width="33%"><img src="assets/readme/economy-deck-chart.png" alt="經濟報告中的原生成長圖表投影片"></td>
    <td width="33%"><img src="assets/readme/economy-deck-sources.png" alt="可編輯的來源台帳投影片"></td>
  </tr>
  <tr>
    <td align="center"><sub>簡報封面</sub></td>
    <td align="center"><sub>原生圖表頁</sub></td>
    <td align="center"><sub>可編輯來源台帳</sub></td>
  </tr>
</table>

<a id="install-guide"></a>

## 在 Codex 或 Claude Code 中安裝

RAS 是報告撰寫技能，並以外掛形式提供給 Codex 與 Claude Code。請安裝至你使用的代理程式。`ras-report` 指令是可選的獨立渲染器，適合直接執行或透過腳本使用。

### Codex

在 Codex CLI 中加入穩定版 `v0.1.0` 市集並安裝外掛：

```bash
codex plugin marketplace add CharlesArea/ras --ref v0.1.0
codex plugin add ras@ras-marketplace
```

若要透過 Codex 應用程式的外掛瀏覽器安裝，只執行第一個指令以註冊市集，接著開啟 `/plugins`，選取 **RAS — Report Anything Skill** 並按下 **Install plugin**。安裝後開始新的 Codex 對話並呼叫 `$ras`。

```text
Use $ras to turn these notes into an evidence-grounded decision memo and
deliver DOCX, PDF, and an editable PPTX companion.
```

### Claude Code

在 Claude Code 終端機加入 RAS 市集並安裝外掛：

```bash
claude plugin marketplace add CharlesArea/ras
claude plugin install ras@ras-marketplace
```

在互動工作階段中，也可以執行 `/plugin marketplace add CharlesArea/ras`，接著執行 `/plugin install ras@ras-marketplace` 並選擇安裝範圍。技能的呼叫方式是 `/ras:ras`；渲染器設定方式是 `/ras:setup`。詳情請參閱 [Claude Code 外掛安裝指南](https://code.claude.com/docs/en/plugins/install)。

### 外掛與市集檔案

可攜式外掛清單位於 [`plugin.json`](plugin.json)。此專案提供 [Codex](.agents/plugins/marketplace.json) 與 [Claude Code](.claude-plugin/marketplace.json) 市集目錄，以及相容於 [Codex](.codex-plugin/plugin.json) 和 [Claude Code](.claude-plugin/plugin.json) 的清單。

## 快速開始

安裝後，以一般語言要求技能建立所需報告。請說明是否需要深入分析、外部研究，以及 DOCX/PDF 等交付格式。

在 Codex 中：

```text
$ras 請建立一份有證據依據的詳細報告，比較 COVID 前後的經濟狀況。請研究
最新的一手資料、說明主要變化與限制，並提供 DOCX 和 PDF。
```

在 Claude Code 中：

```text
/ras:ras 請建立一份有證據依據的詳細報告，比較 COVID 前後的經濟狀況。
請研究最新的一手資料、說明主要變化與限制，並提供 DOCX 和 PDF。
```

RAS 會依據請求推斷 `quick`、`standard` 或 `deep` 計畫。產生 DOCX/PDF 需要本機渲染器和 Python 3.11 以上版本；系統提示設定時請確認。PPTX 為選用格式，需要提供支援之 Node.js 和 Artifact Tool 的主機環境。

## 選用：直接使用渲染器 CLI

本節僅適用於直接或透過腳本使用渲染器，不會安裝技能：

```bash
python -m pip install "ras-report-anything[render] @ git+https://github.com/CharlesArea/ras.git@v0.1.0"
```

需要 Python 3.11 或以上版本。

初始化一個報告專案：

```bash
ras-report init reports/my-report \
  --request "Create an evidence-grounded decision memo from these notes" \
  --archetype decision-memo
```

RAS 會從一般語言推斷內容深度，也可以明確指定：

```bash
ras-report init reports/economy-deep-dive \
  --request "Create a detailed comparison of the economy before and after COVID" \
  --depth deep --research web --pages 15
```

可用深度為 `quick`、`standard` 與 `deep`。使用以下指令查看已解析的計畫：

```bash
ras-report plan reports/economy-deep-dive/manifest.yaml
```

編輯產生的 `manifest.yaml`、`sources.yaml` 與 Markdown 區塊，然後執行驗證、建置與品質檢查：

```bash
ras-report validate reports/my-report/manifest.yaml
ras-report build reports/my-report/manifest.yaml --formats docx,pdf,pptx
ras-report qa reports/my-report/manifest.yaml
```

DOCX 與 PDF 是核心輸出，可使用 Python 渲染附加功能。PPTX 是可選的可編輯伴侶，需要提供 Node.js 與 Artifact Tool 的支援主機環境。

### 輸出目標

| 格式 | 支援情況 | 執行環境 |
| --- | --- | --- |
| DOCX | 核心輸出 | Python 與 `python-docx` |
| PDF | 核心輸出 | Python 與 ReportLab |
| PPTX | 可選的可編輯伴侶 | 提供 Node.js 和 Artifact Tool 的支援主機 |

也可以從可重複使用的模板目錄建立更完整的專案：

```bash
ras-report template list
ras-report init reports/board-decision --template decision-memo \
  --request "Compare the options and recommend a path for the board"
```

使用以下指令探索視覺語言：

```bash
ras-report theme list
ras-report theme inspect data-forward
```

<details>
<summary><strong>報告專案包含什麼</strong></summary>

```text
reports/my-report/
├── manifest.yaml       # 請求、風格決策、區塊、輸出、QA 收據
├── sources.yaml        # 來源與聲明支援
├── blocks/*.md         # 獨立、可恢復的內容單位
├── assets/             # 提供或產生的視覺資產
├── build/              # 規範模型與中間視覺結果
├── qa/                 # 收據與渲染頁面圖像
└── dist/               # 最終 DOCX、PDF 與可選 PPTX
```

</details>

## RAS 可以製作什麼

RAS 適合需要結構、判斷與可追溯性的報告：

| 意圖 | 適用場景 |
| --- | --- |
| 執行摘要 | 管理階層摘要與簡潔檢視 |
| 決策備忘錄 | 方案、取捨、建議與後續行動 |
| 研究綜述 | 跨來源的證據型發現 |
| 深度分析 | 趨勢、原因、影響與解讀 |
| 比較評估 | 前後、方案、供應商或政策比較 |
| 提案與路線圖 | 商業論證、策略、計畫與里程碑 |
| KPI 與狀態檢視 | 指標、圖表、進度與營運節奏 |
| 稽核、風險與合規 | 控制措施、證據缺口、發現與緩解 |
| 技術報告 | 架構、系統、事故與調查 |
| SOP 與案例研究 | 可重複流程與記錄型案例 |

路由器提供 16 種報告原型；若請求已經明確指定形狀，顯式覆寫會優先採用。

### 可重複使用的模板

模板是一組可編輯、可恢復的區塊起始結構，而不是鎖定的版式：

| 模板族 | 包含形狀 |
| --- | --- |
| 決策與比較 | 決策備忘錄、比較評估、提案/商業論證 |
| 研究與分析 | 研究綜述、深度分析、調查/根本原因 |
| 營運節奏 | 狀態/進度、績效/KPI、策略路線圖 |
| 風險與保證 | 稽核評估、合規/風險、事故檢討 |
| 技術與程序 | 技術架構、政策/SOP、案例研究 |

使用 `ras-report template inspect <template>` 查看精確的區塊藍圖。

### 輕量內容規劃

每個新專案都會自動記錄內容計畫，包括目標頁數範圍、字數範圍、投影片目標與各節字數預算。「詳細分析」會選擇 deep，「簡潔簡報」會選擇 quick。主機可以據此擴展脈絡、證據、影響與限制，而不是填充無依據的內容。

## 運作方式

1. **路由請求：** 從請求解析原型、讀者、語氣、證據等級、頁面形狀、視覺風格、密度與強調方式；明確的使用者選擇優先。
2. **規劃內容：** 解析深度、目標頁數、章節預算與研究模式。外部研究需要明確的 `web` 模式或清楚的線上研究請求。
3. **建立獨立區塊：** 每個區塊都有穩定 ID、溝通目的、狀態、來源引用、版面預算與可選視覺契約。
4. **解析設計系統：** 在渲染前統一解析主題、品牌權杖、語義元件、字型、圖表調色盤、圖示語言、間距與頁面節奏。
5. **渲染與驗證：** DOCX 與 PDF 來自同一個規範模型；PPTX 讓圖表保持 PowerPoint 圖表、表格保持可編輯表格，並將來源與完整區塊文字保留在講者備註中。QA 會檢查結構、章節一致性、可存取性、PDF 可讀性與渲染頁面完整性。

## 設計系統

主題不只是色彩預設，也會改變階層、封面、語義面板、表格、圖表、圖示、字體、間距與構圖規則。

| 主題 | 個性 | 適用場景 |
| --- | --- | --- |
| `minimal` | 安靜、緊湊 | 短小、少裝飾的報告 |
| `editorial` | 溫暖、敘事化 | 執行摘要與故事型工作 |
| `data-forward` | 清晰、指標導向 | KPI、比較與儀表板 |
| `institutional` | 正式、結構化 | 政策、稽核與合規 |
| `technical` | 如藍圖般精確 | 架構與營運 |
| `narrative` | 富有表現力、節奏鮮明 | 案例研究與長篇綜合 |

專案級 `.ras/brand.yaml` 可以覆寫品牌顏色、字型、間距、元件權杖、圖表調色盤與圖示權杖。Markdown 的 **粗體**、*斜體* 與 `code` 會在請求的輸出格式中保持一致。

## 證據模型

使用者提供的資料是主要證據。只有在使用者要求或明確授權時才使用外部研究。來源台帳記錄出處：

```yaml
sources:
  - id: S1
    title: Official source title
    publisher: Publisher
    url: https://example.com/source
    publication_date: "2026-01-01"
```

區塊使用穩定標記引用來源：

```markdown
The supported finding is stated here [S1].
```

驗證器會檢查來源引用、聲明支援、必需視覺的說明文字與替代文字、不安全路徑，以及未解析的佔位符。

## 視覺與可存取性

圖表支援帶有標籤、數值、說明與替代文字的 `bar`、`line`、`pie` 規格。圖示使用輕量語義語法，產生原始 SVG 與 PNG 資產。資訊型視覺會包含可見說明文字、報告中的替代文字、DOCX 中的嵌入影像中繼資料，以及建置模型中的確定性資產。

## 範例與夾具

- [`examples/executive-brief`](examples/executive-brief) — 編輯風格的管理檢視
- [`examples/kpi-report`](examples/kpi-report) — 資料驅動的圖表報告
- [`examples/technical-report`](examples/technical-report) — 帶架構圖的技術報告
- [`examples/decision-memo`](examples/decision-memo) — 帶選項與建議的可重複模板
- [`examples/strategy-roadmap`](examples/strategy-roadmap) — 優先事項、里程碑與衡量指標
- [`examples/incident-postmortem`](examples/incident-postmortem) — 無責事故時間線與矯正措施
- [`fixtures/traditional-chinese`](fixtures/traditional-chinese) — CJK 渲染驗收夾具
- [`fixtures/insufficient-evidence`](fixtures/insufficient-evidence) — 證據不足行為夾具
- [`reports/covid-economy-comparison`](reports/covid-economy-comparison) — 有來源的全球前後比較專案

產生的 `build/`、`qa/` 與 `dist/` 目錄會被忽略，因此原始專案保持可審查且可重現。

## 開發

```bash
python -m unittest discover -s tests -v
```

完整驗收：

```bash
python -m unittest discover -s tests -v
ras-report validate examples/executive-brief/manifest.yaml
ras-report build examples/executive-brief/manifest.yaml --formats docx,pdf,pptx
ras-report qa examples/executive-brief/manifest.yaml
```

可選渲染相依套件在 [`pyproject.toml`](pyproject.toml) 中宣告：

```bash
python -m pip install -e ".[render]"
```

## 範圍

RAS v1 聚焦有證據依據的 DOCX 與 PDF 報告、可選的可編輯 PPTX 伴侶、可重複使用的模板與輕量內容規劃。Web 報告、試算表附錄與協作編輯流程仍不在目前渲染器契約內。

## 授權條款

請參閱 [`LICENSE`](LICENSE)。
