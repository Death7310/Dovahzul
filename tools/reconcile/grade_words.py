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
and are labelled by game.

Ruling (proposal 4, accepted 2026-11-15) on the 59 wiki entries that have no
Fifth Edition heading:

  recorded forms   21 are forms of words the project already has (an ending
                   or a compound). They are filed under their base word and
                   are not separate vocabulary entries.
  later game       11 have a meaning given in a later game's own material.
                   Graded game, labelled with the game, usable in the forge.
  reserved         10 later-game words have no recorded meaning. They are
                   never given an invented meaning and their spellings are
                   not reused for new words.
  unconfirmed      7 words from the untraced list have nothing else behind
                   them.
  singles          Shor is a name. Ros keeps a guide-level grade with the
                   single-source mark. Au is graded game with a note. Vun
                   keeps a guide grade with a doubt mark and is not built on.
  spelling         6 are spelling variants of other words (proposal 5,
                   accepted 2026-11-15); see spelling.json.
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
ESO = 'The Elder Scrolls Online'
FORMS = {  # proposal 4: forms of words the project already has
    'Dezu': ['dez', '-u'], 'Dinokii': ['dinok', '-ii'], 'Dovahzin': ['dovah', 'zin'], 'Fenjuntiid': ['fen', 'jun', 'tiid'],
    'Gronsezin': ['gron', 'se', 'zin'], 'Juntiid': ['jun', 'tiid'], 'Nikrent': ['ni-', 'krent'], 'Sosmir': ['sos', 'mir'],
    'Briinahii': ['briinah', '-ii'], 'Duaan': ['du', '-aan'], 'Frini': ['frin', '-i'], 'Junnesejer': ['jun', '(plural)', 'se', 'jer'],
    'Ziil': ['zii', '-l'], 'Zindro': ['zind', '-ro (ending not explained)'], 'Funta': ['funt', '-a'], 'Stinselok': ['stin', 'se', 'lok'],
    'Voqostiid': ['vo-', 'qostiid'], 'Naaktiid': ['naak', 'tiid'], 'Pelaan': ['pel', '-aan'], 'Fahlah': ['fah', 'lah'],
    'Qahnaaran': ['qahnaar', '-aan (vowel shortened)'],
}
FORMS_NOT_IN_TEXT = {'Juntiid', 'Naaktiid', 'Pelaan', 'Fahlah', 'Qahnaaran'}
LATER_WITH_MEANING = {'Dey': ESO, 'Fey': ESO, 'Jiid': ESO, 'Jol': ESO, 'On': ESO, 'Ron': ESO, 'Roth': ESO, 'Wiix': ESO, 'Laar': ESO, 'Miir': ESO, 'Nihnzey': ESO}
RESERVED = {'Han', 'Hof', 'Jaag', 'Kohg', 'Liik', 'Moh', 'Nel', 'Riis', 'Thaan', 'Tosh'}
SPELLING = {'Kriivaan': 'Krivaan', 'Tovinaan': 'Tovitaan', 'Tiiraz': 'Tiiraaz', 'Quethsegol': 'Qethsegol', 'Nall': 'Naal', 'Thurri': 'Thuri'}  # proposal 5
SINGLES = {
    'Shor': {'meaning_grade': 'name', 'may_be_built_on': None, 'note': 'a god\'s name; belongs to the list of names'},
    'Ros': {'meaning_grade': 'guide', 'single_source': True, 'may_be_built_on': True, 'note': 'from a Bethesda article; graded like a guide word'},
    'Au': {'meaning_grade': 'game', 'may_be_built_on': True, 'note': 'occurs once in an in-game book, translated "on"; may be a misprint of nau'},
    'Vun': {'meaning_grade': 'guide', 'may_be_built_on': False, 'doubt': 'the Fifth Edition says the word for voice was once vun and is now zul'},
}
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
    elif w in FORMS:
        row.update({'meaning_grade': 'recorded_form', 'parts': FORMS[w], 'occurs_in_game_text_as_spelt': w not in FORMS_NOT_IN_TEXT,
                    'meaning_is': 'the wiki reading', 'single_source': False, 'may_be_built_on': None,
                    'note': 'filed under its base word; not a separate vocabulary entry'})
    elif w in LATER_WITH_MEANING:
        row.update({'meaning_grade': 'game', 'later_game': LATER_WITH_MEANING[w], 'meaning_is': 'given in the later game\'s own material',
                    'single_source': False, 'may_be_built_on': True})
    elif w in RESERVED:
        row.update({'meaning_grade': 'reserved', 'later_game': ESO, 'meaning_is': 'not recorded', 'single_source': False, 'may_be_built_on': False,
                    'note': 'never to be given an invented meaning; the spelling is not reused for new words'})
    elif w in SPELLING:
        row.update({'meaning_grade': 'variant', 'variant_of': SPELLING[w], 'single_source': False, 'may_be_built_on': False,
                    'note': 'a recorded spelling variant, not a separate word; see spelling.json'})
    elif w in SINGLES:
        row.update({'single_source': False}); row.update(SINGLES[w])
    else:
        games = sorted({LATER[x] for x in refs[w] if x in LATER})
        if games:
            row.update({'meaning_grade': 'later_game', 'later_game': games[0], 'meaning_is': 'the wiki reading' if defs[w] else 'not recorded',
                        'single_source': False, 'may_be_built_on': None, 'waits_on': 'proposal 4'})
        elif r['wiki_source_class'] == 'untraced_list_only':
            # proposal 14: the words with nothing behind them but the untraced list are kept and usable, labelled
            row.update({'meaning_grade': 'source_untraced', 'meaning_sources': [], 'single_source': True, 'may_be_built_on': True,
                        'note': 'kept by the owner\'s ruling on proposal 14; shown with the label "source untraced"'})
        else:
            row.update({'meaning_grade': None, 'single_source': False, 'may_be_built_on': None, 'waits_on': 'proposal 4'})
    rows.append(row)
counts = collections.Counter(str(r['meaning_grade']) for r in rows)
out = {'meta': {'what': 'The standing of each wiki dictionary entry\'s meaning, by the rulings in docs/decisions-log.md, proposals 2, 4, 5 and 14.',
                'grades': {'game': 'defined in the game\'s own material', 'guide': 'defined in the printed official guide, no game source',
                           'guide_website': 'defined only in the guide publisher\'s online word list (single source)',
                           'unconfirmed': 'no official definition found; may not be built on until ruled',
                           'source_untraced': 'known only from a word list whose origin could not be traced; kept and usable by the owner\'s ruling, with that label',
                           'recorded_form': 'a form of a word the project already has; filed under that word',
                           'reserved': 'a later-game word with no recorded meaning; never given one, spelling not reused',
                           'name': 'a proper name',
                           'variant': 'a recorded spelling variant of another word; not a separate word'},
                'word_attested': 'where the wiki says the word itself occurs: game_text, game_data, guide_only, untraced_list_only, other, no_source',
                'counts': dict(sorted(counts.items())),
                'caution': 'A grade says where the definition is cited from. A few definitions are misprinted in the Fifth Edition copy (see the doubt field), and no cited definition replaces a wiki meaning until the game source has been checked.'},
       'words': rows}
json.dump(out, open(sys.argv[4], 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(sys.argv[4], 'a').write('\n')
print(dict(sorted(counts.items())), '| may be built on:', sum(1 for r in rows if r['may_be_built_on']), '| single source:', sum(1 for r in rows if r['single_source']))
