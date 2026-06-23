#!/usr/bin/env python3
"""Control-plane CLI for ProofOps."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = REPO_ROOT / "manifests" / "agents"
PLUGIN_DIR = REPO_ROOT / "plugins"
CATALOG_DIR = REPO_ROOT / "catalog"
TARGET_DIR = REPO_ROOT / "targets"
ADAPTER_DIR = REPO_ROOT / "adapters"
PROFILE_TEMPLATE_DIR = REPO_ROOT / "project-profiles" / "templates"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifests() -> list[dict]:
    return [read_json(path) for path in sorted(MANIFEST_DIR.glob("*.json"))]


def load_plugins() -> list[dict]:
    return [read_json(path) for path in sorted(PLUGIN_DIR.glob("*/plugin.json"))]


def load_target_presets() -> list[dict]:
    return [read_json(path) for path in sorted(TARGET_DIR.glob("*.json"))]


def load_evidence_adapters() -> list[dict]:
    return [read_json(path) for path in sorted(ADAPTER_DIR.glob("*.json"))]


def load_profile_templates() -> list[dict]:
    return [read_json(path) for path in sorted(PROFILE_TEMPLATE_DIR.glob("*.json"))]


def find_manifest(agent_id: str) -> dict:
    for manifest in load_manifests():
        if manifest["id"] == agent_id:
            return manifest
    raise SystemExit(f"unknown agent: {agent_id}")


def print_table(headers: list[str], rows: list[list[str]]) -> None:
    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))
    print("  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        print("  ".join(cell.ljust(widths[index]) for index, cell in enumerate(row)))


def cmd_list(args: argparse.Namespace) -> int:
    manifests = load_manifests()
    rows = [
        [
            manifest["id"],
            manifest["version"],
            manifest["lifecycle"],
            manifest["source"]["claudeMarkdown"],
            manifest["distributions"]["codexToml"],
        ]
        for manifest in manifests
    ]
    if args.json:
        print(json.dumps({"agents": manifests}, ensure_ascii=False, indent=2))
    else:
        print_table(["agent", "version", "lifecycle", "source", "codex"], rows)
    return 0


def cmd_plugins(args: argparse.Namespace) -> int:
    plugins = load_plugins()
    if args.json:
        print(json.dumps({"plugins": plugins}, ensure_ascii=False, indent=2))
        return 0
    rows = [[plugin["id"], plugin["version"], plugin["lifecycle"], plugin["category"], ",".join(plugin["agents"])] for plugin in plugins]
    print_table(["plugin", "version", "lifecycle", "category", "agents"], rows)
    return 0


def searchable_blob(item: dict) -> str:
    return json.dumps(item, ensure_ascii=False).lower()


def cmd_search(args: argparse.Namespace) -> int:
    query = " ".join(args.query).strip().lower()
    if not query:
        raise SystemExit("search query is required")
    agent_catalog = read_json(CATALOG_DIR / "agents.json")
    plugin_catalog = read_json(CATALOG_DIR / "plugins.json")
    agent_hits = [agent for agent in agent_catalog["agents"] if query in searchable_blob(agent)]
    plugin_hits = [plugin for plugin in plugin_catalog["plugins"] if query in searchable_blob(plugin)]
    if args.json:
        print(json.dumps({"query": query, "agents": agent_hits, "plugins": plugin_hits}, ensure_ascii=False, indent=2))
        return 0
    print(f"Query: {query}")
    if plugin_hits:
        print("\nPlugins:")
        print_table(["plugin", "lifecycle", "category", "agents"], [[p["id"], p["lifecycle"], p["category"], ",".join(p["agents"])] for p in plugin_hits])
    if agent_hits:
        print("\nAgents:")
        print_table(["agent", "plugin", "lifecycle", "category"], [[a["id"], a["pluginId"], a["lifecycle"], a["category"]] for a in agent_hits])
    if not plugin_hits and not agent_hits:
        print("No matches.")
        return 1
    return 0


def codex_status_for_project(project_root: Path) -> list[dict]:
    installed_dir = project_root / ".codex" / "agents"
    statuses = []
    for manifest in load_manifests():
        source = REPO_ROOT / manifest["distributions"]["codexToml"]
        installed = installed_dir / source.name
        status = {
            "id": manifest["id"],
            "version": manifest["version"],
            "lifecycle": manifest["lifecycle"],
            "source": str(source),
            "installed": str(installed),
            "installedExists": installed.exists(),
            "matchesToolkit": False,
        }
        if source.exists() and installed.exists():
            status["sourceSha256"] = sha256(source)
            status["installedSha256"] = sha256(installed)
            status["matchesToolkit"] = status["sourceSha256"] == status["installedSha256"]
        statuses.append(status)
    return statuses


def codex_goal_feature_status() -> dict:
    codex = shutil.which("codex")
    if not codex:
        return {"codexFound": False, "goalsFeature": "unknown", "detail": "codex command not found"}
    completed = subprocess.run(
        [codex, "features", "list"],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        return {
            "codexFound": True,
            "goalsFeature": "unknown",
            "detail": (completed.stderr or completed.stdout).strip(),
        }
    for line in completed.stdout.splitlines():
        parts = line.split()
        if parts and parts[0] == "goals":
            enabled = parts[-1].lower() == "true"
            return {
                "codexFound": True,
                "goalsFeature": "enabled" if enabled else "disabled",
                "enableCommand": "" if enabled else "codex features enable goals",
            }
    return {"codexFound": True, "goalsFeature": "unknown", "detail": "goals feature not listed"}


def cmd_codex_status(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).resolve()
    statuses = codex_status_for_project(project_root)
    goal_feature = codex_goal_feature_status()
    if args.json:
        print(json.dumps({"projectRoot": str(project_root), "codexGoalFeature": goal_feature, "codexAgents": statuses}, ensure_ascii=False, indent=2))
        return 0

    rows = []
    for item in statuses:
        if not item["installedExists"]:
            state = "missing"
        elif item["matchesToolkit"]:
            state = "current"
        else:
            state = "drifted"
        rows.append([item["id"], item["version"], item["lifecycle"], state, item["installed"]])
    print(f"Project: {project_root}")
    print_table(["agent", "version", "lifecycle", "status", "installed"], rows)
    if goal_feature["goalsFeature"] == "disabled":
        print("\nCodex /goal adapter: goals feature is disabled. Enable with: codex features enable goals")
    elif goal_feature["goalsFeature"] == "enabled":
        print("\nCodex /goal adapter: goals feature is enabled.")
    else:
        print(f"\nCodex /goal adapter: goals feature status is unknown ({goal_feature.get('detail', 'no detail')}).")
    return 1 if any(not item["installedExists"] or not item["matchesToolkit"] for item in statuses) else 0


def build_goal_plan(manifest: dict, project_id: str, goal: str) -> dict:
    codex_goal = manifest["runtimeAdapters"]["codexGoal"]
    loop_contract = manifest["loopContract"]

    def resolve(value: str) -> str:
        return value.replace("<projectId>", project_id)

    return {
        "schema": "proofops-codex-goal-plan/v1",
        "agentId": manifest["id"],
        "version": manifest["version"],
        "projectId": project_id,
        "codexGoal": {
            "feature": codex_goal["requiresFeature"],
            "outerGoal": goal or codex_goal["outerGoal"],
            "recommendedCommand": "/goal",
            "adapterRole": "Codex owns the outer objective runtime; the agent owns the inner loop protocol.",
        },
        "innerLoop": {
            "agent": codex_goal["innerLoopAgent"],
            "inputs": loop_contract["inputs"],
            "goalWindow": loop_contract["goalWindow"],
            "coverageMatrix": loop_contract["coverageMatrix"],
            "repairPolicy": loop_contract["repairPolicy"],
            "decisionChain": loop_contract["decisionChain"],
            "cadenceModes": loop_contract["cadenceModes"],
            "stopPolicies": loop_contract["stopPolicies"],
            "stateFields": loop_contract["stateFields"],
            "resumePolicy": codex_goal["resumePolicy"],
        },
        "artifacts": {
            "stateArtifact": resolve(codex_goal["stateArtifact"]),
            "statusArtifact": resolve(codex_goal["statusArtifact"]),
            "evidenceRoot": resolve(codex_goal["evidenceRoot"]),
        },
        "gates": {
            "confirmationGates": manifest["confirmationGates"],
            "dangerousActions": manifest["dangerousActions"],
            "evidenceRequired": loop_contract["evidenceRequired"],
            "confirmationGatesPreserved": loop_contract["confirmationGatesPreserved"],
        },
    }


def cmd_goal_plan(args: argparse.Namespace) -> int:
    manifest = find_manifest(args.agent)
    plan = build_goal_plan(manifest, args.project_id, " ".join(args.goal).strip())
    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    print(f"Agent: {plan['agentId']} {plan['version']}")
    print(f"Project: {plan['projectId']}")
    print(f"Codex command: {plan['codexGoal']['recommendedCommand']}")
    print(f"Outer goal: {plan['codexGoal']['outerGoal']}")
    print(f"Inner loop: {plan['innerLoop']['agent']}")
    print(f"State: {plan['artifacts']['stateArtifact']}")
    print(f"Status: {plan['artifacts']['statusArtifact']}")
    print(f"Evidence: {plan['artifacts']['evidenceRoot']}")
    print(f"Goal window fields: {', '.join(plan['innerLoop']['goalWindow']['fields'])}")
    print(f"Coverage matrix fields: {', '.join(plan['innerLoop']['coverageMatrix']['fields'])}")
    print(f"Repair policy actions: {', '.join(plan['innerLoop']['repairPolicy']['actions'])}")
    print(f"Decision chain fields: {', '.join(plan['innerLoop']['decisionChain']['fields'])}")
    print("Decision chain reporting: required per phase and printed in every phase report")
    print(f"Stop policies: {', '.join(plan['innerLoop']['stopPolicies'])}")
    print(f"Confirmation gates: {', '.join(plan['gates']['confirmationGates'])}")
    return 0


def cmd_target_presets(args: argparse.Namespace) -> int:
    presets = load_target_presets()
    if args.json:
        print(json.dumps({"schema": "proofops-target-preset-list/v1", "targets": presets}, ensure_ascii=False, indent=2))
        return 0
    rows = [
        [
            preset["id"],
            preset["lifecycleTarget"],
            str(len(preset["phaseTargets"])),
            str(len(preset["architectureCriteria"])),
            preset["title"],
        ]
        for preset in presets
    ]
    print_table(["target", "lifecycle", "phases", "architecture", "title"], rows)
    return 0


def cmd_adapters(args: argparse.Namespace) -> int:
    adapters = load_evidence_adapters()
    if args.json:
        print(json.dumps({"schema": "proofops-evidence-adapter-list/v1", "adapters": adapters}, ensure_ascii=False, indent=2))
        return 0
    rows = [[adapter["id"], adapter["category"], adapter["evidenceType"], adapter["title"]] for adapter in adapters]
    print_table(["adapter", "category", "evidence", "title"], rows)
    return 0


def cmd_profile_templates(args: argparse.Namespace) -> int:
    templates = load_profile_templates()
    if args.json:
        print(json.dumps({"schema": "proofops-profile-template-list/v1", "templates": templates}, ensure_ascii=False, indent=2))
        return 0
    rows = [
        [
            template["id"],
            template["target"],
            ",".join(template.get("requiredAdapters", [])),
            template["title"],
        ]
        for template in templates
    ]
    print_table(["template", "target", "adapters", "title"], rows)
    return 0


def cmd_init_profile(args: argparse.Namespace) -> int:
    template_by_id = {template["id"]: template for template in load_profile_templates()}
    template = template_by_id.get(args.template)
    if not template:
        raise SystemExit(f"unknown profile template: {args.template}")
    lifecycle_id = args.lifecycle_id or f"{args.project_id}-{template['target']}"
    output = Path(args.output).resolve()
    profile = {
        "schema": "proofops-project-profile/v1",
        "projectId": args.project_id,
        "releaseTarget": template["target"].upper(),
        "lifecycleId": lifecycle_id,
        "projectRoot": args.project_root,
        "templateId": template["id"],
        "requiredAdapters": template.get("requiredAdapters", []),
        "targetPlan": {
            "finalGoal": f"{args.project_id} reaches {template['target']} readiness using {template['title']}.",
            "phaseGoals": [f"{row['capability']}: {row['scenario']}" for row in template.get("matrixSeed", [])],
            "acceptanceCriteria": [row["requiredEvidence"] for row in template.get("matrixSeed", [])],
            "finalDecision": ["GO", "CONDITIONAL-GO", "NO-GO", "BLOCKED"],
        },
        "targetPlanConfirmation": {
            "status": "pending",
            "instruction": "Review and confirm this generated target plan before running the release coverage matrix.",
        },
        "releaseDecision": {
            "mode": "profile-final-report",
            "goStatus": "GO",
            "source": "runner coverage matrix and final report",
        },
        "runner": {
            "mode": "once",
            "intervalMs": 1000,
            "blockerPolicy": {
                "mode": "stop-on-required-blocker",
                "reason": "Required release coverage blockers require productized repair before release evidence can be used.",
                "nextAction": "Repair the blocker, verify targeted evidence, then rerun the profile.",
                "exitCode": 2,
                "repairWorkflows": {
                    "enabled": True,
                    "types": ["repository-quality", "coverage-evidence-gap", "release-criterion"],
                },
            },
            "finalReports": {
                "markdown": f"data/proofops/{lifecycle_id}/final-report.md",
                "json": f"data/proofops/{lifecycle_id}/final-report.json",
                "includeIterationTargetSummaries": True,
                "includeFinalTargetSummary": True,
            },
        },
        "steps": [
            {
                "id": f"{row['capability']}-{row['scenario']}".replace("_", "-"),
                "type": "command",
                "capability": row["capability"],
                "scenario": row["scenario"],
                "command": "true",
                "args": [],
                "requiredEvidence": row["requiredEvidence"],
                "required": True,
            }
            for row in template.get("matrixSeed", [])
        ],
    }
    if args.confirmed:
        profile["targetPlanConfirmation"] = {
            "status": "confirmed",
            "confirmedBy": "profile-generator",
            "instruction": "Generated profile was explicitly confirmed through proofops init-profile --confirmed.",
        }
    if args.dry_run:
        print(json.dumps(profile, ensure_ascii=False, indent=2))
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


def cmd_install(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).resolve()
    agents: list[str] = []
    if args.agent:
        agents.extend(args.agent)
    if args.plugin:
        plugin_by_id = {plugin["id"]: plugin for plugin in load_plugins()}
        for plugin_id in args.plugin:
            plugin = plugin_by_id.get(plugin_id)
            if not plugin:
                raise SystemExit(f"unknown plugin: {plugin_id}")
            agents.extend(plugin["agents"])
    if not agents:
        command = [str(REPO_ROOT / "scripts" / "install.sh"), "--tool", args.tool, "--update"]
        if args.dry_run:
            command.append("--dry-run")
        return subprocess.call(command, cwd=project_root)
    status = 0
    for agent_id in sorted(set(agents)):
        command = [str(REPO_ROOT / "scripts" / "install.sh"), "--tool", args.tool, "--agent", agent_id, "--update"]
        if args.dry_run:
            command.append("--dry-run")
        status = subprocess.call(command, cwd=project_root) or status
    return status


def cmd_proposals(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).resolve()
    proposal_root = project_root / ".proofops" / "proposals"
    proposals = []
    for manifest_path in sorted(proposal_root.glob("proposal-*/manifest.json")):
        manifest = read_json(manifest_path)
        proposals.append({
            "path": str(manifest_path.parent),
            "title": manifest.get("title") or "",
            "created_at": manifest.get("created_at") or "",
            "tool": manifest.get("tool") or "",
            "changeCount": len(manifest.get("changes", [])),
        })
    if args.json:
        print(json.dumps({"projectRoot": str(project_root), "proposals": proposals}, ensure_ascii=False, indent=2))
        return 0
    if not proposals:
        print(f"No proposals under {proposal_root}")
        return 0
    print_table(["created", "tool", "changes", "title", "path"], [[p["created_at"], p["tool"], str(p["changeCount"]), p["title"], p["path"]] for p in proposals])
    return 0


def cmd_sandbox_verify(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(REPO_ROOT / "sandbox" / "production-representative" / "scripts" / "verify-sandbox.py"),
    ]
    if args.output_root:
        command.extend(["--output-root", args.output_root])
    if args.generated:
        command.append("--generated")
    if args.include_fault:
        command.append("--include-fault")
    if args.json:
        command.append("--json")
    return subprocess.run(command, cwd=REPO_ROOT).returncode


def cmd_sandbox_create(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(REPO_ROOT / "sandbox" / "production-representative" / "scripts" / "create-projects.py"),
        "--output-root",
        args.output_root,
    ]
    if args.force:
        command.append("--force")
    if args.skip_validation:
        command.append("--skip-validation")
    return subprocess.run(command, cwd=REPO_ROOT).returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ProofOps control plane")
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="List managed agents")
    list_parser.add_argument("--json", action="store_true")
    list_parser.set_defaults(func=cmd_list)

    plugins_parser = sub.add_parser("plugins", help="List plugin packages")
    plugins_parser.add_argument("--json", action="store_true")
    plugins_parser.set_defaults(func=cmd_plugins)

    search_parser = sub.add_parser("search", help="Search agent and plugin catalog")
    search_parser.add_argument("query", nargs="+")
    search_parser.add_argument("--json", action="store_true")
    search_parser.set_defaults(func=cmd_search)

    status_parser = sub.add_parser("codex-status", help="Check project-scoped Codex install drift")
    status_parser.add_argument("--project-root", default=".")
    status_parser.add_argument("--json", action="store_true")
    status_parser.set_defaults(func=cmd_codex_status)

    goal_parser = sub.add_parser("goal-plan", help="Render a Codex /goal adapter plan for an agent")
    goal_parser.add_argument("--agent", required=True)
    goal_parser.add_argument("--project-id", default="default")
    goal_parser.add_argument("--json", action="store_true")
    goal_parser.add_argument("goal", nargs="*")
    goal_parser.set_defaults(func=cmd_goal_plan)

    target_parser = sub.add_parser("target-presets", help="List ProofOps maturity target presets")
    target_parser.add_argument("--json", action="store_true")
    target_parser.set_defaults(func=cmd_target_presets)

    adapters_parser = sub.add_parser("adapters", help="List evidence adapter contracts")
    adapters_parser.add_argument("--json", action="store_true")
    adapters_parser.set_defaults(func=cmd_adapters)

    templates_parser = sub.add_parser("profile-templates", help="List reusable project profile templates")
    templates_parser.add_argument("--json", action="store_true")
    templates_parser.set_defaults(func=cmd_profile_templates)

    init_profile_parser = sub.add_parser("init-profile", help="Generate a project profile from a reusable template")
    init_profile_parser.add_argument("--template", required=True)
    init_profile_parser.add_argument("--project-id", required=True)
    init_profile_parser.add_argument("--project-root", default=".")
    init_profile_parser.add_argument("--lifecycle-id")
    init_profile_parser.add_argument("--output", required=True)
    init_profile_parser.add_argument("--confirmed", action="store_true")
    init_profile_parser.add_argument("--dry-run", action="store_true")
    init_profile_parser.set_defaults(func=cmd_init_profile)

    install_parser = sub.add_parser("install", help="Install agents or plugins into a target project")
    install_parser.add_argument("--project-root", default=".")
    install_parser.add_argument("--tool", choices=["codex", "claude-code"], default="codex")
    install_parser.add_argument("--agent", action="append", default=[])
    install_parser.add_argument("--plugin", action="append", default=[])
    install_parser.add_argument("--dry-run", action="store_true")
    install_parser.set_defaults(func=cmd_install)

    proposal_parser = sub.add_parser("proposals", help="List offline proposals in a target project")
    proposal_parser.add_argument("--project-root", default=".")
    proposal_parser.add_argument("--json", action="store_true")
    proposal_parser.set_defaults(func=cmd_proposals)

    sandbox_verify_parser = sub.add_parser("sandbox-verify", help="Verify the production representative sandbox")
    sandbox_verify_parser.add_argument("--output-root", default=str(REPO_ROOT / "data" / "production-representative-sandbox"))
    sandbox_verify_parser.add_argument("--generated", action="store_true")
    sandbox_verify_parser.add_argument("--include-fault", action="store_true")
    sandbox_verify_parser.add_argument("--json", action="store_true")
    sandbox_verify_parser.set_defaults(func=cmd_sandbox_verify)

    sandbox_create_parser = sub.add_parser("sandbox-create", help="Create production representative project repositories")
    sandbox_create_parser.add_argument("--output-root", default=str(REPO_ROOT / "data" / "production-representative-sandbox"))
    sandbox_create_parser.add_argument("--force", action="store_true")
    sandbox_create_parser.add_argument("--skip-validation", action="store_true")
    sandbox_create_parser.set_defaults(func=cmd_sandbox_create)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
