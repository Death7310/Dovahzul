#!/usr/bin/env python3
"""Parse the saved wikitext of the UESP page Lore:Dragon_Language into JSON.

Standard library only.  Re-runnable from the repository root:

    python3 tools/ingest/parse_lexicon.py                 # parse, check, write
    python3 tools/ingest/parse_lexicon.py --sample 15     # also print 15 random
                                                          # entries beside their raw rows
    python3 tools/ingest/parse_lexicon.py --check-only    # check, write nothing

Input  (written by fetch_lexicon.py):
    research/sources/uesp/Lore_Dragon_Language.wikitext
    research/sources/uesp/manifest.d/Lore_Dragon_Language.json
Output:
    research/data/canon-lexicon.json

Ground rules of this parser:

  * Faithful.  Spellings are never changed, variants are never merged, nothing
    is added that is not in the wikitext.  Every word row keeps its exact raw
    line in "raw", so any decision made here can be checked or redone.
  * Every line of the page is accounted for.  A line the parser does not
    understand goes to "unparsed" with its raw text; it is never dropped.
  * Deterministic.  The same wikitext always gives byte-identical JSON (no
    clock, no randomness in the output).
  * The wikitext is treated as data only.  Nothing in it is executed.

The script checks itself before writing: it counts the ";" rows per letter
straight from the raw text with a separate, much simpler routine and compares
that with the parsed entries.  It exits with status 1 if a check fails.
"""

import argparse
import hashlib
import json
import random
import re
import sys
from collections import OrderedDict
from pathlib import Path

PARSER_VERSION = "1.0.1"

REPO_ROOT = Path(__file__).resolve().parents[2]
WIKITEXT = REPO_ROOT / "research" / "sources" / "uesp" / "Lore_Dragon_Language.wikitext"
MANIFEST = REPO_ROOT / "research" / "sources" / "uesp" / "manifest.d" / "Lore_Dragon_Language.json"
OUTPUT = REPO_ROOT / "research" / "data" / "canon-lexicon.json"

# Private-use code points used as internal markers while a row is taken apart.
# They never reach the output.  main() checks that the source has none of them.
REF_OPEN, REF_CLOSE, SMALL_OPEN, SMALL_CLOSE = "", "", "", ""
REF_MARK = re.compile(REF_OPEN + r"(\d+)" + REF_CLOSE)
SMALL_TAG = re.compile(r"<\s*(/?)\s*small\s*>", re.I)
HEADING = re.compile(r"^(={2,6})\s*(.*?)\s*\1\s*$")
TABLE_MARKUP = re.compile(r"^(\{\||\|\}|\|-|\|\||\|\s*(width=\S+\s*\|)?\s*$)")

# Part-of-speech markers.  A bracketed note counts as a part of speech only if
# it is exactly one of these (compared in lower case).  The stored value is the
# source's own spelling ("v.", "verb", ...), never a normalised one.
POS_MARKERS = {
    "v", "v.", "n", "n.", "adj", "adj.", "adv", "adv.", "verb", "noun",
    "adjective", "adverb", "interjection", "prep", "prep.", "preposition",
    "pron", "pron.", "pronoun", "conj", "conj.", "conjunction",
}
LITERAL = re.compile(r"^(?:lit\.|lit:|literally\s*:?|literal\s*:|lit\s)\s*", re.I)
SEE_ALSO = re.compile(r'see also\s+"([^"]+)"', re.I)
QUOTED = r'"([^"]*)"'


# --------------------------------------------------------------------------
# Small wikitext helpers
# --------------------------------------------------------------------------

def match_close(text, start, open_tok, close_tok):
    """text[start:] begins with open_tok.  Return the index just past the
    matching close_tok (nesting respected), or -1 if it is never closed."""
    depth, i, n = 0, start, len(text)
    while i < n:
        if text.startswith(open_tok, i):
            depth += 1
            i += len(open_tok)
        elif text.startswith(close_tok, i):
            depth -= 1
            i += len(close_tok)
            if depth == 0:
                return i
        else:
            i += 1
    return -1


def _walk_top(text):
    """Yield (index, char) for characters outside {{...}} and [[...]]."""
    depth_t = depth_l = 0
    i, n = 0, len(text)
    while i < n:
        two = text[i:i + 2]
        if two == "{{":
            depth_t += 1
            i += 2
        elif two == "}}" and depth_t:
            depth_t -= 1
            i += 2
        elif two == "[[":
            depth_l += 1
            i += 2
        elif two == "]]" and depth_l:
            depth_l -= 1
            i += 2
        else:
            if depth_t == 0 and depth_l == 0:
                yield i, text[i]
            i += 1


def split_top(text, sep):
    """Split on a one-character separator that is outside {{...}} and [[...]]."""
    cuts = [i for i, ch in _walk_top(text) if ch == sep]
    parts, last = [], 0
    for cut in cuts:
        parts.append(text[last:cut])
        last = cut + 1
    parts.append(text[last:])
    return parts


def find_top(text, char):
    for i, ch in _walk_top(text):
        if ch == char:
            return i
    return -1


def parse_template(raw):
    """'{{name|a|k=v}}' -> (name, [positional], {named})."""
    parts = split_top(raw[2:-2], "|")
    positional, named = [], OrderedDict()
    for part in parts[1:]:
        eq = find_top(part, "=")
        if eq >= 0:
            named[part[:eq].strip()] = part[eq + 1:].strip()
        else:
            positional.append(part)
    return parts[0].strip(), positional, named


def collapse(text):
    return re.sub(r"\s+", " ", text).strip()


def plain(wikitext):
    """Best-effort readable text of a short piece of wikitext (used only for
    the convenience field "text" of reference definitions)."""
    out, i, n = [], 0, len(wikitext)
    while i < n:
        if wikitext.startswith("{{", i):
            j = match_close(wikitext, i, "{{", "}}")
            if j > 0:
                name, positional, _named = parse_template(wikitext[i:j])
                low = name.lower()
                if low == "=":
                    out.append("=")
                elif low == "cite book":
                    out.append(plain(positional[0]) if positional else "")
                elif low == "lore link":
                    out.append(plain(positional[-1]) if positional else "")
                elif low != "ref":
                    out.append(wikitext[i:j])
                i = j
                continue
        if wikitext.startswith("[[", i):
            j = match_close(wikitext, i, "[[", "]]")
            if j > 0:
                target, bar, label = wikitext[i + 2:j - 2].partition("|")
                out.append(plain(label) if bar else target)
                i = j
                continue
        if wikitext[i] == "[":
            m = re.match(r"\[(https?://[^\s\]]+)(?:\s+([^\]]*))?\]", wikitext[i:])
            if m:
                out.append(plain(m.group(2)) if m.group(2) else m.group(1))
                i += m.end()
                continue
        out.append(wikitext[i])
        i += 1
    text = re.sub(r"'{2,}", "", "".join(out))
    text = re.sub(r"<[^>]+>", "", text)
    return collapse(text)


class Row:
    """What is collected while one row is taken apart."""

    def __init__(self):
        self.refs = []      # one dict per {{ref}} in the row, in order
        self.links = []     # one dict per [[link]] / {{Lore Link}}
        self.flags = []

    def flag(self, name):
        if name not in self.flags:
            self.flags.append(name)

    def ref_names(self, indexes=None):
        refs = self.refs if indexes is None else [self.refs[i] for i in indexes]
        names = []
        for ref in refs:
            if ref["key"] not in names:
                names.append(ref["key"])
        return names


def ref_record(positional, named):
    content = positional[0] if positional else named.get("1")
    content = content.strip() if content and content.strip() else None
    name = named.get("name")
    return {"name": name, "group": named.get("group"), "content": content,
            "key": name if name else "(unnamed: %s)" % (content or "")}


def to_marked(text, row):
    """Rewrite a piece of a row so that it can be cut up safely:
    {{ref ...}} -> a numbered marker, [[target|label]] -> label,
    <small>/</small> -> markers.  Everything else is left exactly as it is."""
    out, i, n = [], 0, len(text)
    while i < n:
        if text.startswith("{{", i):
            j = match_close(text, i, "{{", "}}")
            if j > 0:
                raw = text[i:j]
                name, positional, named = parse_template(raw)
                low = name.lower()
                if low == "ref":
                    row.refs.append(ref_record(positional, named))
                    out.append(REF_OPEN + str(len(row.refs) - 1) + REF_CLOSE)
                elif low == "vn":
                    row.flag("template_vn")
                elif low == "lore link":
                    label = positional[-1].strip() if positional else ""
                    target = positional[0].strip() if positional else ""
                    row.links.append({"target": target, "label": label, "via": "{{Lore Link}}"})
                    out.append(label)
                elif low == "=":
                    out.append("=")
                else:
                    row.flag("unknown_template:" + name)
                    out.append(raw)
                i = j
                continue
            row.flag("unbalanced_braces")
        if text.startswith("[[", i):
            j = match_close(text, i, "[[", "]]")
            if j > 0:
                target, bar, label = text[i + 2:j - 2].partition("|")
                label = label if bar else target
                row.links.append({"target": target.strip(), "label": label, "via": "[[link]]"})
                out.append(label)
                i = j
                continue
            row.flag("unbalanced_brackets")
        m = SMALL_TAG.match(text, i)
        if m:
            out.append(SMALL_CLOSE if m.group(1) else SMALL_OPEN)
            i = m.end()
            continue
        out.append(text[i])
        i += 1
    marked = "".join(out)
    if marked.count(SMALL_OPEN) != marked.count(SMALL_CLOSE):
        row.flag("unbalanced_small_tag")
        marked = marked.replace(SMALL_OPEN, "").replace(SMALL_CLOSE, "")
    return marked


def pull_refs(marked):
    """-> (text without ref markers, [ref indexes in order])."""
    return REF_MARK.sub("", marked), [int(x) for x in REF_MARK.findall(marked)]


def display(marked):
    """Marked text -> the text a reader sees (no refs, no <small> tags)."""
    text = REF_MARK.sub("", marked).replace(SMALL_OPEN, "").replace(SMALL_CLOSE, "")
    return collapse(text)


def has_text(marked):
    return bool(display(marked))


def open_paren_index(text):
    """text ends with ')'.  Index of the '(' that opens that group, or -1."""
    depth = 0
    for i in range(len(text) - 1, -1, -1):
        if text[i] == ")":
            depth += 1
        elif text[i] == "(":
            depth -= 1
            if depth == 0:
                return i
    return -1


def open_small_index(text):
    """text ends with the small-close marker.  Index of its opener, or -1."""
    depth = 0
    for i in range(len(text) - 1, -1, -1):
        if text[i] == SMALL_CLOSE:
            depth += 1
        elif text[i] == SMALL_OPEN:
            depth -= 1
            if depth == 0:
                return i
    return -1


def strip_outer_parens(text):
    """'(abc)' -> ('abc', True) when one bracket pair wraps the whole text."""
    text = text.strip()
    if text.startswith("(") and text.endswith(")") and open_paren_index(text) == 0:
        return text[1:-1].strip(), True
    return text, False


def unquote(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"' and text.count('"') == 2:
        return text[1:-1].strip()
    return text


def classify(text):
    """Decide what a bracketed / small-print remark is."""
    text = text.strip()
    if text.lower() in POS_MARKERS:
        return {"kind": "pos", "text": text}
    m = LITERAL.match(text)
    if m and text[m.end():].strip():
        return {"kind": "literal", "text": text, "value": unquote(text[m.end():])}
    if re.fullmatch(r'see also\s+"[^"]+"', text, re.I):
        return {"kind": "see_also", "text": text}
    return {"kind": "note", "text": text}


# --------------------------------------------------------------------------
# Translation Key rows:  ;Word:Definition{{ref|...}} <small>(remark)</small>
# --------------------------------------------------------------------------

def split_senses(marked):
    """Cut a definition at top-level ',' and '/' (not inside brackets or
    small print).  -> (segments, separators) where separators[k] is the
    character that stood before segments[k] (None for the first)."""
    segments, separators, buf = [], [None], []
    paren = small = 0
    i, n = 0, len(marked)
    while i < n:
        ch = marked[i]
        if ch == REF_OPEN:
            j = marked.index(REF_CLOSE, i) + 1
            buf.append(marked[i:j])
            i = j
            continue
        if ch == SMALL_OPEN:
            small += 1
        elif ch == SMALL_CLOSE:
            small = max(0, small - 1)
        elif ch == "(":
            paren += 1
        elif ch == ")":
            paren = max(0, paren - 1)
        elif ch in ",/" and paren == 0 and small == 0:
            segments.append("".join(buf))
            separators.append(ch)
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    segments.append("".join(buf))
    return segments, separators


def analyse_segment(segment, row):
    """One gloss with whatever trails it.

    Only TRAILING remarks are lifted out of the gloss: a "(...)" group or a
    <small>...</small> run that comes after the gloss text.  A group at the
    start or in the middle stays in the gloss exactly as written, e.g.
    "(Great) Victory", "(Battle)field".  A short suffix glued to the word,
    such as "Savage(s)" or "Bold(ly)", also stays."""
    rest = segment
    trailing = []                       # collected back to front
    while True:
        cut = rest.rstrip()
        if not cut:
            break
        if cut.endswith(REF_CLOSE):
            j = cut.rfind(REF_OPEN)
            trailing.append(("ref", int(cut[j + 1:-1])))
            rest = cut[:j]
            continue
        if cut.endswith(SMALL_CLOSE):
            j = open_small_index(cut)
            if j < 0 or not has_text(cut[:j]):
                break                   # small print that leads the gloss
            trailing.append(("small", cut[j + 1:-1]))
            rest = cut[:j]
            continue
        if cut.endswith(")"):
            j = open_paren_index(cut)
            if j < 0 or not has_text(cut[:j]):
                break                   # a bracket group that leads the gloss
            inner = cut[j + 1:-1]
            glued = cut[j - 1].isalnum()
            if glued and re.fullmatch(r"[A-Za-z]{1,3}", inner):
                break                   # "Savage(s)", "A(n)", "Bold(ly)"
            trailing.append(("paren", inner))
            rest = cut[:j]
            continue
        break

    # What is left is the gloss.  Refs standing before its first letter are
    # "lead" refs: the caller gives them to the gloss before this one.
    gloss_marked = REF_MARK.sub("", rest)
    lead_refs, refs, seen_text, i = [], [], False, 0
    while i < len(rest):
        m = REF_MARK.match(rest, i)
        if m:
            (refs if seen_text else lead_refs).append(int(m.group(1)))
            i = m.end()
            continue
        if not rest[i].isspace() and rest[i] not in (SMALL_OPEN, SMALL_CLOSE):
            seen_text = True
        i += 1
    remarks = []
    for kind, payload in reversed(trailing):
        if kind == "ref":
            refs.append(payload)
            continue
        text, remark_refs = pull_refs(payload)
        text = collapse(text.replace(SMALL_OPEN, "").replace(SMALL_CLOSE, ""))
        if kind == "small":
            text, _wrapped = strip_outer_parens(text)
        if not text:
            refs.extend(remark_refs)
            continue
        remark = classify(text)
        remark["refs"] = row.ref_names(remark_refs)
        remark["markup"] = "small" if kind == "small" else "parentheses"
        remarks.append(remark)
    return {"gloss": display(gloss_marked), "lead_refs": lead_refs,
            "refs": refs, "remarks": remarks}


def parse_entry(line, lineno, letter):
    row = Row()
    marked = to_marked(line[1:], row)
    colon = marked.find(":")
    if colon < 0:
        head, definition, has_colon = marked, "", False
    else:
        head, definition, has_colon = marked[:colon], marked[colon + 1:], True

    head_text, head_refs = pull_refs(head)
    word = collapse(head_text.replace(SMALL_OPEN, "").replace(SMALL_CLOSE, ""))
    if not word:
        return None
    if SMALL_OPEN in head_text:
        row.flag("small_print_in_headword")

    senses, remarks = [], []
    segments, separators = split_senses(definition)
    for k, segment in enumerate(segments):
        part = analyse_segment(segment, row)
        if ":" in part["gloss"] and senses:
            # Not a gloss but a statement about usage ("as suffix: -hood, -self").
            # It and everything after it is kept whole, as a remark.
            tail = segment
            for k2 in range(k + 1, len(segments)):
                tail += separators[k2] + segments[k2]
            tail_text, tail_refs = pull_refs(tail)
            remarks.append({"kind": "note", "text": display(tail_text),
                            "refs": row.ref_names(tail_refs), "markup": "plain",
                            "after_sense": len(senses) - 1})
            row.flag("usage_statement_kept_as_note")
            break
        if not part["gloss"]:
            # nothing but references / remarks here
            target = senses[-1] if senses else None
            if target is not None:
                for name in row.ref_names(part["lead_refs"] + part["refs"]):
                    if name not in target["refs"]:
                        target["refs"].append(name)
            for remark in part["remarks"]:
                remark["after_sense"] = len(senses) - 1 if senses else None
                remarks.append(remark)
            if len(segments) > 1:
                row.flag("empty_definition_segment")
            continue
        own_refs = part["refs"]
        if part["lead_refs"]:
            if senses:
                # "Dragonkind,{{ref}} Dragon": the ref belongs to the gloss before
                for name in row.ref_names(part["lead_refs"]):
                    if name not in senses[-1]["refs"]:
                        senses[-1]["refs"].append(name)
            else:
                own_refs = part["lead_refs"] + own_refs
        sense = {"text": part["gloss"], "pos": None,
                 "refs": row.ref_names(own_refs), "separator_before": separators[k]}
        senses.append(sense)
        for remark in part["remarks"]:
            remark["after_sense"] = len(senses) - 1
            if remark["kind"] == "pos":
                sense["pos"] = remark["text"] if not sense["pos"] else sense["pos"] + "; " + remark["text"]
            remarks.append(remark)

    # "Flow, Fly, Move{{ref}}": the tag stands after the last gloss only.  For a
    # gloss with no tag of its own, note the tags of the next gloss that has some.
    for i, sense in enumerate(senses):
        sense["refs_following"] = []
        if not sense["refs"]:
            for later in senses[i + 1:]:
                if later["refs"]:
                    sense["refs_following"] = list(later["refs"])
                    break

    if "''" in display(marked):
        row.flag("wiki_emphasis_left_in_text")
    if len(re.findall(r"\{\{\s*ref\s*\|", line, re.I)) != len(row.refs):
        row.flag("ref_count_mismatch")
    if not senses:
        row.flag("no_definition_in_source")
    if word[0].upper() != letter:
        row.flag("first_letter_differs_from_section")

    pos_markers = []
    for sense in senses:
        if sense["pos"] and sense["pos"] not in pos_markers:
            pos_markers.append(sense["pos"])
    note_texts = [r["text"] for r in remarks if r["kind"] != "pos"]
    literals = [r["value"] for r in remarks if r["kind"] == "literal"]
    see_also = []
    for remark in remarks:
        for target in SEE_ALSO.findall(remark["text"]):
            if target not in see_also:
                see_also.append(target)
    if len(literals) > 1:
        row.flag("several_literal_glosses")

    return OrderedDict([
        ("word", word),
        ("definitions", [s["text"] for s in senses]),
        ("pos", "; ".join(pos_markers) if pos_markers else None),
        ("notes", "; ".join(note_texts) if note_texts else None),
        ("section", letter),
        ("raw", line),
        # ---- extra detail; everything below is derived from "raw" ----
        ("line", lineno),
        ("word_forms", [collapse(w) for w in word.split(",")] if "," in word else [word]),
        ("definition_text", display(definition) if has_colon and has_text(definition) else None),
        ("senses", senses),
        ("remarks", remarks),
        ("literal", literals[0] if literals else None),
        ("see_also", see_also),
        ("refs", row.ref_names()),
        ("word_refs", row.ref_names(head_refs)),
        ("links", row.links),
        ("flags", row.flags),
    ])


# --------------------------------------------------------------------------
# Phrases:   '''Dovahzul'''{{ref}}      (line 1)
#            :"English" (literally: word word)   (line 2)
# --------------------------------------------------------------------------

def top_paren_groups(text):
    """-> [(start, end)] of bracket groups that are not inside another."""
    groups, depth, start = [], 0, -1
    for i, ch in enumerate(text):
        if ch == "(":
            if depth == 0:
                start = i
            depth += 1
        elif ch == ")" and depth:
            depth -= 1
            if depth == 0:
                groups.append((start, i + 1))
    return groups


def parse_phrase(head_line, head_no, def_line):
    row = Row()
    end = head_line.find("'''", 3)
    if end < 0:
        return None
    dovahzul = display(to_marked(head_line[3:end], row))
    if not dovahzul:
        return None
    after = to_marked(head_line[end + 3:], row)
    if has_text(after):
        row.flag("text_after_phrase")

    english, variants, literal, notes, quoted, gloss_text = None, [], None, None, False, None
    if def_line is None:
        row.flag("no_translation_line")
    else:
        text = display(to_marked(def_line[1:], row))
        gloss_text = text
        literal_span = None
        for a, b in top_paren_groups(text):
            inner = text[a + 1:b - 1].strip()
            m = LITERAL.match(inner)
            if m and inner[m.end():].strip():
                literal, literal_span = inner[m.end():].strip(), (a, b)
                break
        m = re.match(QUOTED + r"(?:\s*/\s*" + QUOTED + r")*", text)
        if m:
            quoted = True
            variants = re.findall(QUOTED, m.group(0))
            # Several quoted renderings ('"gods (of) creation" / "creator gods"'): join them
            # without their quotation marks, as meta.field_notes promises for english.
            # (Up to version 1.0.0 the quote marks were left in for this one case.)
            english = " / ".join(variants)
            remainder = text[m.end():].strip().lstrip(",").strip()
        else:
            if literal_span:
                core = collapse(text[:literal_span[0]] + " " + text[literal_span[1]:])
            else:
                core = text
            if not core or core.startswith(","):
                remainder = text          # no free translation is given
            else:
                english, variants = core, [core]
                remainder = text[literal_span[0]:literal_span[1]] if literal_span else ""
        remainder, _wrapped = strip_outer_parens(remainder)
        notes = remainder or None

    raw = head_line if def_line is None else head_line + "\n" + def_line
    return OrderedDict([
        ("dovahzul", dovahzul),
        ("english", english),
        ("notes", notes),
        ("raw", raw),
        # ---- extra detail ----
        ("line", head_no),
        ("literal", literal),
        ("english_variants", variants),
        ("english_in_quotes", quoted),
        ("translation_text", gloss_text),
        ("refs", row.ref_names()),
        ("flags", row.flags),
    ])


# --------------------------------------------------------------------------
# Names and Locations:   :'''[[Lore:Alduin|Alduin]]''': Destroyer-Devour-Master
# --------------------------------------------------------------------------

def parse_name(line, lineno, context):
    m = re.match(r"^:\s*'''", line)
    if not m:
        return None
    end = line.find("'''", m.end())
    if end < 0:
        return None
    row = Row()
    name = display(to_marked(line[m.end():end], row))
    if name.endswith(":"):
        name = name[:-1].strip()
        row.flag("colon_inside_bold")
    if not name:
        return None
    link = row.links[0] if row.links else None

    rest = display(to_marked(line[end + 3:], row))
    if rest.startswith(":"):
        rest = rest[1:].strip()

    analyses, notes = [], []
    if rest:
        for alternative in re.split(r"\s*''\s*or\s*''\s*", rest):
            alternative = alternative.strip()
            segmentation, remark = None, None
            m2 = re.match(r"^(.*?)\s*\(([^()]*)\)$", alternative)
            gloss = alternative
            if m2 and m2.group(1):
                gloss, inner = m2.group(1).strip(), m2.group(2).strip()
                if re.sub(r"[-\s]", "", inner).lower() == re.sub(r"[-\s]", "", name).lower():
                    segmentation = inner      # the name itself, cut into its words
                else:
                    remark = inner
                    notes.append(inner)
            if "''" in gloss:
                row.flag("wiki_emphasis_left_in_text")
            analyses.append(OrderedDict([
                ("meaning", gloss),
                ("parts", gloss.split("-")),
                ("segmentation", segmentation),
                ("segments", segmentation.split("-") if segmentation else None),
                ("notes", remark),
            ]))
    meaning = collapse(re.sub(r"''\s*or\s*''", "or", rest)) if rest else None
    if len(analyses) > 1:
        row.flag("several_analyses")

    return OrderedDict([
        ("name", name),
        ("meaning", meaning),
        ("parts", analyses[0]["parts"] if analyses else []),
        ("raw", line),
        # ---- extra detail ----
        ("line", lineno),
        ("group", "translated" if analyses else "untranslated"),
        ("list_intro", context),
        ("analyses", analyses),
        ("notes", "; ".join(notes) if notes else None),
        ("link_target", link["target"] if link else None),
        ("link_via", link["via"] if link else None),
        ("refs", row.ref_names()),
        ("flags", row.flags),
    ])


# --------------------------------------------------------------------------
# Reference definitions ({{ref|name=X|...}} anywhere on the page)
# --------------------------------------------------------------------------

def scan_refs(text):
    named, unnamed, i = OrderedDict(), [], 0
    while True:
        i = text.find("{{", i)
        if i < 0:
            break
        j = match_close(text, i, "{{", "}}")
        if j < 0:
            i += 2
            continue
        name, positional, named_args = parse_template(text[i:j])
        if name.lower() != "ref":
            i += 2
            continue
        record = ref_record(positional, named_args)
        lineno = text.count("\n", 0, i) + 1
        if record["name"] is None:
            unnamed.append(OrderedDict([
                ("line", lineno), ("group", record["group"]),
                ("wikitext", record["content"]),
                ("text", plain(record["content"]) if record["content"] else None),
            ]))
        else:
            slot = named.setdefault(record["name"], OrderedDict([
                ("group", None), ("wikitext", None), ("text", None), ("urls", []),
                ("defined_at_line", None), ("uses", 0), ("other_definitions", []),
            ]))
            slot["uses"] += 1
            if record["group"] and not slot["group"]:
                slot["group"] = record["group"]
            if record["content"]:
                if slot["wikitext"] is None:
                    slot["wikitext"] = record["content"]
                    slot["text"] = plain(record["content"])
                    slot["urls"] = [u.replace("{{=}}", "=") for u in
                                    re.findall(r"https?://[^\s\]|]+", record["content"])]
                    slot["defined_at_line"] = lineno
                elif record["content"] != slot["wikitext"]:
                    slot["other_definitions"].append(
                        OrderedDict([("line", lineno), ("wikitext", record["content"])]))
        i = j
    return named, unnamed


# --------------------------------------------------------------------------
# The page as a whole
# --------------------------------------------------------------------------

def parse_page(text):
    lines = text.split("\n")
    ledger = OrderedDict()              # what each line was counted as

    def count(kind):
        ledger[kind] = ledger.get(kind, 0) + 1

    # where the level-2 sections start and end
    level2 = [(i, HEADING.match(line).group(2)) for i, line in enumerate(lines)
              if HEADING.match(line) and len(HEADING.match(line).group(1)) == 2]
    bounds = OrderedDict()
    for k, (start, title) in enumerate(level2):
        stop = level2[k + 1][0] if k + 1 < len(level2) else len(lines)
        bounds[title] = (start, stop)

    def verbatim(title):
        if title not in bounds:
            return None
        start, stop = bounds[title]
        return "\n".join(lines[start:stop]).rstrip("\n")

    first = level2[0][0] if level2 else len(lines)
    lead = "\n".join(lines[:first]).rstrip("\n")

    entries, phrases, names, locations, unparsed = [], [], [], [], []
    key_intro, phrases_intro, letter_menu = [], [], None
    section2 = section3 = None
    context = None                      # last prose line before a list of names
    pending_phrase = None               # (line number, text) waiting for its ':' line

    def flush_phrase():
        nonlocal pending_phrase
        if pending_phrase is not None:
            item = parse_phrase(pending_phrase[1], pending_phrase[0], None)
            if item is None:
                unparsed.append(OrderedDict([("section", "Phrases"), ("line", pending_phrase[0]),
                                             ("raw", pending_phrase[1]), ("reason", "phrase line not understood")]))
                count("unparsed")
            else:
                phrases.append(item)
                count("phrase line")
            pending_phrase = None

    for index, line in enumerate(lines):
        lineno = index + 1
        heading = HEADING.match(line)
        if heading:
            flush_phrase()
            if len(heading.group(1)) == 2:
                section2, section3 = heading.group(2), None
            else:
                section3 = heading.group(2)
            context = None
            count("heading")
            continue
        if section2 is None:
            count("lead")
            continue
        if section2 in ("Grammar", "Notes", "References"):
            count(section2.lower() + " (kept verbatim)")
            continue
        if not line.strip():
            count("blank")
            continue

        if section2 == "Translation Key":
            if line.startswith(";"):
                entry = parse_entry(line, lineno, section3) if section3 else None
                if entry is None:
                    unparsed.append(OrderedDict([("section", "Translation Key" + ("/" + section3 if section3 else "")),
                                                 ("line", lineno), ("raw", line),
                                                 ("reason", "word row without a headword or outside a letter section")]))
                    count("unparsed")
                else:
                    entries.append(entry)
                    count("entry")
            elif TABLE_MARKUP.match(line):
                count("table markup")
            elif section3 is None and line.startswith("{{LetterMenu"):
                letter_menu = line
                count("letter menu")
            elif section3 is None:
                key_intro.append(line)
                count("translation key intro")
            else:
                unparsed.append(OrderedDict([("section", "Translation Key/" + section3), ("line", lineno),
                                             ("raw", line), ("reason", "not a ';' word row and not table markup")]))
                count("unparsed")
            continue

        if section2 == "Phrases":
            if line.startswith("'''"):
                flush_phrase()
                pending_phrase = (lineno, line)
            elif line.startswith(":") and pending_phrase is not None:
                item = parse_phrase(pending_phrase[1], pending_phrase[0], line)
                if item is None:
                    for no, raw in (pending_phrase, (lineno, line)):
                        unparsed.append(OrderedDict([("section", "Phrases"), ("line", no), ("raw", raw),
                                                     ("reason", "phrase line not understood")]))
                        count("unparsed")
                else:
                    phrases.append(item)
                    count("phrase line")
                    count("phrase translation line")
                pending_phrase = None
            elif not phrases and pending_phrase is None and not line.startswith(":"):
                phrases_intro.append(line)
                count("phrases intro")
            else:
                flush_phrase()
                unparsed.append(OrderedDict([("section", "Phrases"), ("line", lineno), ("raw", line),
                                             ("reason", "no phrase line before it, or stray text")]))
                count("unparsed")
            continue

        if section2 == "Names":
            where = "Names/Locations" if section3 == "Locations" else "Names"
            if TABLE_MARKUP.match(line):
                count("table markup")
            elif line.startswith(":"):
                item = parse_name(line, lineno, context)
                if item is None:
                    unparsed.append(OrderedDict([("section", where), ("line", lineno), ("raw", line),
                                                 ("reason", "list row without a bold name")]))
                    count("unparsed")
                elif section3 == "Locations":
                    locations.append(item)
                    count("location")
                elif section3 is None:
                    names.append(item)
                    count("name")
                else:
                    unparsed.append(OrderedDict([("section", "Names/" + section3), ("line", lineno),
                                                 ("raw", line), ("reason", "row in an unexpected sub-section")]))
                    count("unparsed")
            else:
                context = line.strip()
                count("names prose (kept verbatim)")
            continue

        unparsed.append(OrderedDict([("section", section2), ("line", lineno), ("raw", line),
                                     ("reason", "line in a section this parser does not know")]))
        count("unparsed")
    flush_phrase()

    named_refs, unnamed_refs = scan_refs(text)
    return {
        "lines": lines, "ledger": ledger, "sections": list(bounds),
        "entries": entries, "phrases": phrases, "names": names,
        "locations": locations, "unparsed": unparsed,
        "lead": lead, "key_intro": "\n".join(key_intro) or None,
        "letter_menu": letter_menu, "phrases_intro": "\n".join(phrases_intro) or None,
        "grammar": verbatim("Grammar"), "names_section": verbatim("Names"),
        "notes": verbatim("Notes"), "references": verbatim("References"),
        "named_refs": named_refs, "unnamed_refs": unnamed_refs,
    }


# --------------------------------------------------------------------------
# Checks.  independent_row_counts() deliberately shares no code with the parser.
# --------------------------------------------------------------------------

def independent_row_counts(text):
    """Count lines that start with ';' under each ===Letter=== heading, using
    nothing but two regular expressions on the raw text."""
    start = re.search(r"(?m)^==\s*Translation Key\s*==\s*$", text)
    stop = re.search(r"(?m)^==\s*Phrases\s*==\s*$", text)
    key = text[start.end():stop.start()] if start and stop else ""
    pieces = re.split(r"(?m)^===\s*(.+?)\s*===\s*$", key)
    counts = OrderedDict()
    counts["(before first letter)"] = len(re.findall(r"(?m)^;", pieces[0]))
    for k in range(1, len(pieces), 2):
        counts[pieces[k]] = counts.get(pieces[k], 0) + len(re.findall(r"(?m)^;", pieces[k + 1]))
    return counts, len(re.findall(r"(?m)^;", text))


def run_checks(text, page):
    """-> (report lines, problems, warnings, entries per letter).
    A problem means the parse cannot be trusted and nothing is written.
    A warning is something a person should look at; the file is still written."""
    problems, warnings, report = [], [], []
    raw_counts, all_semicolon_lines = independent_row_counts(text)
    first = "(before first letter)"
    parsed_counts, unparsed_counts = OrderedDict(), {}
    for entry in page["entries"]:
        parsed_counts[entry["section"]] = parsed_counts.get(entry["section"], 0) + 1
    for item in page["unparsed"]:
        if item["raw"].startswith(";") and item["section"].startswith("Translation Key"):
            letter = item["section"].partition("/")[2] or first
            unparsed_counts[letter] = unparsed_counts.get(letter, 0) + 1

    report.append("Rows per letter: lines starting with ';' in the raw wikitext vs what the parser kept")
    report.append("  %-8s %5s %8s %9s" % ("letter", "raw", "entries", "unparsed"))
    letters = [k for k in raw_counts if k != first or raw_counts[k]]
    for letter in letters + [k for k in parsed_counts if k not in raw_counts]:
        raw_n, parsed_n = raw_counts.get(letter, 0), parsed_counts.get(letter, 0)
        unparsed_n = unparsed_counts.get(letter, 0)
        ok = raw_n == parsed_n + unparsed_n
        report.append("  %-8s %5d %8d %9d  %s" % (letter, raw_n, parsed_n, unparsed_n, "ok" if ok else "MISMATCH"))
        if not ok:
            problems.append("letter %s: %d raw rows but %d entries + %d unparsed"
                            % (letter, raw_n, parsed_n, unparsed_n))
    raw_total = sum(raw_counts.values())
    unparsed_rows = sum(unparsed_counts.values())
    total_ok = raw_total == len(page["entries"]) + unparsed_rows
    report.append("  %-8s %5d %8d %9d  %s" % ("total", raw_total, len(page["entries"]), unparsed_rows,
                                              "ok" if total_ok else "MISMATCH"))
    if not total_ok:
        problems.append("%d raw rows in the Translation Key, %d entries + %d unparsed rows"
                        % (raw_total, len(page["entries"]), unparsed_rows))
    if all_semicolon_lines != raw_total:
        warnings.append("%d lines start with ';' on the whole page but only %d are in the Translation Key"
                        % (all_semicolon_lines, raw_total))
    if page["unparsed"]:
        warnings.append("%d line(s) were not understood and are kept in \"unparsed\"" % len(page["unparsed"]))
    report.append("  ';' lines on the whole page: %d (outside the Translation Key: %d)"
                  % (all_semicolon_lines, all_semicolon_lines - raw_total))

    # every line of the page was counted exactly once
    ledger_total = sum(page["ledger"].values())
    if ledger_total != len(page["lines"]):
        problems.append("line ledger covers %d lines, page has %d" % (ledger_total, len(page["lines"])))

    # raw rows are exact lines of the source, in source order
    lines = page["lines"]
    last = 0
    for entry in page["entries"]:
        if lines[entry["line"] - 1] != entry["raw"]:
            problems.append("entry %r: raw differs from source line %d" % (entry["word"], entry["line"]))
        if entry["line"] <= last:
            problems.append("entry %r is out of source order" % entry["word"])
        last = entry["line"]
        # number of {{ref}} templates in the row == number the parser saw
        if "ref_count_mismatch" in entry["flags"]:
            problems.append("entry %r: not every {{ref}} of the row was recognised" % entry["word"])
        # every word of every definition can be found in the raw row
        for definition in entry["definitions"]:
            for token in re.findall(r"[A-Za-z']+", definition):
                if token not in entry["raw"]:
                    problems.append("entry %r: %r is not in the raw row" % (entry["word"], token))
        if not entry["raw"].startswith(";" + entry["word"].split(",")[0].split("(")[0][:3]):
            problems.append("entry %r: headword does not start the raw row" % entry["word"])

    # the phrases and names found match a plain count of their rows
    def section_text(title, nxt):
        a = re.search(r"(?m)^==\s*%s\s*==\s*$" % re.escape(title), text)
        b = re.search(r"(?m)^==\s*%s\s*==\s*$" % re.escape(nxt), text)
        return text[a.end():b.start()] if a and b else ""

    phrase_rows = len(re.findall(r"(?m)^'''", section_text("Phrases", "Names")))
    names_text = section_text("Names", "Notes")
    names_part, _sep, locations_part = names_text.partition("===Locations===")
    name_rows = len(re.findall(r"(?m)^:\s*'''", names_part))
    location_rows = len(re.findall(r"(?m)^:\s*'''", locations_part))
    report.append("Phrases  : %d bold phrase lines in the raw text, %d parsed" % (phrase_rows, len(page["phrases"])))
    report.append("Names    : %d bold list rows in the raw text, %d parsed" % (name_rows, len(page["names"])))
    report.append("Locations: %d bold list rows in the raw text, %d parsed" % (location_rows, len(page["locations"])))

    def kept_elsewhere(section):
        return sum(1 for u in page["unparsed"] if u["section"] == section
                   and re.match(r"^(:\s*)?'''", u["raw"]))

    for label, raw_n, parsed, section in (
            ("phrases", phrase_rows, page["phrases"], "Phrases"),
            ("names", name_rows, page["names"], "Names"),
            ("locations", location_rows, page["locations"], "Names/Locations")):
        if raw_n != len(parsed) + kept_elsewhere(section):
            problems.append("%s: %d rows in the raw text, %d parsed + %d unparsed"
                            % (label, raw_n, len(parsed), kept_elsewhere(section)))
    return report, problems, warnings, parsed_counts


def print_samples(entries, how_many, seed):
    rng = random.Random(seed)
    chosen = rng.sample(entries, min(how_many, len(entries)))
    print("\n%d random entries beside their raw rows (seed %s)" % (len(chosen), seed))
    for entry in sorted(chosen, key=lambda e: e["line"]):
        print("-" * 78)
        print("raw  (line %d): %s" % (entry["line"], entry["raw"]))
        print("  word       : %s" % json.dumps(entry["word"], ensure_ascii=False))
        print("  definitions: %s" % json.dumps(entry["definitions"], ensure_ascii=False))
        print("  pos        : %s" % json.dumps(entry["pos"], ensure_ascii=False))
        print("  notes      : %s" % json.dumps(entry["notes"], ensure_ascii=False))
        print("  section    : %s   refs: %s   flags: %s"
              % (entry["section"], ", ".join(entry["refs"]) or "-", ", ".join(entry["flags"]) or "-"))
    print("-" * 78)


FIELD_NOTES = OrderedDict([
    ("word", "The headword exactly as written before the first colon of the row. A row that lists "
             "several spellings (\"Bahlaan, Balaan\") or an optional ending (\"Kel(le)\") is kept as one "
             "string; word_forms only cuts it at commas and changes nothing else."),
    ("definitions", "The glosses of the row, cut at top-level commas and slashes, with reference tags "
                    "removed and trailing bracketed or small-print remarks moved to notes/pos. Leading "
                    "or embedded brackets are part of the gloss and stay (\"(Great) Victory\", "
                    "\"Savage(s)\"). Empty when the source gives the word without a meaning. "
                    "definition_text is the same text before cutting."),
    ("pos", "Only what the source states, in the source's own spelling (\"v.\", \"verb\", \"adj.\"). "
            "Several markers on one row are joined with '; '. A marker belongs to the gloss it follows; "
            "senses[].pos says which one. The source may mean it for neighbouring glosses too."),
    ("notes", "Bracketed and small-print remarks of the row, joined with '; ' in source order. "
              "remarks[] holds them one by one with their kind (note, literal, see_also, pos), the "
              "markup they came in, their own references and the sense they follow."),
    ("section", "The letter heading (===A===) the row stands under."),
    ("raw", "The exact source line. For a phrase: its two lines joined with a newline."),
    ("senses", "One object per gloss: text, pos, separator_before (',' or '/' or null, so the source's "
               "grouping can be rebuilt), refs (the reference tags placed directly after this gloss) "
               "and refs_following (for a gloss with no tag of its own, the tags after the next gloss "
               "that has some, as in \"Flow, Fly, Move{{ref}}\"). Reading refs_following as covering "
               "the earlier glosses is an inference; the page does not say so."),
    ("refs", "Names of all {{ref}} tags on the row, in order; this is the field to use for 'is this row "
             "sourced at all'. An entry with no refs is unsourced on the wiki page. ref_definitions maps "
             "each name to the source it stands for (wikitext = as written, text = a plain reading of "
             "it, uses = how often the tag occurs on the whole page)."),
    ("flags", "Things a reader of this file should know about the row, e.g. no_definition_in_source, "
              "template_vn (the wiki's {{vn}} marker follows the row), usage_statement_kept_as_note."),
    ("names", "name = the bold name; meaning = the text after it with ''or'' written as or; parts = the "
              "hyphen-separated English parts of the FIRST analysis; analyses[] has every analysis the "
              "source lists, with the name's own segmentation where the source gives one. Rows with no "
              "meaning are the names the page lists as untranslated (group = untranslated)."),
    ("phrases", "english = the free translation without its quotation marks, or null when the source "
                "gives only a literal reading; literal = the text after 'literally:'; notes = whatever "
                "else the translation line says, in source order; translation_text = the whole line "
                "without reference tags."),
    ("verbatim", "lead_wikitext, grammar_wikitext, names_section_wikitext, notes_wikitext and "
                 "references_wikitext are exact slices of the page (a section starts at its == heading "
                 "line); only trailing newlines are trimmed."),
    ("status", "This file records what the wiki page says. It does not say which facts are canon: use "
               "refs and ref_definitions (game dialogue, Word Walls, official guide, developer "
               "dictionary, ...) to decide that."),
])


def build_output(page, manifest, sha256, parsed_counts):
    untranslated = sum(1 for n in page["names"] if n["group"] == "untranslated")
    per_ref, only_ref = {}, {}
    for entry in page["entries"]:
        for name in entry["refs"]:
            per_ref[name] = per_ref.get(name, 0) + 1
        if len(entry["refs"]) == 1:
            only_ref[entry["refs"][0]] = only_ref.get(entry["refs"][0], 0) + 1
    by_count = lambda table: OrderedDict(sorted(table.items(), key=lambda kv: (-kv[1], kv[0])))
    counts = OrderedDict([
        ("entries", len(page["entries"])),
        ("entries_per_section", parsed_counts),
        ("entries_without_definition", sum(1 for e in page["entries"] if not e["definitions"])),
        ("entries_with_pos", sum(1 for e in page["entries"] if e["pos"])),
        ("entries_without_refs", sum(1 for e in page["entries"] if not e["refs"])),
        ("entries_with_several_spellings", sum(1 for e in page["entries"] if len(e["word_forms"]) > 1)),
        ("entries_citing_each_ref", by_count(per_ref)),
        ("entries_citing_only_this_ref", by_count(only_ref)),
        ("phrases", len(page["phrases"])),
        ("names", len(page["names"])),
        ("names_translated", len(page["names"]) - untranslated),
        ("names_untranslated", untranslated),
        ("locations", len(page["locations"])),
        ("unparsed", len(page["unparsed"])),
        ("named_references", len(page["named_refs"])),
        ("source_lines", len(page["lines"])),
        ("source_line_ledger", page["ledger"]),
    ])
    meta = OrderedDict([
        ("source", "UESP, The Unofficial Elder Scrolls Pages (en.uesp.net), via its MediaWiki API"),
        ("page", manifest.get("title")),
        ("revid", manifest.get("revid")),
        ("timestamp", manifest.get("timestamp")),
        ("license", manifest.get("license")),
        ("generated_by", "tools/ingest/parse_lexicon.py %s (input saved by tools/ingest/fetch_lexicon.py)"
                         % PARSER_VERSION),
        ("license_url", manifest.get("license_url")),
        ("license_deed_url", manifest.get("license_deed_url")),
        ("page_url", manifest.get("page_url")),
        ("permalink", manifest.get("permalink")),
        ("api_url", manifest.get("api_url")),
        ("source_file", manifest.get("saved_as")),
        ("source_sha256", sha256),
        ("reproduce", ["python3 tools/ingest/fetch_lexicon.py --revid %s" % manifest.get("revid"),
                       "python3 tools/ingest/parse_lexicon.py --sample 15"]),
        ("sections_on_page", page["sections"]),
        ("letter_menu", page["letter_menu"]),
        ("counts", counts),
        ("field_notes", FIELD_NOTES),
    ])
    undefined = [name for name, slot in page["named_refs"].items() if slot["wikitext"] is None]
    return OrderedDict([
        ("meta", meta),
        ("entries", page["entries"]),
        ("phrases", page["phrases"]),
        ("names", page["names"]),
        ("locations", page["locations"]),
        ("unparsed", page["unparsed"]),
        ("grammar_wikitext", page["grammar"]),
        ("notes_wikitext", page["notes"]),
        ("references_wikitext", page["references"]),
        # ---- extra detail ----
        ("lead_wikitext", page["lead"]),
        ("translation_key_intro_wikitext", page["key_intro"]),
        ("phrases_intro_wikitext", page["phrases_intro"]),
        ("names_section_wikitext", page["names_section"]),
        ("ref_definitions", page["named_refs"]),
        ("unnamed_refs", page["unnamed_refs"]),
        ("refs_used_but_not_defined", undefined),
    ])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--wikitext", type=Path, default=WIKITEXT)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--out", type=Path, default=OUTPUT)
    parser.add_argument("--sample", type=int, default=0, metavar="N",
                        help="print N random entries beside their raw rows")
    parser.add_argument("--seed", default="dovahzul",
                        help="seed for --sample (default: %(default)s)")
    parser.add_argument("--check-only", action="store_true", help="run the checks, write nothing")
    args = parser.parse_args(argv)

    raw_bytes = args.wikitext.read_bytes()
    text = raw_bytes.decode("utf-8")
    sha256 = hashlib.sha256(raw_bytes).hexdigest()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))

    problems = []
    if manifest.get("sha256") != sha256:
        problems.append("the wikitext file does not match the sha256 in its provenance record")
    if any(mark in text for mark in (REF_OPEN, REF_CLOSE, SMALL_OPEN, SMALL_CLOSE)):
        problems.append("the source contains a private-use character this parser uses as a marker")
    if "\r" in text:
        problems.append("the source contains carriage returns")

    page = parse_page(text)
    report, check_problems, warnings, parsed_counts = run_checks(text, page)
    problems.extend(check_problems)
    output = build_output(page, manifest, sha256, parsed_counts)
    counts = output["meta"]["counts"]

    print("page     : %s  revision %s  %s" % (manifest.get("title"), manifest.get("revid"), manifest.get("timestamp")))
    print("licence  : %s" % manifest.get("license"))
    print("source   : %d lines, sha256 %s" % (len(page["lines"]), sha256))
    print()
    print("\n".join(report))
    print()
    print("entries  : %d  (without a definition: %d, with a stated part of speech: %d, without refs: %d)"
          % (counts["entries"], counts["entries_without_definition"],
             counts["entries_with_pos"], counts["entries_without_refs"]))
    print("phrases  : %d" % counts["phrases"])
    print("names    : %d  (translated %d, untranslated %d)"
          % (counts["names"], counts["names_translated"], counts["names_untranslated"]))
    print("locations: %d" % counts["locations"])
    print("unparsed : %d" % counts["unparsed"])
    for item in page["unparsed"]:
        print("   line %d [%s] %s: %s" % (item["line"], item["section"], item["reason"], item["raw"]))
    print("refs     : %d named, %d unnamed, %d used but never defined"
          % (len(page["named_refs"]), len(page["unnamed_refs"]), len(output["refs_used_but_not_defined"])))
    print("line ledger:")
    for kind, number in page["ledger"].items():
        print("   %5d  %s" % (number, kind))
    print("   %5d  lines in all (the page has %d)" % (sum(page["ledger"].values()), len(page["lines"])))

    if args.sample:
        print_samples(page["entries"], args.sample, args.seed)

    for warning in warnings:
        print("\nwarning: " + warning)
    if problems:
        print("\nCHECKS FAILED, nothing written:", file=sys.stderr)
        for problem in problems:
            print("  - " + problem, file=sys.stderr)
        return 1
    print("\nall checks passed")

    if not args.check_only:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
        args.out.write_text(payload, encoding="utf-8")
        try:
            shown = args.out.resolve().relative_to(REPO_ROOT).as_posix()
        except ValueError:
            shown = str(args.out)
        print("wrote    : %s (%d bytes, sha256 %s)"
              % (shown, len(payload.encode("utf-8")), hashlib.sha256(payload.encode("utf-8")).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
