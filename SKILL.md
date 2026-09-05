---
name: coding-workspace-governance
description: Enforce a clean, reusable coding workspace for repository-based development. Use when coding, adding features, creating helper scripts, writing or running tests, flashing firmware, debugging hardware, generating logs or intermediate responses, or introducing reusable developer tooling. Require tool discovery through TOOLS.md before creating or invoking tooling, prefer reuse or extension over duplication, keep reusable tools under tools/, test-only code under test/, disposable artifacts under temp/, update TOOLS.md whenever tool capabilities or usage change, and validate workspace hygiene before finishing.
---

# Coding Workspace Governance

Apply this policy while working inside a source repository. Treat it as an always-on repository hygiene and tool-reuse workflow whenever the task creates, changes, discovers, or invokes development tooling, tests, flashing procedures, debugging utilities, or temporary artifacts.

## Core invariants

1. Search before creating.
   - Read `TOOLS.md` before creating a helper tool or before performing testing, flashing, hardware interaction, capture, conversion, packaging, or other repeatable developer operations.
   - Search `tools/` and `test/` when `TOOLS.md` is missing, incomplete, or references a related capability.
2. Reuse before duplicating.
   - Prefer an existing documented command.
   - Otherwise extend an existing tool with an option or subcommand when that preserves a coherent interface.
   - Create a new tool only when existing functionality cannot reasonably absorb the new capability.
3. Keep locations deterministic.
   - Put reusable developer utilities in `tools/`.
   - Put test cases, test-only scripts, fixtures, mocks, and test data in `test/`.
   - Put disposable logs, captures, debug dumps, generated responses, scratch output, and intermediate artifacts in `temp/`.
   - Do not place agent-created helper scripts, tests, or temporary files in the repository root.
4. Document with implementation.
   - Update `TOOLS.md` in the same task whenever a reusable tool, reusable test procedure, flashing procedure, command, dependency, argument, output location, or capability is added or materially changed.
   - Do not finish with stale tool documentation.
5. Clean before finishing.
   - Remove only disposable artifacts created by the current task when they are no longer useful.
   - Never delete pre-existing user files merely because they are inside `temp/`.
   - Validate the workspace before reporting completion.

## Scope and compatibility

Apply these rules to files created or materially reorganized by the current task. Do not silently migrate a mature repository from an existing `tests/`, `scripts/`, or project-specific convention solely to satisfy this skill. If the repository already has an explicit higher-priority convention, preserve it and adapt the registry workflow to that convention unless the user specifically asks for migration.

Do not put production source code in `tools/`, `test/`, or `temp/` merely to satisfy directory rules.

## Task workflow

### 1. Identify the repository root

Use the Git repository root when available. Otherwise use the current project directory selected by the user.

### 2. Inspect project policy and registry

Before creating or invoking development tooling:

1. Read repository instructions such as `AGENTS.md` when present.
2. Read `TOOLS.md` when present.
3. Search `tools/` and `test/` for related names, commands, protocols, device families, interfaces, file formats, and capabilities.
4. Treat `TOOLS.md` as an index, not as proof that a tool is correct. Inspect the referenced implementation or `--help` output when execution details matter.

If `TOOLS.md` does not exist and the task introduces reusable tooling or procedures, create it from `assets/TOOLS.md.template` or an equivalent structure before finishing.

### 3. Classify every new artifact

Use this decision table:

| Artifact | Location |
| --- | --- |
| Production source/configuration | Existing project structure |
| Reusable flashing/debug/conversion/build/developer utility | `tools/` |
| Test case, test-only script, fixture, mock, golden data | `test/` |
| Reusable test harness used as a general developer utility | `tools/` and document the test entry points in `TOOLS.md` |
| Log, trace, dump, capture, generated response, scratch file, intermediate output | `temp/` |
| Final user-requested deliverable | User-requested or project-appropriate location |

When uncertain whether code is a test or a reusable tool, ask: "Would a developer invoke this independently outside one specific test case?" If yes, prefer `tools/`; otherwise prefer `test/`.

### 4. Reuse or extend before creating

For each needed capability:

1. Search `TOOLS.md` by capability and keywords.
2. Inspect referenced tools or procedures.
3. Reuse the documented path and command when suitable.
4. If functionality is close but incomplete, extend the existing interface rather than creating a sibling with overlapping behavior.
5. Create a new tool only after confirming no reasonable reusable implementation exists.

Avoid proliferation such as `flash2.py`, `debug_new.py`, `test_final.py`, or multiple one-off wrappers around the same command.

### 5. Handle testing, flashing, and hardware interaction

Before running a test, programmer, debugger, serial monitor, hardware capture, or firmware flashing command:

1. Read the relevant `TOOLS.md` entry.
2. Prefer the documented executable, programmer, adapter, baud rate, interface, environment variable, and command syntax.
3. Inspect the tool's current help or implementation when options may have changed.
4. Write execution logs and transient captures under `temp/` unless the project explicitly requires a persistent artifact elsewhere.
5. If the documented procedure is wrong, fix the underlying tool or procedure and update `TOOLS.md`; do not leave an undocumented workaround as the final solution.

Never store secrets, access tokens, private keys, or credentials in `TOOLS.md`. Document environment variable names or secret-manager references instead.

### 6. Maintain TOOLS.md

Use the format in `references/tools-registry-format.md`.

For every reusable capability, document enough information that a future agent can discover and use it without re-deriving the procedure. At minimum include:

- Capability or tool name
- Purpose
- Path or external command
- When to use it
- Usage examples
- Inputs and relevant arguments
- Outputs and persistent/transient output locations
- Requirements or dependencies
- Important constraints or safety notes

When modifying an existing tool, update its existing entry instead of appending a duplicate entry.

### 7. Finish with workspace validation

Before reporting completion:

1. Confirm newly created reusable helpers are under `tools/`.
2. Confirm newly created test-only artifacts are under `test/`.
3. Confirm disposable output is under `temp/`.
4. Confirm new or changed reusable capabilities are reflected in `TOOLS.md`.
5. Confirm commands shown in `TOOLS.md` match the implementation.
6. Remove unnecessary disposable artifacts created by the current task.

When code execution is available, run:

```bash
python <skill-dir>/scripts/validate_workspace.py --root <repo-root>
```

Treat errors as blockers. Review warnings and either fix them or explicitly explain why the repository's existing convention should be preserved.

## Repository initialization

When the user asks to initialize or retrofit this policy into a repository, run:

```bash
python <skill-dir>/scripts/init_workspace.py --root <repo-root>
```

This creates missing `tools/`, `test/`, and `temp/` directories, creates `TOOLS.md` from the bundled template when missing, and ensures `temp/` is ignored by Git without overwriting existing files.

Use `--install-agent-rules` only when the user wants the repository itself to carry these rules for coding agents. This appends a managed policy block to `AGENTS.md` without replacing existing repository instructions.

## Resource map

- `scripts/init_workspace.py`: Initialize the workspace layout, `TOOLS.md`, `.gitignore`, and optional `AGENTS.md` policy block.
- `scripts/validate_workspace.py`: Check required structure, root-level disposable files, likely misplaced new-style tests, Git ignore coverage, and undocumented files under `tools/`.
- `references/tools-registry-format.md`: Canonical `TOOLS.md` structure and update rules.
- `assets/TOOLS.md.template`: Starter tool registry.
- `assets/AGENTS.workspace-policy.md`: Managed repository-policy block for cross-agent use.
