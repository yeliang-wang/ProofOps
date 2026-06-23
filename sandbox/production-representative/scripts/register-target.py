#!/usr/bin/env python3
"""Register generated representative projects into a target product."""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path


SANDBOX_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SANDBOX_ROOT.parents[1]


def post_json(url: str, token: str, payload: dict) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {token}",
            "user-agent": "proofops-production-representative-sandbox/1",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return {"status": response.status, "body": json.loads(response.read().decode("utf-8"))}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {"status": exc.code, "body": body}


def main() -> int:
    parser = argparse.ArgumentParser(description="Register production-representative projects into a target product")
    parser.add_argument("--target", choices=["evopilot"], required=True)
    parser.add_argument("--base-url", required=True, help="target product base URL, for example http://127.0.0.1:3000")
    parser.add_argument("--output-root", default=str(REPO_ROOT / "data" / "production-representative-sandbox"))
    parser.add_argument("--profile", default=str(SANDBOX_ROOT / "profiles" / "evopilot.release-matrix.json"))
    parser.add_argument("--apply", action="store_true", help="perform POST requests; default only prints registration plan")
    args = parser.parse_args()

    generated = json.loads((Path(args.output_root).resolve() / "generated-projects.json").read_text(encoding="utf-8"))
    profile = json.loads(Path(args.profile).read_text(encoding="utf-8"))
    token_env = profile["projectRegistration"]["authTokenEnv"]
    token = os.environ.get(token_env, "")
    registrations = []
    for project in generated["projects"]:
        payload = {
            "id": f"prs-{project['id']}",
            "name": project["name"],
            "profileId": project["id"],
            "repository": {
                "provider": "local-git",
                "root": project["root"],
                "defaultBranch": project["repository"]["defaultBranch"],
            },
            "cicd": {
                "mode": "jenkins",
                "jenkins": {
                    "connectorId": "default",
                    "job": project["cicd"]["job"],
                },
            },
        }
        item = {"projectId": payload["id"], "payload": payload}
        if args.apply:
            if not token:
                raise SystemExit(f"{token_env} is required when --apply is used")
            item["response"] = post_json(f"{args.base_url.rstrip('/')}{profile['projectRegistration']['endpoint']}", token, payload)
        registrations.append(item)
    print(json.dumps({"target": args.target, "apply": args.apply, "registrations": registrations}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
