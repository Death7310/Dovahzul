#!/usr/bin/env python3
"""Core-concept gap analysis of the canon dragon-language lexicon.

Compares the English glosses of research/data/canon-lexicon.json against
three core-concept inventories and writes
research/data/core-concept-gaps.json. Standard library only; deterministic.

    python3 -I tools/analysis/core_concept_gaps.py        # from the repo root

The three inventories
---------------------
swadesh207   The 207-item composite Swadesh list (the union of Swadesh's
             200-item and 100-item lists as conventionally tabulated).
leipzig100   The Leipzig-Jakarta list of 100 borrowing-resistant meanings
             (Tadmor 2009, in Haspelmath & Tadmor, Loanwords in the World's
             Languages), in rank order.
nsm65        The 65 semantic primes of Natural Semantic Metalanguage in the
             English exponents of Goddard & Wierzbicka (2014).

HOW THE LISTS WERE OBTAINED: typed in from the analyst's knowledge of the
published lists, NOT downloaded (Concepticon and WOLD are not reachable from
the build container). Item counts were checked (207, 100, 65). Before the
lists are frozen into the app they should be diffed against the Concepticon
concept lists Swadesh-1952-200 + Swadesh-1955-100, Tadmor-2009-100 and
Goddard-2014-65 (reliability: high for membership, unchecked for exact
English label wording).

How a concept is scored
-----------------------
Each concept carries two hand-written sets of English gloss strings:
  accept  glosses that express the concept itself in the right word class
  near    glosses that are a hyponym, a derivative in another word class, or
          a close relative; they show the root material exists but a human
          must rule whether the concept counts as covered
A lexicon gloss is normalised (lower case; "Mortal(s)" -> mortal, mortals;
"(Dragon) Shout" -> shout, dragon shout; "(v.)", "(noun)" and bracketed
remarks dropped) and compared for EXACT string equality. No stemming and no
substring test, so the script under-detects rather than over-detects.
  covered  at least one accept hit
  partial  no accept hit, at least one near hit
  missing  neither
Each hit records the entry's sourcing tier (see tier_of). English glosses
are the wiki's reading of each word; sense distinctions English does not
mark (you sg/pl, lie down / tell a lie) are flagged in "note".
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEX = ROOT / "research/data/canon-lexicon.json"
CORPUS = ROOT / "research/data/canon-corpus.json"
OUT = ROOT / "research/data/core-concept-gaps.json"

SEMI = {"Prima", "TIL", "BN", "DBgamedata", "GI", "RelivingSkyrim"}


def tier_of(refs):
    """Sourcing tier of a dictionary row, following research/data/README.md."""
    if not refs:
        return "unsourced"
    if any(r not in SEMI for r in refs):
        return "canon"          # at least one game-text / in-game-book reference
    return "semi-canon"         # Prima guide, Imperial Library list, press, game data only


def norm_gloss(g):
    """Return the set of normalised strings one gloss stands for."""
    g = g.strip().lower().rstrip(".")
    g = re.sub(r"\((v\.|n\.|adj\.|noun|verb|similar)\)", "", g).strip()
    out = set()
    m = re.match(r"^\(([^)]+)\)\s*(.+)$", g)          # "(dragon) shout"
    if m:
        out.add(m.group(2).strip())
        out.add((m.group(1) + " " + m.group(2)).strip())
        return out
    m = re.match(r"^(.+?)\(([^)]+)\)$", g)            # "mortal(s)", "bold(ly)", "a(n)"
    if m:
        out.add(m.group(1).strip())
        out.add((m.group(1) + m.group(2)).strip())
        return out
    out.add(g)
    return out


def C(label, accept, near=(), note=None):
    return {"concept": label, "accept": list(accept), "near": list(near), "note": note}


SWADESH = [
    C("I", ["i"]), C("you (singular)", ["you"]), C("he", ["he"]), C("we", ["we"]),
    C("you (plural)", [], ["you"], "canon 'hi' is glossed 'you' with no number stated"),
    C("they", ["they"]), C("this", ["this"]), C("that", ["that"]), C("here", ["here"]),
    C("there", ["there"]), C("who", ["who"]), C("what", ["what"]), C("where", ["where"]),
    C("when", ["when"]), C("how", ["how"]), C("not", ["not"]), C("all", ["all"]),
    C("many", ["many"]), C("some", ["some"]), C("few", ["few"], ["little"]),
    C("other", ["other", "another"]), C("one", ["one"]), C("two", ["two"], ["both", "twin"]),
    C("three", ["three"]), C("four", ["four"]), C("five", ["five"]),
    C("big", ["big", "large"], ["great", "mighty"]), C("long", ["long"]), C("wide", ["wide", "broad"]),
    C("thick", ["thick"]), C("heavy", ["heavy"]), C("small", ["small"], ["little"]),
    C("short", ["short"], ["brief"]), C("narrow", ["narrow"]), C("thin", ["thin"]),
    C("woman", ["woman", "women"], ["maiden", "wife"]), C("man (adult male)", ["man"]),
    C("man (human being)", ["human", "humans", "person", "mankind"], ["mortal", "mortals"]),
    C("child", ["child"]), C("wife", ["wife"]), C("husband", ["husband"]),
    C("mother", ["mother"]), C("father", ["father"]), C("animal", ["animal"], ["beast", "beasts"]),
    C("fish", ["fish"]), C("bird", ["bird"], ["raven"]), C("dog", ["dog", "hound"], ["wolf"]),
    C("louse", ["louse"]), C("snake", ["snake", "serpent"]), C("worm", ["worm"]),
    C("tree", ["tree"]), C("forest", ["forest"]), C("stick", ["stick"]), C("fruit", ["fruit"]),
    C("seed", ["seed"]), C("leaf", ["leaf"]), C("root", ["root"]), C("bark (of a tree)", ["bark"]),
    C("flower", ["flower"]), C("grass", ["grass"]), C("rope", ["rope"]), C("skin", ["skin", "hide"]),
    C("meat", ["meat", "flesh"]), C("blood", ["blood"]), C("bone", ["bone"]), C("fat (noun)", ["fat"]),
    C("egg", ["egg"]), C("horn", ["horn"]), C("tail", ["tail"]), C("feather", ["feather"]),
    C("hair", ["hair"]), C("head", ["head"]), C("ear", ["ear"]), C("eye", ["eye"]),
    C("nose", ["nose"]), C("mouth", ["mouth"], ["maw"]), C("tooth", ["tooth"]),
    C("tongue", ["tongue"]), C("fingernail", ["fingernail", "nail"], ["claw"]),
    C("foot", ["foot"]), C("leg", ["leg"]), C("knee", ["knee"]), C("hand", ["hand"]),
    C("wing", ["wing"]), C("belly", ["belly", "stomach"]), C("guts", ["guts", "intestines"]),
    C("neck", ["neck"], ["throat"]), C("back", ["back"]), C("breast", ["breast", "chest"]),
    C("heart", ["heart"]), C("liver", ["liver"]), C("to drink", ["drink"]), C("to eat", ["eat"]),
    C("to bite", ["bite"]), C("to suck", ["suck"]), C("to spit", ["spit"]), C("to vomit", ["vomit"]),
    C("to blow", ["blow"]), C("to breathe", ["breathe"], ["breath"]), C("to laugh", ["laugh"]),
    C("to see", ["see"]), C("to hear", ["hear"]), C("to know", ["know"]),
    C("to think", ["think"], ["thought"]), C("to smell", ["smell"], ["stink"]),
    C("to fear", ["fear"]), C("to sleep", ["sleep"], ["rest", "dream"]), C("to live", ["live"]),
    C("to die", ["die"]), C("to kill", ["kill"]), C("to fight", ["fight"]), C("to hunt", ["hunt"]),
    C("to hit", ["hit", "strike"]), C("to cut", ["cut"]), C("to split", ["split"], ["break", "rip"]),
    C("to stab", ["stab", "pierce"], ["sting"]), C("to scratch", ["scratch"]),
    C("to dig", ["dig"], ["bury"]), C("to swim", ["swim"]), C("to fly", ["fly"]),
    C("to walk", ["walk"], ["march", "wander", "travel"]), C("to come", ["come"]),
    C("to lie (as in a bed)", ["lie down"], ["lie"],
      "canon 'nok' is glossed 'lie' with a wiki remark that it covers both 'lie down' and 'tell a lie'"),
    C("to sit", ["sit"]), C("to stand", ["stand"]), C("to turn (intransitive)", ["turn"]),
    C("to fall", ["fall"]), C("to give", ["give"]), C("to hold", ["hold"], ["keep", "wield"]),
    C("to squeeze", ["squeeze"]), C("to rub", ["rub"]), C("to wash", ["wash"]), C("to wipe", ["wipe"]),
    C("to pull", ["pull"]), C("to push", ["push"]), C("to throw", ["throw"]),
    C("to tie", ["tie", "bind"]), C("to sew", ["sew"]), C("to count", ["count"]),
    C("to say", ["say"], ["talk", "told", "speech"]), C("to sing", ["sing"], ["song"]),
    C("to play", ["play"]), C("to float", ["float"]), C("to flow", ["flow"]),
    C("to freeze", ["freeze"]), C("to swell", ["swell"]), C("sun", ["sun"]), C("moon", ["moon"]),
    C("star", ["star"]), C("water", ["water"]), C("rain", ["rain"]), C("river", ["river"]),
    C("lake", ["lake"]), C("sea", ["sea"]), C("salt", ["salt"]), C("stone", ["stone"]),
    C("sand", ["sand"]), C("dust", ["dust"]), C("earth", ["earth", "soil"]), C("cloud", ["cloud"]),
    C("fog", ["fog", "mist"]), C("sky", ["sky"]), C("wind", ["wind"]), C("snow", ["snow"]),
    C("ice", ["ice"]), C("smoke", ["smoke"]), C("fire", ["fire"]), C("ash", ["ash", "ashes"]),
    C("to burn", ["burn"]), C("road", ["road"], ["path"]), C("mountain", ["mountain"]),
    C("red", ["red"]), C("green", ["green"]), C("yellow", ["yellow"], ["gold", "golden"]),
    C("white", ["white"]), C("black", ["black"]), C("night", ["night"]), C("day", ["day"]),
    C("year", ["year"]), C("warm", ["warm"], ["warmth", "hot"]), C("cold", ["cold"]),
    C("full", ["full"]), C("new", ["new"], ["young"]), C("old", ["old"]), C("good", ["good"]),
    C("bad", ["bad"], ["evil", "foul", "wrong"]), C("rotten", ["rotten"], ["foul"]),
    C("dirty", ["dirty"]), C("straight", ["straight"]), C("round", ["round"]),
    C("sharp (as a knife)", ["sharp"]), C("dull (as a knife)", ["dull", "blunt"]),
    C("smooth", ["smooth"]), C("wet", ["wet"]), C("dry", ["dry"]),
    C("correct", ["correct", "right"], ["true"]), C("near", ["near", "close"]), C("far", ["far"]),
    C("right (side)", ["right"]), C("left (side)", ["left"]), C("at", ["at"]), C("in", ["in"]),
    C("with", ["with"]), C("and", ["and"]), C("if", ["if"]), C("because", ["because"]),
    C("name", ["name"]),
]

LEIPZIG = [
    C("fire", ["fire"]), C("nose", ["nose"]), C("to go", ["go"], ["travel", "move", "march"]),
    C("water", ["water"]), C("mouth", ["mouth"], ["maw"]), C("tongue", ["tongue"]),
    C("blood", ["blood"]), C("bone", ["bone"]), C("2SG pronoun", ["you"]), C("root", ["root"]),
    C("to come", ["come"]), C("breast", ["breast", "chest"]), C("rain", ["rain"]),
    C("1SG pronoun", ["i"]), C("name", ["name"]), C("louse", ["louse"]), C("wing", ["wing"]),
    C("flesh/meat", ["flesh", "meat"]), C("arm/hand", ["arm", "hand"]), C("fly (insect)", [],
      [], "canon 'bo' is the verb 'fly'; no insect word"),
    C("night", ["night"]), C("ear", ["ear"]), C("neck", ["neck"], ["throat"]), C("far", ["far"]),
    C("to do/make", ["do", "make"], ["create", "build"]), C("house", ["house"], ["home", "steading", "palace"]),
    C("stone/rock", ["stone", "rock"]), C("bitter", ["bitter"]),
    C("to say", ["say"], ["talk", "told", "speech"]), C("tooth", ["tooth"]), C("hair", ["hair"]),
    C("big", ["big", "large"], ["great", "mighty"]), C("one", ["one"]), C("who?", ["who"]),
    C("3SG pronoun", ["he", "she", "it"]), C("to hit/beat", ["hit", "beat", "strike"]),
    C("leg/foot", ["leg", "foot"]), C("horn", ["horn"]), C("this", ["this"]), C("fish", ["fish"]),
    C("yesterday", ["yesterday"]), C("to drink", ["drink"]), C("black", ["black"]),
    C("navel", ["navel"]), C("to stand", ["stand"]), C("to bite", ["bite"]), C("back", ["back"]),
    C("wind", ["wind"]), C("smoke", ["smoke"]), C("what?", ["what"]),
    C("child (kin term)", ["child"], ["son", "daughter"]), C("egg", ["egg"]), C("to give", ["give"]),
    C("new", ["new"], ["young"]), C("to burn (intransitive)", ["burn"]), C("not", ["not"]),
    C("good", ["good"]), C("to know", ["know"]), C("knee", ["knee"]), C("sand", ["sand"]),
    C("to laugh", ["laugh"]), C("to hear", ["hear"]), C("soil", ["soil", "earth"]), C("leaf", ["leaf"]),
    C("red", ["red"]), C("liver", ["liver"]), C("to hide", ["hide", "conceal"]),
    C("skin/hide", ["skin"]), C("to suck", ["suck"]), C("to carry", ["carry"], ["bring"]),
    C("ant", ["ant"]), C("heavy", ["heavy"]), C("to take", ["take"], ["steal", "receive", "borrow"]),
    C("old", ["old"]), C("to eat", ["eat"]), C("thigh", ["thigh"]), C("thick", ["thick"]),
    C("long", ["long"]), C("to blow", ["blow"]), C("wood", ["wood"], ["tree", "forest"],
      "tree/wood colexification is common cross-linguistically; a human must rule"),
    C("to run", ["run"]), C("to fall", ["fall"]), C("eye", ["eye"]), C("ash", ["ash", "ashes"]),
    C("tail", ["tail"]), C("dog", ["dog", "hound"], ["wolf"]), C("to cry/weep", ["cry", "weep"], [],
      "canon 'luv' is glossed 'tear' (sense unstated); 'vaaz' is 'tear, rip', expressly not lacrimal"),
    C("to tie", ["tie", "bind"]), C("to see", ["see"]), C("sweet", ["sweet"]), C("rope", ["rope"]),
    C("shade/shadow", ["shade", "shadow"]), C("bird", ["bird"], ["raven"]), C("salt", ["salt"]),
    C("small", ["small"], ["little"]), C("wide", ["wide", "broad"]), C("star", ["star"]),
    C("in", ["in"]), C("hard", ["hard"]), C("to crush/grind", ["crush", "grind"]),
]

NSM = [
    C("I", ["i"]), C("YOU", ["you"]), C("SOMEONE", ["someone", "somebody"]),
    C("SOMETHING~THING", ["something", "thing"]),
    C("PEOPLE", ["people"], ["humans", "mankind", "men", "mortals"]), C("BODY", ["body"]),
    C("KIND", ["kind", "sort"]), C("PART", ["part"]), C("THIS", ["this"]),
    C("THE SAME", ["same", "the same"]), C("OTHER~ELSE", ["other", "else", "another"]),
    C("ONE", ["one"]), C("TWO", ["two"], ["both", "twin"]), C("SOME", ["some"]), C("ALL", ["all"]),
    C("MUCH~MANY", ["much", "many"]),
    C("LITTLE~FEW", ["few"], ["little"], "canon 'mal' is glossed 'little'; size or quantity is not stated"),
    C("GOOD", ["good"]), C("BAD", ["bad"], ["evil", "foul", "wrong"]),
    C("BIG", ["big", "large"], ["great", "mighty"]), C("SMALL", ["small"], ["little"]),
    C("THINK", ["think"], ["thought"]), C("KNOW", ["know"]), C("WANT", ["want"], ["wish"]),
    C("DON'T WANT", [], [], "no lexical exponent; composable from NOT + WANT if the grammar allows"),
    C("FEEL", ["feel"]), C("SEE", ["see"]), C("HEAR", ["hear"]),
    C("SAY", ["say"], ["talk", "told", "speech"]), C("WORDS", ["word", "words"]), C("TRUE", ["true"]),
    C("DO", ["do"]), C("HAPPEN", ["happen"]), C("MOVE", ["move"]),
    C("BE (SOMEWHERE)", ["be", "is"], [], "one canon copula stands for three primes"),
    C("THERE IS", [], ["be", "is"], "no dedicated existential attested in the dictionary"),
    C("BE (SOMEONE/SOMETHING)", ["be", "is"]), C("(IS) MINE", ["mine"]),
    C("LIVE", ["live"]), C("DIE", ["die"]), C("WHEN~TIME", ["when", "time"]), C("NOW", ["now"]),
    C("BEFORE", ["before"]), C("AFTER", ["after"]),
    C("A LONG TIME", [], ["long", "eternity", "forever"], "composable"),
    C("A SHORT TIME", [], ["brief", "temporary", "ephemeral"], "composable"),
    C("FOR SOME TIME", [], [], "composable from SOME + TIME"), C("MOMENT", ["moment"]),
    C("WHERE~PLACE", ["where", "place"]), C("HERE", ["here"]), C("ABOVE", ["above", "over"]),
    C("BELOW", ["below", "under"], ["down"]), C("FAR", ["far"]), C("NEAR", ["near", "close"]),
    C("SIDE", ["side"]), C("INSIDE", ["inside", "within"], ["inner", "in"]), C("TOUCH", ["touch"]),
    C("NOT", ["not"]), C("MAYBE", ["maybe", "perhaps"], ["may"]), C("CAN", ["can"], ["cannot", "may"]),
    C("BECAUSE", ["because"]), C("IF", ["if"]), C("VERY", ["very"]), C("MORE", ["more"], ["most"]),
    C("LIKE~AS~WAY", ["like", "as"]),
]

LISTS = [
    ("swadesh207", "Swadesh 207 (composite of the 200- and 100-item lists)", SWADESH, 207),
    ("leipzig_jakarta100", "Leipzig-Jakarta 100 (Tadmor 2009)", LEIPZIG, 100),
    ("nsm65", "NSM semantic primes (Goddard & Wierzbicka 2014)", NSM, 65),
]


def spearman(xs, ys):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def clean_form(w):
    w = w.strip().lower()
    w = re.sub(r"\(.*?\)", "", w)
    w = w.replace("...", "")
    return w


def main():
    lex = json.loads(LEX.read_text(encoding="utf-8"))
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    entries = lex["entries"]

    index = {}                                  # normalised gloss -> [hit]
    for e in entries:
        t = tier_of(e["refs"])
        for g in e["definitions"]:
            for n in norm_gloss(g):
                index.setdefault(n, []).append(
                    {"word": e["word"], "gloss": g.strip(), "tier": t})

    fan = {}                                    # wiki hover glosses in dialogue
    for rec in corpus["texts"]:
        for seg in rec.get("segments") or []:
            eng = (seg.get("english") or "").strip().lower()
            if eng and len(eng.split()) <= 2:
                fan.setdefault(eng, set()).add(seg.get("dovahzul", "").strip())

    out_lists = {}
    for key, title, concepts, expect in LISTS:
        assert len(concepts) == expect, (key, len(concepts))
        rows, tally, tier_tally = [], Counter(), Counter()
        for c in concepts:
            acc = [h for a in c["accept"] for h in index.get(a, [])]
            near = [h for a in c["near"] for h in index.get(a, [])]
            status = "covered" if acc else ("partial" if near else "missing")
            tally[status] += 1
            row = {"concept": c["concept"], "status": status}
            if acc:
                row["canon_words"] = acc
                best = ("canon" if any(h["tier"] == "canon" for h in acc)
                        else "semi-canon" if any(h["tier"] == "semi-canon" for h in acc)
                        else "unsourced")
                row["best_tier"] = best
                tier_tally[best] += 1
            if near and not acc:
                row["near_words"] = near
            if not acc:
                hits = sorted({w for a in c["accept"] for w in fan.get(a, ())})
                if hits:
                    row["corpus_hover_gloss_only"] = hits   # fan-level evidence
            if c["note"]:
                row["note"] = c["note"]
            rows.append(row)
        n = len(concepts)
        out_lists[key] = {
            "title": title,
            "n_concepts": n,
            "covered": tally["covered"], "partial": tally["partial"], "missing": tally["missing"],
            "pct_covered": round(100 * tally["covered"] / n, 1),
            "pct_covered_or_partial": round(100 * (tally["covered"] + tally["partial"]) / n, 1),
            "pct_missing": round(100 * tally["missing"] / n, 1),
            "covered_by_best_tier": dict(tier_tally),
            "pct_covered_by_game_text_referenced_words": round(100 * tier_tally["canon"] / n, 1),
            "missing_concepts": [r["concept"] for r in rows if r["status"] == "missing"],
            "partial_concepts": [r["concept"] for r in rows if r["status"] == "partial"],
            "concepts": rows,
        }

    # ---- supplementary statistics used by the forge rule proposals ----------
    forms = []
    for e in entries:
        for wf in e["word_forms"]:
            w = clean_form(wf)
            if w and re.fullmatch(r"[a-z']+", w):
                forms.append(w)
    form_count = Counter(forms)
    distinct = sorted(form_count)
    homographs = sorted(w for w, k in form_count.items() if k > 1)
    multi_gloss = sum(1 for e in entries if len(e["definitions"]) > 1)

    def neighbours(w, pool):
        k = 0
        for v in pool:
            if v == w or abs(len(v) - len(w)) > 1:
                continue
            if len(v) == len(w):
                if sum(a != b for a, b in zip(v, w)) == 1:
                    k += 1
            else:
                s, l = (v, w) if len(v) < len(w) else (w, v)
                if any(l[:i] + l[i + 1:] == s for i in range(len(l))):
                    k += 1
        return k
    nb = {w: neighbours(w, distinct) for w in distinct}
    by_len = {}
    for w, k in nb.items():
        by_len.setdefault(len(w), []).append(k)
    nb_by_len = {str(L): {"n_words": len(v), "mean_neighbours": round(sum(v) / len(v), 2),
                          "max": max(v), "share_with_zero": round(sum(1 for x in v if x == 0) / len(v), 3)}
                 for L, v in sorted(by_len.items())}

    tok = Counter()
    for rec in corpus["texts"]:
        if rec["type"] == "name" or rec.get("duplicate_of"):
            continue
        if not str(rec.get("canon_status", "")).startswith("canon"):
            continue
        for t in re.findall(r"[a-z']+", (rec.get("dovahzul") or "").lower()):
            tok[t.strip("'")] += 1
    in_lex = {w: c for w, c in tok.items() if w in form_count}
    ws = sorted(in_lex)
    rho = spearman([in_lex[w] for w in ws], [len(w) for w in ws])
    bands = {}
    for w in ws:
        f = in_lex[w]
        b = "f>=20" if f >= 20 else "f 5-19" if f >= 5 else "f 2-4" if f >= 2 else "f=1"
        bands.setdefault(b, []).append(len(w))
    band_len = {b: {"n_types": len(v), "mean_letters": round(sum(v) / len(v), 2)}
                for b, v in bands.items()}
    never = [len(w) for w in distinct if w not in tok]

    gloss_owner = {}
    for e in entries:
        for g in e["definitions"]:
            for n in norm_gloss(g):
                gloss_owner.setdefault(n, set()).add(e["word"])
    synonym_sets = {g: sorted(ws_) for g, ws_ in gloss_owner.items() if len(ws_) > 1}

    out = {
        "meta": {
            "generator": "tools/analysis/core_concept_gaps.py 1.0.0",
            "inputs": ["research/data/canon-lexicon.json", "research/data/canon-corpus.json"],
            "lexicon_revid": lex["meta"].get("revid"),
            "method": "Exact match of normalised dictionary glosses against hand-written "
                      "accept/near gloss sets per concept; see the script docstring.",
            "list_provenance": "All three lists were typed in from the analyst's knowledge of the "
                               "published lists, not downloaded; counts verified (207/100/65). "
                               "Diff against Concepticon before freezing.",
            "status_values": {
                "covered": "a dictionary gloss expresses the concept in the right word class",
                "partial": "only a hyponym, related word or other word class is glossed; human ruling needed",
                "missing": "no dictionary gloss matches"},
            "caveats": [
                "Glosses are the wiki's English; most are single words with no sense notes.",
                "'covered' says a word exists, not that its grammar or sense range is known.",
                "tier 'canon' = the row cites at least one game-text or in-game-book source; "
                "'semi-canon' = only Prima guide, Imperial Library list, press or game data.",
                "corpus_hover_gloss_only lists dragon-language strings that wiki editors glossed "
                "with the concept word in dialogue; fan-level evidence.",
            ],
        },
        "summary": {k: {f: v[f] for f in ("n_concepts", "covered", "partial", "missing", "pct_covered",
                                           "pct_covered_or_partial", "pct_missing", "covered_by_best_tier",
                                           "pct_covered_by_game_text_referenced_words")}
                    for k, v in out_lists.items()},
        "lists": out_lists,
        "supplementary_lexicon_statistics": {
            "note": "Descriptive statistics of canon spelling used to set forge defaults. "
                    "Lengths are in letters; neighbours are spellings one letter substitution, "
                    "insertion or deletion away.",
            "distinct_spellings": len(distinct),
            "homograph_spellings_listed_in_more_than_one_row": homographs,
            "rows_with_more_than_one_gloss": multi_gloss,
            "english_glosses_shared_by_more_than_one_row": len(synonym_sets),
            "examples_of_shared_glosses": dict(sorted(synonym_sets.items())[:40]),
            "neighbourhood_by_length": nb_by_len,
            "mean_neighbours_all": round(sum(nb.values()) / len(nb), 2),
            "zipf_length_frequency": {
                "basis": "dictionary spellings that occur as tokens in canon, non-duplicate, non-name corpus texts",
                "n_types": len(ws),
                "n_tokens": sum(in_lex.values()),
                "spearman_rho_frequency_vs_letters": round(rho, 3),
                "mean_letters_by_frequency_band": band_len,
                "dictionary_spellings_never_in_corpus": {
                    "n": len(never), "mean_letters": round(sum(never) / len(never), 2) if never else None},
                "top_20_tokens": tok.most_common(20),
            },
        },
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for k, v in out["summary"].items():
        print(k, json.dumps(v))
    s = out["supplementary_lexicon_statistics"]
    print("distinct", s["distinct_spellings"], "homographs", len(homographs), homographs[:15])
    print("shared glosses", s["english_glosses_shared_by_more_than_one_row"])
    print("neigh", json.dumps(nb_by_len))
    print("zipf", json.dumps({k: v for k, v in s["zipf_length_frequency"].items() if k != "basis"}))
    for k, v in out_lists.items():
        print(k, "MISSING:", ", ".join(v["missing_concepts"]))
        print(k, "PARTIAL:", ", ".join(v["partial_concepts"]))
        fanhits = [(r["concept"], r["corpus_hover_gloss_only"]) for r in v["concepts"]
                   if "corpus_hover_gloss_only" in r]
        print(k, "FAN-ONLY:", fanhits)


if __name__ == "__main__":
    sys.exit(main())
