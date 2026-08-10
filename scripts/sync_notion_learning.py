#!/usr/bin/env python3
"""Two-way sync helper for Baylea's Notion daily AI learning database.

What it does:
1. Pulls rows from Notion「每日 AI 學習」into data/notion_learning_items.json.
2. Reads local learning sources from:
   - data/learning_articles_index.json
   - data/digests.json
   - data/pending_threads_urls.txt
3. Deduplicates both sides by canonical source_url, falling back to normalized title.
4. Optionally creates missing local learning items in Notion.

Required for Notion API mode:
- NOTION_TOKEN
- NOTION_LEARNING_DATABASE_ID

This script does not delete Notion pages. Duplicate Notion pages are reported in
`data/notion_learning_duplicates.json` for safe manual review.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

DEFAULT_DB_ID = "411f716ad31943f6bfde6cd1d73382a0"
NOTION_VERSION = "2022-06-28"
VALID_CATEGORIES = {
    "Prompt／需求定義",
    "GAS／自動化可靠性",
    "Notion／知識治理",
    "Agent／Workflow",
    "資料分析／Insight",
    "AI 產品案例",
    "本週複盤",
    "Security／治理",
    "RAG／知識檢索",
    "Document AI／文件解析",
    "Web Crawling／資料取得",
    "Frontend／UI",
    "DevTools／軟體工程",
    "SEO／GEO／行銷",
}

CATEGORY_MAP = {
    "mcp": "RAG／知識檢索",
    "knowledge_base": "RAG／知識檢索",
    "coding": "DevTools／軟體工程",
    "developer_ops": "DevTools／軟體工程",
    "content_marketing": "SEO／GEO／行銷",
    "productivity": "Agent／Workflow",
    "automation": "Agent／Workflow",
    "ai_workflow": "Agent／Workflow",
    "education_ai": "AI 產品案例",
    "frontend_design": "Frontend／UI",
    "design_ops": "Frontend／UI",
}

GENERIC_URLS = {
    "https://www.threads.com",
    "https://www.threads.com/",
    "https://www.threads.net",
    "https://www.threads.net/",
}


def canonical_url(url: str | None) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    url = url.replace("https://www.threads.net/", "https://www.threads.com/")
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return url.rstrip("/")
    path = parsed.path.rstrip("/")
    return f"{parsed.scheme.lower()}://{parsed.netloc.lower()}{path}"


def normalize_title(title: str | None) -> str:
    text = (title or "").strip().lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[\|｜:：\-—–_]+", "", text)
    return text[:80]


def dedupe_key(item: dict[str, Any]) -> str:
    url = canonical_url(item.get("source_url"))
    if url:
        return f"url:{url}"
    return f"title:{normalize_title(item.get('title'))}"


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def notion_request(token: str, method: str, endpoint: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.notion.com/v1{endpoint}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Notion API {method} {endpoint} failed: {exc.code} {body}") from exc


def rich_text_plain(value: list[dict[str, Any]] | None) -> str:
    return "".join(part.get("plain_text", "") for part in (value or [])).strip()


def title_plain(value: list[dict[str, Any]] | None) -> str:
    return rich_text_plain(value)


def property_text(props: dict[str, Any], name: str) -> str:
    prop = props.get(name) or {}
    typ = prop.get("type")
    if typ == "title":
        return title_plain(prop.get("title"))
    if typ == "rich_text":
        return rich_text_plain(prop.get("rich_text"))
    if typ == "url":
        return prop.get("url") or ""
    if typ == "select":
        return (prop.get("select") or {}).get("name") or ""
    if typ == "status":
        return (prop.get("status") or {}).get("name") or ""
    if typ == "date":
        return (prop.get("date") or {}).get("start") or ""
    if typ == "checkbox":
        return "__YES__" if prop.get("checkbox") else "__NO__"
    if typ == "number":
        value = prop.get("number")
        return "" if value is None else str(value)
    return ""


def notion_page_to_item(page: dict[str, Any]) -> dict[str, Any]:
    props = page.get("properties") or {}
    source_url = canonical_url(property_text(props, "來源 URL"))
    title = property_text(props, "學習主題")
    return {
        "title": title,
        "source_url": source_url,
        "notion_url": page.get("url", ""),
        "notion_page_id": page.get("id", ""),
        "category": property_text(props, "主題分類"),
        "status": property_text(props, "狀態"),
        "difficulty": property_text(props, "難度"),
        "date": property_text(props, "日期"),
        "summary": property_text(props, "10 分鐘摘要"),
        "practice": property_text(props, "今日實作"),
        "notes": property_text(props, "我的筆記"),
        "upgradeable_skill": property_text(props, "可升級 SOP／Skill"),
        "origin": "notion",
    }


def fetch_notion_items(token: str, database_id: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    cursor: str | None = None
    while True:
        payload: dict[str, Any] = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor
        result = notion_request(token, "POST", f"/databases/{database_id}/query", payload)
        items.extend(notion_page_to_item(page) for page in result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    return items


def local_sources_from_learning_index(path: Path) -> list[dict[str, Any]]:
    rows = read_json(path, [])
    out: list[dict[str, Any]] = []
    for row in rows if isinstance(rows, list) else []:
        url = canonical_url(row.get("source_url"))
        if not url or url in GENERIC_URLS:
            continue
        out.append({
            "title": row.get("title") or f"Threads AI 學習｜{row.get('source_author', 'unknown')}",
            "source_url": url,
            "category": CATEGORY_MAP.get(row.get("category", ""), "Agent／Workflow"),
            "status": "待閱讀",
            "difficulty": "實作",
            "date": dt.date.today().isoformat(),
            "summary": row.get("summary") or f"由 Threads 來源自動產生的 AI 學習草稿，content_quality={row.get('content_quality', 'unknown')}。",
            "practice": "閱讀草稿，確認可複製 workflow，必要時補充主文、回覆重點與實作限制。",
            "origin": "github_learning_index",
        })
    return out


def local_sources_from_digests(path: Path) -> list[dict[str, Any]]:
    rows = read_json(path, [])
    out: list[dict[str, Any]] = []
    for row in rows if isinstance(rows, list) else []:
        for source in row.get("sources", []) or []:
            url = canonical_url(source.get("url"))
            if not url or url in GENERIC_URLS:
                continue
            if not ("threads.com" in url or "github.com" in url or "claude" in url or "notion" in url):
                continue
            out.append({
                "title": row.get("title") or source.get("title") or "AI 學習來源",
                "source_url": url,
                "category": CATEGORY_MAP.get((row.get("scene") or [""])[0] if isinstance(row.get("scene"), list) and row.get("scene") else "", "AI 產品案例"),
                "status": "待閱讀",
                "difficulty": "入門",
                "date": row.get("date") or dt.date.today().isoformat(),
                "summary": row.get("summary") or "從公開案例庫同步而來的 AI 學習來源。",
                "practice": row.get("workflow") or "閱讀來源並補成可複製工作流。",
                "origin": "github_digests",
            })
    return out


def local_sources_from_pending(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        url = canonical_url(line)
        if not url:
            continue
        out.append({
            "title": f"Threads 待讀來源｜{urlparse(url).path.split('/post/')[0].replace('/@', '@')}",
            "source_url": url,
            "category": "AI 產品案例",
            "status": "待閱讀",
            "difficulty": "入門",
            "date": dt.date.today().isoformat(),
            "summary": "從 pending_threads_urls.txt 同步而來，等待抓取與整理。",
            "practice": "等待 fetch workflow 抓取正文後，再整理成學習草稿。",
            "origin": "github_pending_threads",
        })
    return out


def collect_local_items(repo_root: Path) -> list[dict[str, Any]]:
    return (
        local_sources_from_learning_index(repo_root / "data/learning_articles_index.json")
        + local_sources_from_digests(repo_root / "data/digests.json")
        + local_sources_from_pending(repo_root / "data/pending_threads_urls.txt")
    )


def merge_deduped(*groups: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_key: dict[str, dict[str, Any]] = {}
    duplicates: list[dict[str, Any]] = []
    for group in groups:
        for item in group:
            key = dedupe_key(item)
            if not key or key == "title:":
                continue
            item = dict(item)
            item["dedupe_key"] = key
            if key in by_key:
                duplicates.append({"dedupe_key": key, "kept": by_key[key], "duplicate": item})
                # Prefer Notion metadata when present, otherwise keep first richer item.
                if item.get("origin") == "notion" and by_key[key].get("origin") != "notion":
                    by_key[key] = {**by_key[key], **item}
            else:
                by_key[key] = item
    return sorted(by_key.values(), key=lambda x: (x.get("date") or "", x.get("title") or ""), reverse=True), duplicates


def rich_text(value: str, limit: int = 1900) -> list[dict[str, Any]]:
    value = (value or "")[:limit]
    return [{"type": "text", "text": {"content": value}}] if value else []


def notion_properties_for(item: dict[str, Any]) -> dict[str, Any]:
    category = item.get("category") or "Agent／Workflow"
    if category not in VALID_CATEGORIES:
        category = CATEGORY_MAP.get(category, "Agent／Workflow")
    props: dict[str, Any] = {
        "學習主題": {"title": rich_text(item.get("title") or "AI 學習來源", 180)},
        "來源 URL": {"url": item.get("source_url")},
        "狀態": {"status": {"name": item.get("status") or "待閱讀"}},
        "主題分類": {"select": {"name": category}},
        "難度": {"select": {"name": item.get("difficulty") or "入門"}},
        "日期": {"date": {"start": item.get("date") or dt.date.today().isoformat()}},
        "10 分鐘摘要": {"rich_text": rich_text(item.get("summary") or "")},
        "今日實作": {"rich_text": rich_text(item.get("practice") or "")},
        "可升級 SOP／Skill": {"checkbox": False},
    }
    return props


def create_missing_in_notion(token: str, database_id: str, local_items: list[dict[str, Any]], notion_items: list[dict[str, Any]], limit: int) -> int:
    notion_keys = {dedupe_key(item) for item in notion_items}
    created = 0
    for item in local_items:
        if created >= limit:
            break
        if dedupe_key(item) in notion_keys:
            continue
        if not item.get("source_url"):
            continue
        payload = {"parent": {"database_id": database_id}, "properties": notion_properties_for(item)}
        notion_request(token, "POST", "/pages", payload)
        notion_keys.add(dedupe_key(item))
        created += 1
    return created


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default="data/notion_learning_items.json")
    parser.add_argument("--duplicates-out", default="data/notion_learning_duplicates.json")
    parser.add_argument("--push-to-notion", action="store_true")
    parser.add_argument("--create-limit", type=int, default=25)
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    token = os.getenv("NOTION_TOKEN", "").strip()
    database_id = os.getenv("NOTION_LEARNING_DATABASE_ID", DEFAULT_DB_ID).strip().replace("-", "")

    notion_items: list[dict[str, Any]] = []
    if token:
        notion_items = fetch_notion_items(token, database_id)
    else:
        print("NOTION_TOKEN not set; syncing local GitHub sources only.", file=sys.stderr)

    local_items = collect_local_items(repo_root)
    merged, duplicates = merge_deduped(notion_items, local_items)

    created = 0
    if token and args.push_to_notion:
        created = create_missing_in_notion(token, database_id, local_items, notion_items, args.create_limit)
        if created:
            notion_items = fetch_notion_items(token, database_id)
            merged, duplicates = merge_deduped(notion_items, local_items)

    write_json(repo_root / args.out, merged)
    write_json(repo_root / args.duplicates_out, duplicates)
    print(json.dumps({
        "notion_items": len(notion_items),
        "local_items": len(local_items),
        "merged_items": len(merged),
        "duplicates": len(duplicates),
        "created_in_notion": created,
        "out": args.out,
        "duplicates_out": args.duplicates_out,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
