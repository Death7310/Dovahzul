#!/usr/bin/env python3
"""Parse the UESP snapshot into the canon dragon-language corpus.

Standard library only.  Reads the pages that tools/ingest/fetch_corpus.py saved
under research/sources/uesp/ and writes three files:

    research/data/canon-corpus.json      word walls, songs, dialogue, names, ...
    research/data/canon-shouts.json      every shout with its words and meanings
    research/data/dragon-alphabet.json   every rune with its Latin value

Run from anywhere:

    python3 tools/ingest/parse_corpus.py
    python3 tools/ingest/parse_corpus.py --report    # also print a summary

Rules this parser keeps:

  * Nothing is translated here.  Every English gloss is text that stands on the
    wiki page; where the wiki gives none, "english" is null.
  * The wiki's spelling is kept.  In word-wall and alphabet material the wiki
    writes one-rune letters in upper case and the nine two-letter runes in
    lower case (aa ah ei ey ii ir oo uu ur), e.g. "DOVahKiiN".  That casing is
    data: it says which rune was carved.  It is not normalised away.
  * Line breaks (<br>) are kept as newlines.
  * {{sic|written|corrected}} keeps what was written; the correction goes into
    the notes.  {{huh}}, {{vn}} and hedging words set "uncertain".
  * The dictionary page Lore:Dragon_Language belongs to another tool.  If its
    snapshot is present it is only READ here, as a word list for spotting
    dragon words that stand un-glossed inside English dialogue lines.
  * Where the wiki prints the same line on several pages the record is kept
    once, with the other pages under "also_on"; where the same dragon text has
    two different English renderings both are kept and linked by
    "duplicate_of".

What is heuristic (and flagged as such in the output): finding un-glossed
dragon words inside English dialogue by word-list match, attributing a quote to
a speaker when the wiki gives no label, and reading name meanings out of prose
sentences.  Every such record keeps the wiki's full line or sentence beside it.

Everything read from the snapshot is treated as data and never executed.
"""

import argparse
import hashlib
import html
import json
import re
import sys
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "research" / "sources" / "uesp"
MANIFEST_DIR = SRC_DIR / "manifest.d"
OUT_DIR = REPO_ROOT / "research" / "data"
LEXICON_PAGE = "Lore:Dragon Language"          # read-only, optional

FONT_DIGITS = {"1": "aa", "2": "ei", "3": "ii", "4": "ah", "5": "uu",
               "6": "ur", "7": "ir", "8": "oo", "9": "ey"}
DIGRAPHS = ["aa", "ah", "ei", "ey", "ii", "ir", "oo", "uu", "ur"]

PH_OPEN, PH_CLOSE = "", ""       # private-use marks for hovers


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------
class Page:
    def __init__(self, manifest, text):
        self.title = manifest["title"]
        self.revid = manifest["revid"]
        self.timestamp = manifest.get("timestamp")
        self.groups = manifest.get("groups") or []
        self.manifest = manifest
        self.text = text
        self.ns, _, self.name = self.title.partition(":")
        if not _:
            self.ns, self.name = "", self.title
        self.subject = re.sub(r"\s*\([^)]*\)\s*$", "", self.name)


def load_pages():
    pages = OrderedDict()
    for mf in sorted(MANIFEST_DIR.glob("*.json")):
        manifest = json.loads(mf.read_text(encoding="utf-8"))
        wt = SRC_DIR / (mf.stem + ".wikitext")
        if not wt.exists():
            continue
        raw = wt.read_bytes()
        if hashlib.sha256(raw).hexdigest() != manifest.get("sha256"):
            sys.stderr.write("WARNING sha256 mismatch, skipping %s\n" % wt.name)
            continue
        pages[manifest["title"]] = Page(manifest, raw.decode("utf-8"))
    return pages


# ---------------------------------------------------------------------------
# Wikitext helpers
# ---------------------------------------------------------------------------
def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def template_spans(text):
    """All {{...}} spans, outermost and nested, as (start, end)."""
    stack, out, i, n = [], [], 0, len(text)
    while i < n - 1:
        two = text[i:i + 2]
        if two == "{{":
            stack.append(i)
            i += 2
        elif two == "}}" and stack:
            out.append((stack.pop(), i + 2))
            i += 2
        else:
            i += 1
    return sorted(out)


def split_top(s, sep="|"):
    """Split on sep outside {{ }} and [[ ]]."""
    parts, depth_c, depth_s, cur, i, n = [], 0, 0, [], 0, len(s)
    while i < n:
        two = s[i:i + 2]
        if two == "{{":
            depth_c += 1; cur.append(two); i += 2; continue
        if two == "}}" and depth_c:
            depth_c -= 1; cur.append(two); i += 2; continue
        if two == "[[":
            depth_s += 1; cur.append(two); i += 2; continue
        if two == "]]" and depth_s:
            depth_s -= 1; cur.append(two); i += 2; continue
        if s.startswith(sep, i) and depth_c == 0 and depth_s == 0:
            parts.append("".join(cur)); cur = []; i += len(sep); continue
        cur.append(s[i]); i += 1
    parts.append("".join(cur))
    return parts


def template_calls(text, wanted=None):
    """Yield (name_lower, params_dict, positional_list, start, end)."""
    for start, end in template_spans(text):
        inner = text[start + 2:end - 2]
        parts = split_top(inner)
        name = parts[0].strip().replace("_", " ").lower()
        if wanted and name not in wanted:
            continue
        named, positional = OrderedDict(), []
        for p in parts[1:]:
            m = re.match(r"\s*([A-Za-z0-9_ ]+?)\s*=(.*)\Z", p, flags=re.S)
            if m:
                named[m.group(1).strip().lower()] = m.group(2)
            else:
                positional.append(p)
        yield name, named, positional, start, end


def decode_font(s):
    """{{DragonFont}} input -> the wiki's rune spelling (digits are two-letter runes)."""
    return "".join(FONT_DIGITS.get(ch, ch) for ch in s)


def strip_refs(text):
    text = re.sub(r"<ref[^>/]*/>", "", text)
    text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.S)
    # {{ref|...}} / {{Ref|...}} with nested templates
    out, last = [], 0
    spans = [(s, e) for s, e in template_spans(text)
             if re.match(r"\{\{\s*(ref|intnote|rp)\s*[|}]", text[s:e], flags=re.I)]
    outer = []
    for s, e in spans:
        if outer and s < outer[-1][1]:
            continue
        outer.append((s, e))
    for s, e in outer:
        out.append(text[last:s]); last = e
    out.append(text[last:])
    return "".join(out)


_INNER_T = re.compile(r"\{\{([^{}]*)\}\}")


def _template_text(inner, sic_log=None, flags=None):
    parts = split_top(inner)
    name = parts[0].strip().replace("_", " ").lower()
    pos = [p for p in parts[1:] if not re.match(r"\s*[A-Za-z0-9_ ]+=", p)]
    if name in ("fc",):
        return pos[-1] if pos else ""
    if name == "hover":
        return pos[1] if len(pos) > 1 else ""
    if name == "sic":
        if sic_log is not None and len(pos) > 1:
            sic_log.append((pos[0].strip(), pos[1].strip()))
        return pos[0] if pos else ""
    if name in ("lore link", "ore link", "place link", "book link", "item link",
                "quest link", "cite book", "bullet link"):
        if not pos:
            return ""
        return pos[1] if len(pos) > 1 and name != "cite book" else pos[0]
    if name == "dragonfont":
        return decode_font(pos[0]) if pos else ""
    if name in ("letterpic", "year", "anchor", "card", "small", "tag", "nowrap"):
        return pos[-1] if (pos and name == "anchor") else (pos[0] if pos else "")
    if name == "huh":
        if flags is not None:
            flags.add("wiki marks this as unknown ({{huh}})")
        return "[?]"
    if name in ("vn", "fact"):
        if flags is not None:
            flags.add("wiki marks this as needing verification ({{%s}})" % name)
        return ""
    if name == "!":
        return "|"
    if name == "pagename":
        return ""
    return ""


MARKUP_TAGS = ("small|big|center|span|div|sup|sub|b|i|u|s|font|nowiki|noinclude|includeonly|"
               "onlyinclude|code|tt|pre|blockquote|p|hr|table|tr|td|th|ul|ol|li|gallery|poem|"
               "section|references|ref|abbr|cite|em|strong|del|ins|q|var|kbd|samp|strike|h[1-6]|"
               "cleanspace|cleantable")


def clean(text, sic_log=None, flags=None, keep_newlines=True):
    """Inline wikitext -> plain text.  <br> becomes a newline."""
    if text is None:
        return None
    t = strip_comments(text)
    t = strip_refs(t)
    for _ in range(12):
        new = _INNER_T.sub(lambda m: _template_text(m.group(1), sic_log, flags), t)
        if new == t:
            break
        t = new
    # files and categories go; other links keep their label
    for _ in range(3):
        t = re.sub(r"\[\[(?:File|Image|Category):(?:[^\[\]]|\[\[[^\[\]]*\]\])*\]\]", "", t,
                   flags=re.I)
    t = re.sub(r"\[\[(?:[^\[\]|]*\|)?([^\[\]|]*)\]\]", r"\1", t)
    t = re.sub(r"\[(?:https?:)?//[^\s\]]+\s+([^\]]+)\]", r"\1", t)
    t = re.sub(r"\[(?:https?:)?//[^\s\]]+\]", "", t)
    t = re.sub(r"<br\s*/?>", "\n", t, flags=re.I)
    # Only mark-up tags are removed.  Other text in angle brackets is the game's own
    # placeholder (e.g. "<man/woman>", "<Alias=Player>") and stays in the line.
    t = re.sub(r"</?(?:%s)\b[^<>]*>" % MARKUP_TAGS, "", t, flags=re.I)
    t = re.sub(r"__[A-Z]+__", "", t)
    t = re.sub(r"'{2,}", "", t)
    t = html.unescape(t).replace(" ", " ")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    if not keep_newlines:
        t = re.sub(r"\s*\n\s*", " ", t)
    return t.strip()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


WORD_RE = re.compile(r"[^\W\d_]+(?:['’\-][^\W\d_]+)*")


def tokens(s):
    return WORD_RE.findall(s or "")


def norm(s):
    return " ".join(t.lower() for t in tokens(s or ""))


def runes_of(word):
    """Wiki rune-case spelling -> list of rune values (upper-case Latin values)."""
    out, i = [], 0
    while i < len(word):
        two = word[i:i + 2]
        if two in DIGRAPHS:
            out.append(two.upper()); i += 2
        elif word[i].isalpha():
            out.append(word[i].upper()); i += 1
        else:
            i += 1
    return out


def sections(text):
    """Yield (level, heading, body) for each == heading == block (plus the lead)."""
    pat = re.compile(r"^(={2,6})\s*(.*?)\s*\1\s*$", flags=re.M)
    last_end, level, head = 0, 0, ""
    for m in pat.finditer(text):
        yield level, head, text[last_end:m.start()]
        level, head, last_end = len(m.group(1)), m.group(2), m.end()
    yield level, head, text[last_end:]


def heading_before(text, pos):
    best = ""
    for m in re.finditer(r"^(={2,6})\s*(.*?)\s*\1\s*$", text[:pos], flags=re.M):
        best = m.group(2)
    return clean(best)


# --- tables ----------------------------------------------------------------
def table_blocks(text):
    """Outermost {| ... |} blocks as (start, end)."""
    out, depth, start = [], 0, None
    for m in re.finditer(r"^\s*:*\s*(\{\||\|\})", text, flags=re.M):
        if m.group(1) == "{|":
            if depth == 0:
                start = m.start()
            depth += 1
        elif depth:
            depth -= 1
            if depth == 0:
                out.append((start, m.end()))
    return out


def _cell_content(cell):
    parts = split_top(cell, "|")
    if len(parts) > 1 and "[[" not in parts[0] and "{{" not in parts[0] and \
            ("=" in parts[0] or re.fullmatch(r"\s*[a-z]+\s*", parts[0] or "x")):
        return "|".join(parts[1:])
    return cell


def parse_table(block):
    """-> list of rows; each row is a list of (is_header, raw cell text)."""
    lines = block.split("\n")[1:]
    rows, row, cur = [], [], None

    def flush_cell():
        nonlocal cur
        if cur is not None:
            row.append((cur[0], _cell_content(cur[1]).strip()))
            cur = None

    for line in lines:
        s = line.strip()
        if s.startswith("|}"):
            break
        if s.startswith("|-"):
            flush_cell()
            if row:
                rows.append(row)
            row = []
            continue
        if s.startswith("|+"):
            continue
        if s.startswith("!") or s.startswith("|"):
            flush_cell()
            is_h = s.startswith("!")
            body = s[1:]
            pieces = split_top(body, "!!") if is_h else split_top(body, "||")
            if is_h and len(pieces) == 1:
                pieces = split_top(body, "||")
            for p in pieces[:-1]:
                row.append((is_h, _cell_content(p).strip()))
            cur = [is_h, pieces[-1]]
        elif cur is not None:
            cur[1] += "\n" + line
    flush_cell()
    if row:
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Corpus assembly
# ---------------------------------------------------------------------------
class Corpus:
    def __init__(self):
        self.texts = []
        self.ids = Counter()
        self.pages_used = Counter()

    def add(self, typ, page, where, dovahzul, english, notes=None, base_id=None, **extra):
        if not dovahzul or not dovahzul.strip():
            return None
        base = base_id or "%s-%s" % (typ.replace("_", ""), slug(page.title))
        self.ids[base] += 1
        tid = "%s-%d" % (base, self.ids[base])
        entry = OrderedDict([
            ("id", tid), ("type", typ), ("source_page", page.title),
            ("revid", page.revid), ("location_or_speaker", where),
            ("dovahzul", dovahzul), ("english", english),
            ("notes", notes or None),
        ])
        for k, v in extra.items():
            if v not in (None, [], ""):
                entry[k] = v
        self.texts.append(entry)
        self.pages_used[page.title] += 1
        return entry


# ---------------------------------------------------------------------------
# b. Shouts
# ---------------------------------------------------------------------------
def word_display(w):
    return w[:1].upper() + w[1:].lower() if w else w


def parse_shout_pages(pages):
    shouts = []
    available = set()
    ds = pages.get("Skyrim:Dragon Shouts")
    if ds:
        for name, named, pos, s, e in template_calls(ds.text, {"shout entry"}):
            if pos:
                available.add(pos[0].strip())
    for page in pages.values():
        if page.ns != "Skyrim":
            continue
        for name, p, pos, s, e in template_calls(page.text, {"shout summary"}):
            flags = set()
            words = []
            for i in (1, 2, 3):
                w = clean(p.get("word%d" % i, ""), flags=flags)
                if not w or w.upper() == "N/A":
                    continue
                meaning = clean(p.get("transword%d" % i, ""), flags=flags)
                letters = clean(p.get("letters%d" % i, "")) or None
                words.append(OrderedDict([
                    ("position", i),
                    ("word", word_display(w)),
                    ("word_wiki_spelling", w),
                    ("runes", runes_of(w)),
                    ("meaning", None if meaning.upper() == "N/A" else meaning),
                    ("word_id", clean(p.get("wordid%d" % i, "")) or None),
                    ("effect", clean(p.get("info%d" % i, "")) or None),
                    ("recharge_seconds", clean(p.get("cooldown%d" % i, "")) or None),
                    ("location", clean(p.get("location%d" % i, "")) or None),
                    ("font_letters_param", letters),
                ]))
            mod = clean(p.get("mod", "")) or None
            game = {"DB": "Skyrim: Dragonborn", "DG": "Skyrim: Dawnguard"}.get(mod, "Skyrim")
            shout_name = page.subject
            locs = [w["location"] for w in words if w["location"]]
            lead = clean(page.text[e:e + 1500].split("\n==")[0], keep_newlines=False)
            lead = re.sub(r"^\s*(?:\S+\.(?:jpg|png)\S*)?\s*", "", lead)
            first = re.split(r"(?<=[.!?])\s+", lead.strip())
            shouts.append(OrderedDict([
                ("id", "shout-" + slug(shout_name)),
                ("name", shout_name),
                ("game", game),
                ("availability", "player" if shout_name in available
                 else "not on the wiki's list of shouts available to the player"),
                ("phrase", " ".join(w["word"] for w in words) or None),
                ("meaning_phrase", " ".join((w["meaning"] or "?") for w in words) or None),
                ("words", words),
                ("form_id", clean(p.get("id", "")) or None),
                ("in_game_description", (lambda q: None if q.upper() == "N/A" else q)(
                    clean(p.get("quote", "")))),
                ("locations", locs),
                ("wiki_summary", " ".join(first[:2]) if first and first[0] else None),
                ("source_page", page.title),
                ("revid", page.revid),
                ("source_kind", "Skyrim shout page ({{Shout Summary}} infobox)"),
                ("notes", "; ".join(sorted(flags)) or None),
                ("also_attested_in", []),
            ]))
    have = {s["source_page"] for s in shouts}
    for page in pages.values():
        if page.ns == "Skyrim" and page.title not in have and \
                re.search(r"is an exclusive \[\[Skyrim:Dragon Shouts\|shout\]\]", page.text):
            lead = [clean(l, keep_newlines=False) for l in page.text.split("\n")
                    if l.startswith("'''" + page.subject)]
            shouts.append(OrderedDict([
                ("id", "shout-" + slug(page.subject)), ("name", page.subject), ("game", "Skyrim"),
                ("availability", "not available to the player (dragon or NPC only)"),
                ("phrase", None), ("meaning_phrase", None), ("words", []),
                ("form_id", None), ("in_game_description", None), ("locations", []),
                ("wiki_summary", lead[0] if lead else None),
                ("source_page", page.title), ("revid", page.revid),
                ("source_kind", "Skyrim shout page without a {{Shout Summary}} infobox"),
                ("notes", "the wiki gives no words of power for this shout"),
                ("also_attested_in", []),
            ]))
    return shouts, available


def add_attestation(shouts, phrase, meanings, name, page, kind, note=None, extra=None):
    """Attach an attestation to the shout with the same words, or add a new shout."""
    key = norm(phrase)
    att = OrderedDict([("source_page", page.title), ("revid", page.revid),
                       ("source_kind", kind), ("name_there", name),
                       ("phrase_there", phrase), ("meaning_there", meanings),
                       ("note", note)])
    for sh in shouts:
        if sh["phrase"] and norm(sh["phrase"]) == key and key:
            if meanings and sh["meaning_phrase"] and norm(meanings) != norm(sh["meaning_phrase"]):
                att["differs_from_primary"] = True
            sh["also_attested_in"].append(att)
            return sh
    wl = tokens(phrase)
    ml = [m.strip() for m in re.split(r"\s+(?![^(]*\))", meanings.strip())] if meanings else []
    words = []
    for i, w in enumerate(wl, 1):
        words.append(OrderedDict([
            ("position", i), ("word", word_display(w)), ("word_wiki_spelling", w),
            ("runes", None),
            ("meaning", ml[i - 1] if len(ml) == len(wl) else None),
        ]))
    sh = OrderedDict([
        ("id", "shout-" + slug(name or phrase)),
        ("name", name),
        ("game", (extra or {}).get("game")),
        ("availability", (extra or {}).get("availability")),
        ("phrase", " ".join(word_display(w) for w in wl) or None),
        ("meaning_phrase", meanings or None),
        ("words", words),
        ("form_id", None), ("in_game_description", None), ("locations", []),
        ("wiki_summary", note),
        ("source_page", page.title), ("revid", page.revid),
        ("source_kind", kind),
        ("notes", (extra or {}).get("notes")),
        ("also_attested_in", []),
    ])
    if len(ml) != len(wl) and meanings:
        sh["notes"] = ((sh["notes"] + "; ") if sh["notes"] else "") + \
            "word-by-word meanings not aligned automatically; see meaning_phrase"
    shouts.append(sh)
    return sh


def parse_unavailable_shouts(pages, shouts):
    page = pages.get("Skyrim:Dragon Shouts")
    if not page:
        return
    for level, head, body in sections(page.text):
        if clean(head) != "Unavailable Dragon Shouts":
            continue
        for line in body.split("\n"):
            if not line.startswith("*"):
                continue
            txt = clean(line.lstrip("* "), keep_newlines=False)
            m = re.search(r'words of power are "([^"]+)",? (?:which |and )?(?:is |are )?'
                          r'(?:translate[ds]?|translated) (?:to|as) "([^"]+)"', txt)
            anchors = [pos[0].strip() for n, nd, pos, s, e in
                       template_calls(line, {"anchor"}) if pos]
            links = re.findall(r"\[\[Skyrim:([^|\]]+?)\u200e?(?:\|[^\]]*)?\]\]", line)
            if m:
                name = None
                if anchors:
                    name = anchors[0]
                else:
                    for l in links:
                        if any(norm(l) == norm(s["name"]) for s in shouts) or \
                                l.strip("\u200e ") in ("Phantom Form", "Soul Cairn Summon"):
                            name = l.strip("\u200e ")
                            break
                if name is None:
                    if "soul-snare mist" in txt.lower():
                        name = "Soul-snare mist (Alduin, Sovngarde)"
                    elif "Tsun" in txt:
                        name = "Tsun's shout returning the player to Nirn"
                add_attestation(shouts, m.group(1), m.group(2), name, page,
                                "Skyrim:Dragon Shouts, section 'Unavailable Dragon Shouts'",
                                note=txt,
                                extra={"game": "Skyrim",
                                       "availability": "not available to the player (dragon or NPC only)"})
            elif anchors and "Bex" not in txt:
                sh = OrderedDict([
                    ("id", "shout-" + slug(anchors[0])), ("name", anchors[0]),
                    ("game", "Skyrim"),
                    ("availability", "not available to the player (dragon or NPC only)"),
                    ("phrase", None), ("meaning_phrase", None), ("words", []),
                    ("form_id", None), ("in_game_description", None), ("locations", []),
                    ("wiki_summary", txt),
                    ("source_page", page.title), ("revid", page.revid),
                    ("source_kind", "Skyrim:Dragon Shouts, section 'Unavailable Dragon Shouts'"),
                    ("notes", "the wiki gives no words of power for this shout"),
                    ("also_attested_in", []),
                ])
                shouts.append(sh)
            m2 = re.search(r'by saying "(\w+)", meaning "(\w+)"', txt)
            if m2:
                add_attestation(shouts, m2.group(1), m2.group(2),
                                "Open (Borri's gate word; the wiki says it is a script, not a shout)",
                                page, "Skyrim:Dragon Shouts, section 'Unavailable Dragon Shouts'",
                                note=txt,
                                extra={"game": "Skyrim",
                                       "availability": "not a shout according to the wiki (a script)"})


def parse_lore_thuum(pages, shouts):
    page = pages.get("Lore:Thu'um")
    if not page:
        return []
    listed = []
    for level, head, body in sections(page.text):
        if clean(head) != "Known Shouts":
            continue
        for line in body.split("\n"):
            m = re.match(r"\*\s*'''(.+?)'''(?:\s*/\s*'''(.+?)''')?\s*-\s*(.*)", line)
            if not m:
                continue
            name = clean(m.group(1))
            rest = clean(m.group(3), keep_newlines=False)
            mm = re.match(r'([A-Z][\w\']*(?: [A-Z][\w\']*){0,3}), meaning "?(.+?)"?, '
                          r'(?:is a|allows|can |summons|are )', rest)
            entry = OrderedDict([("name", name),
                                 ("alternate_name", clean(m.group(2)) if m.group(2) else None),
                                 ("phrase", None), ("meaning_phrase", None),
                                 ("description", rest)])
            if mm:
                entry["phrase"], entry["meaning_phrase"] = mm.group(1), mm.group(2)
                add_attestation(shouts, mm.group(1), mm.group(2), name, page,
                                "Lore:Thu'um, list 'Known Shouts'", note=rest,
                                extra={"game": "lore"})
            elif re.fullmatch(r"[A-Z]\w+ [A-Z]\w+ [A-Z]\w+", name) and "shout used by" in rest:
                entry["phrase"] = name
                add_attestation(shouts, name, None, name, page,
                                "Lore:Thu'um, list 'Known Shouts'", note=rest,
                                extra={"game": "lore"})
            listed.append(entry)
    return listed


def parse_eso_shouts(pages, shouts):
    page = pages.get("Online:Dragon")
    out = []
    if not page:
        return out
    for s, e in table_blocks(page.text):
        rows = parse_table(page.text[s:e])
        if not rows:
            continue
        heads = [clean(c[1]).lower() for c in rows[0]]
        if heads[:2] != ["shout", "translated"]:
            continue
        for row in rows[1:]:
            cells = [clean(c[1], keep_newlines=False) for c in row]
            if len(cells) < 2 or not cells[0]:
                continue
            ability = cells[2] if len(cells) > 2 and cells[2] else None
            remark = ability if (ability or "").startswith("(") else None
            out.append((cells[0], cells[1], ability))
            add_attestation(shouts, cells[0], cells[1], None, page,
                            "Online:Dragon, table of shouts spoken by generic dragons in ESO",
                            note=("Corresponding ability: " + ability) if ability else None,
                            extra={"game": "The Elder Scrolls Online",
                                   "availability": "dragon only (ESO)",
                                   "notes": ("ESO shout line; the wiki gives a remark in place of an "
                                             "ability name: " + remark) if remark else
                                   "ESO shout line; name is the ESO ability the wiki pairs it with"
                                   if ability else "ESO shout line; the wiki names no ability for it"})
            sh = [x for x in shouts if x["phrase"] and norm(x["phrase"]) == norm(cells[0])]
            if sh and sh[0]["game"] == "The Elder Scrolls Online":
                unknown = [w["word"] for w in sh[0]["words"] if w["meaning"] == "???"]
                for w in sh[0]["words"]:
                    if w["meaning"] == "???":
                        w["meaning"] = None
                if unknown and "unknown" not in (sh[0]["notes"] or ""):
                    sh[0]["notes"] += "; the wiki marks the meaning of %s as unknown (???)" \
                        % ", ".join(unknown)
            if sh and sh[0]["name"] is None and sh[0]["game"] == "The Elder Scrolls Online":
                sh[0]["name"] = None if (ability or "").startswith("(") else ability
                sh[0]["id"] = "shout-eso-" + slug(cells[0])
    return out


def parse_legends_audio(pages, shouts, corpus, lex):
    for page in pages.values():
        if page.ns != "Legends":
            continue
        for name, p, pos, s0, e0 in template_calls(page.text, {"legends audio", "legends audio 2"}):
            use = clean(p.get("use", "")) or None
            level = clean(p.get("headertext", "")) or None
            is_shout = clean(p.get("creature", "")) == "shout"
            for key in ("text", "text2", "text3", "text4"):
                text = clean(p.get(key, ""))
                if not text:
                    continue
                if is_shout:
                    k = norm(text)
                    for sh in shouts:
                        if sh["phrase"] and (norm(sh["phrase"]) == k or
                                             norm(sh["phrase"]).startswith(k + " ")):
                            sh["also_attested_in"].append(OrderedDict([
                                ("source_page", page.title), ("revid", page.revid),
                                ("source_kind", "Legends card audio line"),
                                ("name_there", page.name), ("phrase_there", text),
                                ("meaning_there", None), ("note", level)]))
                            break
                    corpus.add("shout", page, "%s (Legends card), %s" % (page.name, level or use),
                               text, None, base_id="shouttext-" + slug(page.title),
                               notes="Card audio line in The Elder Scrolls: Legends; the page "
                                     "gives no translation.",
                               subtype="legends_card_audio", canon_status="canon",
                               source_title="The Elder Scrolls: Legends")
                    continue
                segs = dragon_runs(text, lex)
                if not segs:
                    continue
                gloss = None
                for line in page.text.split("\n"):
                    cl = clean(line, keep_newlines=False)
                    if any(sg.rstrip(".!") in cl for sg in segs) and \
                            re.search(r"\b(means|translates)\b", cl):
                        gloss = cl.lstrip("* ")
                for sh in shouts:
                    if sh["phrase"] and any(norm(sg) == norm(sh["phrase"]) for sg in segs):
                        sh["also_attested_in"].append(OrderedDict([
                            ("source_page", page.title), ("revid", page.revid),
                            ("source_kind", "Legends card audio line"),
                            ("name_there", page.name), ("phrase_there", text),
                            ("meaning_there", None), ("note", use)]))
                corpus.add("dialogue", page, "%s (Legends card audio, %s)" % (page.name, use),
                           "\n".join(segs), None, base_id="dlg-" + slug(page.title),
                           notes=("Card audio line: \"%s\". " % text) +
                                 ("Wiki note on the page: " + gloss if gloss else
                                  "The page gives no translation."),
                           subtype="legends_card_audio", context=text, canon_status="canon",
                           source_title="The Elder Scrolls: Legends",
                           gloss_source="none as a field; see notes" if gloss else None)


def parse_other_title_shouts(pages, shouts, corpus):
    """Shout lines recorded for Skyrim Very Special Edition and as ESO ability names."""
    page = pages.get("SkyrimVSE:Combat")
    if page:
        for s0, e0 in table_blocks(page.text):
            rows = parse_table(page.text[s0:e0])
            if not rows or [clean(c[1]).lower() for c in rows[0]] != ["shout level", "shout"]:
                continue
            for row in rows[1:]:
                if len(row) < 2:
                    continue
                level, text = clean(row[0][1]), clean(row[1][1])
                first = (tokens(text) or [""])[0].lower()
                for sh in shouts:
                    if sh["words"] and sh["game"].startswith("Skyrim") and \
                            sh["words"][0]["word"].lower() == first:
                        sh["also_attested_in"].append(OrderedDict([
                            ("source_page", page.title), ("revid", page.revid),
                            ("source_kind", "Skyrim Very Special Edition, 'Shout Progression' table"),
                            ("name_there", None), ("phrase_there", text), ("meaning_there", None),
                            ("note", "learned at shout level " + level)]))
                        break
                corpus.add("shout", page, "Skyrim Very Special Edition, shout level " + level, text,
                           None, base_id="shouttext-skyrim-vse",
                           notes="Line from the 'Shout Progression' table; spelling as on the "
                                 "wiki page (it writes 'Roh'). No translation on the page.",
                           subtype="vse_shout_line", canon_status="canon",
                           source_title="Skyrim Very Special Edition")
    for page in pages.values():
        if page.ns != "Online":
            continue
        for line in page.text.split("\n"):
            m = re.match(r";\s*([A-Z][a-z]+ [a-z]+ [a-z]+)\s*:", line)
            if not m:
                continue
            for sh in shouts:
                if sh["phrase"] and norm(sh["phrase"]) == norm(m.group(1)):
                    sh["also_attested_in"].append(OrderedDict([
                        ("source_page", page.title), ("revid", page.revid),
                        ("source_kind", "ESO ability name on a boss page"),
                        ("name_there", m.group(1)), ("phrase_there", m.group(1)),
                        ("meaning_there", None),
                        ("note", clean(line.split(":", 1)[1], keep_newlines=False)[:200])]))


# ---------------------------------------------------------------------------
# a. Word walls
# ---------------------------------------------------------------------------
def fc_words(raw):
    return [clean(pos[-1]) for n, nd, pos, s, e in template_calls(raw, {"fc"}) if pos]


def parse_word_walls(pages, shouts, corpus):
    by_name = {s["name"]: s for s in shouts}
    for page in pages.values():
        if page.ns != "Skyrim":
            continue
        for name, p, pos, s, e in template_calls(page.text, {"wordwall"}):
            head = heading_before(page.text, s)
            unused = bool(re.search(r"unused|only in the game files", head, flags=re.I))
            allwords = clean(p.get("allwords", "")).lower() == "true"
            shout = by_name.get(page.subject)
            n_walls = sum(1 for i in (1, 2, 3) if p.get("wordwall%d" % i))
            for i in (1, 2, 3):
                raw_d, raw_e = p.get("wordwall%d" % i), p.get("translation%d" % i)
                if not raw_d:
                    continue
                sic, flags = [], set()
                dz = clean(raw_d, sic_log=sic, flags=flags)
                en = clean(raw_e, sic_log=sic, flags=flags) if raw_e else None
                hl_d, hl_e = fc_words(raw_d), fc_words(raw_e or "")
                words = shout["words"] if shout else []
                if allwords:
                    taught = [w["word"] for w in words]
                    taught_m = [w["meaning"] for w in words]
                    widx = None
                else:
                    w = next((w for w in words if w["position"] == i), None)
                    taught = [w["word"]] if w else []
                    taught_m = [w["meaning"]] if w else []
                    widx = i
                locs = []
                for loc in (shout["locations"] if shout else []):
                    if not re.search(r"\b(Taught|taught|Learned|learned from)\b|^N/A$|^Unavailable$", loc) \
                            and loc not in locs:
                        locs.append(loc)
                if n_walls == 1 and not allwords and shout:
                    w1 = next((w for w in shout["words"] if w["position"] == i), None)
                    locs = [w1["location"]] if w1 and w1["location"] else locs
                if unused:
                    where = "No in-game location: the wiki lists this wall under \"%s\"" % head
                elif allwords and locs:
                    where = locs[0]
                else:
                    where = " / ".join(locs) if locs else None
                notes = []
                if not unused and not allwords and len(locs) > 1:
                    notes.append("Per Skyrim:Word Wall, which text a wall shows depends on how many "
                                 "words of the shout you already know, not on which of the listed "
                                 "locations you visit; this is the text shown when the wall teaches "
                                 "word %d." % i)
                if unused:
                    notes.append("Wiki section: \"%s\"." % head)
                for a, b in sic:
                    notes.append("sic: wiki keeps \"%s\" and notes the correction \"%s\"." % (a, b))
                notes.extend(sorted(flags))
                corpus.add(
                    "word_wall", page, where, dz, en, notes=" ".join(notes) or None,
                    base_id="ww-" + slug(page.subject),
                    shout=page.subject, teaches_word_index=widx,
                    teaches_words=taught, teaches_meanings=taught_m,
                    highlighted_dovahzul=hl_d, highlighted_english=hl_e,
                    in_game=not unused, game=shout["game"] if shout else "Skyrim",
                    spelling="wiki rune-case (upper case = one rune, lower-case pair = one two-letter rune)",
                    canon_status="canon",
                    translation_source="translation as given on the wiki page")


def parse_lore_word_walls(pages, corpus):
    page = pages.get("Lore:Word Walls")
    if not page:
        return
    in_known = False
    for level, head, body in sections(page.text):
        if level == 2:
            in_known = clean(head) == "Known Inscriptions"
            continue
        if not in_known or level != 3:
            continue
        for s, e in table_blocks(body):
            rows = parse_table(body[s:e])
            if len(rows) < 2 or len(rows[1]) < 3:
                continue
            raw_i, raw_t, raw_e = rows[1][0][1], rows[1][1][1], rows[1][2][1]
            insc = None
            for n, nd, pos, ts, te in template_calls(raw_i, {"dragonfont"}):
                insc = clean(decode_font(pos[0])) if pos else None
            sic, flags = [], set()
            translit = clean(raw_t, sic_log=sic, flags=flags)
            en = clean(raw_e, sic_log=sic, flags=flags)
            refs = re.findall(r"\{\{[Rr]ef\|name=([^|}]+)(\|group=UOL)?", raw_e)
            notes = []
            wall_text, other_column = translit, None
            if insc and norm(insc) != norm(translit):
                # The page's two columns disagree.  Take the one the shout page confirms:
                # the column that equals a {{WordWall}} inscription whose translation is
                # this row's translation.  (Before the verification pass of 2026-11-14 the
                # transliteration column was always taken, which paired this row's English
                # with the text of a different wall.)
                def confirmed(text):
                    return any(t["type"] == "word_wall" and t["source_page"].startswith("Skyrim:")
                               and norm(t["dovahzul"]) == norm(text)
                               and norm(t["english"] or "") == norm(en or "")
                               for t in corpus.texts)
                if confirmed(insc) and not confirmed(translit):
                    wall_text, other_column = insc, translit
                    notes.append("The wiki's rune inscription column and its transliteration column "
                                 "DIFFER for this wall. dovahzul is the inscription column, which "
                                 "agrees with the shout page's wall and with the translation given "
                                 "here. The transliteration column reads: " +
                                 translit.replace("\n", " / "))
                else:
                    notes.append("The wiki's rune inscription column and its transliteration column "
                                 "DIFFER for this wall. Inscription column reads: " +
                                 insc.replace("\n", " / "))
            if any(g for _, g in refs):
                notes.append("The wiki cites this to its 'UOL' reference group (unused game-file "
                             "content / unofficial lore).")
            if "intnote" in raw_e:
                notes.append("See the wiki's note 1 on the Throw Voice walls: the separate Zul, Mey "
                             "and Gut walls exist only in the game files.")
            notes.extend(sorted(flags))
            corpus.add("word_wall", page, "Lore:Word Walls, inscription \"%s\"" % clean(head),
                       wall_text, en, notes=" ".join(notes) or None,
                       base_id="wwlore-" + slug(clean(head)),
                       wall_word=clean(head), inscription_column=insc,
                       transliteration_column=other_column,
                       wiki_refs=[r for r, _ in refs],
                       spelling="wiki rune-case (upper case = one rune, lower-case pair = one two-letter rune)",
                       canon_status="canon",
                       translation_source="translation as given on the wiki page")


def parse_lore_place_word_walls(pages, corpus):
    """Lore place pages that quote one word wall in a "Word Wall's translation" box.

    Added by the verification pass of 2026-11-14 (Lore:Vundeheim, Lore:Korvag Crag).
    The box holds the English; the {{DragonFont}} call after it holds the wall text.
    These walls are already recorded from the shout pages, so mark_duplicates links them.
    """
    for page in pages.values():
        if page.ns != "Lore" or page.title == "Lore:Word Walls" or \
                "Word Wall's translation" not in page.text:
            continue
        english = wall = None
        for name, named, pos, s0, e0 in template_calls(page.text, {"quote box", "dragonfont"}):
            if name == "quote box" and len(pos) >= 2 and "Word Wall's translation" in pos[1]:
                english = clean(pos[0])
            elif name == "dragonfont" and english and wall is None and pos:
                wall = clean(decode_font(pos[0]))
        if not (english and wall):
            continue
        corpus.add("word_wall", page, "%s, box \"Word Wall's translation\"" % page.title,
                   wall, english,
                   notes="A lore page about the place this wall names; it quotes the wall and its "
                         "translation and cites the shout page for both.",
                   base_id="wwplace-" + slug(page.name),
                   spelling="wiki rune-case (upper case = one rune, lower-case pair = one two-letter rune)",
                   canon_status="canon",
                   translation_source="translation as given on the wiki page")


# ---------------------------------------------------------------------------
# c. Alphabet
# ---------------------------------------------------------------------------
def parse_alphabet(pages):
    page = pages.get("Lore:Dragon Alphabet")
    runes, statements, examples = [], [], []
    if not page:
        return None
    text = page.text
    lead = text.split("{|", 1)[0]
    for para in lead.split("\n"):
        c = clean(para, keep_newlines=False)
        if c:
            statements.append(OrderedDict([
                ("statement", c), ("source_page", page.title), ("revid", page.revid),
                ("wiki_source_note",
                 "The wiki cites this to Game Informer, 'Skyrim's Dragon Shouts', 20 January 2011, "
                 "in its 'UOL' reference group." if "talons" in c else
                 ("The wiki cites the in-game book Dragon Language: Myth no More for the first "
                  "two sentences." if "Word Walls" in c else None))]))
    blocks = table_blocks(text)
    order = 0
    for s, e in blocks:
        rows = parse_table(text[s:e])
        head = heading_before(text, s)
        if head:
            continue                      # example tables are handled below
        i = 0
        while i + 1 < len(rows):
            hdr, vals = rows[i], rows[i + 1]
            if all(h for h, _ in hdr) and len(hdr) == len(vals) and \
                    all("dragonfont" in v.lower() for _, v in vals):
                for (h, latin), (_, cell) in zip(hdr, vals):
                    latin = clean(latin)
                    code = None
                    for n, nd, pos, ts, te in template_calls(cell, {"dragonfont"}):
                        code = pos[0].strip() if pos else None
                    order += 1
                    lat = latin.strip('"')
                    if lat == "C":
                        kind = "not used by the language (wiki: 'the letter is unused in the Dragon Language')"
                    elif lat == "0":
                        kind = "font-only glyph (wiki: 'goes unused as there is no associated letter')"
                    elif len(lat) == 2:
                        kind = "two-letter rune"
                    else:
                        kind = "single-letter rune"
                    runes.append(OrderedDict([
                        ("order_on_wiki", order),
                        ("latin", lat),
                        ("kind", kind),
                        ("dragonfont_template_code", code),
                        ("wiki_spelling_in_transcriptions",
                         lat.lower() if len(lat) == 2 else (lat if lat not in ("0",) else None)),
                        ("in_main_alphabet_table", lat not in ("C", "0")),
                        ("shape_description", None),
                        ("glyph_source",
                         "The wiki shows the glyph only by rendering the code above in its "
                         "DragonscriptRegular web font; it gives no per-rune description."),
                        ("source_page", page.title), ("revid", page.revid),
                    ]))
                i += 2
            else:
                i += 1
    for para in text.split("\n"):
        c = clean(para, keep_newlines=False)
        if c.startswith('The letter "C"') or c.startswith('The character "0"') or \
                c.startswith("This is the only instance"):
            statements.append(OrderedDict([("statement", c), ("source_page", page.title),
                                           ("revid", page.revid), ("wiki_source_note", None)]))
    # English written in dragon runes (not Dragon Language): kept here, not in the corpus
    for s, e in blocks:
        if heading_before(text, s) != "Legends Card Packs":
            continue
        for row in parse_table(text[s:e])[1:]:
            if len(row) >= 2:
                code = None
                for n, nd, pos, ts, te in template_calls(row[0][1], {"dragonfont"}):
                    code = clean(decode_font(pos[0])) if pos else None
                examples.append(OrderedDict([
                    ("runes_as_written", code), ("latin_reading_on_wiki", clean(row[1][1])),
                    ("language", "English written in dragon runes (not Dragon Language)"),
                    ("where", "Heroes of Skyrim Legendary card packs, The Elder Scrolls: Legends"),
                    ("source_page", page.title), ("revid", page.revid)]))
    font = OrderedDict()
    doc = pages.get("Template:DragonFont/Doc")
    if doc:
        m = re.search(r"<pre[^>]*>(.*?)</pre>", doc.text, flags=re.S)
        mapping = OrderedDict()
        if m:
            for line in m.group(1).strip().split("\n"):
                a, _, b = line.partition("=")
                if b:
                    mapping[a.strip()] = b.strip()
        font = OrderedDict([
            ("template", "Template:DragonFont"),
            ("digit_codes", mapping),
            ("usage_note", clean(re.search(r"\|1\|required\|(.*?)<pre", doc.text, flags=re.S).group(1),
                                 keep_newlines=False)
             if re.search(r"\|1\|required\|(.*?)<pre", doc.text, flags=re.S) else None),
            ("font_family_in_template", "DragonscriptRegular"),
            ("source_page", doc.title), ("revid", doc.revid)])
    extra = []
    pf = pages.get("Skyrim:Phantom Form")
    if pf:
        for line in pf.text.split("\n"):
            if "single glyph" in line:
                extra.append(OrderedDict([("statement", clean(line.lstrip("* "), keep_newlines=False)),
                                          ("source_page", pf.title), ("revid", pf.revid),
                                          ("wiki_source_note", None)]))
    fonts = pages.get("General:Fonts")
    if fonts:
        for line in fonts.text.split("\n"):
            if "Dragon_script" in line and "File:" in line:
                extra.append(OrderedDict([
                    ("statement", "General:Fonts lists a font 'Dragon_script' as appearing in Skyrim "
                                  "(2011), used for the Dragon Language."),
                    ("source_page", fonts.title), ("revid", fonts.revid), ("wiki_source_note", None)]))
            if "DragonTES.zip" in line:
                extra.append(OrderedDict([
                    ("statement", clean(line.lstrip("* "), keep_newlines=False)),
                    ("source_page", fonts.title), ("revid", fonts.revid), ("wiki_source_note", None)]))
    gi = pages.get("General:Skyrim\u2019s Dragon Shouts")
    if gi:
        for para in gi.text.split("\n"):
            c = clean(para, keep_newlines=False)
            if re.search(r"talon|dewclaw|runic alphabet|written alphabet|upper and lower case|"
                         r"individual runes in the written", c) and not para.startswith("|"):
                extra.append(OrderedDict([
                    ("statement", c), ("source_page", gi.title), ("revid", gi.revid),
                    ("wiki_source_note",
                     "Text of the Game Informer feature 'Skyrim\u2019s Dragon Shouts' (Matt Miller; "
                     "quotes Todd Howard and Emil Pagliarulo) as archived on the wiki. Developer "
                     "statements reported by the press: semi-canon.")]))
    return OrderedDict([("runes", runes), ("statements", statements + extra),
                        ("dragonfont_template", font),
                        ("non_language_uses_of_the_script", examples)])


# ---------------------------------------------------------------------------
# Tables of dragon text with a translation column
# ---------------------------------------------------------------------------
DZ_HEADS = ("latin alphabet", "dragon tongue", "the greybeards' chant")
EN_HEADS = ("translation", "translated", "direct translation")


def parse_translation_tables(pages, corpus):
    for page in pages.values():
        if page.title in ("Lore:Word Walls",):
            continue
        text = page.text
        for s, e in table_blocks(text):
            rows = parse_table(text[s:e])
            if not rows:
                continue
            heads = [clean(c[1]).lower() for c in rows[0] if c[0]]
            di = next((i for i, h in enumerate(heads) if h in DZ_HEADS), None)
            ei = next((i for i, h in enumerate(heads) if h in EN_HEADS), None)
            if di is None or ei is None:
                continue
            head = heading_before(text, s)
            third = next((i for i, h in enumerate(heads) if h.startswith("according to")), None)
            dz_lines, en_lines, alt_lines = [], [], []
            for row in rows[1:]:
                cells = [c[1] for c in row]
                if len(cells) <= max(di, ei):
                    if len(cells) == 1:           # a spacer row = stanza break
                        dz_lines.append(""); en_lines.append("")
                    continue
                dz_lines.append(clean(cells[di]))
                en_lines.append(clean(cells[ei]))
                if third is not None and len(cells) > third:
                    alt_lines.append(clean(cells[third]))
            dz = "\n".join(dz_lines).strip()
            en = "\n".join(en_lines).strip()
            rune_case = bool(re.search(r"[A-Z]{2}", dz)) and bool(re.search(r"[A-Z](?:aa|ah|ei|ey|ii)|[a-z]{2}[A-Z]", dz))
            common = dict(table_heading=head, canon_status="canon",
                          spelling="wiki rune-case (upper case = one rune, lower-case pair = one "
                                   "two-letter rune)" if rune_case else "as written on the wiki")
            if page.title == "Lore:Dragon Alphabet" and head == "Song of the Dragonborn":
                corpus.add("song", page, "Song of the Dragonborn (the 'Dragon Poem' of the Game Informer "
                           "cover, January 2011)", dz, en,
                           notes="Two stanzas as first published; the wiki says they are part of the "
                                 "longer Song of the Dragonborn printed in the in-game book Songs of "
                                 "Skyrim. Blank line = the table's stanza break.",
                           base_id="song-dragon-poem",
                           translation_source="translation column of the wiki table", **common)
            elif page.title == "Lore:Dragon Alphabet" and head == "E3 Word Wall":
                corpus.add("word_wall", page, "Word wall shown at Bethesda's booth, E3 2011", dz, en,
                           notes="The wiki says the same text is on the collector's-edition dragon wall "
                                 "statue and is the first Word Wall for the shout Storm Call.",
                           base_id="ww-e3-2011",
                           translation_source="translation column of the wiki table", **common)
            elif "Dragonstone" in (head, page.subject) or head == "Dragonstone Text":
                corpus.add("other", page, "Inscription on the back of the Dragonstone (Bleak Falls Barrow)",
                           dz, en, base_id="inscription-dragonstone-" + slug(page.ns),
                           subtype="inscription",
                           translation_source="translation column of the wiki table", **common)
            elif "chant" in heads[di] or heads[di] == "dragon tongue":
                notes = ["The Greybeards' formal greeting to a Dragonborn (quest: The Horn of Jurgen "
                         "Windcaller)."]
                extra = {}
                if alt_lines:
                    extra["english_in_game"] = "\n".join(alt_lines)
                    notes.append("english = the wiki's 'Direct translation' column; english_in_game = "
                                 "the wiki's 'According to Arngeir' column (Arngeir's own rough "
                                 "translation in the game).")
                else:
                    notes.append("english = the wiki's 'Direct translation' column.")
                corpus.add("dialogue", page, "The Greybeards (Arngeir, Borri, Einarth, Wulfgar)",
                           dz, en, notes=" ".join(notes), base_id="dlg-greybeards-chant",
                           subtype="ceremony", gloss_source="wiki table column 'Direct translation'",
                           **common, **extra)
            else:
                corpus.add("other", page, head or page.title, dz, en,
                           base_id="table-" + slug(page.title),
                           translation_source="translation column of the wiki table", **common)


# ---------------------------------------------------------------------------
# d. Songs and books
# ---------------------------------------------------------------------------
def parse_song_books(pages, corpus):
    for title in ("Skyrim:Songs of Skyrim", "Lore:Songs of Skyrim: Revised"):
        page = pages.get(title)
        if not page:
            continue
        blocks = re.findall(r"<p align=\"center\">(.*?)</p>", page.text, flags=re.S)
        m_o = re.search(r"The original version\.\.\.\s*(?:<br>\s*)*<p align=\"center\">(.*?)</p>",
                        page.text, flags=re.S)
        m_t = re.search(r"And the translation\.\.\.\s*(?:<br>\s*)*<p align=\"center\">(.*?)</p>",
                        page.text, flags=re.S)
        if m_o:
            sic = []
            dz = "\n".join(l for l in clean(m_o.group(1), sic_log=sic).split("\n") if l.strip())
            en = "\n".join(l for l in clean(m_t.group(1)).split("\n") if l.strip()) if m_t else None
            book = "Songs of Skyrim" if title.startswith("Skyrim:") else "Songs of Skyrim: Revised"
            intro = re.search(r"\n([^\n]*ancient song[^\n]*)\n", page.text)
            corpus.add("song", page, "Song of the Dragonborn, as printed in the in-game book %s" % book,
                       dz, en,
                       notes=("Book's introduction: " + clean(intro.group(1), keep_newlines=False) + " "
                              if intro else "") +
                             "Text under 'The original version...'; english is the book's own text "
                             "under 'And the translation...'. Line n of one matches line n of the other.",
                       base_id="song-of-the-dragonborn-" + slug(book),
                       canon_status="canon", translation_source="in-source (the book gives it)",
                       spelling="as written on the wiki (the book's own Latin-letter text)")
    page = pages.get("Lore:Dragon Skull Parchment")
    if page:
        body = re.sub(r"\{\{Lore Book.*?\n\}\}", "", page.text, flags=re.S)
        body = body.replace("{{Book End}}", "")
        dz = "\n".join(l for l in clean(body).split("\n") if l.strip())
        m = re.search(r'roughly translates to "(.+?)"', page.text, flags=re.S)
        desc = re.search(r"\|description=(.*)", page.text)
        corpus.add("song", page, "Dragon Skull Parchment (book, The Elder Scrolls Online)", dz,
                   clean(m.group(1)) if m else None,
                   notes="Wiki description: " + (clean(desc.group(1)) if desc else "") +
                         ". english is the wiki's editorial text note on the page ('roughly "
                         "translates to'), which points to the Song of the Dragonborn; the ESO book "
                         "itself carries no translation.",
                   base_id="song-dragon-skull-parchment", canon_status="canon",
                   source_title="The Elder Scrolls Online",
                   translation_source="wiki text note quoting the Songs of Skyrim translation")
    page = pages.get("Lore:Songs")
    if page:
        for m in re.finditer(r"\{\{Showhide/Start\|([^|}]+)[^}]*\}\}(.*?)\{\{Showhide/End\}\}",
                             page.text, flags=re.S):
            name, body = clean(m.group(1)), m.group(2)
            lines = [clean(l.lstrip(":")) for l in body.split("\n")]
            dz_lines = [l for l in lines if l and looks_dragon_line(l)]
            if not dz_lines:
                continue
            corpus.add("song", page, "%s (song, as collected on Lore:Songs)" % name,
                       "\n".join(dz_lines), None,
                       notes="Only the dragon-language lines of the song are given here; the other "
                             "lines of this song on the wiki are English. The page gives no separate "
                             "translation next to these lines.",
                       base_id="song-" + slug(name), canon_status="canon",
                       context="\n".join(l for l in lines if l),
                       spelling="as written on the wiki")


SONG_WORDS = {"dovahkiin", "naal", "zin", "vahriin", "wah", "dein", "vokul", "mahfaeraak",
              "ahst", "vaal", "ahrk", "norok", "paal", "graan", "nust", "zindro", "zaan",
              "kogaan", "draal", "huzrah", "lingrah", "boziik", "reyliik", "suleyk", "krein",
              "morokei", "taazokaan", "sahrot", "thu'um", "hokoron", "komeyt", "prodah",
              "zeymah", "fundein", "kruziik", "vokun", "staadnau", "bahlok", "diivon",
              "nahlot", "keizaal", "saviik"}


def looks_dragon_line(line):
    toks = [t.lower() for t in tokens(line)]
    if len(toks) < 3:
        return False
    hits = sum(1 for t in toks if t in SONG_WORDS)
    return hits >= 2 and hits / len(toks) >= 0.3


def parse_myth_no_more(pages, corpus):
    page = pages.get("Lore:Dragon Language: Myth no More")
    if not page:
        return
    paras = [p for p in page.text.split("\n") if p.strip()]
    n = 0
    for i, para in enumerate(paras):
        calls = list(template_calls(para, {"dragonfont"}))
        if not calls or not para.strip().startswith("{{DragonFont"):
            continue
        raw_runes = calls[0][2][0]
        # the next non-connective paragraphs: transliteration, then translation
        following = [p for p in paras[i + 1:i + 6]]
        body = [p for p in following if not re.match(
            r"\s*(Assigning|Which|Translates)\b.*:\s*$", clean(p))]
        if len(body) < 2:
            continue
        sic = []
        translit, en = clean(body[0], sic_log=sic), clean(body[1], sic_log=sic)
        n += 1
        insc = decode_font(raw_runes)
        notes = ["Passage %d of the in-game book Dragon Language: Myth no More by Hela "
                 "Thrice-Versed. dovahzul = the book's Latin-letter line; rune_inscription = the "
                 "book's rune line as the wiki encodes it; english = the book's own 'Tamrielic' "
                 "translation." % n]
        a_words = [w.lower() for w in re.findall(r"[A-Za-z']+", insc)]
        b_words = [w.lower() for w in re.findall(r"[A-Za-z']+", translit)]
        if a_words != b_words:
            only_a = [w for w in a_words if w not in b_words]
            only_b = [w for w in b_words if w not in a_words]
            notes.append("The book's rune line and its Latin-letter line differ as transcribed on "
                         "the wiki: rune line only: %s; Latin line only: %s."
                         % (", ".join(only_a) or "-", ", ".join(only_b) or "-"))
        corpus.add("word_wall", page, "Word wall transcribed in the book Dragon Language: Myth no More "
                   "(no location given in the book)", translit, en, notes=" ".join(notes),
                   base_id="ww-myth-no-more", rune_inscription=insc,
                   dragonfont_code=raw_runes, canon_status="canon",
                   translation_source="in-source (the book gives it)",
                   spelling="as written on the wiki (the book's own Latin-letter text)")


def parse_flying_gods(pages, corpus):
    page = pages.get("Lore:Wisdom of the Flying Gods")
    if not page:
        return
    lines = page.text.split("\n")
    for i, line in enumerate(lines):
        m = re.match(r':"(.+?)"\s*$', line.strip())
        if not m or i + 1 >= len(lines) or not lines[i + 1].startswith(":"):
            continue
        dz = clean(m.group(1))
        en = clean(lines[i + 1].lstrip(":"))
        commentary = []
        for l in lines[i + 2:]:
            if "* * *" in l or l.startswith("{{"):
                break
            if l.strip():
                commentary.append(clean(l, keep_newlines=False))
        corpus.add("other", page, "Saying attributed to Dragons, recorded by Magnius Calussa in the "
                   "book Wisdom of the Flying Gods (ESO: Elsweyr)", dz, en,
                   notes="english is the in-book interpretation, which the author himself calls "
                         "imperfect ('my interpretation of what those Words mean, imperfect though "
                         "that interpretation may be'). Author's commentary: " + " ".join(commentary),
                   base_id="proverb-flying-gods", subtype="proverb", canon_status="canon",
                   source_title="The Elder Scrolls Online: Elsweyr", uncertain=True,
                   translation_source="in-source (the book gives it)")


# ---------------------------------------------------------------------------
# e. Dialogue
# ---------------------------------------------------------------------------
HOVER_BAD_GLOSS = re.compile(
    r"^(Base Damage|Health|Values?:|If the Imperial|Alternate dialogue|Shows if|Jawanan|"
    r"Fire Variant|Frost Variant|Shock Variant|Imperial |Gold Necklace|\(Base Damage)", re.I)


REJECTED_HOVERS = []


def valid_hover(gloss, text, lex=None):
    if not gloss or not text:
        return False
    if re.search(r"\d|§|\{\{|&times;|×", gloss + text):
        return False
    if HOVER_BAD_GLOSS.search(gloss.strip()):
        return False
    if len(tokens(text)) > 14 and re.search(r"\b(the|and|would|from)\b", text):
        return False
    if lex:
        words = re.findall(r"[^\W\d_]+(?:['\u2019][^\W\d_]+)*", text)
        cls = [classify(w, lex) for w in words]
        if not words or sum(1 for c in cls if c != "E") / len(words) < 0.5:
            REJECTED_HOVERS.append((gloss, text))
            return False
    return True


def mask_hovers(line, store, sic_log, flags, lex=None):
    """Replace language hovers by placeholders; other hovers by their shown text."""
    out, last = [], 0
    spans = []
    for name, nd, pos, s, e in template_calls(line, {"hover"}):
        if spans and s < spans[-1][1]:
            continue
        spans.append((s, e, pos))
    for s, e, pos in spans:
        out.append(line[last:s])
        gloss = clean(pos[0], sic_log=sic_log, flags=flags) if pos else ""
        text = clean(pos[1], sic_log=sic_log, flags=flags) if len(pos) > 1 else ""
        if valid_hover(gloss, text, lex):
            store.append((gloss, text.strip().strip('"')))
            out.append("%s%d%s" % (PH_OPEN, len(store) - 1, PH_CLOSE))
        else:
            out.append(pos[1] if len(pos) > 1 else "")
        last = e
    out.append(line[last:])
    return "".join(out)


def italic_spans(line):
    """-> list of (text, is_italic, is_bold) pieces of one line."""
    pieces, italic, bold = [], False, False
    for part in re.split(r"('{2,})", line):
        if re.fullmatch(r"'{2,}", part):
            n = len(part)
            if n == 2:
                italic = not italic
            elif n == 3:
                bold = not bold
            elif n == 4:
                pieces.append(("'", italic, bold)); bold = not bold
            else:
                italic, bold = not italic, not bold
                if n > 5:
                    pieces.append(("'" * (n - 5), italic, bold))
        elif part:
            pieces.append((part, italic, bold))
    return pieces


ENGLISH_COLLISIONS = set("""
a an am as at au be by do go h he hi i if in is it me my no of oh ok on or re so to um un up us we
ah ha fun gut lot mid sun son sin win lost rein jot sot for nor not den med nah dun
brit hon mal fen fey rot ruth grind mar aye hah han vex bah dah lo nu mu bo al du od nil
luv pal him key kip gram sod til tosh name online ref vol
dovah dov dovahkiin thu'um thuum sovngarde alduin paarthurnax odahviing durnehviir miraak
keizaal tamriel oblivion nirn akatosh kyne shor atmora mundus skyrim sahloknir mirmulnir
konahrik hela korthor
""".split())
SUFFIXES = ("aan", "ii", "i", "u")


def build_lexicon(pages, corpus):
    """Word list used only to spot un-glossed dragon words in English dialogue lines."""
    lex = set()
    dict_path = SRC_DIR / "Lore_Dragon_Language.wikitext"
    used_dictionary = False
    if dict_path.exists():
        for line in dict_path.read_text(encoding="utf-8").split("\n"):
            if not line.startswith(";"):
                continue
            head = strip_refs(line[1:]).split(":", 1)[0]
            head = clean(head)
            if not head or not re.fullmatch(r"[A-Za-z' ,/()\-.]+", head):
                continue
            for alt in re.split(r"\s*[/,]\s*", head):
                alt = alt.strip(" .")
                m = re.fullmatch(r"([A-Za-z'\-]+)\(([a-z]+)\)", alt)
                forms = [m.group(1), m.group(1) + m.group(2)] if m else [alt]
                for f in forms:
                    for t in tokens(f):
                        lex.add(t.lower())
                        used_dictionary = True
    for t in corpus.texts:
        if t["type"] in ("word_wall", "song", "shout") or t.get("subtype") in ("proverb", "ceremony"):
            for tok in tokens(t["dovahzul"]):
                lex.add(tok.lower())
    lex.discard("")
    return lex, used_dictionary


def is_dragon_word(tok, lex, depth=0):
    w = tok.lower().replace("\u2019", "'")
    if w in lex:
        return True
    if w in ENGLISH_COLLISIONS:
        return False
    for suf in SUFFIXES:                      # possessives and perfect: thur-i, thu'um-u, kri-aan
        if w.endswith(suf) and len(w) - len(suf) >= 3 and w[:-len(suf)] in lex \
                and w[:-len(suf)] not in ENGLISH_COLLISIONS:
            return True
    if len(w) >= 5 and w[-1] == "e" and w[-2] == w[-3] and w[:-2] in lex:
        return True                           # plural: joor -> joorre
    if len(w) >= 6:                           # compounds: sille+se+joor, dovah+kriid
        for i in range(3, len(w) - 2):
            a, b = w[:i], w[i:]
            if a in lex:
                if b in lex and len(b) >= 3:
                    return True
                if b.startswith("se") and len(b) >= 5 and b[2:] in lex:
                    return True
    return False


EN_STOP = set("""
the you your yours and are that not this will have with what for from they there when can was
were has had but all been would could should their them then than here which into more only
one now yes no i a of to is it be my me we he she her his by at as if or an am so on in do did
does how why where who whom our us its these those such very too also just even still never
ever again must may might shall let come go know see say said time like out about some any
many much before after over under while because though through than well good great mortal
mortals dragon dragons old new little long way thing things nothing something
greetings hail farewell rest speak die kill peace patience true false sorrow fire sky voice hear
listen look fight battle strong weak brother master lord king slave fool fools enough indeed
perhaps worthy enemy beautiful
""".split())
NAME_TOKENS = set()


# Words and phrases the word list cannot know, each checked by eye against the page at the
# snapshot revision (verification pass, 2026-11-14).  On that page only, the matcher takes
# them as dragon text; the record's notes name them.  Without them the matcher cut the
# phrase short ("Kfir voth ahkrin" -> "voth ahkrin") or missed the word.
REVIEWED_TEXT = {
    "Blades:Shulkunaak": {
        "kfir": "the page writes \"Kfir voth ahkrin\"; Blades:Facing the Dragon has the same "
                "line as \"Krif voth ahkrin\"",
    },
    "Online:Nahfahlaar": {
        "fez": "\"Vomindok fez\" is listed as a phrase on Lore:Dragon Language",
    },
    "Skyrim:Paarthurnax (dragon)": {
        "krongah": "the page's spelling; the dictionary page has Krongrah",
        "uznahgar": "the page's spelling; the dictionary page has Uznahgaar",
        "bruniike": "the page's spelling; the dictionary page has Bruniik(ke)",
        "dovah sos": "\"Dovah Sos\" is glossed 'dragonblood' on Skyrim:Dovahkiin",
    },
}


def _force_phrases(words, cls, phrases):
    """Mark every token of a hand-checked phrase as dragon text ("D")."""
    if not phrases:
        return cls
    low = [w.lower().replace("\u2019", "'") for w in words]
    for ph in phrases:
        k = len(ph)
        for i in range(len(low) - k + 1):
            if low[i:i + k] == list(ph):
                for j in range(i, i + k):
                    cls[j] = "D"
    return cls


def classify(word, lex, extra=()):
    w = word.lower().replace("\u2019", "'")
    if w in extra:
        return "D"
    if w in NAME_TOKENS:
        return "A"
    if w in ENGLISH_COLLISIONS:
        return "A" if w in lex else "E"
    return "D" if is_dragon_word(w, lex) else "E"


def _tidy_run(run):
    run = run.strip().strip('"\u201c\u201d').strip()
    run = re.sub(r'\s*"\s*', " ", run)
    return re.sub(r"\s+", " ", run).strip(" ,;:-/")


def _all_dragon(toks, cls):
    """True when a stretch of text reads as dragon language from end to end."""
    n, d = len(cls), cls.count("D")
    unknown = [t for t, c in zip(toks, cls) if c == "E"]
    if d == 0:
        return False
    if any(t.lower() in EN_STOP for t in unknown):
        return False
    if not unknown:
        return True
    return n >= 4 and d >= 2 and len(unknown) / n <= 0.4


def dragon_runs(text, lex, extra=(), phrases=()):
    """Dragon-language stretches inside a line that may be mostly English (heuristic).

    Words are matched against a word list.  A whole line or sentence is taken when
    it holds no English function word and nearly every word is on the list;
    otherwise only unbroken runs of listed words are taken.
    """
    if not lex or not text:
        return []
    words = [m.group(0) for m in WORD_RE.finditer(text)]
    cls = _force_phrases(words, [classify(w, lex, extra) for w in words], phrases)
    if "D" not in cls:
        return []
    if _all_dragon(words, cls):
        return [_tidy_run(text)]
    runs = []           # (text, whole_sentence)
    for sm in re.finditer(r"[^.!?\u2026]+(?:[.!?\u2026]+|$)", text):
        sent = sm.group(0)
        toks = list(WORD_RE.finditer(sent))
        if not toks:
            continue
        cl = _force_phrases([m.group(0) for m in toks],
                            [classify(m.group(0), lex, extra) for m in toks], phrases)
        if "D" not in cl:
            runs.append((None, False))
            continue
        if _all_dragon([m.group(0) for m in toks], cl):
            runs.append((sent.strip(), True))
            continue
        i = 0
        while i < len(cl):
            if cl[i] == "E":
                i += 1
                continue
            j = i
            while j + 1 < len(cl) and cl[j + 1] != "E" and \
                    re.fullmatch(r"[\s,'\u2019\-]*", sent[toks[j].end():toks[j + 1].start()]):
                j += 1
            lo, hi = i, j
            while lo <= hi and cl[lo] == "A":
                lo += 1
            while hi >= lo and cl[hi] == "A":
                hi -= 1
            if lo <= hi:
                runs.append((sent[toks[lo].start():toks[hi].end()], False))
            i = j + 1
        runs.append((None, False))
    out, prev_whole = [], False
    for run, whole in runs:
        if run is None:
            prev_whole = False
            continue
        if whole and prev_whole and out:
            out[-1] = out[-1] + " " + _tidy_run(run)
        else:
            out.append(_tidy_run(run))
        prev_whole = whole
    return [r for r in out if r]


KNOWN_SPEAKERS = []


SPEECH_VERBS = (r"(?:say|says|said|saying|reply|replies|replying|respond|responds|responding|"
                r"shout|shouts|shouting|speak|speaks|speaking|add|adds|adding|exclaim|exclaims|"
                r"exclaiming|greet|greets|greeting|ask|asks|asking|interject|interjects|continue|"
                r"continues|declare|declares|declaring|taunt|taunts|taunting|tell|tells|telling|"
                r"yell|yells|remark|remarks|answer|answers|announce|announces|state|states|stating|"
                r"urge|urges|encourage|encourages|explain|explains|explaining|comment|comments|"
                r"address|addresses|addressing|interfere|interrupt|interrupts|mutter|mutters|"
                r"hail|hails|hailing|utter|utters|proclaim|proclaims)")


def speaker_from_narration(gap, before, default):
    frag = re.split(r"(?<=[.!?])\s+|\n", gap[-400:])[-1]
    best, pos = None, len(frag) + 1
    for name in KNOWN_SPEAKERS:
        m = re.search(r"\b%s\b(?:'s voice)?[^.!?]{0,160}?\b%s\b" % (re.escape(name), SPEECH_VERBS),
                      frag)
        if m and m.start() < pos:
            best, pos = name, m.start()
    if best:
        return best, "narration on the page (first name in the clause before the quote that " \
                     "is followed by a verb of speaking)"
    if default:
        return default, "page subject"
    last, lpos = None, -1
    for name in KNOWN_SPEAKERS:
        for m in re.finditer(r"\b%s\b" % re.escape(name), before[-700:]):
            if m.start() > lpos:
                last, lpos = name, m.start()
    if last and re.search(r"\b(he|she|his|her|him)\b", gap[-200:], flags=re.I):
        return last, "narration on the page (pronoun; the last character named earlier in the " \
                     "paragraph) - uncertain"
    return None, "unattributed on the page"


NPC_NS = ("Skyrim", "Online", "Blades", "Legends")
QUEST_PAGES = {
    "Skyrim:Unbound", "Skyrim:Dragon Rising", "Skyrim:The Way of the Voice",
    "Skyrim:The Horn of Jurgen Windcaller", "Skyrim:A Blade in the Dark",
    "Skyrim:The Throat of the World", "Skyrim:Alduin's Bane", "Skyrim:Season Unending",
    "Skyrim:The Fallen", "Skyrim:The World-Eater's Eyrie", "Skyrim:Sovngarde (quest)",
    "Skyrim:Dragonslayer", "Skyrim:Paarthurnax (quest)", "Skyrim:Beyond Death",
    "Skyrim:Durnehviir (quest)", "Skyrim:The Temple of Miraak",
    "Skyrim:At the Summit of Apocrypha", "Skyrim:The Staff of Magnus",
    "Skyrim:Volskygge (quest)", "Skyrim:Easter Eggs", "Skyrim:Unobtainable Items",
    "Skyrim:Anniversary Edition", "Skyrim:Dragon Riding", "Skyrim:High Hrothgar",
    "Skyrim:Dovahkiin", "Skyrim:Dragon", "Skyrim:Draugr", "Skyrim:Dragon Priest",
    "Skyrim:Greybeards", "Skyrim:Loading Screens", "Skyrim:Music", "Skyrim:Bards College",
    "Skyrim:Kinect Commands", "Skyrim:The Words of Power", "Skyrim:Dragonstone",
    "Skyrim:Word Wall", "Skyrim:Dragon Shouts", "Skyrim:Konahrik", "Skyrim:Krosis",
    "Skyrim:Bromjunaar Sanctuary",
    "Online:The Dragon's Lair", "Online:Dragonhold", "Online:Dragon", "Online:The Dragon",
    "Online:Elder Scrolls Historical References", "Online:Dovah's Du'ul Style",
    "Online:Lendoran Ruin", "Blades:Facing the Dragon", "Blades:Dragon",
}
PAGE_DEFAULT_SPEAKER = {
    # quest pages whose un-labelled dragon lines all belong to one speaker (checked by hand)
    "Blades:Facing the Dragon": "Shulkunaak",
    "Skyrim:Draugr": "Draugr (combat lines)",
    "Skyrim:Dragon Riding": "Tamed dragon (Dragonborn add-on, dragon riding)",
    "Skyrim:Dragonslayer": "Dragons gathered on the Throat of the World after Alduin's defeat",
}
SOURCE_TITLE = {"Skyrim": "The Elder Scrolls V: Skyrim", "Online": "The Elder Scrolls Online",
                "Blades": "The Elder Scrolls: Blades", "Legends": "The Elder Scrolls: Legends"}


def parse_dialogue(pages, corpus, lex):
    ceremony = " ".join(norm(t["dovahzul"]) for t in corpus.texts if t.get("subtype") == "ceremony")
    raw_entries = []
    for page in pages.values():
        if page.ns not in NPC_NS:
            continue
        if page.ns == "Legends":
            continue                          # card audio lines are read by parse_legends_audio
        if page.title in ("Skyrim:Dragon Shouts",) or \
                any(True for _ in template_calls(page.text, {"shout summary"})):
            continue
        if any(True for _ in template_calls(page.text, {"game book"})):
            continue
        is_npc = bool(re.search(r"\{\{\s*(?:Online |Basic |Blades )?(?:NPC|Creature) Summary",
                                page.text, flags=re.I))
        is_quest = page.title in QUEST_PAGES or not is_npc
        default = PAGE_DEFAULT_SPEAKER.get(page.title) or (None if is_quest else page.subject)
        text = strip_refs(strip_comments(page.text))
        for _ in range(3):                    # image captions are not dialogue
            text = re.sub(r"\[\[(?:File|Image):(?:[^\[\]]|\[\[[^\[\]]*\]\])*\]\]", "", text,
                          flags=re.I)
        text = re.sub(r"<gallery.*?</gallery>", "", text, flags=re.S | re.I)
        text = lift_chants(page, text, default, raw_entries)
        text = lift_bullet_pairs(page, text, raw_entries, lex)
        for line in text.split("\n"):
            if "''" not in line and "hover" not in line.lower():
                continue
            store, sic, flags = [], [], set()
            masked = mask_hovers(line, store, sic, flags, lex)
            if not store and not lex:
                continue
            # walk the line: plain italics = speech, bold = speaker label or player line
            utts, cur, before, label, pending, gap = [], None, "", None, None, ""
            for txt, it, bd in italic_spans(masked):
                if it and (not bd or cur is not None):
                    if cur is None:
                        cur = {"text": "", "before": before, "label": label, "gap": gap}
                    cur["text"] += txt
                    continue
                if it and bd:                 # the player's own line
                    label = pending = None
                    continue
                if cur is not None:
                    utts.append(cur)
                    cur, label, gap = None, None, ""
                if bd:
                    lab = clean(txt).strip()
                    at_start = clean(gap).strip(" :*#|\n") == ""
                    if lab.endswith(":") and at_start:
                        label, pending = lab[:-1].strip(), None
                    else:
                        label, pending = None, (lab if at_start else None)
                else:
                    if pending is not None:
                        label = pending if re.match(r"\s*(?:\([^)]*\))?\s*:", txt) else None
                        pending = None
                    elif clean(txt).strip(' :"') != "":
                        label = None
                    before += txt
                gap += txt
            if cur is not None:
                utts.append(cur)
            for k, u in enumerate(utts):
                after = utts[k + 1]["gap"] if k + 1 < len(utts) else gap if cur is None else ""
                m_par = re.match(r"\s*\(([^()]{3,160})\)", clean(after))
                if m_par and PH_OPEN not in u["text"]:
                    u["inline_gloss"] = m_par.group(1).strip()
                    u["inline_kind"] = "wiki's own translation in parentheses after the quote"
            for k in range(1, len(utts)):
                if re.fullmatch(r"\s*,?\s*meaning,?\s*", clean(utts[k]["gap"])) and \
                        PH_OPEN not in utts[k]["text"]:
                    utts[k - 1]["inline_gloss"] = clean(utts[k]["text"]).strip().strip('"')
                    utts[k]["skip"] = True
            utts = [u for u in utts if not u.get("skip")]
            prev = None                       # a list of quotes shares the speaker of its first
            for u in utts:
                if u.get("label"):
                    u["speaker"], u["basis"] = u["label"], "label"
                elif prev and re.fullmatch(r"[\s,;]*(?:or|and)?[\s,;]*", clean(u["gap"])):
                    u["speaker"], u["basis"] = prev
                else:
                    u["speaker"], u["basis"] = speaker_from_narration(
                        clean(u["gap"]), clean(u["before"]), default)
                prev = (u["speaker"], u["basis"])
            seen_ph = set()
            for u in utts:
                u["quoted"] = bool(re.match(r'\s*["\u201c]', u["text"])) or \
                    page.ns == "Blades" or bool(u.get("label"))
                ph = [int(x) for x in re.findall(PH_OPEN + r"(\d+)" + PH_CLOSE, u["text"])]
                seen_ph.update(ph)
                raw_entries.extend(build_utterance(page, u, store, sic, flags, lex, default,
                                                   is_quest, ceremony=ceremony))
            # hovers that stand outside any italic span
            for m in re.finditer(PH_OPEN + r"(\d+)" + PH_CLOSE, masked):
                idx = int(m.group(1))
                if idx in seen_ph:
                    continue
                a0 = max(masked.rfind(". ", 0, m.start()) + 2, 0)
                b0 = masked.find(". ", m.end())
                sent = masked[a0:b0 + 1 if b0 != -1 else len(masked)]
                u = {"text": sent, "before": masked[:m.start()], "label": None, "prose": True}
                raw_entries.extend(build_utterance(page, u, store, sic, flags, lex, default,
                                                   is_quest, only=[idx], ceremony=ceremony))

    def compatible(x, y):
        return x["speaker"] == y["speaker"] or x["speaker"] is None or y["speaker"] is None

    def absorb(target, e):
        if e["speaker"] and (target["speaker"] is None or
                             (target["basis"] != "label" and e["basis"] == "label")):
            target["speaker"], target["basis"] = e["speaker"], e["basis"]
        for ref in ["%s (rev %d)" % (e["page"].title, e["page"].revid)] + e["also_on"]:
            if not ref.startswith(target["page"].title + " (rev") and ref not in target["also_on"]:
                target["also_on"].append(ref)

    def rank(e):
        return (-sum(1 for sg in e["segments"] if sg["english"]),
                e["page"].subject != e["speaker"], e["page"].title in QUEST_PAGES)

    # 1. the same line (same full context) quoted on several pages
    merged, by_ctx = [], {}
    for e in sorted(raw_entries, key=rank):
        key = norm(e["context"])
        hit = next((c for c in by_ctx.get(key, []) if compatible(c, e)), None) if key else None
        if hit is not None:
            absorb(hit, e)
        else:
            by_ctx.setdefault(key, []).append(e)
            merged.append(e)
    # 2. the same dragon text with the same gloss
    out, by_text = [], {}
    for e in merged:
        key = (norm(e["dovahzul"]), norm(e["english"] or ""))
        hit = next((c for c in by_text.get(key, []) if compatible(c, e)), None)
        if hit is not None:
            absorb(hit, e)
        else:
            by_text.setdefault(key, []).append(e)
            out.append(e)
    # 3. un-glossed repeats of segments that another page glosses for the same speaker
    glossed_index = {}
    for e in out:
        for sg in e["segments"]:
            if sg["english"]:
                glossed_index.setdefault(norm(sg["dovahzul"]), []).append(e)
    final = []
    for e in out:
        if e["glossed"]:
            final.append(e)
            continue
        hits = []
        for sg in e["segments"]:
            cands = [c for c in glossed_index.get(norm(sg["dovahzul"]), [])
                     if c["speaker"] and c["speaker"] == e["speaker"] and c["page"] is not e["page"]]
            hits.append(cands[0] if cands else None)
        if hits and all(h is not None for h in hits):
            for h in hits:
                absorb(h, e)
        else:
            final.append(e)
    order = {id(e): i for i, e in enumerate(raw_entries)}
    final.sort(key=lambda e: order[id(e)])
    for e in final:
        page = e["page"]
        notes = []
        if e["basis"] != "label":
            notes.append("Speaker from: %s." % e["basis"])
        if e["glossed"]:
            notes.append("english = the wiki editors' gloss (hover text or running text), not "
                         "in-game text.")
        if e["unglossed"]:
            notes.append("Segments marked 'none on the wiki' were picked out by word-list match "
                         "(heuristic); the wiki gives no separate gloss for them, though the "
                         "speaker often restates the meaning in English in the same line (see context).")
        for a1, b1 in e["sic"]:
            notes.append("sic: wiki keeps \"%s\" and notes the correction \"%s\"." % (a1, b1))
        for w, why in e.get("reviewed", []):
            notes.append("Checked by hand against the page: \"%s\" is not on the word list and "
                         "was taken as dragon text (%s)." % (w, why))
        notes.extend(sorted(e["flags"]))
        corpus.add("dialogue", page, e["speaker"] or "unattributed (%s)" % page.title,
                   e["dovahzul"], e["english"], notes=" ".join(notes) or None,
                   base_id="dlg-" + slug(page.title),
                   context=e["context"], segments=e["segments"],
                   also_on=e["also_on"], canon_status="canon",
                   source_title=SOURCE_TITLE.get(page.ns),
                   subtype=e.get("subtype"),
                   gloss_source=gloss_source_of(e["segments"]),
                   uncertain=True if e["flags"] else None)


def gloss_source_of(segs):
    kinds = []
    for sg in segs:
        k = sg["gloss"] if sg["english"] else None
        if k and k not in kinds:
            kinds.append(k)
    if not kinds:
        return "none on the wiki"
    out = "; ".join(kinds)
    if any(sg["english"] is None for sg in segs):
        out += " (for some segments; none for the rest)"
    return out


def lift_bullet_pairs(page, text, raw_entries, lex):
    """'*Speaker: (italic dragon line)' with a '**translation' line under it."""
    lines = text.split("\n")
    out, i = [], 0
    pat = re.compile(r"\*\s*(?:''')?([A-Z][\w' \-]{1,30}?)(?:''')?:\s*''(.+?)''\s*$")
    while i < len(lines):
        m = pat.match(lines[i])
        if m and i + 1 < len(lines) and lines[i + 1].startswith("**"):
            dz = clean(m.group(2)).strip().strip('"').strip()
            runs = dragon_runs(dz, lex)
            if len(runs) == 1 and norm(runs[0]) == norm(dz):
                en = clean(lines[i + 1].lstrip("* ")).strip()
                if en.startswith("(") and en.endswith(")") and en.count("(") == 1:
                    en = en[1:-1]
                kind = "wiki's translation line under the quote"
                seg = OrderedDict([("dovahzul", dz), ("english", en), ("gloss", kind)])
                raw_entries.append({
                    "page": page, "speaker": m.group(1).strip(), "basis": "label",
                    "dovahzul": dz, "english": en, "segments": [seg], "context": dz,
                    "glossed": True, "unglossed": False, "segments_glossed": True,
                    "sic": [], "flags": set(), "also_on": [], "subtype": "line_with_translation"})
                i += 2
                continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def lift_chants(page, text, default, raw_entries):
    """A run of bullet lines, each one italic line, most of them hover-glossed = one chant."""
    lines = text.split("\n")
    out, i = [], 0
    pat = re.compile(r"\*\s*''(.+?)''\s*$")
    while i < len(lines):
        j = i
        block = []
        while j < len(lines) and (pat.match(lines[j]) or (block and not lines[j].strip())):
            if lines[j].strip():
                block.append(pat.match(lines[j]).group(1))
            j += 1
        hov = [b for b in block if re.match(r"\{\{[Hh]over\|", b)]
        if len(block) >= 4 and len(hov) >= len(block) / 2:
            known, segs = {}, []
            for b in block:
                calls = list(template_calls(b, {"hover"}))
                if calls and len(calls[0][2]) > 1:
                    gl, dz = clean(calls[0][2][0]), clean(calls[0][2][1])
                    known[norm(dz)] = gl
                    segs.append(OrderedDict([("dovahzul", dz), ("english", gl),
                                             ("gloss", "wiki hover gloss")]))
                else:
                    dz = clean(b)
                    gl = known.get(norm(dz))
                    segs.append(OrderedDict([
                        ("dovahzul", dz), ("english", gl),
                        ("gloss", "wiki hover gloss given on the first occurrence of this refrain"
                         if gl else "none on the wiki")]))
            raw_entries.append({
                "page": page, "speaker": default, "basis": "page subject" if default else
                "unattributed on the page",
                "dovahzul": "\n".join(sg["dovahzul"] for sg in segs),
                "english": "\n".join(sg["english"] or "[no gloss on the wiki]" for sg in segs),
                "segments": segs, "context": "\n".join(sg["dovahzul"] for sg in segs),
                "glossed": True, "unglossed": any(sg["english"] is None for sg in segs),
                "segments_glossed": True, "sic": [], "flags": set(), "also_on": [],
                "subtype": "chant"})
            i = j
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def build_utterance(page, u, store, sic, flags, lex, default, is_quest, only=None,
                    ceremony=""):
    raw = u["text"]
    parts = re.split("(" + PH_OPEN + r"\d+" + PH_CLOSE + ")", raw)
    segs = []            # (kind, dovahzul, english)
    context = []
    # merge neighbouring hovers
    i = 0
    items = []
    for p in parts:
        m = re.fullmatch(PH_OPEN + r"(\d+)" + PH_CLOSE, p)
        if m:
            idx = int(m.group(1))
            if only is not None and idx not in only:
                items.append(("t", clean(store[idx][1])))
            else:
                items.append(("h", idx))
        else:
            items.append(("t", p))
    k = 0
    merged = []
    while k < len(items):
        kind, val = items[k]
        if kind == "h":
            dz, gl = [store[val][1]], [store[val][0]]
            j = k + 1
            while j + 1 < len(items) and items[j][0] == "t" and items[j + 1][0] == "h":
                between = clean(items[j][1])
                nxt = store[items[j + 1][1]]
                same = nxt[0] == store[val][0] and len(tokens(between)) <= 3 and \
                    not re.search(r"[.!?]", between)
                if between.strip() == "" or same:
                    if between.strip():
                        dz.append(between.strip())
                    dz.append(nxt[1])
                    if not same:
                        gl.append(nxt[0])
                    j += 2
                else:
                    break
            merged.append(("h", " ".join(dz), " ".join(gl)))
            k = j
        else:
            merged.append(("t", val, None))
            k += 1
    glossed = unglossed = False
    reviewed = []        # hand-checked words (REVIEWED_TEXT) that ended up in a segment
    for kind, a, b in merged:
        if kind == "h":
            segs.append(OrderedDict([("dovahzul", a), ("english", b), ("gloss", "wiki hover gloss")]))
            context.append(a)
            glossed = True
        else:
            c = clean(a, sic_log=sic, flags=flags)
            context.append(c)
            if u.get("prose"):
                continue
            extra = {a.lower() for a, b in sic
                     if b.lower() not in ENGLISH_COLLISIONS and is_dragon_word(b, lex)}
            checked = REVIEWED_TEXT.get(page.title, {})
            extra |= {w for w in checked if " " not in w}
            runs = dragon_runs(c, lex, extra,
                               phrases=[tuple(w.split()) for w in checked if " " in w])
            if not u.get("quoted"):
                # italics without quote marks or a speaker label are usually not speech:
                # keep them only when the whole span is dragon language (two words or more)
                if not (len(runs) == 1 and norm(runs[0]) == norm(c) and len(tokens(c)) >= 2):
                    continue
            for run in runs:
                if ceremony and norm(run) and norm(run) in ceremony:
                    continue                  # the Greybeards' chant is read from its table
                segs.append(OrderedDict([("dovahzul", run), ("english", None),
                                         ("gloss", "none on the wiki (word-list match)")]))
                unglossed = True
                for w, why in sorted(checked.items()):
                    if (" " + w + " ") in (" " + norm(run) + " ") and (w, why) not in reviewed:
                        reviewed.append((w, why))
    if not segs:
        return []
    if u.get("inline_gloss") and len(segs) == 1 and segs[0]["english"] is None and \
            norm(segs[0]["dovahzul"]) == norm(" ".join(x for x in context if x)):
        segs[0]["english"] = u["inline_gloss"]
        segs[0]["gloss"] = u.get("inline_kind") or \
            "wiki's own translation in the running text ('meaning, ...')"
        glossed, unglossed = True, False
    ctx = re.sub(r"\s+([.,!?])", r"\1", " ".join(x for x in context if x))
    ctx = re.sub(r"[ \t]+", " ", ctx).strip().strip('"').strip()
    if "speaker" in u:
        speaker, basis = u["speaker"], u["basis"]
    else:
        speaker, basis = speaker_from_narration(clean(u.get("gap") or u["before"]),
                                                clean(u["before"]), default)
    return [{
        "page": page, "speaker": speaker, "basis": basis,
        "dovahzul": "\n".join(s["dovahzul"] for s in segs),
        "english": "\n".join(s["english"] if s["english"] else "[no gloss on the wiki]"
                             for s in segs) if glossed else None,
        "segments": segs, "context": ctx, "glossed": glossed, "unglossed": unglossed,
        "segments_glossed": glossed, "sic": list(sic), "flags": set(flags), "also_on": [],
        "reviewed": reviewed,
    }]


# ---------------------------------------------------------------------------
# Single passages that need their own pattern (each checked against the page)
# ---------------------------------------------------------------------------
def parse_special(pages, corpus):
    page = pages.get("Skyrim:Anniversary Edition")
    if page:
        m = re.search(r"\*The cover features text written in the[^\n]*It reads:\n((?:\*\*[^\n]*\n)+)",
                      page.text)
        if m:
            dz, en = [], []
            for line in m.group(1).strip().split("\n"):
                mm = re.match(r"\*\*\s*(.+?)\s*\((.+)\)\s*$", clean(line))
                if mm:
                    dz.append(mm.group(1))
                    en.append(mm.group(2))
            corpus.add("other", page, "Cover of Skyrim Anniversary Edition", "\n".join(dz),
                       "\n".join(en),
                       notes="The wiki's note: 'The cover features text written in the Dragon "
                             "Language. It reads:' followed by these lines, each with its English "
                             "in parentheses. Spelling as on the wiki (e.g. 'Thuum' without "
                             "apostrophe).",
                       base_id="inscription-anniversary-edition-cover", subtype="inscription",
                       canon_status="canon (official packaging); the English is the wiki's",
                       translation_source="parentheses after each line on the wiki page")
    page = pages.get("Skyrim:High Hrothgar")
    if page:
        for line in page.text.split("\n"):
            if '"LOK BO"' in line and '"THUUM TUUM"' in line:
                note = clean(line.lstrip("* "), keep_newlines=False)
                for phrase in ("LOK BO", "THUUM TUUM"):
                    corpus.add("other", page, "Banners inside High Hrothgar", phrase, None,
                               notes="No translation on the wiki, which says it cannot be "
                                     "translated completely. Wiki note: " + note,
                               base_id="inscription-high-hrothgar-banner", subtype="inscription",
                               uncertain=True, canon_status="canon (in-game banner text)")
    page = pages.get("Lore:Way of the Voice")
    if page:
        m = re.search(r"motto of the Dragon tongue: ([^\"]+?) \"([^\"]+)\"", clean(page.text))
        if m:
            corpus.add("other", page, "Motto of the Way of the Voice (the wiki cites Arngeir's dialogue)",
                       m.group(1).strip(), m.group(2),
                       notes="Wiki sentence: This philosophy is exemplified in a motto of the "
                             "Dragon tongue: %s \"%s\"." % (m.group(1).strip(), m.group(2)),
                       base_id="motto-way-of-the-voice", subtype="motto", canon_status="canon",
                       translation_source="quoted on the wiki page next to the motto")
    page = pages.get("Merchandise:Thu'um Master Blazer")
    if page:
        m = re.search(r'embroidered with dragon language reading, "([^"]+)"', clean(page.text))
        if m:
            corpus.add("other", page, "Sleeve cuffs of the Thu'um Master Blazer (BlackMilk Clothing, 2026)",
                       m.group(1), None,
                       notes="Official merchandise text as quoted from the product listing on the "
                             "wiki; the listing gives no translation beside it. It is the first "
                             "line of the Song of the Dragonborn.",
                       base_id="merchandise-thu-um-master-blazer", subtype="merchandise_text",
                       canon_status="official merchandise")
    for page in pages.values():
        if not page.title.startswith("General:Saltatio Mortis"):
            continue
        blocks, cur = [], []
        for line in page.text.split("\n"):
            calls = list(template_calls(line, {"hover"}))
            if calls and len(calls[0][2]) > 1:
                cur.append((clean(calls[0][2][1]), clean(calls[0][2][0])))
            elif not line.strip() and cur:
                cur.append(("", ""))
            elif cur:
                blocks.append(cur)
                cur = []
        if cur:
            blocks.append(cur)
        if blocks:
            first = blocks[0]
            while first and first[-1] == ("", ""):
                first.pop()
            same = sum(1 for b in blocks if [x for x in b if x[0]] == [x for x in first if x[0]])
            corpus.add("song", page, "Dragon-language refrain of \"Pray to the Hunter\" (Saltatio Mortis "
                       "feat. The Elder Scrolls Online, 2022)",
                       "\n".join(x[0] for x in first), "\n".join(x[1] for x in first),
                       notes="Refrain as set out in the lyrics on the wiki; it stands %d times in the "
                             "song. The other lines of the song are English. english = the wiki "
                             "editors' hover glosses, not text from the song's publisher."
                             % same,
                       base_id="song-pray-to-the-hunter", canon_status="official promotional song "
                       "(the wiki credits Saltatio Mortis, Promethius Productions and Bethesda Softworks)",
                       source_title="The Elder Scrolls Online (promotional music video)",
                       gloss_source="wiki hover gloss", spelling="as written on the wiki")
    page = pages.get("General:Skyrim\u2019s Dragon Shouts")
    if page:
        text = clean(page.text)
        seen = set()
        for m in re.finditer(r"[\u201c\u2018]([A-Za-z\u2019']+)[\u201d\u2019],? "
                             r"(translates to|means|could mean either|could mean) "
                             r"[\u201c]?([^.,\u201d]+)", text):
            word, verb, gloss = m.group(1), m.group(2), m.group(3).strip()
            if word.lower() in seen:
                continue
            seen.add(word.lower())
            a0 = max(text.rfind(". ", 0, m.start()) + 2, text.rfind("\n", 0, m.start()) + 1, 0)
            b0 = text.find(".", m.end())
            corpus.add("other", page, "Game Informer feature \"Skyrim\u2019s Dragon Shouts\" "
                       "(Matt Miller; interview with Todd Howard and Emil Pagliarulo), as archived "
                       "on the wiki", word, gloss,
                       notes="Sentence in the article: " + text[a0:b0 + 1].strip(),
                       base_id="word-gloss-game-informer", subtype="word_gloss_in_press_article",
                       uncertain=True if "could" in verb else None,
                       canon_status="semi-canon (developer statements reported by the press)",
                       translation_source="stated in the article")


CUSTOM_NAMES = [
    # (page, regex on the cleaned page text, term group, gloss groups, note)
    ("Skyrim:Dovahkiin", r'"(Dovah Sos)" \((dragonblood)\)', 1, (2,),
     "the wiki gives the English in parentheses and cites Paarthurnax"),
    ("Skyrim:Dovahkiin", r'Although "(Dovah Kiin)" translates to "(Dragonborn)"', 1, (2,),
     "the wiki states this meaning in a note"),
    ("Skyrim:Dovahkiin", r'"(Dov Ah Kiin)", as a three-word dragon name, translates to "([^"]+)", or "([^"]+)"',
     1, (2, 3), "the wiki states this meaning in a note (its own analysis)"),
    ("Lore:Ja'darri", r"in the dragon tongue as (Toshrakhat)\), (was an ancient Khajiiti hero)", 1, (),
     "the wiki gives this as the dragon-tongue name of Ja'darri the Endless and states no meaning"),
    ("Lore:Akatosh", r"(Bormahu) \((Our Father)\) to the dragons", 1, (2,),
     "the wiki gives the English in parentheses and cites Paarthurnax's dialogue"),
    ("Lore:Throat of the World", r"called the (Monahven) \(lit\. ([^)]+)\) by the Dragons", 1, (2,),
     "the wiki gives a literal meaning in parentheses and cites Paarthurnax's dialogue"),
    ("Lore:Nordic", r'(Season Unending): "War" or "War without end"\. Comes from the word "(Evgir Unslaad)" '
                    r"in the Dragon language", 2, (1,),
     "the wiki's Nordic word list: the Nordic phrase 'Season Unending' is glossed this way and "
     "is said to come from the dragon-language phrase"),
]


def parse_custom_names(pages, corpus):
    for title, pattern, tg, ggs, how in CUSTOM_NAMES:
        page = pages.get(title)
        if not page:
            continue
        m = text = None
        for raw_line in page.text.split("\n"):
            if raw_line.startswith(("|", "!", "{|")):
                continue                      # not prose
            text = clean(raw_line, keep_newlines=False)
            m = re.search(pattern, text)
            if m:
                break
        if not m:
            continue
        dot = text.rfind(". ", 0, m.start())
        a0 = max(dot + 2 if dot != -1 else 0, m.start() - 300, 0)
        b0 = text.find(". ", m.end())
        sent = text[a0:b0 + 1 if b0 != -1 else len(text)].strip(" *")
        corpus.add("name", page, page.title, m.group(tg),
                   " | ".join(m.group(g) for g in ggs) or None,
                   notes="Wiki sentence: " + sent[:600], base_id="name-" + slug(page.title),
                   how_stated=how,
                   uncertain=True if "possible reference" in sent else None,
                   canon_status="term is canon; the meaning is the wiki's statement")


# ---------------------------------------------------------------------------
# f. Names
# ---------------------------------------------------------------------------
LANG_RE = re.compile(r"(dragon[ -]language|dragon[ -]tongue|draconic|language of (?:the )?dragons|"
                     r"native language|their tongue|tongue of the (?:\[\[[^\]|]*\|)?dragons)", re.I)
GLOSS_VERB = r"(?:means?|meant|meaning|translates?|translated|literally)"
VERB_RE = re.compile(r"\b(%s|broken down|broken into|separated)\b" % GLOSS_VERB, re.I)
HEDGE_RE = re.compile(r"\b(may|might|could|either|possibly|perhaps|no known translation|"
                      r"more accurately|more sensible)\b|\[\?\]", re.I)
LANG_LINK = (r"(?:\[\[Lore: ?Dragon Language\|[^\]]*\]\]|[Dd]ragon[ -](?:[Ll]anguage|[Tt]ongue)|"
             r"\[\[Lore: ?Dragon Language\]\])")
TERM_IN_LANG = re.compile(
    r"'''([^']+?)'''(?: or '''([^']+?)''')?\s*,?\s*in (?:the |their )?" + LANG_LINK)
SKIP_NAME_PAGES = ("Lore:Dragon Language", "Lore:Word Walls", "Lore:Dragon Alphabet", "Lore:Songs",
                   "Lore:Thu'um", "Legends:Paarthurnax", "Lore:Scaleborn", "Lore:Fa-Nuit-Hen",
                   "Lore:Dragonling")


def quoted(s):
    out = []
    for m in re.finditer(r"\"([^\"]{1,90})\"|'''([^']{1,90})'''|''([^']{1,90})''|"
                         r"“([^”]{1,90})”|(?<![\w'])'([A-Z][^']{1,60})'(?![\w'])", s):
        g = next(g for g in m.groups() if g)
        g = g.strip().strip('"').strip().rstrip(",.;").strip()
        if g:
            out.append(g)
    return out


def raw_inline(sent):
    """A raw sentence with templates and links resolved but quote marks kept."""
    t = strip_refs(sent)
    for _ in range(6):
        new = _INNER_T.sub(lambda m: _template_text(m.group(1)), t)
        if new == t:
            break
        t = new
    return re.sub(r"\[\[(?:[^\[\]|]*\|)?([^\[\]|]*)\]\]", r"\1", t)


def sentence_head(sent, page):
    """What an English sentence is about: its leading bold term or link, else the page."""
    lead = sent.lstrip("*: ")
    m = re.match(r"(?:The )?'''(?:\[\[[^\]|]*\|)?([^'\]]+?)(?:\]\])?'''", lead)
    if m:
        return clean(m.group(1))
    m = re.match(r"(?:The )?\[\[[^\]|]*\|([^\]]+)\]\]", lead)
    if m:
        return clean(m.group(1))
    return page.subject


def name_candidates(sent, plain, page, text_before, lex):
    """-> list of (term, gloss, how).  Heuristic reading of one wiki sentence."""
    raw = raw_inline(sent)
    stated = "the wiki states this meaning in the sentence"
    pairs = re.findall(r'"([^"]+)" means "([^"]+)"', plain)
    if len(pairs) >= 2:
        return [(a, b, stated) for a, b in pairs]
    pairs = re.findall(r'"(\w+)" \(([^)]+)\)', plain)
    if len(pairs) >= 2 and re.search(r"broken (?:down )?into", plain):
        whole = re.search(r'name "(\w+)"', plain)
        out = [(a, b, stated) for a, b in pairs]
        if whole:
            out.insert(0, (whole.group(1), " + ".join("%s (%s)" % p for p in pairs),
                           "the wiki breaks the name into these parts"))
        return out

    vm = re.search(r"\b%s\b" % GLOSS_VERB, raw, flags=re.I)
    tail = raw[vm.start():] if vm else ""
    cut = re.split(r"\bin\s+(?:the )?(?:Dragon|dragon)", tail)[0]
    glosses = quoted(cut) or quoted(tail)
    gloss = " | ".join(clean(g) for g in glosses) if glosses else None
    if vm and not gloss:
        m = re.match(r"%s(?: to| as| from [^,]+? as)?\s+(.{2,90}?)(?:\s+in (?:the )?[Dd]ragon|[.;]?\s*$)"
                     % GLOSS_VERB, clean(tail, keep_newlines=False), flags=re.I)
        if m:
            gloss = m.group(1).strip()
    how = stated

    pm = re.search(r"\b%s\b" % GLOSS_VERB, plain, flags=re.I)
    pre_plain = plain[:pm.start()] if pm else plain
    term = None
    m = re.search(r'called "([^"]+)"', plain)
    if m and vm:
        term = m.group(1)
    if term is None:
        m = re.match(r"\W*In (?:the )?" + LANG_LINK + r"[^.]{0,60}?known as '''([^']+)'''", sent)
        if m:
            term = clean(m.group(1))
    if term is None:
        tm = TERM_IN_LANG.search(sent)
        if tm and not re.search(r"\b%s\b" % GLOSS_VERB,
                                clean(sent[:tm.start()], keep_newlines=False)[-40:], flags=re.I):
            terms = [clean(tm.group(1))]
            if tm.group(2):
                first = terms[0]
                terms = ([first] if is_dragon_word(tokens(first)[0], lex) else []) + \
                    [clean(tm.group(2))]
            term = " / ".join(terms)
            after = raw_inline(sent[tm.end():])
            am = re.match(r"\s*,?\s*\)?,?\s*(?:which means|literally|meaning)\s+(.+)", after, flags=re.S)
            if am and quoted(am.group(1)[:160]):
                gloss = " | ".join(clean(q) for q in quoted(am.group(1)[:160]))
            else:
                # "'''Light''' or '''Aether''' (known as '''Jun''' ...": keep both English terms
                bm = re.search(r"((?:'''[^']+'''\s+or\s+)*'''[^']+''')\s*\((?:also )?known as[^()]*$",
                               sent[:tm.start()])
                gloss = clean(bm.group(1)) if bm else sentence_head(sent, page)
                how = "the wiki gives this as the dragon-language name of the English term"
    if term is None:
        m = re.search(r"(?:'''|\")([^'\"]{2,40})(?:'''|\")\s*\(\s*(?:which )?mean\w*", raw)
        if m:
            term = clean(m.group(1))
            inner = quoted(raw[m.end():m.end() + 140].split(")")[0])
            if inner:
                gloss = " | ".join(clean(q) for q in inner)
    if term is None and vm:
        m = re.search(r"[\"“']{1,2}([^\"”']{2,40})[\"”']{1,2}\s*"
                      r"(?:literally |simply |either |may |might |could |can either be |roughly )*$",
                      raw[:vm.start()])
        if m:
            term = clean(m.group(1))
    if term is None and vm:
        m = re.search(r"\b(?:the name|the dragon|the word) ([A-Z][\w']+)\b[^.]*$", pre_plain) or \
            re.search(r"\b([A-Z][\w']+), whose name\s*$", pre_plain) or \
            re.match(r"([A-Z][\w']+) is a name in\b", plain) or \
            re.match(r"([A-Z][\w']+)'s name\s*$", pre_plain)
        if m and m.group(1) != page.subject.split()[0] and \
                not re.match(r"(His|Her|Its|The|Their)$", m.group(1)):
            term = m.group(1)
    if term is None and vm:
        m = re.search(r"(?:^|, )([A-Z][\w']+(?: [A-Z][\w']+){0,2})\s*"
                      r"(?:literally |simply |either |may |might |could |can either be |roughly )*$",
                      pre_plain.strip() + " ")
        if m and not re.match(r"(His|Her|Its|The|Their|Name)\b", m.group(1)) and \
                "name" not in pre_plain.lower():
            term = m.group(1)
    if term is None and re.match(r"Name means\b", plain):
        anchors = [pos[0].strip() for n, nd, pos, s0, e0 in
                   template_calls(text_before[-1500:], {"anchor"}) if pos]
        if anchors:
            term = anchors[-1]
            how = "the wiki states this meaning in a note under the item"
    if term is None and re.match(r"(Its|His|Her) (default )?name\b", plain):
        dm = re.search(r'default name is "([^"]+)"', page.text)
        if dm:
            term = dm.group(1)
            how = "the wiki states this meaning of the pet's default name"
    if term is None:
        term = page.subject
        if page.ns == "Online" and term.endswith(" Style"):
            term = term[:-len(" Style")]     # ESO outfit-style pages are titled "<name> Style"
        m_sep = re.search(r"(?:separated|broken down) into (?:three words[^:]*: )?"
                          r"\"?([A-Z][a-z]+(?:[ -][A-Z][a-z]+)+)\"?", plain)
        if m_sep:
            term = "%s (%s)" % (page.subject, m_sep.group(1))
            if gloss and gloss.startswith(m_sep.group(1) + " | "):
                gloss = gloss[len(m_sep.group(1)) + 3:]
    if gloss and term and gloss.startswith(term + " | "):
        gloss = gloss[len(term) + 3:]
    return [(term, gloss, how)]


def parse_names(pages, corpus, lex):
    seen = set()
    for page in pages.values():
        if page.title in SKIP_NAME_PAGES or page.ns in ("Template", "General", "Books"):
            continue
        text = strip_refs(strip_comments(page.text))
        text = re.sub(r"<includeonly>.*?</includeonly>", "", text, flags=re.S)
        text = re.sub(r"</?(?:noinclude|includeonly)>", "", text)
        offset = 0
        # on a creature's own page a sentence about "<Name>'s name" needs no mention of the language
        subj = re.escape(page.subject.split()[0])
        own = re.compile(r"(?:\"%s\"|%s's name|^%s) (?:can be broken down|literally translates|"
                         r"translates|literally means|means)\b" % (subj, subj, subj)) \
            if page.ns in ("Skyrim", "Online", "Blades") and \
            re.search(r"\{\{\s*(?:Online |Basic |Blades )?(?:NPC|Creature) Summary", page.text, flags=re.I) \
            else None
        for line in text.split("\n"):
            offset += len(line) + 1
            if not LANG_RE.search(line) and not (own and own.search(clean(line.lstrip("*: ")))):
                continue
            for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z'\[*\"])", line):
                if not LANG_RE.search(sent) and not (own and own.search(clean(sent.lstrip("*: ")))):
                    continue
                flags = set()
                plain = clean(sent.lstrip("*: "), flags=flags, keep_newlines=False)
                has_term = TERM_IN_LANG.search(sent) or re.search(r"known as '''", sent)
                if not has_term and not VERB_RE.search(plain):
                    continue
                if re.search(r"\b(passage|rhymes|roughly translates as|impossible to translate|"
                             r"when translated|versed in|can be translated\.$)", plain) or \
                        "Direct translation" in plain or "predates the creation" in plain:
                    continue
                for term, gloss, how in name_candidates(sent, plain, page, text[:offset], lex):
                    if not term:
                        continue
                    no_translation = "no known translation" in plain
                    if gloss is None and not no_translation:
                        continue
                    if no_translation and "translates to" not in plain:
                        gloss = None
                    key = (page.title, norm(term), norm(gloss or ""))
                    if key in seen:
                        continue
                    seen.add(key)
                    scope = re.split(r"\bin (?:the )?[Dd]ragon", plain)[0] if gloss else plain
                    uncertain = bool(HEDGE_RE.search(scope)) or bool(flags) or no_translation
                    corpus.add("name", page, page.title, term, gloss,
                               notes="Wiki sentence: " + plain +
                                     (" " + " ".join(sorted(flags)) if flags else ""),
                               base_id="name-" + slug(page.title), how_stated=how,
                               uncertain=True if uncertain else None,
                               canon_status="name is canon; the meaning is the wiki's statement "
                                            "(see the sentence in notes for any source it names)")
    # dragon names set in dragon runes with a gloss (Skyrim:Dragon)
    page = pages.get("Skyrim:Dragon")
    if page:
        for m in re.finditer(r"\{\{DragonFont\|([^|}]+)\|3\}\}<br\s*/?>\s*<small>\"([^\"]+)\"</small>",
                             page.text):
            spelled = decode_font(m.group(1))
            corpus.add("name", page, "Skyrim:Dragon, table of named dragons", spelled, m.group(2),
                       notes="Name as the wiki sets it in dragon runes, with the meaning the table gives.",
                       base_id="name-skyrim-dragon-table", runes=runes_of(spelled),
                       how_stated="wiki table (name in dragon runes with a quoted meaning)",
                       spelling="wiki rune-case (upper case = one rune, lower-case pair = one two-letter rune)",
                       canon_status="name is canon; the meaning is the wiki's statement")
    page = pages.get("Lore:Holdings of Jarl Gjalund")
    if page:
        for line in page.text.split("\n"):
            for name, nd, pos, s, e in template_calls(line, {"dragonfont"}):
                if len(pos) < 3:
                    continue
                spelled = decode_font(pos[0])
                title = clean(pos[2])
                mm = re.match(r"(.+?)\s+-\s+(.+)", title)
                place = clean(line[:s], keep_newlines=False).rstrip(" -")
                corpus.add("name", page, "Holdings of Jarl Gjalund (map text): %s" % place, spelled,
                           mm.group(2) if mm else None,
                           notes="Rune label on the map as encoded by the wiki; english = the wiki's "
                                 "mouse-over text for it (\"%s\"). Entry for: %s" % (title, place),
                           base_id="name-holdings-of-jarl-gjalund", runes=runes_of(spelled),
                           how_stated="wiki mouse-over text on the rune label",
                           spelling="wiki rune-case (upper case = one rune, lower-case pair = one two-letter rune)",
                           canon_status="canon (official map text); the gloss is the wiki's")
    page = pages.get("Lore:Dragon Priest Masks")
    if page:
        for level, head, body in sections(page.text):
            m = re.search(r"\}\}\s*Meaning \"([^\"]+)\"(?: \(literally \"([^\"]+)\"\))?", body)
            if m and level >= 2:
                gloss = m.group(1) + (" | literally: " + m.group(2) if m.group(2) else "")
                corpus.add("name", page, "Lore:Dragon Priest Masks, section %s" % clean(head),
                           clean(head), gloss,
                           notes="Wiki sentence opens: Meaning \"%s\"%s" % (
                               m.group(1), " (literally \"%s\")" % m.group(2) if m.group(2) else ""),
                           base_id="name-dragon-priest-mask",
                           how_stated="the wiki states this meaning in the section",
                           canon_status="name is canon; the meaning is the wiki's statement")


# ---------------------------------------------------------------------------
# Shouts as corpus texts, duplicates, counts, output
# ---------------------------------------------------------------------------
def add_shout_texts(shouts, corpus, pages):
    for sh in shouts:
        if not sh["phrase"]:
            continue
        page = pages[sh["source_page"]]
        where = "; ".join(sh["locations"]) if sh["locations"] else (sh["availability"] or sh["game"])
        corpus.add("shout", page, where, sh["phrase"], sh["meaning_phrase"],
                   notes=("Shout: %s. " % sh["name"] if sh["name"] else "") +
                         "Word-by-word meanings as the wiki gives them; see canon-shouts.json.",
                   base_id="shouttext-" + slug(sh["name"] or sh["phrase"]),
                   shout=sh["name"], shout_id=sh["id"], game=sh["game"],
                   uncertain=True if "???" in (sh["meaning_phrase"] or "") else None,
                   canon_status="canon", subtype="shout_phrase")


def mark_duplicates(corpus):
    first = {}
    order = {"word_wall": 0, "song": 1, "other": 2, "dialogue": 3, "shout": 4, "name": 5}
    for t in corpus.texts:
        if t["type"] not in ("word_wall", "song", "other") and t.get("subtype") != "ceremony":
            continue
        key = norm(t["dovahzul"])
        if key in first and first[key]["id"] != t["id"]:
            t["duplicate_of"] = first[key]["id"]
            if norm(t["english"] or "") != norm(first[key]["english"] or ""):
                t["notes"] = ((t["notes"] + " ") if t["notes"] else "") + \
                    "Same dragon text as %s, but the wiki's English differs between the two pages." \
                    % first[key]["id"]
        else:
            first[key] = t
    # dialogue lines given a second time with the wiki's line-by-line translation
    seg_index = {}
    for t in corpus.texts:
        if t["type"] == "dialogue" and t.get("subtype") != "line_with_translation":
            for sg in t.get("segments", []):
                seg_index.setdefault(norm(sg["dovahzul"]), t)
            seg_index.setdefault(norm(t["dovahzul"]), t)
    for t in corpus.texts:
        if t.get("subtype") == "line_with_translation":
            hit = seg_index.get(norm(t["dovahzul"]))
            if hit is None:
                parts = [seg_index.get(norm(x)) for x in re.findall(r"[^.!?]+[.!?]*", t["dovahzul"])
                         if norm(x)]
                hit = parts[0] if parts and all(parts) else None
            if hit is not None:
                t["duplicate_of"] = hit["id"]
                t["notes"] = ((t["notes"] + " ") if t["notes"] else "") + \
                    "The same line is on %s with a hover gloss (%s); this record keeps the wiki's " \
                    "other translation of it." % (hit["source_page"], hit["id"])
    # song fragments that repeat lines of the full Song of the Dragonborn
    full = [t for t in corpus.texts if t["id"].startswith("song-of-the-dragonborn-")]
    if full:
        full_lines = set(norm(l) for l in full[0]["dovahzul"].split("\n"))
        full_norm = norm(full[0]["dovahzul"])
        for t in corpus.texts:
            if not (t["type"] == "song" or t.get("subtype") == "merchandise_text") or \
                    t is full[0] or t.get("duplicate_of"):
                continue
            mine = [norm(l) for l in t["dovahzul"].split("\n") if l.strip()]
            if mine and all(m in full_norm or m in full_lines for m in mine):
                t["duplicate_of"] = full[0]["id"]
                t["notes"] = ((t["notes"] + " ") if t["notes"] else "") + \
                    "All of these lines also occur in %s." % full[0]["id"]


RED_LINKS = ["Lore:Songs of Skyrim", "Lore:Kahvozein", "Lore:Lodunost", "Lore:Krahnoviir",
             "Lore:Bahlokdaan", "Lore:Vahlokzin", "Lore:Shulkunaak", "Lore:Sahrotnax", "Lore:Vahlok"]

# Pages that were read by hand and hold something dragon-related the parser does not turn
# into records (or that were fetched on a search hit that proved to be something else).
NOT_PARSED_NOTES = {
    "Lore:Calcelmo's Stone": "Search hit only: the text is Falmer and Dwemer, not Dragon Language.",
    "Online:Dwarven Bear": "Default mount name 'Btham Ahrk' is given without any meaning or language note.",
    "Lore:Songs of the Return, Vol 19": "Ship names Kaal Kaaz and Sadon Reyth occur in an English book "
                                        "text; the wiki does not call them Dragon Language here. Not parsed.",
    "Lore:Ysgramor": "Ship names Kaal Kaaz, Krilot Lok and Sadon Reyth occur in English prose; the wiki "
                     "states no meanings. Not parsed.",
    "Lore:Dragonne Papr\u00e9": "Pre-Skyrim dragon name; the wiki says it has no known translation.",
    "Lore:Skakmat": "Pre-Skyrim dragon name; the wiki says it has no known translation.",
    "Lore:Tosh Raka": "Says Toshrakhat was the dragon-tongue name Nahfahlaar gave Ja'darri (recorded "
                      "from Lore:Ja'darri instead).",
    "Redguard:Nafaalilargus": "Pre-Skyrim spelling of Nahfahlaar; no dragon-language text.",
    "Daggerfall:Dragonish": "Daggerfall's 'Dragonish' language skill; no text, and not the Skyrim language.",
    "Lore:Debudjen": "Dragon named in an older source; no dragon-language text or meaning.",
    "Lore:Numinex": "No stated meaning for the name.",
    "Books:The Elder Scrolls V: Skyrim: Prima Official Game Guide":
        "Bibliographic page only; the guide's own word list is not reproduced on it.",
    "Skyrim:Kinect Commands": "Says shouts can be spoken in English or Dragon Language and points to "
                              "Skyrim:Dragon Shouts; holds no list of its own.",
    "General:Behind the Wall: The Making of Skyrim": "Developers describe writing the theme song in the "
                                                     "dragon language; no dragon text.",
    "General:Emil Pagliarulo": "Biography of the language's author; no dragon text.",
    "General:Elsweyr & Update 22 AUA": "A fan's question uses the word 'Dovahzul'; the ZeniMax reply "
                                       "speaks of 'Dov words'. No dragon text.",
    "General:A Matter of Voice and Brass: Dragon Bones DLC Interview": "Background on Zaan the "
                                                                       "Scalecaller; no dragon text.",
    "Lore:Kireth's Taarengrav Note": "Mentions carvings in the Dragon tongue; gives none of the text.",
    "Lore:The Sublime Brazier": "Mentions dragons whispering in a long-dead tongue; no text.",
    "Lore:Whiterun Hold Jarl's Letter": "Says a ring is engraved with the city's name in Dragon Language; "
                                        "the name itself is on Lore:Whiterun.",
    "Merchandise:The Elder Scrolls Whiterun Honorary Citizen Chest": "Same ring; no text.",
    "Merchandise:Skyrim Limited Edition Dragonstone Replica": "Gives only the English of the Dragonstone "
                                                              "inscription ('Here lie our fallen lords "
                                                              "until power of Alduin revives').",
    "Merchandise:Skyrim Limited Edition Coin 1": "Quotes Esbern's trailer line with the word Dovahkiin.",
    "General:The Elder Scrolls V: Skyrim Announcement Trailer": "Esbern's narration; the only dragon word "
                                                                "is Dovahkiin.",
    "General:The Elder Scrolls V: Skyrim - Official Trailer": "Esbern's narration; the only dragon word "
                                                              "is Dovahkiin.",
    "Skyrim:Easter Eggs": "Refers to the Become Ethereal wall (Azaran the Cruel); the wall text is "
                          "recorded from Skyrim:Become Ethereal.",
    "Skyrim:Music": "Says the main theme is sung in the dragon tongue; no lyrics on the page.",
    "Skyrim:Loading Screens": "Names the 'Song of the Dragonborn'; no dragon text.",
    "Legends:Word Wall": "Card page; no inscription text.",
    "Online:Lendoran Ruin": "ESO location with a word wall; the page gives no inscription text.",
    "Lore:Dragon Priest": "List of priests; meanings are recorded from Lore:Dragon Priest Masks.",
    "Skyrim:Dragon Priest": "Generic creature page; meanings are recorded from the named priests' pages.",
    "Lore:Arngeir": "Lists the shouts Arngeir is known to master (all recorded from the shout pages).",
}


def why_nothing(page):
    if page.title in NOT_PARSED_NOTES:
        return NOT_PARSED_NOTES[page.title]
    if page.ns == "Template":
        return "Template page, fetched to understand the markup of the pages that use it."
    if re.search(r"\{\{\s*Game Book", page.text) and len(page.text) < 1500:
        return "Infobox only: the book's text stands on the matching Lore: page, which is parsed."
    return "Read by the parser; no dragon-language text or stated meaning was found on it."


def count_tokens(t):
    if t.get("segments"):
        return sum(len(tokens(s["dovahzul"])) for s in t["segments"])
    return len(tokens(t["dovahzul"]))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--report", action="store_true", help="print a summary to stdout")
    args = ap.parse_args()

    pages = load_pages()
    if not pages:
        sys.stderr.write("no pages under %s; run fetch_corpus.py first\n" % SRC_DIR)
        return 1
    dictionary = pages.pop(LEXICON_PAGE, None)

    for p in pages.values():
        if p.ns in NPC_NS and re.search(r"\{\{\s*(?:Online |Basic |Blades )?(?:NPC|Creature) Summary",
                                        p.text, flags=re.I) and \
                re.fullmatch(r"[A-Z][\w'\-]+(?: [A-Z][\w'\-]+){0,2}", p.subject) and \
                p.subject not in ("Dragon", "Draugr", "Dragon Priest", "Skeletal Dragon"):
            KNOWN_SPEAKERS.append(p.subject)
    for extra in ("Paarthurnax", "Alduin", "Odahviing", "Durnehviir", "Miraak", "Arngeir",
                  "Einarth", "Borri", "Wulfgar", "Tsun", "Morokei", "Sahloknir", "Mirmulnir",
                  "Nahfahlaar", "Laatvulon", "Shulkunaak", "Kaalgrontiid", "Joorahmaar"):
        if extra not in KNOWN_SPEAKERS:
            KNOWN_SPEAKERS.append(extra)

    for p in pages.values():
        if re.fullmatch(r"[A-Z][\w']+", p.subject):
            NAME_TOKENS.add(p.subject.lower())
    NAME_TOKENS.update(n.lower() for n in KNOWN_SPEAKERS if " " not in n)
    NAME_TOKENS.update(["ysmir", "skuldafn", "sovngarde", "tamriel", "keizaal", "akatosh",
                        "vahlok", "ahkahtuz", "toshrakhat"])
    NAME_TOKENS.difference_update(["dragon", "draugr", "krosis"])

    corpus = Corpus()
    shouts, available = parse_shout_pages(pages)
    parse_unavailable_shouts(pages, shouts)
    thuum_list = parse_lore_thuum(pages, shouts)
    eso_rows = parse_eso_shouts(pages, shouts)

    parse_word_walls(pages, shouts, corpus)
    parse_lore_word_walls(pages, corpus)
    parse_lore_place_word_walls(pages, corpus)
    parse_translation_tables(pages, corpus)
    parse_song_books(pages, corpus)
    parse_myth_no_more(pages, corpus)
    parse_flying_gods(pages, corpus)
    add_shout_texts(shouts, corpus, pages)
    lex, used_dictionary = build_lexicon(pages, corpus)
    parse_legends_audio(pages, shouts, corpus, lex)
    parse_other_title_shouts(pages, shouts, corpus)
    parse_dialogue(pages, corpus, lex)
    parse_names(pages, corpus, lex)
    parse_custom_names(pages, corpus)
    parse_special(pages, corpus)
    mark_duplicates(corpus)
    alphabet = parse_alphabet(pages)

    # ---- order, ids, counts
    type_order = ["word_wall", "song", "dialogue", "name", "shout", "other"]
    corpus.texts.sort(key=lambda t: type_order.index(t["type"]))
    assert len(set(t["id"] for t in corpus.texts)) == len(corpus.texts), "duplicate ids"
    by_type = Counter(t["type"] for t in corpus.texts)
    unique = [t for t in corpus.texts if not t.get("duplicate_of")]
    tok_all = sum(count_tokens(t) for t in corpus.texts)
    tok_unique = sum(count_tokens(t) for t in unique)
    tok_by_type = Counter()
    for t in unique:
        tok_by_type[t["type"]] += count_tokens(t)
    vocab = set()
    for t in unique:
        segs = t.get("segments") or [{"dovahzul": t["dovahzul"]}]
        for s in segs:
            vocab.update(x.lower() for x in tokens(s["dovahzul"]))

    used = set(corpus.pages_used) | {s["source_page"] for s in shouts}
    for s in shouts:
        used.update(a["source_page"] for a in s["also_attested_in"])
    if alphabet:
        used.update(["Lore:Dragon Alphabet", "Template:DragonFont/Doc"])
    for t in corpus.texts:
        for ref in t.get("also_on", []):
            used.add(ref.split(" (rev ")[0])
    not_used = [p.title for p in pages.values() if p.title not in used]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lic = next(iter(pages.values())).manifest
    source_pages = [OrderedDict([("title", p.title), ("revid", p.revid),
                                 ("timestamp", p.timestamp), ("sha256", p.manifest["sha256"]),
                                 ("groups", p.groups),
                                 ("texts_extracted", corpus.pages_used.get(p.title, 0))])
                    for p in pages.values()]
    common_meta = OrderedDict([
        ("generated_at", now),
        ("generator", "tools/ingest/parse_corpus.py"),
        ("source", "UESP wiki (en.uesp.net), MediaWiki API snapshot under research/sources/uesp/"),
        ("license", lic.get("license")),
        ("license_url", lic.get("license_url")),
        ("attribution", "Text from the Unofficial Elder Scrolls Pages (UESP), "
                        "https://en.uesp.net/ ; each record names its page and revision id."),
    ])

    corpus_out = OrderedDict([
        ("meta", OrderedDict(list(common_meta.items()) + [
            ("schema", OrderedDict([
                ("id", "stable within one run of the parser: <kind>-<page or work>-<n>"),
                ("type", "word_wall | song | dialogue | name | shout | other"),
                ("source_page", "UESP page title the text was read from"),
                ("revid", "revision id of that page in the snapshot"),
                ("location_or_speaker", "where the text stands or who speaks it, as the wiki gives it"),
                ("dovahzul", "the dragon-language text, wiki spelling, newline = wiki line break; for "
                             "dialogue: only the dragon-language segments of the line, one per line"),
                ("english", "the translation or gloss that stands on the wiki, or null; never supplied "
                            "by this parser"),
                ("notes", "provenance of the gloss, wiki caveats, sic notes"),
                ("optional fields",
                 "subtype, shout, teaches_word_index, teaches_words, teaches_meanings, "
                 "highlighted_dovahzul, highlighted_english, in_game, game, spelling, canon_status, "
                 "translation_source, gloss_source, context (full line as shown on the wiki), "
                 "segments (aligned dragon/gloss pairs), also_on (other snapshot pages with the same "
                 "line), duplicate_of (id of an earlier record with the same dragon text), "
                 "uncertain, needs_review, inscription_column, transliteration_column, "
                 "rune_inscription, english_in_game, runes, how_stated, source_title"),
            ])),
            ("conventions", [
                "Word-wall and rune-table text keeps the wiki's rune-case: UPPER CASE = a one-letter "
                "rune, a lower-case pair (aa ah ei ey ii ir oo uu ur) = one two-letter rune.",
                "Parentheses and square brackets inside english are the wiki's own: they mark words "
                "added for English grammar.",
                "canon_status 'canon' means the dragon text is reported by the wiki from an official "
                "game, book or publication. It does not certify the English: see translation_source "
                "or gloss_source for where the English comes from.",
                "Hover glosses on dialogue pages are written by wiki editors; they are not in-game "
                "text. Treat them as semi-canon readings.",
                "Dialogue segments with gloss 'none on the wiki (word-list match)' were found by "
                "matching words against the wiki's own dictionary page and this corpus; that step "
                "is a heuristic and can miss or mis-cut a phrase. The 'context' field always holds "
                "the full line as the wiki prints it.",
                "Name meanings are sentences written by wiki editors, mostly built from the "
                "dictionary; 'uncertain': true marks the wiki's own hedging (may, might, either, ...).",
                "Records with duplicate_of repeat dragon text found on another page; they are kept "
                "for provenance and left out of the unique token count.",
            ]),
            ("counts", OrderedDict([
                ("texts_total", len(corpus.texts)),
                ("texts_by_type", OrderedDict((k, by_type.get(k, 0)) for k in type_order)),
                ("texts_unique_dragon_text", len(unique)),
                ("dragon_tokens_all_records", tok_all),
                ("dragon_tokens_unique_records", tok_unique),
                ("dragon_tokens_unique_by_type",
                 OrderedDict((k, tok_by_type.get(k, 0)) for k in type_order)),
                ("distinct_word_forms_lowercased", len(vocab)),
                ("token_rule", "letters with inner apostrophes or hyphens count as one token; "
                               "dialogue counts only its dragon-language segments"),
            ])),
            ("dialogue_word_list", OrderedDict([
                ("used_dictionary_snapshot", used_dictionary),
                ("size", len(lex)),
                ("note", "headwords read (not modified) from Lore_Dragon_Language.wikitext when "
                         "present, plus every word of the word walls, songs and shouts parsed here"),
            ])),
            ("source_pages", source_pages),
            ("pages_fetched_but_nothing_extracted",
             [OrderedDict([("title", t), ("why", why_nothing(pages[t]))]) for t in sorted(not_used)]),
            ("titles_linked_from_the_dictionary_page_that_do_not_exist_on_the_wiki", RED_LINKS),
            ("discovery_on_2026-11-14", OrderedDict([
                ("how", "tools/ingest/fetch_corpus.py --discover: links out of and into "
                        "Lore:Dragon_Language, 22 full-text searches over the content namespaces, "
                        "8 categories"),
                ("titles_found", 1372),
                ("titles_in_the_fetch_list", 328),
                ("added_after_discovery", "2 (Lore:Vundeheim, Lore:Korvag Crag), found on the same "
                                          "day by a further search for \"Word Wall's translation\"; "
                                          "the fetch list now holds 330 titles"),
                ("not_fetched", "About 1,040 titles: talk and user pages; ESO patch notes, item, "
                                "pet and crown-store lists; Legends card lists; alphabetical "
                                "Lore index pages (People, Places, Bestiary, Gods, Factions, "
                                "Artifacts) that only repeat the lead of pages fetched here; other "
                                "languages' pages; pages that merely mention the word Dovahkiin. "
                                "They were judged from titles and search context, not opened."),
            ])),
            ("known_limits", [
                "Dragon names that appear only inside English prose (e.g. the ships Kaal Kaaz, Sadon "
                "Reyth, Krilot Lok) are not collected unless a wiki sentence states a meaning or a "
                "speaker uses them in a quoted line.",
                "Dialogue on pages that were not fetched is not covered. The page list was built from "
                "links, categories and word searches; a line that uses only dragon words no search "
                "term matched could have been missed.",
                "Speaker names come from the wiki's labels, or else from the page subject or the "
                "narration before the quote; the basis is stated in each record's notes.",
                "The wiki states no source for most word-wall translations; they are recorded as "
                "'translation as given on the wiki page'.",
                "The wiki's footnotes are not carried into the records. Each record names its page "
                "and revision, so the footnote behind a statement can be looked up there.",
                "When the same dragon text stands on several pages, or several times on one page, "
                "one record is kept (other pages under also_on). A second English context or a "
                "differently worded gloss on another page is then not recorded, e.g. the gloss "
                "'Ceaseless enemy!' for 'Unslaad hokoron!' on Skyrim:Alduin beside 'Unending enemy!' "
                "on Skyrim:Paarthurnax (dragon).",
                "A dialogue record's english joins its segments' glosses line by line and writes "
                "'[no gloss on the wiki]' for a segment without one; use segments[] for aligned pairs.",
                "Where the wiki sets one word outside a hover gloss (e.g. {{sic|Thurri|Thuri}} before "
                "the glossed rest of the sentence) the sentence is split into two segments as marked up.",
            ]),
            ("verification_pass_2026-11-14", OrderedDict([
                ("what", "An independent check of this file against the raw wikitext "
                         "(tools/ingest/verify_counts.py, a random sample, and a by-eye review of "
                         "every word-list segment and every name record) led to these parser changes."),
                ("changes", [
                    "Lore:Word Walls: where the inscription and transliteration columns differ "
                    "(walls 'Diin' and 'Zul, Mey, Gut'), dovahzul is now the column that the shout "
                    "page and the row's translation confirm (the inscription column); the other "
                    "column is kept in transliteration_column.",
                    "Word-list matching: six hand-checked words or phrases (REVIEWED_TEXT in the "
                    "parser) are taken as dragon text on their page, which repairs five cut-short "
                    "or incomplete dialogue records; each such record says so in its notes.",
                    "Names: 'Dovah's Du'ul' no longer carries the English word 'Style' from the page "
                    "title; Jun is glossed 'Light or Aether' as the sentence has it.",
                    "English context: the game's own placeholders in angle brackets (<man/woman>) are "
                    "kept; only mark-up tags are removed.",
                    "Two more pages fetched and parsed: Lore:Vundeheim and Lore:Korvag Crag, each "
                    "quoting a word wall already recorded from its shout page.",
                ]),
            ])),
        ])),
        ("texts", corpus.texts),
    ])

    shouts_out = OrderedDict([
        ("meta", OrderedDict(list(common_meta.items()) + [
            ("notes", [
                "One record per distinct shout. Skyrim shout pages are the primary source for the "
                "words, their rune spelling and their meanings; other pages that name the same "
                "words are listed under also_attested_in, with differs_from_primary set where "
                "their English differs.",
                "word = first letter upper case, rest lower case (as the wiki's infobox renders "
                "it); word_wiki_spelling = the infobox parameter as typed, in rune-case.",
                "ESO rows come from the table on Online:Dragon; their 'name' is the ESO ability "
                "the wiki pairs with the line, where it gives one.",
                "lore_thuum_list repeats the whole 'Known Shouts' list of Lore:Thu'um, including "
                "shouts for which the wiki records no dragon words.",
            ]),
            ("counts", OrderedDict([
                ("shouts_total", len(shouts)),
                ("with_words_of_power", sum(1 for s in shouts if s["phrase"])),
                ("skyrim_player_available", sum(1 for s in shouts if s["availability"] == "player")),
                ("by_game", OrderedDict(sorted(Counter(s["game"] or "unknown" for s in shouts).items()))),
                ("distinct_words_of_power",
                 len({w["word"].lower() for s in shouts for w in s["words"]})),
            ])),
        ])),
        ("shouts", shouts),
        ("lore_thuum_list", thuum_list),
        ("player_available_per_Skyrim_Dragon_Shouts", sorted(available)),
    ])

    alpha_out = OrderedDict([
        ("meta", OrderedDict(list(common_meta.items()) + [
            ("notes", [
                "The wiki describes the script as a whole but gives no description of any single "
                "rune's shape; shape_description is therefore null for every rune. Glyphs exist on "
                "the wiki only as a web font.",
                "latin = the Latin value the wiki's table heads the rune with.",
                "dragonfont_template_code = what the wiki's {{DragonFont}} template is given to "
                "print the rune: the letter itself, or a digit 1-9 for the two-letter runes.",
                "wiki_spelling_in_transcriptions = how the rune is typed in the wiki's rune-case "
                "transcriptions (lower-case pair for two-letter runes).",
            ]),
            ("counts", OrderedDict([
                ("runes_in_main_table", sum(1 for r in alphabet["runes"] if r["in_main_alphabet_table"])),
                ("single_letter_runes", sum(1 for r in alphabet["runes"] if r["kind"] == "single-letter rune")),
                ("two_letter_runes", sum(1 for r in alphabet["runes"] if r["kind"] == "two-letter rune")),
                ("extra_font_glyphs", sum(1 for r in alphabet["runes"] if not r["in_main_alphabet_table"])),
            ])),
        ])),
        ("runes", alphabet["runes"]),
        ("statements", alphabet["statements"]),
        ("dragonfont_template", alphabet["dragonfont_template"]),
        ("non_language_uses_of_the_script", alphabet["non_language_uses_of_the_script"]),
    ]) if alphabet else None

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    def dump(name, obj):
        (OUT_DIR / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n",
                                    encoding="utf-8")

    dump("canon-corpus.json", corpus_out)
    dump("canon-shouts.json", shouts_out)
    if alpha_out:
        dump("dragon-alphabet.json", alpha_out)

    if args.report:
        print(json.dumps(corpus_out["meta"]["counts"], indent=2))
        print(json.dumps(shouts_out["meta"]["counts"], indent=2))
        if alpha_out:
            print(json.dumps(alpha_out["meta"]["counts"], indent=2))
        print("pages with nothing extracted: %d of %d" % (len(not_used), len(pages)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
