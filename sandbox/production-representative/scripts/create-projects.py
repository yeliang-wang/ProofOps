#!/usr/bin/env python3
"""Create production-representative project repositories from toolkit templates."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


SANDBOX_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SANDBOX_ROOT.parents[1]
MANIFEST_PATH = SANDBOX_ROOT / "manifest.json"


def run(command: list[str], cwd: Path) -> dict:
    completed = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return {
        "command": command,
        "cwd": str(cwd),
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def require_ok(result: dict) -> None:
    if result["returncode"] != 0:
        raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))


def copy_template(template: Path, destination: Path, force: bool) -> None:
    if destination.exists():
        if not force:
            raise SystemExit(f"{destination} already exists; pass --force to replace generated project")
        shutil.rmtree(destination)
    shutil.copytree(template, destination, ignore=shutil.ignore_patterns("node_modules", ".git"))


def init_git_repo(project_root: Path) -> list[dict]:
    results = [
        run(["git", "init", "-b", "main"], project_root),
        run(["git", "add", "."], project_root),
        run(
            [
                "git",
                "-c",
                "user.name=ProofOps Representative Sandbox",
                "-c",
                "user.email=proofops-representative@example.invalid",
                "commit",
                "-m",
                "Initial representative project",
            ],
            project_root,
        ),
    ]
    for result in results:
        require_ok(result)
    return results


def validate_project(project_root: Path, commands: list[str]) -> list[dict]:
    results = []
    for command in commands:
        result = run(command.split(), project_root)
        require_ok(result)
        results.append(result)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Create production-representative sandbox projects")
    parser.add_argument("--output-root", default=str(REPO_ROOT / "data" / "production-representative-sandbox"))
    parser.add_argument("--force", action="store_true", help="replace generated projects")
    parser.add_argument("--skip-validation", action="store_true", help="create repositories without running validation commands")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    output_root = Path(args.output_root).resolve()
    projects_root = output_root / "projects"
    projects_root.mkdir(parents=True, exist_ok=True)

    generated_projects = []
    for project in manifest["projects"]:
        template = SANDBOX_ROOT / project["template"]
        destination = projects_root / project["id"]
        copy_template(template, destination, args.force)
        git_results = init_git_repo(destination)
        validation_results = [] if args.skip_validation else validate_project(destination, project["validation"]["commands"])
        generated_projects.append(
            {
                "id": project["id"],
                "name": project["name"],
                "root": str(destination),
                "repository": {
                    "provider": "local-git",
                    "root": str(destination),
                    "defaultBranch": project["repository"]["defaultBranch"],
                },
                "cicd": project["cicd"],
                "coverageTags": project["coverageTags"],
                "validationCommands": project["validation"]["commands"],
                "faultInjectionCommand": project["validation"].get("faultInjectionCommand"),
                "git": git_results[-1],
                "validation": validation_results,
            }
        )

    generated = {
        "schema": "proofops-production-representative-generated/v1",
        "sourceManifest": str(MANIFEST_PATH),
        "outputRoot": str(output_root),
        "projects": generated_projects,
    }
    generated_path = output_root / "generated-projects.json"
    generated_path.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "generated": str(generated_path), "projectCount": len(generated_projects)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
