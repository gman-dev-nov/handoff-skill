#!/usr/bin/env python3
"""Builds the skill distributions from the single source SKILL.md.

- system-prompt.md — the same body without YAML frontmatter plus a header,
  for assistants without skill support: a system prompt, custom instructions
  of a chat app (Custom GPT, Project, Gem), or the first message (kept under
  8000 chars to fit the Custom GPT instructions field).
- Install copies: ~/.agents/skills/handoff/ (Codex, ZCode and other agents
  that read ~/.agents/skills) and ~/.claude/skills/handoff/ (Claude Code).

Usage: python3 build.py [--install] [--check]
  --install  also copy SKILL.md into the install directories
  --check    do not write anything; exit 1 if system-prompt.md is stale
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROMPT_FILE = os.path.join(HERE, "system-prompt.md")
PROMPT_LIMIT = 8000  # Custom GPT "Instructions" field limit, in characters
INSTALL_DIRS = [
    os.path.expanduser("~/.agents/skills/handoff"),
    os.path.expanduser("~/.claude/skills/handoff"),
]

def render_prompt():
    src = open(os.path.join(HERE, "SKILL.md"), encoding="utf-8").read()
    if src.startswith("---\n"):
        end = src.index("\n---\n", 4)
        body = src[end + len("\n---\n"):].strip()
    else:
        body = src.strip()
    return (
        "# Operating mode: writing HANDOFF documents\n\n"
        "These instructions are your standing operating mode.\n\n"
        + body + "\n"
    )

def main(install=False, check=False):
    prompt = render_prompt()
    if len(prompt) > PROMPT_LIMIT:
        sys.exit(f"system-prompt.md: {len(prompt)} chars, over the {PROMPT_LIMIT} limit")

    if check:
        current = open(PROMPT_FILE, encoding="utf-8").read() if os.path.exists(PROMPT_FILE) else ""
        if current != prompt:
            sys.exit("system-prompt.md is stale: run python3 build.py and commit the result")
        print(f"system-prompt.md is up to date ({len(prompt)}/{PROMPT_LIMIT} chars)")
        return

    with open(PROMPT_FILE, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"system-prompt.md: {len(prompt)}/{PROMPT_LIMIT} chars")

    if install:
        for d in INSTALL_DIRS:
            os.makedirs(d, exist_ok=True)
            shutil.copy(os.path.join(HERE, "SKILL.md"), os.path.join(d, "SKILL.md"))
            print(f"installed: {d}/SKILL.md")

if __name__ == "__main__":
    main(install="--install" in sys.argv, check="--check" in sys.argv)
