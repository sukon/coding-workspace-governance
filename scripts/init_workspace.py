#!/usr/bin/env python3
"""Initialize repository layout for coding workspace governance."""

from __future__ import annotations

import argparse
from pathlib import Path

BEGIN = "<!-- BEGIN CODING WORKSPACE GOVERNANCE -->"
END = "<!-- END CODING WORKSPACE GOVERNANCE -->"


def append_once(path: Path, block: str) -> str:
    if not path.exists():
        path.write_text(block.rstrip() + "\n", encoding="utf-8")
        return "created"

    text = path.read_text(encoding="utf-8")
    if BEGIN in text and END in text:
        start = text.index(BEGIN)
        end = text.index(END, start) + len(END)
        updated = text[:start].rstrip() + "\n\n" + block.rstrip() + "\n" + text[end:].lstrip("\n")
        path.write_text(updated, encoding="utf-8")
        return "updated"

    separator = "" if not text.strip() else "\n\n"
    path.write_text(text.rstrip() + separator + block.rstrip() + "\n", encoding="utf-8")
    return "appended"


def ensure_gitignore(root: Path) -> str:
    path = root / ".gitignore"
    line = "temp/"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        entries = {item.strip() for item in text.splitlines()}
        if line in entries or "/temp/" in entries:
            return "unchanged"
        separator = "" if not text.strip() else "\n"
        path.write_text(text.rstrip() + separator + "\n# Disposable coding-agent artifacts\n" + line + "\n", encoding="utf-8")
        return "updated"

    path.write_text("# Disposable coding-agent artifacts\n" + line + "\n", encoding="utf-8")
    return "created"


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a governed coding workspace.")
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument(
        "--install-agent-rules",
        action="store_true",
        help="Install or refresh the managed workspace policy block in AGENTS.md.",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    skill_root = Path(__file__).resolve().parent.parent
    tools_template = skill_root / "assets" / "TOOLS.md.template"
    agents_template = skill_root / "assets" / "AGENTS.workspace-policy.md"

    root.mkdir(parents=True, exist_ok=True)
    created = []
    existed = []

    for rel in ("tools", "tests", "temp", "temp/logs", "temp/responses", "temp/artifacts"):
        path = root / rel
        if path.exists():
            existed.append(rel + "/")
        else:
            path.mkdir(parents=True, exist_ok=True)
            created.append(rel + "/")

    tools_md = root / "TOOLS.md"
    if tools_md.exists():
        tools_status = "unchanged"
    else:
        tools_md.write_text(tools_template.read_text(encoding="utf-8"), encoding="utf-8")
        tools_status = "created"

    gitignore_status = ensure_gitignore(root)

    agents_status = "not requested"
    if args.install_agent_rules:
        block = agents_template.read_text(encoding="utf-8")
        agents_status = append_once(root / "AGENTS.md", block)

    print(f"Workspace root: {root}")
    if created:
        print("Created directories: " + ", ".join(created))
    if existed:
        print("Existing directories: " + ", ".join(existed))
    print(f"TOOLS.md: {tools_status}")
    print(f".gitignore: {gitignore_status}")
    print(f"AGENTS.md policy: {agents_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
