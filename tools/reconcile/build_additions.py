"""Build the list of words added to the project's vocabulary from the Fifth
Edition, under the ruling recorded as proposal 3 in docs/decisions-log.md.

    python3 -I tools/reconcile/build_additions.py research/data/fifth-edition.json \
        research/data/canon-lexicon.json research/data/canon-corpus.json \
        research/data/lexicon-additions.json
"""
import json, re, sys
F = json.load(open(sys.argv[1], encoding='utf-8'))
L = json.load(open(sys.argv[2], encoding='utf-8'))
C = json.load(open(sys.argv[3], encoding='utf-8'))
fe = {e['word']: e for e in F['entries']}
GAME = ['Alok-Dilon', 'Bormahu', 'Dovahsebrom', 'Gaaffesejul', 'Sossedov', 'Tiid-Ahraan', 'Ulse', 'Vomir', 'Vosaraan', 'Wuldsetiid']
GUIDE = ['Rahgron', 'Suleykaar']
WEB = ['Kras', 'Saan', 'Sahsun', 'Sik', 'Viidost', 'Vu']
NAMES = ['Ahroldan', 'Ahrolsedovah', 'Bromjunaar', 'Hillgrundhofkah', 'Korvanjund', 'Quethsegol Ahrol', 'Rorikhofkah', 'Volunruud', 'Alikr', 'Oblivion', 'Sovngarde']
SEEN_ONLY = ['Dohaviin', 'Sadonvum', "Tu'um"]
PARTS = {  # how each compound or set form divides into words the dictionary already has
    'Alok-Dilon': ['alok', 'dilon'], 'Bormahu': ['bormah', '-u'], 'Dovahsebrom': ['dovah', 'se', 'brom'],
    'Gaaffesejul': ['gaaf', '(plural)', 'se', 'jul'], 'Sossedov': ['sos', 'se', 'dov'], 'Tiid-Ahraan': ['tiid', 'ahraan'],
    'Ulse': ['ul', 'se'], 'Vomir': ['vo-', 'mir'], 'Vosaraan': ['vo-', 'saraan'], 'Wuldsetiid': ['wuld', 'se', 'tiid'],
}
known = {re.sub(r"[^a-z]", "", f.lower()) for e in L['entries'] for f in (e.get('word_forms') or [e['word']])} | \
        {re.sub(r"[^a-z]", "", e['word'].lower()) for e in F['entries']}
def occurrences(word):
    pat = re.compile(r"(?<![a-z'])" + r"[\s\-]*".join(re.escape(p) for p in re.split(r"[\s\-]+", word.lower())) + r"(?![a-z'])")
    hits = []
    for t in C['texts']:
        if t.get('duplicate_of'): continue
        if pat.search((t.get('dovahzul') or '').lower()): hits.append(t['id'])
    return hits
def entry(w, grade):
    e = fe[w]; occ = occurrences(w)
    out = {'word': w, 'meaning': e['official_definition'], 'meaning_grade': grade, 'single_source': grade == 'guide_website',
           'sources_cited_by_fifth_edition': e['citations'], 'may_be_built_on': True,
           'occurs_in_game_texts': len(occ), 'example_text_ids': occ[:3]}
    if w in PARTS:
        out['parts'] = PARTS[w]
        out['parts_all_known'] = all(p.strip('-()') in known or p in ('(plural)',) for p in PARTS[w] if p not in ('-u', 'vo-')) 
    return out
vocab = [entry(w, 'game') for w in GAME] + [entry(w, 'guide') for w in GUIDE] + [entry(w, 'guide_website') for w in WEB]
places_in_wiki = json.dumps(L.get('locations'), ensure_ascii=False).lower()
names = [{'word': w, 'meaning': fe[w]['official_definition'], 'sources_cited_by_fifth_edition': fe[w]['citations'],
          'already_in_wiki_place_list': w.lower() in places_in_wiki, 'occurs_in_game_texts': len(occurrences(w))} for w in NAMES]
seen = [{'word': w, 'meaning': None, 'note': 'The Fifth Edition has an entry and prints no official definition.', 'occurs_in_game_texts': len(occurrences(w))} for w in SEEN_ONLY]
out = {'meta': {'what': 'Words added to the project from the Dragon Language Dictionary, Fifth Edition (Thuum.org), under the ruling recorded as proposal 3 in docs/decisions-log.md, accepted 2026-11-15.',
                'credit': 'Compiled and cited by Thuum.org; see research/sources/thuum/ATTRIBUTION.md. Non-commercial use.',
                'meaning': 'The official definition as the Fifth Edition quotes it. Not yet checked against the game source.',
                'parts': 'How this project divides the form into words it already has. This is the project\'s analysis.',
                'counts': {'vocabulary': len(vocab), 'names': len(names), 'forms_seen_without_meaning': len(seen)}},
       'vocabulary': vocab, 'names': names, 'forms_seen_without_meaning': seen}
json.dump(out, open(sys.argv[4], 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(sys.argv[4], 'a').write('\n')
for v in vocab: print("%-13s %-13s %-38s texts=%d parts=%s" % (v['word'], v['meaning_grade'], v['meaning'][:38], v['occurs_in_game_texts'], v.get('parts', '')))
print(out['meta']['counts'])
