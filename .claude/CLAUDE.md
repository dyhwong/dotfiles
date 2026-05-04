# Claude guidelines for this repo

Repo layout and conventions are documented in README.md — read that first.

## What to avoid

- Don't hardcode absolute paths — use `$HOME`, `$PWD`, or `~`.
- Don't add machine-specific config — this repo is shared across machines.
- Don't commit secrets or tokens.
- `CLAUDE.md` is symlinked to `~/.claude/CLAUDE.md` and affects global Claude behavior — don't add project-specific content there.

## Commit style

The global `CLAUDE.md` covers the full PR style guide. Dotfiles-specific patterns:

- Most commits touch one file for one reason — keep them that way.
- Name the target explicitly: "Add git-absorb installation to setup.sh", not "Update setup.sh".
- No PR body needed for straightforward additions or config tweaks — the title is enough.

## When making changes

- Adding a tool: add an install block to `setup.sh` following the idempotency and Mac/Linux branching pattern already there.
- Adding a script: drop it in `bin/` (executable); `setup.sh` auto-symlinks it — no other changes needed.
- Config changes: edit the right dotfile per the table in README.md, not `setup.sh`.
