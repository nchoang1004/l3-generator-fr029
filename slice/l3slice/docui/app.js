"use strict";
const $ = id => document.getElementById(id);
const labels = {running:"Đang chạy",finished:"Đã xuất kết quả",failed:"Gặp lỗi",completed:"Hoàn tất",partial:"Chưa đầy đủ",passed:"Khớp",not_evaluated:"Chưa đối chiếu",ready:"Sẵn sàng"};
let config, selected = null, timer, previewVersion = 0;
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
  $("history").replaceChildren(node("option", "Chọn lần chạy trong phiên server"));
  $("history").firstChild.value = "";
  for(const run of [...runs].reverse()) {
    const option = node("option", `${run.name} · ${labels[run.status] || run.status} · ${run.run_id.slice(-6)}`);
    option.value = run.run_id; $("history").append(option);
  }
  $("history").hidden = !runs.length;
  $("history").value = selected || "";
  $("submit").disabled = runs.some(r => r.status === "running");
  return runs;
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
  $("coverage").textContent = r.coverage.complete ? "Đủ trong phạm vi" : "Chưa đọc đủ";
  $("parity").textContent = labels[r.architecture_parity.status] || r.architecture_parity.status;
  const files = r.coverage.files;
  const complete = files.filter(f => !f.missing.length && !f.cut_lines.length).length;
  $("coverage-note").textContent = `${complete}/${files.length} file trong phạm vi đã đọc đủ; ${r.coverage.not_readable.length} file ngoài phạm vi đọc. ${r.agent.turns} lượt model. ${r.agent.reason || ""}`;
  $("output-path").textContent = run.output_directory;
  $("artifacts").replaceChildren();
  for(const art of r.artifacts) {
    const row = node("div", "", "artifact"), title = node("div", art.path, "artifact-name");
    title.append(node("small", labels[art.status] || art.status)); row.append(title);
    if(art.status === "ready") {
      const url = `/api/runs/${encodeURIComponent(run.run_id)}/artifacts/${encodeURIComponent(art.artifact_id)}`;
      const actions = node("div", "", "artifact-actions"), preview = node("button", "Xem");
      preview.type = "button"; preview.setAttribute("aria-label", `Xem ${art.path}`);
      preview.onclick = () => showPreview(url, art.path);
      const download = node("a", "Tải xuống", "download"); download.href = url; download.download = art.path.split("/").pop();
      download.setAttribute("aria-label", `Tải ${art.path}`); actions.append(preview, download); row.append(actions);
    }
    $("artifacts").append(row);
  }
  $("limits-title").textContent = `Giới hạn cần xem (${r.limitations.length})`;
  $("limits-panel").open = r.limitations.length > 0;
  $("limits").replaceChildren(...r.limitations.map(l => node("li", `${l.code}: ${l.message}`)));
  $("coverage-files").replaceChildren(...files.map(f => {
    const tr = document.createElement("tr");
    tr.append(node("td", f.path), node("td", !f.missing.length && !f.cut_lines.length ? "Đã đọc đủ" : "Chưa đủ"), node("td", `Thiếu: ${JSON.stringify(f.missing)}; cắt: ${JSON.stringify(f.cut_lines)}`));
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
    if(selected !== id) return;
    render(run);
    if(run.status === "running") timer = setTimeout(() => selectRun(id), 1500);
    else await history();
  } catch(error) {
    if(selected !== id) return;
    $("empty").hidden = true; $("run").hidden = false;
    $("status").textContent = "Mất kết nối";
    $("run-message").textContent = errorMessage(error); $("retry").hidden = false;
  }
}
async function showPreview(url, path) {
  const version = ++previewVersion;
  $("preview").hidden = false; $("preview-path").textContent = path; $("preview-text").textContent = "Đang đọc tài liệu…";
  $("preview").scrollIntoView({block:"start"}); $("preview-text").focus({preventScroll:true});
  try {
    const response = await fetch(url, {cache:"no-store", signal:AbortSignal.timeout(20000)});
    if(!response.ok) throw new Error("Không đọc được tài liệu. Hãy kiểm tra lại lần chạy.");
    const text = await response.text();
    if(version === previewVersion) $("preview-text").textContent = text; // Source/Markdown never becomes executable HTML.
  } catch(error) { if(version === previewVersion) $("preview-text").textContent = errorMessage(error); }
}
$("history").onchange = () => { if($("history").value) { $("preview").hidden = true; previewVersion++; selectRun($("history").value); } };
$("retry").onclick = () => selectRun(selected);
$("close-preview").onclick = () => { $("preview").hidden = true; previewVersion++; $("history").focus(); };
$("run-form").onsubmit = async event => {
  event.preventDefault(); if(!config) return;
  $("form-error").textContent = ""; $("submit").disabled = true; $("preview").hidden = true;
  const body = Object.fromEntries(new FormData(event.target)); body.notice_version = config.notice_version;
  try {
    const run = await api("/api/runs", {method:"POST", headers:{"Content-Type":"application/json", "X-L3GEN-Client":"web-v1"}, body:JSON.stringify(body)});
    render(run); selected = run.run_id; await history(); await selectRun(run.run_id);
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
    for(const [key, value] of Object.entries(config.defaults)) if($(key)) $(key).value = value;
    const runs = await history();
    if(runs.length) await selectRun(runs.find(r => r.status === "running")?.run_id || runs.at(-1).run_id);
  } catch(error) { $("model").textContent = "Chưa kết nối được server"; $("form-error").textContent = errorMessage(error) + " Hãy tải lại trang."; }
})();
