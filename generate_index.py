#!/usr/bin/env python3
"""
Generate index.html for PDF files in the output directory.
This script creates an HTML page with a PDF upload interface and translated PDF listing.
"""

import os
import re
import subprocess
from pathlib import Path
from html import escape
from datetime import datetime, timezone


def get_repo_info():
    """Detect GitHub repository owner and name."""
    # GitHub Actions sets GITHUB_REPOSITORY as "owner/repo"
    github_repo = os.environ.get('GITHUB_REPOSITORY', '')
    if github_repo and '/' in github_repo:
        owner, repo = github_repo.split('/', 1)
        return owner, repo.rstrip('.git')

    # Fallback: parse from git remote URL
    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True, text=True, check=True,
        )
        url = result.stdout.strip()
        match = re.search(r'github\.com[:/]([^/]+)/([^/.]+)', url)
        if match:
            return match.group(1), match.group(2).rstrip('.git')
    except Exception:
        pass

    return '', ''


def _pdf_items_html(pdf_files):
    """Return the HTML snippet for the translated-PDF card list."""
    if not pdf_files:
        return """
        <div class="empty-state">
            <div class="empty-icon">📭</div>
            <p>尚無翻譯結果</p>
            <small>上傳 PDF 後，GitHub Actions 將自動翻譯並在此顯示結果（約需 2–10 分鐘）</small>
        </div>"""

    items = []
    for pdf_file in pdf_files:
        filename = escape(pdf_file.name)
        size_bytes = pdf_file.stat().st_size
        if size_bytes < 1024:
            size_str = f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.1f} KB"
        else:
            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
        mtime = datetime.fromtimestamp(pdf_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        items.append(f"""
        <div class="pdf-card">
            <div class="pdf-icon">📕</div>
            <div class="pdf-info">
                <div class="pdf-name" title="{filename}">{filename}</div>
                <div class="pdf-meta">{size_str} &bull; {mtime}</div>
            </div>
            <a href="{filename}" class="btn btn-view" target="_blank">👁 預覽</a>
            <a href="{filename}" class="btn btn-download" download>⬇ 下載</a>
        </div>""")
    return '\n'.join(items)


def _build_html(owner, repo, update_time, file_count, pdf_items):
    """Return the full HTML string for index.html."""
    actions_url = f"https://github.com/{owner}/{repo}/actions" if owner and repo else "#"
    token_url = "https://github.com/settings/tokens"

    # JavaScript uses {{ }} for literal braces inside f-string
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="PDF2zh - 線上 PDF 翻譯工具">
  <title>PDF2zh 翻譯器</title>
  <style>
    *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}

    :root {{
      --primary: #6366f1;
      --primary-dk: #4f46e5;
      --success: #10b981;
      --danger: #ef4444;
      --warn: #f59e0b;
      --bg: #0f172a;
      --surface: #1e293b;
      --surface2: #334155;
      --text: #f1f5f9;
      --muted: #94a3b8;
      --border: #475569;
      --radius: 12px;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      padding: 20px;
    }}

    a {{ color: inherit; }}

    .container {{ max-width: 820px; margin: 0 auto; }}

    /* ── Header ── */
    .header {{ text-align: center; padding: 40px 0 28px; }}
    .header h1 {{
      font-size: 2.2em;
      background: linear-gradient(135deg, var(--primary), #ec4899);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 8px;
    }}
    .header p {{ color: var(--muted); }}

    /* ── Card ── */
    .card {{
      background: var(--surface);
      border-radius: var(--radius);
      padding: 24px;
      margin-bottom: 20px;
      border: 1px solid var(--border);
    }}
    .card-title {{
      font-size: 1.05em;
      font-weight: 600;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .section-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }}
    .badge {{
      background: var(--primary);
      color: #fff;
      border-radius: 20px;
      padding: 2px 10px;
      font-size: 0.8em;
    }}

    /* ── Warning banner ── */
    .banner {{
      background: rgba(245,158,11,.1);
      border: 1px solid rgba(245,158,11,.3);
      color: #fcd34d;
      padding: 10px 16px;
      border-radius: 8px;
      font-size: 0.85em;
      margin-bottom: 16px;
    }}

    /* ── Settings toggle ── */
    .settings-toggle {{
      background: none;
      border: 1px solid var(--border);
      color: var(--muted);
      padding: 7px 14px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.85em;
      margin-bottom: 12px;
    }}
    .settings-panel {{
      display: none;
      background: var(--surface2);
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 16px;
    }}
    .settings-panel.open {{ display: block; }}

    /* ── Form ── */
    .form-group {{ margin-bottom: 12px; }}
    .form-group label {{
      display: block;
      font-size: 0.82em;
      color: var(--muted);
      margin-bottom: 5px;
    }}
    .form-group input {{
      width: 100%;
      background: var(--bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 0.9em;
    }}
    .form-group input:focus {{ outline: none; border-color: var(--primary); }}

    /* ── Drop zone ── */
    .dropzone {{
      border: 2px dashed var(--border);
      border-radius: var(--radius);
      padding: 40px 20px;
      text-align: center;
      cursor: pointer;
      transition: border-color .2s, background .2s;
      position: relative;
    }}
    .dropzone:hover, .dropzone.dragover {{
      border-color: var(--primary);
      background: rgba(99,102,241,.05);
    }}
    .dropzone input[type="file"] {{
      position: absolute;
      inset: 0;
      opacity: 0;
      cursor: pointer;
      width: 100%;
      height: 100%;
    }}
    .dz-icon {{ font-size: 2.5em; margin-bottom: 10px; }}
    .dz-text {{ color: var(--muted); font-size: 0.95em; }}
    .dz-text strong {{ color: var(--text); }}

    /* ── File list ── */
    .file-list {{ margin-top: 14px; }}
    .file-item {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 14px;
      background: var(--surface2);
      border-radius: 8px;
      margin-bottom: 8px;
    }}
    .fi-name {{
      flex: 1;
      font-size: 0.9em;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .fi-size {{ font-size: 0.8em; color: var(--muted); white-space: nowrap; }}
    .fi-status {{ font-size: 0.85em; white-space: nowrap; }}
    .fi-remove {{
      background: none;
      border: none;
      color: var(--danger);
      cursor: pointer;
      font-size: 1.1em;
      padding: 2px 6px;
      line-height: 1;
    }}

    /* ── Buttons ── */
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 9px 18px;
      border-radius: 8px;
      font-size: 0.88em;
      font-weight: 500;
      cursor: pointer;
      border: none;
      text-decoration: none;
      transition: background .2s, transform .15s;
      white-space: nowrap;
    }}
    .btn-primary {{ background: var(--primary); color: #fff; }}
    .btn-primary:hover:not(:disabled) {{ background: var(--primary-dk); }}
    .btn-primary:disabled {{ opacity: .45; cursor: not-allowed; }}
    .btn-ghost {{ background: var(--surface2); color: var(--text); }}
    .btn-ghost:hover {{ background: var(--border); }}
    .btn-download {{ background: var(--primary); color: #fff; font-size: 0.8em; padding: 6px 12px; }}
    .btn-view {{ background: var(--surface2); color: var(--text); font-size: 0.8em; padding: 6px 12px; }}

    /* ── Status messages ── */
    .status-msg {{
      padding: 12px 16px;
      border-radius: 8px;
      margin-top: 14px;
      font-size: 0.9em;
      line-height: 1.6;
    }}
    .status-success {{ background: rgba(16,185,129,.1); border: 1px solid rgba(16,185,129,.3); color: #34d399; }}
    .status-error   {{ background: rgba(239,68,68,.1);  border: 1px solid rgba(239,68,68,.3);  color: #fc8181; }}
    .status-info    {{ background: rgba(99,102,241,.1); border: 1px solid rgba(99,102,241,.3); color: #a5b4fc; }}

    /* ── How-it-works ── */
    .steps {{ padding-left: 20px; line-height: 2.1; color: var(--muted); font-size: 0.92em; }}
    .steps a {{ color: var(--primary); text-decoration: none; }}

    /* ── PDF result cards ── */
    .pdf-card {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 13px 15px;
      background: var(--surface2);
      border-radius: 10px;
      margin-bottom: 10px;
      transition: background .2s;
    }}
    .pdf-card:hover {{ background: #3d526b; }}
    .pdf-icon {{ font-size: 1.4em; flex-shrink: 0; }}
    .pdf-info {{ flex: 1; min-width: 0; }}
    .pdf-name {{ font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .pdf-meta {{ font-size: 0.78em; color: var(--muted); margin-top: 2px; }}

    /* ── Empty state ── */
    .empty-state {{ text-align: center; padding: 36px 20px; color: var(--muted); }}
    .empty-icon {{ font-size: 2.8em; margin-bottom: 10px; }}
    .empty-state small {{ display: block; margin-top: 6px; font-size: 0.85em; }}

    /* ── Footer ── */
    .footer {{ text-align: center; color: var(--muted); font-size: 0.8em; padding: 20px 0 10px; }}
    .footer a {{ color: var(--primary); text-decoration: none; }}

    /* ── Responsive ── */
    @media (max-width: 600px) {{
      .header h1 {{ font-size: 1.7em; }}
      .pdf-card {{ flex-wrap: wrap; }}
      .section-header {{ flex-wrap: wrap; gap: 8px; }}
    }}
  </style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>🔄 PDF2zh 翻譯器</h1>
    <p>上傳 PDF，透過 GitHub Actions 自動翻譯成中文</p>
  </div>

  <!-- ═══ Upload card ═══ -->
  <div class="card">
    <div class="card-title">📤 上傳 PDF 進行翻譯</div>

    <div class="banner">
      ⚠️ 需要擁有 <strong>repo</strong> 權限（或 fine-grained token 中的
      <strong>Contents: Write</strong>）的 GitHub Personal Access Token。
      Token 僅存在您的瀏覽器 localStorage 中，不會傳送到任何第三方。
    </div>

    <button class="settings-toggle" onclick="toggleSettings()">⚙️ 設定 GitHub Token</button>

    <div class="settings-panel" id="settings-panel">
      <div class="form-group">
        <label>GitHub Personal Access Token</label>
        <input type="password" id="github-token"
               placeholder="ghp_xxxxxxxxxxxxxxxxxxxx"
               oninput="saveToken(this.value)">
      </div>
      <div style="font-size:0.8em;color:var(--muted)">
        前往
        <a href="{token_url}" target="_blank" style="color:var(--primary)">
          GitHub → Settings → Developer settings → Personal access tokens
        </a>
        建立 Token，勾選 <strong>repo</strong> 範圍（或 fine-grained：Contents Write）。
      </div>
    </div>

    <div class="dropzone" id="dropzone">
      <input type="file" id="file-input" accept=".pdf" multiple
             onchange="handleFileInput(this.files)">
      <div class="dz-icon">📄</div>
      <div class="dz-text">
        <strong>拖曳 PDF 到這裡</strong>，或點擊選擇檔案<br>
        <small style="margin-top:6px;display:block;">支援多個 PDF 同時上傳，每個最大 50&nbsp;MB</small>
      </div>
    </div>

    <div class="file-list" id="file-list"></div>

    <div style="margin-top:16px;display:flex;gap:12px;flex-wrap:wrap;">
      <button class="btn btn-primary" id="upload-btn" onclick="startUpload()" disabled>
        🚀 上傳並翻譯
      </button>
      <button class="btn btn-ghost" onclick="clearFiles()">🗑 清除</button>
    </div>

    <div id="upload-status"></div>
  </div>

  <!-- ═══ How it works ═══ -->
  <div class="card">
    <div class="card-title">💡 使用流程</div>
    <ol class="steps">
      <li>點擊「設定 GitHub Token」輸入您的 PAT（只需設定一次）</li>
      <li>選擇要翻譯的 PDF 檔案</li>
      <li>點擊「上傳並翻譯」— 檔案會上傳到 GitHub 倉庫的 <code>input/</code> 資料夾</li>
      <li>GitHub Actions 自動開始翻譯（約 2–10 分鐘）</li>
      <li>翻譯完成後，重新整理本頁，在下方「翻譯結果」區下載</li>
    </ol>
    <div style="margin-top:12px">
      <a href="{actions_url}" target="_blank" style="color:var(--primary);font-size:0.9em">
        📊 查看 GitHub Actions 翻譯進度 →
      </a>
    </div>
  </div>

  <!-- ═══ Results card ═══ -->
  <div class="card">
    <div class="section-header">
      <div class="card-title" style="margin-bottom:0">
        📥 翻譯結果 <span class="badge">{file_count} 個</span>
      </div>
      <button class="btn btn-ghost" style="font-size:0.82em" onclick="location.reload()">
        🔄 重新整理
      </button>
    </div>
    {pdf_items}
  </div>

  <div class="footer">
    <p>最後更新：{update_time} &bull;
       由 <a href="https://github.com/Byaidu/PDFMathTranslate" target="_blank">PDFMathTranslate</a> 提供翻譯核心
    </p>
  </div>

</div><!-- /container -->

<script>
// ── Repo detection ────────────────────────────────────────────────────────────
function getRepoInfo() {{
  const hostname = window.location.hostname;
  const pathname = window.location.pathname;
  const m = hostname.match(/^(.+)\\.github\\.io$/);
  if (m) {{
    const owner = m[1];
    const parts = pathname.split('/').filter(Boolean);
    return {{ owner, repo: parts[0] || '' }};
  }}
  // Fallback: values baked in at build time
  return {{ owner: '{owner}', repo: '{repo}' }};
}}

// ── Token persistence ─────────────────────────────────────────────────────────
function saveToken(v) {{
  if (v) localStorage.setItem('gh_token', v);
  else   localStorage.removeItem('gh_token');
}}

function toggleSettings() {{
  document.getElementById('settings-panel').classList.toggle('open');
}}

window.addEventListener('DOMContentLoaded', () => {{
  const t = localStorage.getItem('gh_token');
  if (t) document.getElementById('github-token').value = t;
  setupDrop();
}});

// ── Drag-and-drop ─────────────────────────────────────────────────────────────
function setupDrop() {{
  const dz = document.getElementById('dropzone');
  dz.addEventListener('dragover',  e => {{ e.preventDefault(); dz.classList.add('dragover'); }});
  dz.addEventListener('dragleave', ()  => dz.classList.remove('dragover'));
  dz.addEventListener('drop', e => {{
    e.preventDefault();
    dz.classList.remove('dragover');
    handleFileInput(e.dataTransfer.files);
  }});
}}

function handleFileInput(fileList) {{
  for (const file of fileList) {{
    if (!file.name.toLowerCase().endsWith('.pdf')) {{
      showStatus(`❌ "${{esc(file.name)}}" 不是 PDF 檔案`, 'error'); continue;
    }}
    if (file.size > 50 * 1024 * 1024) {{
      showStatus(`❌ "${{esc(file.name)}}" 超過 50 MB 限制`, 'error'); continue;
    }}
    if (!selectedFiles.find(f => f.name === file.name)) selectedFiles.push(file);
  }}
  renderFileList();
  updateBtn();
}}

// ── File list state ───────────────────────────────────────────────────────────
let selectedFiles = [];

function renderFileList() {{
  const el = document.getElementById('file-list');
  if (!selectedFiles.length) {{ el.innerHTML = ''; return; }}
  el.innerHTML = selectedFiles.map((f, i) => `
    <div class="file-item" id="fi-${{i}}">
      <span>📄</span>
      <span class="fi-name" title="${{esc(f.name)}}">${{esc(f.name)}}</span>
      <span class="fi-size">${{fmtSize(f.size)}}</span>
      <span class="fi-status" id="fis-${{i}}"></span>
      <button class="fi-remove" onclick="removeFile(${{i}})">✕</button>
    </div>`).join('');
}}

function removeFile(i) {{
  selectedFiles.splice(i, 1);
  renderFileList();
  updateBtn();
}}

function clearFiles() {{
  selectedFiles = [];
  renderFileList();
  updateBtn();
  document.getElementById('upload-status').innerHTML = '';
  document.getElementById('file-input').value = '';
}}

function updateBtn() {{
  document.getElementById('upload-btn').disabled = selectedFiles.length === 0;
}}

// ── Upload ────────────────────────────────────────────────────────────────────
async function startUpload() {{
  const token = document.getElementById('github-token').value.trim();
  if (!token) {{
    document.getElementById('settings-panel').classList.add('open');
    showStatus('❌ 請先設定 GitHub Personal Access Token', 'error');
    return;
  }}

  const {{ owner, repo }} = getRepoInfo();
  if (!owner || !repo) {{
    showStatus('❌ 無法識別 GitHub 倉庫資訊，請確認頁面 URL', 'error');
    return;
  }}

  const btn = document.getElementById('upload-btn');
  btn.disabled = true;
  btn.textContent = '⏳ 上傳中…';
  showStatus('⏳ 正在上傳檔案，請稍候…', 'info');

  let ok = 0, errs = [];

  for (let i = 0; i < selectedFiles.length; i++) {{
    try {{
      await uploadOne(selectedFiles[i], token, owner, repo, i);
      ok++;
    }} catch (e) {{
      errs.push(`${{esc(selectedFiles[i].name)}}: ${{esc(e.message)}}`);
    }}
  }}

  btn.textContent = '🚀 上傳並翻譯';
  updateBtn();

  if (ok === selectedFiles.length) {{
    showStatus(
      `✅ 成功上傳 ${{ok}} 個檔案！<br>` +
      `GitHub Actions 已自動開始翻譯，請稍候 2–10 分鐘後重新整理本頁。<br>` +
      `<a href="${{actionsUrl(owner,repo)}}" target="_blank" style="color:var(--primary)">` +
      `📊 查看翻譯進度 →</a>`,
      'success'
    );
  }} else if (ok > 0) {{
    showStatus(
      `⚠️ 部分成功：${{ok}}/${{selectedFiles.length}} 個檔案已上傳。<br>失敗：${{errs.join('<br>')}}`,
      'error'
    );
  }} else {{
    showStatus(`❌ 上傳失敗：<br>${{errs.join('<br>')}}`, 'error');
  }}
}}

async function uploadOne(file, token, owner, repo, idx) {{
  setFiStatus(idx, '⏳ 讀取中…');
  let b64;
  try {{
    b64 = await toBase64(file);
  }} catch (e) {{
    setFiStatus(idx, '❌ 讀取失敗');
    throw new Error('無法讀取檔案');
  }}

  setFiStatus(idx, '⏳ 上傳中…');

  const url = `https://api.github.com/repos/${{owner}}/${{repo}}/contents/input/${{encodeURIComponent(file.name)}}`;
  const headers = {{
    'Authorization': `Bearer ${{token}}`,
    'Accept': 'application/vnd.github+json',
    'Content-Type': 'application/json',
    'X-GitHub-Api-Version': '2022-11-28',
  }};

  // Get existing SHA (needed to overwrite)
  let sha = null;
  try {{
    const r = await fetch(url, {{ headers }});
    if (r.ok) sha = (await r.json()).sha;
  }} catch (_) {{}}

  const body = {{ message: `翻譯請求: ${{file.name}}`, content: b64 }};
  if (sha) body.sha = sha;

  const resp = await fetch(url, {{ method: 'PUT', headers, body: JSON.stringify(body) }});

  if (!resp.ok) {{
    let msg = '上傳失敗';
    try {{ msg = (await resp.json()).message || msg; }} catch (_) {{}}
    if (resp.status === 401) msg = 'Token 無效或已過期，請重新設定';
    if (resp.status === 403) msg = '權限不足，請確認 Token 有 repo（或 Contents: Write）權限';
    setFiStatus(idx, '❌ 失敗');
    throw new Error(msg);
  }}

  setFiStatus(idx, '✅ 完成');
}}

// ── Helpers ───────────────────────────────────────────────────────────────────
function toBase64(file) {{
  return new Promise((res, rej) => {{
    const r = new FileReader();
    r.onload  = () => res(r.result.split(',')[1]);
    r.onerror = rej;
    r.readAsDataURL(file);
  }});
}}

function setFiStatus(i, html) {{
  const el = document.getElementById(`fis-${{i}}`);
  if (el) el.innerHTML = html;
}}

function showStatus(html, type) {{
  document.getElementById('upload-status').innerHTML =
    `<div class="status-msg status-${{type}}">${{html}}</div>`;
}}

function actionsUrl(owner, repo) {{
  return `https://github.com/${{owner}}/${{repo}}/actions`;
}}

function fmtSize(b) {{
  if (b < 1024) return b + ' B';
  if (b < 1048576) return (b/1024).toFixed(1) + ' KB';
  return (b/1048576).toFixed(1) + ' MB';
}}

function esc(s) {{
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}}
</script>
</body>
</html>"""


def generate_index():
    """Generate index.html file listing all PDFs in output directory."""
    output_dir = Path('output')
    output_dir.mkdir(parents=True, exist_ok=True)

    # PDF files, newest first
    pdf_files = sorted(
        (f for f in output_dir.glob('*.pdf') if f.is_file()),
        key=lambda x: x.stat().st_mtime,
        reverse=True,
    )

    owner, repo = get_repo_info()
    update_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    file_count = len(pdf_files)

    html = _build_html(owner, repo, update_time, file_count, _pdf_items_html(pdf_files))

    index_path = output_dir / 'index.html'
    index_path.write_text(html, encoding='utf-8')

    print(f"✅ 已生成 index.html - 包含 {file_count} 個 PDF 檔案 (owner={owner}, repo={repo})")
    if pdf_files:
        print("\n📋 包含的檔案:")
        for f in pdf_files:
            print(f"  - {f.name}")


if __name__ == '__main__':
    try:
        generate_index()
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        exit(1)
