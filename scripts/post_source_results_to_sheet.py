#!/usr/bin/env python3
"""Post fetched source JSON results to a Google Apps Script Web App."""

from __future__ import annotations

import argparse
import json
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file")
    parser.add_argument("webhook_url")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--run-url", default="")
    parser.add_argument("--artifact-url", default="")
    args = parser.parse_args()

    with open(args.json_file, "r", encoding="utf-8") as f:
        results = json.load(f)

    payload = {
        "meta": {
            "run_id": args.run_id,
            "run_url": args.run_url,
            "artifact_url": args.artifact_url,
        },
        "results": results,
    }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        args.webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        print(response.read().decode("utf-8"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
