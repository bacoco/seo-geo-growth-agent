#!/usr/bin/env node
/**
 * Capture desktop and mobile screenshots for an audited page.
 *
 * Preferred workflow: use Agent Browser when the agent runtime exposes it.
 * This script is the deterministic fallback for local environments with Chrome.
 */
import { spawn } from "node:child_process";
import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import net from "node:net";

function parseArgs(argv) {
  const args = {
    outputDir: "screenshots",
    evidenceOut: "",
    evidenceEngineOut: "",
    studyOut: "",
    url: "",
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--url") args.url = argv[++i];
    else if (arg === "--output-dir") args.outputDir = argv[++i];
    else if (arg === "--evidence-out") args.evidenceOut = argv[++i];
    else if (arg === "--evidence-engine-out") args.evidenceEngineOut = argv[++i];
    else if (arg === "--study-out") args.studyOut = argv[++i];
    else if (arg === "--help" || arg === "-h") {
      usage();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  if (!args.url) throw new Error("--url is required");
  return args;
}

function usage() {
  console.log(`Usage: node scripts/capture_site_screenshots.mjs --url URL --output-dir DIR [--evidence-out site-visual-evidence.json] [--study-out responsive-study.json] [--evidence-engine-out evidence-engine.json]`);
}

function detectChrome() {
  const candidates = [
    process.env.CHROME_PATH,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ].filter(Boolean);
  for (const candidate of candidates) {
    if (existsSync(candidate)) return candidate;
  }
  throw new Error("Chrome/Chromium not found. Set CHROME_PATH or use Agent Browser screenshots.");
}

function freePort() {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.on("error", reject);
    server.listen(0, "127.0.0.1", () => {
      const address = server.address();
      server.close(() => resolve(address.port));
    });
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForJson(url, attempts = 80) {
  for (let i = 0; i < attempts; i += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
    } catch {
      // Keep polling until Chrome DevTools is ready.
    }
    await sleep(250);
  }
  throw new Error(`DevTools endpoint unavailable: ${url}`);
}

async function connectWebSocket(url) {
  const socket = new WebSocket(url);
  await new Promise((resolve, reject) => {
    socket.onopen = resolve;
    socket.onerror = reject;
  });
  let nextId = 1;
  const callbacks = new Map();
  const events = [];
  socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (!message.id && message.method) {
      events.push(message);
      return;
    }
    if (!message.id || !callbacks.has(message.id)) return;
    const { resolve, reject } = callbacks.get(message.id);
    callbacks.delete(message.id);
    if (message.error) reject(new Error(JSON.stringify(message.error)));
    else resolve(message.result || {});
  };
  function send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = nextId;
      nextId += 1;
      callbacks.set(id, { resolve, reject });
      socket.send(JSON.stringify({ id, method, params }));
    });
  }
  return { socket, send, events };
}

function hostname(value) {
  try {
    return new URL(value).hostname;
  } catch {
    return "";
  }
}

function eventParams(events, method) {
  return events.filter((event) => event.method === method).map((event) => event.params || {});
}

function lowerHeaders(headers = {}) {
  const out = {};
  for (const [key, value] of Object.entries(headers || {})) {
    out[String(key).toLowerCase()] = String(value);
  }
  return out;
}

async function readLayout(send) {
  const layout = await send("Runtime.evaluate", {
    expression: `JSON.stringify((() => {
      const doc = document.documentElement;
      const body = document.body || {};
      const headings = Array.from(document.querySelectorAll("h1"))
        .map((node) => (node.innerText || node.textContent || "").trim())
        .filter(Boolean)
        .slice(0, 5);
      const navLinks = Array.from(document.querySelectorAll("nav a, [role='navigation'] a, header a"))
        .map((node) => (node.innerText || node.textContent || "").trim())
        .filter(Boolean);
      const images = Array.from(document.images || []).map((img, index) => {
        const rect = img.getBoundingClientRect();
        return {
          index,
          src: img.currentSrc || img.src || img.getAttribute("src") || "",
          loading: img.getAttribute("loading") || "",
          complete: Boolean(img.complete),
          naturalWidth: img.naturalWidth || 0,
          naturalHeight: img.naturalHeight || 0,
          renderedWidth: Math.round(rect.width),
          renderedHeight: Math.round(rect.height),
          top: Math.round(rect.top + window.scrollY),
          bottom: Math.round(rect.bottom + window.scrollY),
          inViewport: rect.bottom >= 0 && rect.top <= window.innerHeight
        };
      });
      const isVisible = (node) => {
        const rect = node.getBoundingClientRect();
        const style = window.getComputedStyle(node);
        return rect.width > 0 && rect.height > 0 && rect.bottom >= 0 && rect.top <= window.innerHeight && style.visibility !== "hidden" && style.display !== "none";
      };
      const ctaPattern = /(contact|demo|start|book|buy|subscribe|download|get started|try|essai|devis|réserver|commencer|acheter|télécharger)/i;
      const ctaNodes = Array.from(document.querySelectorAll("a, button, input[type='submit'], [role='button']"));
      const visibleCtas = ctaNodes
        .filter(isVisible)
        .map((node) => (node.innerText || node.value || node.getAttribute("aria-label") || node.textContent || "").trim())
        .filter((label) => label && ctaPattern.test(label));
      const trustPattern = /(trusted by|client|customer|case study|review|testimonial|security|certified|press|award|partner|institution|universit|public institution|avis|témoignage|partenaire|certifié|presse)/i;
      const firstScreenText = Array.from(document.body ? document.body.querySelectorAll("body *") : [])
        .filter(isVisible)
        .map((node) => (node.innerText || node.textContent || "").trim())
        .filter(Boolean)
        .join(" ")
        .slice(0, 5000);
      const main = document.querySelector("main, [role='main'], header, .hero, section");
      const heroRect = main ? main.getBoundingClientRect() : { height: 0, bottom: 0 };
      const missingImages = images.filter((img) => !img.complete || img.naturalWidth === 0).length;
      return {
        title: document.title,
        innerWidth,
        innerHeight,
        scrollWidth: doc.scrollWidth,
        bodyScrollWidth: body.scrollWidth || 0,
        horizontalOverflow: doc.scrollWidth > innerWidth || (body.scrollWidth || 0) > innerWidth,
        documentHeight: Math.max(doc.scrollHeight, body.scrollHeight || 0),
        hasViewportMeta: Boolean(document.querySelector("meta[name='viewport']")),
        h1Count: headings.length,
        h1Text: headings,
        navLinkCount: navLinks.length,
        imageCount: images.length,
        missingImages,
        images,
        firstScreen: {
          cta_visible: visibleCtas.length > 0,
          cta_labels: visibleCtas.slice(0, 5),
          trust_signal_visible: trustPattern.test(firstScreenText),
          hero_height: Math.round(heroRect.height || 0),
          hero_height_ratio: Number(((heroRect.height || 0) / Math.max(1, window.innerHeight)).toFixed(2)),
          next_section_visible: Boolean(heroRect.bottom && heroRect.bottom < window.innerHeight * 0.96)
        },
        visibleTextLength: (body.innerText || "").trim().length,
        textSample: (body.innerText || "").trim().replace(/\\s+/g, " ").slice(0, 240)
      };
    })())`,
    returnByValue: true,
  });
  return JSON.parse(layout.result.value);
}

async function scrollThroughPage(send) {
  const metricsResult = await send("Runtime.evaluate", {
    expression: `JSON.stringify((() => {
      const doc = document.documentElement;
      const body = document.body || {};
      const documentHeight = Math.max(doc.scrollHeight, body.scrollHeight || 0);
      return {
        innerHeight: window.innerHeight,
        documentHeight,
        maxScroll: Math.max(0, documentHeight - window.innerHeight)
      };
    })())`,
    returnByValue: true,
  });
  const metrics = JSON.parse(metricsResult.result.value);
  const stepSize = Math.max(320, Math.floor(metrics.innerHeight * 0.75));
  let steps = 0;
  for (let y = 0; y < metrics.maxScroll; y += stepSize) {
    await send("Runtime.evaluate", { expression: `window.scrollTo(0, ${y}); true`, returnByValue: true });
    steps += 1;
    await sleep(260);
  }
  if (metrics.maxScroll > 0) {
    await send("Runtime.evaluate", { expression: `window.scrollTo(0, ${metrics.maxScroll}); true`, returnByValue: true });
    steps += 1;
    await sleep(360);
  }
  await send("Runtime.evaluate", {
    expression: `(async () => {
      const pending = Array.from(document.images || []).filter((img) => !img.complete);
      await Promise.all(pending.map((img) => new Promise((resolve) => {
        img.addEventListener("load", resolve, { once: true });
        img.addEventListener("error", resolve, { once: true });
        setTimeout(resolve, 1200);
      })));
      return true;
    })()`,
    awaitPromise: true,
    returnByValue: true,
  });
  await send("Runtime.evaluate", { expression: "window.scrollTo(0, 0); true", returnByValue: true });
  await sleep(160);
  return {
    scrollSteps: steps,
    maxScroll: metrics.maxScroll,
    documentHeight: metrics.documentHeight,
  };
}

function imageKey(image) {
  return image.src || `image-${image.index}`;
}

function isLoaded(image) {
  return Boolean(image.complete && image.naturalWidth > 0);
}

function summarizeImageLoading(initialImages = [], finalImages = []) {
  const initialByKey = new Map(initialImages.map((image) => [imageKey(image), image]));
  const loadedInitially = finalImages.filter((image) => isLoaded(initialByKey.get(imageKey(image)) || {})).length;
  const loadedAfterScroll = finalImages.filter((image) => isLoaded(image) && !isLoaded(initialByKey.get(imageKey(image)) || {})).length;
  const broken = finalImages.filter((image) => image.complete && image.naturalWidth === 0).length;
  const stillDeferred = finalImages.filter((image) => !image.complete).length;
  const unresolved = finalImages
    .filter((image) => !isLoaded(image))
    .slice(0, 5)
    .map((image) => ({
      src: image.src,
      loading: image.loading,
      complete: image.complete,
      naturalWidth: image.naturalWidth,
      top: image.top,
    }));
  return {
    total: finalImages.length,
    lazy: finalImages.filter((image) => image.loading.toLowerCase() === "lazy").length,
    loaded_initially: loadedInitially,
    loaded_after_scroll: loadedAfterScroll,
    broken,
    still_deferred: stillDeferred,
    initial_missing: initialImages.filter((image) => !isLoaded(image)).length,
    missing_after_scroll: broken + stillDeferred,
    unresolved_sample: unresolved,
  };
}

async function captureViewport(send, url, viewport, outputPath) {
  await send("Page.enable");
  await send("Runtime.enable");
  await send("Emulation.setDeviceMetricsOverride", {
    width: viewport.width,
    height: viewport.height,
    deviceScaleFactor: 1,
    mobile: viewport.mobile,
  });
  await send("Page.navigate", { url });
  await sleep(1400);
  const initialLayout = await readLayout(send);
  const scrollProbe = await scrollThroughPage(send);
  const finalLayout = await readLayout(send);
  finalLayout.initialMissingImages = initialLayout.missingImages;
  finalLayout.imageLoadStates = summarizeImageLoading(initialLayout.images, finalLayout.images);
  finalLayout.scrollProbe = scrollProbe;
  const screenshot = await send("Page.captureScreenshot", {
    format: "png",
    fromSurface: true,
    captureBeyondViewport: false,
  });
  writeFileSync(outputPath, Buffer.from(screenshot.data, "base64"));
  return finalLayout;
}

function analyzeViewport(layout) {
  const issues = [];
  if (layout.horizontalOverflow) issues.push("Horizontal overflow detected.");
  if (!layout.hasViewportMeta) issues.push("Missing viewport meta tag.");
  if (!layout.title) issues.push("Missing document title.");
  if (layout.h1Count === 0) issues.push("No visible H1 detected.");
  if (layout.h1Count > 2) issues.push(`Multiple H1 elements detected (${layout.h1Count}).`);
  const imageStates = layout.imageLoadStates || null;
  if (imageStates) {
    if (imageStates.broken > 0) issues.push(`${imageStates.broken} image(s) are broken after scroll.`);
    if (imageStates.still_deferred > 0) issues.push(`${imageStates.still_deferred} image(s) remain deferred after scroll.`);
  } else if (layout.missingImages > 0) {
    issues.push(`${layout.missingImages} image(s) did not load.`);
  }
  if (layout.visibleTextLength < 120) issues.push("Very little visible text detected.");
  return {
    status: issues.length ? "warning" : "pass",
    issues,
  };
}

function summarizeStudy(viewports) {
  const issueCount = viewports.reduce((sum, item) => sum + item.issues.length, 0);
  const hasMobileOverflow = viewports.some((item) => item.label === "Mobile" && item.metrics.horizontalOverflow);
  if (issueCount === 0) {
    return {
      status: "pass",
      verdict: "Homepage responds correctly on tested mobile and desktop viewports.",
    };
  }
  if (hasMobileOverflow) {
    return {
      status: "warning",
      verdict: "Homepage has responsive issues on mobile that should be fixed before relying on visual/agent readability.",
    };
  }
  return {
    status: "warning",
    verdict: "Homepage renders on tested viewports, but browser evidence found issues to review.",
  };
}

function classifyConsoleMessage(item, targetUrl) {
  const text = `${item.text || item.args?.map((arg) => arg.value || arg.description || "").join(" ") || ""}`;
  const sourceHost = hostname(item.url || item.stackTrace?.callFrames?.[0]?.url || "");
  const targetHost = hostname(targetUrl);
  if (/Content Security Policy|CORS|Mixed Content|Permissions-Policy|Refused/i.test(text)) return "browser_policy";
  if (sourceHost && targetHost && sourceHost !== targetHost) return "third_party";
  if (sourceHost && targetHost && sourceHost === targetHost) return "first_party";
  return "unknown";
}

function summarizeConsole(events, targetUrl) {
  const runtimeMessages = eventParams(events, "Runtime.consoleAPICalled").map((item) => ({
    level: item.type || "log",
    text: (item.args || []).map((arg) => arg.value || arg.description || "").filter(Boolean).join(" ").slice(0, 500),
    url: item.stackTrace?.callFrames?.[0]?.url || "",
  }));
  const logMessages = eventParams(events, "Log.entryAdded").map((item) => ({
    level: item.entry?.level || "log",
    text: String(item.entry?.text || "").slice(0, 500),
    url: item.entry?.url || "",
  }));
  const messages = [...runtimeMessages, ...logMessages]
    .filter((item) => item.text || item.url)
    .map((item) => ({ ...item, classification: classifyConsoleMessage(item, targetUrl) }));
  const byClassification = {};
  for (const item of messages) {
    byClassification[item.classification] = (byClassification[item.classification] || 0) + 1;
  }
  return {
    summary: {
      total: messages.length,
      errors: messages.filter((item) => /error|assert/i.test(item.level)).length,
      warnings: messages.filter((item) => /warn|warning/i.test(item.level)).length,
      by_classification: byClassification,
    },
    sample: messages.slice(0, 12),
  };
}

function summarizeNetwork(events) {
  const responses = eventParams(events, "Network.responseReceived").map((item) => ({
    url: item.response?.url || "",
    type: item.type || "",
    status: item.response?.status || 0,
    mime_type: item.response?.mimeType || "",
    from_disk_cache: Boolean(item.response?.fromDiskCache),
    from_service_worker: Boolean(item.response?.fromServiceWorker),
    headers: lowerHeaders(item.response?.headers || {}),
  }));
  const failures = eventParams(events, "Network.loadingFailed").map((item) => ({
    request_id: item.requestId || "",
    type: item.type || "",
    error_text: item.errorText || "",
    blocked_reason: item.blockedReason || "",
  }));
  const statusCounts = {};
  for (const response of responses) {
    const key = String(response.status || "unknown");
    statusCounts[key] = (statusCounts[key] || 0) + 1;
  }
  return {
    summary: {
      response_count: responses.length,
      failed_requests: failures.length,
      status_counts: statusCounts,
      non_2xx_3xx: responses.filter((item) => item.status >= 400).length,
    },
    failed_sample: failures.slice(0, 12),
    response_sample: responses.slice(0, 12).map((item) => ({
      url: item.url,
      type: item.type,
      status: item.status,
      mime_type: item.mime_type,
    })),
    responses,
  };
}

function summarizeCacheCdn(networkWatch, targetUrl) {
  const targetHost = hostname(targetUrl);
  const responses = networkWatch.responses || [];
  const documentResponse = responses.find((item) => item.type === "Document" && (!targetHost || hostname(item.url) === targetHost)) || responses[0] || null;
  if (!documentResponse) {
    return {
      status: "not_available",
      verdict: "No response headers were captured for cache/CDN diagnostics.",
      headers: {},
    };
  }
  const headers = documentResponse.headers || {};
  const selected = {};
  for (const key of ["cache-control", "cdn-cache-control", "cf-cache-status", "x-cache", "x-vercel-cache", "age", "etag", "last-modified", "server"]) {
    if (headers[key]) selected[key] = headers[key];
  }
  const cacheSignals = Object.keys(selected).filter((key) => /cache|age|etag|last-modified/i.test(key));
  return {
    status: Object.keys(selected).length ? "headers_available" : "headers_sparse",
    verdict: cacheSignals.length
      ? "Cache/CDN headers captured; compare with deployment state before calling a page stale."
      : "Response captured, but cache/CDN headers are sparse.",
    url: documentResponse.url,
    status_code: documentResponse.status,
    headers: selected,
  };
}

function summarizeDesignMetrics(responsiveViewports) {
  const output = {};
  for (const viewport of responsiveViewports) {
    output[String(viewport.label || "viewport").toLowerCase()] = viewport.metrics?.firstScreen || {};
  }
  return output;
}

function buildEvidenceEngine(url, events, responsiveViewports) {
  const consoleWatch = summarizeConsole(events, url);
  const networkWatch = summarizeNetwork(events);
  const cacheCdnWatch = summarizeCacheCdn(networkWatch, url);
  const { responses, ...networkPublic } = networkWatch;
  return {
    url,
    generated_at: new Date().toISOString(),
    method: "Chrome DevTools fallback",
    console_watch: consoleWatch,
    network_watch: networkPublic,
    cache_cdn_watch: cacheCdnWatch,
    design_watch_metrics: summarizeDesignMetrics(responsiveViewports),
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  mkdirSync(args.outputDir, { recursive: true });
  const chrome = detectChrome();
  const port = await freePort();
  const userDataDir = join(tmpdir(), `seo-geo-report-chrome-${Date.now()}`);
  const chromeProcess = spawn(chrome, [
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    `--remote-debugging-port=${port}`,
    "--remote-allow-origins=*",
    `--user-data-dir=${userDataDir}`,
    "--no-first-run",
    "--no-default-browser-check",
    "about:blank",
  ], { stdio: "ignore" });

  try {
    await waitForJson(`http://127.0.0.1:${port}/json/version`);
    const targetResponse = await fetch(`http://127.0.0.1:${port}/json/new?${encodeURIComponent("about:blank")}`, { method: "PUT" });
    const target = await targetResponse.json();
    const { socket, send, events } = await connectWebSocket(target.webSocketDebuggerUrl);
    await send("Page.enable");
    await send("Runtime.enable");
    await send("Log.enable");
    await send("Network.enable");
    const viewports = [
      { label: "Desktop", file: "desktop.png", width: 1440, height: 1800, mobile: false },
      { label: "Mobile", file: "mobile.png", width: 390, height: 1400, mobile: true },
    ];
    const evidence = [];
    const responsiveViewports = [];
    for (const viewport of viewports) {
      const outputPath = join(args.outputDir, viewport.file);
      const layout = await captureViewport(send, args.url, viewport, outputPath);
      const analysis = analyzeViewport(layout);
      evidence.push({
        label: `${viewport.label} screenshot`,
        path: viewport.file,
        viewport: `${viewport.width}x${viewport.height}`,
        notes: [
          `Page title: ${layout.title || "unknown"}`,
          `Horizontal overflow: ${layout.horizontalOverflow ? "yes" : "no"}`,
          `Document width: ${layout.scrollWidth}px`,
        ],
      });
      responsiveViewports.push({
        label: viewport.label,
        viewport: `${viewport.width}x${viewport.height}`,
        status: analysis.status,
        issues: analysis.issues,
        metrics: layout,
      });
      console.log(`Wrote ${outputPath}`);
    }
    if (args.evidenceOut) {
      writeFileSync(args.evidenceOut, `${JSON.stringify(evidence, null, 2)}\n`);
      console.log(`Wrote ${args.evidenceOut}`);
    }
    if (args.studyOut) {
      const summary = summarizeStudy(responsiveViewports);
      const study = {
        url: args.url,
        generated_at: new Date().toISOString(),
        method: "Chrome DevTools fallback; prefer Agent Browser when available",
        summary,
        viewports: responsiveViewports,
      };
      writeFileSync(args.studyOut, `${JSON.stringify(study, null, 2)}\n`);
      console.log(`Wrote ${args.studyOut}`);
    }
    if (args.evidenceEngineOut) {
      const evidenceEngine = buildEvidenceEngine(args.url, events, responsiveViewports);
      writeFileSync(args.evidenceEngineOut, `${JSON.stringify(evidenceEngine, null, 2)}\n`);
      console.log(`Wrote ${args.evidenceEngineOut}`);
    }
    socket.close();
  } finally {
    chromeProcess.kill("SIGTERM");
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
