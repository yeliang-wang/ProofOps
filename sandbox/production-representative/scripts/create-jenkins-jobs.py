#!/usr/bin/env python3
"""Create Jenkins job definitions for generated representative projects."""

from __future__ import annotations

import argparse
import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def job_config(project: dict) -> str:
    commands = "\n".join(f"        sh 'cd {project['root']} && {command}'" for command in project["validationCommands"])
    return f"""<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job">
  <description>Production-representative validation for {project['id']}.</description>
  <keepDependencies>false</keepDependencies>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps">
    <script>pipeline {{
  agent any
  stages {{
    stage('Validate') {{
      steps {{
{commands}
      }}
    }}
  }}
}}</script>
    <sandbox>true</sandbox>
  </definition>
  <disabled>false</disabled>
</flow-definition>
"""


def request(url: str, user: str, token: str, method: str, body: bytes | None = None, content_type: str = "application/xml") -> dict:
    headers = {"user-agent": "proofops-production-representative-sandbox/1"}
    if user or token:
        auth = base64.b64encode(f"{user}:{token}".encode("utf-8")).decode("ascii")
        headers["authorization"] = f"Basic {auth}"
    if body is not None:
        headers["content-type"] = content_type
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return {"status": response.status, "body": response.read().decode("utf-8", errors="replace")}
    except urllib.error.HTTPError as exc:
        return {"status": exc.code, "body": exc.read().decode("utf-8", errors="replace")}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create Jenkins job configs for representative projects")
    parser.add_argument("--output-root", default=str(REPO_ROOT / "data" / "production-representative-sandbox"))
    parser.add_argument("--jenkins-url", default=os.environ.get("JENKINS_URL", ""))
    parser.add_argument("--jenkins-user", default=os.environ.get("JENKINS_USER", ""))
    parser.add_argument("--jenkins-token", default=os.environ.get("JENKINS_TOKEN", ""))
    parser.add_argument("--apply", action="store_true", help="create or update jobs in Jenkins; default writes job config files only")
    args = parser.parse_args()

    output_root = Path(args.output_root).resolve()
    generated = json.loads((output_root / "generated-projects.json").read_text(encoding="utf-8"))
    jobs_root = output_root / "jenkins" / "jobs"
    jobs_root.mkdir(parents=True, exist_ok=True)
    jobs = []
    for project in generated["projects"]:
        name = project["cicd"]["job"]
        config = job_config(project)
        config_path = jobs_root / f"{name}.xml"
        config_path.write_text(config, encoding="utf-8")
        item = {"job": name, "config": str(config_path)}
        if args.apply:
            if not args.jenkins_url:
                raise SystemExit("JENKINS_URL or --jenkins-url is required when --apply is used")
            encoded = urllib.parse.quote(name)
            base = args.jenkins_url.rstrip("/")
            create = request(
                f"{base}/createItem?name={urllib.parse.quote(name)}",
                args.jenkins_user,
                args.jenkins_token,
                "POST",
                config.encode("utf-8"),
            )
            if create["status"] in {200, 201}:
                item["response"] = create
            elif create["status"] in {400, 409}:
                item["response"] = request(
                    f"{base}/job/{encoded}/config.xml",
                    args.jenkins_user,
                    args.jenkins_token,
                    "POST",
                    config.encode("utf-8"),
                )
            else:
                item["response"] = create
        jobs.append(item)
    print(json.dumps({"apply": args.apply, "jobs": jobs}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
