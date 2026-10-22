---
name: fb-voice
description: >-
  Sets up and maintains the page owner's writing voice in
  ~/.claude/facebook/voice.md, which every other fb-* skill reads. Builds a draft
  from existing material (an Instagram voice file, past posts, the user's own
  words) and settles conflicts between registers. Use when the user says "my
  voice", "my style", "how should I write on facebook", "write like me", "adjust
  the tone", "match my posts", or when fb-post cannot find voice.md.
---

# fb-voice

A wrong voice means text the page owner will not publish. This skill exists so
that voice is decided once, written down, and never guessed silently.

## Step 1: read what exists

1. `~/.claude/facebook/voice.md` -> if present, show only the fields still marked
   `{{...}}` or `[TO CONFIRM]` and ask about those.
2. If absent, build a draft from whatever the user has: an Instagram voice file
   (`~/.claude/instagram/voice.md`, if they use a companion pack), a bio, pasted
   posts, or older skills they point to. Mark every claim with its source.
3. If Composio is connected and the Page has posts, fetch a few with
   `FACEBOOK_GET_PAGE_POSTS` (see `fb-audit`) and infer the voice from the
   user's own words. This is the best source.

## Step 2: one question to settle the conflicts

Ask one batched multiple-choice question, because everything else depends on it:

1. **Who is the page owner on Facebook?** e.g. an explainer for ordinary
   people, a specialist speaking to professionals, or both depending on the post.
2. **Which register is the default?**
   **SIMPLE**: short sentences, numbers, direct address, conclusion at the end.
   **ESSAY**: scene-first, 2-3 fresh metaphors, long and short sentences
   alternating, a reflective line after the facts, a question at the end.
   **MIXED**: simple hook and numbers, one metaphor in the middle.
3. **Who is the reader?** Ordinary people, business owners, a profession.
4. **Should the ESSAY register be used at all** on this Page, and if so only for
   behind-the-scenes and long stories?

Without answers, default to SIMPLE for everything and mark the file
`[TO CONFIRM]`.

## Step 3: file format for `~/.claude/facebook/voice.md`

```
# voice.md - {{name}}, Facebook
Version: {{date}}. Sources: {{list}}.

## Who I am and who I write for
- Positioning: ...
- Reader: ...
- Goal of the Page: personal brand / trust / (offer: {{when there is one}})

## Registers (fb-post picks one per post)
- SIMPLE (default): short sentences, one idea per paragraph, numbers,
  direct address, conclusion at the end.
- ESSAY: scene-first opening, 2-3 fresh metaphors, long/short sentences
  alternating, one reflective line after concrete facts, closing question.

## Words I use
## Words I never say
(start from fb-human/lexicon.<lang>.json, then add the owner's own)

## Formatting
- Plain text. No asterisks, markdown headers or backticks.
- Emoji 0-3 per post, never first.
- Hashtags 0-3. One link per post.

## My positions
## Proof I may use       (real numbers only; skills never invent them)
## Off limits
## CTA
```

## Rules that hold in every register

- **Never invent** numbers, clients, results or memories. If a post needs a
  personal experience the user has not provided, ask one question or leave
  `{{your story}}`. The ESSAY register is especially tempting ("last night at
  the workshop..."). Not allowed until the user has said it happened.
- **One language per post**, the one set in `config.md` (`language`).
- Before handing anything over, run it through `/fb-human`.

## Output

Show the file once in full, list what is still `[TO CONFIRM]`, save it to
`~/.claude/facebook/voice.md`. Nothing is published.
