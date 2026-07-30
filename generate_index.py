#!/usr/bin/env python3
"""
Generate index.html for PDF files in the output directory.
This script creates a simple HTML page listing all translated PDFs for GitHub Pages.
"""

import os
from pathlib import Path
from html import escape
from datetime import datetime


def generate_index():
    """Generate index.html file listing all PDFs in output directory."""
    output_dir = Path('output')
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all PDF files sorted by name
    pdf_files = sorted(output_dir.glob('*.pdf'))
    
    # Remove index.html from the list (if it exists)
    pdf_files = [f for f in pdf_files if f.name != 'index.html']
    
    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="PDF 翻譯結果 - PDF2zh 自動翻譯系統">
    <title>PDF 翻譯結果</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
            padding: 40px 0;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            padding: 40px;
        }}
        
        .info-box {{
            background-color: #f0f4ff;
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 30px;
            color: #333;
        }}

        .upload-card {{
            background-color: #f7f9ff;
            border: 1px solid #e1e6ff;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
        }}

        .upload-card h2 {{
            font-size: 1.2em;
            color: #333;
            margin-bottom: 8px;
        }}

        .upload-form {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 12px;
        }}

        .upload-field {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .upload-field label {{
            font-size: 0.9em;
            color: #555;
        }}

        .upload-field input {{
            padding: 10px;
            border: 1px solid #d7dce8;
            border-radius: 6px;
            font-size: 0.95em;
        }}

        .upload-actions {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 12px;
        }}

        .upload-btn {{
            background-color: #667eea;
            color: white;
            padding: 10px 18px;
            border-radius: 6px;
            border: none;
            font-size: 0.95em;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .upload-btn:hover {{
            background-color: #764ba2;
            transform: translateY(-1px);
        }}

        .upload-status {{
            margin-top: 12px;
            padding: 10px 12px;
            border-radius: 6px;
            font-size: 0.95em;
            display: none;
        }}

        .upload-status.success {{
            background-color: #e8f5e9;
            color: #2e7d32;
        }}

        .upload-status.error {{
            background-color: #ffebee;
            color: #c62828;
        }}

        .upload-status.info {{
            background-color: #e3f2fd;
            color: #1565c0;
        }}

        .upload-note {{
            font-size: 0.9em;
            color: #666;
        }}

        .remember-token {{
            font-size: 0.9em;
            color: #555;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .pdf-list {{
            list-style: none;
        }}
        
        .pdf-item {{
            display: flex;
            align-items: center;
            padding: 15px;
            margin: 10px 0;
            background-color: #f9f9f9;
            border-left: 4px solid #667eea;
            border-radius: 6px;
            transition: all 0.3s ease;
        }}
        
        .pdf-item:hover {{
            background-color: #f0f4ff;
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
        }}
        
        .pdf-icon {{
            font-size: 1.5em;
            margin-right: 15px;
            color: #ff6b6b;
        }}
        
        .pdf-info {{
            flex: 1;
        }}
        
        .pdf-name {{
            color: #333;
            font-weight: bold;
            word-break: break-word;
        }}
        
        .pdf-link {{
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }}
        
        .pdf-link:hover {{
            color: #764ba2;
            text-decoration: underline;
        }}
        
        .download-btn {{
            display: inline-block;
            background-color: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            margin-left: 10px;
            transition: all 0.3s ease;
            white-space: nowrap;
        }}
        
        .download-btn:hover {{
            background-color: #764ba2;
            transform: scale(1.05);
        }}
        
        .empty-message {{
            text-align: center;
            color: #999;
            padding: 40px 20px;
            font-size: 1.1em;
        }}
        
        .empty-icon {{
            font-size: 3em;
            margin-bottom: 15px;
            opacity: 0.5;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .file-count {{
            display: inline-block;
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-left: 10px;
        }}
        
        @media (max-width: 600px) {{
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .download-btn {{
                display: block;
                margin: 10px 0 0 0;
                text-align: center;
            }}
            
            .pdf-item {{
                flex-direction: column;
                align-items: flex-start;
            }}
            
            .pdf-icon {{
                margin-bottom: 10px;
            }}

            .upload-form {{
                grid-template-columns: 1fr;
            }}

            .upload-actions {{
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📄 PDF 翻譯結果
                <span class="file-count">{len(pdf_files)} 個檔案</span>
            </h1>
            <p>由 PDFMathTranslate (pdf2zh) 自動翻譯至中文</p>
        </div>
        
        <div class="content">
            <div class="info-box">
                ℹ️ 這些 PDF 檔案已由 GitHub Actions 自動翻譯。點擊下方連結下載翻譯後的中文版本，或使用下方工具直接上傳新 PDF 觸發翻譯。
            </div>
            <div class="upload-card">
                <h2>📤 上傳 PDF 進行翻譯</h2>
                <div class="upload-note">上傳後會自動提交到 <code>input/</code> 並觸發翻譯工作流。</div>
                <div class="upload-form">
                    <div class="upload-field">
                        <label for="gh-repo">GitHub 倉庫 (owner/repo)</label>
                        <input id="gh-repo" type="text" placeholder="username/PDF2zh">
                    </div>
                    <div class="upload-field">
                        <label for="gh-branch">分支</label>
                        <input id="gh-branch" type="text" value="main">
                    </div>
                    <div class="upload-field">
                        <label for="gh-token">GitHub Token</label>
                        <input id="gh-token" type="password" placeholder="ghp_...">
                    </div>
                    <div class="upload-field">
                        <label for="pdf-file">PDF 檔案</label>
                        <input id="pdf-file" type="file" accept="application/pdf">
                    </div>
                </div>
                <div class="upload-actions">
                    <label class="remember-token">
                        <input type="checkbox" id="remember-token">記住 Token
                    </label>
                    <button id="upload-btn" class="upload-btn" type="button">上傳並翻譯</button>
                    <span id="file-info" class="upload-note"></span>
                </div>
                <div id="upload-status" class="upload-status" role="status" aria-live="polite"></div>
                <div class="upload-note">
                    需要具備「Contents: Read and write」權限的 Fine-grained token，或 classic <code>repo</code> 權限。
                    建議檔案大小不超過 100MB。
                </div>
            </div>
"""
    
    if pdf_files:
        html_content += '            <ul class="pdf-list">\n'
        for pdf_file in pdf_files:
            filename = escape(pdf_file.name)
            size_kb = pdf_file.stat().st_size / 1024
            size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"
            
            html_content += f"""                <li class="pdf-item">
                    <span class="pdf-icon">📕</span>
                    <div class="pdf-info">
                        <div class="pdf-name">{filename}</div>
                        <small style="color: #999;">大小: {size_str}</small>
                    </div>
                    <a href="{filename}" class="download-btn">下載</a>
                </li>
"""
        html_content += '            </ul>\n'
    else:
        html_content += """            <div class="empty-message">
                <div class="empty-icon">📭</div>
                <p>暫無翻譯結果</p>
                <p style="font-size: 0.9em; color: #bbb; margin-top: 10px;">
                    請上傳 PDF 到 input/ 資料夾並推送到 GitHub
                </p>
            </div>
"""
    
    html_content += f"""        </div>
        
        <div class="footer">
            <p>最後更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (UTC)</p>
            <p>🤖 由 <a href="https://github.com/bigbangbang0000/PDF2zh" style="color: white;">PDFMathTranslate</a> 提供</p>
        </div>
    </div>
    <script>
        (() => {{
            const repoInput = document.getElementById("gh-repo");
            const branchInput = document.getElementById("gh-branch");
            const tokenInput = document.getElementById("gh-token");
            const fileInput = document.getElementById("pdf-file");
            const rememberToken = document.getElementById("remember-token");
            const uploadBtn = document.getElementById("upload-btn");
            const statusEl = document.getElementById("upload-status");
            const fileInfoEl = document.getElementById("file-info");

            const detectRepo = () => {{
                const host = window.location.hostname;
                if (host.endsWith("github.io")) {{
                    const owner = host.split(".")[0];
                    const pathParts = window.location.pathname.split("/").filter(Boolean);
                    const repo = pathParts[0];
                    if (owner && repo) {{
                        return `${{owner}}/${{repo}}`;
                    }}
                }}
                return "";
            }};

            const savedToken = localStorage.getItem("pdf2zh_token");
            if (savedToken) {{
                tokenInput.value = savedToken;
                rememberToken.checked = true;
            }}

            const detectedRepo = detectRepo();
            if (detectedRepo && !repoInput.value) {{
                repoInput.value = detectedRepo;
            }}

            const setStatus = (type, message) => {{
                statusEl.className = `upload-status ${{type}}`;
                statusEl.textContent = message;
                statusEl.style.display = "block";
            }};

            const clearStatus = () => {{
                statusEl.style.display = "none";
                statusEl.textContent = "";
            }};

            const formatBytes = (bytes) => {{
                if (!bytes && bytes !== 0) return "";
                const units = ["B", "KB", "MB", "GB"];
                let size = bytes;
                let unitIndex = 0;
                while (size >= 1024 && unitIndex < units.length - 1) {{
                    size /= 1024;
                    unitIndex += 1;
                }}
                return `${{size.toFixed(1)}} ${{units[unitIndex]}}`;
            }};

            fileInput.addEventListener("change", () => {{
                clearStatus();
                const file = fileInput.files[0];
                if (!file) {{
                    fileInfoEl.textContent = "";
                    return;
                }}
                fileInfoEl.textContent = `${{file.name}} · ${{formatBytes(file.size)}}`;
            }});

            rememberToken.addEventListener("change", () => {{
                if (!rememberToken.checked) {{
                    localStorage.removeItem("pdf2zh_token");
                }}
            }});

            const apiRequest = async (url, options = {{}}) => {{
                const token = tokenInput.value.trim();
                const headers = options.headers || {{}};
                headers.Authorization = `token ${{token}}`;
                headers.Accept = "application/vnd.github+json";
                return fetch(url, {{
                    ...options,
                    headers,
                }});
            }};

            const arrayBufferToBase64 = (buffer) => {{
                let binary = "";
                const bytes = new Uint8Array(buffer);
                const chunkSize = 0x8000;
                for (let i = 0; i < bytes.length; i += chunkSize) {{
                    binary += String.fromCharCode.apply(
                        null,
                        bytes.subarray(i, i + chunkSize),
                    );
                }}
                return btoa(binary);
            }};

            const validateInputs = () => {{
                const repo = repoInput.value.trim();
                const token = tokenInput.value.trim();
                const file = fileInput.files[0];
                if (!repo || !repo.includes("/")) {{
                    setStatus("error", "請填寫正確的倉庫格式（owner/repo）。");
                    return false;
                }}
                if (!token) {{
                    setStatus("error", "請提供 GitHub Token。");
                    return false;
                }}
                if (!file) {{
                    setStatus("error", "請選擇要上傳的 PDF。");
                    return false;
                }}
                if (!file.name.toLowerCase().endsWith(".pdf")) {{
                    setStatus("error", "僅支援 PDF 檔案。");
                    return false;
                }}
                if (file.size > 100 * 1024 * 1024) {{
                    setStatus("error", "檔案大小超過 100MB，請改用 git push。");
                    return false;
                }}
                return true;
            }};

            uploadBtn.addEventListener("click", async () => {{
                if (!validateInputs()) {{
                    return;
                }}

                const repo = repoInput.value.trim();
                const [owner, repoName] = repo.split("/");
                const branch = branchInput.value.trim() || "main";
                const token = tokenInput.value.trim();
                const file = fileInput.files[0];
                const safeName = file.name.replace(/[\\/]/g, "_");
                const commitMessage = `Upload ${{safeName}} for translation`;

                if (rememberToken.checked) {{
                    localStorage.setItem("pdf2zh_token", token);
                }}

                try {{
                    setStatus("info", "正在讀取檔案並準備上傳...");
                    uploadBtn.disabled = true;

                    const buffer = await file.arrayBuffer();
                    const contentBase64 = arrayBufferToBase64(buffer);

                    setStatus("info", "正在建立 Git 物件...");
                    const refResponse = await apiRequest(
                        `https://api.github.com/repos/${{owner}}/${{repoName}}/git/ref/heads/${{branch}}`,
                    );
                    if (!refResponse.ok) {{
                        throw new Error("無法取得分支資訊，請檢查倉庫與分支名稱。");
                    }}
                    const refData = await refResponse.json();
                    const baseCommitSha = refData.object.sha;

                    const commitResponse = await apiRequest(
                        `https://api.github.com/repos/${{owner}}/${{repoName}}/git/commits/${{baseCommitSha}}`,
                    );
                    if (!commitResponse.ok) {{
                        throw new Error("無法取得最新 commit 資訊。");
                    }}
                    const commitData = await commitResponse.json();

                    const blobResponse = await apiRequest(
                        `https://api.github.com/repos/${{owner}}/${{repoName}}/git/blobs`,
                        {{
                            method: "POST",
                            body: JSON.stringify({{
                                content: contentBase64,
                                encoding: "base64",
                            }}),
                        }},
                    );
                    if (!blobResponse.ok) {{
                        throw new Error("建立檔案內容失敗，請確認 token 權限。");
                    }}
                    const blobData = await blobResponse.json();

                    const treeResponse = await apiRequest(
                        `https://api.github.com/repos/${{owner}}/${{repoName}}/git/trees`,
                        {{
                            method: "POST",
                            body: JSON.stringify({{
                                base_tree: commitData.tree.sha,
                                tree: [
                                    {{
                                        path: `input/${{safeName}}`,
                                        mode: "100644",
                                        type: "blob",
                                        sha: blobData.sha,
                                    }},
                                ],
                            }}),
                        }},
                    );
                    if (!treeResponse.ok) {{
                        throw new Error("建立 Git tree 失敗。");
                    }}
                    const treeData = await treeResponse.json();

                    const newCommitResponse = await apiRequest(
                        `https://api.github.com/repos/${{owner}}/${{repoName}}/git/commits`,
                        {{
                            method: "POST",
                            body: JSON.stringify({{
                                message: commitMessage,
                                tree: treeData.sha,
                                parents: [baseCommitSha],
                            }}),
                        }},
                    );
                    if (!newCommitResponse.ok) {{
                        throw new Error("建立 commit 失敗。");
                    }}
                    const newCommitData = await newCommitResponse.json();

                    const updateRefResponse = await apiRequest(
                        `https://api.github.com/repos/${{owner}}/${{repoName}}/git/refs/heads/${{branch}}`,
                        {{
                            method: "PATCH",
                            body: JSON.stringify({{
                                sha: newCommitData.sha,
                            }}),
                        }},
                    );
                    if (!updateRefResponse.ok) {{
                        throw new Error("更新分支失敗。");
                    }}

                    setStatus(
                        "success",
                        `✅ 上傳成功！已提交 ${{safeName}}，請稍後前往 Actions 查看翻譯進度。`,
                    );
                }} catch (error) {{
                    setStatus("error", `❌ 上傳失敗：${{error.message || error}}`);
                }} finally {{
                    uploadBtn.disabled = false;
                }}
            }});
        }})();
    </script>
</body>
</html>"""
    
    # Write index.html
    index_path = output_dir / 'index.html'
    index_path.write_text(html_content, encoding='utf-8')
    
    print(f"✅ 已生成 index.html - 包含 {len(pdf_files)} 個 PDF 檔案")
    if pdf_files:
        print("\n📋 包含的檔案:")
        for pdf_file in pdf_files:
            print(f"  - {pdf_file.name}")


if __name__ == '__main__':
    try:
        generate_index()
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        exit(1)
