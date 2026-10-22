---
name: fb-plan
description: >-
  Plans the week on a Facebook Page: what to publish, in which format, when, and
  who to talk to, based on the post log and (if available) data from the Page. Use
  when the user says "plan my week", "what should I post", "content calendar", "I
  have nothing to post about", "schedule my posts", "weekly plan".
---

# fb-plan

The control room of the pack. The other skills execute; this one decides what.
Run it once a week, on the same day.

## Input

Read, if present: `~/.claude/facebook/voice.md`, `log.md` (so a theme from the last
two weeks is not repeated), `audit.md` (findings from `/fb-audit` outrank the
general rules below), and an Instagram log such as `~/.claude/instagram/log.md` if
the user runs a companion pack (the same ideas may return, but not in the same week
on both platforms without a change).

If files are missing, ask four things and write them down:

1. What does the user sell (today maybe nothing; building a brand) and to whom.
2. Three or four themes they want to be known for.
3. What actually happened this week: a call, a number, a mistake, something built,
   an argument. This is where posts come from.
4. Ten Pages and groups where it is worth being visible (see `fb-comment`).

## How much, and what

A sensible start is **3-4 posts a week** plus 15 minutes a day of conversation
(comments under your own posts plus a few on others'). Tune frequency to what the
user can sustain; three good ones beat seven weak ones. Short videos are the main
format for reaching people who do not follow the Page, but that is a working
assumption from practice, not a hard rule: `/fb-audit` will show whether reach to
non-followers on this Page confirms it.

| Type | Share | Job |
|------|-------|-----|
| Proof | 1 per week | something that happened, with a number (reel or post) |
| Teach | 1-2 per week | one thing to do today (educational post, reel) |
| Opinion | 1 per week | a position that might cost a follower (opinion post) |
| Behind-the-scenes / story | every 2 weeks | a scene with a cost |
| Offer | every 2 weeks | what you sell, plainly (skip if nothing is for sale) |

Never two posts of the same type back to back. For each slot give: the topic, a
**concrete angle** from what really happened (not "AI", but "the conversation where
the chatbot forgot the first half"), the format, the register and the hook pattern
from `fb-reel/hooks.md`.

## When

Pick a time when the audience is off work (an evening for ordinary people) or early
morning (for businesses). Say it plainly: **the hour matters much less than the
hook**. Until hooks work, optimising times is polishing the wrong thing. After 4-6
weeks `/fb-audit` will show whether time matters at all (it usually does not).

Plan in the audience's timezone (`config.md`), and watch for daylight-saving changes
inside the planned week.

## Conversations (not optional)

15 minutes a day, before publishing. A list of ten places: five with large reach
(groups and Pages with your audience), three peers, two with potential customers.
Comment so that the comment adds something (`/fb-comment`). Never drop adverts into
a group; many groups forbid it and Facebook has its own group rules to read.

## Output

```
WEEK OF OCT 26

MON  conversations (15 min), list below
TUE  7:00 pm  REEL   TEACH    verbatim question   - why the chatbot forgets
WED  conversations
THU  7:00 pm  POST   OPINION  nobody tells you    - stop keeping one chat open
FRI  -
SAT  -
SUN  6:00 pm  POST   STORY    ESSAY register      - a scene from the workshop  [needs a true story]

CONVERSATIONS (5 reach / 3 peers / 2 buyers)
  ...

Say "write Tuesday" and I will draft that slot.
```

Save the plan to `~/.claude/facebook/plan.md` so `fb-post` and `fb-reel` read it.
Nothing is scheduled on Facebook; this is a plan the user executes. Scheduling a
specific post on Facebook is a separate step and a separate approval
(`/fb-publish`).
