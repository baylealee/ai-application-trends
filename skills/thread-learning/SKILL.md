---
name: thread-learning-article
version: "0.1.0"
description: Convert fetched public Threads source records into Traditional Chinese AI workflow learning drafts.
---

# Thread Learning Article Skill

This repo-local skill turns public Threads source records into stable Traditional Chinese learning drafts.

## Contract

When the user provides a Threads single-post URL:

1. Normalize the URL by removing query parameters.
2. Add the canonical URL to `data/pending_threads_urls.txt` if it is not already present.
3. Let `.github/workflows/fetch-threads-artifact.yml` fetch public source text.
4. Build learning drafts with `scripts/build_learning_articles.py`.
5. Commit generated drafts to `data/learning_drafts/` and refresh `data/learning_articles_index.json`.

## Output policy

Generated files are drafts by default. Do not treat them as published editorial content until reviewed.

Each draft must preserve:

- `source_url`
- `source_author`
- `post_id`
- `content_quality`
- `raw_content` excerpt
- `reply_summary_status`

## Quality rules

- If no reliable public text is fetched, do not create a learning article.
- If replies cannot be separated reliably, set `reply_summary_status: unavailable`.
- If reply candidates are available but not guaranteed complete, set `reply_summary_status: partial`.
- Do not invent tools, workflow steps, claims, metrics, or author intent.
- Prefer Traditional Chinese output.
- Keep drafts reviewable and source-grounded.

## Manual invocation

```bash
python scripts/fetch_threads_clean_data.py data/pending_threads_urls.txt --batch --debug > /tmp/threads.json
python scripts/build_learning_articles.py /tmp/threads.json
```

## Promotion rule

A draft may be promoted into the public digest only when:

- the source is relevant to AI application trends,
- the fetched text is medium or strong quality,
- the case contains a concrete workflow or reproducible method,
- the source URL remains attached.
