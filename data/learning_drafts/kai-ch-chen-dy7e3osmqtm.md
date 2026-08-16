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
  - "GitHub"
status: "draft"
content_quality: "strong"
zh_ratio: 0.0568
generated_at: "2026-08-16T02:08:24+00:00"
---

# kai_ch_chen 的 AI 工作流案例：今天opus 4.8推出新功能 Claude Code Workflow 但你的跟我

> 狀態：自動草稿。本文由公開 Threads 抓取結果產生，尚未人工校稿。

## 一句話結論

今天opus 4.8推出新功能 Claude Code Workflow 但你的跟我的一樣嗎？

## 這篇在解決什麼問題

這篇來源指向一個 AI 應用或工作流案例。根據目前抓到的公開文字，核心價值在於把工具、步驟或方法整理成可重複使用的做法。

## 使用工具

Claude、Claude Code、MCP、GitHub

## 原始工作流拆解

1. 乍看大家都有超棒團隊可以用，但實際上⋯ 它是已存的 subagent / skill 上編排；所以當你的基本功夫越好，workflow的效果也越好￼
2. 底層機制（Anthropic 官方）： • Workflow = Claude 即時寫的 JS 腳本 • 同一句「audit API」,根據你的 codebase 寫出不同編排 • subagent 一律 acceptEdits + 繼承 allowlist • 同時 16 隻 / 單次 1000 隻上限
3. [Image 9: Orchestrate subagents at scale with dynamic workflows - Claude Code Docs](https://external-sea5-1.xx.fbcdn.net/emg1/v/t13/12691295212030448036?
4. 同一個任務，丟進聊天介面跟在 Claude Code 裡做，體感差很多，但原因不是品質——是流程的摩擦點不同。
5. 我試過的例子是「解析這份 JSON，找出格式有問題的欄位，輸出修正後的結構」。

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

URL Source: https://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm

Markdown Content:
[](https://www.threads.com/)

[](https://www.threads.com/)

[](https://www.threads.com/search)

# [Thread 1.8K views](https://www.th
- Title: Kai Chen (@kai_ch_chen) on Threads

URL Source: https://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm

Markdown Content:
[![Image 1: kai_ch_chen's profile picture](https://scontent-sea5-1.cdninstagram.com/v/t51.82787-19/703222852_17965468269115625_38893
- ⚠️ v2.1.154+ research preview 📚 [code.claude.com/docs…](https://l.threads.com/?u=http%3A%2F%2Fcode.claude.com%2Fdocs%2Fen%2Fworkflows&e=AUCPDLow6ULjMBiRtQlPiUAIFnOLvI1Cqse1Y7rkChWYKzl26ukSA1hnhzFgfVo2VEeCKtEHx3DShU7_JCv2U-9XkqCrKR1Vi2TnJ-ECF3Ib4fWh7Qk)
- 甚至可以整理成 [CLAUDE.md](https://l.threads.com/?u=http%3A%2F%2FCLAUDE.md%2F&e=AUCPDLow6ULjMBiRtQlPiUAIFnOLvI1Cqse1Y7rkChWYKzl26ukSA1hnhzFgfVo2VEeCKtEHx3DShU7_JCv2U-9XkqCrKR1Vi2TnJ-ECF3Ib4fWh7Qk) 的改善建議。

## 抓取品質

- content_quality: `strong`
- keyword_hits: AI、Claude、MCP、Agent、agent、自動化、流程、prompt、工具、摘要、整理、GitHub、CLI、workflow
- zh_ratio: `0.0568`
- source_url: https://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm

## 原始抓取內容

```text
Title: Kai Chen (@kai_ch_chen) on Threads

URL Source: http://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm

Markdown Content:
[](http://www.threads.com/)

[](http://www.threads.com/)

[](http://www.threads.com/search)

# [Thread 1.8K views](http://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm)

[![Image 1: kai_ch_chen's profile picture](https://scontent-sea5-1.cdninstagram.com/v/t51.82787-19/703222852_17965468269115625_388939806295097201_n.jpg?stp=dst-jpg_s150x150_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby45MDAuYzIifQ&_nc_ht=scontent-sea5-1.cdninstagram.com&_nc_cat=105&_nc_oc=Q6cZ2gE_rKau9EpyLJvkLDQ6f2KW6LHTYLhTLWZ3aFyO5uiW1sUik2oVDY_taEr4PmlcevY&_nc_ohc=CTCwqVsiFl0Q7kNvwEWwpWs&_nc_gid=Vn991-vDw8ECCz3p9--D6g&edm=APs17CUBAAAA&ccb=7-5&oh=00_AQHpeAp2Xd0bTLMyDv_9GHgG3_k_pgVuj2lGT5hP2UvoNA&oe=6A86E97A&_nc_sid=10d13b)](http://www.threads.com/@kai_ch_chen)

[kai_ch_chen](http://www.threads.com/@kai_ch_chen)

[05/29/26](http://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm)

今天opus 4.8推出新功能 Claude Code Workflow 但你的跟我的一樣嗎？

乍看大家都有超棒團隊可以用，但實際上⋯ 它是已存的 subagent / skill 上編排；所以當你的基本功夫越好，workflow的效果也越好￼

底層機制（Anthropic 官方）： • Workflow = Claude 即時寫的 JS 腳本 • 同一句「audit API」,根據你的 codebase 寫出不同編排 • subagent 一律 acceptEdits + 繼承 allowlist • 同時 16 隻 / 單次 1000 隻上限

3 件你能做: 1️⃣ /workflows 按 s 存成 /<name> 重跑 2️⃣ 路徑 .claude/workflows/ 或 ~/ 3️⃣ 弱 stage 換小 model 控成本

#ClaudeCode #AIWorkflow #VibeCoding

Translate

![Image 2](https://scontent-sea1-1.cdninstagram.com/v/t51.82787-15/708436994_17967927015115625_4354799560386143001_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=106&ig_cache_key=MzkwNzczNzUwOTI3MDkwNTUzOA%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0ueHBpZHMuMTA4MC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=f4jLEDGeZ8UQ7kNvwFvDTBL&_nc_oc=AdqSVUtnNqG1SSSEAo-fUrU-W-6oCg3iblPPbQUd3EFBLS53PskCzXxS64au9Cdr5as&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-sea1-1.cdninstagram.com&_nc_gid=Vn991-vDw8ECCz3p9--D6g&_nc_ss=7a22e&oh=00_AQF0Jv0SJxihjrGIeEIGRsHFHIw8_kbcfOkE43AsWJxmmg&oe=6A87011C)

![Image 3](https://scontent-sea5-1.cdninstagram.com/v/t51.82787-15/710423704_17967927042115625_806239602093737943_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=111&ig_cache_key=MzkwNzczNzUwOTkyNTYwOTk1OA%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0ueHBpZHMuMTA4MC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=-LHOSQWT8_QQ7kNvwEqrxP2&_nc_oc=AdquRxygIwdjrDqYkcSZ-NrYdBamAPmAhVZLhKsegeGEaW78zaF2DW27F4HPnDHkjuk&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-sea5-1.cdninstagram.com&_nc_gid=Vn991-vDw8ECCz3p9--D6g&_nc_ss=7a22e&oh=00_AQFi5nAt4kolAGdn5n0VVOLZU7DUMctJMPalswohcPcTmQ&oe=6A86F73E)

![Image 4](https://scontent-sea1-1.cdninstagram.com/v/t51.82787-15/709266337_17967927027115625_4606066761855847356_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=100&ig_cache_key=MzkwNzczNzUxMDAzNDE2NDI4OA%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0ueHBpZHMuMTA4MC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=wJNzYDj7oEcQ7kNvwFwyIcr&_nc_oc=Adpi
```
