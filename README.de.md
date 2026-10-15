<div align="center">

<img src="assets/readme/ras-pipeline.svg" alt="RAS-Pipeline von Anfrage und Belegen bis zur Berichtsausgabe" width="100%">

# RAS — Report Anything Skill

### Aus einer Anfrage und ihren Belegen wird ein Bericht, den Menschen wirklich lesen möchten.

Sechs visuelle Themes · Sechzehn wiederverwendbare Vorlagen · DOCX + PDF + optionales editierbares PPTX aus einem kanonischen Modell

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

![Ausgaben](https://img.shields.io/badge/ausgaben-DOCX%20%2B%20PDF%20%2B%20optionales%20PPTX-117A8B?style=flat-square)
![Themes](https://img.shields.io/badge/themes-6-117A8B?style=flat-square)
![Tests](https://img.shields.io/badge/tests-19%20passing-027A48?style=flat-square)

</div>

## Warum RAS

Die meisten Automatisierungen für Berichte enden beim Text. RAS behandelt einen Bericht als gestaltetes, prüfbares Artefakt: Es wählt die passende Kommunikationsform, hält die Belegkette sichtbar, löst ein visuelles System auf, rendert DOCX und PDF aus demselben Modell, ergänzt optional ein editierbares PPTX und prüft die Ausgaben vor der Übergabe.

Fordere das Ergebnis in Alltagssprache an:

> „Vergleiche die Optionen für den Vorstand und empfehle einen Weg.“

> „Erstelle eine KPI-Prüfung mit einem klaren Trenddiagramm.“

> „Verwandle diese Recherche in eine evidenzbasierte Synthese.“

> „Erkläre den Vorfall, die Grundursache, die Auswirkungen und die Korrekturmaßnahmen.“

RAS macht daraus ein strukturiertes Projekt mit unabhängigen Markdown-Blöcken, Quellenregister, Visual-Vertrag und Qualitätsnachweis.

### Lokalisierte Dokumentation

Das Projekt ist auf [简体中文](README.zh-CN.md), [繁體中文](README.zh-TW.md), [日本語](README.ja.md), [한국어](README.ko.md), [Español](README.es.md), [Français](README.fr.md), [Deutsch](README.de.md), [Português (Brasil)](README.pt-BR.md) und [Русский](README.ru.md) verfügbar. RAS bewahrt Unicode-Text in Berichtblöcken und unterstützt konfigurierbare CJK-Ersatzschriften.

## RAS in Aktion

Die folgenden Vorschauen werden aus Beispielen und Akzeptanz-Fixtures dieses Repositories gerendert.

<table>
  <tr>
    <td width="50%"><img src="assets/readme/kpi-dashboard.png" alt="Datenorientierter KPI-Bericht mit Trenddiagramm"></td>
    <td width="50%"><img src="assets/readme/technical-blueprint.png" alt="Technischer Bericht mit eigenem Architekturdiagramm"></td>
  </tr>
  <tr>
    <td align="center"><sub>Datenorientierte KPI-Prüfung</sub></td>
    <td align="center"><sub>Technischer Architekturbericht</sub></td>
  </tr>
</table>

<table>
  <tr>
    <td width="50%"><img src="assets/readme/editorial-brief.png" alt="Redaktionelles Executive Briefing mit warmer Papierpalette"></td>
    <td width="50%"><img src="assets/readme/ras-growth-chart.png" alt="Globales Wachstumsvergleichsdiagramm in einem RAS-Bericht"></td>
  </tr>
  <tr>
    <td align="center"><sub>Redaktionelles Executive Briefing</sub></td>
    <td align="center"><sub>Analytischer Vergleich mit Diagramm</sub></td>
  </tr>
</table>

### Editierbare PPTX-Begleiter

Der Präsentations-Renderer überträgt dasselbe Berichtspaket in ein editierbares Breitbild-Deck. Diagramme bleiben native PowerPoint-Diagramme, das Quellenregister bleibt eine editierbare Tabelle, und vollständige Quellen sowie Blocktexte werden in den Sprechernotizen erhalten.

<table>
  <tr>
    <td width="33%"><img src="assets/readme/economy-deck-cover.png" alt="Editierbare PPTX-Titelfolie für den Weltwirtschaftsbericht"></td>
    <td width="33%"><img src="assets/readme/economy-deck-chart.png" alt="Folie mit nativem Wachstumsdiagramm"></td>
    <td width="33%"><img src="assets/readme/economy-deck-sources.png" alt="Editierbare Folie des Quellenregisters"></td>
  </tr>
  <tr>
    <td align="center"><sub>Deck-Cover</sub></td>
    <td align="center"><sub>Natives Diagramm</sub></td>
    <td align="center"><sub>Editierbares Quellenregister</sub></td>
  </tr>
</table>

## In Codex installieren

RAS wird als versioniertes Codex-Plugin verteilt. Füge den Marketplace für die stabile Version `v0.1.0` hinzu:

```bash
codex plugin marketplace add CharlesArea/ras --ref v0.1.0
codex plugin add ras@ras-marketplace
```

Starte danach einen neuen Codex-Chat und bitte um die Verwendung von `$ras`. Alternativ kannst du `codex` starten, `/plugins` ausführen, **RAS — Report Anything Skill** öffnen und **Install plugin** wählen. Folge anschließend der Einrichtung für die Python-Rendering-Umgebung.

```text
Use $ras to turn these notes into an evidence-grounded decision memo and
deliver DOCX, PDF, and an editable PPTX companion.
```

Codex installiert gemeinsam genutzte Skills derzeit mit `codex plugin add` und nicht mit `codex skill install`. Die obigen Befehle pinnen die getestete Version; lasse `--ref v0.1.0` weg, wenn du den neuesten Marketplace-Stand verwenden möchtest.

### Herunterladen oder manuell installieren

Lade den gepackten Quellcode aus den [GitHub Releases](https://github.com/CharlesArea/ras/releases/latest) herunter oder installiere dieselbe feste Version für die lokale Entwicklung:

```bash
git clone --branch v0.1.0 https://github.com/CharlesArea/ras.git
cd ras
python -m pip install -e ".[render]"
```

Python 3.11 oder neuer ist erforderlich. Das portable Plugin-Manifest ist [`plugin.json`](plugin.json), der Marketplace-Katalog befindet sich in [`marketplace.json`](.agents/plugins/marketplace.json), und kompatible Manifeste für [Codex](.codex-plugin/plugin.json) und [Claude](.claude-plugin/plugin.json) sind enthalten.

## Schnellstart

Initialisiere ein Berichtprojekt:

```bash
ras-report init reports/my-report \
  --request "Create an evidence-grounded decision memo from these notes" \
  --archetype decision-memo
```

Die Tiefe wird aus der Alltagssprache abgeleitet. Du kannst Tiefe, Recherchemodus und Seitenzahl überschreiben:

```bash
ras-report init reports/economy-deep-dive \
  --request "Create a detailed comparison of the economy before and after COVID" \
  --depth deep --research web --pages 15
```

Die Profile heißen `quick`, `standard` und `deep`. Den aufgelösten Plan kannst du jederzeit anzeigen:

```bash
ras-report plan reports/economy-deep-dive/manifest.yaml
```

Bearbeite `manifest.yaml`, `sources.yaml` und die Markdown-Blöcke, und führe danach Validierung, Build und QA aus:

```bash
ras-report validate reports/my-report/manifest.yaml
ras-report build reports/my-report/manifest.yaml --formats docx,pdf,pptx
ras-report qa reports/my-report/manifest.yaml
```

DOCX und PDF sind die Kernformate. PPTX ist ein optionaler editierbarer Begleiter und benötigt die Node.js- und Artifact-Tool-Umgebung des Hosts.

### Ausgabeformate

| Format | Unterstützung | Laufzeit |
| --- | --- | --- |
| DOCX | Kernformat | Python mit `python-docx` |
| PDF | Kernformat | Python mit ReportLab |
| PPTX | Optionaler editierbarer Begleiter | Node.js des Hosts und Artifact Tool |

### Inhalt eines Berichtprojekts

```text
reports/my-report/
├── manifest.yaml       # Anfrage, Stil, Blöcke, Ausgaben und QA-Nachweis
├── sources.yaml        # Herkunft und Beleg für Aussagen
├── blocks/*.md         # unabhängige, fortsetzbare Inhaltseinheiten
├── assets/             # bereitgestellte oder erzeugte Visuals
├── build/              # kanonisches Modell und Zwischenvisuals
├── qa/                 # Nachweise und gerenderte Seitenbilder
└── dist/               # finale DOCX-, PDF- und optionale PPTX-Ausgaben
```

## Was RAS erstellt

RAS unterstützt Berichte, die Struktur, Urteil und Nachvollziehbarkeit benötigen:

| Zweck | Geeignet für |
| --- | --- |
| Executive Brief | Management-Zusammenfassungen und kurze Reviews |
| Entscheidungsvorlage | Optionen, Abwägungen, Empfehlungen und nächste Schritte |
| Research-Synthese | Evidenzbasierte Ergebnisse aus mehreren Quellen |
| Tiefenanalyse | Trends, Ursachen, Auswirkungen und Interpretation |
| Vergleichsbewertung | Vorher/Nachher-, Options-, Anbieter- oder Politikvergleich |
| Vorschlag und Roadmap | Business Cases, Strategien, Pläne und Meilensteine |
| KPI- und Statusbericht | Kennzahlen, Diagramme, Fortschritt und Betriebsrhythmus |
| Audit, Risiko und Compliance | Kontrollen, Evidenzlücken, Befunde und Maßnahmen |
| Technischer Bericht | Architektur, Systeme, Vorfälle und Untersuchungen |
| SOP und Fallstudie | Wiederholbare Verfahren und dokumentierte Beispiele |

Der Router bietet sechzehn Archetypen; explizite Vorgaben der Anfrage haben Vorrang.

### Wiederverwendbare Vorlagen

Vorlagen sind editierbare, fortsetzbare Block-Sets und keine festgeschriebenen Layouts:

| Vorlagenfamilie | Enthaltene Formen |
| --- | --- |
| Entscheidung und Vergleich | Entscheidungsvorlage, Vergleichsbewertung, Vorschlag/Business Case |
| Recherche und Analyse | Research-Synthese, Tiefenanalyse, Untersuchung/Ursachenanalyse |
| Betriebsrhythmus | Status/Fortschritt, KPI, Strategie-Roadmap |
| Risiko und Assurance | Audit, Compliance/Risiko, Incident-Postmortem |
| Technik und Verfahren | Technische Architektur, Policy/SOP, Fallstudie |

Das genaue Block-Blueprint zeigt `ras-report template inspect <template>`.

### Leichte Inhaltsplanung

Jedes neue Paket speichert automatisch einen Inhaltsplan mit Seiten- und Wortbereich, Folienziel und Wortbudget je Abschnitt. „Detaillierte Analyse“ wählt deep, „kurzes Briefing“ wählt quick. So können Kontext, Belege, Folgen und Grenzen erweitert werden, ohne unbelegte Fülltexte zu erzeugen.

## Funktionsweise

1. **Anfrage routen:** Archetyp, Zielgruppe, Ton, Evidenzniveau, Seitengröße, visueller Stil, Dichte und Schwerpunkt werden aufgelöst.
2. **Inhalt planen:** Tiefe, Zielseiten, Abschnittsbudgets und Recherchmodus werden bestimmt. Externe Recherche benötigt `web` oder eine klare Anforderung.
3. **Unabhängige Blöcke bauen:** Jeder Block hat eine stabile ID, ein Kommunikationsziel, Status, Quellen, Layoutbudget und optionalen Visual-Vertrag.
4. **Ein Designsystem auflösen:** Theme, Markentokens, Komponenten, Typografie, Diagrammpalette, Diagrammsprache, Abstände und Seitenrhythmus werden vor dem Rendern festgelegt.
5. **Rendern und prüfen:** DOCX und PDF entstehen aus demselben Modell; PPTX behält native Diagramme, editierbare Tabellen und Quellen in Sprechernotizen. QA prüft Struktur, Abschnittsparität, Barrierefreiheit, Lesbarkeit und Seitenintegrität.

## Designsystem

Themes ändern Hierarchie, Cover, semantische Panels, Tabellen, Diagramme, Typografie, Abstände und Komposition – nicht nur Farben.

| Theme | Charakter | Am besten für |
| --- | --- | --- |
| `minimal` | Ruhig und kompakt | Kurze, zurückhaltende Berichte |
| `editorial` | Warm und narrativ | Executive Briefs und Storytelling |
| `data-forward` | Klar und kennzahlenorientiert | KPIs, Vergleiche und Dashboards |
| `institutional` | Formal und strukturiert | Politik, Audit und Compliance |
| `technical` | Präzise wie ein Blueprint | Architektur und Betrieb |
| `narrative` | Ausdrucksstark und rhythmisch | Fallstudien und lange Synthesen |

`.ras/brand.yaml` kann Farben, Schriften, Abstände, Komponenten-, Diagramm- und Chart-Tokens überschreiben. Markdown unterstützt **fett**, *kursiv* und `code` konsistent.

## Evidenzmodell

Vom Nutzer bereitgestelltes Material ist die primäre Evidenz. Externe Recherche wird nur auf Anfrage oder mit klarer Autorisierung verwendet. Das Quellenregister speichert die Herkunft; Blöcke zitieren mit stabilen Markern wie `[S1]`.

```yaml
sources:
  - id: S1
    title: Official source title
    publisher: Publisher
    url: https://example.com/source
    publication_date: "2026-01-01"
```

Die Validierung prüft Quellenverweise, Beleg für Aussagen, Captions und Alternativtexte, sichere Pfade und ungelöste Platzhalter.

## Visuals und Barrierefreiheit

Diagramme akzeptieren `bar`-, `line`- und `pie`-Spezifikationen mit Labels, Werten, Captions und Alternativtext. Diagramme nutzen eine kleine semantische Grammatik und erzeugen originale SVG- und PNG-Assets. Informative Visuals erhalten sichtbare Captions, Alternativtext, Bildmetadaten in DOCX und ein deterministisches Build-Asset.

## Beispiele und Fixtures

- [`examples/executive-brief`](examples/executive-brief) — redaktionelle Management-Review
- [`examples/kpi-report`](examples/kpi-report) — datenorientierter Diagrammbericht
- [`examples/technical-report`](examples/technical-report) — technischer Bericht mit Diagramm
- [`examples/decision-memo`](examples/decision-memo) — Vorlage mit Optionen und Empfehlung
- [`examples/strategy-roadmap`](examples/strategy-roadmap) — Prioritäten, Meilensteine und Messgrößen
- [`examples/incident-postmortem`](examples/incident-postmortem) — blameless Zeitlinie und Korrekturmaßnahmen
- [`fixtures/traditional-chinese`](fixtures/traditional-chinese) — CJK-Rendering-Akzeptanz-Fixture
- [`fixtures/insufficient-evidence`](fixtures/insufficient-evidence) — Fixture für Evidenzlücken
- [`reports/covid-economy-comparison`](reports/covid-economy-comparison) — quellenbasierter globaler Vergleich

Generierte `build/`, `qa/` und `dist/`-Verzeichnisse werden ignoriert, damit Quellpakete prüfbar und reproduzierbar bleiben.

## Entwicklung

```bash
python -m unittest discover -s tests -v
```

Vollständiger Akzeptanzlauf:

```bash
python -m unittest discover -s tests -v
ras-report validate examples/executive-brief/manifest.yaml
ras-report build examples/executive-brief/manifest.yaml --formats docx,pdf,pptx
ras-report qa examples/executive-brief/manifest.yaml
```

Optionale Rendering-Abhängigkeiten sind in [`pyproject.toml`](pyproject.toml) definiert:

```bash
python -m pip install -e ".[render]"
```

## Umfang

RAS v1 konzentriert sich auf evidenzbasierte DOCX- und PDF-Berichte, optionale editierbare PPTX-Begleiter, wiederverwendbare Vorlagen und leichte Inhaltsplanung. Webberichte, Tabellenanhänge und kollaborative Bearbeitung liegen außerhalb des aktuellen Renderer-Vertrags.

## Lizenz

Siehe [`LICENSE`](LICENSE).
