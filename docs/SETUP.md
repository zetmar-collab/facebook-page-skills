# Setup

A step-by-step guide from zero to your first approved post.

## 1. Prerequisites

| Need | Why | Check |
|------|-----|-------|
| Claude Code | runs the skills | `claude --version` |
| Python 3.8+ | `lint.py`, `beats.py` | `python3 --version` (`python --version` on Windows) |
| A Facebook **Page** | publishing target | you see "Page" tools in Meta Business Suite |
| A Composio account | the bridge to Facebook | https://composio.dev |

## 2. Install the skills

```bash
./install.sh            # or: powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Restart Claude Code. Type `/fb-` and you should see the twelve skills.

## 3. Connect Facebook through Composio

1. Make sure the Composio MCP server is added to Claude Code (follow Composio's own
   quick start for Claude Code).
2. Run `/fb-start`. If Facebook is not connected, the skill asks Composio for an
   authorisation link and shows it. Open it, log in to Facebook, and approve.
   - Links expire after a few minutes; ask for a new one if it does.
   - Authorise with the account that **manages the Page**.
3. Tell Claude when you are done. The skill lists the connected accounts and checks
   that the status is ACTIVE.
4. `fb-start` then lists your Pages (`FACEBOOK_LIST_MANAGED_PAGES`). Pick the main
   one; its **id** is saved to `~/.claude/facebook/config.md`.

### Things that commonly go wrong

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| "No active connection for toolkit facebook" | not authorised, or link expired | repeat step 3 |
| Your Page is not in the list | the authorised account does not manage it | authorise with the right account, or check Page roles |
| Error code 190 / OAuthException | expired or revoked token | reconnect Facebook in Composio |
| Error #10 when reading comments or insights | missing engagement-read permission | the skills fall back to pasted data |
| 400 (#100) when publishing a photo | the image URL is not publicly fetchable | host the image at a public URL |
| 400 (#100) when scheduling | `scheduled_publish_time` missing or in the past | use a future timestamp |
| You post from a personal profile | Composio supports Pages only | use the "ready-to-paste text" mode |

> The Facebook tool names (`FACEBOOK_CREATE_POST`, `FACEBOOK_GET_PAGE_POSTS`, ...)
> and the pitfalls above come from Composio's tool search at the time of writing.
> Composio may rename or change tools; `fb-publish` always re-queries
> `COMPOSIO_SEARCH_TOOLS` and `COMPOSIO_GET_TOOL_SCHEMAS` before the first call.

## 4. Build your voice

Run `/fb-voice`. It reads what exists, asks one batched question (who you are on
Facebook, default register, reader, whether to use the essay register at all) and
writes `~/.claude/facebook/voice.md`. Open the file and fill in the `{{...}}`
fields: your own phrases, your real numbers, your off-limits topics.

Every other skill reads this file. The better it is, the less you edit.

## 5. Your first post

```
/fb-post why you should not trust a chatbot's first answer
```

You get two variants, an image prompt, and a receipt. When you like one:

```
publish A
```

`fb-publish` shows the Page, text, link, image and time and asks for a yes. Say
"yes" and it publishes, verifies with `FACEBOOK_GET_POST`, logs the post id to
`log.md`, and returns the permalink.

To schedule instead: `schedule B for Thursday 19:00`. Confirm the time in your own
timezone (set in `config.md`) and watch for daylight-saving changes.

## 6. The weekly rhythm

| When | Run |
|------|-----|
| Once a week, same day | `/fb-plan` |
| Each slot | `/fb-post ...` or `/fb-reel ...`, then publish |
| Daily, 15 min | comment under your posts (`/fb-reply`) and on others' (`/fb-comment`) |
| After 4-6 weeks | `/fb-audit` and feed the result back to `/fb-plan` |

## Uninstall

Delete `~/.claude/skills/fb-*`. Your `~/.claude/facebook/` folder holds your own
files; delete it only if you want your voice, config and log gone. To revoke
Facebook access, disconnect the account in Composio and remove the app in your
Facebook settings.
