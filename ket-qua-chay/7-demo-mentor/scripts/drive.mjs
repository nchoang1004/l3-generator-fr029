// Drive the local L3 UI like a user (Edge over the DevTools protocol) and screenshot every step. Node 22, no packages.
import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync } from "node:fs";

const OUT = process.argv[2];
const ZIP = process.argv[3];
const BAD = process.argv[4];
const EDGE = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe";
const PORT = 9333;
mkdirSync(OUT, { recursive: true });
const edge = spawn(EDGE, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${OUT}/profile`,
  "--window-size=1280,900", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let tab;
for (let i = 0; i < 50 && !tab; i++) {
  await sleep(200);
  try { tab = (await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json()).find((t) => t.type === "page"); } catch {}
}
const ws = new WebSocket(tab.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let seq = 0;
const waiting = new Map();
ws.addEventListener("message", (m) => { const d = JSON.parse(m.data); if (d.id && waiting.has(d.id)) { waiting.get(d.id)(d); waiting.delete(d.id); } });
const send = (method, params = {}) => new Promise((r) => { const id = ++seq; waiting.set(id, r); ws.send(JSON.stringify({ id, method, params })); });
const js = async (expr) => (await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;
const log = [];
async function shot(name, note, full = true) {
  const m = await send("Page.getLayoutMetrics");
  const h = Math.min(Math.ceil(m.result.cssContentSize.height), 6000);
  const r = await send("Page.captureScreenshot", full ? { format: "png", captureBeyondViewport: true,
    clip: { x: 0, y: 0, width: 1280, height: h, scale: 1 } } : { format: "png" });
  writeFileSync(`${OUT}/${name}.png`, Buffer.from(r.result.data, "base64"));
  log.push({ name, note, url: await js("location.href"), text: (await js("document.querySelector('main').innerText")).slice(0, 1500) });
  console.log("shot", name);
}
async function waitFor(expr, ms = 15000) {
  for (let t = 0; t < ms; t += 200) { if (await js(expr)) return true; await sleep(200); }
  return false;
}
async function setFile(path) {
  const doc = await send("DOM.getDocument", { depth: -1 });
  const q = await send("DOM.querySelector", { nodeId: doc.result.root.nodeId, selector: "#zip" });
  await send("DOM.setFileInputFiles", { nodeId: q.result.nodeId, files: [path] });
}
await send("Page.enable"); await send("Runtime.enable"); await send("DOM.enable");
await send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 900, deviceScaleFactor: 1, mobile: false });

// 1 home
await send("Page.navigate", { url: "http://127.0.0.1:8765/" });
await waitFor("!!document.querySelector('#zip')");
await shot("01-trang-chu", "Trang gửi repository");

// 2 wrong file: not a ZIP
await setFile(BAD);
await js("document.querySelector('#zip').form.requestSubmit()");
await waitFor("/invalid_zip|không phải ZIP/i.test(document.body.innerText)", 5000);
await shot("02-loi-khong-phai-zip", "Gửi file không phải ZIP");

// 3 GitHub URL while GitHub is off
await js("[...document.querySelectorAll('button[role=tab]')].find(b=>b.textContent.includes('GitHub')).click()");
await js("const i=document.querySelector('#gh'); i.value='https://github.com/rhoboro/async-fastapi-sqlalchemy'; i.dispatchEvent(new Event('input',{bubbles:true})); i.form.requestSubmit()");
await waitFor("/503|github_disabled|chưa bật|tắt/i.test(document.body.innerText)", 5000);
await shot("03-github-dang-tat", "Gửi URL GitHub khi tính năng còn tắt");

// 4 the real ZIP
await send("Page.navigate", { url: "http://127.0.0.1:8765/" });
await waitFor("!!document.querySelector('#zip')");
await setFile(ZIP);
const t0 = Date.now();
await js("document.querySelector('#zip').form.requestSubmit()");
await waitFor("location.hash.startsWith('#/run/')", 5000);
await sleep(150);
await shot("04-dang-chay", "Ngay sau khi gửi ZIP", false);
await waitFor("/Tổng quan kiến trúc/.test(document.body.innerText)", 20000);
const took = Date.now() - t0;
await sleep(600);
await shot("05-ket-qua", `Kết quả, ${took} ms từ lúc bấm gửi`);

// 5 component detail: pick the component that owns the routes ("app")
await js("[...document.querySelectorAll('ul.list button.link')].find(b=>b.textContent.trim()==='app').click()");
await sleep(300);
await shot("06-component-app", "Bấm component app");

// 6 open one evidence of the first contract row
await js("[...document.querySelectorAll('td button.secondary')].find(b=>/views\\.py:18/.test(b.textContent))?.click() || document.querySelector('td button.secondary').click()");
await waitFor("/Bằng chứng/.test([...document.querySelectorAll('.panel h2')].map(x=>x.textContent).join(' '))", 5000);
await sleep(300);
await shot("07-bang-chung", "Mở một bằng chứng");

// 7 search
await js("const q=document.querySelector('#q'); q.value='notebooks'; q.dispatchEvent(new Event('input',{bubbles:true}))");
await sleep(300);
await shot("08-tim-kiem", "Gõ 'notebooks' vào ô tìm");

writeFileSync(`${OUT}/log.json`, JSON.stringify({ took_ms: took, steps: log }, null, 1));
ws.close(); edge.kill();
console.log("done", took, "ms");
process.exit(0);
