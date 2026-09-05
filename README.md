# Coding Workspace Governance

Agent Skill for keeping coding repositories clean, reusable, and self-documenting.

It establishes a workspace policy built around four repository artifacts:

- `tools/` - reusable developer, flashing, debugging, conversion, and build utilities
- `tests/` - tests, fixtures, mocks, and test-only scripts
- `temp/` - disposable logs, traces, dumps, generated responses, and intermediate output
- `TOOLS.md` - the project's tool/capability registry and usage guide

The central rule is **search before create**: before an agent writes a new helper, runs a test, flashes firmware, or performs repeatable hardware/debug operations, it must inspect `TOOLS.md` and existing tooling first. When reusable tooling changes, `TOOLS.md` must change in the same task.

## Agent installation

This repository is itself a complete Agent Skill: `SKILL.md` is at the repository root and all supporting files are kept beside it.

### Codex / OpenCode / Agent-Skills compatible agents

Install globally by cloning the repository into the user Agent Skills directory:

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/sukon/coding-workspace-governance.git \
  ~/.agents/skills/coding-workspace-governance
```

OpenCode discovers `~/.agents/skills/<name>/SKILL.md` directly. Current Codex installations also use the Agent Skills location for user-installed skills. Agent runtimes that follow the `.agents/skills` convention can use the same checkout.

### Claude Code

Claude Code's documented personal-skill location is `~/.claude/skills/`:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/sukon/coding-workspace-governance.git \
  ~/.claude/skills/coding-workspace-governance
```

### Use one checkout for multiple agents

On Linux/macOS, keep the canonical checkout under `~/.agents/skills` and symlink it for Claude Code:

```bash
mkdir -p ~/.agents/skills ~/.claude/skills
git clone https://github.com/sukon/coding-workspace-governance.git \
  ~/.agents/skills/coding-workspace-governance
ln -s ~/.agents/skills/coding-workspace-governance \
  ~/.claude/skills/coding-workspace-governance
```

On Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills" | Out-Null
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
git clone https://github.com/sukon/coding-workspace-governance.git `
  "$HOME\.agents\skills\coding-workspace-governance"
New-Item -ItemType Junction `
  -Path "$HOME\.claude\skills\coding-workspace-governance" `
  -Target "$HOME\.agents\skills\coding-workspace-governance"
```

If a runtime has a different configured Skill directory, clone this repository into that directory instead. The required invariant is:

```text
<skills-root>/coding-workspace-governance/SKILL.md
```

## Ask an agent to install it

Give a coding agent this instruction:

> Install the Agent Skill from `https://github.com/sukon/coding-workspace-governance.git`. Put it in your persistent user Skill directory as `coding-workspace-governance`, verify that `SKILL.md` is discoverable, and do not copy only `SKILL.md` because the Skill also uses bundled scripts, references, and assets.

For Claude Code, explicitly tell it to use `~/.claude/skills/coding-workspace-governance`. For Codex or other Agent-Skills compatible runtimes, prefer `~/.agents/skills/coding-workspace-governance` unless that runtime reports a different configured location.

## Updating

For an installation under `~/.agents/skills`:

```bash
git -C ~/.agents/skills/coding-workspace-governance pull --ff-only
```

For Claude Code installed directly under `~/.claude/skills`:

```bash
git -C ~/.claude/skills/coding-workspace-governance pull --ff-only
```

## Initialize a project

After the Skill is available to the agent, ask it to apply the workspace policy to a repository. The bundled initializer creates missing directories and registry files without replacing unrelated existing content:

```bash
python <skill-dir>/scripts/init_workspace.py --root <repo-root>
```

To also install a managed repository policy block into `AGENTS.md`:

```bash
python <skill-dir>/scripts/init_workspace.py --root <repo-root> --install-agent-rules
```

A newly governed project uses:

```text
<repo-root>/
├── tools/
├── tests/
├── temp/
└── TOOLS.md
```

## Validate a project

```bash
python <skill-dir>/scripts/validate_workspace.py --root <repo-root>
```

The validator checks workspace structure, common root-level temporary/test pollution, Git ignore coverage for temporary artifacts, and whether reusable files under `tools/` are represented in `TOOLS.md`.

## Repository layout

```text
coding-workspace-governance/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── AGENTS.workspace-policy.md
│   └── TOOLS.md.template
├── references/
│   └── tools-registry-format.md
└── scripts/
    ├── init_workspace.py
    └── validate_workspace.py
```
