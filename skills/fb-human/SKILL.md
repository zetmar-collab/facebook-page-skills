---
name: fb-human
description: >-
  Quality control for Facebook text: finds language errors, doubtful facts and
  AI tells (AI-vocabulary lexicon, triads, "not just X but Y", markdown
  asterisks, invisible characters), and runs lint.py with Facebook platform
  rules. Use ALWAYS before showing the page owner a finished post, comment, reply
  or script, and whenever they say "check this text", "proofread", "does this
  sound like AI", "remove the AI-isms", "edit this".
---

# fb-human

Two modes, plus a tool that actually runs.

```bash
python3 ~/.claude/skills/fb-human/lint.py post.txt --lang en --type opinion
python3 ~/.claude/skills/fb-human/lint.py post.txt --fix -o post_clean.txt
```

`lint.py` reads `lexicon.<lang>.json` (English and Polish are bundled) and
checks: markdown, invisible characters, emoji, links, hashtags, a greeting as
the opening, number of asks (CTA), chat residue, negative parallelism, triads,
dashes, sentence-length variation and a missing number. It returns READY,
REVIEW or FAIL (exit code 1).

These are local heuristics. They are not GPTZero or any other detector, and you
must never promise a text is "undetectable". The goal is natural, specific
writing.

Pass `--lang` to match the post language. Add a language by copying
`lexicon.en.json` to `lexicon.<code>.json` and translating (see
`docs/CUSTOMIZING.md`).

## Mode A: the user pastes their own text

1. **Language errors.** Quote the exact fragment, give the fix and a short
   reason. Spelling, punctuation, grammar, style.
2. **Facts.** Flag a claim that looks wrong or cannot be checked. If you can
   verify it (search), give the source. If you cannot, say so instead of guessing.
3. **Style.** AI tells from the linter, separately from errors, as suggestions.
4. Do not "fix" what is correct. A concrete list of notes beats a full rewrite.

## Mode B: you wrote the text for the user

A mandatory check, no request needed:

1. Save the draft to a file in the scratchpad and run `lint.py` with the right
   `--lang` and `--type` (educational, behind-the-scenes, showcase, opinion, offer).
2. `--fix` removes only safe things: invisible characters, asterisks, runs of
   blank lines. Nothing else is rewritten automatically.
3. Fix every FAIL. Decide every WARN out loud or fix it. Never ignore one silently.
4. Structural tells (parallelism, triads, one-word questions) are flagged, then
   rewritten by hand, keeping the meaning.
5. Re-run. Two rounds is normal. Five means the draft came from a template; write
   a different draft instead of polishing this one.
6. Show the user the **text**, not just the lint output.

## What the lexicon catches

- Hard (FAIL): stock marketing words, "in today's fast-paced world" openers,
  "have you ever wondered", "in conclusion", chat residue like "I hope this
  helps".
- Soft (WARN when several appear): crucial, pivotal, landscape, ecosystem,
  comprehensive, "plays a key role", "whether you're...".

## What lint cannot catch

- Factual errors (your job in Mode A).
- A register that does not match `~/.claude/facebook/voice.md`.
- An invented story. Check that every number and anecdote came from the user.

## Caveat

No single signal proves a text is artificial. Do not torture a text for
naturalness' sake: sometimes "crucial" or a dash is simply the right word.
