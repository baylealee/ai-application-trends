#!/usr/bin/env python3
"""Build learning-article Markdown drafts from fetched Threads source JSON.

This is intentionally deterministic and repo-local. It does not call an LLM.
The goal is to turn fetched source records into stable draft files that can be
reviewed, edited, or later promoted into the public digest.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List
from urllib.parse import urlparse

ZH_RE = re.compile(r"[\u4e00-\u9fff]")
POST_RE = re.compile(r"/@([^/]+)/post/([^/?#]+)")
TOOL_WORDS = [
    "Claude", "Claude Code", "ChatGPT", "GPT", "Gemini", "NotebookLM", "Manus",
    "MCP", "RAG", "Dify", "n8n", "Make", "Zapier", "Notion", "Slack", "Gmail",
    "Google Sheet", "Google Sheets", "Apps Script", "GAS", "Cursor", "Codex",
    "GitHub", "Vercel", "OpenClaw", "Qwen", "Perplexity", "Figma", "Canva",
]
WORKFLOW_WORDS = [
    "流程", "工作流", "步驟", "做法", "自動化", "串接", "整理", "摘要", "生成", "分析",
    "搜尋", "拆解", "排程", "輸出", "範本", "提示詞", "prompt", "agent", "Agent",
]
CATEGORY_RULES = [
    ("mcp", ["MCP"]),
    ("knowledge_base", ["RAG", "知識庫", "搜尋", "檢索", "題庫"]),
    ("coding", ["Claude Code", "Codex", "Cursor", "GitHub", "程式", "code", "PR"]),
    ("content_marketing", ["自媒體", "內容", "貼文", "月曆", "行銷", "品牌"]),
    ("productivity", ["生產力", "待辦", "專注", "會議", "摘要", "整理"]),
    ("automation", ["自動化", "n8n", "Make", "Zapier", "GAS", "Apps Script"]),
]


def clean_text(text: str) -> str:
    text = text or ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def canonical_url(url: str) -> str:
    url = (url or "").strip().replace("https://www.threads.net/", "https://www.threads.com/")
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return url
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")


def post_parts(url: str) -> tuple[str, str]:
    m = POST_RE.search(url)
    if not m:
        return "unknown", "unknown"
    return m.group(1), m.group(2)


def slugify(value: str, max_len: int = 90) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return (value[:max_len].strip("-") or "thread-source")


def detect_tools(text: str) -> List[str]:
    found = []
    lower = text.lower()
    for word in TOOL_WORDS:
        if word.lower() in lower and word not in found:
            found.append(word)
    return found


def detect_category(text: str, tools: List[str]) -> str:
    haystack = f"{text}\n{' '.join(tools)}"
    for category, words in CATEGORY_RULES:
        if any(w.lower() in haystack.lower() for w in words):
            return category
    return "ai_workflow"


def zh_ratio(text: str) -> float:
    compact = re.sub(r"\s+", "", text)
    if not compact:
        return 0.0
    return len(ZH_RE.findall(compact)) / max(len(compact), 1)


def sentence_split(text: str) -> List[str]:
    text = clean_text(text)
    if not text:
        return []
    parts = re.split(r"(?<=[。！？!?])\s*|\n+", text)
    out = []
    for part in parts:
        part = clean_text(part)
        if 12 <= len(part) <= 260:
            out.append(part)
    return out


def pick_summary(text: str) -> str:
    sentences = sentence_split(text)
    for s in sentences:
        if any(w.lower() in s.lower() for w in WORKFLOW_WORDS + TOOL_WORDS):
            return s[:180]
    if sentences:
        return sentences[0][:180]
    return clean_text(text)[:180]


def pick_workflow_steps(text: str) -> List[str]:
    sentences = sentence_split(text)
    steps = []
    for s in sentences:
        if any(w.lower() in s.lower() for w in WORKFLOW_WORDS):
            steps.append(s)
        if len(steps) >= 5:
            break
    if not steps and text:
        steps = ["閱讀原文後，先確認它實際解決的工作情境。", "拆出輸入資料、AI 工具、處理步驟與輸出成果。", "再判斷是否能轉成自己的工作流範本。"]
    return steps[:5]


def extract_reply_candidates(record: Dict[str, Any]) -> List[str]:
    # Existing fetcher keeps generic candidates. Until a dedicated reply parser exists,
    # treat non-best candidates as possible public context only, never as complete replies.
    raw = record.get("candidates") or []
    best = clean_text(record.get("raw_content", ""))
    replies: List[str] = []
    for item in raw:
        text = clean_text(str(item.get("text", "")))
        if not text or text == best or len(text) < 30:
            continue
        if text[:160] in best:
            continue
        replies.append(text[:260])
        if len(replies) >= 5:
            break
    return replies


def iter_records(payload: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                yield item
    elif isinstance(payload, dict):
        results = payload.get("results")
        if isinstance(results, list):
            for item in results:
                if isinstance(item, dict):
                    yield item
        else:
            yield payload


def should_build(record: Dict[str, Any]) -> bool:
    status = record.get("status")
    quality = record.get("content_quality")
    text = clean_text(str(record.get("raw_content", "")))
    if status not in {"success", "weak_content"}:
        return False
    if quality not in {"strong", "medium", "weak"}:
        return False
    if len(text) < 40:
        return False
    return True


def markdown_for(record: Dict[str, Any], generated_at: str) -> tuple[str, Dict[str, Any]]:
    source_url = canonical_url(str(record.get("source_url", "")))
    author, post_id = post_parts(source_url)
    raw_content = clean_text(str(record.get("raw_content", "")))
    tools = detect_tools(raw_content)
    category = detect_category(raw_content, tools)
    summary = pick_summary(raw_content)
    steps = pick_workflow_steps(raw_content)
    replies = extract_reply_candidates(record)
    ratio = round(zh_ratio(raw_content), 4)
    keyword_hits = record.get("keyword_hits") or []
    quality = record.get("content_quality", "unknown")
    status = "draft"
    title = f"{author} 的 AI 工作流案例：{summary[:42]}" if summary else f"{author} 的 AI 工作流案例"
    filename = f"{slugify(author)}-{slugify(post_id, 32)}.md"

    frontmatter = {
        "title": title,
        "source_url": source_url,
        "source_author": author,
        "post_id": post_id,
        "language": "zh-TW" if ratio >= 0.2 else "unknown",
        "category": category,
        "tools": tools,
        "status": status,
        "content_quality": quality,
        "zh_ratio": ratio,
        "generated_at": generated_at,
    }

    fm_lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, list):
            fm_lines.append(f"{key}:")
            for item in value:
                fm_lines.append(f"  - {json.dumps(item, ensure_ascii=False)}")
        else:
            fm_lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    fm_lines.append("---")

    step_lines = "\n".join(f"{idx + 1}. {step}" for idx, step in enumerate(steps))
    reply_status = "partial" if replies else "unavailable"
    reply_lines = "\n".join(f"- {r}" for r in replies) if replies else "- 目前公開抓取結果沒有可可靠分離的回覆內容。"
    tools_line = "、".join(tools) if tools else "待人工確認"
    hits_line = "、".join(map(str, keyword_hits)) if keyword_hits else "無"

    md = f"""\n{chr(10).join(fm_lines)}\n\n# {title}\n\n> 狀態：自動草稿。本文由公開 Threads 抓取結果產生，尚未人工校稿。\n\n## 一句話結論\n\n{summary or "待人工補充。"}\n\n## 這篇在解決什麼問題\n\n這篇來源指向一個 AI 應用或工作流案例。根據目前抓到的公開文字，核心價值在於把工具、步驟或方法整理成可重複使用的做法。\n\n## 使用工具\n\n{tools_line}\n\n## 原始工作流拆解\n\n{step_lines}\n\n## 可以直接複製的做法\n\n1. 先確認你的輸入資料是什麼，例如文件、貼文、客戶資料、程式碼或任務描述。\n2. 將原文中的 AI 工具與步驟拆成固定 SOP。\n3. 用小範圍案例測試一次，不要一開始就全自動化。\n4. 把輸出結果保存到 Sheet、Notion、GitHub 或你的知識庫。\n5. 成功後再擴大成可重複執行的工作流。\n\n## 適合誰使用\n\n- 想收集繁中 AI 實戰案例的人\n- 想把 Threads 靈感轉成內部 SOP 的營運或 PM\n- 想建立 AI 工作流知識庫的團隊\n\n## 限制與風險\n\n- 這是自動草稿，只能根據公開抓到的文字整理。\n- 如果原文需要登入、圖片 OCR 或完整留言串，內容可能不完整。\n- 回覆區只整理公開抓得到的候選文字，不代表完整留言脈絡。\n\n## 回覆區重點\n\nreply_summary_status: `{reply_status}`\n\n{reply_lines}\n\n## 抓取品質\n\n- content_quality: `{quality}`\n- keyword_hits: {hits_line}\n- zh_ratio: `{ratio}`\n- source_url: {source_url}\n\n## 原始抓取內容\n\n```text\n{raw_content[:3000]}\n```\n""".lstrip()

    index_row = {
        "title": title,
        "filename": filename,
        "source_url": source_url,
        "source_author": author,
        "post_id": post_id,
        "category": category,
        "tools": tools,
        "status": status,
        "content_quality": quality,
        "zh_ratio": ratio,
        "reply_summary_status": reply_status,
        "generated_at": generated_at,
    }
    return md, index_row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", help="Fetched source JSON file")
    parser.add_argument("--out-dir", default="data/learning_drafts")
    parser.add_argument("--index", default="data/learning_articles_index.json")
    parser.add_argument("--min-zh-ratio", type=float, default=0.0, help="Set >0 to require Chinese ratio")
    args = parser.parse_args()

    input_path = Path(args.input_json)
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    index_path = Path(args.index)
    if index_path.exists():
        try:
            existing_index = json.loads(index_path.read_text(encoding="utf-8"))
        except Exception:
            existing_index = []
    else:
        existing_index = []
    by_url = {row.get("source_url"): row for row in existing_index if isinstance(row, dict)}

    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    built = 0
    skipped = 0
    for record in iter_records(payload):
        if not should_build(record):
            skipped += 1
            continue
        text = clean_text(str(record.get("raw_content", "")))
        if zh_ratio(text) < args.min_zh_ratio:
            skipped += 1
            continue
        md, row = markdown_for(record, generated_at)
        (out_dir / row["filename"]).write_text(md, encoding="utf-8")
        by_url[row["source_url"]] = row
        built += 1

    merged_index = sorted(by_url.values(), key=lambda r: (r.get("generated_at", ""), r.get("source_url", "")), reverse=True)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(merged_index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"built": built, "skipped": skipped, "out_dir": str(out_dir), "index": str(index_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
