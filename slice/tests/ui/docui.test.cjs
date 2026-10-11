// DOM integration tests, not a browser/layout test. Requires jsdom and Python 3.11+.
const {test, before, after} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {spawn} = require('node:child_process');
const {JSDOM} = require(process.env.L3_UI_JSDOM || 'jsdom');
const slice = path.resolve(__dirname, '../..');
let server, origin, temp;
const waitFor = async condition => {
  const end = Date.now() + 10000;
  while(Date.now() < end) { if(condition()) return; await new Promise(r => setTimeout(r, 25)); }
  throw new Error('Timed out waiting for UI state');
};
before(async () => {
  temp = fs.mkdtempSync(path.join(os.tmpdir(), 'fr029-dom-'));
  server = spawn(process.env.L3_UI_PYTHON || 'python', ['-m', 'l3slice.docweb', '--workdir', temp,
    '--port', '0', '--script', 'demo/fr029.script.json', '--source', 'tests/fixtures/fr029_e2e',
    '--membership', 'tests/fixtures/fr029_e2e.membership.json'], {cwd:slice, windowsHide:true});
  let output = '';
  server.stdout.on('data', chunk => { output += chunk; origin = output.match(/http:\/\/127\.0\.0\.1:\d+/)?.[0]; });
  server.stderr.on('data', chunk => { output += chunk; });
  await waitFor(() => origin || server.exitCode !== null);
  assert.ok(origin, output);
});
after(async () => {
  if(server && server.exitCode === null) {
    const exited = new Promise(resolve => server.once('exit', resolve));
    server.kill(); await exited;
  }
  // Only this test's mkdtemp directory; leave source and product output untouched.
  if(temp) {
    assert.equal(path.dirname(path.resolve(temp)), path.resolve(os.tmpdir()));
    assert.ok(path.basename(temp).startsWith('fr029-dom-'));
    fs.rmSync(temp, {recursive:true});
  }
});
async function page() {
  const dom = new JSDOM(fs.readFileSync(path.join(slice, 'l3slice/docui/index.html'), 'utf8'), {url:origin, runScripts:'outside-only'});
  dom.window.fetch = (url, options) => fetch(new URL(url, origin), options);
  dom.window.AbortSignal = AbortSignal;
  dom.window.HTMLElement.prototype.scrollIntoView = () => {};
  dom.window.eval(fs.readFileSync(path.join(slice, 'l3slice/docui/app.js'), 'utf8'));
  await waitFor(() => !dom.window.document.getElementById('submit').disabled);
  if(!dom.window.document.getElementById('history').hidden)
    await waitFor(() => !dom.window.document.getElementById('result').hidden);
  return dom;
}
test('offline source -> rendered verdicts -> preview -> download -> reload', async () => {
  const dom = await page();
  const d = dom.window.document;
  try {
    assert.match(d.getElementById('notice').textContent, /offline/);
    assert.equal(d.getElementById('result').hidden, true);
    d.getElementById('consent').click(); d.getElementById('submit').click();
    await waitFor(() => d.getElementById('status').textContent === 'Đã xuất kết quả');
    assert.equal(d.getElementById('coverage').textContent, 'Đủ trong phạm vi');
    assert.equal(d.getElementById('parity').textContent, 'Chưa đối chiếu');
    assert.match(d.getElementById('limits').textContent, /DIAGRAM_NOT_PROVIDED/);
    d.querySelector('#artifacts button').click();
    await waitFor(() => !d.getElementById('preview-text').textContent.startsWith('Đang đọc'));
    assert.ok(d.getElementById('preview-text').textContent.length > 100);
    const link = d.querySelector('#artifacts a');
    const response = await fetch(link.href);
    assert.equal(response.status, 200); assert.match(response.headers.get('content-disposition'), /attachment/);
    const reloaded = await page();
    try { await waitFor(() => !reloaded.window.document.getElementById('result').hidden); }
    finally { reloaded.window.close(); }
  } finally { dom.window.close(); }
});
test('invalid source displays actionable error and enables retry', async () => {
  const dom = await page(); const d = dom.window.document;
  try {
    d.getElementById('source').value = 'relative/path';
    d.getElementById('consent').click(); d.getElementById('submit').click();
    await waitFor(() => !!d.getElementById('form-error').textContent);
    await waitFor(() => !d.getElementById('submit').disabled);
    assert.match(d.getElementById('form-error').textContent, /đường dẫn tuyệt đối/);
  } finally { dom.window.close(); }
});
test('source-looking HTML in previews stays text', async () => {
  const dom = await page();
  try {
    const payload = '<img src=x onerror="window.pwned=true"><script>window.pwned=true</script>';
    dom.window.fetch = async () => new Response(payload);
    dom.window.document.querySelector('#artifacts button').click();
    await waitFor(() => dom.window.document.getElementById('preview-text').textContent === payload);
    assert.equal(dom.window.document.getElementById('preview-text').textContent, payload);
    assert.equal(dom.window.document.querySelector('#preview-text img'), null);
    assert.equal(dom.window.pwned, undefined);
  } finally { dom.window.close(); }
});
test('lost polling connection offers retry without claiming completion', async () => {
  const dom = await page(); const d = dom.window.document;
  try {
    const realFetch = dom.window.fetch;
    dom.window.fetch = async () => { throw new Error('Mất kết nối'); };
    d.getElementById('history').dispatchEvent(new dom.window.Event('change'));
    await waitFor(() => !d.getElementById('retry').hidden);
    assert.equal(d.getElementById('retry').hidden, false);
    assert.match(d.getElementById('run-message').textContent, /Mất kết nối/);
    assert.equal(d.getElementById('status').textContent, 'Mất kết nối');
    dom.window.fetch = realFetch;
    d.getElementById('retry').click();
    await waitFor(() => d.getElementById('status').textContent === 'Đã xuất kết quả');
  } finally { dom.window.close(); }
});
