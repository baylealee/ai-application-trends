---
title: "open-slide｜為 AI Agent 設計的 React 簡報框架"
source_url: "https://open-slide.dev/"
canonical_project_url: "https://github.com/1weiho/open-slide"
language: "zh-TW"
category: "Agent／Workflow"
tools:
  - "React"
  - "Claude"
  - "Codex"
  - "Cursor"
  - "Gemini CLI"
status: "draft"
origin: "notion_mcp"
generated_at: "2026-08-13T09:19:00Z"
---

# open-slide｜為 AI Agent 設計的 React 簡報框架

> 狀態：MCP 同步草稿。這筆來源是官方網站，和既有 GitHub repo 學習項目 `https://github.com/1weiho/open-slide` 屬於同一專案，公開上架時應合併處理，不要拆成兩篇。

## 一句話結論

open-slide 是 React-first 的簡報框架，把每一頁簡報當成 1920×1080 canvas 上的任意 React component，讓 AI coding agent 可以直接產生、修改、註解與迭代簡報。

## 這篇在解決什麼問題

傳統簡報工具對 AI agent 不夠友善：版面、元件與互動通常不是 code-first。open-slide 的核心做法是把 slide deck 變成可被 agent 編輯的 React 專案，讓 Claude、Codex、Cursor、Gemini CLI 等工具能直接改檔案、套用 comment、管理 assets，並即時看到渲染結果。

## 官方網站重點

- React-first slide framework。
- 每頁都是 arbitrary code，固定在 1920×1080 canvas。
- 可用 `npx @open-slide/cli init` 建立 deck。
- Agent 可以透過 `/create-slide` 產生簡報。
- 可在畫布上點選元素、留下 comment，再用 `/apply-comments` 讓 agent 精準修改。
- 支援圖片與 logo assets 管理。
- 任何能修改 React 的 coding agent 都可使用。

## 今日實作

1. 執行 `npx @open-slide/cli init my-deck` 建立專案。
2. 啟動 dev server，請 agent 用 `/create-slide` 建立一份 5 頁簡報。
3. 測試 canvas inspect：點選標題、文字、圖片並修改。
4. 留下 comment marker，再執行 `/apply-comments`。
5. 測試 assets：上傳圖片、搜尋 logo、替換 slide 中的圖像。
6. 比較它和 PPTX／Google Slides 自動生成流程的差異。

## 適合轉成的 SOP／Skill

AI 簡報生成與修改 SOP：

1. 使用 open-slide 建立固定 slide workspace。
2. 用 prompt 定義簡報目的、頁數、受眾與視覺風格。
3. 讓 agent 產生 React slide pages。
4. 人在 canvas 針對具體元素留言。
5. agent 依 comment marker 精準改檔。
6. 將可複用版型整理成 `skills/` 或 template。
7. 匯出或部署為 HTML／PDF。

## Baylea 筆記

這個專案很適合放進 AI Trends 的「簡報自動化」與「Agent-native 文件產出」分類。它和一般 slide generator 不同，重點不是一次性產生 PPT，而是讓簡報保留為可被 agent 反覆修改的 React codebase。

## 來源

https://open-slide.dev/

相關 GitHub：

https://github.com/1weiho/open-slide
