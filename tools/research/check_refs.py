#!/usr/bin/env python3
"""Bulk-verify a bibliography against Crossref and the DOI registry.

Every research report in research/ carries a machine-readable reference list
in research/refs/<key>.json. This script checks that each cited work really
exists and that the cited title, year and first author match the registry
record, so that no invented or garbled citation survives into a report.

Usage (from the repository root):

    python3 tools/research/check_refs.py research/refs/<key>.json

Input: a JSON list of objects:

    {"id": "cepeda2006",            # short handle used in the report
     "type": "article",             # article | chapter | book | proceedings |
                                    # preprint | thesis | legal | web | other
     "authors": "Cepeda, N. J.; Pashler, H.; Vul, E.",   # family name first
     "year": 2006,
     "title": "Distributed practice in verbal recall tasks ...",
     "venue": "Psychological Bulletin",
     "doi": "10.1037/0033-2909.132.3.354",   # omit or null when unknown
     "url": null}

Output: research/refs/<key>.check.json plus a table on stdout. Statuses:

    verified          DOI exists; title, year and first author all match
    mismatch          DOI exists but the record differs (see "registry")
    found             no DOI was given; a confident match was found (see
                      "suggested_doi") -- add the DOI to the entry
    doi_resolves      DOI exists outside Crossref (e.g. DataCite); existence
                      confirmed, metadata NOT compared
    doi_not_found     the DOI does not exist; best title matches are listed
    not_found         nothing in Crossref matches confidently. For books this
                      is common and proves nothing: confirm another way.
    manual            legal / web / other: confirm by search, not by registry
    error             network failure; re-run

Exit status is 1 when any entry is mismatch, doi_not_found or error.
Standard library only. One request per second, generic client name.
"""
import difflib
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

UA = "research-client/1.0"
CROSSREF = "https://api.crossref.org/works"
DOI_HANDLE = "https://doi.org/api/handles/"
DELAY = 1.0
TITLE_OK = 0.82      # similarity needed to accept a title as the same work
TITLE_FOUND = 0.88   # stricter when we had no DOI to anchor on
MANUAL_TYPES = {"legal", "web", "other"}

_last_call = [0.0]


def _get(url, timeout=30, tries=3):
    """GET a JSON document politely. Returns (status_code, parsed_or_None)."""
    for attempt in range(tries):
        wait = DELAY - (time.time() - _last_call[0])
        if wait > 0:
            time.sleep(wait)
        _last_call[0] = time.time()
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as err:
            if err.code == 404:
                return 404, None
            if err.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                time.sleep(8 * (attempt + 1))
                continue
            return err.code, None
        except Exception:
            if attempt < tries - 1:
                time.sleep(5 * (attempt + 1))
                continue
            return 0, None
    return 0, None


def norm(text):
    """Lower-case, strip accents, markup and punctuation for comparison."""
    text = unicodedata.normalize("NFKD", str(text or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return " ".join(text.split())


def similarity(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    # A cited title is often the registry title without its subtitle (or the
    # reverse). Accept that when the shorter one is a real title, not a stub.
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    if len(short) >= 25 and long_.startswith(short):
        ratio = max(ratio, 0.9)
    return ratio


def first_family(authors):
    """Family name of the first author from 'Family, G.; Family, G.' text."""
    first = re.split(r";|\band\b|&", str(authors or ""))[0].strip()
    if "," in first:
        first = first.split(",")[0]
    else:
        parts = first.split()
        first = parts[-1] if parts else ""
    return norm(first)


def summarise(item):
    """Reduce a Crossref work record to the fields we compare and report."""
    titles = item.get("title") or []
    subtitles = item.get("subtitle") or []
    title = titles[0] if titles else ""
    if subtitles and subtitles[0] and norm(subtitles[0]) not in norm(title):
        title = title + ": " + subtitles[0]
    year = None
    for key in ("published-print", "published-online", "published", "issued", "created"):
        parts = (item.get(key) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            year = parts[0][0]
            break
    people = item.get("author") or item.get("editor") or []
    families = [p.get("family") or p.get("name") or "" for p in people]
    venue = (item.get("container-title") or [""])[0]
    return {
        "doi": item.get("DOI"),
        "title": title,
        "year": year,
        "authors": "; ".join(f for f in families if f),
        "venue": venue,
        "type": item.get("type"),
    }


def compare(ref, record):
    """List the ways a cited reference differs from a registry record."""
    problems = []
    if similarity(ref.get("title"), record["title"]) < TITLE_OK:
        problems.append("title differs")
    try:
        cited_year = int(str(ref.get("year"))[:4])
    except (TypeError, ValueError):
        cited_year = None
    if cited_year and record["year"] and abs(cited_year - int(record["year"])) > 1:
        problems.append("year differs (registry %s)" % record["year"])
    family = first_family(ref.get("authors"))
    registry_families = [norm(f) for f in record["authors"].split(";")]
    if family and registry_families and registry_families != [""]:
        if not any(family == f or family in f or f in family for f in registry_families if f):
            problems.append("first author not among registry authors")
    return problems


def search(ref, rows=4):
    """Bibliographic search in Crossref; returns candidate records, best first."""
    query = " ".join(str(x) for x in (ref.get("title"), first_family(ref.get("authors")), ref.get("year")) if x)
    url = CROSSREF + "?" + urllib.parse.urlencode({"query.bibliographic": query, "rows": rows})
    status, data = _get(url)
    if status != 200 or not data:
        return None
    items = (data.get("message") or {}).get("items") or []
    cands = [summarise(i) for i in items]
    for c in cands:
        c["similarity"] = round(similarity(ref.get("title"), c["title"]), 3)
    cands.sort(key=lambda c: c["similarity"], reverse=True)
    return cands


def check(ref):
    out = {"id": ref.get("id"), "cited": {k: ref.get(k) for k in ("authors", "year", "title", "venue", "doi", "type")}}
    kind = str(ref.get("type") or "").lower()
    doi = str(ref.get("doi") or "").strip()
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi, flags=re.I)

    if doi:
        status, data = _get(CROSSREF + "/" + urllib.parse.quote(doi, safe="/"))
        if status == 200 and data:
            record = summarise(data.get("message") or {})
            out["registry"] = record
            problems = compare(ref, record)
            out["status"] = "mismatch" if problems else "verified"
            if problems:
                out["problems"] = problems
            return out
        if status == 404:
            h_status, h_data = _get(DOI_HANDLE + urllib.parse.quote(doi, safe="/"))
            if h_status == 200 and h_data and h_data.get("responseCode") == 1:
                out["status"] = "doi_resolves"
                out["note"] = "DOI is registered outside Crossref; metadata not compared"
                return out
            out["status"] = "doi_not_found"
            out["candidates"] = (search(ref) or [])[:3]
            return out
        out["status"] = "error"
        out["note"] = "Crossref returned HTTP %s" % status
        return out

    if kind in MANUAL_TYPES:
        out["status"] = "manual"
        return out

    cands = search(ref)
    if cands is None:
        out["status"] = "error"
        out["note"] = "Crossref search failed"
        return out
    for cand in cands:
        if cand["similarity"] >= TITLE_FOUND and not compare(ref, cand):
            out["status"] = "found"
            out["suggested_doi"] = cand["doi"]
            out["registry"] = cand
            return out
    out["status"] = "not_found"
    out["candidates"] = cands[:3]
    return out


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    path = argv[1]
    with open(path, encoding="utf-8") as handle:
        refs = json.load(handle)
    if not isinstance(refs, list):
        print("Input must be a JSON list of reference objects.")
        return 2

    results = []
    for ref in refs:
        result = check(ref)
        results.append(result)
        line = "%-14s %-22s %s" % (result["status"], str(result.get("id"))[:22], str(ref.get("title"))[:70])
        if result.get("problems"):
            line += "\n" + " " * 15 + "-> " + "; ".join(result["problems"])
            reg = result.get("registry") or {}
            line += "\n" + " " * 15 + "   registry: %s (%s) %s" % (reg.get("authors", "")[:50], reg.get("year"), str(reg.get("title"))[:70])
        if result["status"] in ("doi_not_found", "not_found") and result.get("candidates"):
            best = result["candidates"][0]
            line += "\n" + " " * 15 + "   closest: %s (%s) %s [%s] sim=%s" % (
                best.get("authors", "")[:40], best.get("year"), str(best.get("title"))[:60], best.get("doi"), best.get("similarity"))
        if result["status"] == "found":
            line += "\n" + " " * 15 + "   add doi: %s" % result.get("suggested_doi")
        print(line, flush=True)

    counts = {}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1
    out_path = re.sub(r"\.json$", "", path) + ".check.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump({"source": path, "counts": counts, "results": results}, handle, indent=1, ensure_ascii=False)
        handle.write("\n")
    print("\n" + ", ".join("%s: %d" % (k, v) for k, v in sorted(counts.items())))
    print("written: " + out_path)
    bad = sum(counts.get(k, 0) for k in ("mismatch", "doi_not_found", "error"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
