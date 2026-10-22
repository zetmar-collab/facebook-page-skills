# facebook-page-skills

A pack of 12 [Claude Code](https://claude.com/claude-code) skills for running a
**Facebook Page**: plan the week, write posts and short-video scripts in your own
voice, check them for AI tells, publish or schedule through
[Composio](https://composio.dev), audit what works and handle comments.

- **Human in the loop by design.** Nothing is published, sent or deleted without an
  explicit "yes" from you over the exact text (see [Safety](#safety)).
- **Your voice, not generic AI copy.** Every skill reads one `voice.md` that you
  control, and every text passes a linter before you see it.
- **Works in English and Polish** out of the box; add another language by writing one
  small lexicon file ([docs/CUSTOMIZING.md](docs/CUSTOMIZING.md)).
- **Two small tools that actually run** (plain Python 3, no dependencies):
  `lint.py` for post drafts and `beats.py` for video scripts.

> **Status: alpha.** The skills and scripts were written and the scripts tested on
> sample text. The Facebook/Composio calls follow the tool names and pitfalls that
> Composio's tool search returned, but the publishing path has **not** yet been
> exercised end to end against a live Page. Expect rough edges and please open issues.

## Skills

| Skill | What it does |
|-------|--------------|
| `fb-start` | Readiness check: state files, Composio connection, which Page; routes you to the right skill |
| `fb-voice` | Builds and maintains your `voice.md` and settles conflicts between registers (simple vs essay) |
| `fb-post` | Writes a post (text / photo / multi-photo / link): two variants, one CTA, 0-3 hashtags, and **always a tailored image prompt** |
| `fb-reel` | Script for a short video: three hooks, spoken script, on-screen text, timed beat sheet (`beats.py`) |
| `fb-human` | Proofreads and removes AI tells; runs `lint.py` with Facebook platform rules |
| `fb-plan` | Weekly plan: types, formats, hook patterns, times, a daily conversation round |
| `fb-publish` | Publishes, schedules, edits and verifies via Composio, behind a confirmation gate |
| `fb-audit` | Post-mortem from Page data: multiples of median, shares per reach, what to stop and do more |
| `fb-reply` | Triage and reply to comments under your own posts; Messenger etiquette |
| `fb-comment` | Comments for other people's posts that add something (nine comment types) |
| `fb-repurpose` | One long source (video, article, podcast) into a week of posts |
| `fb-profile` | Scores a Page out of 100 and rewrites name, About, button, pinned post |

```
              fb-voice  (your voice, single source of truth)
                  |
  fb-plan -> fb-post / fb-reel -> fb-human -> fb-publish -> Facebook Page
     ^                                                          |
     |                   fb-audit  <-- insights from the Page --+
     |                   fb-reply  <-- comments under your posts
  fb-repurpose (long source -> a week of posts)
  fb-comment (other people's posts)       fb-profile (the Page itself)
```

## Requirements

- [Claude Code](https://claude.com/claude-code) (the CLI, desktop app or IDE extension)
- Python 3.8+ (for `lint.py` and `beats.py`; standard library only)
- A **Facebook Page** you manage (see the limitation below)
- A [Composio](https://composio.dev) account connected to Claude Code with the
  `facebook` toolkit authorised. Without it the pack still writes, plans and lints;
  it just hands you text to paste instead of publishing.

**Limitation you should know about:** Composio's Facebook toolkit works with
**Facebook Pages only**, not personal profiles. If you post from a personal profile,
`fb-publish` falls back to "ready-to-paste text".

## Install

```bash
git clone https://github.com/zetmar-collab/facebook-page-skills.git
cd facebook-page-skills
./install.sh            # macOS / Linux / Git Bash
```

On Windows PowerShell:

```powershell
git clone https://github.com/zetmar-collab/facebook-page-skills.git
cd facebook-page-skills
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

The installer copies `skills/fb-*` to `~/.claude/skills/` and creates
`config.md`, `voice.md` and `log.md` in `~/.claude/facebook/` **only if they do not
exist**. Your own files are never overwritten. Restart Claude Code afterwards.

Manual install: copy the folders in `skills/` to `~/.claude/skills/` and the files
in `templates/` to `~/.claude/facebook/` (dropping the `.template` part of the name).

## Quick start

1. `/fb-start` - connects Composio's Facebook toolkit, lists your Pages, saves the
   Page id (never a token) to `config.md`.
2. `/fb-voice` - answer four questions; it writes your `voice.md`.
3. `/fb-plan` - plan the week.
4. `/fb-post a topic you want to post about` - get two variants plus an image prompt.
5. `publish A` - `fb-publish` shows exactly what will go out and waits for your "yes".

Full walk-through with the Composio details: [docs/SETUP.md](docs/SETUP.md).

## The tools

```bash
# Lint a post draft (en | pl). Exit code 1 if there is a FAIL.
python3 ~/.claude/skills/fb-human/lint.py post.txt --lang en --type opinion
python3 ~/.claude/skills/fb-human/lint.py post.txt --fix -o post_clean.txt

# Timed beat sheet for a short-video script (one line = one beat)
python3 ~/.claude/skills/fb-reel/beats.py script.txt --target 35 --wpm 150
```

Try them on the files in [`examples/`](examples).

`lint.py` is a set of local heuristics: Facebook rules (no markdown asterisks, one
link, few hashtags/emoji, no greeting opener), a lexicon of AI-isms, structural
tells ("not just X but Y", triads) and rhythm checks. **It is not an AI detector**
and promises no score in any detection tool.

## Safety

- **Confirmation gate.** `fb-publish` shows the Page, full text, link, image and
  time, and publishes only after you say yes to *that* set. Approving one post does
  not approve the next. Approving a weekly plan does not approve any post in it.
- **No blind retries.** Creating a post is not idempotent; after an error the skill
  checks the Page before retrying, to avoid duplicates.
- **Tokens are secrets.** Page access tokens returned by Composio are never printed,
  stored or logged. Only the Page id is saved.
- **No automated engagement.** Comments on other people's posts and Messenger
  messages are drafted for you to paste; the skills never post or send them
  automatically, because automated engagement violates Facebook's terms.
- **No invented facts.** The skills never make up numbers, clients, results or
  anecdotes; they leave `{{your number}}` and flag it.
- You are responsible for what you publish. Read the output.

## Customising

Language, lexicon, registers, limits and image-prompt style:
[docs/CUSTOMIZING.md](docs/CUSTOMIZING.md).

## Repository layout

```
skills/fb-*/            the 12 skills (SKILL.md each; fb-human has lint.py + lexicons,
                        fb-reel has beats.py + hooks.md)
templates/              starter config.md, voice.md, log.md
examples/               sample posts and a script for trying the tools
docs/                   SETUP.md, CUSTOMIZING.md
install.sh / install.ps1
```

## Credits

Built for Claude Code. The structure of the engagement, audit and planning skills is
inspired by common social-media workflows; hook patterns in `fb-reel/hooks.md` are
common short-form patterns written up in our own words. The AI-tell lexicon is
informed by the community guide
[Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
(a guideline page, not official policy).

## License

[MIT](LICENSE)
