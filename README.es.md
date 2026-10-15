<div align="center">

<img src="assets/readme/ras-pipeline.svg" alt="Flujo de RAS desde la solicitud y la evidencia hasta el informe" width="100%">

# RAS — Report Anything Skill

### Convierte una solicitud y su evidencia en un informe que la gente realmente quiere leer.

Seis temas visuales · Dieciséis plantillas reutilizables · DOCX + PDF + PPTX editable opcional desde un modelo canónico

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

![Salidas](https://img.shields.io/badge/salidas-DOCX%20%2B%20PDF%20%2B%20PPTX%20opcional-117A8B?style=flat-square)
![Temas](https://img.shields.io/badge/temas-6-117A8B?style=flat-square)
![Pruebas](https://img.shields.io/badge/pruebas-19%20passing-027A48?style=flat-square)

</div>

## Por qué RAS

La mayoría de la automatización de informes se detiene en el texto. RAS trata el informe como un artefacto diseñado y auditable: elige la forma de comunicación, conserva la trazabilidad de la evidencia, resuelve un sistema visual, genera DOCX y PDF desde el mismo modelo canónico, añade opcionalmente un PPTX editable y comprueba las salidas antes de entregarlas.

Pide el resultado en lenguaje natural:

> «Compara las opciones para el consejo y recomienda un camino.»

> «Crea una revisión de KPI con un gráfico de tendencia claro.»

> «Convierte esta investigación en una síntesis basada en evidencia.»

> «Explica el incidente, la causa raíz, el impacto y las acciones correctivas.»

RAS convierte la solicitud en un proyecto estructurado con bloques Markdown independientes, un registro de fuentes, un contrato visual y un recibo de calidad.

### Documentación localizada

Lee el proyecto en [简体中文](README.zh-CN.md), [繁體中文](README.zh-TW.md), [日本語](README.ja.md), [한국어](README.ko.md), [Español](README.es.md), [Français](README.fr.md), [Deutsch](README.de.md), [Português (Brasil)](README.pt-BR.md) o [Русский](README.ru.md). RAS conserva el texto Unicode en los bloques y admite fuentes CJK de respaldo configurables.

## En acción

Estas vistas previas se generan a partir de los ejemplos y fixtures de aceptación del repositorio.

<table>
  <tr>
    <td width="50%"><img src="assets/readme/kpi-dashboard.png" alt="Informe KPI orientado a datos con gráfico de tendencia"></td>
    <td width="50%"><img src="assets/readme/technical-blueprint.png" alt="Informe técnico con diagrama de arquitectura original"></td>
  </tr>
  <tr>
    <td align="center"><sub>Revisión KPI orientada a datos</sub></td>
    <td align="center"><sub>Informe de arquitectura técnica</sub></td>
  </tr>
</table>

<table>
  <tr>
    <td width="50%"><img src="assets/readme/editorial-brief.png" alt="Resumen ejecutivo editorial con paleta de papel cálida"></td>
    <td width="50%"><img src="assets/readme/ras-growth-chart.png" alt="Gráfico comparativo de crecimiento global en un informe RAS"></td>
  </tr>
  <tr>
    <td align="center"><sub>Resumen ejecutivo editorial</sub></td>
    <td align="center"><sub>Comparación analítica con gráfico</sub></td>
  </tr>
</table>

### Compañeros PPTX editables

El renderizador de presentaciones adapta el mismo paquete a una presentación panorámica editable. Los gráficos siguen siendo gráficos nativos de PowerPoint, las tablas de fuentes siguen siendo editables y las referencias completas y el texto de los bloques se conservan en las notas del orador.

<table>
  <tr>
    <td width="33%"><img src="assets/readme/economy-deck-cover.png" alt="Portada PPTX editable del informe de economía global"></td>
    <td width="33%"><img src="assets/readme/economy-deck-chart.png" alt="Diapositiva con gráfico de crecimiento nativo"></td>
    <td width="33%"><img src="assets/readme/economy-deck-sources.png" alt="Diapositiva editable del registro de fuentes"></td>
  </tr>
  <tr>
    <td align="center"><sub>Portada</sub></td>
    <td align="center"><sub>Gráfico nativo</sub></td>
    <td align="center"><sub>Registro de fuentes editable</sub></td>
  </tr>
</table>

## Instalar en Codex

RAS se distribuye como un plugin versionado de Codex. Añade el marketplace de la versión estable `v0.1.0`:

```bash
codex plugin marketplace add CharlesArea/ras --ref v0.1.0
codex plugin add ras@ras-marketplace
```

Después inicia un chat nuevo de Codex y pide usar `$ras`. Desde el navegador de plugins, inicia `codex`, ejecuta `/plugins`, abre **RAS — Report Anything Skill** y elige **Install plugin**. Sigue la configuración para instalar el entorno de renderizado de Python.

```text
Use $ras to turn these notes into an evidence-grounded decision memo and
deliver DOCX, PDF, and an editable PPTX companion.
```

Codex instala actualmente las habilidades compartidas con `codex plugin add`, no con `codex skill install`. Los comandos anteriores fijan la versión probada; omite `--ref v0.1.0` para usar el estado más reciente del marketplace.

### Descargar o instalar manualmente

Descarga el código empaquetado desde [GitHub Releases](https://github.com/CharlesArea/ras/releases/latest) o instala la misma versión fijada para desarrollo local:

```bash
git clone --branch v0.1.0 https://github.com/CharlesArea/ras.git
cd ras
python -m pip install -e ".[render]"
```

Se requiere Python 3.11 o posterior. El manifiesto portátil es [`plugin.json`](plugin.json), el catálogo está en [`marketplace.json`](.agents/plugins/marketplace.json) y también se incluyen manifiestos compatibles con [Codex](.codex-plugin/plugin.json) y [Claude](.claude-plugin/plugin.json).

## Inicio rápido

Inicializa un proyecto de informe:

```bash
ras-report init reports/my-report \
  --request "Create an evidence-grounded decision memo from these notes" \
  --archetype decision-memo
```

La profundidad se infiere del lenguaje natural; puedes sobrescribirla junto con la investigación y el número de páginas:

```bash
ras-report init reports/economy-deep-dive \
  --request "Create a detailed comparison of the economy before and after COVID" \
  --depth deep --research web --pages 15
```

Los perfiles disponibles son `quick`, `standard` y `deep`. Consulta el plan resuelto con:

```bash
ras-report plan reports/economy-deep-dive/manifest.yaml
```

Edita `manifest.yaml`, `sources.yaml` y los bloques Markdown generados; después valida, construye y ejecuta QA:

```bash
ras-report validate reports/my-report/manifest.yaml
ras-report build reports/my-report/manifest.yaml --formats docx,pdf,pptx
ras-report qa reports/my-report/manifest.yaml
```

DOCX y PDF son las salidas principales. PPTX es un compañero editable opcional y requiere el Node.js incluido y Artifact Tool del host.

### Formatos de salida

| Formato | Soporte | Runtime |
| --- | --- | --- |
| DOCX | Salida principal | Python con `python-docx` |
| PDF | Salida principal | Python con ReportLab |
| PPTX | Compañero editable opcional | Node.js del host y Artifact Tool |

### Proyecto de informe

```text
reports/my-report/
├── manifest.yaml       # solicitud, estilo, bloques, salidas y recibo QA
├── sources.yaml        # procedencia y soporte de afirmaciones
├── blocks/*.md         # unidades independientes y reanudables
├── assets/             # recursos visuales proporcionados o generados
├── build/              # modelo canónico y visuales intermedios
├── qa/                 # recibos e imágenes de páginas renderizadas
└── dist/               # DOCX, PDF y PPTX opcional finales
```

## Qué produce

RAS ayuda con informes que necesitan estructura, criterio y trazabilidad:

| Intención | Útil para |
| --- | --- |
| Resumen ejecutivo | Síntesis para dirección y revisiones breves |
| Memo de decisión | Opciones, trade-offs, recomendaciones y siguientes pasos |
| Síntesis de investigación | Hallazgos basados en varias fuentes |
| Análisis profundo | Tendencias, causas, implicaciones e interpretación |
| Evaluación comparativa | Comparaciones antes/después, de opciones, proveedores o políticas |
| Propuesta y roadmap | Casos de negocio, estrategias, planes y hitos |
| KPI y estado | Métricas, gráficos, progreso y cadencia operativa |
| Auditoría, riesgo y compliance | Controles, brechas de evidencia, hallazgos y mitigaciones |
| Informe técnico | Arquitectura, sistemas, incidentes e investigaciones |
| SOP y caso de estudio | Procedimientos repetibles y ejemplos documentados |

El router ofrece dieciséis arquetipos con sobrescrituras explícitas cuando la solicitud ya define la forma.

### Plantillas reutilizables

Las plantillas son conjuntos de bloques editables y reanudables, no diseños bloqueados:

| Familia | Formas incluidas |
| --- | --- |
| Decisión y comparación | Memo de decisión, evaluación comparativa, propuesta/caso de negocio |
| Investigación y análisis | Síntesis, análisis profundo, investigación/causa raíz |
| Cadencia operativa | Estado/progreso, KPI, roadmap estratégico |
| Riesgo y assurance | Auditoría, compliance/riesgo, postmortem |
| Técnica y procedimientos | Arquitectura técnica, política/SOP, caso de estudio |

Consulta el blueprint exacto con `ras-report template inspect <template>`.

### Planificación ligera

Cada paquete registra automáticamente un plan de contenido con rango de páginas, rango de palabras, objetivo de diapositivas y presupuesto por sección. Una solicitud de “análisis detallado” elige deep; un “resumen conciso” elige quick. Así se amplían contexto, evidencia, implicaciones y límites sin rellenar contenido sin respaldo.

## Cómo funciona

1. **Enruta la solicitud:** resuelve arquetipo, audiencia, tono, nivel de evidencia, geometría, estilo visual, densidad y énfasis. Las elecciones explícitas ganan.
2. **Planifica el contenido:** resuelve profundidad, páginas, presupuestos y modo de investigación. La investigación externa requiere `web` explícito o una petición clara.
3. **Construye bloques independientes:** cada bloque tiene ID estable, objetivo, estado, fuentes, presupuesto de diseño y contrato visual opcional.
4. **Resuelve un sistema de diseño:** el compilador decide tema, tokens de marca, componentes, tipografía, paleta de gráficos, lenguaje de diagramas, espacios y ritmo de página.
5. **Renderiza y verifica:** DOCX y PDF usan el mismo modelo; PPTX mantiene gráficos nativos, tablas editables y referencias en las notas. QA comprueba estructura, paridad, accesibilidad, legibilidad y páginas renderizadas.

## Sistema de diseño

Los temas cambian la jerarquía, la portada, los paneles semánticos, tablas, gráficos, diagramas, tipografía, espaciado y composición, no solo los colores.

| Tema | Personalidad | Mejor para |
| --- | --- | --- |
| `minimal` | Tranquilo y compacto | Informes cortos y sobrios |
| `editorial` | Cálido y narrativo | Resúmenes ejecutivos e historias |
| `data-forward` | Nítido y orientado a métricas | KPI, comparaciones y dashboards |
| `institutional` | Formal y estructurado | Política, auditoría y compliance |
| `technical` | Preciso, tipo blueprint | Arquitectura y operaciones |
| `narrative` | Expresivo y pausado | Casos de estudio y síntesis largas |

`.ras/brand.yaml` puede superponer colores, fuentes, espaciado, tokens, paletas y diagramas. Markdown soporta **negrita**, *cursiva* y `code` de forma consistente.

## Modelo de evidencia

El material proporcionado por el usuario es la evidencia principal. La investigación externa solo se usa cuando se solicita o autoriza claramente. El registro de fuentes conserva la procedencia y los bloques citan con marcadores como `[S1]`.

```yaml
sources:
  - id: S1
    title: Official source title
    publisher: Publisher
    url: https://example.com/source
    publication_date: "2026-01-01"
```

La validación comprueba referencias, soporte de afirmaciones, captions y texto alternativo, rutas seguras y placeholders no resueltos.

## Visuales y accesibilidad

Los gráficos aceptan especificaciones `bar`, `line` y `pie` con etiquetas, valores, captions y texto alternativo. Los diagramas usan una gramática semántica pequeña y generan SVG y PNG originales. Cada visual informativo recibe caption visible, texto alternativo, metadatos de imagen en DOCX y un recurso determinista en el modelo de build.

## Ejemplos y fixtures

- [`examples/executive-brief`](examples/executive-brief) — revisión editorial de dirección
- [`examples/kpi-report`](examples/kpi-report) — informe de gráficos orientado a datos
- [`examples/technical-report`](examples/technical-report) — informe técnico con diagrama
- [`examples/decision-memo`](examples/decision-memo) — plantilla con opciones y recomendación
- [`examples/strategy-roadmap`](examples/strategy-roadmap) — prioridades, hitos y medidas
- [`examples/incident-postmortem`](examples/incident-postmortem) — línea de tiempo y acciones correctivas
- [`fixtures/traditional-chinese`](fixtures/traditional-chinese) — fixture de aceptación CJK
- [`fixtures/insufficient-evidence`](fixtures/insufficient-evidence) — comportamiento ante evidencia insuficiente
- [`reports/covid-economy-comparison`](reports/covid-economy-comparison) — paquete comparativo global con fuentes

Los directorios generados `build/`, `qa/` y `dist/` están ignorados para mantener los paquetes fuente revisables y reproducibles.

## Desarrollo

```bash
python -m unittest discover -s tests -v
```

Para una pasada completa:

```bash
python -m unittest discover -s tests -v
ras-report validate examples/executive-brief/manifest.yaml
ras-report build examples/executive-brief/manifest.yaml --formats docx,pdf,pptx
ras-report qa examples/executive-brief/manifest.yaml
```

Las dependencias opcionales de renderizado están declaradas en [`pyproject.toml`](pyproject.toml):

```bash
python -m pip install -e ".[render]"
```

## Alcance

RAS v1 se centra en informes DOCX y PDF basados en evidencia, compañeros PPTX editables opcionales, plantillas reutilizables y planificación ligera. Los informes web, anexos de hojas de cálculo y la edición colaborativa quedan fuera del contrato actual.

## Licencia

Consulta [`LICENSE`](LICENSE).
