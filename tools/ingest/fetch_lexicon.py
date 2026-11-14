#!/usr/bin/env python3
"""Fetch the wikitext of the UESP page Lore:Dragon_Language, politely.

Standard library only.  Re-runnable from the repository root:

    python3 tools/ingest/fetch_lexicon.py              # latest revision
    python3 tools/ingest/fetch_lexicon.py --revid N    # one exact revision

What it writes (and nothing else):

    research/sources/uesp/Lore_Dragon_Language.wikitext
        the raw wikitext, byte for byte as the API returned it (UTF-8)
    research/sources/uesp/manifest.d/Lore_Dragon_Language.json
        provenance: title, revid, timestamp, api_url, sha256, license, ...

How it behaves:

  * It talks only to the MediaWiki API at https://en.uesp.net/w/api.php.
  * It identifies itself as "research-client/1.0" and sends nothing else
    about who is running it.
  * It waits at least one second between calls and makes four calls
    (revision, wikitext, site licence, licence page).
  * The content call is pinned to a revision id (oldid=...), so the
    api_url in the provenance record returns the very same text later.
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
PAGE = "Lore:Dragon_Language"
MIN_INTERVAL_S = 1.0      # at least this long between two calls
TIMEOUT_S = 30
RETRY_WAIT_S = 25         # wait after a 429 / 5xx
MAX_RETRIES = 2

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "research" / "sources" / "uesp"

_last_call = [0.0]


def api_url(params):
    """Build the request URL.  Parameters are sorted so the URL is stable."""
    return API + "?" + urllib.parse.urlencode(sorted(params.items()), safe=":|")


def api_get(params):
    """GET one API URL and return (url, decoded JSON)."""
    url = api_url(params)
    for attempt in range(MAX_RETRIES + 1):
        wait = MIN_INTERVAL_S - (time.monotonic() - _last_call[0])
        if wait > 0:
            time.sleep(wait)
        request = urllib.request.Request(
            url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
        )
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:
                body = response.read()
            _last_call[0] = time.monotonic()
        except urllib.error.HTTPError as err:
            _last_call[0] = time.monotonic()
            if (err.code == 429 or 500 <= err.code < 600) and attempt < MAX_RETRIES:
                print("  HTTP %d, waiting %d s before retry %d of %d"
                      % (err.code, RETRY_WAIT_S, attempt + 1, MAX_RETRIES),
                      file=sys.stderr)
                time.sleep(RETRY_WAIT_S)
                continue
            raise SystemExit("HTTP %d from %s - stopping (not retried)." % (err.code, url))
        except urllib.error.URLError as err:
            _last_call[0] = time.monotonic()
            raise SystemExit("Network error for %s: %s" % (url, err.reason))
        data = json.loads(body.decode("utf-8"))
        if "error" in data:
            raise SystemExit("API error for %s: %s" % (url, json.dumps(data["error"])))
        return url, data
    raise SystemExit("Gave up on %s" % url)


def file_stem(title):
    """'Lore:Dragon Language' -> 'Lore_Dragon_Language' (safe file name)."""
    keep = []
    for ch in title.replace(" ", "_").replace(":", "_").replace("/", "_"):
        keep.append(ch if (ch.isalnum() or ch in "_-.") else "_")
    return "".join(keep)


def write_atomic(path, data):
    """Write bytes through a temporary file so readers never see half a file."""
    tmp = path.with_name(path.name + ".tmp%d" % os.getpid())
    with open(tmp, "wb") as handle:
        handle.write(data)
    os.replace(tmp, path)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--page", default=PAGE, help="page title (default: %(default)s)")
    parser.add_argument("--revid", type=int, default=None,
                        help="fetch this exact revision instead of the latest one")
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR,
                        help="output folder (default: research/sources/uesp)")
    args = parser.parse_args(argv)

    requests_made = []

    # 1. Which revision?  (ids, timestamp, MediaWiki's own SHA-1 and size)
    params = {"action": "query", "prop": "revisions",
              "rvprop": "ids|timestamp|sha1|size",
              "format": "json", "formatversion": "2"}
    if args.revid is None:
        params["titles"] = args.page
    else:
        params["revids"] = str(args.revid)
    url, data = api_get(params)
    requests_made.append(url)
    pages = data.get("query", {}).get("pages", [])
    if not pages or pages[0].get("missing") or not pages[0].get("revisions"):
        raise SystemExit("Page or revision not found: %s" % json.dumps(data)[:400])
    page = pages[0]
    revision = page["revisions"][0]
    revid = revision["revid"]
    print("page      : %s (pageid %s)" % (page["title"], page.get("pageid")))
    print("revision  : %s  %s" % (revid, revision["timestamp"]))

    # 2. The wikitext of exactly that revision.
    url, data = api_get({"action": "parse", "oldid": str(revid),
                         "prop": "wikitext|revid",
                         "format": "json", "formatversion": "2"})
    content_url = url
    requests_made.append(url)
    parsed = data["parse"]
    if parsed.get("revid") != revid:
        raise SystemExit("Asked for revision %s, got %s" % (revid, parsed.get("revid")))
    wikitext = parsed["wikitext"]
    raw = wikitext.encode("utf-8")

    sha1 = hashlib.sha1(raw).hexdigest()
    reported_sha1 = revision.get("sha1")
    if reported_sha1 and reported_sha1 != sha1:
        raise SystemExit("SHA-1 mismatch: MediaWiki says %s, received text has %s"
                         % (reported_sha1, sha1))
    sha256 = hashlib.sha256(raw).hexdigest()

    # 3. The site's content licence.
    url, data = api_get({"action": "query", "meta": "siteinfo",
                         "siprop": "rightsinfo|general", "format": "json"})
    requests_made.append(url)
    rights = data["query"].get("rightsinfo", {})
    general = data["query"].get("general", {})
    articlepath = general.get("articlepath", "/wiki/$1")
    server = general.get("server", "https://en.uesp.net")

    def wiki_link(title):
        return server + articlepath.replace(
            "$1", urllib.parse.quote(title.replace(" ", "_"), safe=":/_"))

    rights_page = rights.get("url") or ""
    if rights_page.startswith("http") or rights_page.startswith("//"):
        license_url = rights_page
    elif rights_page:
        license_url = wiki_link(rights_page)
    else:
        license_url = None

    # 4. The licence page itself, read only to find the link to the licence
    #    deed (the API gives the licence's name but not its address).  The
    #    page is not saved.  If this step fails the record just lacks the link.
    license_deed_url = None
    license_page_revid = None
    if rights_page and license_url and not rights_page.startswith(("http", "//")):
        try:
            url, data = api_get({"action": "parse", "page": rights_page.replace(" ", "_"),
                                 "prop": "wikitext|revid",
                                 "format": "json", "formatversion": "2"})
            requests_made.append(url)
            license_page_revid = data["parse"].get("revid")
            for word in data["parse"].get("wikitext", "").replace("[", " ").replace("]", " ").split():
                if word.startswith(("http://creativecommons.org/licenses/",
                                    "https://creativecommons.org/licenses/")):
                    license_deed_url = word
                    break
        except SystemExit as err:
            print("  licence page not read: %s" % err, file=sys.stderr)

    stem = file_stem(args.page)
    out_dir = args.out_dir
    manifest_dir = out_dir / "manifest.d"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    wikitext_path = out_dir / (stem + ".wikitext")
    manifest_path = manifest_dir / (stem + ".json")

    def shown(path):
        try:
            return path.resolve().relative_to(REPO_ROOT).as_posix()
        except ValueError:
            return str(path)

    manifest = {
        "title": page["title"],
        "revid": revid,
        "timestamp": revision["timestamp"],
        "api_url": content_url,
        "sha256": sha256,
        "license": rights.get("text"),
        # --- extra detail, beyond the six required fields ---
        "license_page": rights_page or None,
        "license_url": license_url,
        "license_deed_url": license_deed_url,
        "license_page_revid": license_page_revid,
        "pageid": page.get("pageid"),
        "parentid": revision.get("parentid"),
        "requested_title": args.page,
        "page_url": wiki_link(page["title"]),
        "permalink": "%s%s?oldid=%s" % (server, general.get("script", "/w/index.php"), revid),
        "sha1": sha1,
        "sha1_matches_mediawiki": bool(reported_sha1) and reported_sha1 == sha1,
        "bytes": len(raw),
        "chars": len(wikitext),
        "lines": wikitext.count("\n") + 1,
        "saved_as": shown(wikitext_path),
        "site": {"sitename": general.get("sitename"),
                 "server": server,
                 "generator": general.get("generator")},
        "requests": requests_made,
        "user_agent": USER_AGENT,
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fetched_by": "tools/ingest/fetch_lexicon.py",
    }

    write_atomic(wikitext_path, raw)
    write_atomic(manifest_path,
                 (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))

    print("licence   : %s (%s; deed %s)" % (manifest["license"], license_url, license_deed_url))
    print("wikitext  : %s  (%d chars, %d bytes)" % (shown(wikitext_path), len(wikitext), len(raw)))
    print("sha256    : %s" % sha256)
    print("sha1 check: %s" % ("matches MediaWiki" if manifest["sha1_matches_mediawiki"]
                              else "not reported by the API"))
    print("manifest  : %s" % shown(manifest_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
