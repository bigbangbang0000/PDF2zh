#!/usr/bin/env python3
"""
互動式 PDF 翻譯工具
掃描 input 資料夾，讓用戶選擇要翻譯的 PDF 檔案
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Optional


class PDFTranslator:
    """互動式 PDF 翻譯管理類"""
    
    def __init__(self, input_dir: str = "input", output_dir: str = "output"):
        """初始化翻譯器"""
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        
        # 創建輸出目錄（如果不存在）
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_pdf_files(self) -> List[Path]:
        """掃描 input 資料夾中的 PDF 檔案"""
        if not self.input_dir.exists():
            return []
        
        pdf_files = sorted(self.input_dir.glob("*.pdf"))
        return pdf_files
    
    def display_menu(self):
        """顯示主菜單"""
        print("\n" + "=" * 60)
        print("  📄 PDF 翻譯工具 (PDF2zh Interactive Translator)")
        print("=" * 60)
    
    def display_files(self, pdf_files: List[Path]):
        """顯示可用的 PDF 檔案列表"""
        if not pdf_files:
            print("\n❌ input 資料夾中沒有找到任何 PDF 檔案。")
            print("   請將待翻譯的 PDF 複製到 input/ 資料夾。\n")
            return False
        
        print(f"\n✅ 在 input 資料夾中找到 {len(pdf_files)} 個 PDF 檔案：\n")
        for idx, pdf_file in enumerate(pdf_files, 1):
            file_size = pdf_file.stat().st_size / (1024 * 1024)  # 轉為 MB
            print(f"  {idx:2d}. {pdf_file.name:<40s} ({file_size:>7.2f} MB)")
        
        return True
    
    def get_translation_engine(self) -> str:
        """讓用戶選擇翻譯引擎"""
        print("\n" + "-" * 60)
        print("選擇翻譯引擎 (Translation Engine):")
        print("-" * 60)
        engines = {
            "1": ("google", "Google 翻譯（免費，推薦）"),
            "2": ("deepl", "DeepL（需要 API Key，品質最佳）"),
            "3": ("azure", "Azure Translator（需要 API Key）"),
            "4": ("bing", "Bing Translator（需要 API Key）"),
            "5": ("openai", "OpenAI（需要 API Key）"),
        }
        
        for key, (engine, desc) in engines.items():
            print(f"  {key}. {desc}")
        
        while True:
            choice = input("\n請選擇翻譯引擎 (輸入 1-5) [預設: 1]: ").strip() or "1"
            if choice in engines:
                engine, engine_name = engines[choice]
                print(f"✅ 已選擇: {engine_name}")
                return engine
            else:
                print("❌ 無效選項，請重新輸入")
    
    def get_language_option(self) -> tuple:
        """讓用戶選擇語言選項"""
        print("\n" + "-" * 60)
        print("選擇語言選項 (Language Option):")
        print("-" * 60)
        
        print("  1. 簡體中文（預設）")
        print("  2. 繁體中文")
        
        while True:
            choice = input("\n請選擇 (輸入 1-2) [預設: 1]: ").strip() or "1"
            if choice == "1":
                print("✅ 已選擇: 簡體中文")
                return ("zh", False)
            elif choice == "2":
                print("✅ 已選擇: 繁體中文")
                return ("zh", True)
            else:
                print("❌ 無效選項，請重新輸入")
    
    def get_api_key_if_needed(self, engine: str) -> Optional[str]:
        """如果選擇的引擎需要 API Key，提示用戶輸入"""
        engines_need_key = ["deepl", "azure", "bing", "openai"]
        
        if engine in engines_need_key:
            api_key = input(f"\n請輸入 {engine.upper()} API Key (留空跳過): ").strip()
            if api_key:
                return api_key
            else:
                print(f"⚠️  未提供 API Key，翻譯可能失敗")
                return None
        
        return None
    
    def select_files_to_translate(self, pdf_files: List[Path]) -> List[Path]:
        """讓用戶選擇要翻譯的 PDF 檔案"""
        print("\n" + "-" * 60)
        print("選擇要翻譯的檔案 (Select files to translate):")
        print("-" * 60)
        print("  輸入檔案編號，多個檔案用逗號分隔，或按 'a' 全選")
        print("  例如: 1,3,5 或 a")
        
        while True:
            choice = input("\n請輸入 [預設: a(全選)]: ").strip().lower() or "a"
            
            if choice == "a":
                selected = pdf_files
                print(f"✅ 已選擇全部 {len(pdf_files)} 個檔案")
                return selected
            
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(",")]
                
                # 檢查索引有效性
                if all(0 <= idx < len(pdf_files) for idx in indices):
                    selected = [pdf_files[idx] for idx in indices]
                    print(f"✅ 已選擇 {len(selected)} 個檔案:")
                    for pdf in selected:
                        print(f"   - {pdf.name}")
                    return selected
                else:
                    print("❌ 索引超出範圍，請重新輸入")
            except ValueError:
                print("❌ 輸入格式錯誤，請輸入編號或 'a'")
    
    def translate_files(self, pdf_files: List[Path], engine: str, 
                       language: str, traditional: bool, api_key: Optional[str] = None) -> dict:
        """翻譯選定的 PDF 檔案"""
        print("\n" + "=" * 60)
        print("  開始翻譯 (Starting translation...)")
        print("=" * 60)
        
        results = {
            "success": [],
            "failed": []
        }
        
        for idx, pdf_file in enumerate(pdf_files, 1):
            print(f"\n[{idx}/{len(pdf_files)}] 正在翻譯: {pdf_file.name}")
            print("-" * 60)
            
            try:
                # 構建 pdf2zh 命令
                cmd = [
                    "pdf2zh",
                    str(pdf_file),
                    "-o", str(self.output_dir),
                    "-e", engine,
                    "-l", language
                ]
                
                # 添加繁體中文選項
                if traditional:
                    cmd.append("--zh-traditional")
                
                # 添加 API Key（如果有）
                if api_key:
                    cmd.extend(["-k", api_key])
                
                # 執行翻譯
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=600  # 10 分鐘超時
                )
                
                if result.returncode == 0:
                    print(f"✅ 翻譯成功！")
                    results["success"].append(pdf_file.name)
                else:
                    error_msg = result.stderr or result.stdout
                    print(f"❌ 翻譯失敗！")
                    print(f"   錯誤: {error_msg[:200]}")
                    results["failed"].append((pdf_file.name, error_msg))
            
            except subprocess.TimeoutExpired:
                print(f"❌ 翻譯超時（超過 10 分鐘）")
                results["failed"].append((pdf_file.name, "Timeout"))
            
            except Exception as e:
                print(f"❌ 出現錯誤: {str(e)}")
                results["failed"].append((pdf_file.name, str(e)))
        
        return results
    
    def display_results(self, results: dict):
        """顯示翻譯結果總結"""
        print("\n" + "=" * 60)
        print("  翻譯結果總結 (Translation Summary)")
        print("=" * 60)
        
        success_count = len(results["success"])
        failed_count = len(results["failed"])
        
        if success_count > 0:
            print(f"\n✅ 成功翻譯 {success_count} 個檔案:")
            for filename in results["success"]:
                print(f"   - {filename}")
        
        if failed_count > 0:
            print(f"\n❌ 失敗 {failed_count} 個檔案:")
            for filename, error in results["failed"]:
                print(f"   - {filename}")
                if error and len(error) > 0:
                    print(f"     原因: {error[:100]}")
        
        if success_count == 0 and failed_count == 0:
            print("\n⚠️  沒有翻譯任何檔案")
        
        print(f"\n📁 翻譯結果已保存到: {self.output_dir.absolute()}")
        print("=" * 60 + "\n")
    
    def run(self):
        """運行互動式翻譯工具"""
        try:
            self.display_menu()
            
            # 掃描 PDF 檔案
            pdf_files = self.get_pdf_files()
            if not self.display_files(pdf_files):
                return
            
            # 選擇翻譯引擎
            engine = self.get_translation_engine()
            
            # 選擇語言選項
            language, traditional = self.get_language_option()
            
            # 如果需要 API Key
            api_key = self.get_api_key_if_needed(engine)
            
            # 選擇要翻譯的檔案
            selected_files = self.select_files_to_translate(pdf_files)
            
            # 確認翻譯設定
            print("\n" + "-" * 60)
            print("翻譯設定確認 (Confirm settings):")
            print("-" * 60)
            print(f"  翻譯引擎: {engine}")
            print(f"  目標語言: {'繁體中文' if traditional else '簡體中文'}")
            print(f"  待翻譯檔案數: {len(selected_files)}")
            
            confirm = input("\n確認開始翻譯？(y/n) [預設: y]: ").strip().lower() or "y"
            
            if confirm != "y":
                print("\n取消翻譯")
                return
            
            # 執行翻譯
            results = self.translate_files(
                selected_files, engine, language, traditional, api_key
            )
            
            # 顯示結果
            self.display_results(results)
            
            # 詢問是否生成索引頁面
            if results["success"]:
                gen_index = input("是否生成 GitHub Pages 索引頁面？(y/n) [預設: y]: ").strip().lower() or "y"
                if gen_index == "y":
                    try:
                        subprocess.run(["python", "generate_index.py"], check=True)
                        print("✅ 索引頁面已生成！")
                    except Exception as e:
                        print(f"⚠️  生成索引頁面失敗: {e}")
        
        except KeyboardInterrupt:
            print("\n\n取消操作")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ 發生錯誤: {e}")
            sys.exit(1)


def main():
    """主函數"""
    translator = PDFTranslator()
    translator.run()


if __name__ == "__main__":
    main()
