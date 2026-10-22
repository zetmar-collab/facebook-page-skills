---
name: fb-repurpose
description: >-
  Turns one long source (a YouTube video, podcast, livestream, newsletter, blog
  post, LinkedIn or Blogger article, client call) into a week of Facebook posts
  and videos. Use when the user says "repurpose this", "turn this into posts", "I
  have a video/article/transcript", "cut this up", "make posts from this
  article", or pastes something long and wants it on Facebook.
---

# fb-repurpose

One good long asset contains four to six posts. Most people extract one and throw
away the rest. This matters most for owners who already write long pieces
(articles, newsletters, transcripts): they can feed the Page without writing from
scratch.

## Input

A transcript, an article, a newsletter, a script, call notes. Read the whole thing
before extracting anything. If it is the owner's own video, ask for the file: a clip
of the real thing beats a re-recording of their own words. If given a URL and the
session has a transcript tool, use it; otherwise ask for a paste.

## Extract, do not summarise

A summary of a video is not a post. Pull out the things that stand alone:

| Pull | What it is |
|------|-----------|
| **Claims** | every sentence that would start an argument |
| **Numbers** | every sum, time, percentage |
| **Stories** | a moment with a person, a scene and a cost |
| **Mechanisms** | "the way this actually works is..." |
| **Mistakes** | every admission that something went wrong |
| **Quotable lines** | a sentence already quotable as-is |

List what you found, with counts, **before** writing anything. If there are fewer
than four items, the source is thin and four posts squeezed out of it will be thin
too. Say so.

## Format per extract

- **Claim, mistake, story** -> a video, or a behind-the-scenes or opinion post (they
  need a voice).
- **Mechanism, list** -> an educational post, several photos, or text with a list.
- **Quotable line** -> a short showcase post or an image.

## Build the week

Each extract becomes one post that stands completely alone. The reader has not seen
the source and will not. Never write "as I said in my last article". Assign a hook
pattern from `fb-reel/hooks.md` to each and vary them: five posts with the same
hook shape look like a content mill, because they are one.

Order: the strongest claim first, the story mid-week, the mechanism last, when
people who liked the earlier ones are watching.

**A second life is not copy-paste.** A long essay cut down to a post must change: a
scene as the opening, fewer metaphors, one CTA. Do not add new facts or anecdotes
that were not in the source.

## Output

```
SOURCE: "Why chatbots make things up" (article, 1,400 words)

FOUND  4 claims, 6 numbers, 2 stories, 3 mechanisms, 1 mistake, 5 quotable lines

WEEK
TUE  VIDEO  verbatim question   "Why does it make things up?" - use the clip at 02:10
WED  POST   educational, SIMPLE  the context-window mechanism
FRI  POST   opinion              "Do not trust an answer without a source"
SUN  POST   story, ESSAY         a scene from the test  [a true story from the owner needed]

Say "write Tuesday" and I will draft that slot.
```

Then draft on request, one at a time, each through `/fb-post` or `/fb-reel` and
`/fb-human`. Do not dump four finished texts at once: they will sound the same and
the owner will use none. Nothing is published.
