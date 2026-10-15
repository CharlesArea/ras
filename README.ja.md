<div align="center">

<img src="assets/readme/ras-pipeline.svg" alt="リクエストと根拠からレポート出力までの RAS フロー" width="920">

# RAS — Report Anything Skill

### リクエストと根拠を、読まれるレポートに変換します。

6 つのビジュアルテーマ · 16 個の再利用可能なテンプレート · 1 つの正規モデルから DOCX、PDF、オプションの編集可能な PPTX を生成

[English](README.md) ·
<a href="README.zh-CN.md">简体中文</a> ·
<a href="README.zh-TW.md">繁體中文</a> ·
<a href="README.ja.md">日本語</a>

![出力](https://img.shields.io/badge/出力-DOCX%20%2B%20PDF%20%2B%20optional%20PPTX-117A8B?style=flat-square)
![テーマ](https://img.shields.io/badge/テーマ-6-117A8B?style=flat-square)
![テスト](https://img.shields.io/badge/テスト-19%20passing-027A48?style=flat-square)

</div>

## RAS とは

RAS はユーザーのリクエストと利用可能な根拠資料を構造化されたレポートプロジェクトに変換します。目的に合うレポートの形を選び、出典と引用関係を保持し、ビジュアルテーマを解決してから、納品前に出力を検証します。

DOCX と PDF がコア出力です。ホストに Node.js と Artifact Tool の実行環境がある場合は、編集可能な PPTX のプレゼンテーション版も生成できます。

## 主な機能

- 16 種類のレポート形式：エグゼクティブブリーフ、意思決定メモ、調査統合、詳細分析、比較評価、ビジネスケース、ロードマップ、KPI、監査、リスク、技術レポート、インシデントレビュー、SOP など。
- 6 つのビジュアルテーマ：`minimal`、`editorial`、`data-forward`、`institutional`、`technical`、`narrative`。
- 自動コンテンツ計画：リクエストから `quick`、`standard`、`deep` を推定し、各セクションのページ数、語数、スライド数の目標を作成します。
- 根拠モデル：出典台帳、主張レコード、安定した引用マーカー、前提、制限事項、根拠の不足を管理します。
- 複数形式のレンダリング：DOCX、PDF、オプションの編集可能な PPTX。PPTX のチャートと表はネイティブ編集可能なまま保持されます。

## 出力形式

| 形式 | サポート | 実行環境 |
| --- | --- | --- |
| DOCX | コア出力 | Python と `python-docx` |
| PDF | コア出力 | Python と ReportLab |
| PPTX | オプションの編集可能なコンパニオン | ホストの Node.js と Artifact Tool |

## インストール

```bash
git clone https://github.com/CharlesArea/ras.git
cd ras
python -m pip install -e ".[render]"
```

ホスト向けスキルの説明は [`skills/ras/SKILL.md`](skills/ras/SKILL.md) にあります。Codex と Claude のプラグイン定義は [`.codex-plugin`](.codex-plugin/plugin.json) と [`.claude-plugin`](.claude-plugin/plugin.json) にあります。

## クイックスタート

レポートプロジェクトを初期化します。

```bash
ras-report init reports/my-report \
  --request "Create an evidence-grounded decision memo from these notes" \
  --archetype decision-memo
```

通常の文章からコンテンツの深さを推定できます。

```bash
ras-report init reports/economy-deep-dive \
  --request "Create a detailed comparison of the economy before and after COVID" \
  --depth deep --research web --pages 15
```

利用できる深さは `quick`、`standard`、`deep` です。解決された計画は次のコマンドで確認できます。

```bash
ras-report plan reports/economy-deep-dive/manifest.yaml
```

生成された `manifest.yaml`、`sources.yaml`、Markdown セクションを編集してから、次を実行します。

```bash
ras-report validate reports/my-report/manifest.yaml
ras-report build reports/my-report/manifest.yaml --formats docx,pdf,pptx
ras-report qa reports/my-report/manifest.yaml
```

既定のリサーチモードは、ユーザーが提供した資料を使います。外部リサーチは `--research web` を明示するか、リクエストでオンライン調査を明確に依頼した場合だけ許可されます。

## 再利用可能なテンプレート

テンプレートは固定レイアウトではなく、編集と再開ができるセクション構成の出発点です。

```bash
ras-report template list
ras-report init reports/board-decision --template decision-memo \
  --request "Compare the options and recommend a path for the board"
```

`ras-report template inspect <template>` で具体的なセクション構成を確認できます。

## サンプルとショーケース

リポジトリには、意思決定メモ、戦略ロードマップ、インシデントレビュー、KPI レポート、技術アーキテクチャレポートのサンプルがあります。完全な DOCX/PDF/PPTX のショーケース画像は英語版 README に掲載しています。

- [`examples/decision-memo`](examples/decision-memo)
- [`examples/strategy-roadmap`](examples/strategy-roadmap)
- [`examples/incident-postmortem`](examples/incident-postmortem)
- [`reports/covid-economy-comparison`](reports/covid-economy-comparison)

## 根拠と品質

ユーザーが提供した資料を主な根拠として扱います。各出典には `sources.yaml` で安定した ID を付け、レポート内では `[S1]` などのマーカーで引用します。RAS は出典参照、主張の根拠、未解決プレースホルダー、ビジュアルのキャプション、代替テキスト、安全なパス、形式間のセクション一致を検証します。

## 開発

```bash
python -m unittest discover -s tests -v
python -m pip install -e ".[render]"
```

現在のスコープは、根拠に基づく DOCX/PDF レポート、オプションの編集可能な PPTX、再利用可能なテンプレート、軽量なコンテンツ計画です。Web レポート、スプレッドシート付録、共同編集は現在のレンダラーの対象外です。

## ライセンス

[`LICENSE`](LICENSE) を参照してください。
