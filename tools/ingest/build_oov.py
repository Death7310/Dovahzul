#!/usr/bin/env python3
"""List every corpus token that is not a headword of the canon lexicon.

Standard library only.  Reads

    research/data/canon-lexicon.json   (headwords, names, phrases)
    research/data/canon-corpus.json    (the dragon-language texts)
    research/data/canon-shouts.json    (word meanings stated for shout words)

and writes

    research/data/corpus-oov.json

Run from the repository root:

    python3 tools/ingest/build_oov.py            # write the file, print a summary
    python3 tools/ingest/build_oov.py --check    # print the summary, write nothing

Nothing is fetched and nothing is translated.  The output is deterministic:
two runs over the same inputs give the same bytes.

Method
  1. Tokens.  The "dovahzul" field of every corpus record is lower-cased and cut
     into runs of letters; an apostrophe inside a word stays (thu'um, zu'u),
     a hyphen separates tokens (Tiid-Ahraan -> tiid, ahraan).  For dialogue the
     field holds only the dragon-language segments of the line.
  2. Headwords.  Every spelling in entries[].word_forms of the lexicon, lower-
     cased; "Kel(le)" counts as kel and kelle; "Vo..." counts as vo.
  3. Documented patterns.  A token that is not a headword is "explained" when it
     follows a rule the dictionary page states in its Grammar section:
       plural       last letter doubled + e          kel  -> kelle
       possessive   + i  (+ l after ii)              thur -> thuri
       our          + u                              bormah -> bormahu
       perfect      + aan                            mah  -> mahlaan is NOT this
                                                     rule (it needs an extra l);
                                                     only stem + aan counts
       compound     two to four headwords (or forms explained above) written
                    together, e.g. sille + se + joor
     Names are never "explained" this way: a name stays in the list, with its
     compound reading shown beside it.
  4. Classes.  Each remaining token gets one class, by the first test that holds
     (see CLASS_NOTES).  Tests 1 to 5 are mechanical; MANUAL holds the reviewer's
     reading of the few tokens no test decides, each with its evidence.

Every class is a best reading, not a ruling: "likely lexicon omission" means the
wiki gives the word a meaning somewhere but its dictionary page has no row for it.
"""
import argparse
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research" / "data"
OUT = DATA / "corpus-oov.json"

TOKEN = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")

CLASS_NOTES = OrderedDict([
    ("name",
     "A proper name: a dragon, dragon priest or place name listed in the Names section of the "
     "dictionary page, a name the corpus records with a wiki-stated meaning, or a word that the "
     "wiki's English translation of the same text carries over unchanged (people and places "
     "named on word walls)."),
    ("spelling variant or error",
     "Differs from a headword, or from another corpus token that is explained, by one letter, "
     "one swapped pair, a dropped apostrophe or a doubled letter; or the wiki itself marks it "
     "{{sic}}. Usually a typo in the game text or on the wiki, or another official spelling."),
    ("inflected or derived form (pattern not in the grammar section)",
     "A headword plus an ending that the dictionary page's Grammar section does not describe "
     "but that the corpus attests, e.g. the possessive -ii (Thu'umii 'his Voice')."),
    ("likely lexicon omission (meaning stated on the wiki)",
     "Not a headword and not derivable from one, but a wiki page states a meaning for it: a "
     "hover gloss on a one-word segment, a word-by-word shout meaning, a phrase entry on the "
     "dictionary page, or a sentence on a name page."),
    ("word of another language inside dragon text",
     "English (or other) wording that stands inside an official dragon-language text."),
    ("unclassified",
     "No test decides it. Either a lexicon omission whose meaning the wiki only gives inside a "
     "longer translation, or an error."),
])

# Reviewer's readings (verification pass, 2026-11-14) for tokens the mechanical tests cannot
# decide or decide wrongly.  token -> (class, evidence).  Each was checked against the raw
# wikitext of the page named.
MANUAL = {
    "moron": ("spelling variant or error",
              "Lore:Dragon Language: Myth no More, passage 1, prints 'moron au' where the wall "
              "itself (Skyrim:Aura Whisper, wall 2) reads MORO NAU ('glory on'): a word-division "
              "slip in the book text as the wiki gives it. The 'au' that follows it counts as "
              "the headword Au in this file."),
    "kfir": ("spelling variant or error",
             "Blades:Shulkunaak writes 'Kfir voth ahkrin'; Blades:Facing the Dragon gives the "
             "same line as 'Krif voth ahkrin' (Krif 'Fight' is a headword)."),
    "dovah's": ("word of another language inside dragon text",
                "English possessive 's on the headword Dovah, in the official ESO style name "
                "\"Dovah's Du'ul\" (Online:Dovah's Du'ul Style)."),
    "men": ("unclassified",
            "Skyrim:Anniversary Edition quotes the cover text 'Naal Thuum Zeim Men Eruvos' with "
            "the wiki's reading '(by shout through many years)'; 'men' stands where 'many' "
            "stands in that reading, but the page states no word-by-word meaning. The headword "
            "for 'many' on the dictionary page is Pogaan."),
    "di": ("spelling variant or error",
           "Skyrim:Alduin prints 'Di kiirre fen alok.' with the hover gloss 'My children will "
           "rise.'; the headword for 'my' is Dii."),
    "zil": ("spelling variant or error",
            "Skyrim:Alduin prints 'zil gro dovah ulse!' in one place and 'ziil gro dovah ulse!' "
            "in another; Ziil is the headword."),
    "ri": ("spelling variant or error",
           "SkyrimVSE:Combat spells the Soul Tear shout 'Ri Vaaz Zoll'; the Skyrim shout page "
           "has Rii Vaaz Zol."),
    "zoll": ("spelling variant or error",
             "SkyrimVSE:Combat spells the Soul Tear shout 'Ri Vaaz Zoll'; the Skyrim shout page "
             "has Rii Vaaz Zol."),
    "tuum": ("unclassified",
             "Skyrim:High Hrothgar gives the banner text 'THUUM TUUM' and says the banners cannot "
             "be translated completely. Tu 'Hammer' + Um 'Twin' is a possible cut but nothing on "
             "the wiki supports it."),
    "mere": ("unclassified",
             "Skyrim:Paarthurnax (dragon): 'Ni liivrah hin mere. True, this is not the final "
             "krongah - victory.' The wiki glosses no word of the sentence; Liiv 'Wither' and "
             "Hin 'Your' are headwords, 'mere' is not."),
}


def norm_token(tok):
    return tok.lower().replace("’", "'")


def tokens_of(text):
    return [norm_token(t) for t in TOKEN.findall(text or "")]


def load(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return json.load(fh)


def headword_forms(lexicon):
    """-> {form: [headword as written, ...]}"""
    forms = {}
    for e in lexicon["entries"]:
        for w in e["word_forms"]:
            m = re.fullmatch(r"([^()]+)\(([^()]+)\)", w)
            spellings = [m.group(1), m.group(1) + m.group(2)] if m else [w]
            for sp in spellings:
                for part in tokens_of(sp):
                    forms.setdefault(part, [])
                    if e["word"] not in forms[part]:
                        forms[part].append(e["word"])
    return forms


def inflection(tok, heads):
    """-> (rule, stem) when tok is a documented inflection of a headword, else None."""
    if len(tok) >= 4 and tok[-1] == "e" and tok[-2] == tok[-3] and tok[:-2] in heads:
        return ("plural: last letter doubled + e", tok[:-2])
    if tok.endswith("aan") and len(tok) >= 5 and tok[:-3] in heads:
        return ("perfect: + aan", tok[:-3])
    if tok.endswith("l") and tok[:-1].endswith("ii") and tok[:-1] in heads:
        return ("possessive after ii: + l", tok[:-1])
    if tok.endswith("i") and tok[:-1] in heads and len(tok) > 3:
        return ("possessive: + i", tok[:-1])
    if tok.endswith("u") and tok[:-1] in heads and len(tok) > 3:
        return ("our: + u", tok[:-1])
    return None


def compound_readings(tok, heads, max_parts=4, inflected_parts=True):
    """-> every way to cut tok into two to max_parts parts, best first.

    A part has at least two letters and is a headword or (if inflected_parts) a documented
    inflection of one.  Order: fewest inflected parts, then fewest two-letter parts (the
    linking word "se" not counted), then fewest parts, then longest first part.
    """
    found = []

    def part_ok(p):
        return len(p) >= 2 and (p in heads or (inflected_parts and inflection(p, heads) is not None))

    def walk(rest, parts):
        if not rest:
            if len(parts) >= 2:
                found.append(list(parts))
            return
        if len(parts) == max_parts:
            return
        for cut in range(len(rest), 1, -1):
            head = rest[:cut]
            if part_ok(head):
                parts.append(head)
                walk(rest[cut:], parts)
                parts.pop()

    walk(tok, [])
    found.sort(key=lambda ps: (sum(1 for x in ps if x not in heads),
                               sum(1 for x in ps if len(x) <= 2 and x != "se"),
                               len(ps), -len(ps[0])))
    return found


def compound(tok, heads):
    """-> the best reading that explains tok as a compound, or None.

    A reading made only of two-letter headwords (plus "se") is not accepted: with some
    thirty-five two-letter headwords such a cut is too easily a coincidence (tu + um).
    """
    for parts in compound_readings(tok, heads):
        if any(len(x) > 2 for x in parts):
            return parts
        return None
    return None


def one_edit(a, b):
    """True when a and b differ by one substitution, insertion, deletion or adjacent swap."""
    if a == b:
        return False
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if la == lb:
        diff = [i for i in range(la) if a[i] != b[i]]
        if len(diff) == 1:
            return True
        return len(diff) == 2 and diff[1] == diff[0] + 1 and \
            a[diff[0]] == b[diff[1]] and a[diff[1]] == b[diff[0]]
    if la > lb:
        a, b = b, a
    return any(b[:i] + b[i + 1:] == a for i in range(len(b)))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="print the summary, write nothing")
    args = ap.parse_args()

    lexicon, corpus, shouts = load("canon-lexicon.json"), load("canon-corpus.json"), \
        load("canon-shouts.json")
    heads = headword_forms(lexicon)

    # ---- names the dictionary page and the corpus know
    names = {}                                   # token -> basis

    def add_name(tok, basis):
        names.setdefault(tok, basis)

    for group, label in (("names", "Names section"), ("locations", "Locations list")):
        for n in lexicon[group]:
            for tok in tokens_of(n["name"]):
                add_name(tok, "listed in the %s of Lore:Dragon Language%s" % (
                    label, (" with the meaning '%s'" % n["meaning"]) if n.get("meaning") else
                    " (as untranslated)"))
    for m in re.finditer(r"\|([A-Z][a-z]+)\]\]\s*(?:\(([^)]+)\))?", lexicon["names_section_wikitext"]):
        if m.group(1) in ("Ahkahtuz", "Toshrakhat"):
            add_name(m.group(1).lower(), "named in the prose of the Names section of "
                     "Lore:Dragon Language as a dragon name granted to a mortal")
    for t in corpus["texts"]:
        if t["type"] != "name":
            continue
        whole = re.sub(r"\s*\(.*\)\s*$", "", t["dovahzul"]).strip()
        toks = tokens_of(whole)
        if len(toks) == 1 and whole[:1].isupper() and "name" in (t.get("notes") or "").lower() \
                + (t.get("canon_status") or "").lower() and toks[0] not in heads:
            add_name(toks[0], "name with a wiki-stated meaning on %s: '%s'" % (
                t["source_page"], t.get("english")))

    # ---- stated meanings for single words (evidence for 'likely lexicon omission')
    stated = {}                                  # token -> [text, ...]

    def add_stated(tok, text):
        stated.setdefault(tok, [])
        if text not in stated[tok]:
            stated[tok].append(text)

    for s in shouts["shouts"]:
        for w in s.get("words") or []:
            if w.get("meaning"):
                add_stated(norm_token(w["word"]), "shout word '%s' = '%s' (%s, %s)" % (
                    w["word"], w["meaning"], s.get("name") or s.get("phrase"), s["source_page"]))
    for t in corpus["texts"]:
        for seg in t.get("segments") or []:
            toks = tokens_of(seg["dovahzul"])
            if len(toks) == 1 and seg.get("english"):
                add_stated(toks[0], "glossed '%s' on %s (%s)" % (
                    seg["english"], t["source_page"], seg.get("gloss") or "wiki gloss"))
        if t["type"] in ("name", "other") and t.get("english"):
            toks = tokens_of(t["dovahzul"])
            if len(toks) == 1:
                add_stated(toks[0], "'%s' on %s" % (t["english"], t["source_page"]))
    for ph in lexicon["phrases"]:
        toks = tokens_of(ph["dovahzul"])
        lit = re.split(r"[\s_\-]+", ph["literal"]) if ph.get("literal") else []
        if lit and len(lit) == len(toks) and "_" not in ph["literal"]:
            for tok, word in zip(toks, lit):
                add_stated(tok, "phrase '%s' on Lore:Dragon Language, literal reading '%s' "
                           "(this word: '%s')" % (ph["dovahzul"], ph["literal"], word))
        elif ph.get("literal") or ph.get("english"):
            for tok in toks:
                if tok not in heads:
                    stated.setdefault(tok, [])
                    stated[tok].append("in the phrase '%s' on Lore:Dragon Language (%s)" % (
                        ph["dovahzul"], ph.get("translation_text")))

    for group in ("names", "locations"):
        for n in lexicon[group]:
            for an in n.get("analyses") or []:
                segs, parts = an.get("segments") or [], an.get("parts") or []
                if segs and len(segs) == len(parts):
                    for seg, part in zip(segs, parts):
                        if norm_token(seg) not in heads:
                            add_stated(norm_token(seg), "segment '%s' = '%s' in the analysis of the "
                                       "name %s (%s) on Lore:Dragon Language"
                                       % (seg, part, n["name"], an.get("segmentation")))

    # ---- words the wiki itself marks {{sic}}
    sic = {}
    for t in corpus["texts"]:
        for kept, fixed in re.findall(r'sic: wiki keeps "([^"]+)" and notes the correction "([^"]+)"',
                                      t.get("notes") or ""):
            sic.setdefault(norm_token(kept), (fixed, t["source_page"]))

    # ---- meanings of headwords, to recognise a stated meaning that repeats a headword's
    head_defs = {}
    for e in lexicon["entries"]:
        for w in e["word_forms"]:
            for part in tokens_of(re.sub(r"\(.*?\)", "", w)):
                head_defs.setdefault(part, set()).update(d.lower() for d in e["definitions"])

    # ---- count tokens
    count, count_unique, where, seen_as = Counter(), Counter(), {}, {}
    english_of = {}                              # token -> set of record ids whose English has it
    total = 0
    for t in corpus["texts"]:
        eng_raw = re.findall(r"[^\W\d_]+(?:['’][^\W\d_]+)*", (t.get("english") or ""))
        eng_words = set(w.lower() for w in eng_raw)
        eng_words |= set(w.replace("'", "") for w in eng_words)
        eng_caps = dict((w.lower(), w) for w in eng_raw if w[:1].isupper() and len(w) >= 5)
        for raw in TOKEN.findall(t["dovahzul"] or ""):
            tok = norm_token(raw)
            total += 1
            count[tok] += 1
            if not t.get("duplicate_of"):
                count_unique[tok] += 1
            where.setdefault(tok, [])
            if t["id"] not in where[tok]:
                where[tok].append(t["id"])
            seen_as.setdefault(tok, [])
            if raw not in seen_as[tok]:
                seen_as[tok].append(raw)
            if tok in eng_words and len(tok) > 2:
                english_of.setdefault(tok, []).append((t["id"], None))
            elif len(tok) >= 5:
                close = sorted(w for w in eng_caps if one_edit(tok, w))
                if close:
                    english_of.setdefault(tok, []).append((t["id"], eng_caps[close[0]]))

    explained_forms = set(heads)
    oov, explained = [], []
    pending = []
    for tok in sorted(count):
        if tok in heads:
            continue
        infl = inflection(tok, heads)
        comp = None if infl else compound(tok, heads)
        analysis = None
        if infl:
            analysis = OrderedDict([("rule", infl[0]), ("stem", infl[1]),
                                    ("headwords", heads[infl[1]])])
        elif comp:
            analysis = OrderedDict([("rule", "compound: headwords written together"),
                                    ("parts", comp),
                                    ("inflected_parts", [x for x in comp if x not in heads]),
                                    ("short_parts", [x for x in comp if len(x) <= 2 and x != "se"])])
        is_name = tok in names or tok in english_of
        if analysis and not is_name and tok not in MANUAL and tok not in sic:
            explained_forms.add(tok)
            explained.append((tok, analysis))
        else:
            pending.append((tok, analysis))

    inflected_class = "inflected or derived form (pattern not in the grammar section)"
    for tok, analysis in pending:
        near = sorted(h for h in heads if len(h) >= 4 and len(tok) >= 4 and one_edit(tok, h))
        near_explained = sorted(x for x in explained_forms - set(heads)
                                if len(x) >= 5 and one_edit(tok, x))
        bare = tok.replace("'", "")
        same_bare = sorted(h for h in heads if h != tok and h.replace("'", "") == bare)
        same_meaning = [h for h in near if any(
            re.search(r"(?<![a-z])%s(?![a-z])" % re.escape(d), " ".join(stated.get(tok, [])).lower())
            for d in head_defs.get(h, ()) if d)]
        stem = next((tok[:-k] for k in (1, 2, 3)
                     if len(tok) - k >= 3 and tok[:-k] in heads), None)
        if tok in MANUAL:
            cls, basis = MANUAL[tok]
            basis = "Reviewer's reading: " + basis
        elif tok in sic:
            cls = "spelling variant or error"
            basis = "the wiki marks it {{sic}} and gives the correction '%s' (%s)" % sic[tok]
        elif tok in names:
            cls, basis = "name", names[tok]
        elif tok in english_of:
            cls = "name"
            rec, close = english_of[tok][0]
            basis = ("carried over unchanged into the wiki's English for the same text (%s)" % rec
                     if close is None else
                     "the wiki's English for the same text (%s) has the name '%s', one letter "
                     "different" % (rec, close))
        elif same_bare:
            cls = "spelling variant or error"
            basis = ("the headword %s written without its apostrophe (rune text has no sign for "
                     "it)" % ", ".join("/".join(heads[h]) for h in same_bare))
        elif same_meaning:
            cls = "spelling variant or error"
            basis = ("one letter away from the headword %s, and the wiki states the same meaning "
                     "for it: %s" % (", ".join("/".join(heads[h]) for h in same_meaning),
                                     "; ".join(stated[tok][:2])))
        elif stem and (len(tok) - len(stem) == 1 or not near):
            # headword + ending.  A longer ending loses to a headword one letter away
            # (krongah is Krongrah misspelled, not Kron + gah).
            ending = tok[len(stem):]
            cls = inflected_class
            basis = "headword %s + '%s'" % ("/".join(heads[stem]), ending)
            if ending == "ii":
                basis += ("; the wiki's translations render such forms as possessives (his, her), "
                          "while the Grammar section names only + i")
            elif ending == "e":
                basis += ("; reads as a plural without the doubled letter (the plural rule would "
                          "give %s)" % (stem + stem[-1] + "e"))
        elif near_explained:
            cls = "spelling variant or error"
            basis = ("one letter away from %s, which the documented rules explain"
                     % ", ".join(near_explained))
        elif near and tok not in stated:
            cls = "spelling variant or error"
            basis = "one letter away from the headword(s) %s" % ", ".join(
                "/".join(heads[h]) for h in near)
        elif tok in stated:
            cls = "likely lexicon omission (meaning stated on the wiki)"
            basis = "; ".join(stated[tok][:4])
        else:
            cls, basis = "unclassified", "no headword, rule or stated meaning accounts for it"
        entry = OrderedDict([
            ("token", tok),
            ("as_written", seen_as[tok]),
            ("count", count[tok]),
            ("count_in_unique_texts", count_unique[tok]),
            ("texts", where[tok]),
            ("class", cls),
            ("basis", basis),
        ])
        if near and cls != "spelling variant or error":
            entry["one_letter_from_headwords"] = ["/".join(heads[h]) for h in near]
        readings = compound_readings(tok, heads, inflected_parts=False)[:5]
        if analysis and analysis["rule"].startswith(("plural", "possessive", "our", "perfect")):
            entry["reading_by_documented_rule"] = analysis
        if readings:
            entry["possible_compound_readings"] = readings
        if tok in stated and cls != "likely lexicon omission (meaning stated on the wiki)":
            entry["meanings_stated_on_the_wiki"] = stated[tok][:4]
        oov.append(entry)

    oov.sort(key=lambda e: (-e["count"], e["token"]))
    explained_out = [OrderedDict([("token", tok), ("as_written", seen_as[tok]),
                                  ("count", count[tok]),
                                  ("count_in_unique_texts", count_unique[tok]),
                                  ("texts", where[tok]), ("reading", analysis)])
                     for tok, analysis in sorted(explained, key=lambda x: (-count[x[0]], x[0]))]

    by_class = Counter(e["class"] for e in oov)
    head_tokens = sum(c for t, c in count.items() if t in heads)
    expl_tokens = sum(count[t] for t, _ in explained)
    oov_tokens = sum(e["count"] for e in oov)
    meta = OrderedDict([
        ("generator", "tools/ingest/build_oov.py"),
        ("inputs", OrderedDict([
            ("lexicon", OrderedDict([("file", "research/data/canon-lexicon.json"),
                                     ("page", lexicon["meta"]["page"]),
                                     ("revid", lexicon["meta"]["revid"])])),
            ("corpus", OrderedDict([("file", "research/data/canon-corpus.json"),
                                    ("texts", len(corpus["texts"]))])),
            ("shouts", "research/data/canon-shouts.json"),
        ])),
        ("license", corpus["meta"].get("license")),
        ("license_url", corpus["meta"].get("license_url")),
        ("attribution", corpus["meta"].get("attribution")),
        ("method", [
            "Tokens: the dovahzul field of every corpus record, lower-cased, cut into runs of "
            "letters; an apostrophe inside a word stays, a hyphen separates tokens. Dialogue "
            "records contribute only their dragon-language segments.",
            "Headwords: every spelling in entries[].word_forms of the lexicon, lower-cased; "
            "'Kel(le)' counts as kel and kelle; 'Vo...' counts as vo.",
            "explained_by_documented_rules: tokens that are not headwords but follow a pattern "
            "stated in the Grammar section of Lore:Dragon Language (plural, possessive, our, "
            "perfect) or are two to four headwords written together (compound). A compound "
            "reading is mechanical and can be a coincidence, above all when it uses two-letter "
            "headwords; such parts are listed under short_parts.",
            "oov: every other token, with one class each. Names stay in oov even when a "
            "compound reading exists. possible_compound_readings lists up to five ways to cut "
            "the token into headwords (best first: fewest two-letter parts, then fewest parts); "
            "these are mechanical and the wiki's own analysis, where it has one, is in basis.",
            "A compound made only of two-letter headwords is not accepted as an explanation "
            "(tu + um for 'tuum'): such tokens stay in oov.",
            "count = occurrences over all records; count_in_unique_texts leaves out records "
            "marked duplicate_of. texts = ids of all records the token occurs in.",
        ]),
        ("classes", CLASS_NOTES),
        ("class_order",
         "manual reading; marked {{sic}} by the wiki; name (dictionary Names/Locations, corpus "
         "name record, or carried into the English of the same text); headword without "
         "apostrophe; one letter from a headword with the same stated meaning; headword + an "
         "ending of one letter, or of two or three letters when no headword is one letter "
         "away; one letter from a rule-explained token; one letter from a headword and no "
         "stated meaning; meaning stated on the wiki; unclassified"),
        ("manual_readings", OrderedDict((k, OrderedDict([("class", v[0]), ("evidence", v[1])]))
                                        for k, v in sorted(MANUAL.items()))),
        ("counts", OrderedDict([
            ("tokens_in_corpus", total),
            ("distinct_tokens", len(count)),
            ("distinct_headword_tokens", sum(1 for t in count if t in heads)),
            ("distinct_explained_by_documented_rules", len(explained_out)),
            ("distinct_oov", len(oov)),
            ("token_occurrences", OrderedDict([("headwords", head_tokens),
                                               ("explained_by_documented_rules", expl_tokens),
                                               ("oov", oov_tokens)])),
            ("oov_by_class", OrderedDict((k, by_class.get(k, 0)) for k in CLASS_NOTES)),
            ("lexicon_headword_forms", len(heads)),
            ("lexicon_headword_forms_never_seen_in_corpus",
             sum(1 for h in heads if h not in count)),
        ])),
        ("headwords_not_in_corpus_note",
         "headwords_not_in_corpus lists the lexicon spellings that never occur as a token of "
         "their own in the corpus. Some occur only inside a longer token (ahmul in ahmulii, "
         "hadrim in hadrimme); the rest are attested only by the source the dictionary page "
         "cites for them."),
        ("caveats", [
            "Classes are best readings made by fixed tests plus a short manual list; they are not "
            "rulings on the language. 'name' in particular is decided by the English text of the "
            "same record and can be wrong for a word the translator chose to leave untranslated.",
            "A token counted as a headword can still be a different word that happens to be "
            "spelled the same (the lexicon lists several homographs).",
            "The corpus keeps the wiki's spelling, so wiki typos appear as tokens.",
        ]),
    ])
    out = OrderedDict([("meta", meta), ("oov", oov), ("explained_by_documented_rules", explained_out),
                       ("headwords_not_in_corpus", sorted(h for h in heads if h not in count))])

    print(json.dumps(meta["counts"], indent=2))
    if args.check:
        return 0
    text = json.dumps(out, ensure_ascii=False, indent=1) + "\n"
    OUT.write_text(text, encoding="utf-8")
    print("wrote %s (%d bytes)" % (OUT.relative_to(ROOT), len(text.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
