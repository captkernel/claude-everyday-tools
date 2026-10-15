# claude-everyday-tools

Practical, everyday tools — Claude prompts for life admin, plus a small app.

- **commands/** — `/flights` (skeptical flight-deal scanner), `/farecheck` (real pricing mechanisms vs myths), `/focus` (break a stuck task into 1-minute steps), `/learn` (4-hour "make me functional" crash plan). `cp commands/*.md ~/.claude/commands/`.
- **prompts/** — the full flight-deal pack and the personal-coach pack (focus/executive-function + accelerated learning).
- **wardrobe-app/** — a "Clueless"-style digital closet + outfit suggester (Python CLI, tested). A standalone bonus app.

## Install

**Claude Code (plugin):**
```
/plugin marketplace add captkernel/plugins
/plugin install everyday-tools@captkernel
```
Manual: copy `skills/<name>/` into `~/.claude/skills/`. claude.ai: upload a zip from `skills/dist/`.

## Use in Claude chat (claude.ai)

These tools are also packaged as **Agent Skills** under `skills/`, so they work in
**claude.ai**, not just Claude Code:

1. Grab a ready-to-upload zip from `skills/dist/` (one per skill).
2. In claude.ai → **Settings → Capabilities → Skills**, upload the zip (Pro/Max/Team/
   Enterprise). Or add it to a **Project** so it's available in that project's chats.
3. Each skill auto-triggers from its description — e.g. ask *"make this sound human"*
   and the `humanize` skill kicks in; no slash command needed.

In **Claude Code**, copy a skill folder into `~/.claude/skills/` (global) or the
project's `.claude/skills/`. The slash commands in `commands/` remain the quick path there.


---

_Curated/built from techniques shared by creators on Instagram (May 2026); marketing hype and inflated stats stripped out. Prompt text is rewritten, not copied; source handles are credited in the pack files._

Maintainers: bump "version" in .claude-plugin/plugin.json on every release, or plugin users never receive the update.
