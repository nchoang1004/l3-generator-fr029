/* Giao diện xem kết quả l3gen — SPEC mục 13.
 *
 * Ràng buộc tự áp, tương ứng mục 13.1:
 *   - Chỉ đọc file JSON do pipeline sinh. Không phân tích lại source.
 *   - Không hiển thị con số nào không suy được từ các file đó. Không làm tròn.
 *   - Dữ liệu đọc từ cây cú pháp và lời do AI viết phải phân biệt được bằng mắt.
 */
'use strict';

const DATA = { iam: null, graph: null, findings: null, descriptions: null, run: null };

/* ---------------------------------------------------------------- tiện ích */

const $ = (sel) => document.querySelector(sel);
const el = (tag, cls, text) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text !== undefined) n.textContent = text;
  return n;
};

/** Luôn dùng hàm này thay cho innerHTML: dữ liệu đến từ source code người khác
 *  viết, có thể chứa ký tự bị trình duyệt hiểu là thẻ HTML. */
const setText = (node, text) => { node.textContent = text; return node; };

const num = (n) => (n === null || n === undefined ? '—' : n.toLocaleString('vi-VN'));

async function loadJSON(name, required) {
  try {
    const res = await fetch('../' + name, { cache: 'no-store' });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    return await res.json();
  } catch (err) {
    if (required) throw new Error(`Không đọc được ${name}: ${err.message}`);
    return null;
  }
}

/* --- nhãn nguồn gốc (SPEC mục 13.4) --------------------------------------
 * exact và full là mặc định, KHÔNG tô màu — tô hết thì không còn gì nổi bật.
 * Chỉ inferred và partial mới được đánh dấu, và reason hiện thẳng ra chứ
 * không giấu trong tooltip. */

function labelCell(item) {
  const box = el('span');
  if (item.confidence === 'inferred') {
    box.appendChild(el('span', 'tag inferred', 'suy ra'));
    box.appendChild(document.createTextNode(' '));
  } else if (item.confidence) {
    box.appendChild(el('span', 'tag plain', item.confidence));
    box.appendChild(document.createTextNode(' '));
  }
  if (item.completeness === 'partial') {
    const t = el('span', 'tag partial', 'chưa đầy đủ');
    if (item.reason) t.title = item.reason;
    box.appendChild(t);
  } else if (item.completeness) {
    box.appendChild(el('span', 'tag plain', item.completeness));
  }
  if (item.reason) box.appendChild(el('span', 'reason', item.reason));
  return box;
}

/** Vị trí source: luôn hiện file:dòng, bấm để chép đường dẫn. */
function locButton(location) {
  if (!location) return el('span', 'muted', '—');
  const text = `${location.file}:${location.line_start}`;
  const b = el('button', 'loc mono', text);
  b.title = 'Bấm để chép đường dẫn';
  b.addEventListener('click', async (e) => {
    e.stopPropagation();
    try { await navigator.clipboard.writeText(text); } catch { /* trình duyệt chặn */ }
    b.classList.add('copied');
    b.textContent = 'đã chép ✓';
    setTimeout(() => { b.classList.remove('copied'); b.textContent = text; }, 1100);
  });
  return b;
}

/** Mô tả do AI viết. Luôn có nền riêng và nhãn "AI" — không bao giờ trình bày
 *  giống dữ liệu đọc từ code. */
function aiText(id) {
  if (!DATA.descriptions) return null;
  const text = DATA.descriptions.descriptions?.[id];
  if (!text) return null;
  return el('span', 'ai-text', text);
}

function table(headers, rows) {
  const t = el('table');
  const thead = el('thead');
  const tr = el('tr');
  headers.forEach((h) => tr.appendChild(el('th', null, h)));
  thead.appendChild(tr);
  t.appendChild(thead);
  const tbody = el('tbody');
  rows.forEach((cells) => tbody.appendChild(cells));
  t.appendChild(tbody);
  return t;
}

function row(cells, onClick) {
  const tr = el('tr');
  cells.forEach((c) => {
    const td = el('td');
    if (c instanceof Node) td.appendChild(c);
    else td.textContent = c === null || c === undefined ? '—' : String(c);
    tr.appendChild(td);
  });
  if (onClick) {
    tr.classList.add('clickable');
    tr.addEventListener('click', () => {
      tr.parentNode.querySelectorAll('tr.selected').forEach((r) => r.classList.remove('selected'));
      tr.classList.add('selected');
      onClick();
    });
  }
  return tr;
}

function dl(pairs) {
  const d = el('dl');
  pairs.forEach(([k, v]) => {
    if (v === null || v === undefined) return;
    d.appendChild(el('dt', null, k));
    const dd = el('dd');
    if (v instanceof Node) dd.appendChild(v);
    else dd.textContent = String(v);
    d.appendChild(dd);
  });
  return d;
}

/* -------------------------------------------------------- U-01 Tổng quan */

function renderOverview() {
  const iam = DATA.iam;
  const m = iam.metrics;
  const stack = iam.detected_stack;

  setText($('#service-name'), stack.services.map((s) => s.name || '(thư mục gốc)').join(', '));

  // Chế độ AI — nói rõ ngay, vì nó quyết định màn Cảnh báo có gì
  const banner = $('#ai-mode');
  banner.className = 'banner ' + (m.ai_enabled ? 'ai' : 'warn');
  setText(banner, m.ai_enabled
    ? 'Lần chạy này CÓ gọi AI. Phần chữ nền tím là do AI viết thêm cho dễ đọc — '
      + 'không phải dữ liệu đọc từ code, đừng dùng làm căn cứ.'
    : 'Lần chạy này chạy với --no-ai: không có mô tả do AI viết. '
      + 'Toàn bộ dữ liệu dưới đây đọc trực tiếp từ cây cú pháp.');

  const cards = $('#metric-cards');
  cards.replaceChildren();
  const metrics = [
    [num(iam.routes.length), 'API route'],
    [num(iam.entities.length), 'bảng dữ liệu'],
    [num(iam.external_calls.length), 'lời gọi ra ngoài'],
    [num(iam.functions.length), 'hàm'],
    [`${num(m.files_analyzed)}/${num(m.files_found)}`, 'file đọc được'],
    [num(m.lines_of_code), 'dòng code'],
    [num(iam.unresolved_references.length), 'tham chiếu chưa nối được'],
    [num(iam.parse_errors.length), 'file lỗi cú pháp'],
  ];
  if (DATA.run?.duration_seconds !== undefined) {
    metrics.push([DATA.run.duration_seconds.toFixed(2) + ' giây', 'thời gian chạy']);
  }
  metrics.forEach(([v, l]) => {
    const c = el('div', 'card');
    c.appendChild(el('div', 'value', v));
    c.appendChild(el('div', 'label', l));
    cards.appendChild(c);
  });

  const rows = stack.services.map((s) => row([
    s.name || '(thư mục gốc)',
    s.language || '—',
    (s.frameworks || []).join(', ') || '—',
    s.orm || '—',
    num(s.file_count),
    labelCell(s),
    s.analyzed ? 'Đã phân tích' : 'Bỏ qua — ' + (s.skip_reason || 'không rõ lý do'),
    s.detection_reason || '—',
  ]));
  $('#services-table').replaceWith(
    Object.assign(
      table(['Đơn vị', 'Ngôn ngữ', 'Framework', 'ORM', 'File', 'Nhãn', 'Trạng thái', 'Căn cứ nhận diện'], rows),
      { id: 'services-table' },
    ),
  );

  const counts = { exact: 0, inferred: 0, full: 0, partial: 0 };
  [...iam.routes, ...iam.entities, ...iam.external_calls].forEach((i) => {
    if (i.confidence in counts) counts[i.confidence] += 1;
    if (i.completeness in counts) counts[i.completeness] += 1;
  });
  const lab = $('#label-cards');
  lab.replaceChildren();
  [
    [counts.exact, 'exact — đọc thẳng từ cú pháp'],
    [counts.inferred, 'inferred — suy từ một quy tắc'],
    [counts.full, 'full — đã biết đủ thuộc tính'],
    [counts.partial, 'partial — còn thuộc tính chưa biết'],
  ].forEach(([v, l]) => {
    const c = el('div', 'card');
    c.appendChild(el('div', 'value', num(v)));
    c.appendChild(el('div', 'label', l));
    lab.appendChild(c);
  });
}

/* -------------------------------------------------------- U-02 API Routes */

function renderRoutes() {
  const routes = DATA.iam.routes;
  const methodSel = $('#route-method');
  [...new Set(routes.map((r) => r.method))].sort().forEach((m) => {
    methodSel.appendChild(Object.assign(el('option', null, m), { value: m }));
  });

  const detail = $('#route-detail');

  function showDetail(r, index) {
    detail.replaceChildren();
    detail.appendChild(el('h3', null, `${r.method} ${r.path}`));

    const resolved = r.calls.filter((c) => c.resolved);
    const unresolved = r.calls.filter((c) => !c.resolved);

    const callList = el('div');
    if (!r.calls.length) callList.appendChild(el('span', 'muted', 'không có lời gọi nào'));
    resolved.forEach((c) => {
      const line = el('div');
      line.appendChild(el('code', null, c.name));
      line.appendChild(el('span', 'muted', ' → ' + (c.resolved_module || '?')));
      callList.appendChild(line);
    });
    unresolved.forEach((c) => {
      const line = el('div', 'unresolved');
      line.appendChild(el('code', null, c.name));
      line.appendChild(el('span', null, ' — không xác định được đích'));
      if (c.reason) line.appendChild(el('span', 'reason', c.reason));
      callList.appendChild(line);
    });

    const pairs = [
      ['Hàm xử lý', r.handler_function],
      ['Đơn vị', r.service],
      ['Nhãn', labelCell(r)],
      ['Vị trí', locButton(r.location)],
      [`Gọi tới (${resolved.length} nối được, ${unresolved.length} chưa)`, callList],
    ];
    const ai = aiText('route-' + index);
    if (ai) pairs.splice(1, 0, ['Mô tả', ai]);
    detail.appendChild(dl(pairs));
  }

  function apply() {
    const q = $('#route-search').value.trim().toLowerCase();
    const method = methodSel.value;
    const conf = $('#route-confidence').value;
    const comp = $('#route-completeness').value;

    const rows = [];
    routes.forEach((r, i) => {
      if (method && r.method !== method) return;
      if (conf && r.confidence !== conf) return;
      if (comp && r.completeness !== comp) return;
      if (q && !(r.path.toLowerCase().includes(q)
                || (r.handler_function || '').toLowerCase().includes(q))) return;
      const resolved = r.calls.filter((c) => c.resolved).length;
      rows.push(row([
        r.method,
        el('code', null, r.path),
        el('code', null, r.handler_function || '—'),
        `${resolved}/${r.calls.length}`,
        labelCell(r),
        locButton(r.location),
      ], () => showDetail(r, i)));
    });

    setText($('#route-count'), `${rows.length} / ${routes.length} route`);
    const t = table(['Method', 'Đường dẫn', 'Hàm xử lý', 'Gọi nối được', 'Nhãn', 'Vị trí'], rows);
    t.id = 'routes-table';
    $('#routes-table').replaceWith(t);
  }

  ['#route-search', '#route-method', '#route-confidence', '#route-completeness']
    .forEach((s) => $(s).addEventListener('input', apply));
  apply();
}

/* ----------------------------------------------------- U-03 Bảng dữ liệu */

function renderEntities() {
  const entities = DATA.iam.entities;
  const detail = $('#entity-detail');

  // Tên bảng null nghĩa là công cụ không đọc được, không phải bảng không có tên.
  const tableName = (e) => (e.table_name === null || e.table_name === undefined
    ? el('span', 'muted', 'chưa đọc được')
    : el('code', null, e.table_name));

  function showDetail(e, index) {
    detail.replaceChildren();
    detail.appendChild(el('h3', null, e.class_name));

    const cols = el('div', 'scroll-x');
    if (!e.columns.length) {
      cols.appendChild(el('span', 'muted', 'không đọc được cột nào'));
    } else {
      cols.appendChild(table(['Cột', 'Kiểu', 'Khoá'], e.columns.map((c) => row([
        c.name,
        el('code', null, c.type),
        c.is_primary_key ? 'khoá chính' : (c.foreign_key_ref ? '→ ' + c.foreign_key_ref : '—'),
      ]))));
    }

    let baseNode = el('span', 'muted', '—');
    if (e.base_class) {
      baseNode = el('span', e.base_class.resolved ? null : 'unresolved');
      baseNode.appendChild(el('code', null, e.base_class.name));
      baseNode.appendChild(el('span', 'muted', e.base_class.resolved
        ? ' — ' + e.base_class.resolved_module
        : ' — không xác định được đích'));
      if (e.base_class.reason) baseNode.appendChild(el('span', 'reason', e.base_class.reason));
    }

    const pairs = [
      ['Tên bảng', tableName(e)],
      ['Class cha', baseNode],
      ['Đơn vị', e.service],
      ['Nhãn', labelCell(e)],
      ['Vị trí', locButton(e.location)],
      [`Cột (${e.columns.length})`, cols],
    ];
    const ai = aiText('entity-' + index);
    if (ai) pairs.splice(1, 0, ['Mô tả', ai]);
    detail.appendChild(dl(pairs));
  }

  function apply() {
    const q = $('#entity-search').value.trim().toLowerCase();
    const rows = [];
    entities.forEach((e, i) => {
      if (q && !(e.class_name.toLowerCase().includes(q)
                 || (e.table_name || '').toLowerCase().includes(q))) return;
      const pk = e.columns.filter((c) => c.is_primary_key).length;
      const fk = e.columns.filter((c) => c.foreign_key_ref).length;
      rows.push(row([
        el('code', null, e.class_name),
        tableName(e),
        num(e.columns.length),
        num(pk),
        num(fk),
        labelCell(e),
        locButton(e.location),
      ], () => showDetail(e, i)));
    });
    setText($('#entity-count'), `${rows.length} / ${entities.length} bảng`);
    const t = table(['Class', 'Bảng', 'Cột', 'Khoá chính', 'Khoá ngoại', 'Nhãn', 'Vị trí'], rows);
    t.id = 'entities-table';
    $('#entities-table').replaceWith(t);
  }

  $('#entity-search').addEventListener('input', apply);
  apply();
}

/* --------------------------------------------------------- U-05 Cảnh báo */

const CATEGORY_LABEL = {
  orphan_entity: 'Bảng chưa thấy ai dùng',
  empty_handler_calls: 'Hàm xử lý chưa nối được lời gọi nào',
  external_call_no_error_handling: 'Gọi ra ngoài không bắt lỗi',
  route_without_entity: 'Route không chạm tới bảng dữ liệu nào',
};

function renderFindings() {
  const body = $('#findings-body');
  body.replaceChildren();

  if (!DATA.findings) {
    body.appendChild(el('div', 'banner warn',
      'Thư mục kết quả không có findings.json, nên không hiển thị được cảnh báo nào. '
      + 'File này do bước rà soát sinh ra.'));
    return;
  }

  const findings = DATA.findings.findings || [];

  const note = el('div', 'banner ' + (DATA.iam.metrics.ai_enabled ? 'ai' : 'warn'));
  setText(note, DATA.iam.metrics.ai_enabled
    ? 'Việc phát hiện cảnh báo là tất định — đếm từ dữ liệu trong IAM, không do AI quyết. '
      + 'AI chỉ viết lại câu tóm tắt cho dễ đọc.'
    : 'Chạy với --no-ai. Các cảnh báo dưới đây vẫn đầy đủ vì việc phát hiện là tất định, '
      + 'chỉ khác là câu tóm tắt do công cụ viết chứ không phải AI.');
  body.appendChild(note);

  if (!findings.length) {
    body.appendChild(el('p', 'muted', 'Không có cảnh báo nào trong lần chạy này.'));
    return;
  }

  const groups = new Map();
  findings.forEach((f) => {
    if (!groups.has(f.category)) groups.set(f.category, []);
    groups.get(f.category).push(f);
  });

  [...groups.entries()].sort().forEach(([cat, items]) => {
    body.appendChild(el('h2', 'group-title',
      `${CATEGORY_LABEL[cat] || cat} (${items.length})`));
    items.forEach((f) => {
      const card = el('div', 'finding');
      card.appendChild(el('div', 'cat', f.category));
      card.appendChild(el('p', null, f.summary));
      const foot = el('div', 'muted');
      foot.appendChild(locButton(f.evidence_location));
      if (f.related_iam_ref) {
        foot.appendChild(document.createTextNode('  ·  '));
        foot.appendChild(el('code', null, f.related_iam_ref));
      }
      card.appendChild(foot);
      body.appendChild(card);
    });
  });
}

/* ------------------------------------------------ U-06 Giới hạn đã biết */

function renderLimits() {
  const iam = DATA.iam;
  const body = $('#limits-body');
  body.replaceChildren();
  let any = false;

  const skipped = iam.detected_stack.services.filter((s) => !s.analyzed);
  if (skipped.length) {
    any = true;
    body.appendChild(el('h2', 'group-title', `Đơn vị bị bỏ qua (${skipped.length})`));
    const ul = el('ul', 'tight');
    skipped.forEach((s) => {
      const li = el('li');
      li.appendChild(el('strong', null, s.name || '(thư mục gốc)'));
      li.appendChild(document.createTextNode(
        ` — ${s.language || 'chưa rõ ngôn ngữ'}, ${s.file_count} file: ${s.skip_reason}. `
        + 'Phần hệ thống này không có trong tài liệu.'));
      ul.appendChild(li);
    });
    body.appendChild(ul);
  }

  if (iam.parse_errors.length) {
    any = true;
    body.appendChild(el('h2', 'group-title',
      `File bỏ qua vì lỗi cú pháp (${iam.parse_errors.length})`));
    const ul = el('ul', 'tight');
    iam.parse_errors.forEach((e) => {
      const li = el('li');
      li.appendChild(el('code', null, e.file));
      li.appendChild(document.createTextNode(': ' + e.error_message));
      ul.appendChild(li);
    });
    body.appendChild(ul);
  }

  const unknownTable = iam.entities.filter((e) => e.table_name === null || e.table_name === undefined);
  if (unknownTable.length) {
    any = true;
    body.appendChild(el('h2', 'group-title',
      `Bảng không đọc được tên (${unknownTable.length})`));
    body.appendChild(el('p', 'note',
      'Các lớp này không khai __tablename__; lớp cơ sở của repo tự sinh tên lúc chạy, '
      + 'mỗi repo một quy tắc riêng. Công cụ ghi "chưa đọc được" thay vì đoán.'));
    const ul = el('ul', 'tight');
    unknownTable.forEach((e) => {
      const li = el('li');
      li.appendChild(el('code', null, e.class_name));
      li.appendChild(document.createTextNode(' — '));
      li.appendChild(locButton(e.location));
      ul.appendChild(li);
    });
    body.appendChild(ul);
  }

  const conditional = iam.routes.filter((r) => r.reason && r.reason.includes('chỉ được đăng ký khi'));
  if (conditional.length) {
    any = true;
    body.appendChild(el('h2', 'group-title',
      `Route chỉ tồn tại ở một số môi trường (${conditional.length})`));
    const ul = el('ul', 'tight');
    conditional.forEach((r) => {
      const li = el('li');
      li.appendChild(el('code', null, `${r.method} ${r.path}`));
      li.appendChild(el('span', 'reason', r.reason));
      ul.appendChild(li);
    });
    body.appendChild(ul);
  }

  if (iam.unresolved_references.length) {
    any = true;
    body.appendChild(el('h2', 'group-title',
      `Tham chiếu chưa nối được đích (${iam.unresolved_references.length})`));
    body.appendChild(el('p', 'note',
      'Đây là giới hạn đã biết của phân tích tĩnh, không phải lỗi: phần lớn do biến '
      + 'không khai báo kiểu, hoặc tên hàm chỉ có lúc chạy. Công cụ ghi "chưa biết" '
      + 'thay vì đoán.'));
    const ul = el('ul', 'tight');
    iam.unresolved_references.slice(0, 200).forEach((u) => {
      const li = el('li', 'unresolved');
      li.appendChild(document.createTextNode(u.description + ' — '));
      li.appendChild(locButton(u.location));
      ul.appendChild(li);
    });
    body.appendChild(ul);
    if (iam.unresolved_references.length > 200) {
      body.appendChild(el('p', 'muted',
        `Đang hiện 200 mục đầu. Còn ${iam.unresolved_references.length - 200} mục nữa, `
        + 'xem đầy đủ trong IAM.json.'));
    }
  }

  if (!any) {
    body.appendChild(el('p', null, 'Không có giới hạn nào được ghi nhận trong lần chạy này.'));
  }
}

/* ------------------------------------------------------------ U-04 Đồ thị */

const NODE_COLOR = {
  Application: '#e68a00', Class: '#17a2a4',
  Route: '#1f77b4', Entity: '#2ca02c', Function: '#7f7f7f',
  Module: '#9467bd', ExternalHost: '#d62728', Unresolved: '#bbbbbb',
};

/* Bật sẵn loại nào.
 *
 * Route và Entity KHÔNG bao giờ nối thẳng với nhau: đường đi thật là
 * Route --calls--> Function --reads_writes--> Entity. Bỏ Function ra khỏi đây
 * thì đồ thị chỉ còn một đám chấm rời, không cạnh nào có đủ hai đầu.
 *
 * Module và Unresolved để tắt: chúng đông nhất mà nói ít nhất về kiến trúc.
 * Người dùng bật thêm được ở bộ lọc. */
const DEFAULT_ON = ['Application', 'Route', 'Entity', 'ExternalHost', 'Function'];

/* Thứ tự ưu tiên khi phải cắt bớt. */
const KEEP_ORDER = ['Application', 'Route', 'Entity', 'ExternalHost', 'Function', 'Class', 'Module', 'Unresolved'];
const MAX_NODES = 400;

/* Bao nhiêu suất dành cho node "quan trọng", phần còn lại để nối chúng lại.
 *
 * Chỉ ưu tiên theo loại là không đủ: dispatch có 290 Route + 113 Entity, đã vượt
 * giới hạn ngay từ hai loại đó, nên không Function nào lọt vào — mà Function mới
 * là thứ nối Route với Entity. Kết quả là 400 chấm rời không cạnh nào.
 * Vì vậy chừa nửa suất để kéo theo node trung gian. */
const SEED_SHARE = 0.5;

/* Trên ngưỡng này thì thôi vẽ nhãn: chữ chồng lên nhau còn khó đọc hơn là
 * không có chữ. Rê chuột hoặc bấm vào node vẫn xem được tên đầy đủ. */
const LABEL_LIMIT = 120;

let graphState = null;

function renderGraph() {
  const svg = $('#graph-svg');
  const filters = $('#graph-filters');
  filters.replaceChildren();

  if (!DATA.graph) {
    $('#graph-note').textContent =
      'Thư mục kết quả không có graph.json nên không vẽ được đồ thị.';
    return;
  }

  const types = [...new Set(DATA.graph.nodes.map((n) => n.type))].sort();
  const enabled = new Set(types.filter((t) => DEFAULT_ON.includes(t)));
  if (!enabled.size) types.forEach((t) => enabled.add(t));

  types.forEach((t) => {
    const count = DATA.graph.nodes.filter((n) => n.type === t).length;
    const lab = el('label');
    const cb = Object.assign(el('input'), { type: 'checkbox', checked: enabled.has(t) });
    cb.addEventListener('change', () => {
      if (cb.checked) enabled.add(t); else enabled.delete(t);
      draw();
    });
    const dot = el('span', 'legend-dot');
    dot.style.background = NODE_COLOR[t] || '#888';
    lab.append(cb, dot, document.createTextNode(` ${t} (${count})`));
    filters.appendChild(lab);
  });

  function draw() {
    const rank = (n) => {
      const i = KEEP_ORDER.indexOf(n.type);
      return i === -1 ? KEEP_ORDER.length : i;
    };
    const all = DATA.graph.nodes.filter((n) => enabled.has(n.type));
    const byPriority = [...all].sort((a, b) => rank(a) - rank(b));

    // Bước 1: lấy node quan trọng nhất làm hạt giống.
    const ids = new Set(byPriority.slice(0, Math.ceil(MAX_NODES * SEED_SHARE)).map((n) => n.id));
    // Bước 2: kéo thêm node đang bật mà nối trực tiếp với hạt giống, cho tới khi
    // hết suất. Nhờ vậy khung nhìn luôn có cạnh chứ không phải một đám chấm rời.
    const canAdd = new Set(byPriority.map((n) => n.id));
    for (const e of DATA.graph.edges) {
      if (ids.size >= MAX_NODES) break;
      const hasS = ids.has(e.source_id), hasT = ids.has(e.target_id);
      if (hasS === hasT) continue;
      const other = hasS ? e.target_id : e.source_id;
      if (canAdd.has(other)) ids.add(other);
    }
    // Bước 3: còn dư suất thì bù nốt theo độ ưu tiên.
    for (const n of byPriority) {
      if (ids.size >= MAX_NODES) break;
      ids.add(n.id);
    }

    const shown = all.filter((n) => ids.has(n.id));
    const edges = DATA.graph.edges.filter((e) => ids.has(e.source_id) && ids.has(e.target_id));

    // SPEC mục 13.4 cấm ẩn thông tin mà không nói. Luôn in ra đang ẩn bao nhiêu.
    const hiddenByFilter = DATA.graph.nodes.length - all.length;
    const hiddenByCap = all.length - shown.length;
    const parts = [`Đang vẽ ${shown.length} node và ${edges.length} cạnh.`];
    if (hiddenByCap > 0) {
      parts.push(`Còn ${hiddenByCap} node đang bật nhưng chưa vẽ vì vượt giới hạn `
        + `${MAX_NODES} node — vẽ hết thì rối tới mức không đọc được gì. `
        + `Phần được giữ là một mẫu có nối với nhau: ưu tiên `
        + `${KEEP_ORDER.join(' → ')}, rồi kéo thêm node nối trực tiếp với chúng. `
        + `Dùng bộ lọc để xem đúng phần bạn cần.`);
    }
    if (hiddenByFilter > 0) parts.push(`${hiddenByFilter} node đang tắt ở bộ lọc.`);
    if (shown.length && !edges.length) {
      parts.push('Không cạnh nào có đủ hai đầu trong khung nhìn — bật thêm loại node '
        + 'ở bộ lọc để thấy đường nối.');
    }
    if (shown.length > LABEL_LIMIT) {
      parts.push(`Đang ẩn nhãn vì hơn ${LABEL_LIMIT} node thì chữ chồng lên nhau — `
        + 'rê chuột hoặc bấm vào node để xem tên.');
    }
    parts.push(`Tổng cộng graph.json có ${DATA.graph.nodes.length} node, `
      + `${DATA.graph.edges.length} cạnh.`);
    $('#graph-note').textContent = parts.join(' ');

    layout(svg, shown, edges);
  }

  draw();
}

/** Layout lực đẩy viết tay: node đẩy nhau, cạnh kéo lại, tất cả hút về tâm.
 *  Đủ để nhìn ra cụm; không nhằm thay thế một thư viện đồ thị đầy đủ. */
function layout(svg, nodes, edges) {
  if (graphState?.stop) graphState.stop();

  const W = svg.clientWidth || 900;
  const H = svg.clientHeight || 500;
  const NS = 'http://www.w3.org/2000/svg';

  const pos = nodes.map((n, i) => {
    const angle = (i / Math.max(nodes.length, 1)) * Math.PI * 2;
    return {
      node: n,
      x: W / 2 + Math.cos(angle) * Math.min(W, H) * 0.35,
      y: H / 2 + Math.sin(angle) * Math.min(W, H) * 0.35,
      vx: 0, vy: 0,
    };
  });
  const index = new Map(pos.map((p) => [p.node.id, p]));
  const links = edges
    .map((e) => ({ s: index.get(e.source_id), t: index.get(e.target_id), edge: e }))
    .filter((l) => l.s && l.t);

  svg.replaceChildren();
  const view = document.createElementNS(NS, 'g');
  svg.appendChild(view);

  const lineFor = links.map((l) => {
    const ln = document.createElementNS(NS, 'line');
    ln.setAttribute('class', 'edge' + (l.edge.resolved === false ? ' unresolved' : ''));
    const title = document.createElementNS(NS, 'title');
    title.textContent = l.edge.type + (l.edge.resolved === false ? ' (chưa nối được đích)' : '');
    ln.appendChild(title);
    view.appendChild(ln);
    return ln;
  });

  const detail = $('#graph-detail');
  const circleFor = pos.map((p) => {
    const g = document.createElementNS(NS, 'g');
    const c = document.createElementNS(NS, 'circle');
    c.setAttribute('r', p.node.type === 'Route' ? 6 : 5);
    c.setAttribute('class', 'node' + (p.node.type === 'Unresolved' ? ' dim' : ''));
    c.setAttribute('fill', NODE_COLOR[p.node.type] || '#888');
    const title = document.createElementNS(NS, 'title');
    title.textContent = `${p.node.type}: ${p.node.label}`;
    c.appendChild(title);

    g.append(c);
    // Đông node thì nhãn chồng lên nhau tới mức không đọc được gì — tệ hơn là
    // không có nhãn. Tên vẫn xem được bằng cách rê chuột hoặc bấm vào node.
    if (nodes.length <= LABEL_LIMIT) {
      const label = document.createElementNS(NS, 'text');
      label.setAttribute('dx', 8);
      label.setAttribute('dy', 3);
      label.textContent = p.node.label.length > 34
        ? p.node.label.slice(0, 33) + '…' : p.node.label;
      g.append(label);
    }
    view.appendChild(g);

    c.addEventListener('click', (ev) => {
      ev.stopPropagation();
      detail.classList.remove('hidden');
      detail.replaceChildren();
      detail.appendChild(el('h3', null, p.node.label));
      const ins = links.filter((l) => l.t === p).length;
      const outs = links.filter((l) => l.s === p).length;
      detail.appendChild(dl([
        ['Loại', p.node.type],
        ['Vị trí', locButton(p.node.location)],
        ['Cạnh trong khung nhìn', `${outs} đi ra, ${ins} đi vào`],
        ['id', el('code', null, p.node.id)],
      ]));
      const close = el('button', 'ghost', 'Đóng');
      close.addEventListener('click', () => detail.classList.add('hidden'));
      detail.appendChild(close);
    });

    // Kéo thả node
    c.addEventListener('pointerdown', (ev) => {
      ev.stopPropagation();
      c.setPointerCapture(ev.pointerId);
      p.fixed = true;
      const move = (e2) => {
        const pt = toLocal(e2);
        p.x = pt.x; p.y = pt.y; p.vx = 0; p.vy = 0;
        paint();
      };
      const up = () => {
        p.fixed = false;
        c.removeEventListener('pointermove', move);
        c.removeEventListener('pointerup', up);
      };
      c.addEventListener('pointermove', move);
      c.addEventListener('pointerup', up);
    });

    return g;
  });

  // Phóng to và dời khung nhìn
  const cam = { x: 0, y: 0, k: 1 };
  const applyCam = () =>
    view.setAttribute('transform', `translate(${cam.x} ${cam.y}) scale(${cam.k})`);
  const toLocal = (ev) => {
    const r = svg.getBoundingClientRect();
    return { x: (ev.clientX - r.left - cam.x) / cam.k, y: (ev.clientY - r.top - cam.y) / cam.k };
  };

  svg.onwheel = (ev) => {
    ev.preventDefault();
    const r = svg.getBoundingClientRect();
    const mx = ev.clientX - r.left, my = ev.clientY - r.top;
    const k = Math.min(4, Math.max(0.2, cam.k * (ev.deltaY < 0 ? 1.12 : 1 / 1.12)));
    cam.x = mx - (mx - cam.x) * (k / cam.k);
    cam.y = my - (my - cam.y) * (k / cam.k);
    cam.k = k;
    applyCam();
  };
  svg.onpointerdown = (ev) => {
    svg.classList.add('panning');
    const sx = ev.clientX - cam.x, sy = ev.clientY - cam.y;
    const move = (e2) => { cam.x = e2.clientX - sx; cam.y = e2.clientY - sy; applyCam(); };
    const up = () => {
      svg.classList.remove('panning');
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', up);
    };
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', up);
  };

  function paint() {
    links.forEach((l, i) => {
      lineFor[i].setAttribute('x1', l.s.x); lineFor[i].setAttribute('y1', l.s.y);
      lineFor[i].setAttribute('x2', l.t.x); lineFor[i].setAttribute('y2', l.t.y);
    });
    pos.forEach((p, i) => circleFor[i].setAttribute('transform', `translate(${p.x} ${p.y})`));
  }

  // Mô phỏng: chạy một số vòng rồi dừng hẳn, không quay vòng vô tận tốn pin.
  let tick = 0;
  const TICKS = 300;
  let raf = 0;
  function step() {
    const repel = 2200, spring = 0.008, ideal = 55, damp = 0.85;
    for (let i = 0; i < pos.length; i++) {
      const a = pos[i];
      if (a.fixed) continue;
      let fx = (W / 2 - a.x) * 0.002, fy = (H / 2 - a.y) * 0.002;
      for (let j = 0; j < pos.length; j++) {
        if (i === j) continue;
        const b = pos[j];
        let dx = a.x - b.x, dy = a.y - b.y;
        let d2 = dx * dx + dy * dy;
        if (d2 < 1) { d2 = 1; dx = Math.random() - 0.5; dy = Math.random() - 0.5; }
        const f = repel / d2;
        const d = Math.sqrt(d2);
        fx += (dx / d) * f; fy += (dy / d) * f;
      }
      a.vx = (a.vx + fx) * damp;
      a.vy = (a.vy + fy) * damp;
    }
    links.forEach((l) => {
      const dx = l.t.x - l.s.x, dy = l.t.y - l.s.y;
      const d = Math.max(Math.sqrt(dx * dx + dy * dy), 0.01);
      const f = (d - ideal) * spring;
      const ux = (dx / d) * f * d, uy = (dy / d) * f * d;
      if (!l.s.fixed) { l.s.vx += ux; l.s.vy += uy; }
      if (!l.t.fixed) { l.t.vx -= ux; l.t.vy -= uy; }
    });
    pos.forEach((p) => {
      if (p.fixed) return;
      p.x += Math.max(-25, Math.min(25, p.vx));
      p.y += Math.max(-25, Math.min(25, p.vy));
    });
    paint();
    if (++tick < TICKS) raf = requestAnimationFrame(step);
  }
  applyCam();
  raf = requestAnimationFrame(step);
  graphState = { stop: () => cancelAnimationFrame(raf) };
}

/* ----------------------------------------------------------- điều hướng */

function setupTabs() {
  const buttons = [...$('#tabs').querySelectorAll('button')];
  let graphDrawn = false;
  buttons.forEach((b) => b.addEventListener('click', () => {
    buttons.forEach((x) => x.classList.toggle('active', x === b));
    document.querySelectorAll('.screen').forEach((s) => s.classList.add('hidden'));
    $('#screen-' + b.dataset.screen).classList.remove('hidden');
    // Vẽ đồ thị lúc mở lần đầu: cần biết kích thước thật của khung SVG.
    if (b.dataset.screen === 'graph' && !graphDrawn) { graphDrawn = true; renderGraph(); }
  }));
}

function setupTheme() {
  const btn = $('#theme-toggle');
  const saved = localStorage.getItem('l3gen-theme');
  const dark = saved ? saved === 'dark'
    : window.matchMedia('(prefers-color-scheme: dark)').matches;
  const apply = (on) => {
    document.body.classList.toggle('dark', on);
    btn.textContent = on ? 'Nền sáng' : 'Nền tối';
    localStorage.setItem('l3gen-theme', on ? 'dark' : 'light');
  };
  apply(dark);
  btn.addEventListener('click', () => apply(!document.body.classList.contains('dark')));
}

async function main() {
  setupTheme();
  try {
    DATA.iam = await loadJSON('IAM.json', true);
    DATA.graph = await loadJSON('graph.json', false);
    DATA.findings = await loadJSON('findings.json', false);
    DATA.descriptions = await loadJSON('descriptions.json', false);
    DATA.run = await loadJSON('run.json', false);
  } catch (err) {
    $('#loading').classList.add('hidden');
    const box = $('#load-error');
    box.classList.remove('hidden');
    setText(box, err.message
      + '  —  Giao diện này phải chạy qua lệnh `l3gen ui <thư-mục-kết-quả>`; '
      + 'mở thẳng file HTML thì trình duyệt chặn việc đọc file JSON.');
    return;
  }

  renderOverview();
  renderRoutes();
  renderEntities();
  renderFindings();
  renderLimits();
  setupTabs();

  $('#loading').classList.add('hidden');
  $('#app').classList.remove('hidden');
}

main();
