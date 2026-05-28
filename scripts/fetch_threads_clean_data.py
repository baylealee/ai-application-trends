#!/usr/bin/env python3
"""
Baylea AI Application Trends - Threads Clean Data Fetcher v2

Purpose:
- Fetch public single Threads pages.
- Recover post text from public HTML metadata / embedded JSON.
- Output a conservative JSON payload for the AI source extractor.

Important:
- Public pages only.
- Do not use Meta / Facebook / Instagram credentials.
- Do not access private groups, private posts, or content behind login walls.
- If clear post text cannot be recovered, return status=need_context rather than guessing.

Usage:
  python scripts/fetch_threads_clean_data.py "https://www.threads.com/@techtip_s/post/DY3If9hj1jA"
  python scripts/fetch_threads_clean_data.py urls.txt --batch --debug
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
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

TEXT_KEYS = {
    "caption",
    "text",
    "description",
    "og:description",
    "message",
    "body",
    "title",
    "name",
}

AI_WORKFLOW_KEYWORDS = [
    "AI", "Claude", "ChatGPT", "GPT", "Gemini", "RAG", "MCP", "OpenClaw", "龍蝦",
    "NotebookLM", "n8n", "Dify", "Make", "Apps Script", "Google Sheet", "Cursor",
    "Qwen", "Codex", "agent", "Agent", "工作流", "自動化", "流程", "prompt", "提示詞",
    "任務", "工具", "記憶", "知識庫", "會議", "摘要", "整理", "生成", "設計", "小工具",
    "表單", "CRM", "Gmail", "Slack", "Notion", "GitHub", "Vercel",
]

GENERIC_BLOCKLIST = [
    "Log in", "登入", "Sign up", "註冊", "Threads 上的貼文", "查看更多", "Meta", "Instagram",
    "This content isn't available", "此內容無法使用", "請先登入", "Create an account",
]


def normalize_url(url: str) -> str:
    url = url.strip()
    url = url.replace("https://www.threads.net/", "https://www.threads.com/")
    return url


def extract_author_from_url(url: str) -> str:
    match = re.search(r"/@([^/]+)/", url)
    return match.group(1) if match else "unknown"


def safe_json_string_decode(value: str) -> str:
    """Decode JSON string escapes without corrupting Chinese / emoji."""
    if not value:
        return ""
    try:
        return json.loads(f'"{value}"')
    except Exception:
        pass
    try:
        return bytes(value, "utf-8").decode("unicode_escape")
    except Exception:
        return value


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = value.replace("\\/", "/")
    value = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), value)
    value = value.replace("\\n", "\n").replace("\\t", "\t")
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def compact_for_debug(text: str, limit: int = 320) -> str:
    text = clean_text(text).replace("\n", " ")
    return text if len(text) <= limit else text[:limit] + "..."


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
    candidates: List[Dict[str, str]] = []
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
    yield obj
    if isinstance(obj, dict):
        for value in obj.values():
            yield from iter_json_objects(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_json_objects(item)


def extract_texts_from_json(obj: Any) -> List[Dict[str, str]]:
    results: List[Dict[str, str]] = []
    for node in iter_json_objects(obj):
        if not isinstance(node, dict):
            continue

        caption = node.get("caption")
        if isinstance(caption, dict) and isinstance(caption.get("text"), str):
            results.append({"source": "json.caption.text", "text": clean_text(caption["text"])})

        for key, value in node.items():
            if key in TEXT_KEYS and isinstance(value, str):
                results.append({"source": f"json.{key}", "text": clean_text(value)})
    return [r for r in results if r["text"]]


def candidate_script_texts(soup: BeautifulSoup) -> List[Dict[str, str]]:
    candidates: List[Dict[str, str]] = []

    for script in soup.find_all("script"):
        raw = script.string or script.get_text() or ""
        if not raw:
            continue

        script_type = (script.get("type") or "").lower()

        if "json" in script_type:
            try:
                parsed = json.loads(raw)
                candidates.extend(extract_texts_from_json(parsed))
            except Exception:
                pass

        if any(token in raw for token in ["caption", "description", "text", "__bbox", "__spin"]):
            patterns = [
                r'"caption"\s*:\s*\{\s*"text"\s*:\s*"((?:\\.|[^"\\])*)"',
                r'"text"\s*:\s*"((?:\\.|[^"\\]){20,})"',
                r'"description"\s*:\s*"((?:\\.|[^"\\]){20,})"',
                r'"message"\s*:\s*"((?:\\.|[^"\\]){20,})"',
            ]
            for pattern in patterns:
                for match in re.findall(pattern, raw):
                    decoded = clean_text(safe_json_string_decode(match))
                    if decoded:
                        candidates.append({"source": "script_regex", "text": decoded})

    return candidates


def has_blocked_generic_text(text: str) -> bool:
    normalized = text.lower()
    return any(block.lower() in normalized for block in GENERIC_BLOCKLIST)


def ai_keyword_hits(text: str) -> List[str]:
    normalized = text.lower()
    hits = []
    for keyword in AI_WORKFLOW_KEYWORDS:
        if keyword.lower() in normalized:
            hits.append(keyword)
    return hits


def quality_for_text(text: str) -> Dict[str, Any]:
    text = clean_text(text)
    hits = ai_keyword_hits(text)
    blocked = has_blocked_generic_text(text)

    if not text or len(text) < 20:
        return {"content_quality": "need_context", "source_level_hint": "need_context", "keyword_hits": hits}

    if blocked and len(hits) == 0:
        return {"content_quality": "need_context", "source_level_hint": "need_context", "keyword_hits": hits}

    if len(text) >= 80 and len(hits) >= 2:
        return {"content_quality": "strong", "source_level_hint": "A_or_B_candidate", "keyword_hits": hits}

    if len(text) >= 50 and len(hits) >= 1:
        return {"content_quality": "medium", "source_level_hint": "B_candidate", "keyword_hits": hits}

    return {"content_quality": "weak", "source_level_hint": "need_context", "keyword_hits": hits}


def score_text(text: str) -> int:
    if not text:
        return 0
    quality = quality_for_text(text)
    score = min(len(text), 700)
    score += len(quality["keyword_hits"]) * 120
    if quality["content_quality"] == "strong":
        score += 500
    elif quality["content_quality"] == "medium":
        score += 250
    elif quality["content_quality"] == "weak":
        score -= 100
    if has_blocked_generic_text(text):
        score -= 300
    return score


def clean_candidates(candidates: List[Dict[str, str]], debug: bool = False) -> List[Dict[str, Any]]:
    cleaned: List[Dict[str, Any]] = []
    seen = set()

    for item in candidates:
        text = clean_text(item.get("text", ""))
        if len(text) < 15:
            continue
        if text in seen:
            continue
        seen.add(text)

        quality = quality_for_text(text)
        entry: Dict[str, Any] = {
            "source": item.get("source", "unknown"),
            "text": text if debug else compact_for_debug(text),
            "score": score_text(text),
            **quality,
        }
        cleaned.append(entry)

    cleaned.sort(key=lambda x: x["score"], reverse=True)
    return cleaned


def pick_best_text(candidates: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
    cleaned = clean_candidates(candidates, debug=True)
    return cleaned[0] if cleaned else None


def fetch_threads_clean_data(url: str, timeout: int = 12, debug: bool = False) -> Dict[str, Any]:
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
    raw_candidates = candidate_script_texts(soup) + candidate_meta_texts(soup)
    candidates = clean_candidates(raw_candidates, debug=debug)
    best = candidates[0] if candidates else None

    if not best:
        return {
            "status": "need_context",
            "source_level_hint": "need_context",
            "content_quality": "need_context",
            "message": "Unable to recover clear post text from public HTML metadata or embedded JSON.",
            "source_author": author,
            "source_url": url,
            "raw_content": "",
            "candidates": [],
        }

    quality = best.get("content_quality", "need_context")
    if quality in {"strong", "medium"}:
        status = "success"
    else:
        status = "weak_content"

    return {
        "status": status,
        "source_level_hint": best.get("source_level_hint", "need_context"),
        "content_quality": quality,
        "keyword_hits": best.get("keyword_hits", []),
        "source_author": author,
        "source_url": url,
        "extraction_source": best.get("source", "unknown"),
        "raw_content": best.get("text", ""),
        "candidate_count": len(candidates),
        "candidates": candidates[:10] if debug else candidates[:5],
    }


def read_urls_from_file(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch public Threads post text from metadata / embedded JSON.")
    parser.add_argument("target", help="Single Threads post URL, or a text file of URLs when --batch is used")
    parser.add_argument("--timeout", type=int, default=12)
    parser.add_argument("--debug", action="store_true", help="Return full candidate texts for debugging")
    parser.add_argument("--batch", action="store_true", help="Treat target as a newline-delimited URL file")
    args = parser.parse_args()

    if args.batch:
        urls = read_urls_from_file(args.target)
        results = [fetch_threads_clean_data(url, timeout=args.timeout, debug=args.debug) for url in urls]
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    result = fetch_threads_clean_data(args.target, timeout=args.timeout, debug=args.debug)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
