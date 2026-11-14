#!/usr/bin/env python3
"""Fetch the UESP pages that carry canon dragon-language text, politely.

Standard library only.  Re-runnable from the repository root:

    python3 tools/ingest/fetch_corpus.py                 # fetch what is missing
    python3 tools/ingest/fetch_corpus.py --force         # re-fetch everything
    python3 tools/ingest/fetch_corpus.py --list          # print the page list
    python3 tools/ingest/fetch_corpus.py --discover      # re-run the discovery
                                                         # queries, print titles
                                                         # that are not in PAGES
    python3 tools/ingest/fetch_corpus.py "Skyrim:Tsun"   # fetch named pages only

What it writes (and nothing else), one pair of files per page:

    research/sources/uesp/<Title_with_underscores>.wikitext
        the raw wikitext, byte for byte as the API returned it (UTF-8)
    research/sources/uesp/manifest.d/<same name>.json
        provenance: title, revid, timestamp, api_url, sha256, license, ...

The page Lore:Dragon_Language (the dictionary) belongs to
tools/ingest/fetch_lexicon.py.  This script refuses to fetch or overwrite it.

How it behaves:

  * It talks only to the MediaWiki API at https://en.uesp.net/w/api.php.
  * It identifies itself as "research-client/1.0" and sends nothing else
    about who is running it.
  * It waits at least one second between calls.  Page text is requested in
    batches (several titles per call) so that a full run needs about thirty
    calls, not one per page.  --max-calls is a hard ceiling.  --discover makes about
    thirty more calls; it only prints titles and saves nothing.
  * Every provenance record carries an api_url pinned to the revision id, so
    that URL returns the very same text later, plus the batch URL that was
    actually requested.
  * On HTTP 429 or a 5xx it waits and retries at most twice.  On any other
    error (403 included) it stops: a refusal is respected, not worked around.
  * The SHA-1 that MediaWiki reports for the revision is compared with the
    SHA-1 of the text received, so a corrupted download is caught.

Everything downloaded is treated as data.  Nothing in it is executed.
"""

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://en.uesp.net/w/api.php"
USER_AGENT = "research-client/1.0"
MIN_INTERVAL_S = 1.1      # at least this long between two calls
TIMEOUT_S = 30
RETRY_WAIT_S = 25         # wait after a 429 / 5xx
MAX_RETRIES = 2
BATCH = 12                # titles per content call
FORBIDDEN = {"lore:dragon language"}   # owned by fetch_lexicon.py

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "research" / "sources" / "uesp"
MANIFEST_DIR = OUT_DIR / "manifest.d"

# ---------------------------------------------------------------------------
# The page list.  It was built on 2026-11-14 from: the links out of and the
# backlinks into Lore:Dragon_Language, full-text searches over every content
# namespace for "dragon language", "word wall" and a set of distinctive
# dragon-language words (ahrk, zu'u, nust, naal, voth, Dovahkiin, ...), and the
# shout and dragon categories.  --discover re-runs those queries.
# Each group names the kind of canon text the pages were chosen for.
# ---------------------------------------------------------------------------
PAGES = {
    # a. Word walls.  The inscriptions live in the {{WordWall}} template on each
    #    shout page (group "shouts") and again, per word, on Lore:Word Walls.
    "word_walls": [
        "Skyrim:Word Wall",
        "Lore:Word Walls",
        "Legends:Word Wall",
        "Online:Lendoran Ruin",
        "Lore:Hoar Father",
        # Added by the verification pass (2026-11-14): the two Lore place pages that
        # quote a word wall in a "Word Wall's translation" box.  Found with the
        # full-text search "Word Wall's translation"; both repeat walls that the
        # shout pages already give (Storm Call, Disarm).
        "Lore:Vundeheim",
        "Lore:Korvag Crag",
    ],
    # b. Shouts: the overview pages, then every member of
    #    Category:Skyrim-Dragon Shouts (player, dragon-only and NPC-only shouts).
    "shouts": [
        "Skyrim:Dragon Shouts",
        "Lore:Thu'um",
        "Skyrim:Animal Allegiance",
        "Skyrim:Aura Whisper",
        "Skyrim:Battle Fury",
        "Skyrim:Become Ethereal",
        "Skyrim:Bend Will",
        "Skyrim:Call Dragon",
        "Skyrim:Call of Valor",
        "Skyrim:Clear Skies",
        "Skyrim:Cyclone",
        "Skyrim:Disarm",
        "Skyrim:Dismay",
        "Skyrim:Dragon Aspect",
        "Skyrim:Dragonrend",
        "Skyrim:Drain Vitality",
        "Skyrim:Elemental Fury",
        "Skyrim:Fire Breath",
        "Skyrim:Frost Breath",
        "Skyrim:Ice Form",
        "Skyrim:Ice Storm (shout)",
        "Skyrim:Kyne's Peace",
        "Skyrim:Marked for Death",
        "Skyrim:Phantom Form",
        "Skyrim:Slow Time",
        "Skyrim:Soul Cairn Summon",
        "Skyrim:Soul Tear",
        "Skyrim:Storm Call",
        "Skyrim:Summon Durnehviir",
        "Skyrim:Throw Voice",
        "Skyrim:Unrelenting Force",
        "Skyrim:Vile Vapor",
        "Skyrim:Whirlwind Sprint",
        "Skyrim:Kinect Commands",
        "Skyrim:The Words of Power",
        "SkyrimVSE:Combat",
        "SkyrimVSE:Enemies",
        "General:Skyrim\u2019s Dragon Shouts",
    ],
    # c. The alphabet.
    "alphabet": [
        "Lore:Dragon Alphabet",
        "General:Fonts",
    ],
    # Templates that the pages above use to hold or render dragon text.
    "templates": [
        "Template:WordWall",
        "Template:WordWall/Doc",
        "Template:WordWallExt",
        "Template:DragonFont",
        "Template:DragonFont/Doc",
        "Template:Shout Summary",
    ],
    # d. Songs and verse, and in-game or official books with dragon text.
    "songs_and_books": [
        "Skyrim:Songs of Skyrim",
        "Skyrim:Songs of Skyrim: Revised",
        "Lore:Songs of Skyrim: Revised",
        "Lore:Songs",
        "Skyrim:Dragon Language: Myth no More",
        "Lore:Dragon Language: Myth no More",
        "Lore:Dragon Skull Parchment",
        "Online:Dragon Skull Parchment",
        "Lore:Wisdom of the Flying Gods",
        "Online:Wisdom of the Flying Gods",
        "Lore:Kireth's Taarengrav Note",
        "Online:Kireth's Taarengrav Note",
        "Lore:The History of Zaan the Scalecaller",
        "Lore:Olaf and the Dragon",
        "Lore:There Be Dragons",
        "Lore:The Guardian and the Traitor",
        "Lore:Holdings of Jarl Gjalund",
        "Lore:Whiterun Hold Jarl's Letter",
        "Lore:Return of the Dragons",
        "Lore:Loremaster's Archive - Dragons in the Second Era",
        "Lore:Loremaster's Archive - Malacath and Maelstrom",
        "Lore:Daedra Dossier: The Titans",
        "Lore:The Sublime Brazier",
        "Lore:War Weather",
        "Lore:Calcelmo's Stone",
        "Skyrim:Loading Screens",
        "Skyrim:Music",
        "Skyrim:Bards College",
        "Skyrim:Dragonstone",
        "Lore:Dragonstone",
        "Books:The Elder Scrolls V: Skyrim: Prima Official Game Guide",
        "General:Saltatio Mortis - Pray To The Hunter feat. \u201eThe Elder Scrolls Online\"",
        "Lore:Songs of the Return, Vol 19",
    ],
    # e. Dialogue: speakers, then the quests whose pages quote them.
    "dialogue": [
        "Skyrim:Paarthurnax (dragon)",
        "Skyrim:Alduin",
        "Skyrim:Odahviing",
        "Skyrim:Durnehviir (dragon)",
        "Skyrim:Miraak (person)",
        "Skyrim:Arngeir",
        "Skyrim:Einarth",
        "Skyrim:Borri",
        "Skyrim:Wulfgar",
        "Skyrim:Greybeards",
        "Skyrim:Tsun",
        "Skyrim:Mirmulnir",
        "Skyrim:Sahloknir",
        "Skyrim:Nahagliiv",
        "Skyrim:Viinturuth",
        "Skyrim:Vuljotnaak",
        "Skyrim:Vulthuryol",
        "Skyrim:Naaslaarum",
        "Skyrim:Voslaarum",
        "Skyrim:Sahrotaar",
        "Skyrim:Krosulhah",
        "Skyrim:Kruziikrel",
        "Skyrim:Relonikiv",
        "Skyrim:Dragon",
        "Skyrim:Skeletal Dragon",
        "Skyrim:Dragon Riding",
        "Skyrim:Draugr",
        "Skyrim:Dragon Priest",
        "Skyrim:Gormlaith Golden-Hilt",
        "Skyrim:Hakon One-Eye",
        "Skyrim:Felldir the Old",
        "Skyrim:Ulfric Stormcloak",
        "Skyrim:Farengar Secret-Fire",
        "Skyrim:Esbern",
        "Skyrim:Delphine",
        "Skyrim:Tharstan",
        "Skyrim:Jawanan",
        "Skyrim:Dovahkiin",
        "Skyrim:High Hrothgar",
        "Skyrim:Unbound",
        "Skyrim:Dragon Rising",
        "Skyrim:The Way of the Voice",
        "Skyrim:The Horn of Jurgen Windcaller",
        "Skyrim:A Blade in the Dark",
        "Skyrim:The Throat of the World",
        "Skyrim:Alduin's Bane",
        "Skyrim:Season Unending",
        "Skyrim:The Fallen",
        "Skyrim:The World-Eater's Eyrie",
        "Skyrim:Sovngarde (quest)",
        "Skyrim:Dragonslayer",
        "Skyrim:Paarthurnax (quest)",
        "Skyrim:Beyond Death",
        "Skyrim:Durnehviir (quest)",
        "Skyrim:The Temple of Miraak",
        "Skyrim:At the Summit of Apocrypha",
        "Skyrim:The Staff of Magnus",
        "Skyrim:Volskygge (quest)",
        "Skyrim:Easter Eggs",
        "Skyrim:Unobtainable Items",
        "Skyrim:Anniversary Edition",
        "Skyrim:Skuldafn",
        "Skyrim:Sovngarde (place)",
        "Skyrim:Hermaeus Mora",
        "Skyrim:Ralof",
        "Skyrim:Bergritte Battle-Born",
        "Skyrim:Elisif the Fair",
        "Skyrim:Nahkriin",
    ],
    # f. Names: dragons (Category:Lore-People-Dragon and the dragons the
    #    dictionary links to), dragon priests and their masks, places and terms
    #    for which the wiki states a dragon-language meaning.
    "names": [
        "Lore:Dragon",
        "Lore:Alduin",
        "Lore:Paarthurnax",
        "Lore:Odahviing",
        "Lore:Durnehviir",
        "Lore:Mirmulnir",
        "Lore:Sahloknir",
        "Lore:Nahagliiv",
        "Lore:Viinturuth",
        "Lore:Vuljotnaak",
        "Lore:Vulthuryol",
        "Lore:Naaslaarum",
        "Lore:Voslaarum",
        "Lore:Sahrotaar",
        "Lore:Krosulhah",
        "Lore:Kruziikrel",
        "Lore:Relonikiv",
        "Lore:Numinex",
        "Lore:Grahkrindrog",
        "Lore:Krahjotdaan",
        "Lore:Nahfahlaar",
        "Lore:Ahbiilok",
        "Lore:Boziikkodstrun",
        "Lore:Dukaanfinsot",
        "Lore:Joorahmaar",
        "Lore:Kaalgrontiid",
        "Lore:Laatvulon",
        "Lore:Lokkestiiz",
        "Lore:Maarselok",
        "Lore:Mulaamnir",
        "Lore:Nahviintaas",
        "Lore:Paarbahlot",
        "Lore:Thurvokun",
        "Lore:Vithrelnaak",
        "Lore:Yahgrondu",
        "Lore:Yolnahkriin",
        "Lore:Debudjen",
        "Lore:Dragonne Papr\u00e9",
        "Lore:Skakmat",
        "Lore:Tosh Raka",
        "Redguard:Nafaalilargus",
        "Daggerfall:Dragonish",
        "Lore:Dragonling",
        "Lore:Dragon Priest",
        "Lore:Dragon Priest Masks",
        "Lore:Dragon Cult",
        "Lore:Miraak",
        "Lore:Ahzidal",
        "Lore:Morokei",
        "Lore:Krosis",
        "Lore:Rahgot",
        "Lore:Labyrinthian",            # the wiki redirects Lore:Bromjunaar here
        "Skyrim:Bromjunaar Sanctuary",
        "Skyrim:Konahrik",
        "Skyrim:Krosis",
        "Skyrim:Ahzidal (creature)",
        "Skyrim:Dukaan (creature)",
        "Skyrim:Hevnoraak (creature)",
        "Skyrim:Krosis (creature)",
        "Skyrim:Morokei (creature)",
        "Skyrim:Nahkriin (creature)",
        "Skyrim:Otar the Mad",
        "Skyrim:Rahgot (creature)",
        "Skyrim:Vahlok the Jailor",
        "Skyrim:Vokun (creature)",
        "Skyrim:Volsung (creature)",
        "Skyrim:Zahkriisos (creature)",
        "Skyrim:Hevnoraak (item)",
        "Skyrim:Krosis (item)",
        "Skyrim:Morokei (item)",
        "Skyrim:Nahkriin (item)",
        "Skyrim:Vokun (item)",
        "Skyrim:Volsung (item)",
        "Lore:Dragonborn",
        "Lore:Last Dragonborn",
        "Lore:Way of the Voice",
        "Lore:Time Wound",
        "Lore:Throat of the World",
        "Lore:Kyne",
        "Lore:Shor",
        "Lore:Sun",
        "Lore:Elements",
        "Lore:Draugr",
        "Lore:Companions",
        "Lore:Nord",
        "Lore:Nordic",
        "Lore:Elder Scrolls",
        "Lore:Rorikstead",
        "Lore:Granite Hill",
        "Lore:Old Hroldan",
        "Lore:Ivarstead",
        "Lore:Whiterun",
        "Lore:Northwind Mine",
        "Lore:Forgotten Vale",
        "Lore:Ja'darri",
        "Lore:Fa-Nuit-Hen",
        "Lore:Scaleborn",
        "Lore:Other Minerals",
        "Lore:Akatosh",
        "Lore:Arngeir",
        "Lore:Skuldafn",
        "Lore:Ysgramor",
    ],
    # g. Other official titles and publications.
    "other_titles": [
        "Online:Dragon",
        "Online:The Dragon",
        "Online:Nahfahlaar",
        "Online:Laatvulon",
        "Online:Kaalgrontiid",
        "Online:Nahviintaas",
        "Online:Bahlokdaan",
        "Online:Mulaamnir",
        "Online:Joorahmaar",
        "Online:Lokkestiiz",
        "Online:Yolnahkriin",
        "Online:Vahlokzin",
        "Online:Sahrotnax",
        "Online:Maarselok",
        "Online:Thurvokun",
        "Online:Paarbahlot",
        "Online:Krahnoviir",
        "Online:Yahgrondu",
        "Online:Korthor",
        "Online:Ja'darri",
        "Online:The Dragon's Lair",
        "Online:Dragonhold",
        "Online:Zaan the Scalecaller",
        "Online:Dovah's Du'ul Style",
        "Online:Yoltoor Dovah-Fly",
        "Online:Green Dragon Imp",
        "Online:Blue Dragon Imp",
        "Online:Regal Dragon Imp",
        "Online:Dwarven Bear",
        "Online:Elder Scrolls Historical References",
        "Online:Chevalier Renald",
        "Online:Yolnahkriin (Infinite Archive)",
        "Online:Arch-Mage Shalidor",
        "Online:Captive (Weaver's Nest)",
        "Online:Legendary Companion",
        "Online:Valdur",
        "Legends:Odahviing",
        "Legends:Miraak, Dragonborn",
        "Legends:Greybeard Mentor",
        "Legends:Studious Greybeard",
        "Legends:Voice of Balance",
        "Legends:Nahkriin, Dragon Priest",
        "Legends:Stormcloak Avenger",
        "Legends:Shouts",
        "Legends:Paarthurnax",
        "Legends:Alduin",
        "Legends:Paarthurnax's Roar",
        "Legends:Dovah of the Voice",
        "Legends:Card Lore",
        "Legends:Heroes of Skyrim",
        "Legends:Call Dragon",
        "Legends:Call of Valor",
        "Legends:Dragon Aspect",
        "Legends:Drain Vitality",
        "Legends:Fire Breath",
        "Legends:Soul Tear",
        "Legends:Unrelenting Force",
        "Blades:Facing the Dragon",
        "Blades:Shulkunaak",
        "Blades:Dragon",
        "General:The Elder Scrolls V: Skyrim Announcement Trailer",
        "General:The Elder Scrolls V: Skyrim - Official Trailer",
        "General:Behind the Wall: The Making of Skyrim",
        "General:Skyrim Fan Interview",
        "General:Emil Pagliarulo",
        "General:Elsweyr & Update 22 AUA",
        "General:Elsweyr Burns \u2013 Dragons In The Elder Scrolls Online",
        "General:ESOU Podcast ft. ESO Loremaster Michael Zenke",
        "General:A Matter of Voice and Brass: Dragon Bones DLC Interview",
        "General:Ehlnofex Languages",
        "Merchandise:Skyrim Limited Edition Dragonstone Replica",
        "Merchandise:Thu'um Master Blazer",
        "Merchandise:Skyrim Limited Edition Coin 1",
        "Merchandise:The Elder Scrolls Whiterun Honorary Citizen Chest",
    ],
}

# Titles that the discovery queries returned (as links from Lore:Dragon_Language) but that did
# not exist on the wiki on 2026-11-14 (red links).  Kept here so the gap is on record.
NOT_ON_WIKI = [
    "Lore:Songs of Skyrim", "Lore:Kahvozein", "Lore:Lodunost", "Lore:Krahnoviir",
    "Lore:Bahlokdaan", "Lore:Vahlokzin", "Lore:Shulkunaak", "Lore:Sahrotnax", "Lore:Vahlok",
]
# Redirects met on the way: Lore:Bromjunaar -> Lore:Labyrinthian (fetched under the target's
# name); Skyrim:Dragon Storm Call, Skyrim:ResurrectionShout and Skyrim:Steam Breath all lead to
# Skyrim:Dragon Shouts, which is in the list under its own name.

_last_call = [0.0]
_calls = [0]
_max_calls = [60]


def log(msg):
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()


def api_url(params):
    """Build the request URL.  Parameters are sorted so the URL is stable."""
    return API + "?" + urllib.parse.urlencode(sorted(params.items()), safe=":|")


def api_get(params):
    """One polite GET to the API.  Returns (parsed JSON, url)."""
    params = dict(params)
    params.setdefault("format", "json")
    params.setdefault("formatversion", "2")
    url = api_url(params)
    if not url.startswith(API + "?"):
        raise RuntimeError("refusing to call anything but the UESP API")
    attempt = 0
    while True:
        if _calls[0] >= _max_calls[0]:
            raise RuntimeError("call ceiling reached (%d); stopping" % _max_calls[0])
        wait = MIN_INTERVAL_S - (time.monotonic() - _last_call[0])
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        _calls[0] += 1
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
                raw = resp.read()
            _last_call[0] = time.monotonic()
            data = json.loads(raw.decode("utf-8"))
            if isinstance(data, dict) and "error" in data:
                raise RuntimeError("API error: %s" % json.dumps(data["error"])[:300])
            return data, url
        except urllib.error.HTTPError as exc:
            _last_call[0] = time.monotonic()
            if exc.code in (429, 500, 502, 503, 504) and attempt < MAX_RETRIES:
                attempt += 1
                log("HTTP %d; waiting %ds (retry %d of %d)"
                    % (exc.code, RETRY_WAIT_S, attempt, MAX_RETRIES))
                time.sleep(RETRY_WAIT_S)
                continue
            raise RuntimeError("HTTP %d from the API; stopping (%s)" % (exc.code, url))


def safe_name(title):
    """Lore:Dragon Alphabet -> Lore_Dragon_Alphabet (file-system safe)."""
    out = []
    for ch in title:
        if ch in " :/":
            out.append("_")
        elif ch in '\\?*"<>|%' or ord(ch) < 32:
            out.append("%%%02X" % ord(ch))
        else:
            out.append(ch)
    return "".join(out)


def all_titles():
    seen, out = set(), []
    for group in PAGES.values():
        for t in group:
            if t not in seen:
                seen.add(t)
                out.append(t)
    return out


def group_of(title):
    return [g for g, ts in PAGES.items() if title in ts]


def already_have(title):
    name = safe_name(title)
    return (OUT_DIR / (name + ".wikitext")).exists() and \
        (MANIFEST_DIR / (name + ".json")).exists()


def site_info():
    data, url = api_get({"action": "query", "meta": "siteinfo",
                         "siprop": "rightsinfo|general"})
    q = data.get("query", {})
    rights = q.get("rightsinfo", {})
    gen = q.get("general", {})
    return {
        "license": rights.get("text", ""),
        "license_page": rights.get("url", ""),
        "site": {"sitename": gen.get("sitename", ""), "server": gen.get("server", ""),
                 "generator": gen.get("generator", "")},
        "request": url,
    }


def write_page(page, requested, batch_url, info, fetched_at):
    title = page["title"]
    if title in all_titles():
        requested = title
    if title.lower().replace("_", " ") in FORBIDDEN:
        log("  skip (owned by fetch_lexicon.py): %s" % title)
        return None
    rev = page["revisions"][0]
    slot = rev.get("slots", {}).get("main", rev)
    text = slot.get("content")
    if text is None:
        return None
    raw = text.encode("utf-8")
    sha1 = hashlib.sha1(raw).hexdigest()
    name = safe_name(title)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / (name + ".wikitext")).write_bytes(raw)
    pinned = api_url({"action": "query", "format": "json", "formatversion": "2",
                      "prop": "revisions", "revids": str(rev["revid"]),
                      "rvprop": "ids|timestamp|sha1|content", "rvslots": "main"})
    server = info["site"].get("server") or "https://en.uesp.net"
    lic_page = info.get("license_page", "")
    manifest = {
        "title": title,
        "revid": rev["revid"],
        "timestamp": rev["timestamp"],
        "api_url": pinned,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "license": info.get("license", ""),
        "license_page": lic_page,
        "license_url": (server + "/wiki/" + lic_page.replace(" ", "_")) if lic_page else "",
        "pageid": page.get("pageid"),
        "ns": page.get("ns"),
        "parentid": rev.get("parentid"),
        "requested_title": requested,
        "redirected_from": requested if requested != title else None,
        "page_url": server + "/wiki/" + urllib.parse.quote(title.replace(" ", "_"), safe=":/()',"),
        "permalink": "%s/w/index.php?oldid=%d" % (server, rev["revid"]),
        "sha1": rev.get("sha1"),
        "sha1_matches_mediawiki": (rev.get("sha1") == sha1) if rev.get("sha1") else None,
        "bytes": len(raw),
        "chars": len(text),
        "lines": text.count("\n") + 1,
        "saved_as": "research/sources/uesp/" + name + ".wikitext",
        "groups": group_of(requested) or group_of(title),
        "site": info.get("site", {}),
        "requests": [batch_url, info.get("request", "")],
        "api_url_note": "api_url is pinned to the revision id and returns this exact "
                        "text; the text was actually received through the batch call "
                        "listed first under requests.",
        "user_agent": USER_AGENT,
        "fetched_at": fetched_at,
        "fetched_by": "tools/ingest/fetch_corpus.py",
    }
    (MANIFEST_DIR / (name + ".json")).write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if manifest["sha1_matches_mediawiki"] is False:
        log("  WARNING sha1 mismatch for %s" % title)
    return manifest


def fetch(titles, force=False):
    todo = []
    for t in titles:
        if t.lower().replace("_", " ") in FORBIDDEN:
            log("skip (owned by fetch_lexicon.py): %s" % t)
            continue
        if not force and already_have(t):
            continue
        todo.append(t)
    if not todo:
        log("nothing to fetch; %d page(s) already on disk" % len(titles))
        return [], [], {}
    info = site_info()
    got, missing, redirects = [], [], {}
    pending = list(todo)
    rounds = 0
    while pending and rounds < 200:
        rounds += 1
        batch, pending = pending[:BATCH], pending[BATCH:]
        data, url = api_get({
            "action": "query", "prop": "revisions", "redirects": "1",
            "rvprop": "ids|timestamp|sha1|size|content", "rvslots": "main",
            "titles": "|".join(batch),
        })
        fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        q = data.get("query", {})
        back = {}                      # resolved title -> requested title
        for n in q.get("normalized", []):
            back[n["to"]] = n["from"]
        for r in q.get("redirects", []):
            back[r["to"]] = back.get(r["from"], r["from"])
            redirects[back[r["to"]]] = r["to"]
        done_requested = set()
        for page in q.get("pages", []):
            requested = back.get(page["title"], page["title"])
            if page.get("missing") or page.get("invalid"):
                missing.append(requested)
                done_requested.add(requested)
                log("  MISSING %s" % requested)
                continue
            revs = page.get("revisions")
            if not revs:
                continue               # truncated batch: ask again below
            m = write_page(page, requested, url, info, fetched_at)
            if m:
                got.append(m)
                done_requested.add(requested)
                log("  ok  %-55s rev %-8d %7d bytes" % (m["title"], m["revid"], m["bytes"]))
        # several requested titles can resolve to one page through redirects
        for t in batch:
            if t in redirects and redirects[t] in [g["title"] for g in got]:
                done_requested.add(t)
        again = [t for t in batch if t not in done_requested]
        if again:
            if len(batch) == 1:
                missing.extend(again)
                log("  GAVE UP %s" % again[0])
            else:
                pending = again + pending
    return got, missing, redirects


# ---------------------------------------------------------------------------
# Discovery: the queries that produced PAGES.  Prints titles, saves nothing.
# ---------------------------------------------------------------------------
CONTENT_NS = "0|10|14|118|130|134|140|144|146|150|152|158|162|164|166|182|184"
SEARCH_TERMS = [
    '"dragon language"', '"word wall"', "ahrk", "zu'u", "nust", "naal", "voth", "Dovahkiin",
    '"drem yol lok"', "Thuri", "joorre OR joor", "dovah", "Dovahzul",
    "zeymah OR pruzah OR lingrah OR kogaan OR unslaad OR meyz OR vahzah OR fahdon OR geh",
    '"Sovngarde Song" OR "Song of the Dragonborn" OR "Dragon Poem"',
    "krosis OR krif OR sahrot OR dreh OR faal OR suleyk OR mulaag",
    '"dragon tongue" OR "dragon script" OR "draconic" OR "tongue of the dragons"',
    '"in the dragon language" OR "dragon language for" OR "in dragon language" OR "dragon-tongue"',
    "Kaaz OR sosmir OR Fenjuntiid OR Dovahzin OR Bormahu OR krentiid OR volaanne OR wundunne "
    "OR nikrent OR koraav",
    '"Fus Ro Dah" OR "Yol Toor Shul" OR "Wuld Nah Kest" OR "Krii Lun Aus" OR "Joor Zah Frul" '
    'OR "Zun Haal Viik" OR "Strun Bah Qo" OR "Tiid Klo Ul" OR "Fo Krah Diin" OR "Lok Vah Koor"',
    "ahkrin OR krif OR unslaad OR hokoron OR nahkriin OR dinok OR dilon OR kendov OR suleyk "
    "OR mulaag",
    "thuri OR joor OR joorre OR nivahriin OR pahlok OR vahzah OR geh OR nid OR pruzah OR bahlok",
]
CATEGORIES = [
    "Category:Skyrim-Dragon Shouts", "Category:Skyrim-Dragon Shouts-Words of Power",
    "Category:Lore-People-Dragon", "Category:Skyrim-Creatures-Monsters-Dragon",
    "Category:Skyrim-Creatures-Undead-Dragon Priest", "Category:Online-Creatures-Dragon",
    "Category:Blades-Dragon", "Category:Legends-Cards-Action-Shouts",
]


def discover():
    found = {}

    def add(title, why):
        found.setdefault(title, []).append(why)

    data, _ = api_get({"action": "query", "titles": "Lore:Dragon_Language",
                       "prop": "links", "pllimit": "max"})
    for page in data["query"]["pages"]:
        for link in page.get("links", []):
            add(link["title"], "linked from Lore:Dragon Language")
    cont = {}
    while True:
        params = {"action": "query", "list": "backlinks", "bllimit": "max",
                  "bltitle": "Lore:Dragon_Language", "blredirect": "1"}
        params.update(cont)
        data, _ = api_get(params)
        for b in data["query"]["backlinks"]:
            add(b["title"], "links to Lore:Dragon Language")
        if "continue" not in data:
            break
        cont = data["continue"]
    for term in SEARCH_TERMS:
        data, _ = api_get({"action": "query", "list": "search", "srsearch": term,
                           "srnamespace": CONTENT_NS, "srlimit": "500",
                           "srprop": "size"})
        for r in data["query"]["search"]:
            add(r["title"], "search: " + term)
    for cat in CATEGORIES:
        data, _ = api_get({"action": "query", "list": "categorymembers",
                           "cmtitle": cat, "cmlimit": "max"})
        for m in data["query"]["categorymembers"]:
            add(m["title"], "member of " + cat)
    have = set(all_titles())
    for title in sorted(found):
        mark = "have" if title in have else "    "
        print("%s\t%s\t%s" % (mark, title, "; ".join(sorted(set(found[title])))))
    log("%d titles found, %d of them in PAGES" % (len(found), len(have & set(found))))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("titles", nargs="*", help="fetch only these titles")
    ap.add_argument("--force", action="store_true", help="re-fetch pages already on disk")
    ap.add_argument("--list", action="store_true", help="print the page list and exit")
    ap.add_argument("--discover", action="store_true", help="re-run the discovery queries")
    ap.add_argument("--max-calls", type=int, default=60, help="hard ceiling on API calls")
    args = ap.parse_args()
    _max_calls[0] = args.max_calls
    if args.list:
        for group, titles in PAGES.items():
            for t in titles:
                print("%s\t%s" % (group, t))
        return 0
    if args.discover:
        discover()
        log("API calls made: %d" % _calls[0])
        return 0
    titles = args.titles or all_titles()
    got, missing, redirects = fetch(titles, force=args.force)
    log("fetched %d page(s); %d missing; %d redirect(s) followed; API calls made: %d"
        % (len(got), len(missing), len(redirects), _calls[0]))
    for src, dst in sorted(redirects.items()):
        log("  redirect  %s -> %s" % (src, dst))
    for t in missing:
        log("  missing   %s" % t)
    return 0


if __name__ == "__main__":
    sys.exit(main())
