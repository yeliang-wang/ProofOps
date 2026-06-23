# ProofOps: Claude Code Integration

Claude Code can use the Markdown agent directly from `agents/proofops-governor.md`.

Install:

```bash
cd /Users/wangyejing/github/ProofOps
./scripts/install.sh --tool claude-code --agent proofops-governor --update
```

Manual install:

```bash
mkdir -p ~/.claude/agents
cp /Users/wangyejing/github/ProofOps/agents/proofops-governor.md ~/.claude/agents/
```

Example:

```text
使用 proofops-governor，评估当前 demo 项目到 beta readiness 的差距，先做 architecture readiness，再生成 target plan，确认后进入 evidence loop。
```
