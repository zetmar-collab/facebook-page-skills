# Customising

## Write posts in another language

Set `language:` in `~/.claude/facebook/config.md` (e.g. `language: de`). The skills
write in that language. The linter needs a lexicon for it:

1. Copy `skills/fb-human/lexicon.en.json` to `lexicon.de.json` (same folder).
2. Translate the entries. Keep the keys:

| Key | Meaning |
|-----|---------|
| `greeting` | regex: greetings that must not open a post |
| `asks` | regex list: phrases that count as a call to action (two or more different ones warn) |
| `chat_remnants` | regex list: "I hope this helps"-style leftovers (FAIL) |
| `structure` | `{name, re}` list: structural tells such as "not just X but Y" (WARN) |
| `triad` | regex: a three-item list pattern (WARN when it repeats) |
| `hard` | `{re, why}` list: banned words and phrases (FAIL) |
| `soft` | `{re}` list: suspicious words (WARN when several appear) |

3. Run `python3 lint.py post.txt --lang de`, or set `FB_LANG=de` in your environment.

Regexes are matched against **lower-cased** text. In languages that inflect (Polish,
German, Russian...), match stems with `\w*` (see `lexicon.pl.json`). In JSON, a
backslash must be doubled: `"\\b"`, not `"\b"` (the second means a backspace
character and silently never matches).

`--lexicon path/to/custom.json` points at any file without renaming anything.

`beats.py` works for any language that separates words with spaces; extend
`SPOKEN_NUM` and `STOPWORDS` at the top of the file for yours.

## Make the linter yours

- A word the lexicon flags but you genuinely use: delete its entry.
- Limits: `--max-emoji`, `--max-hashtags`; defaults are 3 and 5.
- Post lengths per type are in `LENGTHS` at the top of `lint.py`.

## Registers

`fb-voice` defines two: **SIMPLE** (short sentences, numbers, conclusion at the end)
and **ESSAY** (scene-first, fresh metaphors, alternating sentence length, a closing
question). Edit their descriptions in your `voice.md`; `fb-post` and `fb-reel` follow
what is written there. If you want a third (for example "newsletter"), add it to
`voice.md` with a one-paragraph description, and tell `fb-post` which post types use
it.

## Image prompts

`fb-post` builds a tailored prompt for every post. To change the look:

- Edit the **TECHNICAL**, **STYLE** and **NEGATIVE** lines in `skills/fb-post/SKILL.md`
  (the camera line is only a default look; set whatever matches your brand).
- If you do not generate images with AI, delete the **LABEL** line. Keep it if you
  publish generated images: a visible "AI GENERATED" label is good practice and may be
  required by platform policy or local regulation.

## Hook patterns

`skills/fb-reel/hooks.md` is a plain table. Add your own patterns, delete the ones
that never work for you, and let `/fb-audit` show which ones lift your numbers.

## Safety settings

`publish_mode: gate` should stay. The gate is what keeps a misread instruction
from becoming a public post. If you really want fewer prompts, edit `fb-publish`
deliberately, and keep the "show exactly what goes out" step.

## Companion packs

Some skills read optional files from other packs if they exist (for example
`~/.claude/instagram/voice.md` and `log.md` as a starting point for your Facebook
voice and to avoid repeating a topic the same week). Nothing breaks if they are
absent.
