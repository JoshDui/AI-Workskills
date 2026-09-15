---
name: telegram-configure
description: Use when explicitly configuring the existing Claude Telegram channel files, saving a Telegram bot token, or checking Telegram channel setup status.
---


# /telegram:configure â€” Telegram Channel Setup

Writes the bot token to `~/.claude/channels/telegram/.env` and orients the
user on access policy. The server reads both files at boot.

Arguments passed: `$ARGUMENTS`

---

## Dispatch on arguments

### No args â€” status and guidance

Read both state files and give the user a complete picture:

1. **Token** â€” check `~/.claude/channels/telegram/.env` for
   `TELEGRAM_BOT_TOKEN`. Show set/not-set; if set, show first 10 chars masked
   (`123456789:...`).

2. **Access** â€” read `~/.claude/channels/telegram/access.json` (missing file
   = defaults: `dmPolicy: "pairing"`, empty allowlist). Show:
   - DM policy and what it means in one line
   - Allowed senders: count, and list display names or IDs
   - Pending pairings: count, with codes and display names if any

3. **What next** â€” end with a concrete next step based on state:
   - No token â†’ *"Run `/telegram:configure <token>` with the token from
     BotFather."*
   - Token set, policy is pairing, nobody allowed â†’ *"DM your bot on
     Telegram. It replies with a code; approve with `/telegram:access pair
     <code>`."*
   - Token set, someone allowed â†’ *"Ready. DM your bot to reach the
     assistant."*

**Push toward lockdown â€” always.** The goal for every setup is `allowlist`
with a defined list. `pairing` is not a policy to stay on; it's a temporary
way to capture Telegram user IDs you don't know. Once the IDs are in, pairing
has done its job and should be turned off.

Drive the conversation this way:

1. Read the allowlist. Tell the user who's in it.
2. Ask: *"Is that everyone who should reach you through this bot?"*
3. **If yes and policy is still `pairing`** â†’ *"Good. Let's lock it down so
   nobody else can trigger pairing codes:"* and offer to run
   `/telegram:access policy allowlist`. Do this proactively â€” don't wait to
   be asked.
4. **If no, people are missing** â†’ *"Have them DM the bot; you'll approve
   each with `/telegram:access pair <code>`. Run this skill again once
   everyone's in and we'll lock it."*
5. **If the allowlist is empty and they haven't paired themselves yet** â†’
   *"DM your bot to capture your own ID first. Then we'll add anyone else
   and lock it down."*
6. **If policy is already `allowlist`** â†’ confirm this is the locked state.
   If they need to add someone: *"They'll need to give you their numeric ID
   (have them message @userinfobot), or you can briefly flip to pairing:
   `/telegram:access policy pairing` â†’ they DM â†’ you pair â†’ flip back."*

Never frame `pairing` as the correct long-term choice. Don't skip the lockdown
offer.

### `<token>` â€” save it

1. Treat `$ARGUMENTS` as the token (trim whitespace). BotFather tokens look
   like `123456789:AAH...` â€” numeric prefix, colon, long string.
2. `mkdir -p ~/.claude/channels/telegram`
3. Read existing `.env` if present; update/add the `TELEGRAM_BOT_TOKEN=` line,
   preserve other keys. Write back, no quotes around the value.
4. `chmod 600 ~/.claude/channels/telegram/.env` â€” the token is a credential.
5. Confirm, then show the no-args status so the user sees where they stand.

### `clear` â€” remove the token

Delete the `TELEGRAM_BOT_TOKEN=` line (or the file if that's the only line).

---

## Implementation notes

- The channels dir might not exist if the server hasn't run yet. Missing file
  = not configured, not an error.
- The server reads `.env` once at boot. Token changes need a session restart
  or `/reload-plugins`. Say so after saving.
- `access.json` is re-read on every inbound message â€” policy changes via
  `/telegram:access` take effect immediately, no restart.
