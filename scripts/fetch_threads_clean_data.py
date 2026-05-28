#!/usr/bin/env python3
"""
Baylea AI Application Trends - Threads Clean Data Fetcher

Purpose:
- Fetch public single Threads pages.
- Try to recover post text from public HTML metadata / embedded JSON.
- Output a conservative JSON payload for the AI source extractor.

Important:
- This script is for public pages only.
- Do not use Meta / Facebook / Instagram credentials.
- Do not attempt to access private groups, private posts, or content behind login walls.
- If clear post text cannot be recovered, return status=need_context rather than guessing.

Usage:
  python scripts/fetch_threads_clean_data.py "https://www.threads.com/@techtip_s/post/DY3If9hj1jA"
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from typing import Any, Dict, Iterable, List, Optional

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}


TEXT_KEYS = {
    "caption",
    "text",
    "description",
    "og:description",
    "message",
    "body",
    "title",
}


def normalize_url(url: str) -> str:
    """Normalize Threads URL enough for source storage."""
    url = url.strip()
    url = url.replace("https://www.threads.net/", "https://www.threads.com/")
    return url


def extract_author_from_url(url: str) -> str:
    match = re.search(r"/@([^/]+)/", url)
    return match.group(1) if match else "unknown"


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = value.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
    value = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def get_meta_content(soup: BeautifulSoup, *, property_name: str | None = None, name: str | None = None) -> str:
    attrs: Dict[str, str] = {}
    if property_name:
        attrs["property"] = property_name
    if name:
        attrs["name"] = name
    tag = soup.find("meta", attrs=attrs)
    if not tag:
        return ""
    return clean_text(tag.get("content", ""))


def candidate_meta_texts(soup: BeautifulSoup) -> List[Dict[str, str]]:
    candidates = []
    meta_fields = [
        ("og:title", "property"),
        ("og:description", "property"),
        ("twitter:title", "name"),
        ("twitter:description", "name"),
        ("description", "name"),
    ]
    for key, attr_type in meta_fields:
        text = get_meta_content(
            soup,
            property_name=key if attr_type == "property" else None,
            name=key if attr_type == "name" else None,
        )
        if text:
            candidates.append({"source": key, "text": text})
    return candidates


def iter_json_objects(obj: Any) -> Iterable[Any]:
    """Yield all nested JSON-ish objects/lists."""
    yield obj
    if isinstance(obj, dict):
        for value in obj.values():
            yield from iter_json_objects(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_json_objects(item)


def extract_texts_from_json(obj: Any) -> List[str]:
    texts: List[str] = []
    for node in iter_json_objects(obj):
        if isinstance(node, dict):
            # Common Threads pattern: caption: { text: "..." }
            caption = node.get("caption")
            if isinstance(caption, dict) and isinstance(caption.get("text"), str):
                texts.append(clean_text(caption["text"]))

            for key, value in node.items():
                if key in TEXT_KEYS and isinstance(value, str):
                    texts.append(clean_text(value))
    return [t for t in texts if t]


def candidate_script_texts(soup: BeautifulSoup) -> List[Dict[str, str]]:
    candidates: List[Dict[str, str]] = []

    for script in soup.find_all("script"):
        raw = script.string or script.get_text() or ""
        if not raw:
            continue

        script_type = (script.get("type") or "").lower()

        # Strategy 1: Parse clean JSON / JSON-LD.
        if "json" in script_type:
            try:
                parsed = json.loads(raw)
                for text in extract_texts_from_json(parsed):
                    candidates.append({"source": script_type or "application/json", "text": text})
            except Exception:
                pass

        # Strategy 2: Regex fallback for embedded caption text.
        if "caption" in raw or "og:description" in raw or "description" in raw:
            patterns = [
                r'"caption"\s*:\s*\{\s*"text"\s*:\s*"((?:\\.|[^"\\])*)"',
                r'"text"\s*:\s*"((?:\\.|[^"\\]){20,})"',
                r'"description"\s*:\s*"((?:\\.|[^"\\]){20,})"',
            ]
            for pattern in patterns:
                for match in re.findall(pattern, raw):
                    try:
                        decoded = bytes(match, "utf-8").decode("unicode_escape")
                    except Exception:
                        decoded = match
                    decoded = clean_text(decoded)
                    if decoded:
                        candidates.append({"source": "script_regex", "text": decoded})

    return candidates


def score_text(text: str) -> int:
    """Heuristic score: longer, Traditional Chinese, AI/workflow terms rank higher."""
    if not text:
        return 0
    score = min(len(text), 500)
    keywords = [
        "AI",
        "Claude",
        "ChatGPT",
        "Gemini",
        "RAG",
        "MCP",
        "工作流",
        "自動化",
        "流程",
        "prompt",
        "任務",
        "工具",
        "記憶",
        "知識庫",
        "會議",
        "Google",
        "Sheet",
        "Notion",
    ]
    for kw in keywords:
        if kw.lower() in text.lower():
            score += 100
    # Prefer actual post-length content over generic meta title.
    if len(text) > 80:
        score += 200
    return score


def pick_best_text(candidates: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    cleaned: List[Dict[str, str]] = []
    seen = set()
    for item in candidates:
        text = clean_text(item.get("text", ""))
        if len(text) < 15:
            continue
        if text in seen:
            continue
        seen.add(text)
        cleaned.append({"source": item.get("source", "unknown"), "text": text})

    if not cleaned:
        return None

    cleaned.sort(key=lambda x: score_text(x["text"]), reverse=True)
    return cleaned[0]


def fetch_threads_clean_data(url: str, timeout: int = 12) -> Dict[str, Any]:
    url = normalize_url(url)
    author = extract_author_from_url(url)

    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc),
            "source_author": author,
            "source_url": url,
        }

    if response.status_code != 200:
        return {
            "status": "error",
            "message": f"HTTP {response.status_code}",
            "source_author": author,
            "source_url": url,
        }

    soup = BeautifulSoup(response.text, "html.parser")
    candidates = candidate_script_texts(soup) + candidate_meta_texts(soup)
    best = pick_best_text(candidates)

    if not best:
        return {
            "status": "need_context",
            "message": "Unable to recover clear post text from public HTML metadata or embedded JSON.",
            "source_author": author,
            "source_url": url,
            "raw_content": "",
            "candidates": candidates[:5],
        }

    return {
        "status": "success",
        "source_author": author,
        "source_url": url,
        "extraction_source": best["source"],
        "raw_content": best["text"],
        "candidate_count": len(candidates),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch public Threads post text from metadata / embedded JSON.")
    parser.add_argument("url", help="Single Threads post URL")
    parser.add_argument("--timeout", type=int, default=12)
    args = parser.parse_args()

    result = fetch_threads_clean_data(args.url, timeout=args.timeout)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
