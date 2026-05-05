# PDF2zh - PDFMathTranslate

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/jimmymochi/PDF2zh/translate_pdf.yml?style=flat-square)
![Python Version](https://img.shields.io/badge/python-3.10+-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![GitHub Pages](https://img.shields.io/badge/pages-live-success?style=flat-square)

**PDF2zh** 是一個基於 **PDFMathTranslate** 的自動化 PDF 翻譯系統，支援利用 GitHub Actions 自動將 PDF 檔案翻譯為中文，並在 GitHub Pages 上發布翻譯結果。

📖 [完整文檔](./WORKFLOW_README.md) | 🚀 [GitHub Pages](https://jimmymochi.github.io/PDF2zh/) | 📦 [PDFMathTranslate](https://github.com/Byaidu/PDFMathTranslate)

---

## ✨ 主要特性

- 🤖 **自動化翻譯** - GitHub Actions 自動監測並翻譯新上傳的 PDF
- 🌐 **多語言支持** - 支援 Google、DeepL、Azure 等多個翻譯引擎
- 💰 **免費方案** - 預設使用免費的 Google 翻譯引擎，無需 API Key
- 📱 **響應式設計** - 生成的索引頁面支援桌面、平板、手機瀏覽
- 📊 **批量處理** - 一次可翻譯多個 PDF 檔案
- 🔄 **增量更新** - 保留已翻譯檔案，僅翻譯新上傳的文檔
- 📥 **一鍵下載** - GitHub Pages 上直接下載翻譯後的 PDF

---

## 📦 系統需求

| 項目 | 要求 |
|------|------|
| **Python** | 3.10+ |
| **作業系統** | Ubuntu (GitHub Actions 環境) / Windows / macOS (本地使用) |
| **Git** | 2.0+ |
| **網路連接** | 需要連接互聯網（用於翻譯服務） |

---

## 🚀 快速開始

### 1. 本地安裝

#### 使用 pip 安裝：

```bash
# 安裝 pdf2zh
pip install pdf2zh

# 驗證安裝
pdf2zh --version
```

#### 從源代碼安裝：

```bash
git clone https://github.com/jimmymochi/PDF2zh.git
cd PDF2zh
pip install -e .
```

### 2. 本地使用

#### 基本用法：

```bash
# 使用 Google 翻譯（免費，推薦）
pdf2zh input.pdf -o output/ -e google

# 或指定輸出檔名
pdf2zh input.pdf -o output/translated.pdf -e google
```

#### 完整參數說明：

```bash
pdf2zh [OPTIONS] PDF_FILE

Options:
  -o, --output TEXT         輸出目錄或檔案路徑（預設：當前目錄）
  -e, --engine TEXT         翻譯引擎：google, deepl, azure, bing, openai
  -l, --language TEXT       目標語言（預設：zh，簡體中文）
  --zh-traditional          使用繁體中文（預設為簡體）
  -k, --api-key TEXT        API Key（某些引擎需要）
  -v, --verbose             詳細輸出
  --help                    顯示幫助信息
```

#### 翻譯引擎選項：

| 引擎 | 優點 | 缺點 | API Key 需求 |
|------|------|------|------------|
| **google** | 免費、快速、準確度高 | 需要網路連接 | ❌ 無 |
| **deepl** | 翻譯質量最佳 | 需要付費，有免費配額 | ✅ 是 |
| **azure** | 穩定可靠 | 需要付費 | ✅ 是 |
| **bing** | 微軟支持 | 功能有限 | ✅ 是 |
| **openai** | 最先進的翻譯 | 需要付費，較慢 | ✅ 是 |

#### 使用範例：

```bash
# 使用 Google 翻譯，輸出到指定目錄
pdf2zh research.pdf -o ./translated/ -e google

# 使用 DeepL 翻譯（需要 API Key）
pdf2zh thesis.pdf -o output.pdf -e deepl -k your_deepl_api_key

# 繁體中文翻譯
pdf2zh document.pdf -o output/ -e google --zh-traditional

# 詳細輸出
pdf2zh paper.pdf -o output/ -e google -v
```

---

## 🔧 GitHub Actions 自動化工作流

### 工作流說明

本倉庫包含自動化的 GitHub Actions 工作流，可自動翻譯上傳的 PDF：

**工作流檔案**: `.github/workflows/translate_pdf.yml`

### 使用方法

#### Step 1: 上傳 PDF 到 input 資料夾

```bash
# 克隆倉庫
git clone https://github.com/jimmymochi/PDF2zh.git
cd PDF2zh

# 將待翻譯的 PDF 複製到 input 資料夾
cp ~/Documents/my_paper.pdf input/
cp ~/Documents/another_doc.pdf input/

# 查看 input 資料夾內容
ls input/
# my_paper.pdf
# another_doc.pdf
```

#### Step 2: 推送到 GitHub

```bash
# 查看變更
git status

# 添加檔案
git add input/

# 提交
git commit -m "Add PDFs for translation"

# 推送到遠端倉庫
git push origin main
```

#### Step 3: 自動翻譯（無需任何操作）

GitHub Actions 將自動：
1. ✅ 檢測 `input/` 資料夾的變更
2. ✅ 在 Ubuntu 環境中運行工作流
3. ✅ 安裝 pdf2zh 及依賴
4. ✅ 批量翻譯所有 PDF 檔案
5. ✅ 將翻譯結果存入 `output/` 資料夾
6. ✅ 生成美觀的 index.html
7. ✅ 自動部署到 GitHub Pages

#### Step 4: 檢查翻譯進度

前往倉庫的 **Actions** 標籤：
- 查看工作流執行狀態
- 查看詳細日誌（如有錯誤）

```
https://github.com/jimmymochi/PDF2zh/actions
```

#### Step 5: 下載翻譯結果

翻譯完成後，訪問 GitHub Pages：

```
https://jimmymochi.github.io/PDF2zh/
```

頁面將顯示：
- 所有翻譯後的 PDF 檔案列表
- 檔案大小
- 下載連結
- 最後更新時間

---

## 📁 目錄結構

```
PDF2zh/
├── .github/
│   └── workflows/
│       └── translate_pdf.yml        # GitHub Actions 工作流配置
├── input/                           # 上傳待翻譯 PDF 的資料夾
│   └── .gitkeep
├── output/                          # 翻譯結果和索引頁面存放處
│   ├── .gitkeep
│   └── index.html                   # 自動生成的索引頁面
├── src/                             # pdf2zh 源代碼
├── generate_index.py                # 索引頁面生成腳本
├── README.md                        # 本檔案
├── WORKFLOW_README.md               # 工作流詳細說明
├── setup.py                         # Python 包配置
└── requirements.txt                 # 依賴列表
```

---

## ⚙️ 配置選項

### GitHub Actions 工作流配置

編輯 `.github/workflows/translate_pdf.yml` 修改以下設定：

#### 1. 更改翻譯引擎

```yaml
# 預設為 google，修改此行更改引擎
pdf2zh "$pdf_file" -o output/ -e google

# 可選值：deepl, azure, bing, openai
pdf2zh "$pdf_file" -o output/ -e deepl
```

#### 2. 使用 API Key

若使用付費引擎（如 DeepL），需在 GitHub 倉庫 Settings 中設定 Secrets：

1. 進入 **Settings** → **Secrets and variables** → **Actions**
2. 點擊 **New repository secret**
3. 名稱：`TRANSLATION_API_KEY`
4. 值：你的 API Key
5. 在工作流中使用：

```yaml
pdf2zh "$pdf_file" -o output/ -e deepl -k ${{ secrets.TRANSLATION_API_KEY }}
```

#### 3. 繁體中文輸出

編輯 `.github/workflows/translate_pdf.yml`：

```yaml
# 在翻譯命令中添加 --zh-traditional 參數
pdf2zh "$pdf_file" -o output/ -e google --zh-traditional
```

### 生成的索引頁面自定義

編輯 `generate_index.py` 中的 HTML/CSS 部分以自定義頁面外觀：

- 修改顏色主題：搜尋 `#667eea` 和 `#764ba2`
- 修改字體：編輯 `font-family` 值
- 修改佈局：編輯 CSS 類別定義

---

## 🐛 故障排查

### 問題 1: 工作流執行失敗

**症狀**: Actions 標籤顯示紅色 ❌

**解決方案**:
1. 點擊工作流檢查詳細日誌
2. 查看 "Translate PDFs" 步驟的錯誤信息
3. 常見原因：
   - PDF 檔案損壞或格式不支持
   - 網路連接問題
   - Google 翻譯服務臨時不可用

### 問題 2: GitHub Pages 頁面未更新

**症狀**: https://jimmymochi.github.io/PDF2zh/ 未顯示最新檔案

**解決方案**:
1. 確認 `gh-pages` 分支已創建：
   ```bash
   git branch -a | grep gh-pages
   ```
2. 進入 **Settings** → **Pages**，確認：
   - Source: `Deploy from a branch`
   - Branch: `gh-pages`, `/root` 目錄
3. 清除瀏覽器快取：`Ctrl+Shift+Del` (Windows) 或 `Cmd+Shift+Del` (Mac)

### 問題 3: 翻譯質量差

**症狀**: PDF 翻譯結果不準確或遺漏內容

**解決方案**:
1. 嘗試更換翻譯引擎（DeepL 通常質量最佳）
2. 確保 PDF 是文本型而非圖像型
3. 檢查 PDF 是否有密碼保護

### 問題 4: 本地運行出錯

**症狀**: `pdf2zh` 命令未找到或版本錯誤

**解決方案**:
```bash
# 驗證 Python 版本
python --version  # 應為 3.10+

# 重新安裝 pdf2zh
pip uninstall pdf2zh -y
pip install --upgrade pdf2zh

# 驗證安裝
pdf2zh --version
```

---

## 💡 高級用法

### 批量翻譯本地檔案

```bash
#!/bin/bash
# 創建 translate_all.sh

for pdf in input/*.pdf; do
    echo "正在翻譯: $pdf"
    pdf2zh "$pdf" -o output/ -e google
done

echo "全部翻譯完成！"
```

運行：
```bash
chmod +x translate_all.sh
./translate_all.sh
```

### 與其他工具集成

#### 轉換為其他格式

翻譯後轉換為 EPUB：
```bash
pdf2zh input.pdf -o temp/ -e google
# 使用其他工具轉換
pandoc temp/translated.pdf -o output.epub
```

#### 自動化分享

部署後自動發送通知：
```bash
# 在工作流中添加通知步驟
- name: Send Notification
  run: |
    echo "翻譯完成！訪問 https://jimmymochi.github.io/PDF2zh/"
```

---

## 📊 效能統計

典型執行時間（針對 100 頁 PDF）：

| 翻譯引擎 | 執行時間 | 品質評分 |
|--------|---------|---------|
| Google | 2-5 分鐘 | ⭐⭐⭐⭐ |
| DeepL | 3-7 分鐘 | ⭐⭐⭐⭐⭐ |
| Azure | 4-10 分鐘 | ⭐⭐⭐⭐ |
| OpenAI | 5-15 分鐘 | ⭐⭐⭐⭐⭐ |

*實際時間取決於 PDF 複雜度、檔案大小和網路速度*

---

## 🔐 隱私與安全

- 📤 上傳的 PDF 通過 GitHub 服務器進行翻譯，可能被暫時儲存
- 🔒 翻譯結果存儲在公開的 GitHub Pages（若倉庫為公開）
- 🛡️ 建議不要上傳包含機密信息的檔案
- ✅ 倉庫本身的 code 完全開源

---

## 📝 API 參考

### pdf2zh 命令行參數

```python
pdf2zh(
    input_path: str,           # 輸入 PDF 路徑
    output_path: str = None,   # 輸出路徑
    engine: str = "google",    # 翻譯引擎
    language: str = "zh",      # 目標語言代碼
    api_key: str = None,       # API Key
    preserve_layout: bool = True,  # 保留版面
    verbose: bool = False      # 詳細日誌
)
```

### Python 程序中使用

```python
from pdf2zh import translate

# 翻譯單個檔案
translate(
    input_path="input.pdf",
    output_path="output/",
    engine="google"
)

# 批量翻譯
import glob
for pdf_file in glob.glob("input/*.pdf"):
    translate(pdf_file, "output/", engine="google")
```

---

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

1. Fork 本倉庫
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

---

## 📄 許可證

本項目採用 **MIT License** - 詳見 [LICENSE](./LICENSE) 檔案

---

## 🙏 致謝

- 感謝 **[PDFMathTranslate](https://github.com/Byaidu/PDFMathTranslate)** 提供強大的 PDF 翻譯核心
- 感謝 **Google、DeepL、Azure** 等翻譯服務
- 感謝 **GitHub Actions** 和 **GitHub Pages** 的免費基礎設施支持

---

## 📞 聯繫方式

- 🐛 **提交 Bug**: [GitHub Issues](https://github.com/jimmymochi/PDF2zh/issues)
- 💬 **功能建議**: [Discussions](https://github.com/jimmymochi/PDF2zh/discussions)
- 📧 **Email**: jimmymochi@example.com

---

## 🎯 路線圖

- [ ] 支援更多語言對
- [ ] 批量下載功能
- [ ] Web UI 界面
- [ ] 本地 GUI 應用
- [ ] 翻譯進度即時通知
- [ ] 多檔案並發翻譯
- [ ] 翻譯質量評估

---

**最後更新**: 2026年5月5日

**⭐ 如果這個項目對你有幫助，請給一個 Star！** ⭐