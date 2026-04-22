# Project State

Current status as of 2026-04-22.

## Current Focus

Configured Speech-to-Text (Groq Whisper) on both Telegram bots (opencode-telegram-bot and zazentimer).

## Completed (this cycle)

- [x] Found Groq API key in `/home/georg/repos/openclaw/.secrets/.env`
- [x] Configured STT on ZaZen timer bot (`STT_API_URL`, `STT_API_KEY`, `STT_MODEL=whisper-large-v3-turbo`)
- [x] Configured STT on main OpenCode Telegram bot (same keys, same turbo model)
- [x] Verified both bot services restarted successfully
- [x] Tested voice message transcription via Telegram (confirmed working)

## Pending

None

## Blockers

None

## Next Session Suggestion

Consider enabling TTS (Text-to-Speech) on either bot for two-way voice interaction. TTS code already exists in the bot (`src/tts/client.ts`), only needs `TTS_API_URL` and `TTS_API_KEY` in `.env`.
