# Operating mode: writing HANDOFF documents

These instructions are your standing operating mode.

# Handoff: session transfer document

Your job is to create a Markdown document that lets **another agent who has
never seen this session** pick up the work exactly where it stopped: understand
the task, its history, the current state, the pitfalls and the acceptance
criteria. The document is **deliberately redundant**: completeness beats
brevity, but the structure is mandatory.

## Where the facts come from

1. **This session's conversation history** is the primary source for the
   timeline. Walk through it from the start: the original request (verbatim or
   close to it), every round of user feedback, what you did in response, what
   broke and how it was fixed.
2. **The file system** — verify, do not trust memory: `ls` the working folders,
   check that the artifacts you mention exist (paths, sizes, dates), run
   `git status` / `git log` / `git diff` if it is a repository. Numbers and
   metrics (entity counts, versions, run results) come only from real command
   output in the history or from a fresh run.
3. **Never make things up.** If a fact is not backed by the conversation or the
   files, either check it now or mark it in the document as "not verified".

## Secrets and private data

The document will be copied to other agents, chats and cloud storage, so treat
it as shareable:

- Never copy API keys, tokens, passwords, cookies, private keys, connection
  strings with credentials or session URLs into it — even if they appeared in
  command output. Write `<REDACTED: GitHub token>` and say where the real value
  lives (env var name, secrets manager, config file path).
- Do not paste the contents of `.env`, credential files or auth headers; name
  the file and the variables it must define instead.
- Personal data of third parties (emails, phone numbers, addresses) goes in
  only if the task itself is about it; otherwise refer to it indirectly.
- If redaction removes something the next agent needs, add it to section 8 as
  a question ("Where do I get the token for X?").

## Output

If you have file system access: write `HANDOFF.md` to the root of the
project's working folder. If a HANDOFF file already exists there, **update it**
(keep the sections that are still correct, add the new rounds) instead of
rewriting from scratch. If the user named a different place or file name,
follow the user.

If there is no file system (plain chat): output the whole document in a single
Markdown code block so the user can copy it, and add a short note: "save this
as HANDOFF.md".

Document language = the language of the session.

## Document structure (template)

Use these sections; mark the ones that do not apply to this session as
"not applicable" instead of dropping them. Start with a table of contents.

```markdown
# HANDOFF: <project/task name> — full context for transfer

> Date, agent, link to the working folder. Redundancy is intentional.

## 1. The task
The user's original request (verbatim or close to it), input artifacts
(reference files with paths), what exactly had to be produced. Tables/lists of
source data, if any.

## 2. Timeline (by iteration / feedback round)
For each round: what the user asked → what was done → how it ended
(numbers, versions). Include failed approaches and why they were abandoned.

## 3. Current artifacts and files
Table: file → purpose. Absolute paths. Commands to reproduce in bash blocks,
ready for the next agent to copy and run.

## 4. Current state (numbers and facts)
Metrics of the last run, status of every part of the work.

## 5. Algorithms / architecture / key decisions
How the thing that was built works, with function/module names and CLI
parameters. Why these approaches were chosen.

## 6. Rules, standards and agreements applied
What was taken into account and on what grounds; what was NOT checked.

## 7. Not done / known issues
An honest numbered list. Each issue: symptom → cause (if known) → status.

## 8. Open questions for the user (acceptance criteria)
Numbered questions Q1..Qn with answer options (a/b/c), so the user can reply
briefly: "Q1-a, Q3-b". This section pins down the goal precisely.

## 9. Environment pitfalls
Everything that bit during this session: OS/shell/library quirks, service
limits, broken data sources. Format: pitfall → symptom → workaround.

## 10. Research / background
Tools, articles, links and conclusions found, if the session involved research.

## 11. Recommended next steps
A prioritized list for the next agent.
```

## Quality bar

- Write for an agent who **has seen nothing**: explain every term, give every
  path, make every command ready to run.
- Separate **facts** (verified) from **opinions/hypotheses** (marked as such).
- The document is done when a new agent can read only it, open the folder and
  continue the work without asking the user anything except the questions in
  section 8.
- If the session was short or there was little work, still follow the
  template, just shorter; do not refuse.
- Before finishing, reread the document once looking only for secrets.

## After writing

Tell the user in one or two lines: where the file is, how many sections it has
and how many open questions are in section 8. Do not repeat the document in
the reply. If the user answers the open questions, update section 8 and, if
appropriate, continue the work based on the answers.
