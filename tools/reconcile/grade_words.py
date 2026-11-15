"""Grade the standing of each wiki dictionary entry's meaning.

    python3 -I tools/reconcile/grade_words.py research/data/canon-lexicon.json \
        research/data/fifth-edition-reconciliation.json research/data/fifth-edition.json \
        research/data/word-status.json

Ruling (decisions log, proposal 2, accepted 2026-11-15). A word's meaning has
one of four grades, by where its official definition comes from:

  game            the game's own material: developer notes in the game files,
                  in-game books, the Shouts menu
  guide           the printed official guide, with no game source
  guide_website   only the guide publisher's online word list; official, but
                  marked as resting on a single source
  unconfirmed     no official definition found

Grades game, guide and guide_website may be used as building parts in the
forge. Unconfirmed words may not until the owner rules on each. Words from
later games, which the Fifth Edition does not cover, keep the wiki's reading
and are labelled by game. Twelve further wiki entries wait on proposal 4.
"""
import collections, json, sys
L = json.load(open(sys.argv[1], encoding='utf-8'))
R = json.load(open(sys.argv[2], encoding='utf-8'))
F = json.load(open(sys.argv[3], encoding='utf-8'))
doubt = {e['word']: e['doubt'] for e in F['entries'] if e.get('doubt')}
nodef = {e['word'] for e in F['entries'] if e['official_definition'].lower().startswith('no official')}
refs = {e['word']: (e.get('refs') or []) for e in L['entries']}
defs = {e['word']: (e.get('definition_text') or '') for e in L['entries']}
LATER = {'ESONahfahlaar': 'The Elder Scrolls Online', 'ESOLaatvulon': 'The Elder Scrolls Online', 'ESOD': 'The Elder Scrolls Online',
         'Korthor': 'The Elder Scrolls Online', 'WOTFG': 'The Elder Scrolls Online (book: Wisdom of the Flying Gods)',
         'Shulkunaak': 'The Elder Scrolls: Blades'}
LEVEL = {'game_files_or_books': 'game', 'printed_guide': 'guide', 'guide_website_only': 'guide_website'}
rows = []
for r in R['wiki_entries']:
    w = r['word']; row = {'word': w, 'word_attested': r['wiki_source_class'], 'in_fifth_edition': r['in_fifth_edition']}
    if r['in_fifth_edition']:
        heads = r['fifth_edition_headwords']
        g = LEVEL.get(r['fifth_edition_definition_source'], 'unconfirmed')
        if heads and all(h in nodef for h in heads): g = 'unconfirmed'
        row.update({'meaning_grade': g, 'meaning_sources': r['fifth_edition_source_kinds'], 'single_source': g == 'guide_website',
                    'may_be_built_on': g != 'unconfirmed'})
        d = [doubt[h] for h in heads if h in doubt]
        if d: row['doubt'] = '; '.join(d)
    else:
        games = sorted({LATER[x] for x in refs[w] if x in LATER})
        if games:
            row.update({'meaning_grade': 'later_game', 'later_game': games[0], 'meaning_is': 'the wiki reading' if defs[w] else 'not recorded',
                        'single_source': False, 'may_be_built_on': None, 'waits_on': 'proposal 4'})
        elif r['wiki_source_class'] == 'untraced_list_only':
            row.update({'meaning_grade': 'unconfirmed', 'meaning_sources': [], 'single_source': False, 'may_be_built_on': False})
        else:
            row.update({'meaning_grade': None, 'single_source': False, 'may_be_built_on': None, 'waits_on': 'proposal 4'})
    rows.append(row)
counts = collections.Counter(str(r['meaning_grade']) for r in rows)
out = {'meta': {'what': 'The standing of each wiki dictionary entry\'s meaning, by the ruling in docs/decisions-log.md, proposal 2.',
                'grades': {'game': 'defined in the game\'s own material', 'guide': 'defined in the printed official guide, no game source',
                           'guide_website': 'defined only in the guide publisher\'s online word list (single source)',
                           'unconfirmed': 'no official definition found; may not be built on until ruled',
                           'later_game': 'from a later game the Fifth Edition does not cover; keeps the wiki reading',
                           'None': 'waits on proposal 4'},
                'word_attested': 'where the wiki says the word itself occurs: game_text, game_data, guide_only, untraced_list_only, other, no_source',
                'counts': dict(sorted(counts.items())),
                'caution': 'A grade says where the definition is cited from. A few definitions are misprinted in the Fifth Edition copy (see the doubt field), and no cited definition replaces a wiki meaning until the game source has been checked.'},
       'words': rows}
json.dump(out, open(sys.argv[4], 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(sys.argv[4], 'a').write('\n')
print(dict(sorted(counts.items())), '| may be built on:', sum(1 for r in rows if r['may_be_built_on']), '| single source:', sum(1 for r in rows if r['single_source']))
