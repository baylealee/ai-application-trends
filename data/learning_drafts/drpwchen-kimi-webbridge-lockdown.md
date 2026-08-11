---
title: "kimi-webbridge-lockdown｜封鎖 AI 瀏覽器控制擴充存取網銀與信箱"
source_url: "https://github.com/drpwchen/kimi-webbridge-lockdown"
source_author: "drpwchen"
language: "zh-TW"
category: "Security／治理"
tools:
  - "Kimi WebBridge"
  - "Claude in Chrome"
  - "chrome.debugger"
  - "ExtensionSettings.runtime_blocked_hosts"
status: "draft"
content_quality: "source_verified"
generated_at: "2026-08-11T13:01:00Z"
---

# kimi-webbridge-lockdown｜封鎖 AI 瀏覽器控制擴充存取網銀與信箱

> 狀態：Notion MCP 同步草稿。來源已讀 README 與 Notion 每日 AI 學習頁面，尚未實機測試。

## 一句話結論

這個 repo 用瀏覽器 enterprise policy 的 `ExtensionSettings.runtime_blocked_hosts`，把 AI browser-control extension 擋在網銀、券商、Gmail 等高風險 host 之外，同時保留其他網站的自動化能力。

## 這篇在解決什麼問題

AI coding agent 或 browser-control extension 可能透過 `chrome.debugger` API 控制真實瀏覽器。README 指出，若擴充同時持有 `<all_urls>` 類型權限，它可能取得使用者在所有網站的既有登入狀態。一般瀏覽器擴充套件 UI 裡的逐站「網站存取權」主要限制 host permissions，不能完整阻擋 debugger 型擴充。

## 核心工作流

1. 偵測目前安裝的 AI browser-control extensions，特別是持有 `debugger` permission 的擴充。
2. 列出需要保護的 host，例如網銀、券商、Gmail 或公司後台登入頁。
3. 透過 `ExtensionSettings.runtime_blocked_hosts` 合併寫入封鎖清單，不覆蓋既有 policy。
4. 重啟瀏覽器後，檢查 `edge://policy` 或 `chrome://policy`。
5. 實際讓 agent 嘗試 attach 被封鎖 host，確認失敗；再測試未封鎖網站仍可自動化。

## 可以直接複製的做法

- 先用 status 模式做唯讀檢查，不急著寫入 policy。
- host 來源只相信實際登入頁網址列或 repo verified catalog，不靠模型記憶。
- 不用 wildcard 大範圍封鎖，避免誤傷信用卡活動頁、開戶頁或仍想保留自動化的子網域。
- 重要帳號不要和 AI agent 探索未知網頁放在同一個 browser profile。
- 把這個 repo 轉成「AI 瀏覽器自動化安全治理 SOP」。

## 適合誰使用

- 會用 Kimi WebBridge、Claude in Chrome 或類似 browser-control extension 的人
- 想讓 AI agent 操作瀏覽器，但不想讓它碰到網銀、券商、Gmail 的人
- 需要在公司內部建立 AI browser automation 安全邊界的營運、PM 或 IT

## 限制與風險

- 黑名單只會保護列入的 host，新銀行、新券商、新信箱登入 host 要持續補。
- 有本機 admin 權限的人仍可撤銷 policy。
- 這不是 prompt injection 的完整解法；仍應避免在同一個登入 profile 裡讓 agent 瀏覽不可信網站。
- macOS 要確認 policy level 是 `Mandatory`，不是只看 `ExtensionSettings` 有出現在 policy 頁。

## 今日實作

閱讀 README.zh-TW 與 AGENTS.md，確認 Windows Edge／Chrome 與 macOS 的安裝流程；列出自己需要保護的銀行、券商、Gmail 登入 host；先用 status 唯讀檢查，再評估是否在測試瀏覽器 profile 執行。

## 來源

https://github.com/drpwchen/kimi-webbridge-lockdown
