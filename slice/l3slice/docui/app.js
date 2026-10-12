"use strict";
const $ = id => document.getElementById(id);
const labels = {running:"Đang chạy",finished:"Đã xuất kết quả",failed:"Gặp lỗi",completed:"Hoàn tất",partial:"Chưa đầy đủ",passed:"Khớp",not_evaluated:"Chưa đối chiếu",ready:"Sẵn sàng",agent:"Từng file (agent)",oneshot:"Đọc một lần"};
// Reading order on screen: the one file for people first, machine files last.
const groups = [["Đọc chính", p => /(^|\/)(TAI-LIEU|README)\.md$/.test(p)], ["API", p => p.includes("/api/")],
  ["Bảng CSDL", p => p.includes("/schema/")], ["Sự kiện", p => p.includes("/events/")], ["Cho máy đọc", () => true]];
let config, selected = null, timer, previewVersion = 0, openWhenDone = null, previewSource = null;
function node(tag, text, cls) { const n = document.createElement(tag); n.textContent = text; if(cls) n.className = cls; return n; }
async function api(path, options = {}) {
  const response = await fetch(path, {cache:"no-store", credentials:"same-origin", signal:AbortSignal.timeout(20000), ...options});
  const data = await response.json();
  if(!response.ok) throw new Error(data.message || "Không đọc được kết quả từ server.");
  return data;
}
function errorMessage(error) { return error.name === "TimeoutError" ? "Server phản hồi chậm. Hãy thử kết nối lại." : error.message || "Không kết nối được server."; }
async function history() {
  const runs = await api("/api/runs");
  if(!document) return runs;  // page closed while waiting
  $("history").replaceChildren(node("option", "Chọn lần chạy trong phiên server"));
  $("history").firstChild.value = "";
  for(const run of [...runs].reverse()) {
    const option = node("option", `${run.name}, ${labels[run.status] || run.status} (${run.run_id.slice(-6)})`);
    option.value = run.run_id; $("history").append(option);
  }
  $("history").hidden = !runs.length;
  $("history").value = selected || "";
  $("submit").disabled = runs.some(r => r.status === "running");
  return runs;
}
function lineRanges(items) { return items.map(r => Array.isArray(r) ? r.join("-") : String(r)).join(", "); }
function artifactUrl(run, art) { return `/api/runs/${encodeURIComponent(run.run_id)}/artifacts/${encodeURIComponent(art.artifact_id)}`; }
function artifactRow(run, art) {
  const row = node("div", "", "artifact"), title = node("div", art.path, "artifact-name");
  title.append(node("small", art.path.endsWith("TAI-LIEU.md") ? "Nên đọc trước" : labels[art.status] || art.status)); row.append(title);
  if(art.status === "ready") {
    const url = artifactUrl(run, art);
    const actions = node("div", "", "artifact-actions"), preview = node("button", "Xem");
    preview.type = "button"; preview.setAttribute("aria-label", `Xem ${art.path}`);
    preview.onclick = () => showPreview(url, art.path);
    const download = node("a", "Tải xuống", "download"); download.href = url; download.download = art.path.split("/").pop();
    download.setAttribute("aria-label", `Tải ${art.path}`); actions.append(preview, download); row.append(actions);
  }
  return row;
}
function renderArtifacts(run, artifacts) {
  const left = [...artifacts].sort((a, b) => b.path.endsWith("TAI-LIEU.md") - a.path.endsWith("TAI-LIEU.md"));
  $("artifacts").replaceChildren();
  for(const [name, match] of groups) {
    const mine = left.filter(a => match(a.path));
    if(!mine.length) continue;
    left.splice(0, left.length, ...left.filter(a => !mine.includes(a)));
    const group = node("section", "", "artifact-group");
    group.append(node("h4", `${name} (${mine.length})`), ...mine.map(a => artifactRow(run, a)));
    $("artifacts").append(group);
  }
}
function render(run) {
  $("empty").hidden = true; $("run").hidden = false; $("retry").hidden = true;
  $("status").textContent = labels[run.status] || run.status;
  $("run-message").textContent = run.message + (run.status === "running" ? ` Lượt gọi model: ${run.turns}.` : "");
  $("run-id").textContent = run.run_id;
  $("result").hidden = !run.result;
  if(!run.result) return;
  const r = run.result;
  $("agent-status").textContent = labels[r.agent.status] || r.agent.status;
  $("mode").textContent = labels[run.mode || r.agent.mode] || run.mode || r.agent.mode || "agent";
  $("coverage").textContent = r.coverage.complete ? "Đủ trong phạm vi" : "Chưa đọc đủ";
  $("parity").textContent = labels[r.architecture_parity.status] || r.architecture_parity.status;
  const files = r.coverage.files;
  const complete = files.filter(f => !f.missing.length && !f.cut_lines.length).length;
  $("coverage-note").textContent = `${complete}/${files.length} file trong phạm vi đã đọc đủ; ${r.coverage.not_readable.length} file ngoài phạm vi đọc. ${r.agent.turns} lượt model. ${r.agent.reason || ""}`;
  $("output-path").textContent = run.output_directory;
  renderArtifacts(run, r.artifacts);
  $("limits-title").textContent = `Giới hạn cần xem (${r.limitations.length})`;
  $("limits-panel").open = r.limitations.length > 0;
  $("limits").replaceChildren(...r.limitations.map(l => { const li = node("li", ` ${l.message}`); li.prepend(node("code", l.code)); return li; }));
  $("coverage-files").replaceChildren(...files.map(f => {
    const tr = document.createElement("tr"), done = !f.missing.length && !f.cut_lines.length;
    const gaps = [f.missing.length ? `Chưa đọc dòng ${lineRanges(f.missing)}` : "", f.cut_lines.length ? `Dòng bị cắt: ${lineRanges(f.cut_lines)}` : ""].filter(Boolean);
    tr.append(node("td", f.path), node("td", done ? "Đã đọc đủ" : "Chưa đủ"), node("td", gaps.join("; ") || "Không"));
    return tr;
  }));
}
async function selectRun(id) {
  clearTimeout(timer);
  if(selected !== id) {
    $("result").hidden = true; $("run-message").textContent = "Đang tải lần chạy…";
    $("run-id").textContent = id; $("status").textContent = "Đang tải";
  }
  selected = id; $("history").value = id;
  try {
    const run = await api(`/api/runs/${encodeURIComponent(id)}`);
    if(!document || selected !== id) return;
    render(run);
    if(run.status === "running") { timer = setTimeout(() => selectRun(id), 1500); return; }
    await history();
    if(openWhenDone === id && run.result) {
      openWhenDone = null;
      const main = run.result.artifacts.find(a => a.path.endsWith("TAI-LIEU.md") && a.status === "ready");
      if(main) showPreview(artifactUrl(run, main), main.path);
    }
  } catch(error) {
    if(!document || selected !== id) return;
    $("empty").hidden = true; $("run").hidden = false;
    $("status").textContent = "Mất kết nối";
    $("run-message").textContent = errorMessage(error); $("retry").hidden = false;
  }
}

// Markdown to DOM. Every piece of file text goes through textContent, so HTML in a
// generated document or in quoted source code is shown, never run.
const entities = {"&lt;":"<","&gt;":">","&amp;":"&","&quot;":"\"","&#39;":"'","&#124;":"|"};
function plain(text) { return text.replace(/&(lt|gt|amp|quot|#39|#124);/g, m => entities[m]); }
function inline(parent, text) {
  const pattern = /`([^`]+)`|\*\*([^*]+)\*\*|\[([^\]]+)\]\(([^)\s]+)\)/g;
  let last = 0, m;
  while((m = pattern.exec(text))) {
    if(m.index > last) parent.append(plain(text.slice(last, m.index)));
    if(m[1] !== undefined) parent.append(node("code", m[1]));
    else if(m[2] !== undefined) inline(parent.appendChild(document.createElement("strong")), m[2]);
    else if(/^https?:\/\//.test(m[4])) {
      const a = node("a", plain(m[3])); a.href = m[4]; a.rel = "noopener noreferrer"; a.target = "_blank"; parent.append(a);
    } else { const s = node("span", plain(m[3]), "doc-link"); s.title = m[4]; parent.append(s); }
    last = pattern.lastIndex;
  }
  if(last < text.length) parent.append(plain(text.slice(last)));
  return parent;
}
function cells(line) {
  const parts = line.trim().replace(/^\||\|$/g, "").split(/(?<!\\)\|/);
  return parts.map(c => c.trim().replace(/\\\|/g, "|"));
}
function markdown(text) {
  const root = document.createDocumentFragment();
  let lines = text.replace(/\r\n?/g, "\n").split("\n"), i = 0;
  if(lines[0] === "---") {  // frontmatter is for machines; keep it, folded
    const end = lines.indexOf("---", 1);
    if(end > 0) {
      const meta = document.createElement("details"); meta.className = "doc-meta";
      meta.append(node("summary", "Thông tin cho máy (frontmatter)"), node("pre", lines.slice(1, end).join("\n")));
      root.append(meta); i = end + 1;
    }
  }
  const isTable = k => /^\s*\|/.test(lines[k] || "") && /^\s*\|?\s*:?-{3,}/.test(lines[k + 1] || "");
  const isList = l => /^\s*([-*]|\d+\.)\s+/.test(l);
  const starts = k => /^(#{1,6}\s|```|>|\s*([-*_])\2\2+\s*$)/.test(lines[k]) || isList(lines[k]) || isTable(k);
  while(i < lines.length) {
    const line = lines[i];
    if(!line.trim()) { i++; continue; }
    let m;
    if((m = line.match(/^(#{1,6})\s+(.*)$/))) { root.append(inline(document.createElement(`h${Math.min(m[1].length + 2, 6)}`), m[2])); i++; }
    else if(line.startsWith("```")) {
      const end = lines.findIndex((l, k) => k > i && l.startsWith("```"));
      const stop = end < 0 ? lines.length : end;
      const pre = document.createElement("pre"); pre.append(node("code", lines.slice(i + 1, stop).join("\n")));
      root.append(pre); i = stop + 1;
    } else if(isTable(i)) {
      const table = document.createElement("table"), head = table.createTHead().insertRow(), body = table.createTBody();
      for(const c of cells(line)) head.append(inline(document.createElement("th"), c));
      for(i += 2; i < lines.length && /^\s*\|/.test(lines[i]); i++) {
        const row = body.insertRow();
        for(const c of cells(lines[i])) row.append(inline(document.createElement("td"), c));
      }
      const wrap = node("div", "", "table-wrap"); wrap.append(table); root.append(wrap);
    } else if(isList(line)) {
      const list = document.createElement(/^\s*\d+\./.test(line) ? "ol" : "ul");
      for(; i < lines.length && (isList(lines[i]) || /^\s{2,}\S/.test(lines[i])); i++) {
        if(isList(lines[i])) list.append(inline(document.createElement("li"), lines[i].replace(/^\s*([-*]|\d+\.)\s+/, "")));
        else list.lastChild.append(" ", ...inline(document.createDocumentFragment(), lines[i].trim()).childNodes);
      }
      root.append(list);
    } else if(line.startsWith(">")) {
      const quote = document.createElement("blockquote"), body = [];
      for(; i < lines.length && lines[i].startsWith(">"); i++) body.push(lines[i].replace(/^>\s?/, ""));
      root.append(inline(quote, body.join(" ")));
    } else if(/^\s*([-*_])\1\1+\s*$/.test(line)) { root.append(document.createElement("hr")); i++; }
    else {
      const body = [];
      for(; i < lines.length && lines[i].trim() && !(body.length && starts(i)); i++) body.push(lines[i].trim());
      root.append(inline(document.createElement("p"), body.join(" ")));
    }
  }
  return root;
}
function showDocument(raw) {
  const out = $("preview-text"), path = $("preview-path").textContent;
  out.classList.toggle("raw", raw);
  $("raw-toggle").textContent = raw ? "Xem dạng tài liệu" : "Xem văn bản gốc";
  $("raw-toggle").setAttribute("aria-pressed", String(raw));
  if(raw || !path.endsWith(".md")) {
    let text = previewSource;
    if(!raw && path.endsWith(".json")) try { text = JSON.stringify(JSON.parse(previewSource), null, 2); } catch {}
    out.replaceChildren(node("pre", text));
  } else out.replaceChildren(markdown(previewSource));
}
async function showPreview(url, path) {
  const version = ++previewVersion;
  previewSource = null; $("raw-toggle").hidden = true;
  $("preview").hidden = false; $("preview-path").textContent = path; $("preview-text").replaceChildren(node("p", "Đang đọc tài liệu…", "muted"));
  $("preview").scrollIntoView({block:"start"}); $("preview-text").focus({preventScroll:true});
  try {
    const response = await fetch(url, {cache:"no-store", signal:AbortSignal.timeout(20000)});
    if(!response.ok) throw new Error("Không đọc được tài liệu. Hãy kiểm tra lại lần chạy.");
    const text = await response.text();
    if(!document || version !== previewVersion) return;
    previewSource = text; $("raw-toggle").hidden = !path.endsWith(".md"); showDocument(false);
  } catch(error) { if(document && version === previewVersion) $("preview-text").replaceChildren(node("p", errorMessage(error), "error")); }
}
$("history").onchange = () => { if($("history").value) { $("preview").hidden = true; previewVersion++; selectRun($("history").value); } };
$("retry").onclick = () => selectRun(selected);
$("raw-toggle").onclick = () => { if(previewSource !== null) showDocument(!$("preview-text").classList.contains("raw")); };
$("close-preview").onclick = () => { $("preview").hidden = true; previewVersion++; $("history").focus(); };
$("run-form").onsubmit = async event => {
  event.preventDefault(); if(!config) return;
  $("form-error").textContent = ""; $("submit").disabled = true; $("preview").hidden = true;
  const body = Object.fromEntries(new FormData(event.target)); body.notice_version = config.notice_version;
  try {
    const run = await api("/api/runs", {method:"POST", headers:{"Content-Type":"application/json", "X-L3GEN-Client":"web-v1"}, body:JSON.stringify(body)});
    render(run); selected = run.run_id; openWhenDone = run.run_id; await history(); await selectRun(run.run_id);
  } catch(error) {
    $("form-error").textContent = errorMessage(error);
    // A lost POST response may still have started a run; reconcile before permitting another submission.
    try { const runs = await history(); const active = runs.find(r => r.status === "running"); if(active) await selectRun(active.run_id); }
    catch { $("form-error").textContent += " Tải lại trang để kiểm tra trạng thái trước khi chạy lại."; }
  }
};
(async function init() {
  try {
    config = await api("/api/config");
    $("model").textContent = config.model;
    $("notice").textContent = config.offline
      ? "Chế độ phát lại kịch bản offline. Không gọi model và không đo khả năng đọc code của model thật."
      : `Nội dung source trong phạm vi đọc, đường dẫn file, membership và bằng chứng có thể được gửi đến ${config.endpoint}.`;
    const modes = config.modes || ["agent"];
    for(const input of document.querySelectorAll("input[name=mode]")) input.disabled = !modes.includes(input.value);
    if(!modes.includes("oneshot")) $("mode-help").textContent = "Kịch bản offline chỉ phát lại được chế độ agent.";
    for(const [key, value] of Object.entries(config.defaults)) if($(key)) $(key).value = value;
    const runs = await history();
    if(runs.length) await selectRun(runs.find(r => r.status === "running")?.run_id || runs.at(-1).run_id);
  } catch(error) { if(!document) return; $("model").textContent = "Chưa kết nối được server"; $("form-error").textContent = errorMessage(error) + " Hãy tải lại trang."; }
})();
