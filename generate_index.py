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
                ℹ️ 這些 PDF 檔案已由 GitHub Actions 自動翻譯。點擊下方連結下載翻譯後的中文版本。
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
            <p>🤖 由 <a href="https://github.com/jimmymochi/PDF2zh" style="color: white;">PDFMathTranslate</a> 提供</p>
        </div>
    </div>
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
