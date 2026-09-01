# Project State

Current status as of 2026-09-01.

## Current Focus

Session-deliverable tooling: files can now be pushed into the user's Telegram
chat from any opencode session.

## Completed (this cycle)

- [x] Added `skills/telegram-send/SKILL.md` — sends documents/photos to the user's
      private Telegram chat via the Bot API, reusing the local bot's credentials
      (`~/.config/oc-tg-bot*/.env`); available in all sessions via the
      `~/.config/opencode/skills` symlink → this repo's `skills/` (verified 2026-09-01)
- [x] Documented bot topology (4 systemd user services `oc-tg-bot*`, all attached to
      `opencode.service` on 127.0.0.1:62764) and secret-handling rules in the skill

## Pending

None

## Blockers

None

## Next Session Suggestion

Verify `telegram-send` appears in the available skills after the next opencode
restart and works end-to-end from a fresh session.
