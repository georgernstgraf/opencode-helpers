---
name: telegram-send
description: "Send files, documents, and photos into the user's Telegram chat via the locally running bot's credentials. Use when: user asks to send a file to Telegram, 'schick mir X ins Telegram', 'als Attachment schicken', or wants deliverables pushed to their phone chat."
---

# Telegram Send Skill

Deliver files (documents, images) to the user's Telegram chat using the Telegram
Bot API with the credentials of the locally running Telegram bot. No plugin or
restart required.

## Architecture

- `opencode.service` (systemd user service, `127.0.0.1:62764`) is the backend.
- Four Telegram bot frontends (systemd user services, all `@grinev/opencode-telegram-bot`),
  all attached to the same opencode instance:
  - `oc-tg-bot` — default bot, Telegram handle `@schurlixBot`
  - `oc-tg-bot-home`, `oc-tg-bot-experimental`, `oc-tg-bot-zazentimer`
- Per instance, config lives at `~/.config/oc-tg-bot*/`:
  - `settings.json` — `currentSession`, `currentProject`, `pinnedMessageId`
  - `.env` — `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USER_ID`, `OPENCODE_API_URL`,
    `OPENCODE_SERVER_PASSWORD`, STT/TTS settings
  - `logs/bot-YYYY-MM-DD.log` — **timestamps are UTC** (local time is CEST = UTC+2)

## Identifying the Serving Bot

The active bot instance for the current chat can be found by comparing logs:

```bash
grep -E 'promptAsync|Using existing session' ~/.config/oc-tg-bot*/logs/bot-$(date +%Y-%m-%d).log | tail
```

Cross-check the reported session id against `currentSession.id` in each
`~/.config/<instance>/settings.json`. The instance whose log shows the most
recent prompt for that session is the serving bot.

## Sending Files

### 1. Load credentials silently

```bash
ENV_FILE=~/.config/oc-tg-bot/.env   # replace with the serving bot's instance dir
TOKEN=$(grep -E '^TELEGRAM_BOT_TOKEN=' "$ENV_FILE" | cut -d= -f2- | tr -d '"' | tr -d "'")
CHAT=$(grep -E '^TELEGRAM_ALLOWED_USER_ID=' "$ENV_FILE" | cut -d= -f2- | tr -d '"' | tr -d "'")
```

### 2. Verify the chat

For a private chat, `chat_id` equals `TELEGRAM_ALLOWED_USER_ID`:

```bash
curl -s "https://api.telegram.org/bot$TOKEN/getChat?chat_id=$CHAT" \
  | jq '{ok, type: .result.type, title: .result.title, first_name: .result.first_name}'
```

Expected: `{"ok": true, "type": "private", ...}`.

### 3. Send

Documents (any file type):

```bash
curl -s -F "chat_id=$CHAT" -F "caption=Short description" \
  -F "document=@/absolute/path/file.ext" \
  "https://api.telegram.org/bot$TOKEN/sendDocument" \
  | jq '{ok, doc: .result.document.file_name, err: .description}'
```

Images (inline photo previews): use `sendPhoto` with `-F "photo=@/path/img.png"`.

Check `"ok": true` and a non-null `file_name`; on failure `.err` carries
Telegram's error description.

## Security Rules

- **Never** echo, print, or log `TELEGRAM_BOT_TOKEN`, `.env` contents, or
  `OPENCODE_SERVER_PASSWORD`. Tokens exist only as shell variables inside a
  single command invocation.
- Do not `cat` `.env` files. Parse fields with `grep`/`cut` as above.
- Keep secrets out of captions and commit messages.

## Pitfalls

- **Do not call `getUpdates`** — it conflicts with the running bot's polling
  (HTTP 409). Use `getChat`/`sendDocument`/`sendPhoto` only.
- Log timestamps are UTC; convert when correlating with local wall-clock.
- `sendDocument` accepts files up to 50 MB (Telegram Bot API limit).
- Group chats are not yet mapped: `getChat` with the allowed user id only
  resolves the private chat. For a group, ask the user for the chat id or
  inspect the bot's data store.
- Files sent this way do not appear in the opencode session transcript —
  tell the user to check the chat.

## Alternatives

- **User-side download:** the grinev bot supports `/ls` to browse the
  workspace and 📎 attach/download files directly in the chat. Good enough
  when the user initiates.
- **Durable agent-side tool:** the plugin `opencode-telegram-send-file`
  (npm) registers a send tool inside opencode. Requires adding it to the
  `plugin` array in opencode config and an opencode restart. Only worth it
  if file delivery becomes a frequent, first-class need.
