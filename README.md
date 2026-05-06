# PDF2zh — Windows 本地 PDF 翻譯工具

[![Python Version](https://img.shields.io/badge/python-3.12-blue?style=flat-square)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](./LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-0078d7?style=flat-square&logo=windows)](https://github.com/bigbangbang0000/PDF2zh)
[![Based on PDFMathTranslate](https://img.shields.io/badge/based%20on-PDFMathTranslate%201.9.11-purple?style=flat-square)](https://github.com/Byaidu/PDFMathTranslate)

**PDF2zh** 是基於 [PDFMathTranslate](https://github.com/Byaidu/PDFMathTranslate) 的 Windows 本地 PDF 翻譯工具包，**完全免指令操作**。雙擊或拖曳即可將英文 PDF 翻譯成繁體中文，並自動開啟翻譯結果資料夾。

📦 [PDFMathTranslate 原始專案](https://github.com/Byaidu/PDFMathTranslate)

---

## ✨ 主要特性

- 🖱️ **零指令操作** — 雙擊或拖曳，不需要打任何終端機指令
- 📂 **自動開啟資料夾** — 翻譯完成後自動打開 `output` 資料夾，直接拿到結果
- 🌐 **Google 翻譯（免費）** — 預設使用 Google 翻譯，無需 API Key
- 📄 **雙版本輸出** — 同時生成「純中文版（mono）」與「中英雙語對照版（dual）」
- 🧠 **保留數學公式與排版** — 基於 PDFMathTranslate，公式與圖表不會被破壞
- 📦 **內建 Python 環境** — 不需要事先安裝 Python，開箱即用

---

## 🚀 超簡單使用方式（Windows）

> ⚠️ **前提**：請使用 `pdf2zh-v1.9.11-win64` 資料夾內的 `pdf2zh` 子資料夾，裡面已包含所有必要的執行環境。

### 方法 1：拖曳即翻譯 ⭐（最方便）

1. 在資料夾中找到 `拖曳PDF到此翻譯.bat`
2. 把你想翻譯的 PDF 檔案，**直接用滑鼠拖到這個 .bat 圖示上面**放開
3. 可以一次拖曳多個 PDF 檔案
4. 翻譯完成後，程式會**自動開啟 `output` 資料夾**，直接取得翻譯結果

```
📁 pdf2zh\
 └── 拖曳PDF到此翻譯.bat  ← 把 PDF 拖到這裡
```

---

### 方法 2：一鍵自動翻譯（資料夾批次）

1. 雙擊執行 `一鍵自動翻譯.bat`
2. 程式偵測到 `input` 資料夾是空的，會**自動開啟 input 資料夾**
3. 把要翻譯的 PDF 複製進去，然後在黑色視窗按任意鍵
4. 程式自動翻譯所有 PDF
5. 完成後**自動開啟 `output` 資料夾**

```
📁 pdf2zh\
 ├── 一鍵自動翻譯.bat   ← 雙擊執行
 ├── input\             ← 放入要翻譯的 PDF
 └── output\            ← 翻譯結果在這裡
```

---

### 方法 3：本地網頁介面 (Web UI) 🌐

如果你不想點擊 `.bat` 看黑底白字的視窗，我們也提供了一個完整的**網頁圖形介面**！

1. 雙擊執行 `啟動網頁介面.bat`
2. 程式會自動啟動伺服器，並在 3 秒後於瀏覽器中開啟 `http://localhost:7860`
3. 你可以直接在網頁上：
   - 點擊上傳 PDF
   - 選擇翻譯引擎、語言
   - 查看即時預覽與進度條
4. 翻譯完成後直接在網頁上下載！

*(注意：使用期間請勿關閉那個黑色的伺服器視窗)*

---

## ☁️ 雲端自動翻譯（免下載、免安裝）

對於從 GitHub 看到這個專案的使用者，你可以完全不下載任何檔案，直接透過 GitHub 自動幫你翻譯！

> **為什麼不能用 GitHub Pages 直接上傳翻譯？**
> GitHub Pages 只支援「靜態網頁 (HTML/CSS)」，無法執行 Python 翻譯核心程式。因此我們採用「GitHub Actions (雲端運算)」搭配「GitHub Pages (展示結果)」的機制。

### 如何使用 GitHub 雲端翻譯：

1. **上傳檔案**：在 GitHub 網站上，進入 `input/` 資料夾，點擊 `Add file` -> `Upload files`，上傳你要翻譯的 PDF 檔案，並 Commit 儲存。
2. **自動翻譯**：GitHub Actions 會在雲端自動啟動（你可以在 `Actions` 頁籤看到進度），大約需要幾分鐘時間。
3. **下載結果**：翻譯完成後，系統會自動更新你的 GitHub Pages 網站。你可以直接前往你的 `https://你的帳號.github.io/PDF2zh/` 網頁，直接點擊下載翻譯好的 PDF！

每個翻譯完成的 PDF 會在 `output` 資料夾中生成兩個檔案：

| 檔案 | 說明 |
|------|------|
| `原始檔名-mono.pdf` | **純繁體中文版**（推薦閱讀用） |
| `原始檔名-dual.pdf` | **中英雙語對照版**（對照參考用） |

---

## ⚙️ 翻譯設定自訂

如需修改翻譯引擎或目標語言，編輯 `auto_translate.py` 的第 24–27 行：

```python
LANG_IN  = "en"       # 原始語言（en = 英文）
LANG_OUT = "zh-TW"    # 目標語言（zh-TW = 繁體中文 / zh = 簡體中文）
SERVICE  = "google"   # 翻譯引擎（google / deepl / openai ...）
THREADS  = 4          # 執行緒數量
```

### 支援的翻譯引擎

| 引擎 | 是否需要 API Key | 品質 |
|------|----------------|------|
| `google` | ❌ 不需要（預設） | ⭐⭐⭐⭐ |
| `deepl` | ✅ 需要 | ⭐⭐⭐⭐⭐ |
| `openai` | ✅ 需要 | ⭐⭐⭐⭐⭐ |
| `bing` | ✅ 需要 | ⭐⭐⭐ |
| `azure` | ✅ 需要 | ⭐⭐⭐⭐ |

---

## 📁 目錄結構

```
pdf2zh/
├── 一鍵自動翻譯.bat          # 雙擊執行，自動處理 input 資料夾 ⭐
├── 拖曳PDF到此翻譯.bat        # 拖曳 PDF 到此即可翻譯 ⭐
├── auto_translate.py          # 一鍵翻譯的 Python 核心邏輯
├── auto_translate_single.py   # 拖曳翻譯的 Python 核心邏輯
├── input/                     # 放入待翻譯的 PDF
├── output/                    # 翻譯結果輸出位置
├── build/
│   ├── pdf2zh.exe             # GUI 啟動程式（Gradio 介面）
│   ├── runtime/
│   │   └── python.exe         # 內建 Python 3.12 執行環境
│   └── site-packages/         # 內建依賴套件
└── README.md
```

---

## 🐛 常見問題排除

### 問題 1：翻譯失敗，出現 `NoneType` 錯誤

**原因**：排版辨識模型（ONNX）未能正確載入。  
**解決**：確認網路連線，程式首次執行時會自動下載模型快取。

### 問題 2：翻譯結果亂碼

**原因**：PDF 是掃描版（圖片型），並非文字型 PDF。  
**解決**：本工具只支援**可選取文字**的 PDF；掃描版 PDF 請先用 OCR 工具處理。

### 問題 3：拖曳後什麼都沒發生

**原因**：拖曳時放開的位置可能不正確。  
**解決**：把 PDF 圖示拖到 `拖曳PDF到此翻譯.bat` 的圖示**正上方**再放開；或使用方法 2（一鍵自動翻譯）。

### 問題 4：Google 翻譯失敗 / 速度很慢

**原因**：Google 翻譯有時限速或暫時不可用。  
**解決**：等幾分鐘後重試，或更換翻譯引擎（如 DeepL）。

---

## 📊 效能參考

| 頁數 | 大約翻譯時間（Google） |
|------|----------------------|
| 6 頁 | 約 10 秒 |
| 30 頁 | 約 1 分鐘 |
| 100 頁 | 約 3–5 分鐘 |

*實際時間取決於 PDF 複雜度與網路速度*

---

## 🔐 隱私說明

- PDF 內容會透過網路傳送至 Google 翻譯伺服器（使用 google 引擎時）
- 建議不要翻譯含有機密、個人隱私資訊的文件
- 本工具本身完全在本機運行，不會上傳任何資料到第三方（翻譯 API 除外）

---

## 🙏 致謝

- [PDFMathTranslate](https://github.com/Byaidu/PDFMathTranslate) — 提供核心 PDF 翻譯技術
- Google、DeepL、Azure 等翻譯服務提供商

---

**最後更新**：2026 年 5 月 7 日