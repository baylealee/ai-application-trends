# Notion MCP Sync Mode

This project uses ChatGPT's Notion MCP connector as the default Notion write path.
No long-lived Notion API token is required for the normal workflow.

## Default workflow

When Baylea submits a source URL in ChatGPT:

1. Normalize the source URL.
2. Check GitHub local data for duplicates:
   - `data/pending_threads_urls.txt`
   - `data/learning_articles_index.json`
   - `data/notion_learning_items.json`
   - `data/digests.json`
3. Search or query Notion database `每日 AI 學習｜Baylea 自我成長` through the Notion MCP connector.
4. Deduplicate Notion records by:
   - primary key: `來源 URL`
   - fallback key: normalized `學習主題`
5. If the source exists in GitHub but not in Notion, create one Notion database row through MCP.
6. If the source exists in Notion but not in GitHub local JSON, update `data/notion_learning_items.json`.
7. If the source is a Threads URL, also append it to `data/pending_threads_urls.txt` unless it is already queued.
8. Commit GitHub-side data changes.

## Why not GitHub Actions Notion sync by default

GitHub Actions cannot use the ChatGPT Notion MCP session. It can only call Notion directly with a `NOTION_TOKEN` secret. Because Baylea does not want a token-based setup, the scheduled Action is intentionally optional and token-gated.

`.github/workflows/sync-notion-learning.yml` will skip Notion sync when `NOTION_TOKEN` is missing and will not fail the workflow.

## Database mapping

Notion database: `每日 AI 學習｜Baylea 自我成長`

Important properties:

- `學習主題` - title
- `來源 URL` - URL, canonical dedupe key
- `日期` - learning date
- `主題分類` - category select
- `狀態` - status
- `難度` - difficulty
- `10 分鐘摘要` - concise summary
- `今日實作` - practical action
- `我的筆記` - longer notes
- `可升級 SOP／Skill` - checkbox

## Safe write policy

- Do not delete Notion pages automatically.
- Do not overwrite a richer Notion page with a thinner GitHub record.
- If two Notion rows share the same `來源 URL`, record them in `data/notion_learning_duplicates.json` for manual review.
- Threads reply summaries are partial unless a dedicated logged-in local parser captures more context.

## Source classification defaults

- Threads public AI workflow cases: `Agent／Workflow`
- GitHub tools for crawling, extraction, or source pipelines: `Web Crawling／資料取得`
- Frontend/UI skills or design repos: `Frontend／UI`
- Software engineering skills, code review, agent skills: `DevTools／軟體工程`
- Notion knowledge workflows: `Notion／知識治理`
- RAG/search/database learning: `RAG／知識檢索`

## Operating instruction for ChatGPT

When Baylea says a URL should be saved or synced:

- Use Notion MCP tools directly for Notion read/write.
- Use GitHub connector for repo updates.
- Treat MCP sync as the source of truth for Notion writes.
- Do not ask Baylea for `NOTION_TOKEN` unless she explicitly wants unattended GitHub Actions sync.
