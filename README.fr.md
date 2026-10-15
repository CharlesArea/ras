<div align="center">

<img src="assets/readme/ras-pipeline.svg" alt="Pipeline RAS, de la demande et des preuves au rapport" width="100%">

# RAS — Report Anything Skill

### Transformez une demande et ses preuves en un rapport que l’on a vraiment envie de lire.

Six thèmes visuels · Seize modèles réutilisables · DOCX + PDF + PPTX éditable optionnel à partir d’un modèle canonique

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

![Sorties](https://img.shields.io/badge/sorties-DOCX%20%2B%20PDF%20%2B%20PPTX%20optionnel-117A8B?style=flat-square)
![Thèmes](https://img.shields.io/badge/thèmes-6-117A8B?style=flat-square)
![Tests](https://img.shields.io/badge/tests-19%20passing-027A48?style=flat-square)

</div>

## Pourquoi RAS

La plupart des automatisations de rapports s’arrêtent au texte. RAS considère le rapport comme un artefact conçu et auditable : il choisit la forme de communication, conserve la traçabilité des preuves, résout un système visuel, produit DOCX et PDF depuis le même modèle canonique, ajoute éventuellement un PPTX éditable et vérifie les sorties avant livraison.

Décrivez le résultat en langage naturel :

> « Compare les options pour le conseil d’administration et recommande une voie. »

> « Crée une revue KPI avec un graphique de tendance clair. »

> « Transforme cette recherche en synthèse fondée sur des preuves. »

> « Explique l’incident, sa cause racine, son impact et les actions correctives. »

RAS transforme la demande en projet structuré avec des blocs Markdown indépendants, un registre des sources, un contrat visuel et un reçu qualité.

### Documentation localisée

Consultez le projet en [简体中文](README.zh-CN.md), [繁體中文](README.zh-TW.md), [日本語](README.ja.md), [한국어](README.ko.md), [Español](README.es.md), [Français](README.fr.md), [Deutsch](README.de.md), [Português (Brasil)](README.pt-BR.md) ou [Русский](README.ru.md). RAS conserve aussi le texte Unicode dans les blocs et prend en charge des polices CJK de repli configurables.

## Voir RAS en action

Ces aperçus sont générés à partir des exemples et fixtures d’acceptation du dépôt.

<table>
  <tr>
    <td width="50%"><img src="assets/readme/kpi-dashboard.png" alt="Rapport KPI orienté données avec graphique de tendance"></td>
    <td width="50%"><img src="assets/readme/technical-blueprint.png" alt="Rapport technique avec diagramme d’architecture original"></td>
  </tr>
  <tr>
    <td align="center"><sub>Revue KPI orientée données</sub></td>
    <td align="center"><sub>Rapport d’architecture technique</sub></td>
  </tr>
</table>

<table>
  <tr>
    <td width="50%"><img src="assets/readme/editorial-brief.png" alt="Brief exécutif éditorial avec palette papier chaleureuse"></td>
    <td width="50%"><img src="assets/readme/ras-growth-chart.png" alt="Graphique de comparaison de la croissance mondiale dans un rapport RAS"></td>
  </tr>
  <tr>
    <td align="center"><sub>Brief exécutif éditorial</sub></td>
    <td align="center"><sub>Comparaison analytique avec graphique</sub></td>
  </tr>
</table>

### Compagnons PPTX éditables

Le moteur de présentation adapte le même paquet de rapport en diaporama grand écran éditable. Les graphiques restent des graphiques PowerPoint natifs, le registre des sources reste un tableau éditable et les références complètes ainsi que le texte des blocs sont conservés dans les notes du présentateur.

<table>
  <tr>
    <td width="33%"><img src="assets/readme/economy-deck-cover.png" alt="Couverture PPTX éditable du rapport sur l’économie mondiale"></td>
    <td width="33%"><img src="assets/readme/economy-deck-chart.png" alt="Diapositive avec graphique de croissance natif"></td>
    <td width="33%"><img src="assets/readme/economy-deck-sources.png" alt="Diapositive éditable du registre des sources"></td>
  </tr>
  <tr>
    <td align="center"><sub>Couverture</sub></td>
    <td align="center"><sub>Graphique natif</sub></td>
    <td align="center"><sub>Registre éditable</sub></td>
  </tr>
</table>

## Installer dans Codex

RAS est distribué comme plugin Codex versionné. Ajoutez le marketplace de la version stable `v0.1.0` :

```bash
codex plugin marketplace add CharlesArea/ras --ref v0.1.0
codex plugin add ras@ras-marketplace
```

Commencez ensuite une nouvelle conversation Codex et demandez l’utilisation de `$ras`. Vous pouvez aussi lancer `codex`, exécuter `/plugins`, ouvrir **RAS — Report Anything Skill** et choisir **Install plugin**, puis suivre l’installation de l’environnement de rendu Python.

```text
Use $ras to turn these notes into an evidence-grounded decision memo and
deliver DOCX, PDF, and an editable PPTX companion.
```

Codex installe actuellement les compétences partagées avec `codex plugin add`, et non avec `codex skill install`. Les commandes ci-dessus épinglent la version testée ; omettez `--ref v0.1.0` pour utiliser l’état le plus récent du marketplace.

### Télécharger ou installer manuellement

Téléchargez la source empaquetée depuis [GitHub Releases](https://github.com/CharlesArea/ras/releases/latest) ou installez la même version pour le développement local :

```bash
git clone --branch v0.1.0 https://github.com/CharlesArea/ras.git
cd ras
python -m pip install -e ".[render]"
```

Python 3.11 ou une version ultérieure est requis. Le manifeste portable est [`plugin.json`](plugin.json), le catalogue se trouve dans [`marketplace.json`](.agents/plugins/marketplace.json), et des manifestes compatibles avec [Codex](.codex-plugin/plugin.json) et [Claude](.claude-plugin/plugin.json) sont inclus.

## Démarrage rapide

Initialisez un projet de rapport :

```bash
ras-report init reports/my-report \
  --request "Create an evidence-grounded decision memo from these notes" \
  --archetype decision-memo
```

La profondeur est déduite du langage naturel ; vous pouvez préciser la profondeur, le mode de recherche et le nombre de pages :

```bash
ras-report init reports/economy-deep-dive \
  --request "Create a detailed comparison of the economy before and after COVID" \
  --depth deep --research web --pages 15
```

Les profils disponibles sont `quick`, `standard` et `deep`. Affichez le plan résolu avec :

```bash
ras-report plan reports/economy-deep-dive/manifest.yaml
```

Modifiez `manifest.yaml`, `sources.yaml` et les blocs Markdown, puis validez, construisez et vérifiez le résultat :

```bash
ras-report validate reports/my-report/manifest.yaml
ras-report build reports/my-report/manifest.yaml --formats docx,pdf,pptx
ras-report qa reports/my-report/manifest.yaml
```

DOCX et PDF sont les sorties principales. PPTX est un compagnon éditable optionnel qui nécessite le Node.js fourni par l’hôte et l’environnement Artifact Tool.

### Formats de sortie

| Format | Support | Runtime |
| --- | --- | --- |
| DOCX | Sortie principale | Python avec `python-docx` |
| PDF | Sortie principale | Python avec ReportLab |
| PPTX | Compagnon éditable optionnel | Node.js de l’hôte et Artifact Tool |

### Structure d’un projet de rapport

```text
reports/my-report/
├── manifest.yaml       # demande, style, blocs, sorties et reçu QA
├── sources.yaml        # provenance et soutien des affirmations
├── blocks/*.md         # unités indépendantes et reprenables
├── assets/             # ressources visuelles fournies ou générées
├── build/              # modèle canonique et visuels intermédiaires
├── qa/                 # reçus et images des pages rendues
└── dist/               # DOCX, PDF et PPTX optionnel finaux
```

## Ce que RAS produit

RAS convient aux rapports qui exigent structure, jugement et traçabilité :

| Intention | Utile pour |
| --- | --- |
| Brief exécutif | Synthèses de direction et revues concises |
| Note de décision | Options, arbitrages, recommandations et prochaines étapes |
| Synthèse de recherche | Résultats fondés sur plusieurs sources |
| Analyse approfondie | Tendances, causes, implications et interprétation |
| Évaluation comparative | Comparaisons avant/après, d’options, de fournisseurs ou de politiques |
| Proposition et feuille de route | Cas d’affaires, stratégies, plans et jalons |
| Revue KPI et statut | Indicateurs, graphiques, avancement et cadence opérationnelle |
| Audit, risque et conformité | Contrôles, lacunes de preuves, constats et mesures d’atténuation |
| Rapport technique | Architecture, systèmes, incidents et investigations |
| SOP et étude de cas | Procédures répétables et exemples documentés |

Le routeur propose seize archétypes ; les choix explicites sont prioritaires lorsque la demande précise déjà la forme attendue.

### Modèles réutilisables

Les modèles sont des ensembles de blocs éditables et reprenables, pas des mises en page verrouillées :

| Famille | Formes incluses |
| --- | --- |
| Décision et comparaison | Note de décision, évaluation comparative, proposition/cas d’affaires |
| Recherche et analyse | Synthèse, analyse approfondie, investigation/cause racine |
| Cadence opérationnelle | Statut/progrès, performance/KPI, feuille de route stratégique |
| Risque et assurance | Audit, conformité/risque, postmortem |
| Technique et procédures | Architecture technique, politique/SOP, étude de cas |

Consultez le blueprint exact avec `ras-report template inspect <template>`.

### Planification légère du contenu

Chaque paquet conserve automatiquement un plan avec une plage de pages, une plage de mots, un objectif de diapositives et un budget par section. Une demande d’analyse détaillée sélectionne deep ; un brief concis sélectionne quick. Le plan aide à développer contexte, preuves, implications et limites sans ajouter de contenu non étayé.

## Fonctionnement

1. **Routage de la demande :** résolution de l’archétype, de l’audience, du ton, du niveau de preuve, de la géométrie, du style visuel, de la densité et de l’accent.
2. **Planification :** résolution de la profondeur, des pages cibles, des budgets et du mode de recherche. La recherche externe nécessite `web` ou une demande claire.
3. **Blocs indépendants :** chaque bloc possède un ID stable, un objectif, un statut, des sources, un budget de mise en page et un contrat visuel optionnel.
4. **Système de design :** thème, tokens de marque, composants, typographie, palette des graphiques, langage des diagrammes, espacements et rythme de page sont résolus avant le rendu.
5. **Rendu et vérification :** DOCX et PDF utilisent le même modèle ; PPTX conserve les graphiques natifs, les tableaux éditables et les références dans les notes. QA vérifie structure, parité, accessibilité, lisibilité et intégrité des pages.

## Système de design

Les thèmes modifient la hiérarchie, la couverture, les panneaux sémantiques, les tableaux, les graphiques, les diagrammes, la typographie, les espacements et la composition, pas seulement les couleurs.

| Thème | Personnalité | Idéal pour |
| --- | --- | --- |
| `minimal` | Calme et compact | Rapports courts et sobres |
| `editorial` | Chaleureux et narratif | Briefs exécutifs et récits |
| `data-forward` | Net et orienté métriques | KPI, comparaisons et dashboards |
| `institutional` | Formel et structuré | Politique, audit et conformité |
| `technical` | Précis, façon blueprint | Architecture et opérations |
| `narrative` | Expressif et rythmé | Études de cas et synthèses longues |

`.ras/brand.yaml` peut superposer couleurs, polices, espacements, tokens, palettes et tokens de diagrammes. Markdown prend en charge **gras**, *italique* et `code` de façon cohérente.

## Modèle de preuve

Les documents fournis par l’utilisateur sont la preuve principale. La recherche externe n’est utilisée que sur demande ou autorisation claire. Le registre des sources conserve la provenance et les blocs citent avec des marqueurs comme `[S1]`.

```yaml
sources:
  - id: S1
    title: Official source title
    publisher: Publisher
    url: https://example.com/source
    publication_date: "2026-01-01"
```

La validation vérifie les références, le soutien des affirmations, les légendes et textes alternatifs, les chemins sûrs et les placeholders non résolus.

## Visuels et accessibilité

Les graphiques acceptent les spécifications `bar`, `line` et `pie` avec labels, valeurs, légendes et textes alternatifs. Les diagrammes utilisent une petite grammaire sémantique et produisent des ressources SVG et PNG originales. Les visuels informatifs reçoivent légende visible, texte alternatif, métadonnées d’image dans DOCX et ressource déterministe dans le build.

## Exemples et fixtures

- [`examples/executive-brief`](examples/executive-brief) — revue de direction éditoriale
- [`examples/kpi-report`](examples/kpi-report) — rapport graphique orienté données
- [`examples/technical-report`](examples/technical-report) — rapport technique avec diagramme
- [`examples/decision-memo`](examples/decision-memo) — modèle avec options et recommandation
- [`examples/strategy-roadmap`](examples/strategy-roadmap) — priorités, jalons et mesures
- [`examples/incident-postmortem`](examples/incident-postmortem) — chronologie et actions correctives
- [`fixtures/traditional-chinese`](fixtures/traditional-chinese) — fixture d’acceptation CJK
- [`fixtures/insufficient-evidence`](fixtures/insufficient-evidence) — comportement en cas de preuves insuffisantes
- [`reports/covid-economy-comparison`](reports/covid-economy-comparison) — comparaison mondiale sourcée

Les répertoires générés `build/`, `qa/` et `dist/` sont ignorés afin de garder les paquets source révisables et reproductibles.

## Développement

```bash
python -m unittest discover -s tests -v
```

Pour une passe d’acceptation complète :

```bash
python -m unittest discover -s tests -v
ras-report validate examples/executive-brief/manifest.yaml
ras-report build examples/executive-brief/manifest.yaml --formats docx,pdf,pptx
ras-report qa examples/executive-brief/manifest.yaml
```

Les dépendances de rendu optionnelles sont déclarées dans [`pyproject.toml`](pyproject.toml) :

```bash
python -m pip install -e ".[render]"
```

## Périmètre

RAS v1 se concentre sur les rapports DOCX et PDF fondés sur des preuves, les compagnons PPTX éditables optionnels, les modèles réutilisables et la planification légère. Les rapports web, annexes de tableurs et workflows d’édition collaborative restent hors du contrat actuel.

## Licence

Voir [`LICENSE`](LICENSE).
