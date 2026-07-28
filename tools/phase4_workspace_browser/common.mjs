import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const PACKAGE_DIR = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_ROOT = path.resolve(PACKAGE_DIR, "../..");
let routesById = new Map();

export function setRoutes(routes) { routesById = new Map(routes.map(route => [route.id, route])); }

export function parseArgs(argv) {
  const result = {
    baseUrl: "http://127.0.0.1:8770",
    repoRoot: DEFAULT_ROOT,
    shellDir: path.join(DEFAULT_ROOT, "phase4-workspace-shell"),
    outputDir: path.join(DEFAULT_ROOT, "phase4-workspace-browser-evidence"),
  };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--base-url") result.baseUrl = argv[++index];
    else if (value === "--repo-root") result.repoRoot = path.resolve(argv[++index]);
    else if (value === "--shell-dir") result.shellDir = path.resolve(argv[++index]);
    else if (value === "--output-dir") result.outputDir = path.resolve(argv[++index]);
    else throw new Error(`Unknown argument: ${value}`);
  }
  return result;
}

export function stableValue(value) {
  if (Array.isArray(value)) return value.map(stableValue);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.keys(value).sort().map(key => [key, stableValue(value[key])]));
  }
  return value;
}

export function renderJson(value) {
  return `${JSON.stringify(stableValue(value), null, 2)}\n`;
}

export function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

export function seal(record) {
  const unsigned = { ...record };
  delete unsigned.report_digest;
  return { ...record, report_digest: sha256(Buffer.from(renderJson(unsigned))) };
}

export function assertEvidence(condition, code, message) {
  if (!condition) {
    const error = new Error(`${code}: ${message}`);
    error.code = code;
    throw error;
  }
}

export async function readJson(filePath) {
  return JSON.parse(await readFile(filePath, "utf8"));
}

export function normalizeUrl(raw, baseUrl) {
  if (raw.startsWith("blob:")) return "blob:local-download";
  const parsed = new URL(raw);
  const base = new URL(baseUrl);
  if (parsed.origin === base.origin) return `${parsed.pathname}${parsed.search}${parsed.hash}`;
  return `${parsed.protocol}//${parsed.hostname}${parsed.port ? `:${parsed.port}` : ""}${parsed.pathname}${parsed.search}`;
}

export function requestRecord(request, baseUrl, decision) {
  return {
    decision,
    method: request.method(),
    resource_type: request.resourceType(),
    url: normalizeUrl(request.url(), baseUrl),
  };
}

export async function installNetworkPolicy(context, baseUrl, records, blockedPaths = new Set()) {
  const allowedOrigin = new URL(baseUrl).origin;
  await context.route("**/*", async route => {
    const request = route.request();
    const parsed = new URL(request.url());
    if (parsed.origin !== allowedOrigin) {
      records.push(requestRecord(request, baseUrl, "blocked-external"));
      await route.abort("blockedbyclient");
      return;
    }
    if (blockedPaths.has(parsed.pathname)) {
      records.push(requestRecord(request, baseUrl, "blocked-test-loopback"));
      await route.abort("failed");
      return;
    }
    records.push(requestRecord(request, baseUrl, "allowed-loopback"));
    await route.continue();
  });
}

export async function waitReady(page) {
  await page.waitForFunction(() => document.querySelector("#runtime-status")?.textContent === "Accepted workspace verified");
}

export async function focusEvidence(page) {
  return page.evaluate(() => {
    const active = document.activeElement;
    if (!(active instanceof HTMLElement)) return { descriptor: "none", tag: "none", visible: false };
    let descriptor = active.id || active.dataset.routeId || active.getAttribute("aria-label") || active.textContent?.trim() || active.tagName.toLowerCase();
    if (active.classList.contains("skip-link")) descriptor = "skip-link";
    const style = getComputedStyle(active);
    const outlineVisible = style.outlineStyle !== "none" && parseFloat(style.outlineWidth || "0") > 0;
    const shadowVisible = style.boxShadow !== "none";
    return {
      descriptor: String(descriptor).replace(/\s+/g, " ").trim(),
      tag: active.tagName.toLowerCase(),
      visible: active.matches(":focus-visible") && (outlineVisible || shadowVisible),
    };
  });
}

export async function semantics(page) {
  return page.evaluate(() => ({
    language: document.documentElement.lang,
    title: document.title,
    landmarks: {
      banner: document.querySelectorAll("header").length,
      navigation: document.querySelectorAll("nav").length,
      main: document.querySelectorAll("main").length,
      contentinfo: document.querySelectorAll("footer").length,
    },
    headings: [...document.querySelectorAll("h1, h2, h3, h4, h5, h6")].map(node => ({
      level: Number(node.tagName.slice(1)),
      text: node.textContent?.replace(/\s+/g, " ").trim() ?? "",
    })),
    named_buttons: [...document.querySelectorAll("button")].every(button => Boolean(button.getAttribute("aria-label") || button.textContent?.trim())),
    live_regions: document.querySelectorAll('[role="status"], [role="alert"], [aria-live]').length,
    alert_regions: document.querySelectorAll('[role="alert"]').length,
    main_labelled: Boolean(document.querySelector("main")?.getAttribute("aria-labelledby") || document.querySelector("main")?.getAttribute("aria-label")),
  }));
}

export function routeHash(routeId) {
  const route = routesById.get(routeId);
  if (!route) throw new Error(`Unknown expected route ${routeId}`);
  return route.hash;
}

export async function currentView(page) {
  return page.evaluate(() => ({
    hash: location.hash,
    heading: document.querySelector("#content-panel:not([hidden]) #active-view-title, #error-panel:not([hidden]) h2")?.textContent?.trim() ?? null,
    current_route: document.querySelector('a[aria-current="page"]')?.dataset.routeId ?? null,
    error_hidden: document.querySelector("#error-panel")?.hidden ?? null,
    status: document.querySelector("#runtime-status")?.textContent ?? null,
  }));
}

export async function openRoute(page, routeId) {
  await page.locator(`a[data-route-id="${routeId.replaceAll('"', '\\"')}"]`).click();
  await page.waitForFunction(expected => location.hash === expected, routeHash(routeId));
  await page.waitForFunction(expected => document.querySelector(`a[data-route-id="${expected}"]`)?.getAttribute("aria-current") === "page", routeId);
  return currentView(page);
}

export async function readDownload(download) {
  const stream = await download.createReadStream();
  const chunks = [];
  for await (const chunk of stream) chunks.push(chunk);
  return Buffer.concat(chunks);
}
