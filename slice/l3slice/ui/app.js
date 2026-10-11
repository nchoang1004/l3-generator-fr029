"use strict";
// Local UI for the /api/v1 facade (API-001 §6, consumer table §8.1). No third-party code, no browser storage.
// Every text from the server goes through textContent; the SVG is shown as an <img>, so it cannot run script.

const API = "/api/v1";
const NOTICE_VERSION = "l3gen-egress-v1";
const NOTICE = "Dữ kiện đã trích, tên symbol, đường dẫn tương đối, vị trí, literal như route path, chữ ký hàm và đoạn " +
  "code có giới hạn có thể được gửi tới Groq và Google khi bước model được bật. Không gửi cả repository hoặc nguyên " +
  "file; giá trị giống bí mật được che trước. Bộ lọc bí mật có giới hạn; điều khoản của provider do provider công bố.";
const STAGES = ["queue", "intake", "inventory", "extraction", "assembly", "verification", "export"];
const STAGE_NAMES = {queue: "Chờ", intake: "Tiếp nhận", inventory: "Kiểm kê", extraction: "Trích dữ kiện",
  assembly: "Dựng mô hình", verification: "Kiểm bằng chứng", export: "Xuất"};
const KIND_NAMES = {api: "L3 — API", table: "L3 — Bảng dữ liệu", event: "L3 — Sự kiện", readme: "Mục lục (README)",
  json: "Dữ liệu máy đọc (JSON)", diagram_source: "Mã sơ đồ (Mermaid)", diagram_image: "Ảnh sơ đồ (SVG)"};
const STATE_NAMES = {queued: "đang chờ", running: "đang chạy", completed: "hoàn tất", partial: "một phần",
  failed: "thất bại", ready: "sẵn sàng", retrying: "đang thử lại", pending: "chưa sinh"};
const app = document.getElementById("app");
let view = {token: 0, timer: null, ctrl: null};

// ---------- helpers

function el(tag, attrs, ...kids) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k === "text") node.textContent = v;
    else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
    else node.setAttribute(k, v === true ? "" : String(v));
  }
  for (const kid of kids.flat()) {
    if (kid === null || kid === undefined || kid === false) continue;
    node.append(kid instanceof Node ? kid : document.createTextNode(String(kid)));
  }
  return node;
}

function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }

function fv(field) {
  if (!field) return "unknown — trường không có trong dữ kiện";
  if (field.state === "known") {
    const v = field.value;
    if (Array.isArray(v)) return v.length ? v.map(x => typeof x === "object" ? JSON.stringify(x) : String(x)).join(", ") : "(rỗng)";
    if (v && typeof v === "object") return JSON.stringify(v);
    return String(v);
  }
  const label = {unknown: "unknown", redacted: "đã che", not_applicable: "không áp dụng"}[field.state] || field.state;
  return `${label} — ${field.reason || ""}`;
}

function chip(state) { return el("span", {class: `chip s-${state}`, text: STATE_NAMES[state] || state || "—"}); }

// PRD requirement a section shows, so a reviewer can match the screen to FR-019..027
function fr(...keys) { return el("span", {class: "fr", text: keys.join(" · ")}); }

function errorPanel(body, fallback) {
  const e = body && typeof body === "object" && body.code ? body : null;
  return el("div", {class: "panel error", role: "alert"},
    el("strong", {text: e ? e.message : fallback}),
    e ? el("div", {class: "muted", text: `${e.action} (mã ${e.code})`}) : null);
}

async function call(path, opts = {}) {
  const headers = Object.assign({}, opts.headers || {});
  if (opts.method === "POST") headers["X-L3GEN-Client"] = "web-v1";
  const resp = await fetch(API + path, Object.assign({}, opts, {headers, signal: view.ctrl && view.ctrl.signal,
    credentials: "same-origin", cache: "no-store"}));
  const type = resp.headers.get("Content-Type") || "";
  const body = type.startsWith("application/json") ? await resp.json() : await resp.arrayBuffer();
  return {status: resp.status, body, retryAfter: Number(resp.headers.get("Retry-After")) || 0};
}

function stopView() {
  view.token += 1;
  if (view.timer) clearTimeout(view.timer);
  if (view.ctrl) view.ctrl.abort();
  view = {token: view.token, timer: null, ctrl: new AbortController()};
  return view.token;
}

// ---------- routing

function route() {
  stopView();
  clear(app);
  const m = location.hash.match(/^#\/run\/([A-Za-z0-9_:-]{1,128})$/);
  if (m) showRun(m[1]); else showHome();
}
window.addEventListener("hashchange", route);
window.addEventListener("DOMContentLoaded", route);

// ---------- screen 1: submit a repository

function showHome() {
  const out = el("div");
  const zipTab = el("button", {type: "button", role: "tab", "aria-selected": "true", text: "File ZIP"});
  const ghTab = el("button", {type: "button", role: "tab", "aria-selected": "false", text: "URL GitHub"});
  const zipForm = el("form", {},
    el("label", {for: "zip", text: "File ZIP của repository (tối đa 100 MB nén)"}),
    el("input", {type: "file", id: "zip", accept: ".zip,application/zip", required: true}),
    el("div", {class: "row"}, el("button", {type: "submit", text: "Gửi ZIP"})));
  const ghForm = el("form", {hidden: true},
    el("label", {for: "gh", text: "URL repository public: github.com/<owner>/<repo>"}),
    el("input", {type: "url", id: "gh", required: true, placeholder: "github.com/owner/repo", autocomplete: "off"}),
    el("p", {class: "muted", text: "Không nhập token hay mật khẩu. Repository private không được hỗ trợ."}),
    el("div", {class: "row"}, el("button", {type: "submit", text: "Gửi URL"})));
  const select = (zip) => {
    zipTab.setAttribute("aria-selected", String(zip)); ghTab.setAttribute("aria-selected", String(!zip));
    zipForm.hidden = !zip; ghForm.hidden = zip; clear(out);
  };
  zipTab.addEventListener("click", () => select(true));
  ghTab.addEventListener("click", () => select(false));

  async function submit(form, makeRequest) {
    const button = form.querySelector("button[type=submit]");
    button.disabled = true;
    clear(out);
    try {
      const r = await call(...makeRequest());
      if (r.status === 202) { location.hash = `#/run/${r.body.run_id}`; return; }
      out.append(errorPanel(r.body, `Server trả HTTP ${r.status}`));
    } catch (e) {
      if (e.name === "AbortError") return;
      out.append(errorPanel(null, "Mất kết nối khi gửi: chưa rõ server đã nhận hay chưa. Không gửi lại tự động; " +
        "nếu đã có run_id, mở nó bên dưới."));
    } finally { button.disabled = false; }
  }
  zipForm.addEventListener("submit", (ev) => {
    ev.preventDefault();
    const file = zipForm.querySelector("#zip").files[0];
    if (!file) return;
    submit(zipForm, () => {
      const data = new FormData();
      data.append("archive", file, file.name);  // the server keeps a cleaned name as a label only (web.zip_label)
      data.append("egress_notice_version", NOTICE_VERSION);
      return ["/runs/zip", {method: "POST", body: data}];
    });
  });
  ghForm.addEventListener("submit", (ev) => {
    ev.preventDefault();
    let url = ghForm.querySelector("#gh").value.trim();
    if (!/^[a-z]+:\/\//i.test(url)) url = "https:" + "//" + url;
    submit(ghForm, () => ["/runs/github", {method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({github_url: url, egress_notice_version: NOTICE_VERSION})}]);
  });

  const runInput = el("input", {type: "text", id: "runid", placeholder: "run_…", autocomplete: "off"});
  app.append(
    el("h1", {text: "Phân tích một repository"}),
    el("div", {class: "panel notice"},
      el("strong", {text: `Thông báo dữ liệu (${NOTICE_VERSION})`}), el("p", {text: NOTICE})),
    el("div", {class: "panel"}, el("div", {class: "tabs", role: "tablist"}, zipTab, ghTab), zipForm, ghForm),
    out,
    el("div", {class: "panel"},
      el("label", {for: "runid", text: "Mở một run đã gửi"}),
      el("div", {class: "row"}, runInput, el("button", {type: "button", class: "secondary", text: "Mở",
        onclick: () => { const id = runInput.value.trim(); if (id) location.hash = `#/run/${id}`; }}))));
}

// ---------- screen 2: run status, artifacts, retry

function showRun(runId) {
  const token = view.token;
  const status = el("div");
  const result = el("div");
  let loadedResultFor = null;
  let delay = 2000;
  let title = null;  // repository name, known once the result bundle is loaded
  let lastRun = null;
  app.append(el("p", {}, el("a", {href: "#/", text: "← Gửi repository khác"})), status, result);

  async function refresh() {
    if (token !== view.token) return;
    let r;
    try {
      r = await call(`/runs/${runId}`);
      delay = 2000;
    } catch (e) {
      if (e.name === "AbortError" || token !== view.token) return;
      delay = Math.min(delay * 2, 30000);
      clear(status); status.append(errorPanel(null, `Mất kết nối; thử lại sau ${delay / 1000} giây.`));
      view.timer = setTimeout(refresh, delay);
      return;
    }
    if (token !== view.token) return;
    if (r.status === 404 || r.status === 410) {
      clear(status); clear(result);  // run gone or expired: drop every result shown
      status.append(errorPanel(r.body, "Run không còn"), el("p", {}, el("a", {href: "#/", text: "Chạy phân tích mới"})));
      return;
    }
    if (r.status !== 200) { clear(status); status.append(errorPanel(r.body, `HTTP ${r.status}`)); return; }
    const run = r.body;
    if (run.run_id !== runId) return;
    lastRun = run;
    renderStatus(run);
    const key = run.result_available ? run.artifacts.map(a => a.artifact_id + a.status).join("|") : null;
    if (key && key !== loadedResultFor) { loadedResultFor = key; loadResult(); }
    const busy = run.state === "queued" || run.state === "running" || run.artifacts.some(a => a.status === "retrying");
    if (busy) view.timer = setTimeout(refresh, Math.max(2000, r.retryAfter * 1000));
  }

  function renderStatus(run) {
    clear(status);
    const at = STAGES.indexOf(run.stage);
    // stages only while the run moves; a finished run shows its state and reasons
    const steps = run.state === "queued" || run.state === "running" ? el("div", {class: "panel"},
      el("ol", {class: "steps", "aria-label": "Giai đoạn"}, STAGES.map((s, i) =>
        el("li", {class: i < at ? "done" : i === at ? "now" : "", text: STAGE_NAMES[s]})))) : null;
    status.append(...[  // Node.append writes a null child as the text "null"
      el("h1", {}, title || "Kết quả phân tích", " ", chip(run.state), fr("FR-026")),
      steps,
      run.reasons.length ? el("details", {class: "panel notice"},
        el("summary", {text: run.state === "failed" ? `Vì sao thất bại (${run.reasons.length})`
          : `Vì sao kết quả là "${STATE_NAMES[run.state] || run.state}" (${run.reasons.length} lý do)`}),
        el("ul", {}, run.reasons.map(x => el("li", {}, el("strong", {text: x.message}), " — ",
          el("span", {class: "muted", text: `${x.action} (${x.code})`}))))) : null,
      artifactsPanel(run)].filter(Boolean));
  }

  function artifactsPanel(run) {
    if (!run.artifacts.length) return null;
    const order = a => (KIND_NAMES[a.kind] ? Object.keys(KIND_NAMES).indexOf(a.kind) : 99);
    return el("div", {class: "panel"}, el("h2", {}, "Tài liệu tải về", fr("FR-025")), el("div", {class: "table-wrap"},
      el("table", {class: "mini"},
        el("thead", {}, el("tr", {}, ["Loại", "File", "Trạng thái", ""].map(h => el("th", {text: h})))),
        el("tbody", {}, [...run.artifacts].sort((x, y) => order(x) - order(y)).map(a => el("tr", {},
          el("td", {text: KIND_NAMES[a.kind] || a.kind}), el("td", {class: "mono", text: a.path}),
          el("td", {}, chip(a.status), a.error ? el("div", {class: "muted", text: a.error.reason}) : null),
          el("td", {}, a.status === "ready"
            ? el("a", {href: `${API}/runs/${run.run_id}/artifacts/${a.artifact_id}`, download: a.path.split("/").pop(), text: "Tải"})
            : a.status === "failed" && a.error && a.error.retryable
              ? el("button", {type: "button", class: "secondary", text: "Thử lại", onclick: (ev) => retry(ev.target, a)})
              : null)))))));
  }

  async function retry(button, artifact) {
    button.disabled = true;
    try {
      const r = await call(`/runs/${runId}/artifacts/${artifact.artifact_id}/retry`, {method: "POST"});
      if (r.status !== 200 && r.status !== 202) status.prepend(errorPanel(r.body, `HTTP ${r.status}`));
    } catch (e) { if (e.name !== "AbortError") status.prepend(errorPanel(null, "Mất kết nối khi thử lại")); }
    if (view.timer) clearTimeout(view.timer);
    refresh();
  }

  async function loadResult() {
    let r;
    try { r = await call(`/runs/${runId}/result`); } catch (e) { return; }
    if (token !== view.token) return;
    clear(result);
    if (r.status !== 200) { result.append(errorPanel(r.body, `HTTP ${r.status}`)); return; }
    if (r.body.run_id !== runId) return;
    title = r.body.export_context.repository_name;
    if (lastRun) renderStatus(lastRun);
    renderResult(runId, r.body, result, token);
  }

  refresh();
}

// ---------- screens 3–5: the L3 contracts of the run (API, tables, events) and their evidence, from one bundle.
// The component diagram is not shown: components come from a stand-in split (D-03 is still open).

const METHOD_CLASS = {GET: "m-get", POST: "m-post", PUT: "m-put", PATCH: "m-put", DELETE: "m-del"};

function known(field) { return field && field.state === "known"; }

function short(text, n) { return text.length > n ? text.slice(0, n - 1) + "…" : text; }

function typeText(schema, facts) {
  if (!schema || typeof schema !== "object" || !Object.keys(schema).length) return "?";
  if (schema["x-model-fact"]) { const m = facts.get(schema["x-model-fact"]); return m ? modelName(m) : "model?"; }
  if (schema.anyOf) return schema.anyOf.map(s => typeText(s, facts)).join(" | ");
  if (schema.type === "array") return `list[${typeText(schema.items, facts)}]`;
  if (schema.type) return schema.format ? `${schema.type}(${schema.format})` : String(schema.type);
  return "?";
}

function modelName(f) { return known(f.attributes.name) ? String(f.attributes.name.value).split(".").pop() : f.id; }

function unknownText(field) {
  if (!field) return "chưa biết";
  return field.state === "redacted" ? "đã che" : field.state === "not_applicable" ? "không áp dụng" : "chưa biết";
}

function labelChips(f) {
  return [el("span", {class: `chip c-${f.confidence}`, text: f.confidence}), " ",
          el("span", {class: `chip c-${f.completeness}`, text: f.completeness})];
}

function renderResult(runId, bundle, root, token) {
  const res = bundle.result;
  const all = res.facts.facts;
  const facts = new Map(all.map(f => [f.id, f]));
  const evIndex = new Map(res.evidence_index.map(e => [e.id, e]));
  const of = (kind) => all.filter(f => f.kind === kind);
  const routes = of("route").sort((x, y) => routePath(x).localeCompare(routePath(y)) ||
    fv(x.attributes.method).localeCompare(fv(y.attributes.method)));
  const tables = of("table").sort((x, y) => fv(x.attributes.name).localeCompare(fv(y.attributes.name)));
  const events = of("event");
  const models = all.filter(f => f.kind === "request_model" || f.kind === "response_model");
  const limits = [...res.limitations, ...bundle.render_notices.map(n => ({code: n.code, stage: "xuất tài liệu", message: n.reason}))];

  function routePath(f) {
    const a = f.attributes;
    return known(a.path) ? a.path.value : known(a.path_suffix) ? `…${a.path_suffix.value}` : "?";
  }

  // ---- evidence: opened inside the place that asked for it
  function evidenceButtons(ids, box) {
    const seen = new Map();
    for (const id of ids) {
      const e = evIndex.get(id);
      if (!e) continue;
      const where = `${e.path}:${e.start_line}`;
      if (!seen.has(where)) seen.set(where, id);
    }
    return el("div", {class: "evs"}, [...seen].slice(0, 12).map(([where, id]) =>
      el("button", {type: "button", class: "ev", text: where, onclick: () => openEvidence(id, box)})));
  }
  async function openEvidence(id, box) {
    clear(box);
    box.append(el("p", {class: "muted", text: "Đang mở bằng chứng…"}));
    let r;
    try { r = await call(`/runs/${runId}/evidence/${encodeURIComponent(id)}`); } catch (e) { return; }
    if (token !== view.token) return;
    clear(box);
    if (r.status !== 200) { box.append(errorPanel(r.body, `HTTP ${r.status}`)); return; }
    if (r.body.run_id !== runId || r.body.evidence.id !== id) return;
    const ev = r.body.evidence;
    box.append(el("div", {class: "code"},
      el("div", {class: "code-head"}, el("span", {class: "mono", text: `${ev.path}:${ev.start_line}-${ev.end_line}`}),
        el("span", {class: "muted", text: r.body.redacted ? " · đã che bí mật" : ""})),
      el("pre", {text: r.body.content})));
  }

  // ---- API
  function paramsCell(a) {
    if (!known(a.parameters)) return el("span", {class: "muted", text: unknownText(a.parameters)});
    if (!a.parameters.value.length) return el("span", {class: "muted", text: "—"});
    return el("div", {class: "params"}, a.parameters.value.map(p => el("span", {class: "param",
      title: `${fv(p.name)}: ${known(p.in) ? p.in.value : "vị trí chưa biết — " + (p.in.reason || "")}`},
      el("b", {text: fv(p.name)}), " ", el("span", {class: "muted", text: known(p.in) ? p.in.value : "chưa rõ"}))));
  }
  function modelsCell(field) {
    if (!known(field)) return el("span", {class: "muted", text: unknownText(field)});
    if (!field.value.length) return el("span", {class: "muted", text: "—"});
    return field.value.map(id => facts.get(id) ? modelName(facts.get(id)) : id).join(", ");
  }
  function statusCell(a) {
    if (!known(a.status_codes)) return el("span", {class: "muted", text: "chưa biết"});
    return el("span", {}, a.status_codes.value.join(", "),
      known(a.status_rule) ? el("span", {class: "muted small", text: " (mặc định)"}) : null);
  }
  function authCell(a) {
    if (known(a.auth)) return el("span", {text: fv(a.auth)});
    return el("span", {class: "muted", text: unknownText(a.auth), title: (a.auth && a.auth.reason) || ""});
  }
  // what the confidence/completeness labels of a route come from, in words
  const FIELD_NAMES = {path: "path", parameters: "tham số", request_model_ids: "request", response_model_ids: "response",
    status_codes: "status"};
  function certaintyCell(f) {
    const a = f.attributes;
    const inferred = [known(a.status_rule) ? "status" : null, known(a.prefix_rule) ? "prefix" : null].filter(Boolean);
    const unknown = Object.entries(FIELD_NAMES).filter(([k]) => a[k] && a[k].state === "unknown").map(([, n]) => n);
    const text = [inferred.length ? `suy ra: ${inferred.join(", ")}` : null,
      unknown.length ? `chưa biết: ${unknown.join(", ")}` : null].filter(Boolean).join(" · ") || "đọc thẳng từ code";
    return el("span", {class: "small", text, title: `${f.confidence} / ${f.completeness}. ${f.confidence_reason || ""}`});
  }
  function modelTable(id, direction) {
    const m = facts.get(id);
    if (!m) return null;
    const fields = known(m.attributes.fields) ? m.attributes.fields.value : [];
    return el("div", {class: "model"}, el("h4", {}, `${direction}: `, el("span", {class: "mono", text: modelName(m)})),
      el("table", {class: "mini"}, el("thead", {}, el("tr", {}, ["Field", "Kiểu", "Bắt buộc", "Có thể null"].map(h => el("th", {text: h})))),
        el("tbody", {}, fields.map(x => el("tr", {},
          el("td", {class: "mono", text: fv(x.name)}),
          el("td", {text: known(x.type) ? typeText(x.type.value, facts) : unknownText(x.type), title: known(x.type) ? "" : (x.type.reason || "")}),
          el("td", {text: known(x.required) ? (x.required.value ? "có" : "không") : "?"}),
          el("td", {text: known(x.nullable) ? (x.nullable.value ? "có" : "không") : "?"}))))));
  }
  function routeDetail(f) {
    const a = f.attributes, box = el("div");
    const unknowns = Object.entries(a).filter(([, v]) => v && v.state === "unknown" && v.reason)
      .map(([k, v]) => el("li", {}, el("span", {class: "mono", text: k}), " — ", v.reason));
    const ids = id => known(a[id]) ? a[id].value : [];
    return el("div", {class: "detail"},
      el("dl", {},
        el("dt", {text: "Handler"}), el("dd", {class: "mono", text: fv(a.handler)}),
        el("dt", {text: "Status"}), el("dd", {text: known(a.status_codes) ? `${a.status_codes.value.join(", ")}` +
          (known(a.status_rule) ? ` (suy theo ${a.status_rule.value})` : " (ghi trong code)") : fv(a.status_codes)}),
        known(a.prefix_rule) ? [el("dt", {text: "Prefix"}), el("dd", {text: `lấy giá trị mặc định trong Settings (${a.prefix_rule.value})`})] : null,
        el("dt", {text: "Auth"}), el("dd", {text: known(a.auth) ? fv(a.auth) :
          `${unknownText(a.auth)} — ${(a.auth && a.auth.reason) || ""}`}),
        el("dt", {text: "Nhãn"}), el("dd", {}, labelChips(f), " ", el("span", {class: "muted small", text: f.confidence_reason || ""}))),
      el("div", {class: "models"}, ids("request_model_ids").map(id => modelTable(id, "Request")),
        ids("response_model_ids").map(id => modelTable(id, "Response"))),
      unknowns.length ? el("details", {}, el("summary", {text: `Trường chưa biết (${unknowns.length})`}), el("ul", {}, unknowns)) : null,
      el("h4", {}, "Bằng chứng trong code", fr("FR-023")), evidenceButtons(f.evidence.map(e => e.id), box), box);
  }

  const search = el("input", {type: "search", id: "q", placeholder: "Lọc theo path, method, model, tên bảng…"});
  const apiBody = el("tbody");
  const tableBox = el("div");
  const matches = text => { const q = search.value.trim().toLowerCase(); return !q || text.toLowerCase().includes(q); };

  function drawApi() {
    clear(apiBody);
    for (const f of routes) {
      const a = f.attributes;
      const text = [fv(a.method), routePath(f), fv(a.handler), modelsCell(a.request_model_ids), modelsCell(a.response_model_ids)]
        .map(x => typeof x === "string" ? x : x.textContent).join(" ");
      if (!matches(text)) continue;
      const detailRow = el("tr", {class: "detail-row", hidden: true}, el("td", {colspan: 8}, routeDetail(f)));
      const row = el("tr", {class: "route", tabindex: 0, "aria-expanded": "false"},
        el("td", {class: "nowrap"}, el("span", {class: `method ${METHOD_CLASS[fv(a.method)] || ""}`, text: fv(a.method)})),
        el("td", {class: "mono path", text: routePath(f)}),
        el("td", {}, paramsCell(a)),
        el("td", {class: "mono"}, modelsCell(a.request_model_ids)),
        el("td", {class: "mono"}, modelsCell(a.response_model_ids)),
        el("td", {class: "nowrap"}, statusCell(a)),
        el("td", {class: "nowrap"}, authCell(a)),
        el("td", {}, certaintyCell(f)));
      const toggle = () => { detailRow.hidden = !detailRow.hidden; row.setAttribute("aria-expanded", String(!detailRow.hidden)); };
      row.addEventListener("click", toggle);
      row.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); toggle(); } });
      apiBody.append(row, detailRow);
    }
    if (!apiBody.firstChild) apiBody.append(el("tr", {}, el("td", {colspan: 8, class: "muted",
      text: routes.length ? "Không route nào khớp bộ lọc." : "Không tìm thấy route FastAPI."})));
  }

  function drawTables() {
    clear(tableBox);
    const shown = tables.filter(t => matches(`${fv(t.attributes.name)} ` +
      (known(t.attributes.columns) ? t.attributes.columns.value.map(c => fv(c.name)).join(" ") : "")));
    if (!shown.length) tableBox.append(el("p", {class: "muted", text: tables.length ? "Không bảng nào khớp bộ lọc." :
      "Không có bảng khai bằng model SQLAlchemy/SQLModel. Xem mục Giới hạn nếu bảng nằm trong migration."}));
    for (const t of shown) {
      const a = t.attributes, box = el("div");
      const cols = known(a.columns) ? a.columns.value : [];
      tableBox.append(el("div", {class: "card"},
        el("div", {class: "card-head"}, el("h3", {class: "mono", text: fv(a.name)}),
          el("span", {class: "muted", text: `${t.evidence[0].path}:${t.evidence[0].start_line}`}), labelChips(t)),
        el("p", {class: "muted small", text: known(a.dialect) ? `Dialect: ${a.dialect.value}` :
          "Dialect chưa biết, nên kiểu SQL chưa biết; cột Kiểu ghi kiểu khai trong code."}),
        el("table", {class: "mini"}, el("thead", {}, el("tr", {}, ["Cột", "Kiểu", "Khóa", "Có thể null"].map(h => el("th", {text: h})))),
          el("tbody", {}, cols.map(c => {
            const declared = !known(c.type) && /khai trong code: (.+)$/.exec(c.type.reason || "");
            const key = [known(c.primary_key) && c.primary_key.value ? "PK" : "",
              known(c.foreign_key) ? `FK → ${c.foreign_key.value.table}.${c.foreign_key.value.column}` : ""].filter(Boolean).join(", ");
            return el("tr", {}, el("td", {class: "mono", text: fv(c.name)}),
              el("td", {class: "mono", text: known(c.type) ? c.type.value : declared ? declared[1] : "?",
                title: known(c.type) ? "" : (c.type.reason || "")}),
              el("td", {text: key || "—"}),
              el("td", {text: known(c.nullable) ? (c.nullable.value ? "có" : "không") : "?"}));
          }))),
        el("details", {}, el("summary", {text: "Bằng chứng"}), evidenceButtons(t.evidence.map(e => e.id), box), box)));
    }
  }

  const eventBox = events.length ? el("table", {class: "mini"},
    el("thead", {}, el("tr", {}, ["Hành động", "Topic", "Broker", "Nhãn"].map(h => el("th", {text: h})))),
    el("tbody", {}, events.map(e => el("tr", {}, el("td", {text: fv(e.attributes.action)}),
      el("td", {class: "mono", text: fv(e.attributes.topic)}), el("td", {text: fv(e.attributes.broker)}), el("td", {}, labelChips(e))))))
    : el("p", {class: "muted", text: "Không có event Kafka/FastStream. Thư viện hàng đợi khác (Celery, RabbitMQ…) được ghi ở mục Giới hạn."});

  const card = (n, label, href) => el("a", {class: "stat", href}, el("b", {text: String(n)}), el("span", {text: label}));
  const byCode = limits.reduce((m, l) => ((m[l.code] ||= []).push(l), m), {});
  root.append(
    el("div", {class: "stats"},
      card(routes.length, "API route", "#sec-api"), card(models.length, "model", "#sec-api"),
      card(tables.length, "bảng", "#sec-tbl"), card(events.length, "sự kiện", "#sec-evt"),
      card(Object.keys(byCode).length, "loại giới hạn", "#sec-lim")),
    el("div", {class: "panel"}, el("label", {for: "q", text: "Lọc"}), search),
    el("section", {class: "panel", id: "sec-api"}, el("h2", {}, "API", fr("FR-021", "FR-027")),
      el("p", {class: "muted small", text: "Bấm một dòng để xem handler, field của model và bằng chứng trong code. " +
        "Status \"(mặc định)\" là suy theo quy ước của FastAPI. Auth \"chưa biết\": contract chưa có luật cho auth nên " +
        "công cụ không đoán, rê chuột để xem dependency tìm thấy. Cột \"Độ chắc chắn\" nói phần nào suy ra, phần nào chưa biết."}),
      el("div", {class: "table-wrap"}, el("table", {class: "api"},
        el("thead", {}, el("tr", {}, ["Method", "Path", "Tham số", "Request", "Response", "Status", "Auth", "Độ chắc chắn"]
          .map(h => el("th", {text: h})))),
        apiBody))),
    el("section", {class: "panel", id: "sec-tbl"}, el("h2", {}, "Bảng dữ liệu", fr("FR-021", "FR-027")), tableBox),
    el("section", {class: "panel", id: "sec-evt"}, el("h2", {}, "Sự kiện", fr("FR-027")), eventBox),
    el("section", {class: "panel notice", id: "sec-lim"}, el("h2", {}, "Giới hạn — phần công cụ chưa đọc được", fr("FR-024")),
      el("ul", {class: "limits"}, Object.entries(byCode).map(([code, list]) => el("li", {},
        el("details", {}, el("summary", {}, el("code", {text: code}), ` · ${list.length} mục — `, short(list[0].message, 140)),
          el("ul", {}, list.slice(0, 50).map(l => el("li", {class: "small", text: `(${l.stage}) ${l.message}`})))))))),
    el("details", {class: "panel"}, el("summary", {}, "Phạm vi đã xét", fr("FR-020")),
      el("table", {class: "mini"}, el("thead", {}, el("tr", {}, ["Unit", "Ngôn ngữ", "Framework", "Mức hỗ trợ", "Số file"].map(h => el("th", {text: h})))),
        el("tbody", {}, res.inventory.units.map(u => el("tr", {},
          el("td", {class: "mono", text: u.root_path}), el("td", {text: u.language || "chưa nhận diện"}),
          el("td", {text: u.framework || "chưa nhận diện"}), el("td", {text: u.support}), el("td", {text: String(u.file_ids.length)}))))),
      res.inventory.excluded.length ? el("details", {}, el("summary", {text: `${res.inventory.excluded.length} đường dẫn bị loại`}),
        el("ul", {}, res.inventory.excluded.map(x => el("li", {class: "small"}, el("span", {class: "mono", text: x.path}), " — ", x.reason)))) : null));
  search.addEventListener("input", () => { drawApi(); drawTables(); });
  drawApi();
  drawTables();
}
