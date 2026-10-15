<div align="center">

<img src="assets/readme/ras-pipeline.svg" alt="요청과 근거에서 보고서 출력까지 이어지는 RAS 파이프라인" width="100%">

# RAS — Report Anything Skill

### 요청과 근거를 사람들이 실제로 읽고 싶은 보고서로 바꿉니다.

6개 시각 테마 · 16개 재사용 가능한 템플릿 · 하나의 정규 모델에서 DOCX + PDF + 선택 가능한 편집형 PPTX 생성

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

![출력](https://img.shields.io/badge/출력-DOCX%20%2B%20PDF%20%2B%20선택적%20PPTX-117A8B?style=flat-square)
![테마](https://img.shields.io/badge/테마-6-117A8B?style=flat-square)
![테스트](https://img.shields.io/badge/테스트-19%20passing-027A48?style=flat-square)

</div>

## RAS란 무엇인가요?

대부분의 보고서 자동화는 텍스트에서 끝납니다. RAS는 보고서를 설계되고 감사 가능한 결과물로 다룹니다. 적합한 커뮤니케이션 형태를 선택하고, 근거의 흐름을 보존하고, 시각 시스템을 결정하고, 하나의 정규 모델에서 DOCX와 PDF를 렌더링하며, 선택적으로 편집 가능한 PPTX를 추가하고, 전달 전에 결과를 검사합니다.

자연어로 결과를 요청할 수 있습니다.

> “이 선택지들을 비교하고 이사회에 경로를 추천해 줘.”

> “명확한 추세 차트가 포함된 KPI 리뷰를 만들어 줘.”

> “이 연구를 근거 기반 종합 보고서로 바꿔 줘.”

> “사고, 근본 원인, 영향, 시정 조치를 설명해 줘.”

RAS는 요청을 독립적인 Markdown 블록, 출처 원장, 시각 계약, 품질 영수증을 갖춘 구조화된 프로젝트로 바꿉니다.

### 다국어 문서

[简体中文](README.zh-CN.md), [繁體中文](README.zh-TW.md), [日本語](README.ja.md), [한국어](README.ko.md), [Español](README.es.md), [Français](README.fr.md), [Deutsch](README.de.md), [Português (Brasil)](README.pt-BR.md), [Русский](README.ru.md)로 프로젝트를 읽을 수 있습니다. RAS는 보고서 블록의 Unicode 텍스트를 보존하고 현지화된 보고서 출력에 사용할 CJK 대체 글꼴도 설정할 수 있습니다.

## 실제 예시

아래 미리보기는 저장소의 예제와 승인 테스트 픽스처에서 렌더링된 결과입니다.

<table>
  <tr>
    <td width="50%"><img src="assets/readme/kpi-dashboard.png" alt="추세 차트가 있는 데이터 중심 KPI 보고서"></td>
    <td width="50%"><img src="assets/readme/technical-blueprint.png" alt="독창적인 아키텍처 다이어그램이 있는 기술 보고서"></td>
  </tr>
  <tr>
    <td align="center"><sub>데이터 중심 KPI 리뷰</sub></td>
    <td align="center"><sub>기술 아키텍처 보고서</sub></td>
  </tr>
</table>

<table>
  <tr>
    <td width="50%"><img src="assets/readme/editorial-brief.png" alt="따뜻한 종이 색상의 에디토리얼 임원 브리프"></td>
    <td width="50%"><img src="assets/readme/ras-growth-chart.png" alt="RAS 보고서의 글로벌 성장 비교 차트"></td>
  </tr>
  <tr>
    <td align="center"><sub>에디토리얼 임원 브리프</sub></td>
    <td align="center"><sub>차트가 있는 분석 비교</sub></td>
  </tr>
</table>

### 편집 가능한 PPTX 동반 파일

프레젠테이션 렌더러는 같은 보고서 패키지를 와이드 화면의 편집 가능한 덱으로 변환합니다. 차트는 네이티브 PowerPoint 차트로 유지되고, 출처 원장은 편집 가능한 표로 유지되며, 전체 출처와 블록 텍스트는 발표자 노트에 보존됩니다.

<table>
  <tr>
    <td width="33%"><img src="assets/readme/economy-deck-cover.png" alt="세계 경제 보고서의 편집 가능한 PPTX 표지"></td>
    <td width="33%"><img src="assets/readme/economy-deck-chart.png" alt="네이티브 성장 차트 슬라이드"></td>
    <td width="33%"><img src="assets/readme/economy-deck-sources.png" alt="편집 가능한 출처 원장 슬라이드"></td>
  </tr>
  <tr>
    <td align="center"><sub>덱 표지</sub></td>
    <td align="center"><sub>네이티브 차트</sub></td>
    <td align="center"><sub>편집 가능한 출처 원장</sub></td>
  </tr>
</table>

## Codex에 설치

RAS는 버전이 지정된 Codex 플러그인으로 배포됩니다. 안정 버전 `v0.1.0`의 마켓플레이스를 추가하세요.

```bash
codex plugin marketplace add CharlesArea/ras --ref v0.1.0
codex plugin add ras@ras-marketplace
```

그 다음 새 Codex 채팅을 시작하고 `$ras`를 사용해 달라고 요청하세요. 플러그인 브라우저를 사용하려면 `codex`를 시작하고 `/plugins`를 실행한 뒤 **RAS — Report Anything Skill**을 열고 **Install plugin**을 선택하세요. 설정 안내에 따라 Python 렌더링 환경을 설치합니다.

```text
Use $ras to turn these notes into an evidence-grounded decision memo and
deliver DOCX, PDF, and an editable PPTX companion.
```

현재 Codex는 공유 스킬을 `codex skill install`이 아니라 `codex plugin add`로 설치합니다. 위 명령은 테스트된 릴리스를 고정합니다. 기본 브랜치의 최신 마켓플레이스 상태를 사용하려면 `--ref v0.1.0`을 생략하세요.

### 다운로드 또는 수동 설치

[GitHub Releases](https://github.com/CharlesArea/ras/releases/latest)에서 패키지 소스를 다운로드하거나 로컬 개발을 위해 같은 버전을 설치하세요.

```bash
git clone --branch v0.1.0 https://github.com/CharlesArea/ras.git
cd ras
python -m pip install -e ".[render]"
```

Python 3.11 이상이 필요합니다. 포터블 플러그인 매니페스트는 [`plugin.json`](plugin.json), 마켓플레이스 카탈로그는 [`marketplace.json`](.agents/plugins/marketplace.json)에 있으며 [Codex](.codex-plugin/plugin.json) 및 [Claude](.claude-plugin/plugin.json) 호환 매니페스트도 포함됩니다.

## 빠른 시작

보고서 프로젝트를 초기화합니다.

```bash
ras-report init reports/my-report \
  --request "Create an evidence-grounded decision memo from these notes" \
  --archetype decision-memo
```

일반 문장에서 깊이를 추론하며 깊이, 조사 모드, 페이지 수를 지정할 수도 있습니다.

```bash
ras-report init reports/economy-deep-dive \
  --request "Create a detailed comparison of the economy before and after COVID" \
  --depth deep --research web --pages 15
```

사용 가능한 프로필은 `quick`, `standard`, `deep`입니다. 다음 명령으로 해석된 계획을 확인하세요.

```bash
ras-report plan reports/economy-deep-dive/manifest.yaml
```

생성된 `manifest.yaml`, `sources.yaml`, Markdown 블록을 편집한 뒤 검증, 빌드, QA를 실행합니다.

```bash
ras-report validate reports/my-report/manifest.yaml
ras-report build reports/my-report/manifest.yaml --formats docx,pdf,pptx
ras-report qa reports/my-report/manifest.yaml
```

DOCX와 PDF는 핵심 출력입니다. PPTX는 호스트의 Node.js와 Artifact Tool 환경이 있을 때 생성되는 선택 가능한 편집형 동반 파일입니다.

### 출력 대상

| 형식 | 지원 | 런타임 |
| --- | --- | --- |
| DOCX | 핵심 출력 | Python 및 `python-docx` |
| PDF | 핵심 출력 | Python 및 ReportLab |
| PPTX | 선택 가능한 편집형 동반 파일 | 호스트 Node.js 및 Artifact Tool |

### 보고서 프로젝트 구조

```text
reports/my-report/
├── manifest.yaml       # 요청, 스타일, 블록, 출력, QA 영수증
├── sources.yaml        # 출처와 주장 근거
├── blocks/*.md         # 독립적으로 재개할 수 있는 콘텐츠 단위
├── assets/             # 제공되거나 생성된 시각 자료
├── build/              # 정규 모델과 중간 시각 자료
├── qa/                 # 영수증과 렌더링된 페이지 이미지
└── dist/               # 최종 DOCX, PDF, 선택적 PPTX
```

## 무엇을 만들 수 있나요?

RAS는 구조, 판단, 추적 가능성이 필요한 보고서를 지원합니다.

| 목적 | 활용 예 |
| --- | --- |
| 임원 브리프 | 경영진 요약과 간결한 리뷰 |
| 의사결정 메모 | 선택지, 절충, 추천, 다음 단계 |
| 연구 종합 | 여러 출처를 가로지르는 근거 기반 발견 |
| 심층 분석 | 추세, 원인, 영향, 해석 |
| 비교 평가 | 전후, 선택지, 공급업체, 정책 비교 |
| 제안 및 로드맵 | 비즈니스 케이스, 전략, 계획, 마일스톤 |
| KPI 및 상태 리뷰 | 지표, 차트, 진척, 운영 주기 |
| 감사, 위험, 규정 준수 | 통제, 근거 공백, 발견, 완화책 |
| 기술 보고서 | 아키텍처, 시스템, 사고, 조사 |
| SOP 및 사례 연구 | 반복 가능한 절차와 기록된 사례 |

라우터에는 16개의 아키타입이 있으며 요청에 형식이 명시되면 명시적 설정이 우선합니다.

### 재사용 가능한 템플릿

템플릿은 고정된 레이아웃이 아니라 편집하고 다시 시작할 수 있는 블록 구조입니다.

| 템플릿군 | 포함된 형태 |
| --- | --- |
| 의사결정과 비교 | 의사결정 메모, 비교 평가, 제안/비즈니스 케이스 |
| 연구와 분석 | 연구 종합, 심층 분석, 조사/근본 원인 |
| 운영 주기 | 상태/진척, 성과/KPI, 전략 로드맵 |
| 위험과 보증 | 감사 평가, 규정 준수/위험, 사고 회고 |
| 기술과 절차 | 기술 아키텍처, 정책/SOP, 사례 연구 |

정확한 블록 설계는 `ras-report template inspect <template>`으로 확인하세요.

### 가벼운 콘텐츠 계획

새 패키지는 목표 페이지 범위, 단어 범위, 슬라이드 목표, 섹션별 단어 예산을 자동으로 기록합니다. “상세 분석”은 deep, “간결한 브리프”는 quick을 선택합니다. 이를 통해 근거 없는 분량 늘리기 없이 맥락, 근거, 시사점, 한계를 확장할 수 있습니다.

## 작동 방식

1. **요청 라우팅:** 아키타입, 대상 독자, 어조, 근거 수준, 페이지 형태, 시각 스타일, 밀도, 강조를 해결합니다.
2. **콘텐츠 계획:** 깊이, 목표 페이지, 섹션 예산, 조사 모드를 해결합니다. 외부 조사는 `web` 모드나 명확한 요청이 필요합니다.
3. **독립 블록 구축:** 각 블록은 안정적인 ID, 커뮤니케이션 목표, 상태, 출처, 레이아웃 예산, 선택적 시각 계약을 갖습니다.
4. **하나의 디자인 시스템 해결:** 테마, 브랜드 토큰, 의미 컴포넌트, 타이포그래피, 차트 팔레트, 다이어그램 언어, 간격, 페이지 리듬을 렌더링 전에 결정합니다.
5. **렌더링 및 검증:** DOCX와 PDF는 동일한 정규 모델에서 생성되고 PPTX는 네이티브 차트, 편집 가능한 표, 발표자 노트의 출처를 보존합니다. QA는 구조, 섹션 일치, 접근성, PDF 가독성, 페이지 무결성을 검사합니다.

## 디자인 시스템

테마는 색상만 바꾸지 않습니다. 계층, 표지, 의미 패널, 표, 차트, 다이어그램, 글꼴, 간격, 구성 규칙을 바꿉니다.

| 테마 | 성격 | 적합한 용도 |
| --- | --- | --- |
| `minimal` | 조용하고 간결함 | 짧고 장식이 적은 보고서 |
| `editorial` | 따뜻하고 서사적임 | 임원 브리프와 스토리 중심 작업 |
| `data-forward` | 선명하고 지표 중심 | KPI, 비교, 대시보드 |
| `institutional` | 공식적이고 구조적 | 정책, 감사, 규정 준수 |
| `technical` | 청사진처럼 정확함 | 아키텍처와 운영 |
| `narrative` | 표현력 있고 리듬감 있음 | 사례 연구와 장문 종합 |

프로젝트의 `.ras/brand.yaml`로 브랜드 색상, 글꼴, 간격, 컴포넌트 토큰, 차트 팔레트, 다이어그램 토큰을 덮어쓸 수 있습니다. Markdown의 **굵게**, *기울임*, `code` 서식은 출력 형식 간에 일관되게 지원됩니다.

## 근거 모델

사용자가 제공한 자료가 주요 근거입니다. 외부 조사는 사용자가 요청하거나 명확히 승인한 경우에만 사용합니다. 출처 원장은 출처를 기록하고 블록은 `[S1]`과 같은 안정적인 마커로 인용합니다. 검증은 출처 참조, 주장 근거, 시각 자료의 캡션과 대체 텍스트, 안전한 경로, 해결되지 않은 플레이스홀더를 검사합니다.

## 시각 자료와 접근성

차트는 레이블, 값, 캡션, 대체 텍스트가 포함된 `bar`, `line`, `pie` 사양을 지원합니다. 다이어그램은 작은 의미론적 문법을 사용해 SVG와 PNG 자산으로 렌더링됩니다. 정보성 시각 자료에는 보이는 캡션, 대체 텍스트, DOCX 이미지 메타데이터, 빌드 모델의 결정적 자산이 포함됩니다.

## 예제와 픽스처

- [`examples/executive-brief`](examples/executive-brief) — 에디토리얼 경영진 리뷰
- [`examples/kpi-report`](examples/kpi-report) — 데이터 중심 차트 보고서
- [`examples/technical-report`](examples/technical-report) — 다이어그램이 있는 기술 보고서
- [`examples/decision-memo`](examples/decision-memo) — 선택지와 추천이 있는 템플릿
- [`examples/strategy-roadmap`](examples/strategy-roadmap) — 우선순위, 마일스톤, 측정 기준
- [`examples/incident-postmortem`](examples/incident-postmortem) — 비난 없는 사고 타임라인과 시정 조치
- [`fixtures/traditional-chinese`](fixtures/traditional-chinese) — CJK 렌더링 승인 픽스처
- [`fixtures/insufficient-evidence`](fixtures/insufficient-evidence) — 근거 부족 동작 픽스처
- [`reports/covid-economy-comparison`](reports/covid-economy-comparison) — 출처가 있는 글로벌 비교 패키지

생성된 `build/`, `qa/`, `dist/` 디렉터리는 무시되어 소스 패키지를 검토 가능하고 재현 가능하게 유지합니다.

## 개발

```bash
python -m unittest discover -s tests -v
```

전체 승인 테스트:

```bash
python -m unittest discover -s tests -v
ras-report validate examples/executive-brief/manifest.yaml
ras-report build examples/executive-brief/manifest.yaml --formats docx,pdf,pptx
ras-report qa examples/executive-brief/manifest.yaml
```

선택적 렌더링 의존성은 [`pyproject.toml`](pyproject.toml)에 선언되어 있습니다.

```bash
python -m pip install -e ".[render]"
```

## 범위

RAS v1은 근거 기반 DOCX 및 PDF 보고서, 선택적 편집형 PPTX 동반 파일, 재사용 가능한 템플릿, 가벼운 콘텐츠 계획에 집중합니다. 웹 보고서, 스프레드시트 부록, 협업 편집 워크플로는 현재 렌더러 계약의 범위 밖입니다.

## 라이선스

[`LICENSE`](LICENSE)를 참조하세요.
