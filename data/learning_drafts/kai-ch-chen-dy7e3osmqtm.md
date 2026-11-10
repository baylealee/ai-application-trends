---
title: "kai_ch_chen 的 AI 工作流案例：今天opus 4.8推出新功能 Claude Code Workflow 但你的跟我"
source_url: "https://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm"
source_author: "kai_ch_chen"
post_id: "DY7E3oSmqtm"
language: "unknown"
category: "mcp"
tools:
  - "Claude"
  - "Claude Code"
  - "MCP"
  - "Codex"
status: "draft"
content_quality: "strong"
zh_ratio: 0.0708
generated_at: "2026-11-10T07:39:15+00:00"
---

# kai_ch_chen 的 AI 工作流案例：今天opus 4.8推出新功能 Claude Code Workflow 但你的跟我

> 狀態：自動草稿。本文由公開 Threads 抓取結果產生，尚未人工校稿。

## 一句話結論

今天opus 4.8推出新功能 Claude Code Workflow 但你的跟我的一樣嗎？

## 這篇在解決什麼問題

這篇來源指向一個 AI 應用或工作流案例。根據目前抓到的公開文字，核心價值在於把工具、步驟或方法整理成可重複使用的做法。

## 使用工具

Claude、Claude Code、MCP、Codex

## 原始工作流拆解

1. 乍看大家都有超棒團隊可以用，但實際上⋯ 它是已存的 subagent / skill 上編排；所以當你的基本功夫越好，workflow的效果也越好￼
2. 底層機制（Anthropic 官方）： • Workflow = Claude 即時寫的 JS 腳本 • 同一句「audit API」,根據你的 codebase 寫出不同編排 • subagent 一律 acceptEdits + 繼承 allowlist • 同時 16 隻 / 單次 1000 隻上限
3. [Image 9: Orchestrate subagents at scale with dynamic workflows - Claude Code Docs](https://external-ord5-1.xx.fbcdn.net/emg1/v/t13/11422783865225561921?
4. 目前使用 Claude Dynamic Workflow的一些實務心得，整理如下：
5. 以目前的使用經驗來看，對於複雜度不高的單一 Feature，使用 Dynamic Workflow 往往需要較長的執行時間，但最終效果與一般 SDD → Implementation Plan → Implementation 的流程差異不大，反而可能增加 Token 與運算資源的消耗。

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

- Title: Kai Chen (@kai_ch_chen) on Threads

URL Source: http://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm

Final URL: https://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm

Markdown Content:
[](https://www.threads.com/)

[Home](https://www.threads.com/)

New
- [![Image 2: kai_ch_chen's profile picture](https://scontent-ord5-1.cdninstagram.com/v/t51.82787-19/842421879_17989821741115625_4127758461532433539_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=101&ig_cache_key=GHdWNjLpqHPGpek-AIPsQHJzvkg5bmNDAQAB1501500j-ccb7-5&ccb=7
- [![Image 2: kai_ch_chen's profile picture](https://scontent-ord5-1.cdninstagram.com/v/t51.82787-19/842421879_17989821741115625_4127758461532433539_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=101&ig_cache_key=GHdWNjLpqHPGpek-AIPsQHJzvkg5bmNDAQAB1501500j-ccb7-5&ccb=7

## 抓取品質

- content_quality: `strong`
- keyword_hits: AI、Claude、MCP、Codex、Agent、agent、工作流、流程、工具、整理、設計、CLI、workflow
- zh_ratio: `0.0708`
- source_url: https://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm

## 原始抓取內容

```text
Title: Kai Chen (@kai_ch_chen) on Threads

URL Source: https://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm

Markdown Content:
[](https://www.threads.com/)

[](https://www.threads.com/)

[](https://www.threads.com/search)

# [Thread 1.8K views](https://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm)

[![Image 1: kai_ch_chen's profile picture](https://scontent-ord5-1.cdninstagram.com/v/t51.82787-19/842421879_17989821741115625_4127758461532433539_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=101&ig_cache_key=GHdWNjLpqHPGpek-AIPsQHJzvkg5bmNDAQAB1501500j-ccb7-5&ccb=7-5&_nc_sid=43db74&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xNTAuQzMifQ%3D%3D&_nc_ohc=NXfHF6IPfeIQ7kNvwHfJMOw&_nc_oc=Adr2WogZwjAlRr2gA57rvtUZHNAxpsOpTtdJHKgvnpSDwByEWP5uMHgP49gPKGPuEXU&_nc_zt=24&_nc_ht=scontent-ord5-1.cdninstagram.com&_nc_gid=GiAiiT6D1aSyPv-fo6Tlxw&_nc_ss=7b289&oh=00_AQTybOLQYh4cyrwnlbpGGQOho3tOb4oAXn09ayNRBGbK4Q&oe=6AF89636)](https://www.threads.com/@kai_ch_chen)

[kai_ch_chen](https://www.threads.com/@kai_ch_chen)

[05/29/26](https://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm)

今天opus 4.8推出新功能 Claude Code Workflow 但你的跟我的一樣嗎？

乍看大家都有超棒團隊可以用，但實際上⋯ 它是已存的 subagent / skill 上編排；所以當你的基本功夫越好，workflow的效果也越好￼

底層機制（Anthropic 官方）： • Workflow = Claude 即時寫的 JS 腳本 • 同一句「audit API」,根據你的 codebase 寫出不同編排 • subagent 一律 acceptEdits + 繼承 allowlist • 同時 16 隻 / 單次 1000 隻上限

3 件你能做: 1️⃣ /workflows 按 s 存成 /<name> 重跑 2️⃣ 路徑 .claude/workflows/ 或 ~/ 3️⃣ 弱 stage 換小 model 控成本

#ClaudeCode #AIWorkflow #VibeCoding

Translate

![Image 2](https://scontent-ord5-1.cdninstagram.com/v/t51.82787-15/708436994_17967927015115625_4354799560386143001_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=106&ig_cache_key=MzkwNzczNzUwOTI3MDkwNTUzOA%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0ueHBpZHMuMTA4MC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=eQLSrm5ycpUQ7kNvwFzHTkL&_nc_oc=AdouVa7oOFu3BsOgZVRGX9mZ-N7sQ4lmlHCmSN03HjbesOISKEo6NMP01R5EVkHvPcQ&_nc_zt=23&_nc_ht=scontent-ord5-1.cdninstagram.com&_nc_gid=oUIaDstvL-peqIISRa_XrQ&_nc_ss=7b289&oh=00_AQQa9mhqf7NlNOlsINDHHs3Sf_faMVO7oRrWsJ2wPo30Vg&oe=6AF89A5C)

![Image 3](https://scontent-ord5-1.cdninstagram.com/v/t51.82787-15/710423704_17967927042115625_806239602093737943_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=111&ig_cache_key=MzkwNzczNzUwOTkyNTYwOTk1OA%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0ueHBpZHMuMTA4MC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=s0MpHDI4H1oQ7kNvwH_LFO-&_nc_oc=AdpQUyPpOI6bIdO4wuC3bnQxp1bzTdQW1DKJhH5ttdafx8jkFHD5NVIq9hfJr7Om8ME&_nc_zt=23&_nc_ht=scontent-ord5-1.cdninstagram.com&_nc_gid=oUIaDstvL-peqIISRa_XrQ&_nc_ss=7b289&oh=00_AQQDhIImtQP3qlNfuZlEVgy74vAbETZyMNuBgiLhsHaPLw&oe=6AF8907E)

![Image 4](https://scontent-ord5-2.cdninstagram.com/v/t51.82787-15/709266337_17967927027115625_4606066761855847356_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=100&ig_cache_key=MzkwNzczNzUxMDAzNDE2NDI4OA%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0ueHBpZHMuMTA4MC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc
```
