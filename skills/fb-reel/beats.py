#!/usr/bin/env python3
"""
beats.py - turn a short-video script into a timed beat sheet before you record it.

Estimates how long each line takes to say (words / speaking rate), stacks the
lines into timecodes, and flags what kills a short video in the edit: a hook
longer than three seconds, a beat long enough for the viewer to leave, a run of
lines with nothing concrete in them, no loop at the end, and a total length that
misses the target.

The timings are an estimate from word count. Good enough to plan an edit, not a
substitute for recording it. Measure your own pace: read 100 words aloud with a
stopwatch and pass the result as --wpm. Default is 150 words per minute.

Works with any language that uses spaces between words (English, Polish, ...).

Usage
  python3 beats.py script.txt
  python3 beats.py script.txt --target 35
  python3 beats.py script.txt --wpm 165 --target 45
  cat script.txt | python3 beats.py -
  python3 beats.py script.txt --json

One line of the file = one beat (one shot or one change of picture).
"""

import argparse
import json
import re
import sys

WORD_RE = re.compile(r"[\w$%'’-]+")
SENT_RE = re.compile(r"[^.!?]+[.!?]*")
CAP_WORD_RE = re.compile(r"(?<![.!?]\s)\b[^\W\d_]{3,}\b")

SPOKEN_NUM = {
    # en
    "zero", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
    "twelve", "fifteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty",
    "ninety", "hundred", "thousand", "million", "billion", "dozen", "half", "twice",
    # pl
    "dwa", "dwie", "trzy", "cztery", "pięć", "sześć", "siedem", "osiem", "dziewięć", "dziesięć",
    "dwadzieścia", "trzydzieści", "czterdzieści", "pięćdziesiąt", "sto", "tysiąc", "tysiące",
    "milion", "połowa", "dwukrotnie",
}
STOPWORDS = {
    # en
    "the", "a", "an", "and", "or", "but", "if", "of", "to", "in", "on", "for", "with", "that",
    "this", "it", "is", "are", "was", "were", "be", "been", "you", "your", "i", "my", "me", "we",
    "our", "they", "them", "he", "she", "so", "just", "not", "no", "do", "did", "does", "have",
    "has", "had", "will", "can", "at", "as", "by", "from", "out", "up", "off", "one", "all",
    # pl
    "i", "a", "o", "w", "z", "na", "do", "to", "że", "się", "nie", "jest", "są", "był", "była",
    "było", "ale", "lub", "oraz", "jak", "co", "za", "po", "od", "dla", "przez", "ten", "ta", "te",
    "tym", "tego", "ja", "ty", "my", "wy", "on", "ona", "mi", "mnie", "ci", "cię", "go", "ją",
    "ich", "tak", "już", "też", "tylko", "bo", "czy", "by", "być",
}

HOOK_WINDOW = 3.0   # seconds. After this the thumb has already decided.
MAX_BEAT = 4.0      # seconds on one idea with no change on screen.
ABSTRACT_RUN = 3    # beats in a row with nothing checkable in them.


def words(text):
    return WORD_RE.findall(text)


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}"


def concrete_count(text, is_first_in_line=True):
    n = len(re.findall(r"\d", text))
    n += sum(1 for w in words(text) if w.lower() in SPOKEN_NUM)
    # capitalised word that is not the first word of the line = probably a name
    toks = words(text)
    n += sum(1 for w in toks[1:] if w[:1].isupper() and len(w) >= 3)
    return n


def split_beats(raw, wps):
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if len(words(line)) / wps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            cand = (buf + " " + part).strip()
            if buf and len(words(cand)) / wps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = cand
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, wpm=150, target=None):
    wps = wpm / 60.0
    beats = split_beats(raw, wps)
    if not beats:
        return None
    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        n = len(words(text))
        dur = n / wps
        rows.append({"n": i + 1, "start": round(clock, 2), "dur": round(dur, 2), "words": n,
                     "text": text, "concrete": concrete_count(text), "label": "", "flags": []})
        clock += dur
    total = clock

    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "HOOK"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "HOOK" else "HOOK/CTA"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "MID"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"hook runs {rows[0]['dur']:.1f}s, past the {HOOK_WINDOW:.0f}s mark")
        notes.append(f"Beat 1 takes {rows[0]['dur']:.1f}s to say. Cut it to {int(HOOK_WINDOW * wps)} "
                     "words or fewer, or the hook lands after the viewer has decided.")
    if sum(r["concrete"] for r in rows if r["label"].startswith("HOOK")) == 0:
        notes.append("The hook (first 3s) has no number and no name. Hooks without something "
                     "checkable get scrolled past.")

    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f}s on one beat")
    if long_beats:
        notes.append(f"Beat(s) {', '.join(map(str, long_beats))} run past {MAX_BEAT:.0f}s. Split the "
                     "line or change what is on screen inside it. A static frame is where people leave.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Beats {start}-{r['n']} have nothing concrete. Put a number, a name or a price in one of them.")
        else:
            run, start = 0, None

    first = {w.lower() for w in words(rows[0]["text"]) if w.lower() not in STOPWORDS and len(w) > 2}
    last = {w.lower() for w in words(rows[-1]["text"]) if w.lower() not in STOPWORDS and len(w) > 2}
    loop = sorted(first & last)
    if loop:
        notes.append(f"Loop: the last beat repeats '{', '.join(loop[:3])}' from the hook. Replays are free reach.")
    else:
        notes.append("No loop. The last beat shares no word with the hook, so the video ends flat. "
                     "Echo one word from beat 1.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"Length is on target ({total:.1f}s against {target:.0f}s).")
        elif delta > 0:
            notes.append(f"{delta:.1f}s over target. Cut about {int(delta * wps)} words.")
        else:
            notes.append(f"{-delta:.1f}s under target. Add {int(-delta * wps)} words or shoot it short. Short is usually right.")

    return {"wpm": wpm, "target": target, "total_seconds": round(total, 2),
            "total_words": sum(r["words"] for r in rows), "beats": rows, "notes": notes}


def render(a):
    head = (f"BEAT SHEET  |  {a['total_words']} words  |  ~{a['total_seconds']:.1f}s at {a['wpm']:.0f} wpm"
            + (f"  |  target {a['target']:.0f}s" if a["target"] else ""))
    print("\n" + head)
    print("=" * max(len(head), 72))
    for r in a["beats"]:
        label = f"{r['label']:<9}" if r["label"] else " " * 9
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {label}{r['text']}")
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<9}^ {f}")
    print("-" * max(len(head), 72))
    for n in a["notes"]:
        print(f"  - {n}")
    print("")


def main():
    ap = argparse.ArgumentParser(description="Beat sheet from a short-video script.")
    ap.add_argument("input", nargs="?", default="-")
    ap.add_argument("--wpm", type=float, default=150)
    ap.add_argument("--target", type=float)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8-sig").read()
    a = analyse(raw, wpm=args.wpm, target=args.target)
    if not a:
        print("empty script", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(a, indent=2, ensure_ascii=False)) if args.json else render(a)


if __name__ == "__main__":
    main()
