# AI 四格漫畫自動生成系統

這是一個使用 AI 自動生成四格漫畫的系統，涵蓋主題選擇、劇情生成、圖像合成與漫畫排版，並可自動上傳 IG Shorts / YouTube Shorts。

## 💡 核心功能

- 自動生成劇情腳本與角色對話
- 利用 Stable Diffusion 產生漫畫風格圖像
- 自動排版為四格漫畫，疊加對話框
- Gradio 介面操作簡易，未來支援 API 使用

## 📦 安裝需求

```shell
pip install -r requirements.txt
```

建議使用 Python 3.10 以上版本，Stable Diffusion 需 CUDA GPU。

## 🚀 執行方式

單次生成一組漫畫：
```shell
python scripts/main_pipeline.py
```

或執行 Gradio UI：
```shell
python ui/gradio_app.py
```

## 📁 目錄說明

- `scripts/`：各模組執行腳本
- `prompts/`：提示詞模板與角色個性設定
- `assets/`：生成圖像資料
- `ui/`：Gradio 或 Streamlit 前端應用
- `docs/`：技術設計與專案文件

## 🧠 使用模型
- 文案生成：GPT-4 API / LLaMA 2
- 圖像生成：Stable Diffusion + ComicDiffusion
- Prompt Control：ControlNet（人物動作/分鏡）

## 📍 授權
MIT License

## 📅 每週分工明細

### ✅ 第 1 週：技術選型與專案架構
**成員 A 任務**
- 評估 Hugging Face 可用模型（文案/圖像）
- 建立 GitHub Repo 專案架構與 README

**成員 B 任務**
- 安裝 Stable Diffusion / LLM base
- 收集漫畫主題類型與參考範例

### ✅ 第 2 週：劇情生成系統開發
**成員 A 任務**
- 使用 HuggingFace Transformers 撰寫腳本產生器
- 設定角色風格 prompt、格式標準

**成員 B 任務**
- 設計四格漫畫劇情格式（含角色、情境、對話）
- 撰寫測試題材腳本（5~10 組）

### ✅ 第 3 週：漫畫風格圖像生成與微調
**成員 A 任務**
- 安裝 Stable Diffusion + ComicDiffusion
- 測試 ControlNet 加人物動作模板生成

**成員 B 任務**
- 幫助準備 prompt（含角色動作、場景敘述）
- 撰寫圖像生成測試腳本

### ✅ 第 4 週：四格合成與字幕疊加
**成員 A 任務**
- 用 Python PIL / OpenCV 合成四格
- 自動嵌入字幕與角色名稱

**成員 B 任務**
- 設計文字框、對話顯示樣式
- 撰寫四格漫畫合成測試腳本

### ✅ 第 5 週：Pipeline 打通 + Web 原型
**成員 A 任務**
- 用 Gradio 建立輸入主題 → 輸出漫畫介面
- 整合劇情與圖像輸出流程

**成員 B 任務**
- 撰寫 UI 說明文字，測試使用流程
- 撰寫 Pipeline 測試腳本

### ✅ 第 6 週：主題自動獲取 + 自動化全流程
**成員 A 任務**
- 開發新聞摘要 / Reddit API 模組
- 加入每日自動生成腳本（排程）

**成員 B 任務**
- 撰寫簡化 prompt 指令規則
- 測試並記錄生成失敗案例

### ✅ 第 7 週：品牌包裝與影片化導出
**成員 A 任務**
- 用 ffmpeg 或其他工具生成 Shorts 影片格式
- 建立影片導出格式（1080x1920 四格滑入）

**成員 B 任務**
- 註冊 IG、YouTube Shorts 帳號並上架測試作品
- 撰寫影片生成測試腳本

### ✅ 第 8 週：成果整理與簡報發表
**成員 A 任務**
- 撰寫技術報告與系統架構文件
- 部署網頁 demo（Gradio 或 Hugging Face Space）

**成員 B 任務**
- 製作簡報（含流程圖、作品展示）
- 撰寫簡報展示測試腳本