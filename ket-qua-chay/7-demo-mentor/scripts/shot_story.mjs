// Walk the L3 web UI with one ZIP like a presenter and screenshot each step (element-sized crops). Node 22.
import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync } from "node:fs";

const [OUT, ZIP, PORT = "9336"] = process.argv.slice(2);
mkdirSync(OUT, { recursive: true });
const edge = spawn("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe", ["--headless=new",
  `--remote-debugging-port=${PORT}`, `--user-data-dir=${OUT}/profile`, "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
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
const waitFor = async (expr, ms = 30000) => { for (let t = 0; t < ms; t += 150) { if (await js(expr)) return true; await sleep(150); } return false; };
// rect of the union of the elements an expression returns (array of elements), page coordinates
async function shot(name, expr, pad = 10) {
  const box = await js(`(() => { const els = (${expr}).filter(Boolean); if (!els.length) return null;
    const rs = els.map(e => e.getBoundingClientRect());
    const top = Math.min(...rs.map(r => r.top)), bottom = Math.max(...rs.map(r => r.bottom));
    return {x: 0, y: Math.max(0, top + scrollY - ${pad}), width: 1280, height: Math.min(bottom - top + 2 * ${pad}, 3200)}; })()`);
  if (!box) { console.log("missing", name); return; }
  const r = await send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true, clip: { ...box, scale: 1 } });
  writeFileSync(`${OUT}/${name}.png`, Buffer.from(r.result.data, "base64"));
  console.log("shot", name);
}
const $ = (sel) => `[document.querySelector(${JSON.stringify(sel)})]`;
const rowOf = (path, method) => `[...document.querySelectorAll('tr.route')].find(r => r.children[1].textContent === ${JSON.stringify(path)} && r.children[0].textContent === ${JSON.stringify(method)})`;

await send("Page.enable"); await send("Runtime.enable"); await send("DOM.enable");
await send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 900, deviceScaleFactor: 1, mobile: false });
await send("Page.navigate", { url: "http://127.0.0.1:8765/" });
await waitFor("!!document.querySelector('#zip')");
const doc = await send("DOM.getDocument", { depth: -1 });
const q = await send("DOM.querySelector", { nodeId: doc.result.root.nodeId, selector: "#zip" });
await send("DOM.setFileInputFiles", { nodeId: q.result.nodeId, files: [ZIP] });
await shot("01-gui-repo", "[...document.querySelectorAll('main > *')].slice(0, 3)");
await js("document.querySelector('#zip').form.requestSubmit()");
await waitFor("location.hash.startsWith('#/run/')", 5000);
await sleep(120);
await shot("02-dang-chay", "[...document.querySelectorAll('main > div > *')].slice(0, 2)");
await waitFor("!!document.querySelector('#sec-api')");
await sleep(700);
await js("document.querySelector('details.notice')?.setAttribute('open', '')");
await sleep(200);
await shot("03-ket-qua-dau-trang", "[document.querySelector('main h1'), document.querySelector('.stats')]");
await shot("04-bang-api", $("#sec-api"));
// POST /api/v1/user/login: open, then open the first evidence
await js(`${rowOf("/api/v1/user/login", "POST")}.click()`);
await sleep(250);
await js(`${rowOf("/api/v1/user/login", "POST")}.nextElementSibling.querySelector('button.ev').click()`);
await waitFor(`!!${rowOf("/api/v1/user/login", "POST")}.nextElementSibling.querySelector('.code')`, 8000);
await sleep(250);
await shot("05-login-chi-tiet", `[${rowOf("/api/v1/user/login", "POST")}, ${rowOf("/api/v1/user/login", "POST")}.nextElementSibling]`);
await js(`${rowOf("/api/v1/user/login", "POST")}.click()`);
// GET /api/v1/user: what is still unknown
await js(`${rowOf("/api/v1/user", "GET")}.click()`);
await sleep(250);
await js(`${rowOf("/api/v1/user", "GET")}.nextElementSibling.querySelector('details')?.setAttribute('open', '')`);
await sleep(200);
await shot("06-get-user-chi-tiet", `[${rowOf("/api/v1/user", "GET")}, ${rowOf("/api/v1/user", "GET")}.nextElementSibling]`);
await shot("07-bang-du-lieu", $("#sec-tbl"));
await js("for (const d of document.querySelectorAll('#sec-lim details')) if (/QUEUE_LIBRARY|VALUE_REDACTED/.test(d.textContent)) d.setAttribute('open', '')");
await sleep(200);
await shot("08-gioi-han", $("#sec-lim"));
await shot("09-loc", "[document.querySelector('#q').closest('.panel')]");
const info = await js("({run: location.hash})");
writeFileSync(`${OUT}/info.json`, JSON.stringify(info));
console.log(JSON.stringify(info));
ws.close(); edge.kill(); process.exit(0);
