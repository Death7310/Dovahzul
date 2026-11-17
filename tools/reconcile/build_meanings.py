"""Write the meaning of record for each word, under the ruling recorded as
proposal 6 in docs/decisions-log.md (accepted 2026-11-17).

    python3 -I tools/reconcile/build_meanings.py research/data/canon-lexicon.json \
        research/data/fifth-edition.json research/data/fifth-edition-reconciliation.json \
        research/data/word-status.json research/data/meanings.json

The rule.
 1. The meaning of record is the official definition from the best source:
    the game's own material, then the printed guide, then the guide website.
 2. Where the wiki only words it differently, its wording is kept as a note.
 3. Where two games give a word different senses, both are kept, each
    labelled with its game.
 4. Thuum.org's commentary (expanded definitions, connotations, notes) is
    commentary, credited to Thuum.org, never the meaning of record.
 5. Nothing is replaced blind. A definition the copy misprints is not used;
    a definition that rests only on the printed guide or the guide website is
    marked as taken on the Fifth Edition's word.
Owner's addition: the older meanings of Bel, Mindol and Mindok are kept as a
second, labelled sense.
"""
import collections, json, re, sys
L = json.load(open(sys.argv[1], encoding='utf-8'))
F = json.load(open(sys.argv[2], encoding='utf-8'))
R = json.load(open(sys.argv[3], encoding='utf-8'))
W = json.load(open(sys.argv[4], encoding='utf-8'))
fe = collections.defaultdict(list)
for e in F['entries']: fe[e['word']].append(e)
wiki = {e['word']: e for e in L['entries']}
status = {r['word']: r for r in W['words']}
STOP = set('a an the to of as in or and is be for with by on at lit also see used from that this it its not no you your his her my our their them they he she we i'.split())
def toks(s):
    s = re.sub(r'\([^)]*\)', ' ', s.lower())
    return {re.sub(r'(ing|ed|es|s|ly)$', '', w) for w in re.findall(r"[a-z]+", s) if w not in STOP and len(w) > 1}
MISPRINT = {'Krah', 'Krii', 'Sosaal', 'Gron', 'Unslaad', 'Niid'}       # the copy misprints these definitions
RULED = {
    'Bel': {'record': 'Summon', 'source': 'guide website', 'senses': [{'meaning': 'Foul (v.)', 'label': 'from the untraced word list; kept as a second sense by the owner\'s ruling'}]},
    'Mindol': {'record': 'Thought', 'source': 'guide website', 'senses': [{'meaning': 'Trick', 'label': 'from the untraced word list; kept as a second sense by the owner\'s ruling'}]},
    'Mindok': {'record': 'Think', 'source': 'guide website', 'senses': [{'meaning': 'Know, Known, Knowable', 'label': 'the wiki\'s reading; kept as a second sense by the owner\'s ruling'}]},
    'Mindoraan': {'record': 'Understanding', 'source': 'guide website', 'senses': []},
    'Rok': {'record': 'He', 'source': 'game material', 'senses': [{'meaning': 'Word', 'label': 'listed in the printed guide; the Fifth Edition calls this a mistake for rot'}]},
    'Sov': {'record': 'Spend/Spent', 'source': 'printed guide; occurs on a Skyrim word wall', 'senses': [{'meaning': 'Shock', 'label': 'The Elder Scrolls Online, in a dragon\'s shout'}]},
    'Kun': {'record': 'Moonlight', 'source': 'The Elder Scrolls Online, twice with a translation', 'senses': [{'meaning': 'Light', 'label': 'unconfirmed: the Fifth Edition\'s inference; the Skyrim line it cites reads jun'}]},
}
ADDED_RULED = {'Vosaraan': 'the developer note; the wiki editors read the same line as "(your) opposite awaits"'}
def basis(kinds):
    k = set(kinds)
    if k & {'dialogue_file', 'book', 'shout_menu'}: return 'game material'
    if 'prima_guide' in k: return 'printed guide'
    if 'primagames_com' in k: return 'guide website'
    return 'none cited'
rows = []; tally = collections.Counter()
for r in R['wiki_entries']:
    w = r['word']; we = wiki[w]; wdef = we.get('definition_text') or ''
    st = status[w]
    row = {'word': w, 'grade': st.get('meaning_grade')}
    if st.get('meaning_grade') in ('variant', 'recorded_form', 'reserved', 'name'):
        row.update({'meaning_of_record': wdef or None, 'how_settled': st['meaning_grade'], 'from': 'the wiki reading' if wdef else None})
    elif w in RULED:
        row.update({'meaning_of_record': RULED[w]['record'], 'from': RULED[w]['source'], 'other_senses': RULED[w]['senses'], 'how_settled': 'ruled individually'})
        if w == 'Mindoraan': row['wiki_wording'] = wdef
    elif r['in_fifth_edition']:
        heads = [e for h in r['fifth_edition_headwords'] for e in fe[h]]
        odef = ' | '.join(dict.fromkeys(e['official_definition'] for e in heads if e['official_definition']))
        kinds = sorted({k for e in heads for k in e['source_kinds']})
        if any(e['word'] in MISPRINT for e in heads):
            row.update({'meaning_of_record': wdef, 'from': 'the wiki reading', 'how_settled': 'the Fifth Edition copy misprints this definition; to be re-read from the publisher\'s file',
                        'printed_in_copy': odef})
        elif odef.lower().startswith('no official') or not odef:
            row.update({'meaning_of_record': wdef or None, 'from': 'the wiki reading' if wdef else None, 'how_settled': 'no official definition printed'})
        elif wdef and odef.lower().startswith(w.split(',')[0].strip().lower() + ' ('):
            # the official list repeats the word itself and adds a remark; the wiki wording is the usable gloss
            row.update({'meaning_of_record': wdef, 'from': basis(kinds), 'official_remark': odef, 'how_settled': 'sources agree',
                        'checked': 'can be checked against game pages; not yet done' if basis(kinds) == 'game material' else 'taken on the Fifth Edition\'s word'})
        else:
            same = wdef.strip().lower() == odef.strip().lower()
            agree = (same or bool(toks(wdef) & toks(odef)) or not (toks(wdef) or toks(odef))) if wdef else None
            row.update({'meaning_of_record': odef, 'from': basis(kinds),
                        'how_settled': 'sources agree' if agree else ('no wiki meaning' if agree is None else 'official definition taken; wiki wording kept as a note')})
            if wdef and wdef.strip().lower() != odef.strip().lower(): row['wiki_wording'] = wdef
            row['checked'] = 'can be checked against game pages; not yet done' if basis(kinds) == 'game material' else 'taken on the Fifth Edition\'s word'
        if any(e.get('doubt') for e in heads) and 'printed_in_copy' not in row: row['doubt'] = '; '.join(e['doubt'] for e in heads if e.get('doubt'))
    else:
        row.update({'meaning_of_record': wdef or None, 'from': 'the wiki reading' if wdef else None,
                    'how_settled': {'game': 'later game or single ruling', 'guide': 'single ruling', 'unconfirmed': 'unconfirmed'}.get(st.get('meaning_grade'), 'see word-status.json')})
    tally[row['how_settled'] if len(row['how_settled']) < 60 else 'misprint in copy'] += 1
    rows.append(row)
out = {'meta': {'what': 'The meaning of record for each wiki dictionary entry, under the ruling recorded as proposal 6 in docs/decisions-log.md.',
                'credit': 'Official definitions are quoted as compiled and cited by Thuum.org in its Fifth Edition (non-commercial use; see research/sources/thuum/ATTRIBUTION.md). Wiki wordings are from UESP (CC BY-SA 2.5).',
                'fields': {'meaning_of_record': 'the meaning the project uses', 'from': 'the kind of source it rests on', 'wiki_wording': 'the wiki editors\' wording, kept as a note where it differs',
                           'other_senses': 'further senses, each with a label', 'how_settled': 'which part of the rule applied', 'checked': 'whether the cited source has been or can be checked',
                           'printed_in_copy': 'what the Fifth Edition copy prints where that is a known misprint'},
                'added_words': 'Words added from the Fifth Edition are in lexicon-additions.json. Vosaraan there carries the developer note\'s meaning, by this ruling.',
                'counts': dict(sorted(tally.items()))},
       'words': rows}
json.dump(out, open(sys.argv[5], 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(sys.argv[5], 'a').write('\n')
print(dict(sorted(tally.items())))
for w in ['Bel', 'Kun', 'Sov', 'Krii', 'Aak', 'Horvutah']:
    print([{k: v for k, v in r.items() if k != 'grade'} for r in rows if r['word'] == w][0])
