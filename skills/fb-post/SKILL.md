---
name: fb-post
description: >-
  Writes a Facebook Page post: hook, body, one call to action, 0-3 hashtags, two
  variants, and ALWAYS a tailored image prompt (even when the user does not ask
  for one), plus an optional .docx. Handles text, single photo, multi-photo and
  link posts. Use when the user says "write a facebook post", "post for my page",
  "facebook copy", "draft a post about X", or gives a topic and asks for a social
  post without naming a platform (then suggest Facebook).
---

# fb-post

Turns one topic into a post the page owner can publish without edits. It writes
the text. It publishes nothing: that is `/fb-publish`, after an explicit "yes".

## Before writing

1. Read `~/.claude/facebook/voice.md`. Missing -> `/fb-voice`. Pick the register
   (SIMPLE or ESSAY) and say which.
2. Read `~/.claude/facebook/plan.md` if present (a slot gives topic, type and
   hook) and `log.md`, so you do not repeat a theme from the last two weeks.
3. Read `config.md` for `language`, `link_policy`, `hashtags_max`.
4. Topic thin? Ask one batched question: what happened, to whom, what it cost
   or returned. A post needs one true, concrete thing. If the user gave only a
   topic, decide yourself and do not ask about every detail.
5. Settle: post type, goal (traffic, comments, enquiries), and whether there is
   already an image.

## Post types

| Type | When | Words |
|------|------|-------|
| educational | how something works, a practical tip | 150-250 |
| behind-the-scenes | story, process, a scene from the work | 100-180 |
| showcase | presenting a result; the image carries the post | 80-120 |
| opinion | a position, a question for discussion | 60-120 |
| offer | the service, said plainly, no apology | 120-200 |

`fb-human/lint.py --type` knows these ranges.

## Shape

```
HOOK        1-2 sentences. Visible before "See more". A concrete thing, not a greeting.
BODY        3-5 paragraphs of 1-3 sentences, a blank line between them.
            A list only when it organises: use a plain marker, not emoji.
CTA         one action. Best: a question answerable in one sentence.
HASHTAGS    0-3, on the last line.
```

**Hook.** Facebook truncates text on phones, so the first sentence must work
alone. Truncation depends on the device, so do not assume a character count: lint
warns above 140 and asks you to check the preview. Good hooks: a concrete number,
the reader's problem, an opinion with a cost, a scene opened mid-action. Patterns
are in `~/.claude/skills/fb-reel/hooks.md` (they work for text too).

**SIMPLE register** (default): short sentences, one idea per paragraph, a number,
the conclusion at the end. **ESSAY register**: a personal point of entry, 2-3 fresh
metaphors, alternating sentence lengths, one reflective line after the concrete
facts, a closing question, emoji only at the end. Details in `fb-voice`.

## Link

Unlike Instagram, Facebook shows clickable links in a post. Two options: link in
the body (default) or in the first comment. Follow `config.md` (`link_policy`)
and ask if unset. There is no evidence here that the comment trick raises reach.
One link per post, always.

## Hashtags

0-3. On Facebook they are topic labels, not a reach lever, and a long block looks
like spam. Change the limit in `config.md` (`hashtags_max`) if the user wants more.

## Photos

- **One photo:** text + image, published with `FACEBOOK_CREATE_PHOTO_POST`. The
  image needs a public URL (`fb-publish` explains).
- **Several photos:** `FACEBOOK_UPLOAD_PHOTOS_BATCH`. Each frame must make sense
  alone; the first decides the click.
- An image prompt is generated **always** (below), even if the user has their own
  photo; then the prompt is an alternative and the receipt says so.
- The "AI GENERATED" label stays in the prompt for generated images. A real
  photograph is never described with it.

### Image prompt (mandatory)

Every use of this skill ends with an image prompt. Do not ask whether it is
wanted and do not skip it when the request is only "write a post". It is built
from **this** post, not from a template. A prompt that would fit any post on the
topic (a glowing brain, a robot, a hologram) is a bug.

**Step 1: pull one image out of the post.** Ask yourself:
1. What is the core of the post as one thing you can *see*? (a person, an object,
   an action, a contrast)
2. What mood should the image carry? (calm, surprise, relief, tension)
3. Should the image illustrate the hook or the result? Default: the hook, because
   it has to stop the scroll.

**Step 2: choose the scene by post type.**

| Post type | Scene |
|-----------|-------|
| educational | a person doing a concrete thing tied to the topic; a calm interior, no "magic" |
| opinion | one strong contrast or symbol of the thesis; few elements |
| behind-the-scenes | an authentic work scene, equipment details, caught-in-the-moment feel |
| showcase | the result is the hero; clean background |
| offer | a clear benefit: a satisfied person, a clean background, room for the eye |

Default look: ordinary people in ordinary settings (desk, kitchen, workshop);
never robots, glowing brains, holograms, blue neon or "matrix" code.

**Step 3: choose the format by how it is published.**

| Publication | Format |
|-------------|--------|
| single photo (default) | `--ar 4:5` portrait, takes more room in a phone feed |
| link post (thumbnail) | `--ar 1.91:1` landscape |
| reel / video cover | `--ar 9:16` |
| several photos | one prompt per frame, same style, `--ar 4:5` |

State the default format in the receipt.

**Step 4: assemble the prompt in English** in its own block, ready for
Midjourney, DALL-E or Flux, using these fields as a checklist:

```
SUBJECT:      who or what, concretely, from this post
ACTION/SCENE: what they are doing, where; one scene
LIGHT:        e.g. soft morning window light / warm lamp light
COMPOSITION:  e.g. over-the-shoulder, rule of thirds, shallow depth of field
MOOD:         one or two words
TECHNICAL:    camera/lens/ISO (set in config.md or use the default below)
STYLE:        photorealistic, professional photography, sharp focus, cinematic
NEGATIVE:     no robots, no glowing brains, no holograms, no stock-photo feel,
              no plastic skin, no text on image except the label
LABEL:        a clearly visible but elegant AI transparency label in the
              bottom-right corner reading: "AI GENERATED"
FORMAT:       --ar 4:5
```

Default TECHNICAL: `Canon EOS R6 Mark II, 35mm f/1.8, ISO 400, f/2.8, 1/250s`.
Output the prompt as one continuous paragraph ready to paste; the structure above
is a checklist, not what gets pasted. Never put the post's text or hook on the
image (generators fumble lettering and the words are in the post already). The
only exception is the "AI GENERATED" label.

**Step 5: add one sentence** (in the post's language) saying what the image shows
and why it fits **this** post, referring to the hook or thesis.

**One prompt or two.** Default: one shared prompt for both variants. If the
variants suggest different scenes, give one prompt per variant, labelled.

**Self-check:** does the prompt contain anything not in the post or its topic?
Does it fit the register (SIMPLE = a calm, ordinary scene)? Would someone seeing
the image without the text guess the topic? If not, fix it.

## Procedure

1. Write **two variants** that differ in hook and tone: A provocative or
   question-led, B educational or value-led (for ESSAY: A concrete, B deeper).
2. Save each to a file and run
   `python3 ~/.claude/skills/fb-human/lint.py variant_a.txt --lang {language} --type {type}`.
   Fix FAILs, decide WARNs. Repeat.
3. Check claims: every number, name and anecdote must come from the user.
   Leave `{{your number}}` for anything missing and list it in the receipt.
4. **Build the image prompt** (section above). Mandatory: a reply without one is
   incomplete and must not be returned.
5. Print both variants as plain text (no asterisks), the image prompt with its
   one-sentence explanation, and the receipt.
6. On request, generate a `.docx` (heading `Facebook Post - [TOPIC] - [DATE]`,
   variants as H2, hashtags in grey italics, filename `fb_[slug]_[YYYYMMDD].docx`)
   with Node and the `docx` package. Do not generate one by default; the text is
   visible in the chat.

## Receipt

```
POST READY
type:       educational, register SIMPLE
words:      187 (target 150-250)
hook:       "Stop keeping one chat open for seven days." (43 chars)
CTA:        one, a question
link:       none
hashtags:   2
image:      one shared prompt; scene: reading an AI answer and checking it in a notebook; format 4:5
lint:       READY
to fill in: {{your number}} in paragraph 2
Next step:  "publish A" -> /fb-publish   or   "schedule B for Thursday 19:00"
```

## Rules

1. Plain text. No asterisks, markdown headers or backticks.
2. Never open with a greeting. Never open with an emoji.
3. One CTA. Do not ask for three things at once.
4. Emoji 0-3 per post.
5. Banned words and phrases: `fb-human/lexicon.<lang>.json`.
6. Never invent numbers, clients or results. Use `{{...}}` and flag it.
7. Write in the language set in `config.md`.
8. **The image prompt is mandatory in every reply.** Tailored to topic and type,
   scene based on the hook, format based on how it is published. No prompt, no
   post. If no visible image can be drawn from the post, ask the user for one
   thing they would like to show instead of inserting a generic.
