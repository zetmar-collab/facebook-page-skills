---
name: fb-reel
description: >-
  Writes a script for a short Facebook video (reel) from a raw idea: three hook
  options, the spoken script, on-screen text and a timed beat sheet, in the page
  owner's voice. Use when the user says "reel", "short video", "video script",
  "what do I say in this video", "hook for a reel", "write a script", or is about
  to record and has no first line yet.
---

# fb-reel

Turns one idea into a short video somebody finishes. It writes the script. The
user records and posts (or `/fb-publish` after the gate).

A tool that runs:

```bash
python3 ~/.claude/skills/fb-reel/beats.py script.txt --target 35 --wpm 150
```

## Before writing

1. Read `~/.claude/facebook/voice.md`. A video is spoken, so a wrong voice means a
   script the user will not say. Missing -> `/fb-voice`. If an Instagram voice file
   exists and the Facebook one does not, use it as a starting point and say so.
2. Read `hooks.md` in this folder (22 hook patterns).
3. Idea thin? One batched question: what happened, to whom, what it cost or
   returned. A video needs one specific true thing.
4. Read `~/.claude/facebook/plan.md` for the slot (pattern, length).

## Shape

```
0:00-0:03   HOOK     the claim. Spoken line and on-screen line written separately. Motion in frame one.
0:03-0:08   STAKE    why it matters to the viewer. One sentence.
0:08-...    BODY     one idea per beat; the picture changes every beat.
LAST 3s     PAYOFF   what the hook promised, plus one ask.
LAST LINE   LOOP     one word from the hook, so a replay lands cleanly.
```

Working length: 15-45 s. For an explainer series (one concept, one everyday
example) about 30-40 s at 150 words per minute. Do not go longer without a reason.

## The loop

1. **Three hooks, not one.** Choose three different patterns from `hooks.md` that
   fit. For each: the spoken line and the on-screen line (six words or fewer).
2. **Pick a winner** and say why (a concrete number, readable at a glance, something
   only the user can say). There is no hook-scoring script here: text-based scorers can
   catch a plainly bad hook (a greeting, no concrete detail) but cannot reliably rank
   two decent ones, because what decides it is the face, the edit and the audio.
   Judge by eye and by the retention graph after posting.
3. **Write the script** on the winning hook. Spoken language, short lines, sentences
   that can be said without rehearsal. One line of the file = one beat.
4. **Time it:** `beats.py script.txt --target {seconds} --wpm 150` (use the user's
   measured pace). Fix every flag: hook longer than 3 s, beat over 4 s, three beats
   in a row with nothing concrete, no loop. Re-run until clean.
5. **`/fb-human` on the script.** A written-sounding line is obvious when said aloud.
6. **Print the block** (script, on-screen cards with timings, receipt).

## On-screen text is a separate script

- Six words or fewer per card. It is read before it is heard.
- The hook card is up at frame 1.
- Captions for all speech, always. Many people watch muted.
- Vertical 9:16, 1080x1920. Keep key text toward the middle, away from edges and the
  bottom where the interface overlays (check the preview on a phone; the layout
  changes).
- The hook does not sit at the bottom of the frame.

## Rules

- **One idea per video.** Two ideas are two videos. Say so.
- **Numbers over adjectives.** No number: ask, or `{{your number}}`.
- **No intro.** No greeting, "in this video", name or jingle.
- **Change the picture every beat.** A still face for 8 s is where people leave.
- **One ask at the end.** Comment, save, or follow. One.
- **Never invent** results, clients or sums, not even as placeholders.
- Write the caption/description through `/fb-post` (a short post).

## Output

```
REEL READY
hook:       "Why does it forget what I said?" (verbatim question)
            on screen: IT FORGETS
length:     34.8 s, 22 beats, 150 wpm
on screen:  7 cards
lint:       READY
to fill in: none

Reply "yes" to log it, or tell me what to change.
```

On "yes" append to `~/.claude/facebook/log.md`: date, pattern, first line, status
"script ready". Publishing the video is a separate step (`/fb-publish`, tool
`FACEBOOK_CREATE_VIDEO_POST`): the file must be at a public URL or uploaded
locally, and whether it shows up as a Reel or a regular video depends on the
format Facebook accepts. Do not promise a Reel.
