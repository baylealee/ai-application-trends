#!/usr/bin/env python3
"""Find public Threads candidate post URLs for Traditional Chinese AI workflow sharing.

This does not log in and does not use private APIs. It builds public Threads search URLs,
reads public search pages through reader mirrors when available, extracts single-post URLs,
and filters/ranks candidates by Traditional Chinese text signals and AI workflow terms.
"""

from __future__ import annotations

import argparse
import json
import re
from typing import Dict, List
from urllib.parse import quote

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 Chrome/123 Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}

DEFAULT_TERMS = [
    "ClaudeCode 分享",
    "Claude Code 分享",
    "ClaudeCode 教學",
    "Claude Code 教學",
    "ClaudeCode 工作流",
    "Claude Code 工作流",
    "ClaudeCode 實測",
    "Claude Code 實測",
    "ClaudeCode 台灣",
    "Claude Code 繁中",
]

AI_TERMS = ["Claude", "ClaudeCode", "Claude Code", "AI", "工作流", "自動化", "教學", "實測", "分享", "工具", "提示詞", "MCP", "Agent", "Code"]
TW_TERMS = ["分享", "教學", "實測", "台灣", "繁中", "中文", "工作流", "整理", "工具", "用法", "心得", "筆記"]
TRADITIONAL_ONLY = set("體關開發應學實測據雲電腦資料寫程碼這個為與會後對變圖臺灣繁體標籤選擇推薦")


def clean_url(url: str) -> str:
    url = url.strip().replace("https://www.threads.net/", "https://www.threads.com/")
    return re.sub(r"\?.*$", "", url)


def threads_search_url(term: str) -> str:
    return f"https://www.threads.com/search?q={quote(term)}&serp_type=tags&hl=zh-tw"


def reader_url(url: str) -> str:
    return "https://r.jina.ai/http://r.jina.ai/http://" + url


def fetch_text(url: str, timeout: int) -> str:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        if r.status_code == 200:
            return r.text or ""
    except Exception:
        return ""
    return ""


def extract_post_urls(text: str) -> List[str]:
    urls = set()
    patterns = [
        r"https://www\.threads\.com/@[^\s\)\]\}\"'<>]+/post/[A-Za-z0-9_-]+",
        r"https://www\.threads\.net/@[^\s\)\]\}\"'<>]+/post/[A-Za-z0-9_-]+",
        r"/@[A-Za-z0-9._-]+/post/[A-Za-z0-9_-]+",
    ]
    for pattern in patterns:
        for m in re.findall(pattern, text):
            if m.startswith("/@"):
                m = "https://www.threads.com" + m
            urls.add(clean_url(m))
    return sorted(urls)


def zh_ratio(text: str) -> float:
    if not text:
        return 0.0
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    return cjk / max(len(text), 1)


def score_context(text: str, url: str) -> int:
    ctx = text[:4000]
    score = 0
    score += int(zh_ratio(ctx) * 1000)
    score += sum(80 for term in AI_TERMS if term.lower() in ctx.lower())
    score += sum(60 for term in TW_TERMS if term in ctx)
    score += sum(8 for ch in TRADITIONAL_ONLY if ch in ctx)
    if "meta.ai" in url.lower():
        score -= 300
    if "登入" in ctx and zh_ratio(ctx) < 0.05:
        score -= 200
    return score


def search_candidates(terms: List[str], timeout: int, max_results: int) -> Dict:
    seen = set()
    candidates = []
    debug_pages = []

    for term in terms:
        page_url = threads_search_url(term)
        texts = []
        direct = fetch_text(page_url, timeout)
        reader = fetch_text(reader_url(page_url), timeout)
        texts.append(("direct", direct))
        texts.append(("reader", reader))
        debug_pages.append({"term": term, "url": page_url, "direct_len": len(direct), "reader_len": len(reader)})

        combined = "\n".join([t for _, t in texts if t])
        for post_url in extract_post_urls(combined):
            if post_url in seen:
                continue
            seen.add(post_url)
            # Use nearby text as context when possible.
            idx = combined.find(post_url)
            context = combined[max(0, idx - 500): idx + 1200] if idx >= 0 else combined[:1800]
            candidates.append({
                "source_url": post_url,
                "matched_term": term,
                "score": score_context(context, post_url),
                "zh_ratio": round(zh_ratio(context), 4),
                "context_preview": re.sub(r"\s+", " ", context).strip()[:500],
            })

    candidates.sort(key=lambda x: x["score"], reverse=True)
    return {
        "status": "success",
        "strategy": "threads_search_zh_tw_plus_post_filter",
        "note": "hl=zh-tw localizes UI only; this script ranks by Traditional Chinese and AI workflow terms after extracting public post URLs.",
        "query_terms": terms,
        "candidate_count": len(candidates),
        "candidates": candidates[:max_results],
        "debug_pages": debug_pages,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", action="append", help="Custom search term. Can be repeated.")
    parser.add_argument("--timeout", type=int, default=18)
    parser.add_argument("--max-results", type=int, default=30)
    args = parser.parse_args()
    terms = args.query if args.query else DEFAULT_TERMS
    print(json.dumps(search_candidates(terms, args.timeout, args.max_results), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
