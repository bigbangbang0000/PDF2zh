#!/usr/bin/env python3
"""
自動化 PDF 翻譯腳本
透過內建 Python 環境直接呼叫 pdf2zh 核心 API
用法: python auto_translate.py [input_dir] [output_dir]
"""
import sys
import os
import site
from pathlib import Path

# ── 強制 UTF-8 輸出（避免 Windows cp950 亂碼）─────────────────────────
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# ── 路徑設定 ──────────────────────────────────────────────────────────
script_dir    = Path(__file__).resolve().parent
site_packages = script_dir / "build" / "site-packages"

# 注意：不能把 script_dir 加入 path，否則本地的 pdf2zh.py 會遮蔽套件庫
if site_packages.exists():
    site.addsitedir(str(site_packages))
    sys.path.insert(0, str(site_packages))

# ── 翻譯設定（可在此自訂）────────────────────────────────────────────
LANG_IN  = "en"       # 原始語言 (en = 英文)
LANG_OUT = "zh-TW"    # 目標語言 (zh-TW = 繁體中文 / zh = 簡體中文)
SERVICE  = "google"   # 翻譯引擎 (google / deepl / openai / ...)
THREADS  = 4          # 執行緒數量

# ── 資料夾設定 ────────────────────────────────────────────────────────
input_dir  = Path(sys.argv[1]) if len(sys.argv) > 1 else script_dir / "input"
output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else script_dir / "output"

input_dir.mkdir(parents=True, exist_ok=True)
output_dir.mkdir(parents=True, exist_ok=True)

def main():
    # 掃描 input 資料夾中的 PDF
    pdf_files = sorted(input_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"\n[錯誤] 在 {input_dir} 中找不到任何 PDF 檔案。")
        print("請將要翻譯的 PDF 放入 input 資料夾後再執行。")
        sys.exit(1)

    print(f"\n找到 {len(pdf_files)} 個 PDF 檔案，開始翻譯...")
    print(f"  輸入語言: {LANG_IN}  ->  輸出語言: {LANG_OUT}")
    print(f"  翻譯引擎: {SERVICE}  /  執行緒: {THREADS}")
    print(f"  輸出資料夾: {output_dir}\n")

    # ── 載入必要模組 ──────────────────────────────────────────────────
    try:
        from pdf2zh.high_level import translate
        from pdf2zh.doclayout import OnnxModel
    except ImportError as e:
        print(f"[錯誤] 無法載入 pdf2zh: {e}")
        sys.exit(1)

    # 載入 ONNX 排版辨識模型（必須）
    print("[準備] 載入版面辨識模型中，首次執行可能需要下載...")
    model = OnnxModel.load_available()
    print("[準備] 模型載入完成！\n")

    success_list = []
    failed_list  = []

    for idx, pdf_path in enumerate(pdf_files, 1):
        print(f"[{idx}/{len(pdf_files)}] 正在翻譯: {pdf_path.name}")
        try:
            translate(
                files=[str(pdf_path)],
                output=str(output_dir),
                lang_in=LANG_IN,
                lang_out=LANG_OUT,
                service=SERVICE,
                thread=THREADS,
                model=model,
            )
            out_file = output_dir / f"{pdf_path.stem}-mono.pdf"
            print(f"  [成功] 輸出: {out_file.name}")
            success_list.append(pdf_path.name)
        except Exception as e:
            print(f"  [失敗] {e}")
            failed_list.append((pdf_path.name, str(e)))

    print("\n" + "="*55)
    print(f"  翻譯完成！成功 {len(success_list)} / 失敗 {len(failed_list)}")
    print("="*55)
    if failed_list:
        print("\n失敗清單:")
        for name, err in failed_list:
            print(f"  X  {name}  ->  {err[:200]}")

if __name__ == "__main__":
    main()
