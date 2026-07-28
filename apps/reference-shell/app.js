const DATA_URL = "./data/reference-shell-data.json";

const elements = {
  statusCard: document.querySelector(".status-card"),
  runtimeStatus: document.querySelector("#runtime-status"),
  runtimeDetail: document.querySelector("#runtime-detail"),
  viewList: document.querySelector("#view-list"),
  failureButton: document.querySelector("#failure-button"),
  authoritySummary: document.querySelector("#authority-summary"),
  loadingPanel: document.querySelector("#loading-panel"),
  viewPanel: document.querySelector("#view-panel"),
  failurePanel: document.querySelector("#failure-panel"),
  errorPanel: document.querySelector("#error-panel"),
  main: document.querySelector("#main-content"),
};

let shellData = null;

function node(tag, options = {}, children = []) {
  const element = document.createElement(tag);
  for (const [key, value] of Object.entries(options)) {
    if (key === "className") element.className = value;
    else if (key === "text") element.textContent = value;
    else if (key.startsWith("aria-")) element.setAttribute(key, value);
    else if (key === "dataset") Object.assign(element.dataset, value);
    else element[key] = value;
  }
  for (const child of children) {
    element.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return element;
}

function exactKey(record) {
  return `${record.id}@${record.revision}`;
}

function label(value) {
  return String(value)
    .replaceAll("-", " ")
    .replace(/\b\w/g, character => character.toUpperCase());
}

function pill(text, tone = "") {
  return node("span", { className: `pill ${tone}`.trim(), text });
}

function definitionList(entries, className = "definition-list") {
  const list = node("dl", { className });
  for (const [term, description] of entries) {
    const wrapper = node("div");
    wrapper.append(
      node("dt", { text: term }),
      node("dd", { text: String(description) }),
    );
    list.append(wrapper);
  }
  return list;
}

function referenceList(references) {
  const list = node("ul", { className: "reference-list" });
  for (const reference of references) {
    const item = node("li", { className: "reference-item" });
    item.append(
      node("code", { text: reference.id }),
      node("small", { text: `Exact revision ${reference.revision}` }),
    );
    list.append(item);
  }
  return list;
}

function pathList(values) {
  const list = node("ol", { className: "path-list" });
  values.forEach((value, index) => {
    list.append(node("li", { className: "path-item", text: `${index + 1}. ${label(value)}` }));
  });
  return list;
}

function detailCard(title, content, full = false) {
  const card = node("section", { className: `detail-card${full ? " full" : ""}` });
  card.append(node("h3", { text: title }), content);
  return card;
}

function showOnly(panel) {
  for (const candidate of [elements.loadingPanel, elements.viewPanel, elements.failurePanel, elements.errorPanel]) {
    candidate.hidden = candidate !== panel;
  }
}

function updateCurrentNavigation(key) {
  for (const button of elements.viewList.querySelectorAll("button")) {
    if (button.dataset.key === key) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  }
  if (key === "failures") elements.failureButton.setAttribute("aria-current", "page");
  else elements.failureButton.removeAttribute("aria-current");
}

function renderAuthoritySummary(authority) {
  const entries = [
    ["Exact revisions", authority.exact_revision_required ? "required" : "missing"],
    ["Principia status", authority.principia_status_separate ? "separate" : "inherited"],
    ["Offline", authority.offline_capable ? "capable" : "required network"],
    ["Canonical writes", authority.canonical_mutation ? "enabled" : "blocked"],
    ["Live bridge", authority.live_principia_dependency ? "active" : "inactive"],
  ];
  elements.authoritySummary.replaceChildren();
  for (const [term, description] of entries) {
    const wrapper = node("div");
    wrapper.append(node("dt", { text: term }), node("dd", { text: description }));
    elements.authoritySummary.append(wrapper);
  }
}

function renderNavigation() {
  elements.viewList.replaceChildren();
  for (const view of shellData.views) {
    const key = exactKey(view);
    const button = node("button", {
      className: "view-button",
      type: "button",
      dataset: { key },
      "aria-label": `${view.title}, ${label(view.kind)}`,
    });
    button.append(node("span", { text: label(view.kind) }), node("strong", { text: view.title }));
    button.addEventListener("click", () => {
      location.hash = `view=${encodeURIComponent(key)}`;
    });
    elements.viewList.append(node("li", {}, [button]));
  }
  elements.failureButton.addEventListener("click", () => {
    location.hash = "failures";
  });
}

function renderGeneratedArtifact(artifact) {
  if (!artifact) return node("p", { text: "This view reads canonical exact revisions directly." });
  return definitionList([
    ["Contract", artifact.contract],
    ["Build digest", artifact.build_digest],
    ["Source digest", artifact.source_digest],
    ["Authority", artifact.advisory_only ? "advisory only" : "unexpected authority"],
    ["Replaceable", artifact.replaceable ? "yes" : "no"],
  ]);
}

function renderPrincipiaEnvelope() {
  const record = shellData.principia_references[0];
  if (!record) return node("p", { text: "No Principia reference fixture is available." });
  const container = node("div");
  container.append(
    definitionList([
      ["Principia artifact", record.principia_artifact_id],
      ["Principia revision", record.principia_artifact_revision],
      ["Principia status", record.principia_status],
      ["Impact state", record.impact_state],
      ["Purpose", record.reference_purpose],
    ]),
    node("h3", { text: "Pinned Atlas references" }),
    referenceList(record.atlas_references),
  );
  return container;
}

function renderImpactWarning() {
  const warning = shellData.impact_warnings[0];
  if (!warning) return node("p", { text: "No impact-warning fixture is available." });
  const container = node("div");
  container.append(
    node("div", { className: "tag-row" }, [
      pill(label(warning.impact_state), "danger"),
      pill(label(warning.severity), "warning"),
      pill("No automatic update", "good"),
    ]),
    node("p", { text: warning.message }),
    definitionList([
      ["Requested target", exactKey(warning.target)],
      ["Available revisions", warning.available_revisions.join(", ")],
    ]),
    node("h3", { text: "Recovery actions" }),
    pathList(warning.recovery_actions),
  );
  return container;
}

function renderView(view) {
  updateCurrentNavigation(exactKey(view));
  const panel = elements.viewPanel;
  panel.replaceChildren();

  const heading = node("div");
  heading.append(
    node("p", { className: "eyebrow", text: label(view.kind) }),
    node("h2", { text: view.title }),
  );
  const metadata = node("div", { className: "meta-row" }, [
    pill(`View revision ${view.revision}`, "good"),
    pill(`${view.atlas_refs.length} exact Atlas reference${view.atlas_refs.length === 1 ? "" : "s"}`),
    pill("Advisory only"),
    pill("Offline fixture"),
  ]);

  const authorityEntries = Object.entries(view.authority).map(([key, value]) => [label(key), value ? "visible" : "hidden"]);
  const grid = node("div", { className: "section-grid" });
  grid.append(
    detailCard("Exact Atlas references", referenceList(view.atlas_refs), true),
    detailCard("Authority metadata", definitionList(authorityEntries)),
    detailCard("Deterministic route", node("code", { text: view.route })),
    detailCard("Keyboard path", pathList(view.keyboard_path)),
    detailCard("Equivalent non-graph path", pathList(view.non_graph_path)),
    detailCard("Generated evidence", renderGeneratedArtifact(view.generated_artifact), true),
  );

  if (view.kind === "principia-reference") {
    grid.append(detailCard("Offline Principia envelope", renderPrincipiaEnvelope(), true));
  }
  if (view.kind === "impact-warning") {
    grid.append(detailCard("Cross-repository impact warning", renderImpactWarning(), true));
  }

  panel.append(heading, metadata, grid);
  showOnly(panel);
  document.title = `${view.title} · Atlas Reference Shell`;
}

function renderFailures() {
  updateCurrentNavigation("failures");
  const panel = elements.failurePanel;
  panel.replaceChildren(
    node("p", { className: "eyebrow", text: "DETERMINISTIC FAILURE STATES" }),
    node("h2", { text: "Failure is visible, bounded, and non-mutating" }),
    node("p", { text: "Each failure preserves the previous state, refuses silent fallback, and offers explicit recovery actions." }),
  );
  const list = node("ul", { className: "failure-list" });
  for (const failure of shellData.failure_states) {
    const item = node("li", { className: "failure-item" });
    item.append(
      node("p", { className: "eyebrow", text: label(failure.category) }),
      node("h3", { text: failure.summary }),
      node("code", { text: failure.error_code }),
      node("p", { text: `Recovery: ${failure.recovery_actions.map(label).join(" → ")}` }),
    );
    list.append(item);
  }
  panel.append(list);
  showOnly(panel);
  document.title = "Failure states · Atlas Reference Shell";
}

function renderRoute() {
  if (!shellData) return;
  const fragment = location.hash.slice(1);
  if (fragment === "failures") {
    renderFailures();
    return;
  }
  const value = fragment.startsWith("view=") ? decodeURIComponent(fragment.slice(5)) : "";
  const view = shellData.views.find(candidate => exactKey(candidate) === value) ?? shellData.views[0];
  if (!value && view) history.replaceState(null, "", `#view=${encodeURIComponent(exactKey(view))}`);
  renderView(view);
}

function showError(error) {
  elements.statusCard.classList.add("error");
  elements.runtimeStatus.textContent = "Local fixture unavailable";
  elements.runtimeDetail.textContent = "Canonical knowledge remains unchanged";
  elements.errorPanel.replaceChildren(
    node("p", { className: "eyebrow", text: "EXPLICIT FAILURE" }),
    node("h2", { text: "The generated local artifact could not be loaded" }),
    node("p", { text: error instanceof Error ? error.message : String(error) }),
    node("p", { text: "Run the deterministic shell builder, then serve this directory through a local static server. No fallback to a live service is attempted." }),
  );
  showOnly(elements.errorPanel);
}

async function start() {
  const response = await fetch(DATA_URL, { cache: "no-store" });
  if (!response.ok) throw new Error(`Could not load ${DATA_URL}: HTTP ${response.status}`);
  shellData = await response.json();
  if (shellData.contract !== "atlas-reference-shell-data/0.1") {
    throw new Error(`Unsupported shell data contract: ${shellData.contract ?? "missing"}`);
  }
  renderNavigation();
  renderAuthoritySummary(shellData.authority);
  elements.statusCard.classList.add("ready");
  elements.runtimeStatus.textContent = "Local fixture ready";
  elements.runtimeDetail.textContent = `${shellData.views.length} views · ${shellData.entity_count} canonical entities`;
  window.addEventListener("hashchange", renderRoute);
  renderRoute();
}

start().catch(showError);
