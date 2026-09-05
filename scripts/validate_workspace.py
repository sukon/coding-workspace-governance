#!/usr/bin/env python3
"""Validate repository hygiene and tool-registry coverage."""

from __future__ import annotations

import argparse
import fnmatch
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DISPOSABLE_ROOT_PATTERNS = (
    "*.log",
    "*.tmp",
    "*.trace",
    "*.dump",
    "*.prof",
    "*.out",
)

TEST_NAME_PATTERNS = (
    "test_*.py",
    "*_test.py",
    "*.test.js",
    "*.test.ts",
    "*.test.tsx",
    "*.spec.js",
    "*.spec.ts",
    "*.spec.tsx",
)

IGNORE_TOOL_NAMES = {".gitkeep", ".DS_Store", "README.md", "README"}


@dataclass
class Finding:
    level: str
    message: str


def run_git(root: Path, args: list[str]) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return None


def is_git_repo(root: Path) -> bool:
    result = run_git(root, ["rev-parse", "--is-inside-work-tree"])
    return bool(result and result.returncode == 0 and result.stdout.strip() == "true")


def git_status(root: Path) -> dict[str, str]:
    result = run_git(root, ["status", "--porcelain", "--untracked-files=all"])
    if not result or result.returncode != 0:
        return {}

    items: dict[str, str] = {}
    for raw in result.stdout.splitlines():
        if len(raw) < 4:
            continue
        code = raw[:2]
        path_text = raw[3:]
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        items[path_text.replace("\\", "/")] = code
    return items


def is_new_status(code: str) -> bool:
    return code == "??" or "A" in code


def is_test_name(path: Path) -> bool:
    name = path.name
    return any(fnmatch.fnmatch(name, pattern) for pattern in TEST_NAME_PATTERNS)


def iter_tool_files(tools_dir: Path) -> Iterable[Path]:
    if not tools_dir.is_dir():
        return []
    return (
        path
        for path in tools_dir.rglob("*")
        if path.is_file()
        and path.name not in IGNORE_TOOL_NAMES
        and "__pycache__" not in path.parts
        and not path.name.endswith((".pyc", ".pyo"))
    )


def temp_is_ignored(root: Path) -> bool:
    result = run_git(root, ["check-ignore", "-q", "temp/probe.tmp"])
    if result is not None and result.returncode == 0:
        return True

    path = root / ".gitignore"
    if not path.exists():
        return False
    entries = {line.strip() for line in path.read_text(encoding="utf-8").splitlines()}
    return "temp/" in entries or "/temp/" in entries


def add(findings: list[Finding], level: str, message: str) -> None:
    findings.append(Finding(level, message))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate coding workspace governance rules.")
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Promote governance warnings to errors.",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    findings: list[Finding] = []
    strict_level = "ERROR" if args.strict else "WARN"

    if not root.exists() or not root.is_dir():
        print(f"ERROR: workspace root does not exist or is not a directory: {root}")
        return 1

    required = ["tools", "test", "temp", "TOOLS.md"]
    for rel in required:
        if not (root / rel).exists():
            add(findings, strict_level, f"Missing governance path: {rel}")

    git_repo = is_git_repo(root)
    statuses = git_status(root) if git_repo else {}

    if (root / "temp").exists() and not temp_is_ignored(root):
        add(findings, strict_level, "temp/ is not ignored by Git")

    for path in root.iterdir():
        if not path.is_file():
            continue
        if any(fnmatch.fnmatch(path.name, pattern) for pattern in DISPOSABLE_ROOT_PATTERNS):
            rel = path.name
            code = statuses.get(rel, "")
            if not git_repo or is_new_status(code):
                add(findings, "ERROR", f"Disposable file is in repository root: {rel}; move it under temp/")

    if git_repo:
        for rel_text, code in statuses.items():
            rel = Path(rel_text)
            if not is_new_status(code) or not is_test_name(rel):
                continue
            parts = rel.parts
            if not parts or parts[0] == "test":
                continue
            add(
                findings,
                strict_level,
                f"New test-like file is outside test/: {rel_text}. Preserve an established repository convention only when intentional.",
            )

    tools_md = root / "TOOLS.md"
    registry_text = tools_md.read_text(encoding="utf-8", errors="replace") if tools_md.exists() else ""
    tools_dir = root / "tools"
    for tool_path in iter_tool_files(tools_dir):
        rel = tool_path.relative_to(root).as_posix()
        if rel not in registry_text:
            add(findings, strict_level, f"Tool is not referenced in TOOLS.md: {rel}")

    if git_repo:
        tool_changes = [
            rel for rel in statuses if rel == "tools" or rel.startswith("tools/")
        ]
        registry_changed = "TOOLS.md" in statuses
        if tool_changes and not registry_changed:
            add(
                findings,
                "WARN" if not args.strict else "ERROR",
                "Files under tools/ changed but TOOLS.md has no working-tree change; verify that capability and usage documentation is still current.",
            )

    errors = [f for f in findings if f.level == "ERROR"]
    warnings = [f for f in findings if f.level == "WARN"]

    print(f"Workspace root: {root}")
    if not findings:
        print("PASS: no governance violations detected")
        return 0

    for finding in findings:
        print(f"{finding.level}: {finding.message}")

    print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
