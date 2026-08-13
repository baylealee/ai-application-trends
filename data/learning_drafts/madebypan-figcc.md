---
title: "FigCC｜在 Figma 裡用本機 Codex／Claude Code 操作畫布"
source_url: "https://github.com/madebypan/FigCC"
notion_url: "https://app.notion.com/p/3bbb34f27ab481bf909ccb542027b943?pvs=204"
source_author: "madebypan"
category: "Frontend／UI"
tools:
  - "Figma"
  - "Codex CLI"
  - "Claude Code"
  - "MCP"
  - "Agent SDK"
status: "draft"
content_quality: "strong"
language: "zh-TW"
generated_at: "2026-08-13T01:28:00Z"
---

# FigCC｜在 Figma 裡用本機 Codex／Claude Code 操作畫布

> 狀態：自動學習草稿。已同步到 Notion「每日 AI 學習」，尚未人工實測。

## 一句話結論

FigCC 把 Figma 變成本機 Codex CLI／Claude Code 可操作的設計工作區，讓 Agent 可以讀取選取圖層、樣式、variables、components，並直接修改 canvas。

## 這篇在解決什麼問題

設計與前端協作常卡在「AI 能產 HTML／React，但不能真正理解或修改 Figma 設計稿」。FigCC 的價值在於把 Figma plugin、local bridge、Codex／Claude Code runtime、Figma tools 與 skills 放進同一條 workflow，讓 Agent 可以在實際畫布上做 inspection、reasoning 與 editing。

## 核心架構

```text
Figma plugin UI
    ⇅ authenticated WebSocket
FigCC local bridge
    ├⇄ Codex App Server
    └⇄ Claude Agent SDK + FigCC MCP server
    ⇅ tool calls and results
Figma plugin sandbox → current Figma document
```

## 可複製工作流

1. 在 Mac 安裝 FigCC，執行 `npm install`、`npm run build`、`npm run bridge:install`、`npm run bridge:token`。
2. 在 Figma desktop 匯入 `public/manifest.json`。
3. 在 FigCC settings 設定 bridge URL 與 pairing token。
4. 選取 Figma 畫布上的 frame、component、text 或 image。
5. 用 Codex 或 Claude 要求 Agent 做 component audit、命名整理、variables 轉換、icon export 或 selected card restyle。
6. 依影響範圍選擇 Read only、Workspace 或更高權限；重要檔案先用 Figma version history 保護。
7. 把重複使用的設計規則寫成 `skills/<name>/SKILL.md`，讓 Codex 與 Claude Code 共用。

## 適合誰使用

- 想把 Figma 設計稿接到 AI Agent 的設計師與前端工程師
- 想做 design system audit、component 整理、variables/token 轉換的人
- 已經使用 Codex CLI 或 Claude Code，希望它們能直接理解 Figma canvas 的團隊

## 限制與風險

- 目前需求是 macOS、Figma desktop、Node.js 18+，並需要本機已登入 Codex CLI 或 Claude Code。
- `run_figma_code` 可以直接修改 Figma 文件，重要設計檔應先複製或保留 version history。
- 權限 selector 控制的是本機 project files，不等於限制 Figma canvas 修改能力。
- 第三方 skill 應先檢查 `SKILL.md`，不要直接設為 Active。

## 可升級 SOP／Skill

**Figma × Agent 設計工作流 SOP**

1. Figma plugin 安裝與 bridge pairing
2. Agent 讀取 selection／styles／variables／components
3. Component audit 與命名規範
4. Design tokens／Figma variables 轉換
5. 視覺稿自動修正與回寫
6. 權限、version history 與第三方 skill 安全檢查

## 來源

https://github.com/madebypan/FigCC
