---
name: fb-comment
description: >-
  Writes comments under other people's Facebook posts (Pages, groups, public
  profiles) that read as a person with an opinion, not a bot. Use when the user
  pastes someone else's post and says "comment on this", "what do I say here",
  "reply to this post", "join the discussion", or wants a batch of comments for the
  daily conversation round.
---

# fb-comment

A comment under a big post reaches more people than most of a Page's own posts, and
it is the one place where a stranger can click straight through to a Page. A
generic comment is worse than none: it adds nothing and marks the account as
engaging for show.

## Input

The user pastes the post text (or a screenshot) with the author's name and where it
lives (Page, group). If they give a link you cannot open, ask them to paste it. Do
not browse Facebook or scrape the feed. Do not log in.

## Nine comment types

| # | Type | When | Shape |
|---|------|------|-------|
| 1 | **Add a datum** | the post claims, you have a number | "For us it was: 40% of..." |
| 2 | **The missing case** | the post is right but incomplete | "This holds until {condition}." |
| 3 | **Polite disagreement** | you genuinely disagree | first where you agree, then the fork |
| 4 | **Extend one line** | one line in it is the good one | quote it, build on it |
| 5 | **The skipped question** | the post avoided the hard part | one specific question |
| 6 | **Receipt** | you did the thing described | what happened, two sentences |
| 7 | **Correction** | a factual error | be sure, brief, kind |
| 8 | **Reframe** | right facts, wrong frame | "Another way to read this:" |
| 9 | **One-liner** | it needs nothing, you want presence | under 10 words, funny or true |

Choose by what the post actually is. Never default to 1.

## Rules

- **One to three sentences.** A long comment collapses behind "See more".
- **Never open with** "Great post", "Love this", "So true", "Exactly", or the author's
  first name with an exclamation mark. All of them are invisible.
- **Emoji alone** is not a comment. No emoji as the first character.
- **Do not restate the post.** Everyone just read it.
- **One idea.** Two points read as a hijack.
- **Say the specific thing.** If the comment would fit under any post on the topic,
  it is noise.
- **Zero selling.** No offer, no link, no "check out my Page". It is the fastest way
  to be removed from a group and blocked by the person you wanted to reach. Groups
  have their own rules: read them before the owner writes anything, and do not
  break them.
- **Early counts for more.** A comment in the first hour on a post that then grows
  is carried with it.
- Real experience only: types 1 and 6 need a number or event from the owner. If
  there is none, pick another type; do not invent.

## Output

Two options of different types, labelled, plus one line on which to post and why.
Both through `fb-human`.

```
COMMENT  (under @page's post about AI tool prices)

[6 - Receipt]
I tested it on my own account for a week. The cheaper model came out dearer,
because I had to fix the result twice. You pay for the task, not the price list.

[3 - Polite disagreement]
Agreed on the per-token prices. I would disagree that they are enough to compare...

Post the first: it has something concrete and gives something back.
```

## Batch mode

For the conversation round: 5-10 pasted posts in one message -> one comment for each
in one block. Append a note to `~/.claude/facebook/log.md` of who was commented on
this week. Commenting on the same three accounts every day is visible and looks like
exactly what it is.

## Never

Never post under other people's posts (neither through Composio nor browser
automation). Automated engagement violates Facebook's terms and ends in account
restrictions. The skill writes the comment; the owner pastes it.
