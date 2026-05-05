# PDF 自動翻譯工作流 (PDF2zh + GitHub Actions)

## 概述

本倉庫使用 **GitHub Actions** 自動化工作流，將上傳到 `input/` 資料夾的 PDF 檔案翻譯為中文，並在 GitHub Pages 上發布。

## 使用說明

### 1. 上傳 PDF 檔案

將要翻譯的 PDF 檔案放在 `input/` 資料夾中：

```
input/
├── document1.pdf
├── document2.pdf
└── ...
```

### 2. 推送到 GitHub

提交並推送您的更改：

```bash
git add input/*.pdf
git commit -m "Add PDFs for translation"
git push origin main
```

### 3. 自動翻譯

GitHub Actions 將自動：
- ✅ 檢測 `input/` 資料夾中的新 PDF
- ✅ 使用 `pdf2zh` 翻譯工具翻譯為中文
- ✅ 使用免費的 Google 翻譯引擎（無需 API Key）
- ✅ 將翻譯結果存放在 `output/` 資料夾
- ✅ 生成 `index.html` 列出所有可下載的翻譯 PDF

### 4. 下載翻譯結果

翻譯完成後，可在 GitHub Pages 上訪問結果：

```
https://jimmymochi.github.io/PDF2zh/
```

頁面將顯示所有可用的翻譯 PDF，點擊即可下載。

## 工作流配置

### 觸發條件

工作流在以下情況下自動運行：
- 推送新的 PDF 到 `input/` 資料夾
- 更新工作流檔案本身 (`.github/workflows/translate_pdf.yml`)
- 手動觸發 (`workflow_dispatch`)

### 工作流步驟

1. **檢出代碼** - 從倉庫拉取最新代碼
2. **設定 Python** - 安裝 Python 3.10+
3. **安裝依賴** - 安裝 pdf2zh 及其依賴
4. **創建目錄** - 確保 `input/` 和 `output/` 目錄存在
5. **翻譯 PDF** - 逐個翻譯 `input/` 中的所有 PDF
6. **生成索引** - 創建 `index.html` 列出翻譯結果
7. **部署到 GitHub Pages** - 將 `output/` 推送到 `gh-pages` 分支

## 配置說明

### 翻譯引擎

目前使用免費的 **Google 翻譯引擎**：
```bash
pdf2zh input.pdf -o output/ -e google
```

無需額外的 API Key。

### 輸出目錄結構

```
output/
├── index.html           # 自動生成的索引頁面
├── document1.pdf        # 翻譯後的 PDF
├── document2.pdf        # 翻譯後的 PDF
└── ...
```

## GitHub Pages 配置

確保倉庫設定中啟用了 GitHub Pages：

1. 進入倉庫 **Settings**
2. 找到 **Pages** 部分
3. 選擇 **Source**: 由 GitHub Actions 部署
4. Pages 將在推送後自動更新

## 故障排查

### PDF 翻譯失敗

如果工作流報告翻譯失敗：
1. 檢查 Actions 日誌查看詳細錯誤信息
2. 確認 PDF 檔案完整且未損壞
3. 檢查檔案名稱是否包含特殊字符

### GitHub Pages 未更新

1. 檢查 `gh-pages` 分支是否創建
2. 驗證 Pages 設定指向 `gh-pages` 分支
3. 清除瀏覽器快取

### 翻譯結果為空

1. 確認 PDF 確實上傳到 `input/` 資料夾
2. 檢查 Actions 日誌是否有錯誤信息
3. 等待工作流完成（可能需要幾分鐘）

## 高級配置

### 修改翻譯引擎

要使用其他翻譯引擎（如 DeepL），編輯 `.github/workflows/translate_pdf.yml`：

```bash
pdf2zh "$pdf_file" -o output/ -e deepl  # 改為 deepl
```

**注意**: 某些引擎可能需要 API Key。

### 自定義索引頁面

編輯 `generate_index.py` 自定義生成的 `index.html` 外觀。

## 環境要求

- **Python**: 3.10+
- **操作系統**: Ubuntu (GitHub Actions 標準環境)
- **依賴**: pdf2zh 及其所有依賴項（自動安裝）

## 相關資源

- [PDFMathTranslate (pdf2zh)](https://github.com/Byaidu/PDFMathTranslate)
- [GitHub Actions 文檔](https://docs.github.com/en/actions)
- [GitHub Pages 文檔](https://docs.github.com/en/pages)

## 許可證

本工作流與倉庫遵循相同的許可證。

---

💡 **提示**: 第一次運行工作流可能需要幾分鐘。之後每次推送 PDF 都會自動觸發翻譯。
