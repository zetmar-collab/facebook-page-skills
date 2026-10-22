#!/usr/bin/env python3
"""
lint.py - check a Facebook post draft before it goes to the page owner.

Four things at once:
  1. platform rules      (markdown asterisks, links, hashtags, emoji, greetings)
  2. an AI-tell lexicon  (lexicon.<lang>.json: banned and suspicious words)
  3. structural tells    ("not just X but Y", triads, rhetorical one-word questions)
  4. rhythm and specificity (sentence-length variation, numbers)

These are local heuristics. This is NOT an AI detector and it promises no score
in GPTZero or similar tools. It catches what readers notice without being able
to name it.

Usage
  python3 lint.py post.txt
  python3 lint.py post.txt --lang en --type educational
  python3 lint.py post.txt --fix -o post_clean.txt      # safe fixes only
  cat post.txt | python3 lint.py - --lang pl
  python3 lint.py post.txt --json

Exit code: 0 = READY or REVIEW, 1 = at least one FAIL.
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

URL_RE = re.compile(r"https?://\S+|\b[\w-]+(?:\.[\w-]+)*\.(?:com|net|org|io|eu|pl|de|uk|co|app|dev)\b/?\S*", re.I)
HASHTAG_RE = re.compile(r"(?<!\w)#\w+")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐⬆✅❌]")
INVISIBLE_RE = re.compile("[​‌‍⁠⁣﻿­    ]|[\U000E0000-\U000E007F]")
MD_BOLD_RE = re.compile(r"\*\*(.+?)\*\*|\*(.+?)\*|__(.+?)__")
MD_HEADER_RE = re.compile(r"^\s{0,3}#{1,6}\s+\S", re.M)
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[\w'-]+")

# post type -> (min words, max words)
LENGTHS = {
    "educational": (150, 250),
    "behind-the-scenes": (100, 180),
    "showcase": (80, 120),
    "opinion": (60, 120),
    "offer": (120, 200),
}
TYPE_ALIASES = {
    "edukacyjny": "educational", "kulisy": "behind-the-scenes", "opinia": "opinion",
    "oferta": "offer", "bts": "behind-the-scenes", "behind": "behind-the-scenes",
}


def load_lexicon(lang, path=None):
    path = path or os.path.join(HERE, f"lexicon.{lang}.json")
    if not os.path.exists(path):
        sys.exit(f"lexicon not found: {path}. Available: "
                 + ", ".join(f for f in os.listdir(HERE) if f.startswith("lexicon.")))
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def words(text):
    return WORD_RE.findall(text)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(words(s)) >= 2]


def body_without_tags(text):
    keep = []
    for line in text.splitlines():
        stripped = HASHTAG_RE.sub("", line).strip()
        if line.strip() and not stripped:
            continue
        keep.append(line)
    return "\n".join(keep)


def lint(text, lex, post_type=None, max_emoji=3, max_hashtags=5, hook_chars=140):
    findings = []

    def add(level, check, msg):
        findings.append({"level": level, "check": check, "msg": msg})

    body = body_without_tags(text)
    nwords = len(words(body))

    # --- platform rules -----------------------------------------------------
    if MD_BOLD_RE.search(text) or "`" in text:
        add("FAIL", "markdown", "Asterisks, underscores or backticks. Facebook does not render markdown; they will show up as junk.")
    if MD_HEADER_RE.search(text.replace("\r", "")):
        add("FAIL", "markdown", "Markdown header (# at line start). Replace with a plain sentence.")
    inv = INVISIBLE_RE.findall(text)
    if inv:
        add("FAIL", "characters", f"{len(inv)} invisible characters (zero-width, non-breaking space). Run with --fix.")
    first_char = text.strip()[:1]
    if first_char and EMOJI_RE.match(first_char):
        add("FAIL", "emoji", "Post starts with an emoji. Start with words.")
    n_emoji = len(EMOJI_RE.findall(text))
    if n_emoji > max_emoji:
        add("FAIL", "emoji", f"{n_emoji} emoji, limit {max_emoji}.")
    urls = URL_RE.findall(text)
    if len(urls) > 1:
        add("FAIL", "links", f"{len(urls)} links. Rule: one link per post.")
    tags = HASHTAG_RE.findall(text)
    if len(tags) > max_hashtags:
        add("WARN", "hashtags", f"{len(tags)} hashtags. On Facebook they are labels, not reach. Keep to {max_hashtags}, ideally 0-3.")
    if re.match(lex.get("greeting", r"^$"), text.strip(), re.I):
        add("FAIL", "opening", "A greeting as the opening wastes the most valuable sentence of the post.")

    # --- hook ---------------------------------------------------------------
    first_line = next((l.strip() for l in text.splitlines() if l.strip()), "")
    if len(first_line) > hook_chars:
        add("WARN", "hook", f"First line is {len(first_line)} characters. Facebook truncates early on phones; check the preview so the hook shows before 'See more'.")

    # --- length -------------------------------------------------------------
    if post_type:
        key = TYPE_ALIASES.get(post_type.lower(), post_type.lower())
        if key in LENGTHS:
            lo, hi = LENGTHS[key]
            if nwords < lo or nwords > hi:
                add("WARN", "length", f"{nwords} words; type '{key}' aims for {lo}-{hi}.")
        else:
            add("WARN", "length", f"Unknown type '{post_type}'. Use: {', '.join(LENGTHS)}.")

    # --- asks (CTA) ---------------------------------------------------------
    asks = sorted({p for p in lex.get("asks", []) if re.search(p, body, re.I)})
    if len(asks) >= 2:
        add("WARN", "cta", f"At least {len(asks)} different asks. Keep one.")

    # --- lexicon ------------------------------------------------------------
    low = body.lower()
    for entry in lex.get("hard", []):
        for m in re.finditer(entry["re"], low):
            add("FAIL", "lexicon", f"{entry.get('why', 'banned phrase')} -> '{m.group(0)}'")
    soft_hits = []
    for entry in lex.get("soft", []):
        soft_hits += [f"'{m.group(0)}'" for m in re.finditer(entry["re"], low)]
    if soft_hits:
        density = len(soft_hits) / max(nwords, 1) * 100
        add("WARN", "lexicon", f"Suspicious words ({len(soft_hits)}, {density:.1f}/100 words): {', '.join(sorted(set(soft_hits)))}. One is chance, several is a pattern.")
    for p in lex.get("chat_remnants", []):
        m = re.search(p, body, re.I | re.M)
        if m:
            add("FAIL", "chat-residue", f"Addressed to a chat user instead of the reader: '{m.group(0).strip()}'.")

    # --- structure ----------------------------------------------------------
    for s in lex.get("structure", []):
        n = len(re.findall(s["re"], body, re.I))
        if n:
            add("WARN", "structure", f"{s['name']} ({n}x). Rewrite by hand, keep the meaning.")
    triad = lex.get("triad")
    if triad:
        n_triads = len(re.findall(triad, body, re.I))
        if n_triads >= 2:
            add("WARN", "structure", f"{n_triads} three-item lists. Sometimes two or four is natural.")
    dashes = body.count("—") + body.count("–")
    if dashes > 2:
        add("WARN", "dashes", f"{dashes} dashes. Use them where they do syntactic work, not for drama.")
    if re.search(r"\b[A-Z]{4,}\b(?:\s+\b[A-Z]{4,}\b){2,}", body):
        add("WARN", "structure", "Three or more ALL-CAPS words in a row.")

    # --- rhythm and specificity --------------------------------------------
    lens = [len(words(s)) for s in sentences(body)]
    burst = None
    if len(lens) >= 5:
        mean = statistics.mean(lens)
        burst = statistics.pstdev(lens) / mean if mean else 0
        if burst < 0.30:
            add("WARN", "rhythm", f"Sentences are similar in length (variation {burst:.2f}). Mix short and long.")
    if nwords >= 60 and not re.search(r"\d", body):
        add("WARN", "specificity", "No number anywhere. Add a real number, price, time or name (never an invented one).")

    fails = [f for f in findings if f["level"] == "FAIL"]
    warns = [f for f in findings if f["level"] == "WARN"]
    return {
        "verdict": "FAIL" if fails else ("REVIEW" if warns else "READY"),
        "words": nwords, "chars": len(text.strip()), "sentences": len(lens),
        "burstiness": None if burst is None else round(burst, 2),
        "emoji": n_emoji, "hashtags": len(tags), "links": len(urls),
        "hook_preview": first_line[:hook_chars], "findings": findings,
    }


def fix(text):
    """Only fixes that cannot change meaning."""
    text = INVISIBLE_RE.sub(lambda m: " " if m.group(0) in (" ", " ") else "", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = text.replace("`", "")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def render(r):
    print(f"\nFB LINT  |  {r['words']} words  |  {r['chars']} chars  |  {r['sentences']} sentences"
          f"  |  emoji {r['emoji']}  |  hashtags {r['hashtags']}  |  links {r['links']}")
    print("=" * 78)
    print("HOOK (first line):")
    print(f"  | {r['hook_preview']}")
    print("-" * 78)
    if not r["findings"]:
        print("  Nothing to fix.")
    for f in r["findings"]:
        print(f"  {f['level']:<5} {f['check']:<13} {f['msg']}")
    print("-" * 78)
    print(f"  VERDICT: {r['verdict']}\n")


def main():
    ap = argparse.ArgumentParser(description="Lint a Facebook post draft.")
    ap.add_argument("input", nargs="?", default="-")
    ap.add_argument("--lang", default=os.environ.get("FB_LANG", "en"), help="lexicon language: en | pl (default en, or $FB_LANG)")
    ap.add_argument("--lexicon", help="path to a custom lexicon JSON")
    ap.add_argument("--type", help="educational | behind-the-scenes | showcase | opinion | offer")
    ap.add_argument("--max-emoji", type=int, default=3)
    ap.add_argument("--max-hashtags", type=int, default=5)
    ap.add_argument("--fix", action="store_true", help="apply safe fixes")
    ap.add_argument("-o", "--out", help="output file for --fix")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8-sig").read()
    if args.fix:
        cleaned = fix(raw)
        if not args.out:
            sys.stdout.write(cleaned)
            return
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"written: {args.out}", file=sys.stderr)
        raw = cleaned
    lex = load_lexicon(args.lang, args.lexicon)
    r = lint(raw, lex, args.type, args.max_emoji, args.max_hashtags)
    print(json.dumps(r, indent=2, ensure_ascii=False)) if args.json else render(r)
    sys.exit(1 if r["verdict"] == "FAIL" else 0)


if __name__ == "__main__":
    main()
