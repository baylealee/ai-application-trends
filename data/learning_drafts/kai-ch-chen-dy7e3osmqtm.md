---
title: "kai_ch_chen 的 AI 工作流案例：今天opus 4.8推出新功能 Claude Code Workflow 但你的跟我"
source_url: "https://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm"
source_author: "kai_ch_chen"
post_id: "DY7E3oSmqtm"
language: "unknown"
category: "coding"
tools:
  - "Claude"
  - "Claude Code"
  - "Codex"
  - "GitHub"
status: "draft"
content_quality: "strong"
zh_ratio: 0.0299
generated_at: "2026-10-08T06:30:39+00:00"
---

# kai_ch_chen 的 AI 工作流案例：今天opus 4.8推出新功能 Claude Code Workflow 但你的跟我

> 狀態：自動草稿。本文由公開 Threads 抓取結果產生，尚未人工校稿。

## 一句話結論

今天opus 4.8推出新功能 Claude Code Workflow 但你的跟我的一樣嗎？

## 這篇在解決什麼問題

這篇來源指向一個 AI 應用或工作流案例。根據目前抓到的公開文字，核心價值在於把工具、步驟或方法整理成可重複使用的做法。

## 使用工具

Claude、Claude Code、Codex、GitHub

## 原始工作流拆解

1. 乍看大家都有超棒團隊可以用，但實際上⋯ 它是已存的 subagent / skill 上編排；所以當你的基本功夫越好，workflow的效果也越好￼
2. 底層機制（Anthropic 官方）： • Workflow = Claude 即時寫的 JS 腳本 • 同一句「audit API」,根據你的 codebase 寫出不同編排 • subagent 一律 acceptEdits + 繼承 allowlist • 同時 16 隻 / 單次 1000 隻上限
3. [Image 9: Orchestrate subagents at scale with dynamic workflows - Claude Code Docs](https://external-atl3-2.xx.fbcdn.net/emg1/v/t13/2040504209610142836?
4. 同一段流程說明、同一份 prompt,你是不是每天重貼一次
5. 指令: claude plugin marketplace add anthropics/skills claude plugin install example-skills@anthropic-agent-skills

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

Markdown Content:
[](http://www.threads.com/)

[Home](http://www.threads.com/)

New thread

[Search](http://www.threads.com/search)

Messages

Activity
- [![Image 9: Orchestrate subagents at scale with dynamic workflows - Claude Code Docs](https://external-atl3-1.xx.fbcdn.net/emg1/v/t13/2040504209610142836?url=https%3A%2F%2Fclaude-code.mintlify.app%2F_next%2Fimage%3Furl%3D%252F_mintlify%252Fapi%252Fog%253Fdivis

## 抓取品質

- content_quality: `strong`
- keyword_hits: AI、Claude、Codex、Agent、agent、工作流、流程、prompt、工具、設計、GitHub、CLI、workflow
- zh_ratio: `0.0299`
- source_url: https://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm

## 原始抓取內容

```text
Title: Kai Chen (@kai_ch_chen) on Threads

URL Source: https://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm

Markdown Content:
[](https://www.threads.com/)

[Home](https://www.threads.com/)

New thread

[Search](https://www.threads.com/search)

Messages

Activity

Profile

Insights

[Log in](https://www.threads.com/login?show_choice_screen=false)

More

[](https://www.threads.com/)

[](https://www.threads.com/)

[](https://www.threads.com/search)

# [Thread](https://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm)

1.8K views

[![Image 1: kai_ch_chen's profile picture](https://scontent-atl3-1.cdninstagram.com/v/t51.82787-19/703222852_17965468269115625_388939806295097201_n.jpg?_nc_cat=103&ccb=7-5&_nc_sid=30ff31&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xNTAuQzMifQ%3D%3D&_nc_ohc=m-EKiHVbMQ8Q7kNvwF8UW3c&_nc_oc=AdqnOpZRhjK5UZD6jRsyEKXT5fcYb_3x0_30wBNjMBnMr9CW47oXj0GWeOqopXngGLE&_nc_zt=24&_nc_ht=scontent-atl3-1.cdninstagram.com&_nc_gid=KCaalplUU_jcFYWRwsDRfw&_nc_ss=7b289&oh=00_AQNddM0Cjnw8pt4JJNfVXKXEq8NEYrYfEq1HM7vzVnj4pw&oe=6ACD013A)](https://www.threads.com/@kai_ch_chen)

[kai_ch_chen](https://www.threads.com/@kai_ch_chen)

[05/29/26](https://www.threads.com/@kai_ch_chen/post/DY7E3oSmqtm)

今天opus 4.8推出新功能 Claude Code Workflow 但你的跟我的一樣嗎？

乍看大家都有超棒團隊可以用，但實際上⋯ 它是已存的 subagent / skill 上編排；所以當你的基本功夫越好，workflow的效果也越好￼

底層機制（Anthropic 官方）： • Workflow = Claude 即時寫的 JS 腳本 • 同一句「audit API」,根據你的 codebase 寫出不同編排 • subagent 一律 acceptEdits + 繼承 allowlist • 同時 16 隻 / 單次 1000 隻上限

3 件你能做: 1️⃣ /workflows 按 s 存成 /<name> 重跑 2️⃣ 路徑 .claude/workflows/ 或 ~/ 3️⃣ 弱 stage 換小 model 控成本

#ClaudeCode #AIWorkflow #VibeCoding

![Image 2](https://scontent-atl3-1.cdninstagram.com/v/t51.82787-15/708436994_17967927015115625_4354799560386143001_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=106&ig_cache_key=MzkwNzczNzUwOTI3MDkwNTUzOA%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0ueHBpZHMuMTA4MC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=DmQm2YGkwvYQ7kNvwET2hMp&_nc_oc=Adr9ZRi9x0LiCm3VhU8y9BeFXzYqenX30_hKqTArVOyPe0oXPs8ZPjuTUh30lPZg6As&_nc_zt=23&_nc_ht=scontent-atl3-1.cdninstagram.com&_nc_gid=EaO8cEGenKVLaXrfNWpwRA&_nc_ss=7b289&oh=00_AQMmoWzjRS8hHTPVYjnQG5j5LkUZChqheAztxwBIc2kE1w&oe=6ACD18DC)

![Image 3](https://scontent-atl3-2.cdninstagram.com/v/t51.82787-15/710423704_17967927042115625_806239602093737943_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=111&ig_cache_key=MzkwNzczNzUwOTkyNTYwOTk1OA%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0ueHBpZHMuMTA4MC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=sIUzF4yA_YkQ7kNvwEdLvft&_nc_oc=AdqBpaEq00s6Hppa4nH8Q18eB_Cz_gKnUyD_b-EUXDwd5AVrpHoBLi1g7W9QYK3p-CA&_nc_zt=23&_nc_ht=scontent-atl3-2.cdninstagram.com&_nc_gid=EaO8cEGenKVLaXrfNWpwRA&_nc_ss=7b289&oh=00_AQMGaEng68nvUvJ0DT25Ym7rxhKgDjjxwJYMhODdyNHLWA&oe=6ACD0EFE)

![Image 4](https://scontent-atl3-1.cdninstagram.com/v/t51.82787-15/709266337_17967927027115625_4606066761855847356_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=100&ig_cache_key=MzkwNzczNzUxMDAzNDE2NDI4OA%3D%3D.
```
