#!/usr/bin/env python3
"""
Baylea AI Application Trends - Threads Clean Data Fetcher v3

Public-source extractor for Threads single-post URLs.
- First tries direct public HTML metadata / embedded JSON.
- If weak, tries public reader fallbacks.
- No credentials, no cookies, no private groups, no login-wall access.
- If clear post text cannot be recovered, returns need_context.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from typing import Any, Dict, Iterable, List
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 Chrome/123 Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

TEXT_KEYS = {"caption", "text", "description", "message", "body", "title", "name", "content", "headline"}
AI_WORDS = [
    "AI", "Claude", "ChatGPT", "GPT", "Gemini", "RAG", "MCP", "OpenClaw", "龍蝦",
    "NotebookLM", "n8n", "Dify", "Make", "Apps Script", "Google Sheet", "Cursor", "Qwen",
    "Codex", "Agent", "agent", "工作流", "自動化", "流程", "prompt", "提示詞", "工具",
    "記憶", "知識庫", "會議", "摘要", "整理", "生成", "設計", "小工具", "CRM", "Gmail",
    "Slack", "Notion", "GitHub", "Vercel", "開源", "CLI", "workflow",
]
BLOCKS = ["Log in", "登入", "Sign up", "註冊", "Threads 上的貼文", "查看更多", "Create an account"]


def normalize_url(url: str) -> str:
    url = url.strip().replace("https://www.threads.net/", "https://www.threads.com/")
    return re.sub(r"\?.*$", "", url)


def author_from_url(url: str) -> str:
    m = re.search(r"/@([^/]+)/", url)
    return m.group(1) if m else "unknown"


def clean(text: str) -> str:
    text = html.unescape(text or "")
    text = text.replace("\\/", "/")
    text = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), text)
    text = text.replace("\\n", "\n").replace("\\t", "\t")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def json_decode(value: str) -> str:
    try:
        return json.loads(f'"{value}"')
    except Exception:
        return value


def walk(obj: Any) -> Iterable[Any]:
    yield obj
    if isinstance(obj, dict):
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk(item)


def json_texts(obj: Any, prefix: str) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for node in walk(obj):
        if not isinstance(node, dict):
            continue
        cap = node.get("caption")
        if isinstance(cap, dict) and isinstance(cap.get("text"), str):
            out.append({"source": f"{prefix}.caption.text", "text": clean(cap["text"])})
        for k, v in node.items():
            if k in TEXT_KEYS and isinstance(v, str):
                out.append({"source": f"{prefix}.{k}", "text": clean(v)})
    return [x for x in out if x["text"]]


def html_candidates(html_text: str, prefix: str) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html_text, "html.parser")
    out: List[Dict[str, str]] = []

    for key, attr in [("og:title", "property"), ("og:description", "property"), ("twitter:title", "name"), ("twitter:description", "name"), ("description", "name")]:
        tag = soup.find("meta", attrs={attr: key})
        if tag and tag.get("content"):
            out.append({"source": f"{prefix}.{key}", "text": clean(tag.get("content", ""))})

    for script in soup.find_all("script"):
        raw = script.string or script.get_text() or ""
        if not raw:
            continue
        if "json" in (script.get("type") or "").lower():
            try:
                out.extend(json_texts(json.loads(raw), f"{prefix}.json"))
            except Exception:
                pass
        for pat in [
            r'"caption"\s*:\s*\{\s*"text"\s*:\s*"((?:\\.|[^"\\])*)"',
            r'"text"\s*:\s*"((?:\\.|[^"\\]){20,})"',
            r'"description"\s*:\s*"((?:\\.|[^"\\]){20,})"',
            r'"message"\s*:\s*"((?:\\.|[^"\\]){20,})"',
        ]:
            for m in re.findall(pat, raw):
                out.append({"source": f"{prefix}.regex", "text": clean(json_decode(m))})

    body = clean(soup.get_text("\n", strip=True))
    for chunk in [clean(x) for x in re.split(r"\n{2,}", body)]:
        if len(chunk) >= 40:
            out.append({"source": f"{prefix}.body_chunk", "text": chunk})
    return out


def hits(text: str) -> List[str]:
    low = text.lower()
    return [w for w in AI_WORDS if w.lower() in low]


def quality(text: str) -> Dict[str, Any]:
    text = clean(text)
    h = hits(text)
    blocked = any(b.lower() in text.lower() for b in BLOCKS)
    if not text or len(text) < 20 or (blocked and not h):
        return {"content_quality": "need_context", "source_level_hint": "need_context", "keyword_hits": h}
    if len(text) >= 80 and len(h) >= 2:
        return {"content_quality": "strong", "source_level_hint": "A_or_B_candidate", "keyword_hits": h}
    if len(text) >= 50 and len(h) >= 1:
        return {"content_quality": "medium", "source_level_hint": "B_candidate", "keyword_hits": h}
    return {"content_quality": "weak", "source_level_hint": "need_context", "keyword_hits": h}


def score(text: str) -> int:
    q = quality(text)
    s = min(len(text), 900) + len(q["keyword_hits"]) * 140
    if q["content_quality"] == "strong":
        s += 600
    elif q["content_quality"] == "medium":
        s += 250
    elif q["content_quality"] == "weak":
        s -= 100
    return s


def clean_candidates(items: List[Dict[str, str]], debug: bool) -> List[Dict[str, Any]]:
    seen = set()
    out: List[Dict[str, Any]] = []
    for item in items:
        text = clean(item.get("text", ""))
        if len(text) < 15:
            continue
        key = re.sub(r"\s+", " ", text)[:500]
        if key in seen:
            continue
        seen.add(key)
        q = quality(text)
        out.append({"source": item.get("source", "unknown"), "text": text if debug else text[:420], "score": score(text), **q})
    out.sort(key=lambda x: x["score"], reverse=True)
    return out


def result(url: str, candidates: List[Dict[str, Any]], method: str, notes: List[str], debug: bool) -> Dict[str, Any]:
    author = author_from_url(url)
    if not candidates:
        return {"status": "need_context", "source_level_hint": "need_context", "content_quality": "need_context", "source_author": author, "source_url": url, "extraction_method": method, "fetch_notes": notes, "raw_content": "", "candidate_count": 0, "candidates": []}
    best = candidates[0]
    q = best.get("content_quality", "need_context")
    return {"status": "success" if q in {"strong", "medium"} else "weak_content", "source_level_hint": best.get("source_level_hint"), "content_quality": q, "keyword_hits": best.get("keyword_hits", []), "source_author": author, "source_url": url, "extraction_method": method, "fetch_notes": notes, "extraction_source": best.get("source"), "raw_content": best.get("text", ""), "candidate_count": len(candidates), "candidates": candidates[:12] if debug else candidates[:5]}


def fetch_direct(url: str, timeout: int, debug: bool) -> Dict[str, Any]:
    notes: List[str] = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        notes.append(f"status={r.status_code}")
        if r.status_code != 200:
            return result(url, [], "direct", notes, debug)
        c = clean_candidates(html_candidates(r.text, "direct"), debug)
        return result(url, c, "direct", notes, debug)
    except Exception as e:
        return result(url, [], "direct_error", [str(e)], debug)


def reader_urls(url: str) -> List[str]:
    return [
        "https://r.jina.ai/http://r.jina.ai/http://" + url,
        "https://r.jina.ai/http://r.jina.ai/http://" + url.replace("https://", "http://"),
        "https://r.jina.ai/http://r.jina.ai/http://" + quote(url, safe=":/"),
    ]


def fetch_reader(url: str, timeout: int, debug: bool) -> Dict[str, Any]:
    notes: List[str] = []
    all_items: List[Dict[str, str]] = []
    for ru in reader_urls(url):
        try:
            r = requests.get(ru, headers=HEADERS, timeout=timeout)
            notes.append(f"reader_status={r.status_code}")
            if r.status_code == 200 and r.text:
                text = clean(r.text)
                all_items.append({"source": "reader.text", "text": text})
                all_items.extend(html_candidates(r.text, "reader"))
        except Exception as e:
            notes.append(f"reader_error={e}")
    c = clean_candidates(all_items, debug)
    return result(url, c, "reader_fallback", notes, debug)


def rank(q: str) -> int:
    return {"strong": 3, "medium": 2, "weak": 1, "need_context": 0}.get(q, 0)


def fetch_threads_clean_data(url: str, timeout: int = 18, debug: bool = False) -> Dict[str, Any]:
    url = normalize_url(url)
    direct = fetch_direct(url, timeout, debug)
    if direct.get("status") == "success":
        return direct
    reader = fetch_reader(url, timeout, debug)
    if rank(reader.get("content_quality")) >= rank(direct.get("content_quality")):
        reader["fallback_from"] = {k: direct.get(k) for k in ["status", "content_quality", "candidate_count", "fetch_notes"]}
        return reader
    direct["fallback_attempt"] = {k: reader.get(k) for k in ["status", "content_quality", "candidate_count", "fetch_notes"]}
    return direct


def read_urls(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [normalize_url(line) for line in f if line.strip() and not line.strip().startswith("#")]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("target")
    p.add_argument("--timeout", type=int, default=18)
    p.add_argument("--debug", action="store_true")
    p.add_argument("--batch", action="store_true")
    args = p.parse_args()
    if args.batch:
        print(json.dumps([fetch_threads_clean_data(u, args.timeout, args.debug) for u in read_urls(args.target)], ensure_ascii=False, indent=2))
    else:
        print(json.dumps(fetch_threads_clean_data(args.target, args.timeout, args.debug), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
