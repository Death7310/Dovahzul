#!/usr/bin/env python3
"""Independent count check of the canon data files against the raw wikitext.

This script deliberately shares no code with parse_lexicon.py or
parse_corpus.py. It re-derives the basic counts from the saved wikitext with
a few plain regular expressions and compares them with what the JSON files
hold. It writes nothing; it prints a report and exits 1 if a check fails.

Run from the repository root:
    python3 tools/ingest/verify_counts.py

Checks
  1. Dictionary rows (lines starting with ';') per ===Letter=== heading on
     Lore:Dragon Language, against entries per section in canon-lexicon.json;
     also headword, raw line, reference-tag names and plain definition text of
     every row, each re-derived here.
  2. Phrase, name and location rows of the same page.
  3. Word-wall inscriptions: every wordwallN= parameter of every {{WordWall}}
     call on the Skyrim shout pages, and every inscription table on
     Lore:Word Walls, against the word_wall records of canon-corpus.json
     (text and translation compared after the same minimal markup removal).
     Lore:Word Walls prints each wall twice (rune font and Latin letters); the
     rows where those two disagree are listed.
  4. Every record of canon-corpus.json: its revision id is the one in the
     snapshot, and each unit of its dragon text and of its English is found
     on the page it cites.
  5. Every {{hover|English|dragon text}} gloss on the pages: the dragon text
     is in the corpus, and with that gloss.
  6. canon-shouts.json against the {{Shout Summary}} infoboxes and the shout
     table on Online:Dragon; dragon-alphabet.json against the rune tables.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "research", "sources", "uesp")
DATA = os.path.join(ROOT, "research", "data")

failures = []


def check(label, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + label + (("  -- " + detail) if detail else ""))
    if not ok:
        failures.append(label)


def read(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as fh:
        return fh.read()


def strip_templates(text):
    """Remove every {{...}} group, nesting included. Nothing else."""
    out, depth, i = [], 0, 0
    while i < len(text):
        if text.startswith("{{", i):
            depth += 1
            i += 2
        elif text.startswith("}}", i) and depth:
            depth -= 1
            i += 2
        else:
            if not depth:
                out.append(text[i])
            i += 1
    return "".join(out)


def squash(text):
    return re.sub(r"\s+", " ", text).strip()


# ---------------------------------------------------------------- lexicon
def lexicon():
    print("== Lore:Dragon Language against canon-lexicon.json ==")
    lines = read("Lore_Dragon_Language.wikitext").split("\n")
    lex = json.load(open(os.path.join(DATA, "canon-lexicon.json"), encoding="utf-8"))

    raw_rows = []          # (section, line number, line)
    top, letter = None, None
    for n, line in enumerate(lines, 1):
        m = re.match(r"^(=+)\s*(.*?)\s*=+\s*$", line)
        if m:
            if len(m.group(1)) == 2:
                top, letter = m.group(2), None
            elif len(m.group(1)) == 3:
                letter = m.group(2)
            continue
        if top == "Translation Key" and line.startswith(";"):
            raw_rows.append((letter, n, line))

    per_raw, per_json = {}, {}
    for sec, _, _ in raw_rows:
        per_raw[sec] = per_raw.get(sec, 0) + 1
    for e in lex["entries"]:
        per_json[e["section"]] = per_json.get(e["section"], 0) + 1
    print("letter  raw  json")
    for sec in sorted(set(per_raw) | set(per_json)):
        flag = "" if per_raw.get(sec) == per_json.get(sec) else "   <-- differs"
        print("  %-4s %4d %5d%s" % (sec, per_raw.get(sec, 0), per_json.get(sec, 0), flag))
    check("dictionary rows per letter", per_raw == per_json,
          "raw %d, json %d" % (len(raw_rows), len(lex["entries"])))

    bad = {"raw": 0, "line": 0, "word": 0, "refs": 0, "definition_text": 0}
    examples = []
    for (sec, n, line), e in zip(raw_rows, lex["entries"]):
        if e.get("raw") != line:
            bad["raw"] += 1
        if e.get("line") != n:
            bad["line"] += 1
        # cut at the first colon that is not inside a {{template}}
        depth, cut = 0, None
        for i in range(1, len(line)):
            if line.startswith("{{", i):
                depth += 1
            elif line.startswith("}}", i):
                depth -= 1
            elif line[i] == ":" and depth == 0:
                cut = i
                break
        head, rest = (line[1:cut], line[cut + 1:]) if cut else (line[1:], "")
        if squash(strip_templates(head)) != e["word"]:
            bad["word"] += 1
            examples.append(("word", line, e["word"]))
        names = re.findall(r"\{\{\s*[Rr]ef\s*\|\s*name\s*=\s*([^|}]+?)\s*[|}]", line)
        names = [x for i, x in enumerate(names) if x not in names[:i]]   # the JSON lists each name once
        if names != e["refs"]:
            bad["refs"] += 1
            examples.append(("refs", line, e["refs"]))
        plain = squash(re.sub(r"</?small>", "", strip_templates(rest)))
        plain = squash(re.sub(r"''+", "", plain))
        plain = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", plain)
        plain = re.sub(r"\s+([,.;)])", r"\1", plain)
        if plain != squash(e["definition_text"] or ""):
            bad["definition_text"] += 1
            examples.append(("definition_text", line, e["definition_text"]))
    for field, count in bad.items():
        check("every row: %s agrees with an independent reading" % field, count == 0,
              "%d of %d rows differ" % (count, len(raw_rows)))
    for kind, line, got in examples[:12]:
        print("      %s: %s\n         json: %r" % (kind, line, got))

    def block(start, stop):
        a = next(i for i, l in enumerate(lines) if l.strip() == start)
        b = next(i for i, l in enumerate(lines) if l.strip() == stop)
        return lines[a + 1:b]

    phrases = [l for l in block("==Phrases==", "==Names==") if l.startswith("'''")]
    names = [l for l in block("==Names==", "===Locations===") if re.match(r":\s*'''", l)]
    places = [l for l in block("===Locations===", "==Notes==") if re.match(r":\s*'''", l)]
    check("phrases", len(phrases) == len(lex["phrases"]), "raw %d, json %d" % (len(phrases), len(lex["phrases"])))
    check("names", len(names) == len(lex["names"]), "raw %d, json %d" % (len(names), len(lex["names"])))
    check("locations", len(places) == len(lex["locations"]), "raw %d, json %d" % (len(places), len(lex["locations"])))
    check("unparsed is empty", not lex["unparsed"], "%d lines" % len(lex["unparsed"]))


# -------------------------------------------------------------- word walls
def clean_wall(text):
    """Minimal clean-up shared by both sides of the comparison."""
    text = re.sub(r"\{\{\s*FC\s*\|[^|{}]*\|([^{}]*)\}\}", r"\1", text)      # colour highlight
    text = strip_templates(text)                                            # refs, notes, layout
    text = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", text)           # wiki links
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"''+", "", text)
    return "\n".join(squash(part) for part in text.split("\n")).strip()


def font_to_rune_case(code):
    """{{DragonFont}} input -> rune-case (the template's digits stand for two-letter runes)."""
    digits = {"1": "aa", "2": "ei", "3": "ii", "4": "ah", "5": "uu", "6": "ur", "7": "ir",
              "8": "oo", "9": "ey"}       # as documented on Template:DragonFont/Doc
    return "".join(digits.get(ch, ch) for ch in code)


def template_calls(text, name):
    """Yield the inside of every {{name ...}} call, with nesting respected."""
    # template names are matched without regard to case ({{hover|...}} and {{Hover|...}})
    for m in re.finditer(r"\{\{\s*" + re.escape(name) + r"\s*[|\n]", text, flags=re.I):
        depth, i = 0, m.start()
        while i < len(text):
            if text.startswith("{{", i):
                depth += 1
                i += 2
            elif text.startswith("}}", i):
                depth -= 1
                i += 2
                if depth == 0:
                    break
            else:
                i += 1
        yield text[m.start() + 2:i - 2]


def split_params(inner):
    """Split a template body at top-level pipes."""
    parts, depth, cur, i = [], 0, [], 0
    while i < len(inner):
        two = inner[i:i + 2]
        if two in ("{{", "[["):
            depth += 1
            cur.append(two)
            i += 2
        elif two in ("}}", "]]"):
            depth -= 1
            cur.append(two)
            i += 2
        elif inner[i] == "|" and depth == 0:
            parts.append("".join(cur))
            cur = []
            i += 1
        else:
            cur.append(inner[i])
            i += 1
    parts.append("".join(cur))
    return parts


def word_walls():
    print("\n== Word walls against canon-corpus.json ==")
    corpus = json.load(open(os.path.join(DATA, "canon-corpus.json"), encoding="utf-8"))
    walls = [t for t in corpus["texts"] if t["type"] == "word_wall"]
    by_page = {}
    for t in walls:
        by_page.setdefault(t["source_page"], []).append(t)

    manifest = {}
    mdir = os.path.join(SRC, "manifest.d")
    for fn in sorted(os.listdir(mdir)):
        rec = json.load(open(os.path.join(mdir, fn), encoding="utf-8"))
        manifest[rec["title"]] = fn[:-5] + ".wikitext"

    # (a) {{WordWall}} calls on game pages
    raw_total, missing, text_diff, eng_diff = 0, [], [], []
    pages_with_calls = 0
    for title, fname in sorted(manifest.items()):
        if title.startswith("Template:"):
            continue
        text = read(fname)
        found = []
        for inner in template_calls(text, "WordWall"):
            params = {}
            for p in split_params(inner)[1:]:
                k, eq, v = p.partition("=")
                if eq:
                    params[k.strip()] = v
            for n in ("1", "2", "3"):
                if params.get("wordwall" + n, "").strip():
                    found.append((clean_wall(params["wordwall" + n]),
                                  clean_wall(params.get("translation" + n, ""))))
        if not found:
            continue
        pages_with_calls += 1
        raw_total += len(found)
        have = by_page.get(title, [])
        have_text = {t["dovahzul"]: t for t in have}
        for dov, eng in found:
            rec = have_text.get(dov)
            if rec is None:
                loose = [t for t in have if squash(t["dovahzul"]) == squash(dov)]
                if loose:
                    rec = loose[0]
                    text_diff.append((title, dov, rec["dovahzul"]))
                else:
                    missing.append((title, dov))
                    continue
            if (rec.get("english") or "") != eng:
                eng_diff.append((title, eng, rec.get("english")))
    in_corpus = sum(len(v) for k, v in by_page.items() if k.startswith("Skyrim:") and k != "Skyrim:Dragon Language: Myth no More")
    print("  pages with {{WordWall}} text: %d; inscriptions in raw pages: %d; corpus records from those namespaces: %d"
          % (pages_with_calls, raw_total, in_corpus))
    check("shout-page inscriptions: none missing from the corpus", not missing, "%d missing" % len(missing))
    check("shout-page inscriptions: count", raw_total == in_corpus, "raw %d, corpus %d" % (raw_total, in_corpus))
    check("shout-page inscriptions: dragon text identical", not text_diff, "%d differ in line breaks/spacing" % len(text_diff))
    check("shout-page inscriptions: translation identical", not eng_diff, "%d differ" % len(eng_diff))
    for item in (missing + text_diff + eng_diff)[:8]:
        print("     ", repr(item)[:400])

    # (b) Lore:Word Walls inscription tables
    text = read(manifest["Lore:Word Walls"])
    a = text.index("==Known Inscriptions==")
    b = text.index("==Gallery==")
    body = text[a:b]
    sections = re.split(r"^===\s*(.*?)\s*===\s*$", body, flags=re.M)
    lore_raw = []
    for i in range(1, len(sections), 2):
        heading, sec = sections[i], sections[i + 1]
        cells = re.split(r"^\|-\s*$", sec, flags=re.M)
        if len(cells) < 2:
            lore_raw.append((heading, None, None))
            continue
        cols = re.split(r"^\|\s*$", cells[1].split("\n|}")[0], flags=re.M)
        cols = [c.strip() for c in cols if c.strip()]
        runes = None
        m = re.search(r"\{\{\s*DragonFont\s*\|(.*?)\|\s*\d+\s*\}\}", cols[0], flags=re.S) if cols else None
        if m:
            runes = clean_wall(font_to_rune_case(m.group(1)))
        translit = clean_wall(cols[1]) if len(cols) > 1 else None
        english = clean_wall(cols[2]) if len(cols) > 2 else None
        lore_raw.append((heading, runes, translit, english))
    lore_json = by_page.get("Lore:Word Walls", [])
    check("Lore:Word Walls inscription sections", len(lore_raw) == len(lore_json),
          "raw %d, corpus %d" % (len(lore_raw), len(lore_json)))
    # The page gives each wall twice: in rune font and in Latin letters.  Where the two
    # agree the record must hold that text; where the page contradicts itself the record
    # must hold one of the two and keep the other beside it.
    bad_text, bad_eng, split_rows = [], [], []
    for (heading, runes, translit, english), rec in zip(lore_raw, lore_json):
        if rec.get("wall_word") != heading:
            bad_text.append(heading + " (order)")
            continue
        if squash(runes or "") == squash(translit or ""):
            if rec["dovahzul"] != translit:
                bad_text.append(heading)
        else:
            took = "inscription" if rec["dovahzul"] == runes else \
                "transliteration" if rec["dovahzul"] == translit else None
            kept = {rec.get("inscription_column"), rec.get("transliteration_column"), rec["dovahzul"]}
            split_rows.append("%s (record holds the %s column)" % (heading, took))
            if took is None or runes not in kept or translit not in kept:
                bad_text.append(heading)
        if (rec.get("english") or "") != (english or ""):
            bad_eng.append(heading)
    check("Lore:Word Walls wall text identical", not bad_text, "differs under: %s" % ", ".join(bad_text[:10]))
    check("Lore:Word Walls translation identical", not bad_eng, "differs under: %s" % ", ".join(bad_eng[:10]))
    print("  rows where the page's own two columns disagree: %s" % ("; ".join(split_rows) or "none"))

    other = {k: len(v) for k, v in by_page.items() if not k.startswith("Skyrim:") and k != "Lore:Word Walls"}
    print("  word_wall records from other pages:", other)
    print("  word_wall records in total: %d" % len(walls))


# ------------------------------------------------- every record against its page
WORD = re.compile(r"[^\W\d_]+(?:['\u2019][^\W\d_]+)*")


def page_words(text):
    """The page as one string of lower-cased words, with the few templates that sit inside
    dragon text reduced to what they display."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"\{\{\s*DragonFont\s*\|([^|{}]*)",
                  lambda m: " " + font_to_rune_case(m.group(1)) + " ", text, flags=re.I)
    for _ in range(4):
        text = re.sub(r"\{\{\s*FC\s*\|[^|{}]*\|([^{}]*)\}\}", r"\1", text, flags=re.I)
        text = re.sub(r"\{\{\s*sic\s*\|([^|{}]*)\|[^{}]*\}\}", r"\1", text, flags=re.I)
        text = re.sub(r"\{\{\s*(?:Lore Link|Quest Link|Place Link|Item Link)\s*\|(?:[^|{}]*\|)?([^|{}]*)\}\}",
                      r"\1", text, flags=re.I)
        text = re.sub(r"\{\{\s*[Rr]ef\b[^{}]*\}\}", " ", text)
    text = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", text)
    text = re.sub(r"</?[a-zA-Z][^>]*>", " ", text)
    text = text.replace("&nbsp;", " ")
    return " " + " ".join(w.lower().replace("\u2019", "'") for w in WORD.findall(text)) + " "


def record_texts():
    """Does the text of every corpus record stand on the page the record cites?

    Each dragon-language unit (a segment, a line, a shout word) and each English unit is
    looked for as an unbroken run of words on the cited page.  A unit that the parser put
    together from neighbouring hover templates cannot be unbroken on the page; for those it
    is enough that every word of it is there.
    """
    print("\n== Every corpus record against the page it cites ==")
    corpus = json.load(open(os.path.join(DATA, "canon-corpus.json"), encoding="utf-8"))
    files = {}
    mdir = os.path.join(SRC, "manifest.d")
    for fn in sorted(os.listdir(mdir)):
        rec = json.load(open(os.path.join(mdir, fn), encoding="utf-8"))
        files[rec["title"]] = (fn[:-5] + ".wikitext", rec["revid"])
    cache = {}

    def where(title):
        if title not in cache:
            cache[title] = page_words(read(files[title][0]))
        return cache[title]

    def words(text):
        return [w.lower().replace("\u2019", "'") for w in WORD.findall(text)]

    counts = {"dragon": [0, 0, 0], "english": [0, 0, 0]}     # unbroken, split, absent
    absent, wrong_rev = [], []
    for t in corpus["texts"]:
        title = t["source_page"]
        if title not in files:
            absent.append((t["id"], "page not in the snapshot: " + title))
            continue
        if files[title][1] != t["revid"]:
            wrong_rev.append(t["id"])
        if t.get("segments"):
            dz = [sg["dovahzul"] for sg in t["segments"]]
            en = [sg["english"] for sg in t["segments"] if sg.get("english")]
        elif t["type"] == "shout":
            dz, en = t["dovahzul"].split(), (t.get("english") or "").split()
        elif t["type"] == "name":
            dz = [x for x in re.split(r"\s*[/()]\s*", t["dovahzul"]) if x.strip()]
            en = [x for x in re.split(r"\s+\|\s+", t.get("english") or "") if x.strip()]
        else:
            dz = [x for x in t["dovahzul"].split("\n") if x.strip()]
            en = [x for line in (t.get("english") or "").split("\n")
                  for x in re.split(r"\s+\|\s+", line) if x.strip()]
        for kind, units in (("dragon", dz), ("english", en)):
            for unit in units:
                ws = words(unit)
                if not ws:
                    continue
                if " " + " ".join(ws) + " " in where(title):
                    counts[kind][0] += 1
                elif all(" " + w + " " in where(title) for w in ws):
                    counts[kind][1] += 1
                else:
                    counts[kind][2] += 1
                    absent.append((t["id"], kind, unit))
    for kind in ("dragon", "english"):
        a, b, c = counts[kind]
        print("  %s units: %d stand on the cited page as written, %d as separate neighbouring "
              "pieces, %d not found" % (kind, a, b, c))
    check("every record cites the revision that is in the snapshot", not wrong_rev,
          "%d records differ" % len(wrong_rev))
    check("every unit of every record is on the page it cites", not absent,
          "%d not found" % len(absent))
    for item in absent[:10]:
        print("     ", repr(item)[:300])


def hover_glosses():
    """Is every hover gloss on a dragon-language phrase in the corpus, with that gloss?

    The wiki marks most dialogue glosses as {{hover|English|dragon text}}.  The same
    template is used for many other things (damage formulas, alternate lines), so a hover
    counts here only when at least 40% of the words it shows are dictionary headwords.
    Texts are compared word by word, ignoring case and punctuation.
    """
    print("\n== Hover glosses on all pages against canon-corpus.json ==")
    corpus = json.load(open(os.path.join(DATA, "canon-corpus.json"), encoding="utf-8"))
    lex = json.load(open(os.path.join(DATA, "canon-lexicon.json"), encoding="utf-8"))
    heads = set()
    for e in lex["entries"]:
        for form in e["word_forms"]:
            for w in WORD.findall(re.sub(r"[()]", "", form)):
                heads.add(w.lower())

    def key(text):
        text = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", text or "")
        return " ".join(w.lower().replace("\u2019", "'") for w in WORD.findall(text))

    pairs, texts = set(), []
    for t in corpus["texts"]:
        for sg in t.get("segments") or []:
            pairs.add((key(sg["dovahzul"]), key(sg.get("english"))))
        texts.append((" " + key(t["dovahzul"]) + " ", " " + key(t.get("english")) + " "))

    same = other_gloss = 0
    absent, differing = [], []
    mdir = os.path.join(SRC, "manifest.d")
    for fn in sorted(os.listdir(mdir)):
        rec = json.load(open(os.path.join(mdir, fn), encoding="utf-8"))
        if rec["title"].startswith("Template:"):
            continue
        for inner in template_calls(read(fn[:-5] + ".wikitext"), "hover"):
            parts = split_params(inner)
            if len(parts) < 3:
                continue
            gloss, shown = key(parts[1]), key("|".join(parts[2:]))
            words = shown.split()
            if not words or sum(1 for w in words if w in heads) / len(words) < 0.4:
                continue
            if (shown, gloss) in pairs or any(" " + shown + " " in a and " " + gloss + " " in b
                                               for a, b in texts):
                same += 1
            elif any(" " + shown + " " in a for a, b in texts):
                other_gloss += 1
                differing.append((rec["title"], shown, gloss))
            else:
                absent.append((rec["title"], shown, gloss))
    print("  dragon-language hovers on the pages: %d; in the corpus with the same gloss: %d; "
          "in the corpus with another page's wording of the gloss: %d; absent: %d"
          % (same + other_gloss + len(absent), same, other_gloss, len(absent)))
    for item in differing[:10]:
        print("      other wording kept:", repr(item)[:240])
    check("the dragon text of every hover gloss is in the corpus", not absent,
          "%d absent" % len(absent))
    for item in absent[:10]:
        print("     ", repr(item)[:240])


def shouts_and_runes():
    """canon-shouts.json against the {{Shout Summary}} infoboxes and the ESO table;
    dragon-alphabet.json against the two rune tables of Lore:Dragon Alphabet."""
    print("\n== Shouts and runes ==")
    shouts = json.load(open(os.path.join(DATA, "canon-shouts.json"), encoding="utf-8"))
    by_page = {}
    for sh in shouts["shouts"]:
        by_page.setdefault(sh["source_page"], []).append(sh)
    mdir = os.path.join(SRC, "manifest.d")
    pages = words = 0
    diffs = []
    for fn in sorted(os.listdir(mdir)):
        rec = json.load(open(os.path.join(mdir, fn), encoding="utf-8"))
        title = rec["title"]
        if title.startswith("Template:"):
            continue
        for inner in template_calls(read(fn[:-5] + ".wikitext"), "Shout Summary"):
            params = {}
            for part in split_params(inner)[1:]:
                k, eq, v = part.partition("=")
                if eq:
                    params[k.strip()] = v.strip()
            pages += 1
            if title not in by_page:
                diffs.append((title, "no shout record"))
                continue
            sh = by_page[title][0]
            if (sh.get("form_id") or "") != params.get("id", ""):
                diffs.append((title, "id", sh.get("form_id"), params.get("id")))
            for n in "123":
                raw_word = params.get("word" + n, "")
                if not raw_word or raw_word == "N/A":
                    continue
                words += 1
                got = [w for w in sh["words"] if w["position"] == int(n)]
                if not got:
                    diffs.append((title, "word" + n, "missing"))
                    continue
                w = got[0]
                for field, key in (("word_wiki_spelling", "word"), ("meaning", "transword"),
                                   ("word_id", "wordid"), ("recharge_seconds", "cooldown")):
                    if (w.get(field) or "") != params.get(key + n, ""):
                        diffs.append((title, key + n, w.get(field), params.get(key + n)))
    check("Skyrim shout words equal the infoboxes (spelling, meaning, ids, recharge)", not diffs,
          "%d pages, %d words, %d differences" % (pages, words, len(diffs)))
    for item in diffs[:8]:
        print("     ", repr(item)[:240])

    eso_rows = re.findall(r"^\|([A-Z][A-Za-z' ]+?)\s*\|\|\s*([^|\n]*?)\s*\|\|[^\n]*$",
                          read("Online_Dragon.wikitext"), flags=re.M)
    known = {sh["phrase"]: sh for sh in shouts["shouts"] if sh.get("phrase")}
    wrong = [(ph, mean) for ph, mean in eso_rows
             if ph not in known or (known[ph]["game"] == "The Elder Scrolls Online"
                                    and known[ph]["meaning_phrase"] != mean)]
    check("every row of the shout table on Online:Dragon has a shout record", not wrong,
          "%d rows, %d without a matching record" % (len(eso_rows), len(wrong)))

    alpha = json.load(open(os.path.join(DATA, "dragon-alphabet.json"), encoding="utf-8"))
    raw = read("Lore_Dragon_Alphabet.wikitext")
    pairs = []
    for tab in re.findall(r"\{\|.*?\n\|\}", raw, flags=re.S)[:2]:
        heads = None
        for row in re.split(r"\n\|-[^\n]*", tab):
            h = re.findall(r'^!\s*"?([A-Z0-9]+)"?\s*$', row, flags=re.M)
            c = re.findall(r"^\|\{\{DragonFont\|([^}|]+)\}\}", row, flags=re.M)
            if h:
                heads = h
            if c and heads and len(c) == len(heads):
                pairs += list(zip(heads, c))
                heads = None
    got = [(r["latin"], r["dragonfont_template_code"]) for r in alpha["runes"]]
    check("runes and font codes equal the two tables of Lore:Dragon Alphabet", got == pairs,
          "raw %d, json %d" % (len(pairs), len(got)))


if __name__ == "__main__":
    lexicon()
    word_walls()
    record_texts()
    hover_glosses()
    shouts_and_runes()
    print("\n%d check(s) failed" % len(failures) if failures else "\nall checks passed")
    sys.exit(1 if failures else 0)
