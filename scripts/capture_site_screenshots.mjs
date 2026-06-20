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
    url: "",
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--url") args.url = argv[++i];
    else if (arg === "--output-dir") args.outputDir = argv[++i];
    else if (arg === "--evidence-out") args.evidenceOut = argv[++i];
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
  console.log(`Usage: node scripts/capture_site_screenshots.mjs --url URL --output-dir DIR [--evidence-out site-visual-evidence.json]`);
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
  socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
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
  return { socket, send };
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
  const layout = await send("Runtime.evaluate", {
    expression: `JSON.stringify({
      title: document.title,
      innerWidth,
      scrollWidth: document.documentElement.scrollWidth,
      bodyScrollWidth: document.body.scrollWidth,
      horizontalOverflow: document.documentElement.scrollWidth > innerWidth || document.body.scrollWidth > innerWidth
    })`,
    returnByValue: true,
  });
  const screenshot = await send("Page.captureScreenshot", {
    format: "png",
    fromSurface: true,
    captureBeyondViewport: false,
  });
  writeFileSync(outputPath, Buffer.from(screenshot.data, "base64"));
  return JSON.parse(layout.result.value);
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
    const { socket, send } = await connectWebSocket(target.webSocketDebuggerUrl);
    const viewports = [
      { label: "Desktop", file: "desktop.png", width: 1440, height: 1800, mobile: false },
      { label: "Mobile", file: "mobile.png", width: 390, height: 1400, mobile: true },
    ];
    const evidence = [];
    for (const viewport of viewports) {
      const outputPath = join(args.outputDir, viewport.file);
      const layout = await captureViewport(send, args.url, viewport, outputPath);
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
      console.log(`Wrote ${outputPath}`);
    }
    if (args.evidenceOut) {
      writeFileSync(args.evidenceOut, `${JSON.stringify(evidence, null, 2)}\n`);
      console.log(`Wrote ${args.evidenceOut}`);
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
