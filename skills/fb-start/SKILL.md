---
name: fb-start
description: >-
  Entry point for the fb-* Facebook Page skill pack. Checks configuration, the
  Facebook connection through Composio and the state files in
  ~/.claude/facebook/, then tells the user which skill to run next. Use when
  the user says "fb", "facebook start", "facebook pack", "what can I do on
  facebook", "set up facebook", "connect facebook", or the first time any fb-*
  skill is used in a session.
---

# fb-start

Router and readiness check. Publishes nothing.

## The pack at a glance

```
              fb-voice  (the page owner's voice, single source of truth)
                  |
  fb-plan -> fb-post / fb-reel -> fb-human -> fb-publish -> Facebook Page
     ^                                                          |
     |                   fb-audit  <-- insights from the Page --+
     |                   fb-reply  <-- comments under own posts
  fb-repurpose (long source -> a week of posts)
  fb-comment (other people's posts)       fb-profile (the Page itself)
```

| The user wants to | Run |
|-------------------|-----|
| set or fix their writing voice | `/fb-voice` |
| plan the week | `/fb-plan` |
| write a post (text, photo, several photos, link) | `/fb-post` |
| script a short video / reel | `/fb-reel` |
| check and clean a text | `/fb-human` |
| publish or schedule through Composio | `/fb-publish` |
| see what works on the Page | `/fb-audit` |
| answer comments under their own posts | `/fb-reply` |
| comment on other people's posts | `/fb-comment` |
| turn one long source into a week of posts | `/fb-repurpose` |
| score and rewrite the Page's profile | `/fb-profile` |

## Startup checks

1. **State files** in `~/.claude/facebook/`: `voice.md`, `config.md`, `log.md`,
   `plan.md`. No `voice.md` -> run `/fb-voice`. No `config.md` -> copy the
   template from the pack's `templates/` folder (the installer does this) and ask
   for the missing fields.
2. **Facebook connection.** Call `COMPOSIO_SEARCH_TOOLS` (toolkit `facebook`)
   and read `toolkit_connection_statuses`. If `has_active_connection` is false,
   call `COMPOSIO_MANAGE_CONNECTIONS` for `facebook`, show the returned link as a
   clickable markdown link, and wait for the user to confirm. Then list the
   accounts and check the status is ACTIVE. Never run a Facebook tool without an
   active connection.
3. **A Page, not a profile.** Composio's Facebook toolkit supports **Facebook
   Pages only**, not personal profiles. Call `FACEBOOK_LIST_MANAGED_PAGES`
   (paginate with `paging.cursors.after`), show names and ids, and ask which one
   is the main Page. If the user's Facebook presence turns out to be a personal
   profile, say plainly that publishing through the API is not possible; the pack
   then works in "ready-to-paste text" mode and `/fb-publish` handles that.
4. **Tokens.** `LIST_MANAGED_PAGES` can return a per-Page `access_token`. That is a
   secret. Never print it, write it to a file, or paste it into a reply.

## `~/.claude/facebook/config.md`

See `templates/config.template.md`. Key fields: `page_name`, `page_id` (the id
only, never a token), `language` (default `en`), `timezone`, `publish_mode`
(`gate`), `link_policy`, `hashtags_max`.

`publish_mode` stays `gate`. Change it only on an explicit instruction from the
user, and even then ask before the first publication of each session.

## Output

A short readiness card: which files exist, whether Facebook is connected, which
Page, and one sentence: "start with X". Nothing more.
