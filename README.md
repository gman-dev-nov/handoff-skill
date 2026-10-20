# handoff — a session handoff skill for any AI agent

[Русская версия](README.ru.md)

`handoff` turns any chat session with an AI agent into an exhaustive
`HANDOFF.md`, so another agent (or a human) can continue the work without
having seen the session: task history, what is done and what is not, what
worked and what failed, file state, commands to reproduce, environment
pitfalls, open questions for you (Q1..Qn with answer options) and next steps.

One source file — [`SKILL.md`](SKILL.md) — works as a native skill in agents
that support the `SKILL.md` format and as plain instructions everywhere else.
It has no dependencies and does not rely on any agent's internal APIs.

See what the result looks like: [`examples/HANDOFF.example.md`](examples/HANDOFF.example.md).

## Usage

Once installed, ask the agent at the end of a session or after a milestone:

> handoff

or in your own words — "pass the context to another agent", "summarize the
session for the next agent", "save progress". Russian phrasing works too
(«сделай хэндоф», «передай контекст другому агенту»). The document is written
in the language of the session.

The agent writes `HANDOFF.md` to the project root (or updates the existing
one), verifies facts against the file system, redacts secrets and replies with
the file path and the number of open questions. Answer them briefly
("Q1-a, Q3-b") and the agent updates the document.

## Install

### Let the agent install it

Paste this into Claude Code, Codex or another agent with file system access:

```text
Install the handoff skill from https://github.com/gman-dev-nov/handoff-skill:
copy its SKILL.md into the skills directory your harness reads
(handoff/SKILL.md inside it), then tell me how to invoke it.
```

### Claude Code

```bash
mkdir -p ~/.claude/skills/handoff
curl -fsSL https://raw.githubusercontent.com/gman-dev-nov/handoff-skill/main/SKILL.md -o ~/.claude/skills/handoff/SKILL.md
```

Invoke with `/handoff` or any of the phrases above.

### Codex, ZCode and other agents that read `~/.agents/skills`

```bash
mkdir -p ~/.agents/skills/handoff
curl -fsSL https://raw.githubusercontent.com/gman-dev-nov/handoff-skill/main/SKILL.md -o ~/.agents/skills/handoff/SKILL.md
```

### Other agents with `SKILL.md` support

Put `SKILL.md` into `handoff/SKILL.md` inside the skills directory from your
agent's documentation. The file is a standard skill: YAML frontmatter with
`name` and `description`, then the instructions.

### Chat assistants without skills (ChatGPT, Gemini, any LLM)

Use [`system-prompt.md`](system-prompt.md) — the same instructions without
the skill frontmatter:

- paste it into the custom instructions of a Custom GPT, Project, Gem or
  similar (5.5k characters, fits the 8k Custom GPT limit);
- or set it as the system prompt when calling a model through an API;
- or send it as the first message: "Follow these instructions when I ask for
  a handoff".

Without file tools the assistant returns the document as a single code block
for you to save.

## Development

`SKILL.md` is the only file to edit. `system-prompt.md` is generated
from it (same body without frontmatter) — do not edit it by hand.

```bash
python3 build.py            # regenerate system-prompt.md
python3 build.py --install  # also copy SKILL.md into ~/.agents/skills and ~/.claude/skills
python3 build.py --check    # CI: fail if the generated file is stale or over the limit
```

Edit `SKILL.md` → `python3 build.py` → commit both files. CI runs
`--check` on every push and pull request.

## Why a skill and not a plugin

A plugin bundles several skills, commands, hooks or MCP servers. Here there is
one workflow and one output document, so a single `SKILL.md` is enough and
stays portable across agents.

## License

[MIT](LICENSE)
