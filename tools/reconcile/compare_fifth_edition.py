"""Compare the wiki dictionary with a parsed Fifth Edition and write the
facts-only reconciliation file.

    python3 -I tools/reconcile/compare_fifth_edition.py \
        research/data/canon-lexicon.json parsed.json \
        research/data/fifth-edition-reconciliation.json

What is written: for each wiki entry, whether the Fifth Edition has it and
what kind of official source the Fifth Edition cites for its definition; the
Fifth Edition headwords the wiki lacks, with the same source kinds; and pairs
that look like spelling variants. Nothing the Fifth Edition's authors wrote
(pronunciations, word types, expanded definitions, notes, examples) is copied.
"""
import collections, json, re, sys
L = json.load(open(sys.argv[1], encoding='utf-8'))
T = json.load(open(sys.argv[2], encoding='utf-8'))
ents = T['entries']
def norm(w): return re.sub(r"[^a-z]", "", w.lower())
def forms_of(e):
    out = set()
    for f in (e.get('word_forms') or [e['word']]):
        m = re.match(r"^(.*?)\((.*?)\)(.*)$", f)
        if m:
            out.add(norm(m.group(1) + m.group(3))); out.add(norm(m.group(1) + m.group(2) + m.group(3)))
        else:
            out.add(norm(f))
    return {x for x in out if x}
NONGAME = {'Prima', 'TIL', 'GI', 'BN', 'RelivingSkyrim', 'DBgamedata'}
def wiki_class(refs):
    r = set(refs or [])
    if not r: return 'no_source'
    if r - NONGAME: return 'game_text'
    if r == {'Prima'}: return 'guide_only'
    if r == {'TIL'}: return 'untraced_list_only'
    if 'DBgamedata' in r: return 'game_data'
    return 'other'
def level(ms):
    ks = set(k for m in ms for k in m['source_kinds'])
    if ks & {'dialogue_file', 'book', 'shout_menu'}: return 'game_files_or_books'
    if 'prima_guide' in ks: return 'printed_guide'
    if 'primagames_com' in ks: return 'guide_website_only'
    return 'no_official_definition_cited'
def ed(a, b):
    dp = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        prev = dp[0]; dp[0] = i
        for j, cb in enumerate(b, 1):
            cur = dp[j]; dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + (ca != cb)); prev = cur
    return dp[-1]
tw = collections.defaultdict(list)
for e in ents: tw[norm(e['word'])].append(e)
rows = []; matched = set()
for e in L['entries']:
    ms = []
    for f in sorted(forms_of(e)):
        if f in tw: ms += tw[f]; matched.add(f)
    rows.append({'word': e['word'], 'wiki_source_class': wiki_class(e.get('refs')), 'in_fifth_edition': bool(ms),
                 'fifth_edition_headwords': sorted({m['word'] for m in ms}),
                 'fifth_edition_definition_source': level(ms) if ms else None,
                 'fifth_edition_source_kinds': sorted({k for m in ms for k in m['source_kinds']})})
only5 = [{'word': e['word'], 'source_kinds': e['source_kinds'], 'definition_source': level([e])}
         for e in ents if norm(e['word']) not in matched]
variants = []
for r in rows:
    if r['in_fifth_edition']: continue
    a = norm(r['word'].split('(')[0])
    for o in only5:
        b = norm(o['word'])
        if a and b and a[0] == b[0] and ed(a, b) == 1 and min(len(a), len(b)) >= 5:
            variants.append({'wiki': r['word'], 'fifth_edition': o['word']})
cross = collections.Counter((r['wiki_source_class'], r['fifth_edition_definition_source'] or 'not_in_fifth_edition') for r in rows)
out = {
    'meta': {
        'what': 'Entry-by-entry comparison of the wiki dictionary (canon-lexicon.json) with the Dragon Language Dictionary, Fifth Edition, published by Thuum.org.',
        'fifth_edition_copy': 'Supplied by the project owner as a Word file on 2026-11-15. Not stored in this repository: it states no licence.',
        'kept_here': 'Facts only: which words each source lists, the kind of official source the Fifth Edition cites for a definition, and likely spelling variants.',
        'not_kept_here': 'Pronunciations, word types, expanded definitions, notes, etymologies and examples, which are the Fifth Edition authors\' own work.',
        'source_kinds': {'dialogue_file': 'developer notes in the game\'s dialogue file', 'book': 'an in-game book', 'shout_menu': 'the in-game Shouts menu',
                         'prima_guide': 'the printed official guide, Legendary Edition', 'primagames_com': 'the guide publisher\'s online word list', 'other': 'a parenthesis that is not a citation'},
        'limits': 'The copy was a PDF converted to Word; 646 of the 647 entries it says it has were identified, one region by hand. Source kinds were read by pattern and not checked entry by entry.',
        'counts': {'wiki_entries': len(rows), 'wiki_entries_in_fifth_edition': sum(r['in_fifth_edition'] for r in rows),
                   'wiki_entries_not_in_fifth_edition': sum(not r['in_fifth_edition'] for r in rows),
                   'fifth_edition_entries_identified': len(ents), 'fifth_edition_entries_not_in_wiki': len(only5)},
        'wiki_class_by_fifth_edition_source': {a + ' -> ' + b: n for (a, b), n in sorted(cross.items())},
    },
    'wiki_entries': rows, 'only_in_fifth_edition': only5, 'likely_spelling_variants': variants,
}
json.dump(out, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(sys.argv[3], 'a').write('\n')
print(json.dumps(out['meta']['counts'])); print(json.dumps(out['meta']['wiki_class_by_fifth_edition_source'], indent=0)); print(variants)
