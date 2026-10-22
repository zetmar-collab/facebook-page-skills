---
name: fb-audit
description: >-
  Post-mortem of what the page owner has already published on a Facebook Page:
  which posts worked, why, and what to stop doing. Pulls data through Composio
  (posts, reactions, comments, shares, insights) or takes pasted screenshots. Use
  when the user says "what's working", "why did this flop", "analyse my page",
  "content audit", "facebook stats", "what should I do more of", "look at my posts".
---

# fb-audit

The only honest source of what works on a Page is that Page. Every rule in this
pack is an assumption. The last 30 posts are the evidence.

## Data

### Through Composio (default, read-only)

The connection must be ACTIVE (`/fb-start`). Call tools through
`COMPOSIO_MULTI_EXECUTE_TOOL`.

1. `FACEBOOK_GET_PAGE_POSTS` for `page_id`: `limit` around 25-50, paginate with
   the `paging.cursors.after` cursor (not `paging.next`). Request each field edge
   once; duplicating the `comments` edge causes error 2500. On a "reduce data"
   error, shrink the field list or `limit`. Narrowing `since/until` too far returns
   `{data: []}`.
2. `FACEBOOK_GET_POST_INSIGHTS` for each `post_id`. **Do not assume** metric names:
   returned metrics can be limited and Meta retires and renames some. See what
   actually comes back and report only that. `values` may be empty: treat as "no
   data", not an error. Zero is a valid value; a missing field is something else.
3. Permissions: error #10 means no consent to read engagement. Say so and fall back
   to pasted data.

### From pasted screenshots

Insights from Meta Business Suite: reach, views, reactions, comments, shares, clicks,
the share of people who do not follow the Page. For videos: average watch time and
retention. A list of posts with view counts is enough for a first pass.

Also read `~/.claude/facebook/log.md` (which hook pattern was behind which post).
Never pull anything from other people's Pages.

## What to compute (show the working)

Raw views are the worst metric, because they mostly measure follower count.

| Metric | How | What it tells you |
|--------|-----|-------------------|
| **Multiple of median** | views (or reach) / the median of your own posts | a real hit or a normal day |
| **Shares per reach** | shares / reach | the strongest signal you can earn |
| **Comments per reach** | comments / reach | did the hook start a conversation |
| **Reactions per reach** | reactions / reach | the weakest signal, a cheap click |
| **Link clicks** | if available | did the post send people where intended |
| **New followers** | if available | did attention turn into the Page |
| **Average watch time** (video) | from insights | does the middle work |

Rank by multiple and shares per reach, not raw views. A post with 400 views and 12
shares beats one with 5,000 views and two.

## Find the pattern

Compare the top five with the bottom five:

- **Hook / pattern** (from the log).
- **Type and register** (educational, behind-the-scenes, opinion; simple or essay).
- **Format** (text, photo, several photos, link, video).
- **Length.**
- **Topic.**
- **Whether the owner replied to comments in the first hour.**
- **Day and time**: check this **last**, only if the rest shows nothing. It is almost
  never the cause, and it is where people want it to be.

With 30 posts a pattern can show. With 6 it cannot, and it is better to say so than
to invent one. State each finding as a claim with the evidence and a confidence
level. Be ready to reach a conclusion the owner will not like.

## The distinction that saves months

A post with big reach and no new followers is not a failure; it is a Page problem
(`/fb-profile`). A post with small reach is a hook problem. Separate the two before
recommending anything.

## Output

```
AUDIT  |  28 posts  |  Jul-Oct  |  median views: 640

TOP 5 BY MULTIPLE
  9.4x  verbatim question   video   6,010 views   shares/reach 1.8%
  ...
BOTTOM 5
  0.3x  superlative         link      190 views   shares/reach 0%

WHAT THE DATA SAYS
1. ... (claim, evidence, n, confidence)

STOP: ...
DO MORE: ...
```

Save the findings to `~/.claude/facebook/audit.md`. Hand them to `/fb-plan` (next
week on your own evidence) and `/fb-reel`. The skill publishes, reacts to and deletes
nothing.
