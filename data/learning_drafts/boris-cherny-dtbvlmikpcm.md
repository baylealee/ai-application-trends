---
title: "boris_cherny 的 AI 工作流案例：8/ I use a few subagents regularly: code-s"
source_url: "https://www.threads.com/@boris_cherny/post/DTBVlMIkpcm"
source_author: "boris_cherny"
post_id: "DTBVlMIkpcm"
language: "unknown"
category: "coding"
tools:
  - "Claude"
  - "Claude Code"
status: "draft"
content_quality: "strong"
zh_ratio: 0.0
generated_at: "2026-11-16T07:06:02+00:00"
---

# boris_cherny 的 AI 工作流案例：8/ I use a few subagents regularly: code-s

> 狀態：自動草稿。本文由公開 Threads 抓取結果產生，尚未人工校稿。

## 一句話結論

8/ I use a few subagents regularly: code-simplifier simplifies the code after Claude is done working, verify-app has detailed instructions for testing Claude Code end to end, and s

## 這篇在解決什麼問題

這篇來源指向一個 AI 應用或工作流案例。根據目前抓到的公開文字，核心價值在於把工具、步驟或方法整理成可重複使用的做法。

## 使用工具

Claude、Claude Code

## 原始工作流拆解

1. 閱讀原文後，先確認它實際解決的工作情境。
2. 拆出輸入資料、AI 工具、處理步驟與輸出成果。
3. 再判斷是否能轉成自己的工作流範本。

## 可以直接複製的做法

1. 先確認你的輸入資料是什麼，例如文件、貼文、客戶資料、程式碼或任務描述。
2. 將原文中的 AI 工具與步驟拆成固定 SOP。
3. 用小範圍案例測試一次，不要一開始就全自動化。
4. 把輸出結果保存到 Sheet、Notion、GitHub 或你的知識庫。
5. 成功後再擴大成可重複執行的工作流。

## 適合誰使用

- 想收集繁中 AI 實戰案例的人
- 想把 Threads 靈感轉成內部 SOP 的營運或 PM
- 想建立 AI 工作流知識庫的團隊

## 限制與風險

- 這是自動草稿，只能根據公開抓到的文字整理。
- 如果原文需要登入、圖片 OCR 或完整留言串，內容可能不完整。
- 回覆區只整理公開抓得到的候選文字，不代表完整留言脈絡。

## 回覆區重點

reply_summary_status: `partial`

- 12/ For very long-running tasks, I will either prompt Claude to verify its work with a background agent when it's done, use an agent Stop hook to do that more deterministically, or use the ralph-wiggum plugin. I will also use either --permission-mode=dontAsk o
- [![Image 32: sanketh_'s profile picture](https://scontent-atl3-2.cdninstagram.com/v/t51.2885-19/441011942_780251840729670_7472623037393270397_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=102&_nc_map=urlgen_bucketless&ig_cache_key=GOZOSRpGUs2JosUCAH32OZQPF7RnbkULAAAB
- 11/ Claude Code uses all my tools for me. It often searches and posts to Slack (via the MCP server), runs BigQuery queries to answer analytics questions (using bq CLI), grabs error logs from Sentry, etc. The Slack MCP configuration is checked into our .mcp.jso
- 2/ I also run 5-10 Claudes on [claude.ai/code](https://l.threads.com/?u=http%3A%2F%2Fclaude.ai%2Fcode&e=AUB0Sn3Lzq1EPqsbH2I_RRwgzegzS7UdNWHzXzDa_hKr09gjDF1nheokTaCBt_nCI6eHh4oDvCq2mJl0pbjfGqI9KgVC1pykekIAHZej2USTFh32nDA), in parallel with my local Claudes. As 
- 7/ I use slash commands for every inner loop workflow that I do many times a day. This saves me from repeated prompting, and makes it so Claude can use these workflows, too. Commands are checked into git and live in .claude/commands/.

## 抓取品質

- content_quality: `strong`
- keyword_hits: AI、Claude、Agent、agent、workflow
- zh_ratio: `0.0`
- source_url: https://www.threads.com/@boris_cherny/post/DTBVlMIkpcm

## 原始抓取內容

```text
8/ I use a few subagents regularly: code-simplifier simplifies the code after Claude is done working, verify-app has detailed instructions for testing Claude Code end to end, and so on. Similar to slash commands, I think of subagents as automating the most common workflows that I do for most PRs.
```
