#!/usr/bin/env python3
"""Empirical phonotactics and rune-spelling statistics of canon Dovahzul.

Reads the canon data files in research/data/ and writes
research/data/canon-phonotactics.json. Standard library only; the output is
deterministic (no timestamp), so a second run gives the same bytes.

    python3 tools/analysis/phonotactics.py            # from the repository root
    python3 tools/analysis/phonotactics.py --check    # recompute and compare, write nothing

What is counted, and how
------------------------
The language is attested in writing only. Everything here is therefore a
statement about SPELLING: "onset", "coda" and "syllable" are orthographic
constructs built by the fixed rules below, not transcriptions of the voice
acting. The rules are meant to be simple enough to re-implement in the app.

1. Word sets
   lexicon      every spelling in entries[].word_forms of canon-lexicon.json.
                "Kel(le)" counts as kel (the bracket is a plural ending);
                "Ro(h)" as ro and roh; "Vo..." as vo; a hyphenated row is cut
                at the hyphen. A spelling the page itself calls a typo
                (Miraad, Pahklok) is left out.
   shout words  distinct words of power in canon-shouts.json.
   dragon names the Names list of the dictionary page (translated group).
   corpus       tokens of canon-corpus.json records that are not duplicates,
                not of type "name", and whose canon_status starts with "canon";
                tokens that corpus-oov.json classes as a name, a spelling
                variant or error, or a word of another language are left out.

2. Units (graphemes)
   u'u                      one vowel unit (rune text writes it as the UU rune)
   aa ei ey ii oo uu        one vowel unit each (each is one rune)
   au ae                    one vowel unit each (written with two runes;
                            treated as diphthongs: nau, mahfaeraak)
   Vh  (ah eh ih oh uh)     one vowel unit when the h ends the word or stands
                            before a consonant; "ah" (a rune of its own) also
                            before a vowel. Otherwise h is a consonant.
   th sh                    one consonant unit each (two runes; no rune of
                            their own)
   qu before a vowel        one consonant unit (only in Quethsegol)
   y                        consonant, except in ey
   ir ur                    NOT units here: counted as vowel + r. Their use as
                            runes is reported under rune_spelling.
   every other letter       one unit

3. Syllables
   Every vowel unit is one nucleus. A consonant run between two nuclei is
   divided by the maximal-onset rule: the longest tail of the run that occurs
   as a word-initial onset in the lexicon goes to the following syllable, the
   rest closes the preceding one; a single consonant always goes to the
   following syllable.

4. "Mechanically decomposable"
   A lexicon word that can be cut into two to four other lexicon words, each
   of at least three letters (the linker "se" is also allowed between parts).
   This is a string test, not an etymology: it over-detects (bahlok = bah +
   lok). Its complement is a conservative set of single-morpheme words.

5. Forge profile (added in 1.1.0)
   A summary for a rule-based word validator, counted over the
   not-decomposable words only so that compound junctures do not pass as
   clusters. Onsets, codas and nuclei get a tier by type count: core (5 or
   more words), marginal (2 to 4), single (1). final_rime crosses the class
   of the last nucleus with the length of the word-final coda.
   wordlikeness_model is a unit-bigram model with word boundaries and add-k
   smoothing; a word's score is its mean log2 transition probability. Scores
   of the training words are leave-one-out (the word's own bigrams are
   removed first), so the percentiles say how a NEW word of the same kind
   would score. The control strings are an illustration, not a test set.
"""

import argparse
import collections
import hashlib
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "research", "data")
OUT = os.path.join(DATA, "canon-phonotactics.json")

VERSION = "1.1.0"
EXAMPLES = 6

SINGLE_VOWELS = set("aeiou")
VOWEL_DIGRAPHS = ("aa", "ei", "ey", "ii", "oo", "uu")
DIPHTHONGS = ("au", "ae")
CONS_DIGRAPHS = ("th", "sh")
RUNE_DIGRAPHS = ("aa", "ah", "ei", "ey", "ii", "ir", "oo", "uu", "ur")
SEMI_CANON_REFS = {"Prima", "TIL", "BN", "DBgamedata"}
LETTERS = "abcdefghijklmnopqrstuvwxyz"


# --------------------------------------------------------------------------
# loading
# --------------------------------------------------------------------------

def load(name):
    path = os.path.join(DATA, name)
    with open(path, "rb") as fh:
        raw = fh.read()
    return json.loads(raw.decode("utf-8")), hashlib.sha256(raw).hexdigest()


def clean_form(form):
    """Lexicon spelling -> list of (word, kind)."""
    f = form.strip()
    out = []
    m = re.fullmatch(r"([A-Za-z']+)\(([a-z]+)\)", f)
    if m:
        base, ext = m.group(1).lower(), m.group(2)
        out.append((base, "base"))
        if ext == "h":
            out.append((base + ext, "variant"))
        return out
    f = f.replace("...", "")
    for part in f.split("-"):
        part = part.strip().lower()
        if part and re.fullmatch(r"[a-z']+", part):
            out.append((part, "base"))
    return out


def typo_forms(entry):
    """Spellings that the dictionary row itself calls a typo."""
    notes = entry.get("notes") or ""
    return {m.lower() for m in re.findall(r'"([A-Za-z\']+)" is a typo', notes)}


def lexicon_words(lex):
    words = {}
    for e in lex["entries"]:
        refs = e.get("refs") or []
        if not refs:
            tier = "unsourced"
        elif all(r in SEMI_CANON_REFS for r in refs):
            tier = "semi_canon_refs_only"
        else:
            tier = "game_ref"
        typos = typo_forms(e)
        for form in e["word_forms"]:
            for w, kind in clean_form(form):
                if w in typos:
                    continue
                rec = words.setdefault(w, {"tiers": set(), "kinds": set(), "rows": []})
                rec["tiers"].add(tier)
                rec["kinds"].add(kind)
                rec["rows"].append(e["word"])
    return words


def tokens_of(text):
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)*", text)


# --------------------------------------------------------------------------
# units and syllables
# --------------------------------------------------------------------------

def units(word):
    """Cut a lower-case word into (unit, class) pairs.

    class: 'V' short vowel, 'VV' two-letter vowel unit, 'Vh' vowel + h,
           'C' consonant.
    """
    w = word.lower()
    out = []
    i = 0
    n = len(w)
    while i < n:
        if w[i:i + 3] == "u'u":
            out.append(("u'u", "VV"))
            i += 3
            continue
        two = w[i:i + 2]
        ch = w[i]
        nxt = w[i + 2] if i + 2 < n else ""
        if two in VOWEL_DIGRAPHS or two in DIPHTHONGS:
            out.append((two, "VV"))
            i += 2
            continue
        if ch in SINGLE_VOWELS and two[1:] == "h":
            if nxt == "" or nxt not in SINGLE_VOWELS or ch == "a":
                out.append((two, "Vh"))
                i += 2
                continue
        if two in CONS_DIGRAPHS:
            out.append((two, "C"))
            i += 2
            continue
        if two == "qu" and nxt in SINGLE_VOWELS:
            out.append((two, "C"))
            i += 2
            continue
        if ch in SINGLE_VOWELS:
            out.append((ch, "V"))
        elif ch == "'":
            out.append((ch, "'"))
        else:
            out.append((ch, "C"))
        i += 1
    return out


def is_vowel(cls):
    return cls in ("V", "VV", "Vh")


def edge_clusters(us):
    """(initial consonant run, list of medial runs, final run) as tuples of units."""
    k = 0
    while k < len(us) and not is_vowel(us[k][1]):
        k += 1
    k2 = len(us)
    while k2 > 0 and not is_vowel(us[k2 - 1][1]):
        k2 -= 1
    initial = tuple(u for u, _ in us[:k])
    final = tuple(u for u, _ in us[k2:]) if k2 >= k else ()
    medial = []
    i = k
    while i < k2:
        if not is_vowel(us[i][1]):
            j = i
            while j < k2 and not is_vowel(us[j][1]):
                j += 1
            medial.append(tuple(u for u, _ in us[i:j]))
            i = j
        else:
            i += 1
    return initial, medial, final


def syllabify(us, licit_onsets):
    """List of syllables; each is (onset tuple, (nucleus, class), coda tuple)."""
    nuclei = [i for i, (_, c) in enumerate(us) if is_vowel(c)]
    if not nuclei:
        return []
    sylls = []
    onset = tuple(u for u, c in us[:nuclei[0]] if c == "C")
    for idx, ni in enumerate(nuclei):
        if idx + 1 < len(nuclei):
            run = [u for u, c in us[ni + 1:nuclei[idx + 1]] if c == "C"]
            cut = len(run)  # everything to the coda unless a licit onset is found
            if run:
                cut = len(run) - 1  # a single consonant always opens the next syllable
                for start in range(0, len(run)):
                    if tuple(run[start:]) in licit_onsets:
                        cut = start
                        break
            coda, next_onset = tuple(run[:cut]), tuple(run[cut:])
        else:
            coda = tuple(u for u, c in us[ni + 1:] if c == "C")
            next_onset = ()
        sylls.append((onset, us[ni], coda))
        onset = next_onset
    return sylls


def shape(syll, fine):
    onset, (nuc, cls), coda = syll
    n = cls if fine else "V"
    return "C" * len(onset) + n + "C" * len(coda)


def rune_count(word, ir_ur_as_runes):
    w = word.lower().replace("u'u", "uu").replace("'", "")
    digs = RUNE_DIGRAPHS if ir_ur_as_runes else tuple(d for d in RUNE_DIGRAPHS if d not in ("ir", "ur"))
    i = 0
    n = 0
    while i < len(w):
        if w[i:i + 2] in digs:
            i += 2
        else:
            i += 1
        n += 1
    return n


# --------------------------------------------------------------------------
# small helpers for output
# --------------------------------------------------------------------------

def table(counter, examples=None, key=lambda k: k):
    rows = []
    for k, v in sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0]))):
        row = {"item": key(k), "count": v}
        if examples is not None:
            row["examples"] = sorted(set(examples[k]))[:EXAMPLES]
        rows.append(row)
    return rows


def dist(counter):
    total = sum(counter.values())
    return {
        "total": total,
        "counts": {str(k): counter[k] for k in sorted(counter)},
        "share": {str(k): round(counter[k] / total, 4) for k in sorted(counter)} if total else {},
        "mean": round(sum(k * v for k, v in counter.items()) / total, 3) if total else None,
    }


def freq(counter):
    total = sum(counter.values())
    return [
        {"item": k, "count": v, "share": round(v / total, 4)}
        for k, v in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    ]


def join(t):
    return "".join(t) if t else "(none)"


def decomposable(word, vocab, memo):
    """Can word be cut into 2-4 vocabulary words of >= 3 letters ('se' allowed inside)?"""
    def cuts(s, parts_left, first):
        key = (s, parts_left, first)
        if key in memo:
            return memo[key]
        res = None
        if not s:
            res = [] if not first else None
        elif parts_left > 0:
            for i in range(2, len(s) + 1):
                head = s[:i]
                ok = (len(head) >= 3 and head in vocab and head != word) or (head == "se" and not first and i < len(s))
                if not ok:
                    continue
                rest = cuts(s[i:], parts_left - (0 if head == "se" else 1), False)
                if rest is not None:
                    res = [head] + rest
                    break
        memo[key] = res
        return res
    r = cuts(word, 4, True)
    if r is None:
        return None
    if len([p for p in r if p != "se"]) < 2:
        return None
    return r


# --------------------------------------------------------------------------
# analysis of one word list
# --------------------------------------------------------------------------

def analyse(words, licit_onsets, weights=None):
    """Type statistics for an iterable of words (weights: word -> count for token statistics)."""
    wt = (lambda w: weights[w]) if weights else (lambda w: 1)
    initial = collections.Counter()
    final = collections.Counter()
    medial = collections.Counter()
    ex_i, ex_f, ex_m = (collections.defaultdict(list) for _ in range(3))
    on_med = collections.Counter()
    co_med = collections.Counter()
    ex_om, ex_cm = collections.defaultdict(list), collections.defaultdict(list)
    shapes_c = collections.Counter()
    shapes_f = collections.Counter()
    ex_sc, ex_sf = collections.defaultdict(list), collections.defaultdict(list)
    word_shapes = collections.Counter()
    ex_ws = collections.defaultdict(list)
    nuclei = collections.Counter()
    nuc_pos = collections.defaultdict(collections.Counter)
    syll_n = collections.Counter()
    len_letters = collections.Counter()
    len_runes_max = collections.Counter()
    len_runes_min = collections.Counter()
    vseq = collections.Counter()
    ex_v = collections.defaultdict(list)
    gem = collections.Counter()
    ex_g = collections.defaultdict(list)
    pos = collections.defaultdict(collections.Counter)
    ucount = collections.Counter()
    ubig = collections.Counter()
    lcount = collections.Counter()
    lbig = collections.Counter()
    for w in sorted(words):
        k = wt(w)
        us = units(w)
        seq = [u for u, c in us if c != "'"]
        cls = [c for u, c in us if c != "'"]
        ini, meds, fin = edge_clusters([(u, c) for u, c in us if c != "'"])
        initial[ini] += k
        ex_i[ini].append(w)
        final[fin] += k
        ex_f[fin].append(w)
        for m in meds:
            medial[m] += k
            ex_m[m].append(w)
        sylls = syllabify(us, licit_onsets)
        syll_n[len(sylls)] += k
        ws = ".".join(shape(s, False) for s in sylls)
        word_shapes[ws] += k
        ex_ws[ws].append(w)
        for si, s in enumerate(sylls):
            sc, sf = shape(s, False), shape(s, True)
            shapes_c[sc] += k
            ex_sc[sc].append(w)
            shapes_f[sf] += k
            ex_sf[sf].append(w)
            nuclei[s[1][0]] += k
            where = "only" if len(sylls) == 1 else ("first" if si == 0 else ("last" if si == len(sylls) - 1 else "middle"))
            nuc_pos[s[1][0]][where] += k
            if si > 0:
                on_med[s[0]] += k
                ex_om[s[0]].append(w)
            if si < len(sylls) - 1:
                co_med[s[2]] += k
                ex_cm[s[2]].append(w)
        letters = w.replace("'", "")
        len_letters[len(letters)] += k
        len_runes_max[rune_count(w, True)] += k
        len_runes_min[rune_count(w, False)] += k
        for a, b, ca, cb in zip(seq, seq[1:], cls, cls[1:]):
            if is_vowel(ca) and is_vowel(cb):
                vseq[(a, b)] += k
                ex_v[(a, b)].append(w)
            if ca == "C" and cb == "C" and a == b:
                gem[a + b] += k
                ex_g[a + b].append(w)
        for i, u in enumerate(seq):
            ucount[u] += k
            if len(seq) == 1:
                pos[u]["whole_word"] += k
            elif i == 0:
                pos[u]["initial"] += k
            elif i == len(seq) - 1:
                pos[u]["final"] += k
            else:
                pos[u]["medial"] += k
        for a, b in zip(["#"] + seq, seq + ["#"]):
            ubig[a + " " + b] += k
        for ch in w:
            lcount[ch] += k
        padded = "#" + w + "#"
        for a, b in zip(padded, padded[1:]):
            lbig[a + b] += k
    all_units = sorted(ucount)
    position_rows = []
    for u in sorted(all_units, key=lambda x: (-ucount[x], x)):
        p = pos[u]
        position_rows.append({
            "unit": u, "total": ucount[u],
            "initial": p["initial"] + p["whole_word"],
            "medial": p["medial"],
            "final": p["final"] + p["whole_word"],
        })
    return {
        "n_words": sum(wt(w) for w in words),
        "word_length": {
            "letters": dist(len_letters),
            "runes_if_ir_ur_written_as_runes": dist(len_runes_max),
            "runes_if_ir_ur_written_as_two_runes": dist(len_runes_min),
            "syllables": dist(syll_n),
        },
        "syllable_shapes": {
            "coarse": table(shapes_c, ex_sc),
            "fine": table(shapes_f, ex_sf),
            "whole_word_coarse": table(word_shapes, ex_ws)[:40],
        },
        "word_initial_onsets": table(initial, ex_i, join),
        "word_final_codas": table(final, ex_f, join),
        "medial_consonant_runs": table(medial, ex_m, lambda t: ".".join(t)),
        "medial_onsets_after_syllabification": table(on_med, ex_om, join),
        "medial_codas_after_syllabification": table(co_med, ex_cm, join),
        "nuclei": [
            {"unit": u, "count": c, "position": dict(sorted(nuc_pos[u].items()))}
            for u, c in sorted(nuclei.items(), key=lambda kv: (-kv[1], kv[0]))
        ],
        "vowel_sequences": table(vseq, ex_v, lambda t: "+".join(t)),
        "doubled_consonants": table(gem, ex_g),
        "unit_positions": position_rows,
        "units_never_word_initial": [r["unit"] for r in position_rows if r["initial"] == 0],
        "units_never_word_final": [r["unit"] for r in position_rows if r["final"] == 0],
        "unit_frequency": freq(ucount),
        "unit_bigrams_top": freq(ubig)[:150],
        "letter_frequency": freq(lcount),
        "letters_absent": [ch for ch in LETTERS if lcount[ch] == 0],
        "letter_bigrams_top": freq(lbig)[:150],
        "letter_bigram_types": len(lbig),
    }


def first_onsets(words):
    s = set()
    for w in words:
        us = [(u, c) for u, c in units(w) if c != "'"]
        ini, _, _ = edge_clusters(us)
        s.add(ini)
    return s


# --------------------------------------------------------------------------
# rune spelling (wiki rune-case: lower-case pair = one rune)
# --------------------------------------------------------------------------

def rune_spelling(corpus, shouts):
    realis = collections.defaultdict(collections.Counter)
    ex = collections.defaultdict(lambda: collections.defaultdict(set))
    rune_freq = collections.Counter()
    stray = collections.Counter()
    apostrophes = 0
    hyphens = 0
    n_records = 0
    n_tokens = 0
    for t in corpus["texts"]:
        if t.get("duplicate_of"):
            continue
        if "rune-case" not in (t.get("spelling") or ""):
            continue
        n_records += 1
        text = t["dovahzul"]
        apostrophes += text.count("'")
        hyphens += text.count("-")
        for w in re.findall(r"[A-Za-z]+", text):
            n_tokens += 1
            low = w.lower()
            for m in re.finditer(r"(?=(aa|ah|ei|ey|ii|ir|oo|uu|ur))", low):
                seg = w[m.start():m.start() + 2]
                kind = "one_rune" if seg.islower() else ("two_runes" if seg.isupper() else "mixed_case_on_wiki")
                realis[m.group(1)][kind] += 1
                ex[m.group(1)][kind].add(w)
            i = 0
            while i < len(w):
                two = w[i:i + 2]
                if len(two) == 2 and two.islower() and two in RUNE_DIGRAPHS:
                    rune_freq[two.upper()] += 1
                    i += 2
                elif w[i].isupper():
                    rune_freq[w[i]] += 1
                    i += 1
                else:
                    stray[w] += 1
                    rune_freq[w[i].upper()] += 1
                    i += 1
    shout_split = []
    seen = set()
    for sh in shouts["shouts"]:
        for wd in sh.get("words") or []:
            ws = wd.get("word_wiki_spelling") or ""
            if not wd.get("runes") or (wd["word"], ws) in seen:
                continue
            seen.add((wd["word"], ws))
            for m in re.finditer(r"(?=(aa|ah|ei|ey|ii|ir|oo|uu|ur))", ws.lower()):
                seg = ws[m.start():m.start() + 2]
                if not seg.islower():
                    shout_split.append({"shout": sh["name"], "word": wd["word"], "wiki_spelling": ws,
                                        "sequence": m.group(1), "runes": wd["runes"]})
    rows = []
    for dg in RUNE_DIGRAPHS:
        c = realis[dg]
        tot = sum(c.values())
        rows.append({
            "sequence": dg,
            "occurrences": tot,
            "written_as_one_rune": c["one_rune"],
            "written_as_two_runes": c["two_runes"],
            "mixed_case_on_wiki": c["mixed_case_on_wiki"],
            "share_one_rune": round(c["one_rune"] / tot, 3) if tot else None,
            "words_one_rune": sorted(ex[dg]["one_rune"])[:12],
            "words_two_runes": sorted(ex[dg]["two_runes"]),
            "words_mixed_case": sorted(ex[dg]["mixed_case_on_wiki"]),
        })
    return {
        "basis": "Non-duplicate corpus records whose spelling field is the wiki's rune-case (word walls and rune tables). "
                 "The casing is the wiki editors' transcription of the in-game rune text; it has not been checked against the game.",
        "records": n_records,
        "tokens": n_tokens,
        "apostrophes_in_rune_text": apostrophes,
        "hyphens_in_rune_text": hyphens,
        "two_letter_sequences": rows,
        "shout_words_with_a_split_sequence": shout_split,
        "tokens_with_a_stray_lower_case_letter": dict(sorted(stray.items())),
        "rune_frequency": freq(rune_freq),
        "runes_never_used": [r for r in [c.upper() for c in LETTERS if c != "c"] + [d.upper() for d in RUNE_DIGRAPHS]
                             if rune_freq[r] == 0],
    }


# --------------------------------------------------------------------------
# recurrent endings and beginnings (mechanical affix candidates)
# --------------------------------------------------------------------------

def affix_candidates(vocab):
    suff = collections.defaultdict(list)
    pref = collections.defaultdict(list)
    for w in sorted(vocab):
        for i in range(2, len(w)):
            stem, end = w[:i], w[i:]
            if stem in vocab and len(stem) >= 2 and 1 <= len(end) <= 4:
                suff[end].append([stem, w])
            head, rest = w[:i], w[i:]
            if rest in vocab and len(rest) >= 3 and 1 <= len(head) <= 3:
                pref[head].append([rest, w])
    # doubled final letter + e (the documented plural)
    plural = [[w[:-2], w] for w in sorted(vocab)
              if len(w) > 3 and w.endswith("e") and w[-2] == w[-3] and w[:-2] in vocab]
    s_rows = [{"ending": "-" + k, "pairs": len(v), "stem_and_word": v}
              for k, v in sorted(suff.items(), key=lambda kv: (-len(kv[1]), kv[0])) if len(v) >= 2]
    p_rows = [{"beginning": k + "-", "pairs": len(v), "base_and_word": v}
              for k, v in sorted(pref.items(), key=lambda kv: (-len(kv[1]), kv[0])) if len(v) >= 2]
    return {
        "note": "Pairs of spellings in which one is the other plus an ending (or beginning) and BOTH are in the word list. "
                "A string test only: many pairs are chance (in + hus, al + ok). Meaning must be checked by hand before "
                "a pair is called a derivation.",
        "endings": s_rows,
        "beginnings": p_rows,
        "doubled_final_letter_plus_e": plural,
    }


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def tiered(rows):
    """Count rows with a tier: core (>= 5 words), marginal (2-4), single (1)."""
    out = []
    for r in rows:
        c = r["count"]
        tier = "core" if c >= 5 else ("marginal" if c >= 2 else "single")
        item = r["item"] if "item" in r else r[next(iter(r))]
        out.append({"item": item, "count": c, "tier": tier, "examples": r.get("examples", [])[:3]})
    return out


def rime_table(words, licit_onsets):
    """Class of the last nucleus x length of the word-final coda; long nucleus + cluster pairs."""
    by_class = collections.Counter()
    pairs = collections.Counter()
    ex = collections.defaultdict(list)
    for w in sorted(words):
        sylls = syllabify(units(w), licit_onsets)
        if not sylls:
            continue
        _, (nuc, cls), coda = sylls[-1]
        by_class["%s + %d C" % (cls, len(coda))] += 1
        if len(coda) >= 2:
            pairs["%s + %s" % (nuc, join(coda))] += 1
            ex["%s + %s" % (nuc, join(coda))].append(w)
    return {
        "nucleus_class_by_coda_length": {k: by_class[k] for k in sorted(by_class)},
        "nucleus_plus_coda_cluster": table(pairs, ex),
    }


WORDLIKENESS_K = 0.5
CONTROL_STRINGS = ("strength", "twelfth", "glimpse", "quick", "school", "thwart", "jumped", "bzdrang",
                   "kaal", "drun", "vothiik", "zaanlok")


def wordlikeness_model(train, extra_sets):
    """Unit-bigram model with boundaries; leave-one-out scores for the training words."""
    def seq(w):
        return ["#"] + [u for u, _ in units(w)] + ["#"]

    big = collections.Counter()
    ctx = collections.Counter()
    types = {"#"}
    for w in train:
        q = seq(w)
        types.update(q)
        for a, b in zip(q, q[1:]):
            big[(a, b)] += 1
            ctx[a] += 1
    v = len(types)
    k = WORDLIKENESS_K

    def score(w, leave_out):
        q = seq(w)
        own = collections.Counter(zip(q, q[1:])) if leave_out else {}
        own_ctx = collections.Counter(q[:-1]) if leave_out else {}
        total = 0.0
        unseen = 0
        for a, b in zip(q, q[1:]):
            c = big[(a, b)] - own.get((a, b), 0)
            if c <= 0:
                unseen += 1
            total += math.log2((c + k) / (ctx[a] - own_ctx.get(a, 0) + k * v))
        return round(total / (len(q) - 1), 4), unseen

    scored = sorted((score(w, True) + (w,) for w in train), key=lambda t: (t[0], t[2]))
    vals = [t[0] for t in scored]

    def pct(p):
        return vals[int(p * (len(vals) - 1))]

    with_unseen = sum(1 for t in scored if t[1] > 0)
    out = {
        "what": "mean log2 P(unit | previous unit) over a word with boundaries, add-k smoothing",
        "k": k,
        "unit_types_including_boundary": v,
        "bigram_types": len(big),
        "trained_on": "lexicon_not_decomposable",
        "n_training_words": len(vals),
        "leave_one_out_score_percentiles": {
            "min": vals[0], "p01": pct(0.01), "p05": pct(0.05), "p10": pct(0.10),
            "p25": pct(0.25), "p50": pct(0.50), "p75": pct(0.75), "max": vals[-1],
        },
        "training_words_with_a_transition_seen_in_no_other_word": with_unseen,
        "share_with_such_a_transition": round(with_unseen / len(vals), 4),
        "lowest_scoring_training_words": [
            {"word": w, "score": sc, "unseen_transitions": u} for sc, u, w in scored[:20]
        ],
        "other_sets": {},
        "control_strings_illustration_only": [],
    }
    for name, words in extra_sets.items():
        sc = sorted(score(w, w in train)[0] for w in words)
        if sc:
            out["other_sets"][name] = {
                "n": len(sc), "min": sc[0], "p05": sc[int(0.05 * (len(sc) - 1))],
                "p50": sc[int(0.5 * (len(sc) - 1))], "max": sc[-1],
            }
    for w in CONTROL_STRINGS:
        sc, u = score(w, w in train)
        out["control_strings_illustration_only"].append(
            {"string": w, "score": sc, "unseen_transitions": u, "in_training_set": w in train})
    return out


def build():
    lex, h_lex = load("canon-lexicon.json")
    corpus, h_cor = load("canon-corpus.json")
    shouts, h_sh = load("canon-shouts.json")
    oov, h_oov = load("corpus-oov.json")

    lw = lexicon_words(lex)
    vocab = set(lw)
    licit = first_onsets(vocab)

    # corpus tokens
    drop_classes = ("name", "spelling variant or error", "word of another language inside dragon text")
    drop = {e["token"] for e in oov["oov"] if e["class"] in drop_classes}
    tok = collections.Counter()
    for t in corpus["texts"]:
        if t.get("duplicate_of") or t["type"] == "name":
            continue
        if not (t.get("canon_status") or "").startswith("canon"):
            continue
        for w in tokens_of(t["dovahzul"]):
            lw_ = w.lower()
            if lw_ in drop:
                continue
            tok[lw_] += 1

    in_corpus = {w for w in vocab if tok[w] > 0}
    memo = {}
    decomp = {w: decomposable(w, vocab, memo) for w in sorted(vocab)}
    simplex = {w for w in vocab if decomp[w] is None}

    game = {w for w, r in lw.items() if "game_ref" in r["tiers"]}
    semi_only = vocab - game

    res_all = analyse(vocab, licit)
    res_simplex = analyse(simplex, licit)
    res_game = analyse(game, licit)
    res_incorpus = analyse(in_corpus, licit)
    res_tokens = analyse(set(tok), licit, weights=tok)

    def items(res, key):
        return {r["item"] for r in res[key]}

    def only_in(a, b, key):
        return sorted(items(a, key) - items(b, key))

    # shout words
    sw = sorted({wd["word"].lower() for sh in shouts["shouts"] for wd in (sh.get("words") or [])})
    sw_syll = collections.Counter()
    sw_multi = []
    for w in sw:
        n = len(syllabify(units(w), licit))
        sw_syll[n] += 1
        if n != 1:
            sw_multi.append(w)
    res_shout = analyse(set(sw), licit)

    # dragon names
    names = []
    name_syll = collections.Counter()
    for nrec in lex["names"]:
        if nrec.get("group") != "translated":
            continue
        nm = nrec["name"].lower()
        if not re.fullmatch(r"[a-z']+", nm):
            continue
        sy = syllabify(units(nm), licit)
        parts = ["".join(o) + n[0] + "".join(c) for o, n, c in sy]
        name_syll[len(sy)] += 1
        names.append({"name": nrec["name"], "syllables": len(sy), "cut": "-".join(parts),
                      "wiki_meaning": nrec.get("meaning")})

    # syllabification of every lexicon word, for inspection and reuse
    syll_list = {}
    for w in sorted(vocab):
        sy = syllabify(units(w), licit)
        syll_list[w] = "-".join("".join(o) + n[0] + "".join(c) for o, n, c in sy)

    unit_classes = collections.defaultdict(set)
    for w in vocab:
        for u, c in units(w):
            unit_classes[c].add(u)

    out = {
        "meta": {
            "generator": "tools/analysis/phonotactics.py " + VERSION,
            "inputs": {
                "research/data/canon-lexicon.json": h_lex,
                "research/data/canon-corpus.json": h_cor,
                "research/data/canon-shouts.json": h_sh,
                "research/data/corpus-oov.json": h_oov,
            },
            "license": "Derived from UESP wiki text, Attribution-ShareAlike 2.5 (see research/data/README.md)",
            "what_this_is": "Counts over SPELLING. The language has no official phonemic description; 'onset', 'coda' and "
                            "'syllable' are built by the fixed rules in the script's docstring.",
            "rules": {
                "vowel_units": "u'u, aa ei ey ii oo uu, au ae, and vowel+h (ah eh ih oh uh) when the h ends the word or "
                               "precedes a consonant ('ah' also before a vowel)",
                "consonant_units": "th, sh, qu-before-vowel; every other consonant letter; y is a consonant except in ey",
                "ir_ur": "counted as vowel + r; their status as runes is under rune_spelling",
                "syllabification": "one nucleus per vowel unit; medial consonant runs split by maximal onset, where a licit "
                                   "onset is one that begins a lexicon word; a single consonant always opens the next syllable",
                "decomposable": "cut into 2-4 other lexicon words of >= 3 letters, 'se' allowed between parts (string test)",
                "tiers": "game_ref = at least one reference other than Prima, TIL, BN, DBgamedata on the dictionary row",
            },
            "caveats": [
                "Compounds dominate the longer words, so many medial clusters are junctures between words (sos-mir), "
                "not clusters inside a morpheme. Use lexicon_not_decomposable for morpheme-internal patterns.",
                "ng is counted as n + g; whether it is one sound (viing) cannot be decided from spelling.",
                "The maximal-onset rule cuts kendov as ken-dov and ahkrin as ah-krin; it knows nothing of morphemes.",
                "Token statistics leave out names and misspellings as classed in corpus-oov.json.",
            ],
            "counts": {
                "lexicon_spellings": len(vocab),
                "lexicon_spellings_in_canon_corpus": len(in_corpus),
                "lexicon_spellings_with_game_ref": len(game),
                "lexicon_spellings_semi_canon_or_unsourced": len(semi_only),
                "lexicon_not_decomposable": len(simplex),
                "lexicon_mechanically_decomposable": len(vocab) - len(simplex),
                "shout_words": len(sw),
                "dragon_names": len(names),
                "corpus_token_types": len(tok),
                "corpus_tokens": sum(tok.values()),
            },
        },
        "unit_inventory": {
            "short_vowels": sorted(unit_classes["V"]),
            "two_letter_vowel_units": sorted(unit_classes["VV"]),
            "vowel_plus_h_units": sorted(unit_classes["Vh"]),
            "consonant_units": sorted(unit_classes["C"]),
            "licit_word_initial_onsets": sorted(join(o) for o in licit),
        },
        "lexicon": res_all,
        "lexicon_not_decomposable": res_simplex,
        "lexicon_game_ref_only": {
            "n_words": res_game["n_words"],
            "word_initial_onsets": res_game["word_initial_onsets"],
            "word_final_codas": res_game["word_final_codas"],
            "syllable_shapes": res_game["syllable_shapes"],
            "word_length": res_game["word_length"],
        },
        "found_only_in_semi_canon_or_unsourced_words": {
            "word_initial_onsets": only_in(res_all, res_game, "word_initial_onsets"),
            "word_final_codas": only_in(res_all, res_game, "word_final_codas"),
            "medial_consonant_runs": only_in(res_all, res_game, "medial_consonant_runs"),
            "vowel_sequences": only_in(res_all, res_game, "vowel_sequences"),
        },
        "found_only_in_words_absent_from_the_canon_corpus": {
            "note": "Patterns carried only by dictionary spellings that never occur as a token in the canon corpus "
                    "(the weakest-attested layer: mostly Prima-guide-only and Imperial-Library-only rows).",
            "word_initial_onsets": only_in(res_all, res_incorpus, "word_initial_onsets"),
            "word_final_codas": only_in(res_all, res_incorpus, "word_final_codas"),
            "medial_consonant_runs": only_in(res_all, res_incorpus, "medial_consonant_runs"),
            "vowel_sequences": only_in(res_all, res_incorpus, "vowel_sequences"),
            "words": sorted(vocab - in_corpus),
        },
        "corpus_tokens": {
            "n_tokens": res_tokens["n_words"],
            "word_length": res_tokens["word_length"],
            "letter_frequency": res_tokens["letter_frequency"],
            "unit_frequency": res_tokens["unit_frequency"],
            "letter_bigrams_top": res_tokens["letter_bigrams_top"][:80],
            "syllable_shapes_coarse": res_tokens["syllable_shapes"]["coarse"],
            "word_frequency_top": [
                {"word": w, "count": c, "in_lexicon": w in vocab}
                for w, c in sorted(tok.items(), key=lambda kv: (-kv[1], kv[0]))[:200]
            ],
            "hapax_types": sum(1 for c in tok.values() if c == 1),
        },
        "shout_words": {
            "n": len(sw),
            "syllable_counts": dist(sw_syll),
            "not_monosyllabic": sw_multi,
            "syllable_shapes_fine": res_shout["syllable_shapes"]["fine"],
            "word_initial_onsets": res_shout["word_initial_onsets"],
            "word_final_codas": res_shout["word_final_codas"],
        },
        "dragon_names": {
            "n": len(names),
            "syllable_counts": dist(name_syll),
            "names": names,
        },
        "rune_spelling": rune_spelling(corpus, shouts),
        "affix_candidates": affix_candidates(vocab),
        "forge_profile": {
            "basis": "lexicon_not_decomposable (see the docstring, section 5)",
            "tiers": "core: 5 or more words; marginal: 2 to 4; single: 1",
            "word_initial_onsets": tiered(res_simplex["word_initial_onsets"]),
            "word_final_codas": tiered(res_simplex["word_final_codas"]),
            "nuclei": tiered(res_simplex["nuclei"]),
            "final_rime": rime_table(simplex, licit),
            "wordlikeness_model": wordlikeness_model(
                simplex,
                {"lexicon_mechanically_decomposable": vocab - simplex,
                 "shout_words": set(sw),
                 "dragon_names": {n_["name"] for n_ in names} if names and isinstance(names[0], dict) and "name" in names[0] else set()},
            ),
        },
        "mechanically_decomposable_words": {w: p for w, p in decomp.items() if p is not None},
        "syllabification_of_lexicon": syll_list,
    }
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="recompute and compare with the file on disk; write nothing")
    args = ap.parse_args(argv)
    out = build()
    text = json.dumps(out, ensure_ascii=False, indent=1, sort_keys=False) + "\n"
    if args.check:
        try:
            with open(OUT, encoding="utf-8") as fh:
                same = fh.read() == text
        except FileNotFoundError:
            same = False
        print("canon-phonotactics.json is %s" % ("up to date" if same else "OUT OF DATE or missing"))
        return 0 if same else 1
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    c = out["meta"]["counts"]
    print("wrote %s" % os.path.relpath(OUT, ROOT))
    print("lexicon spellings: %d (not decomposable: %d); shout words: %d; corpus tokens: %d"
          % (c["lexicon_spellings"], c["lexicon_not_decomposable"], c["shout_words"], c["corpus_tokens"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
