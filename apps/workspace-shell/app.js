const DATA_URLS = {
  shell: "./data/workspace-shell-data.json",
  export: "./data/workspace-export.json",
  manifest: "./data/workspace-manifest.json",
};

const elements = {
  runtimeCard: document.querySelector(".runtime-card"),
  runtimeStatus: document.querySelector("#runtime-status"),
  runtimeDetail: document.querySelector("#runtime-detail"),
  routeList: document.querySelector("#route-list"),
  authoritySummary: document.querySelector("#authority-summary"),
  downloadButton: document.querySelector("#download-export"),
  downloadNote: document.querySelector("#download-note"),
  loadingPanel: document.querySelector("#loading-panel"),
  contentPanel: document.querySelector("#content-panel"),
  errorPanel: document.querySelector("#error-panel"),
  main: document.querySelector("#main-content"),
};

let shellData = null;
let workspaceExport = null;
let workspaceManifest = null;
let exportBytes = null;
let lastValidHash = "#overview";

function node(tag, options = {}, children = []) {
  const element = document.createElement(tag);
  for (const [key, value] of Object.entries(options)) {
    if (key === "className") element.className = value;
    else if (key === "text") element.textContent = value;
    else if (key.startsWith("aria-")) element.setAttribute(key, String(value));
    else if (key === "dataset") Object.assign(element.dataset, value);
    else element[key] = value;
  }
  for (const child of children) {
    element.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return element;
}

function label(value) {
  return String(value)
    .replaceAll("-", " ")
    .replaceAll("_", " ")
    .replace(/\b\w/g, character => character.toUpperCase());
}

function exactKey(reference) {
  return `${reference.id}@${reference.revision}`;
}

function pill(text, tone = "") {
  return node("span", { className: `pill ${tone}`.trim(), text });
}

function definitionList(entries, className = "definition-list") {
  const list = node("dl", { className });
  for (const [term, description] of entries) {
    const wrapper = node("div");
    wrapper.append(node("dt", { text: term }), node("dd", { text: String(description) }));
    list.append(wrapper);
  }
  return list;
}

function list(values, className = "summary-list", ordered = false) {
  const container = node(ordered ? "ol" : "ul", { className });
  for (const value of values) container.append(node("li", { text: value }));
  return container;
}

function exactReferenceList(references) {
  const container = node("ul", { className: "reference-list" });
  for (const reference of references) {
    const item = node("li");
    item.append(node("code", { text: exactKey(reference) }));
    container.append(item);
  }
  return container;
}

function detailCard(title, content, full = false) {
  const card = node("section", { className: `detail-card${full ? " full" : ""}` });
  card.append(node("h3", { text: title }), content);
  return card;
}

function showOnly(panel) {
  for (const candidate of [elements.loadingPanel, elements.contentPanel, elements.errorPanel]) {
    candidate.hidden = candidate !== panel;
  }
}

function setDocumentTitle(title) {
  document.title = `${title} · Atlas Research Workspace`;
}

function updateCurrentNavigation(hash) {
  for (const link of elements.routeList.querySelectorAll("a")) {
    if (link.getAttribute("href") === hash) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  }
}

function renderAuthoritySummary(authority) {
  const entries = [
    ["Workspace authority", authority.workspace_authority],
    ["Browser state", authority.browser_state_authority],
    ["Exact revisions", authority.exact_revision_required ? "required" : "missing"],
    ["Entry order", authority.entry_order_preserved ? "preserved" : "mutable"],
    ["Decisions", authority.decisions_read_only ? "read only" : "editable"],
    ["Candidates", authority.candidates_unresolved ? "unresolved" : "resolved"],
    ["Canonical writes", authority.canonical_mutation ? "enabled" : "blocked"],
    ["Live Principia", authority.live_principia_dependency ? "active" : "inactive"],
  ];
  elements.authoritySummary.replaceChildren();
  for (const [term, description] of entries) {
    const wrapper = node("div");
    wrapper.append(node("dt", { text: term }), node("dd", { text: String(description) }));
    elements.authoritySummary.append(wrapper);
  }
}

function renderNavigation() {
  elements.routeList.replaceChildren();
  shellData.routes.forEach((route, index) => {
    const link = node("a", {
      className: "route-link",
      href: route.hash,
      dataset: { routeId: route.id, routeKind: route.kind },
      "aria-label": route.label,
    });
    const routeIndex = route.kind === "entry" ? String(route.position) : String(index + 1).padStart(2, "0");
    link.append(
      node("span", { className: "route-index", text: routeIndex, "aria-hidden": "true" }),
      node("span", { className: "route-label", text: route.label }),
    );
    elements.routeList.append(node("li", {}, [link]));
  });
}

async function sha256Hex(buffer) {
  const digest = await crypto.subtle.digest("SHA-256", buffer);
  return [...new Uint8Array(digest)]
    .map(value => value.toString(16).padStart(2, "0"))
    .join("");
}

async function verifyPackage() {
  if (shellData.contract !== "atlas-workspace-shell-data/0.1") throw new Error("Unsupported workspace shell contract");
  if (workspaceExport.contract !== "atlas-research-workspace-export/0.1") throw new Error("Unsupported workspace export contract");
  if (workspaceManifest.contract !== "atlas-research-workspace-manifest/0.1") throw new Error("Unsupported workspace manifest contract");
  if (shellData.routes.length !== 13 || workspaceExport.entries.length !== 5) throw new Error("Workspace route or entry count mismatch");
  if (shellData.workspace.id !== workspaceExport.workspace.id || shellData.workspace.revision !== workspaceExport.workspace.revision) {
    throw new Error("Workspace identity mismatch");
  }
  const observedSha = await sha256Hex(exportBytes);
  if (observedSha !== shellData.accepted_export.artifact.sha256) throw new Error("Workspace export SHA-256 mismatch");
  if (exportBytes.byteLength !== shellData.accepted_export.artifact.bytes) throw new Error("Workspace export byte length mismatch");
  const manifestFile = workspaceManifest.files.find(item => item.file === "workspace-export.json");
  if (!manifestFile || manifestFile.sha256 !== observedSha || manifestFile.bytes !== exportBytes.byteLength) {
    throw new Error("Workspace manifest does not bind the accepted export");
  }
  const positions = workspaceExport.entries.map(entry => entry.position);
  if (positions.join(",") !== "1,2,3,4,5") throw new Error("Workspace entry order mismatch");
  if (workspaceExport.candidate_references.some(candidate => candidate.resolution !== "unresolved")) {
    throw new Error("Workspace candidates must remain unresolved");
  }
  if (!workspaceExport.principia_references.every(reference => reference.principia_status_separate === true && reference.live === false)) {
    throw new Error("Principia status must remain separate and non-live");
  }
}

function panelHeading(eyebrow, title, description) {
  const fragment = document.createDocumentFragment();
  fragment.append(
    node("p", { className: "eyebrow", text: eyebrow }),
    node("h2", { id: "active-view-title", text: title }),
  );
  if (description) fragment.append(node("p", { text: description }));
  return fragment;
}

function renderOverview() {
  const panel = elements.contentPanel;
  panel.replaceChildren(
    panelHeading(
      "WORKSPACE OVERVIEW",
      "One accepted research package, read without mutation",
      "The browser exposes the accepted export exactly as built. Decisions, order, candidates, and status cannot be edited here.",
    ),
  );
  panel.setAttribute("aria-labelledby", "active-view-title");
  panel.append(
    node("div", { className: "meta-row" }, [
      pill(`${workspaceExport.entries.length} ordered entries`, "good"),
      pill(`${workspaceExport.candidate_references.length} unresolved candidates`),
      pill(`${workspaceExport.principia_references.length} separate Principia reference`),
      pill("No canonical writes", "good"),
    ]),
  );
  const decisions = workspaceExport.entries.map(entry => {
    const metadata = entry.visible_metadata;
    return `${entry.position}. ${label(entry.decision.action)} — ${metadata.title} (${exactKey(entry.exact_reference)})`;
  });
  const grid = node("div", { className: "section-grid" });
  grid.append(
    detailCard("Workspace identity", definitionList([
      ["Workspace", exactKey(workspaceExport.workspace)],
      ["Source digest", workspaceExport.source_digest],
      ["Export digest", workspaceExport.report_digest],
      ["Authority", workspaceExport.authority.workspace_authority],
    ])),
    detailCard("Package counts", definitionList([
      ["Entries", workspaceExport.entries.length],
      ["Candidates", workspaceExport.candidate_references.length],
      ["Principia references", workspaceExport.principia_references.length],
      ["Warnings", workspaceExport.warning_references.length],
      ["Open questions", workspaceExport.open_questions.length],
    ])),
    detailCard("Ordered research decisions", list(decisions, "summary-list", true), true),
    detailCard("Accepted input boundary", definitionList([
      ["Export file", shellData.accepted_export.file],
      ["Export bytes", shellData.accepted_export.artifact.bytes],
      ["Export SHA-256", shellData.accepted_export.artifact.sha256],
      ["Manifest SHA-256", shellData.accepted_manifest.artifact.sha256],
    ]), true),
  );
  panel.append(grid);
  showOnly(panel);
  setDocumentTitle("Workspace overview");
}

function renderEntry(route) {
  const entry = workspaceExport.entries.find(candidate => candidate.entry_id === route.entry_id);
  if (!entry) return renderRouteFailure(location.hash, "The accepted export does not contain this entry.");
  const metadata = entry.visible_metadata;
  const panel = elements.contentPanel;
  panel.replaceChildren(
    panelHeading(
      `ENTRY ${entry.position} · ${label(entry.decision.action)}`,
      metadata.title,
      entry.decision.rationale,
    ),
  );
  panel.setAttribute("aria-labelledby", "active-view-title");
  panel.append(
    node("div", { className: "meta-row" }, [
      pill(exactKey(entry.exact_reference), "good"),
      pill(`Decision: ${label(entry.decision.action)}`),
      pill(`Original rank ${entry.original_rank}`),
      pill("Research only"),
    ]),
  );
  const grid = node("div", { className: "section-grid" });
  grid.append(
    detailCard("Exact reference", definitionList([
      ["Entity ID", entry.exact_reference.id],
      ["Revision", entry.exact_reference.revision],
      ["Entry ID", entry.entry_id],
      ["Position", entry.position],
    ])),
    detailCard("Decision record", definitionList([
      ["Decision ID", entry.decision.id],
      ["Action", entry.decision.action],
      ["Advisory only", entry.decision.advisory_only ? "yes" : "no"],
      ["Canonical mutation", entry.decision.canonical_mutation ? "enabled" : "blocked"],
    ])),
    detailCard("Visible Atlas metadata", definitionList([
      ["Type", metadata.type],
      ["Lifecycle status", metadata.status],
      ["Review level", metadata.review_level],
      ["Staleness", metadata.staleness],
    ])),
    detailCard("Provenance", metadata.provenance.length ? list(metadata.provenance, "reference-list") : node("p", { text: "No source entity is exposed for this exact record." })),
    detailCard("Rationale", node("p", { text: entry.decision.rationale }), true),
  );
  panel.append(grid);
  showOnly(panel);
  setDocumentTitle(`${entry.position}. ${metadata.title}`);
}

function renderCandidates() {
  const panel = elements.contentPanel;
  panel.replaceChildren(
    panelHeading(
      "ADVISORY CANDIDATES",
      "Potential contradiction and duplication remain unresolved",
      "Candidate records help inspection. They cannot resolve, merge, redirect, supersede, or mutate either referenced revision.",
    ),
  );
  panel.setAttribute("aria-labelledby", "active-view-title");
  const container = node("div", { className: "candidate-list" });
  for (const candidate of workspaceExport.candidate_references) {
    const card = node("article", { className: "candidate-card" });
    card.append(
      node("div", { className: "tag-row" }, [
        pill(label(candidate.kind)),
        pill(label(candidate.assessment), "warning"),
        pill("Unresolved", "good"),
        pill("Advisory only"),
      ]),
      node("h3", { text: candidate.id }),
      definitionList([
        ["Left", exactKey(candidate.left)],
        ["Right", exactKey(candidate.right)],
        ["Resolution", candidate.resolution],
        ["Automatic resolution", candidate.automatic_resolution ? "enabled" : "blocked"],
      ]),
    );
    container.append(card);
  }
  panel.append(container);
  showOnly(panel);
  setDocumentTitle("Advisory candidates");
}

function renderPrincipia() {
  const panel = elements.contentPanel;
  const reference = workspaceExport.principia_references[0];
  panel.replaceChildren(
    panelHeading(
      "PINNED OFFLINE PRINCIPIA REFERENCE",
      "Principia status remains separate",
      "This fixture proves that the workspace can carry an exact offline cross-repository reference without inheriting or changing status.",
    ),
  );
  panel.setAttribute("aria-labelledby", "active-view-title");
  const grid = node("div", { className: "section-grid" });
  grid.append(
    detailCard("Principia envelope", definitionList([
      ["Envelope", exactKey(reference)],
      ["Artifact", `${reference.principia_artifact_id}@${reference.principia_artifact_revision}`],
      ["Principia status", reference.principia_status],
      ["Status separate", reference.principia_status_separate ? "yes" : "no"],
      ["Fixture only", reference.fixture_only ? "yes" : "no"],
      ["Live dependency", reference.live ? "active" : "inactive"],
      ["Automatic inheritance", reference.automatic_status_inheritance ? "enabled" : "blocked"],
    ]), true),
    detailCard("Pinned Atlas references", exactReferenceList(reference.atlas_references), true),
  );
  panel.append(grid);
  showOnly(panel);
  setDocumentTitle("Principia reference");
}

function renderWarnings() {
  const panel = elements.contentPanel;
  panel.replaceChildren(
    panelHeading(
      "EXPLICIT WARNINGS",
      "Unavailable revisions fail visibly",
      "Warnings identify unavailable exact targets and never update, substitute, or remove workspace entries automatically.",
    ),
  );
  panel.setAttribute("aria-labelledby", "active-view-title");
  const container = node("div", { className: "warning-list" });
  for (const warning of workspaceExport.warning_references) {
    const card = node("article", { className: "warning-card" });
    card.append(
      node("div", { className: "tag-row" }, [
        pill(label(warning.impact_state), "danger"),
        pill(label(warning.severity), "warning"),
        pill("No automatic update", "good"),
      ]),
      node("h3", { text: exactKey(warning) }),
      node("p", { text: warning.message }),
      definitionList([
        ["Requested target", exactKey(warning.target)],
        ["Implicit latest", warning.implicit_latest ? "allowed" : "blocked"],
        ["Automatic update", warning.automatic_update ? "enabled" : "blocked"],
      ]),
    );
    container.append(card);
  }
  panel.append(container);
  showOnly(panel);
  setDocumentTitle("Warnings");
}

function renderQuestions() {
  const panel = elements.contentPanel;
  panel.replaceChildren(
    panelHeading(
      "OPEN QUESTIONS",
      "Questions remain research prompts, not authority",
      "These questions belong to the accepted research trail and do not create review, lifecycle, or publication decisions.",
    ),
    list(workspaceExport.open_questions, "question-list", true),
  );
  panel.setAttribute("aria-labelledby", "active-view-title");
  showOnly(panel);
  setDocumentTitle("Open questions");
}

function renderLimitations() {
  const panel = elements.contentPanel;
  panel.replaceChildren(
    panelHeading(
      "LIMITATIONS AND NON-GOALS",
      "Bounded evidence is not production proof",
      "The package states what it cannot establish so the interface does not overclaim its authority or coverage.",
    ),
    list(workspaceExport.limitations, "limitation-list"),
  );
  panel.setAttribute("aria-labelledby", "active-view-title");
  showOnly(panel);
  setDocumentTitle("Limitations");
}

function renderEvidence() {
  const panel = elements.contentPanel;
  panel.replaceChildren(
    panelHeading(
      "EXPORT AND MANIFEST EVIDENCE",
      "Accepted bytes are visible and locally downloadable",
      "The browser verifies the export SHA-256 before enabling download. Downloading creates no Atlas or Principia write.",
    ),
  );
  panel.setAttribute("aria-labelledby", "active-view-title");
  const grid = node("div", { className: "section-grid" });
  grid.append(
    detailCard("Accepted export", definitionList([
      ["Contract", shellData.accepted_export.contract],
      ["File", shellData.accepted_export.file],
      ["Bytes", shellData.accepted_export.artifact.bytes],
      ["SHA-256", shellData.accepted_export.artifact.sha256],
      ["Semantic digest", shellData.accepted_export.report_digest],
    ]), true),
    detailCard("Accepted manifest", definitionList([
      ["Contract", shellData.accepted_manifest.contract],
      ["File", shellData.accepted_manifest.file],
      ["Bytes", shellData.accepted_manifest.artifact.bytes],
      ["SHA-256", shellData.accepted_manifest.artifact.sha256],
      ["Semantic digest", shellData.accepted_manifest.report_digest],
    ]), true),
    detailCard("Local download boundary", definitionList([
      ["Filename", shellData.download.file],
      ["Byte identity", "required"],
      ["Network request", "none after local load"],
      ["Canonical write", shellData.download.canonical_write ? "enabled" : "blocked"],
    ]), true),
  );
  panel.append(grid);
  showOnly(panel);
  setDocumentTitle("Export evidence");
}

function renderSummary() {
  const panel = elements.contentPanel;
  panel.replaceChildren(
    panelHeading(
      "COMPLETE TEXT-ONLY PATH",
      "The entire decision sequence is available without a graph",
      "This ordered summary preserves the accepted entry order and provides a complete non-graph route through the research package.",
    ),
    list(workspaceExport.non_graph_summary, "summary-list", true),
  );
  panel.setAttribute("aria-labelledby", "active-view-title");
  showOnly(panel);
  setDocumentTitle("Text summary");
}

function renderRouteFailure(hash, detail = "No accepted workspace route matches this value.") {
  updateCurrentNavigation("");
  const panel = elements.errorPanel;
  panel.setAttribute("aria-labelledby", "route-error-title");
  const recovery = node("a", {
    className: "route-link",
    href: lastValidHash,
    text: "Return to the previous valid workspace view",
  });
  panel.replaceChildren(
    node("p", { className: "eyebrow", text: "EXPLICIT ROUTE FAILURE" }),
    node("h2", { id: "route-error-title", text: "Workspace route unavailable" }),
    node("p", { text: detail }),
    definitionList([
      ["Requested route", hash || "(empty)"],
      ["Fallback", "refused"],
      ["Previous valid route", lastValidHash],
      ["Workspace mutation", "none"],
    ]),
    recovery,
  );
  showOnly(panel);
  setDocumentTitle("Workspace route unavailable");
}

function renderRoute() {
  if (!shellData || !workspaceExport) return;
  const hash = location.hash || "#overview";
  const route = shellData.routes.find(candidate => candidate.hash === hash);
  if (!route) {
    renderRouteFailure(hash);
    return;
  }
  lastValidHash = hash;
  updateCurrentNavigation(hash);
  if (route.kind === "overview") renderOverview();
  else if (route.kind === "entry") renderEntry(route);
  else if (route.kind === "candidates") renderCandidates();
  else if (route.kind === "principia") renderPrincipia();
  else if (route.kind === "warnings") renderWarnings();
  else if (route.kind === "questions") renderQuestions();
  else if (route.kind === "limitations") renderLimitations();
  else if (route.kind === "evidence") renderEvidence();
  else if (route.kind === "summary") renderSummary();
  else renderRouteFailure(hash, "The route kind is not supported by this shell version.");
}

function downloadAcceptedExport() {
  if (!exportBytes) return;
  const blob = new Blob([exportBytes], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = node("a", { href: url, download: shellData.download.file });
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
  elements.runtimeDetail.textContent = "Accepted export downloaded locally · no repository write";
}

async function loadWorkspace() {
  try {
    const [shellResponse, exportResponse, manifestResponse] = await Promise.all([
      fetch(DATA_URLS.shell, { cache: "no-store" }),
      fetch(DATA_URLS.export, { cache: "no-store" }),
      fetch(DATA_URLS.manifest, { cache: "no-store" }),
    ]);
    if (!shellResponse.ok || !exportResponse.ok || !manifestResponse.ok) {
      throw new Error("One or more required local workspace artifacts are unavailable");
    }
    const [shellText, exportBuffer, manifestText] = await Promise.all([
      shellResponse.text(),
      exportResponse.arrayBuffer(),
      manifestResponse.text(),
    ]);
    shellData = JSON.parse(shellText);
    exportBytes = exportBuffer;
    workspaceExport = JSON.parse(new TextDecoder().decode(exportBuffer));
    workspaceManifest = JSON.parse(manifestText);
    await verifyPackage();

    renderNavigation();
    renderAuthoritySummary(shellData.authority);
    elements.downloadButton.disabled = false;
    elements.downloadButton.addEventListener("click", downloadAcceptedExport);
    elements.runtimeCard.classList.add("ready");
    elements.runtimeStatus.textContent = "Accepted workspace verified";
    elements.runtimeDetail.textContent = "Exact export SHA-256 matched · zero write authority";

    if (!location.hash) history.replaceState(null, "", "#overview");
    renderRoute();
  } catch (error) {
    elements.runtimeCard.classList.add("failed");
    elements.runtimeStatus.textContent = "Workspace package unavailable";
    elements.runtimeDetail.textContent = "The shell refused partial or mismatched local evidence";
    elements.errorPanel.setAttribute("aria-labelledby", "load-error-title");
    elements.errorPanel.replaceChildren(
      node("p", { className: "eyebrow", text: "EXPLICIT PACKAGE FAILURE" }),
      node("h2", { id: "load-error-title", text: "The accepted workspace could not be verified" }),
      node("p", { text: error instanceof Error ? error.message : "Unknown local package failure" }),
      node("p", { text: "No fallback data was loaded and no workspace state was changed." }),
    );
    showOnly(elements.errorPanel);
    setDocumentTitle("Workspace package unavailable");
  }
}

window.addEventListener("hashchange", renderRoute);
loadWorkspace();
