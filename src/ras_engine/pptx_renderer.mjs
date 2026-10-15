import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

const args = parseArgs(process.argv.slice(2));
const inputPath = args.input;
const skillDir = args["skill-dir"];
if (!inputPath || !skillDir) {
  throw new Error("PPTX renderer requires --input and --skill-dir");
}

const artifactSpecifier = process.env.RAS_ARTIFACT_TOOL
  ? pathToFileURL(process.env.RAS_ARTIFACT_TOOL).href
  : "@oai/artifact-tool";
const { Presentation, PresentationFile } = await import(artifactSpecifier);
const payload = JSON.parse(await fs.readFile(inputPath, "utf8"));
const { presentation, nativeChartSlides, nativeTableSlides } = await createDeck(payload);

await fs.mkdir(payload.preview_dir, { recursive: true });
for (const [index, slide] of presentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  await writeBlob(path.join(payload.preview_dir, `${stem}.png`), await slide.export({ format: "png", scale: 1 }));
}
try {
  await writeBlob(path.join(payload.preview_dir, "montage.webp"), await presentation.export({ format: "webp", montage: true }));
} catch {
  // A montage is a convenience preview. Individual slide renders are authoritative.
}

const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(payload.candidate_path);

const { finalizePresentation } = await import(pathToFileURL(path.join(skillDir, "container_tools", "artifact_tool_utils.mjs")).href);
const requirements = {
  workspaceDir: payload.workspace_dir,
  candidatePath: payload.candidate_path,
  finalPath: payload.finalized_path,
  explicitTotalSlideCount: presentation.slides.items.length,
  requiredNativeTableOwnerSlides: nativeTableSlides,
  requiredNativeChartOwnerSlides: nativeChartSlides,
  fontPolicy: { basis: "design", families: ["Arial"] },
  expectedSlideSizeEmu: "12192000,6858000",
  integrityValidatorPath: path.join(skillDir, "container_tools", "inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(skillDir, "container_tools", "inspect_presentation_layout_geometry.py"),
  layoutArgs: [
    "--expected-slide-size-emu", "12192000,6858000",
    "--validate-bullet-geometry",
    "--validate-heading-fit",
    ...nativeTableSlides.flatMap((slideNumber) => ["--require-native-table-slide", String(slideNumber)]),
  ],
  nativeChartTargetApplication: "powerpoint",
  verifyArtifactToolImport: true,
  receiptPath: path.join(path.dirname(payload.candidate_path), "pptx-validation.json"),
  pythonExecutable: process.env.RAS_PYTHON || "python",
};
const result = await finalizePresentation(requirements);
if (!result || result.error || result.errors?.length) {
  throw new Error(`PPTX finalization failed: ${JSON.stringify(result)}`);
}
console.log(JSON.stringify({ slides: presentation.slides.items.length, nativeChartSlides, nativeTableSlides, previewDir: payload.preview_dir }));

async function createDeck(data) {
  const design = data.design || {};
  const palette = design.palette || {};
  const typography = design.typography || {};
  const paper = palette.paper || "#F7FAFC";
  const surface = palette.surface || "#FFFFFF";
  const ink = palette.ink || "#102A43";
  const muted = palette.muted || "#627D98";
  const rule = palette.rule || "#D9E2EC";
  const accent = palette.accent || "#0E7490";
  const softAccent = palette.accent_soft || "#DFF5F7";
  const positive = palette.positive || accent;
  const font = "Arial";
  const presentation = Presentation.create({ slideSize: { width: 1280, height: 720 } });
  const nativeChartSlides = [];
  const nativeTableSlides = [];

  const cover = presentation.slides.add({ background: { fill: paper } });
  cover.background.fill = paper;
  addShape(cover, "rect", { left: 0, top: 0, width: 470, height: 720 }, accent, noLine(), "cover-accent");
  addShape(cover, "rect", { left: 470, top: 0, width: 810, height: 14 }, accent, noLine(), "cover-rule");
  addText(cover, `RAS / ${(design.display_name || "Report Anything").toUpperCase()}`, { left: 64, top: 58, width: 350, height: 28 }, {
    font, fontSize: 14, bold: true, color: paper,
  }, "cover-eyebrow");
  addText(cover, data.title, { left: 64, top: 132, width: 360, height: 210 }, {
    font, fontSize: 46, bold: true, color: paper, autoFit: "shrinkText", verticalAlignment: "middle",
  }, "cover-title");
  addText(cover, `${titleCase((data.style?.archetype || "executive brief").replaceAll("-", " "))}  ·  ${titleCase(data.style?.tone || "professional")}`, { left: 64, top: 382, width: 360, height: 44 }, {
    font, fontSize: 18, color: paper,
  }, "cover-subtitle");
  addText(cover, "Editable slides generated from the same evidence-grounded RAS model as the DOCX and PDF outputs.", { left: 64, top: 510, width: 350, height: 92 }, {
    font, fontSize: 18, color: paper, autoFit: "shrinkText",
  }, "cover-description");
  addText(cover, `${data.blocks.length} report sections  ·  ${data.sources.length} sources  ·  ${design.receipt?.emphasis || "evidence-first"}`, { left: 64, top: 650, width: 410, height: 24 }, {
    font, fontSize: 12, color: paper,
  }, "cover-footer");
  addText(cover, data.title, { left: 532, top: 70, width: 650, height: 44 }, {
    font, fontSize: 18, bold: true, color: muted,
  }, "cover-running-title");
  addShape(cover, "rect", { left: 532, top: 127, width: 560, height: 4 }, accent, noLine(), "cover-divider");
  addText(cover, "A presentation companion for the report package", { left: 532, top: 172, width: 600, height: 60 }, {
    font, fontSize: 30, bold: true, color: ink,
  }, "cover-side-heading");
  addText(cover, "Charts remain native PowerPoint charts, tables remain editable tables, and source references are preserved in speaker notes.", { left: 532, top: 262, width: 570, height: 120 }, {
    font, fontSize: 22, color: muted, autoFit: "shrinkText",
  }, "cover-side-copy");
  addShape(cover, "roundRect", { left: 532, top: 456, width: 570, height: 106 }, softAccent, { style: "solid", fill: rule, width: 1 }, "cover-receipt");
  addText(cover, "DESIGN RECEIPT", { left: 558, top: 478, width: 180, height: 22 }, {
    font, fontSize: 12, bold: true, color: accent,
  }, "cover-receipt-label");
  addText(cover, `${design.display_name || "RAS theme"}  ·  ${design.density || "standard"} density  ·  ${design.emphasis || "text-balanced"}`, { left: 558, top: 510, width: 500, height: 28 }, {
    font, fontSize: 18, color: ink, autoFit: "shrinkText",
  }, "cover-receipt-copy");
  setNotes(cover, coverNotes(data));

  for (let index = 0; index < data.blocks.length; index += 1) {
    const block = data.blocks[index];
    const slide = presentation.slides.add({ background: { fill: paper } });
    addHeader(slide, data, index + 1, block.title, { paper, surface, ink, muted, rule, accent, softAccent, font });
    addShape(slide, "roundRect", { left: 72, top: 126, width: 1136, height: 58 }, softAccent, { style: "solid", fill: rule, width: 1 }, `goal-${block.id}`);
    addText(slide, `${semanticLabel(block)} / ${design.components?.[semanticKind(block)] || "report section"}`, { left: 94, top: 142, width: 250, height: 28 }, {
      font, fontSize: 13, bold: true, color: accent,
    }, `goal-label-${block.id}`);
    addText(slide, block.goal || "Evidence-grounded report section", { left: 360, top: 140, width: 820, height: 34 }, {
      font, fontSize: 17, color: ink, autoFit: "shrinkText",
    }, `goal-copy-${block.id}`);

    const visual = block.visual || {};
    const visualKind = String(visual.kind || "").toLowerCase();
    const elements = block.elements || [];
    const tableElement = elements.find((element) => element.kind === "table" && element.rows?.length);
    const hasVisualAsset = Boolean(block.visual_asset?.png) && await exists(block.visual_asset.png);
    if ((block.type === "chart" || ["line", "bar", "pie"].includes(visualKind)) && Array.isArray(visual.labels) && Array.isArray(visual.values) && visual.labels.length) {
      addText(slide, compactText(blockVisibleText(block), 780), { left: 72, top: 224, width: 380, height: 330 }, {
        font, fontSize: 20, color: ink, autoFit: "shrinkText", verticalAlignment: "top",
      }, `body-${block.id}`);
      addNativeChart(slide, visualKind === "bar" ? "bar" : visualKind === "pie" ? "pie" : "line", visual, { left: 500, top: 224, width: 670, height: 360 }, { font, ink, muted, rule, accent, paper });
      nativeChartSlides.push(index + 2);
      addText(slide, visual.caption || "Source-defined chart", { left: 500, top: 600, width: 670, height: 26 }, {
        font, fontSize: 12, color: muted, autoFit: "shrinkText",
      }, `caption-${block.id}`);
    } else if (hasVisualAsset) {
      addText(slide, compactText(blockVisibleText(block), 650), { left: 72, top: 224, width: 500, height: 320 }, {
        font, fontSize: 20, color: ink, autoFit: "shrinkText",
      }, `body-${block.id}`);
      await addImage(slide, block.visual_asset.png, { left: 650, top: 232, width: 510, height: 340 }, block.visual?.alt_text || block.visual_asset.alt_text || "Report visual", `visual-${block.id}`);
      addText(slide, block.visual?.caption || "Source-defined visual", { left: 650, top: 584, width: 510, height: 30 }, {
        font, fontSize: 12, color: muted, autoFit: "shrinkText",
      }, `caption-${block.id}`);
    } else if (tableElement) {
      addText(slide, compactText(blockVisibleText(block, { excludeTables: true }), 920), { left: 72, top: 219, width: 1136, height: 100 }, {
        font, fontSize: 19, color: ink, autoFit: "shrinkText",
      }, `body-${block.id}`);
      addNativeTable(slide, tableElement.rows, { left: 72, top: 340, width: 1136, height: 270 }, { font, ink, muted, rule, accent, paper, softAccent });
      nativeTableSlides.push(index + 2);
    } else {
      addText(slide, compactText(blockVisibleText(block), 2800), { left: 72, top: 224, width: 1136, height: 380 }, {
        font, fontSize: 21, color: ink, autoFit: "shrinkText", verticalAlignment: "top",
      }, `body-${block.id}`);
    }
    addText(slide, `${String(index + 1).padStart(2, "0")}  ·  ${data.title}`, { left: 72, top: 674, width: 750, height: 22 }, {
      font, fontSize: 11, color: muted,
    }, `footer-${block.id}`);
    addText(slide, `${index + 2}`, { left: 1160, top: 674, width: 48, height: 22 }, {
      font, fontSize: 11, color: muted, alignment: "right",
    }, `folio-${block.id}`);
    setNotes(slide, blockNotes(block, data.sources));
  }

  const sourcesSlide = presentation.slides.add({ background: { fill: paper } });
  addHeader(sourcesSlide, data, data.blocks.length + 1, "Sources and quality receipt", { paper, surface, ink, muted, rule, accent, softAccent, font });
  addText(sourcesSlide, "Source register", { left: 72, top: 132, width: 500, height: 34 }, {
    font, fontSize: 30, bold: true, color: accent,
  }, "sources-title");
  const sourceRows = [["ID", "Source", "Publisher / link"]].concat(data.sources.map((source) => [
    source.id,
    source.title,
    shortPublisher(source),
  ]));
  if (sourceRows.length > 1) {
    addNativeTable(sourcesSlide, sourceRows, { left: 72, top: 174, width: 1136, height: 314 }, { font, ink, muted, rule, accent, paper, softAccent, small: true });
    nativeTableSlides.push(data.blocks.length + 2);
  }
  addText(sourcesSlide, qualityReceipt(data), { left: 72, top: 590, width: 1136, height: 54 }, {
    font, fontSize: 13, color: muted, autoFit: "shrinkText",
  }, "quality-receipt");
  addText(sourcesSlide, `${data.blocks.length + 2}`, { left: 1160, top: 674, width: 48, height: 22 }, {
    font, fontSize: 11, color: muted, alignment: "right",
  }, "sources-folio");
  setNotes(sourcesSlide, sourceNotes(data));

  return { presentation, nativeChartSlides, nativeTableSlides };
}

function addHeader(slide, data, number, title, theme) {
  addShape(slide, "rect", { left: 0, top: 0, width: 1280, height: 12 }, theme.accent, noLine(), `header-band-${number}`);
  addText(slide, "RAS / REPORT ANYTHING", { left: 72, top: 30, width: 300, height: 20 }, {
    font: theme.font, fontSize: 11, bold: true, color: theme.accent,
  }, `header-brand-${number}`);
  addText(slide, `${data.title}  ·  ${titleCase(data.style?.archetype || "report")}`, { left: 740, top: 30, width: 468, height: 20 }, {
    font: theme.font, fontSize: 11, color: theme.muted, alignment: "right", autoFit: "shrinkText",
  }, `header-context-${number}`);
  addShape(slide, "rect", { left: 72, top: 66, width: 1136, height: 1 }, theme.rule, noLine(), `header-rule-${number}`);
  const titleText = `${String(number).padStart(2, "0")}  ${title}`;
  const titleSize = titleText.length > 58 ? 24 : titleText.length > 38 ? 28 : 34;
  addText(slide, titleText, { left: 72, top: 78, width: 1136, height: 38 }, {
    font: theme.font, fontSize: titleSize, bold: true, color: theme.ink, autoFit: "shrinkText",
  }, `section-title-${number}`);
}

function addNativeChart(slide, kind, visual, position, theme) {
  const labels = visual.labels.map((value) => String(value));
  const values = visual.values.map((value) => Number(value));
  const chart = slide.charts.add(kind, {
    position,
    title: visual.title || "Report chart",
    titleTextStyle: { typeface: theme.font, fontSize: 18, fill: theme.ink, bold: true },
    categories: labels,
    series: [{ name: visual.title || "Series", values, fill: theme.accent, line: { style: "solid", fill: theme.accent, width: 3 }, marker: { symbol: "circle", size: 8, fill: theme.accent } }],
    hasLegend: false,
    chartLine: { style: "solid", fill: "none", width: 0 },
    plotAreaFill: theme.paper,
    plotAreaLine: { style: "solid", fill: "none", width: 0 },
    xAxis: { textStyle: { typeface: theme.font, fontSize: 13, fill: theme.muted }, line: { style: "solid", fill: theme.rule, width: 1 } },
    yAxis: { textStyle: { typeface: theme.font, fontSize: 13, fill: theme.muted }, majorGridlines: { style: "solid", fill: theme.rule, width: 1 }, line: { style: "solid", fill: "none", width: 0 } },
    lineOptions: { smooth: false },
    barOptions: { direction: "column", grouping: "clustered", gapWidth: 80 },
    dataLabels: kind === "pie" ? { showPercent: true, showCategoryName: true, position: "outEnd" } : { showValue: false },
  });
  return chart;
}

function addNativeTable(slide, rawRows, position, theme) {
  const rows = rawRows.map((row) => row.map((cell) => stripMarkdown(String(cell))));
  const columns = Math.max(...rows.map((row) => row.length));
  const normalized = rows.map((row) => Array.from({ length: columns }, (_, index) => row[index] || ""));
  const table = slide.tables.add({ rows: normalized.length, columns, left: position.left, top: position.top, width: position.width, height: position.height, values: normalized });
  table.styleOptions = { headerRow: true, bandedRows: true };
  table.borders.assign({ style: "solid", fill: theme.rule, width: 1 });
  for (let row = 0; row < normalized.length; row += 1) {
    for (let column = 0; column < columns; column += 1) {
      const cell = table.getCell(row, column);
      cell.fill = row === 0 ? theme.softAccent : row % 2 === 0 ? theme.surface : theme.paper;
      cell.text.style = {
        typeface: theme.font,
        fontSize: position.small ? 11 : 16,
        color: row === 0 ? theme.accent : theme.ink,
        bold: row === 0,
        verticalAlignment: "middle",
        autoFit: "shrinkText",
      };
    }
  }
  return table;
}

async function addImage(slide, imagePath, position, alt, name) {
  const bytes = await fs.readFile(imagePath);
  const blob = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
  return slide.images.add({ blob, contentType: "image/png", alt, fit: "contain", geometry: "roundRect", borderRadius: "rounded-xl", position, name });
}

function addShape(slide, geometry, position, fill, line, name) {
  return slide.shapes.add({ geometry, position, fill, line, name });
}

function addText(slide, text, position, style, name) {
  const shape = slide.shapes.add({ geometry: "textbox", position, fill: "none", line: noLine(), name });
  shape.text = text || "";
  shape.text.style = {
    typeface: style.font || "Arial",
    fontSize: style.fontSize || 18,
    color: style.color || "#102A43",
    bold: Boolean(style.bold),
    italic: Boolean(style.italic),
    alignment: style.alignment || "left",
    verticalAlignment: style.verticalAlignment || "top",
    autoFit: style.autoFit || "shrinkText",
    wrap: "square",
    insets: style.insets ?? 0,
    lineSpacing: 1.12,
  };
  return shape;
}

function noLine() {
  return { style: "solid", fill: "none", width: 0 };
}

function setNotes(slide, notes) {
  slide.speakerNotes.text = notes;
  slide.speakerNotes.setVisible(true);
}

function blockVisibleText(block, options = {}) {
  const pieces = [];
  for (const element of block.elements || []) {
    if (options.excludeTables && element.kind === "table") continue;
    if (element.kind === "heading" || element.kind === "paragraph" || element.kind === "callout" || element.kind === "code") {
      if (element.text) pieces.push(stripMarkdown(element.text));
    } else if (element.kind === "bullet_list") {
      for (const item of element.items || []) pieces.push(`• ${stripMarkdown(item)}`);
    } else if (element.kind === "table") {
      for (const row of element.rows || []) pieces.push(row.map((cell) => stripMarkdown(cell)).join("  ·  "));
    }
  }
  return pieces.join("\n\n") || "Add supported content to this template section.";
}

function semanticKind(block) {
  const type = String(block.type || "narrative").toLowerCase().replaceAll("-", "_");
  if (["executive_summary", "summary"].includes(type)) return "summary";
  if (["recommendation", "decision", "action"].includes(type)) return "recommendation";
  if (["chart", "diagram", "timeline", "metric_panel", "table_visual"].includes(type)) return "visual";
  if (["finding", "analysis", "risk", "issue"].includes(type)) return "finding";
  return "narrative";
}

function semanticLabel(block) {
  return { summary: "Executive summary", finding: "Key finding", recommendation: "Recommended action", visual: "Evidence visual", narrative: "Report section" }[semanticKind(block)] || "Report section";
}

function blockNotes(block, sources) {
  const selected = new Set(block.source_refs || []);
  const sourceLines = sources.filter((source) => selected.has(source.id)).map((source) => `${source.id}: ${source.title}${source.url ? ` — ${source.url}` : ""}`);
  return [
    `RAS source notes for: ${block.title}`,
    sourceLines.length ? `Sources:\n${sourceLines.join("\n")}` : "Sources: none recorded for this block.",
    "",
    "Full block text:",
    block.body || block.plain_text || "",
  ].join("\n");
}

function coverNotes(data) {
  const sourceLines = data.sources.map((source) => `${source.id}: ${source.title}${source.url ? ` — ${source.url}` : ""}`);
  return [`RAS presentation companion for ${data.title}`, "", "Sources used by the report:", sourceLines.join("\n") || "None recorded.", "", "The deck is an executive adaptation of the canonical report model."].join("\n");
}

function sourceNotes(data) {
  return ["RAS source register", ...data.sources.map((source) => `${source.id}: ${source.title}${source.url ? ` — ${source.url}` : ""}`), "", "Assumptions:", ...(data.assumptions || []).map((item) => `- ${item}`), "", "Omitted material:", ...(data.omitted_material || []).map((item) => `- ${item}`)].join("\n");
}

function compactSourceLocation(source) {
  if (source.url) {
    try {
      return new URL(source.url).hostname.replace(/^www\./, "");
    } catch {
      return "linked source";
    }
  }
  return source.file || "recorded source";
}

function shortPublisher(source) {
  const publisher = String(source.publisher || source.author || "");
  if (/monetary fund/i.test(publisher)) return "IMF";
  if (/labour organization|labor organization/i.test(publisher)) return "ILO";
  if (/world bank/i.test(publisher)) return "World Bank";
  return publisher || compactSourceLocation(source);
}

function qualityReceipt(data) {
  const assumptions = (data.assumptions || []).slice(0, 2).map((item) => `Assumption: ${item}`).join("\n");
  const omitted = (data.omitted_material || []).slice(0, 1).map((item) => `Omitted: ${item}`).join("\n");
  return [assumptions, omitted, "Citations and full block text are preserved in speaker notes."].filter(Boolean).join("\n");
}

function compactText(value, limit) {
  const text = String(value || "");
  if (text.length <= limit) return text;
  return `${text.slice(0, Math.max(0, limit - 1)).trimEnd()}…`;
}

function stripMarkdown(value) {
  return String(value || "")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/__([^_]+)__/g, "$1")
    .replace(/(?<!\w)\*([^*]+)\*(?!\w)/g, "$1")
    .replace(/(?<!\w)_([^_]+)_(?!\w)/g, "$1");
}

function titleCase(value) {
  return String(value || "").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function writeBlob(filePath, blob) {
  const bytes = blob instanceof Uint8Array ? blob : new Uint8Array(await blob.arrayBuffer());
  await fs.writeFile(filePath, bytes);
}

function parseArgs(argv) {
  const result = {};
  for (let index = 0; index < argv.length; index += 1) {
    const item = argv[index];
    if (!item.startsWith("--")) continue;
    result[item.slice(2)] = argv[index + 1] && !argv[index + 1].startsWith("--") ? argv[++index] : true;
  }
  return result;
}
