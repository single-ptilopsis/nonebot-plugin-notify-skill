#!/usr/bin/env python3
"""Send a completion webhook notification."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


ENV_WEBHOOK_URL = "WEBHOOK_URL"
ENV_BEARER_TOKEN = "BEARER_TOKEN"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a webhook notification")
    parser.add_argument("--task-name", required=True, help="Task name")
    parser.add_argument("--status", required=True, help="Task status")
    parser.add_argument("--summary", required=True, help="Short completion summary")
    parser.add_argument("--finished-at", required=True, help="Completion timestamp")
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds")
    return parser.parse_args()



def get_required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"missing required environment variable: {name}")
    return value



def main() -> int:
    args = parse_args()

    try:
        webhook_url = get_required_env(ENV_WEBHOOK_URL)
        bearer_token = get_required_env(ENV_BEARER_TOKEN)
    except RuntimeError as exc:
        print(json.dumps({
            "ok": False,
            "error": "missing_environment_variable",
            "reason": str(exc),
            "required": [ENV_WEBHOOK_URL, ENV_BEARER_TOKEN],
        }, ensure_ascii=False), file=sys.stderr)
        return 2

    payload = {
        "task_name": args.task_name,
        "status": args.status,
        "summary": args.summary,
        "finished_at": args.finished_at,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            print(json.dumps({
                "ok": True,
                "status_code": response.getcode(),
                "response_body": body,
                "payload": payload,
            }, ensure_ascii=False))
            return 0
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(json.dumps({
            "ok": False,
            "error": "http_error",
            "status_code": exc.code,
            "response_body": body,
            "payload": payload,
        }, ensure_ascii=False), file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(json.dumps({
            "ok": False,
            "error": "url_error",
            "reason": str(exc.reason),
            "payload": payload,
        }, ensure_ascii=False), file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover
        print(json.dumps({
            "ok": False,
            "error": "unexpected_error",
            "reason": str(exc),
            "payload": payload,
        }, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
