"""Write the standard spellings and their recorded variants, under the ruling
recorded as proposal 5 in docs/decisions-log.md (accepted 2026-11-15).

    python3 -I tools/reconcile/build_spelling.py research/data/canon-corpus.json \
        research/data/spelling.json

The rule. Each word has one standard spelling: the one the developer notes or
the guide give, or failing that the most frequent in game text. The course
teaches only the standard, and the forge checker accepts only the standard in
new writing. Game texts are never altered: they are shown as written, and a
rare spelling is marked as a variant of its standard word. A variant is not a
separate word.
"""
import json, re, sys
C = json.load(open(sys.argv[1], encoding='utf-8'))
texts = [t for t in C['texts'] if not t.get('duplicate_of')]
def occ(w):
    pat = re.compile(r"(?<![a-z'])" + re.escape(w.lower()) + r"(?![a-z'])")
    return sum(len(pat.findall((t.get('dovahzul') or '').lower())) for t in texts)
CASES = [
    # standard, meaning, basis, [(variant, where the variant comes from)]
    ('Krivaan', 'murderer', 'in the printed guide; occurs on a word wall', [('Kriivaan', 'the untraced word list')]),
    ('Tiiraaz', 'sad', 'the developer note spells it so; the Fifth Edition calls tiiraz a slip in the dialogue', [('Tiiraz', 'game dialogue')]),
    ('Tovitaan', 'searcher', 'on the guide website; single source; neither spelling occurs in game text', [('Tovinaan', 'the untraced word list')]),
    ('Daanik', 'doomed', 'the spelling in game text, including word walls', [('Daniik', 'the guide website; the Fifth Edition has a heading for each spelling')]),
    ('Qethsegol', 'stone', 'the usual spelling in game text', [('Quethsegol', 'an in-game book, in the place name Quethsegol Ahrol (Granite Hill), where it stays as written')]),
    ('Naal', 'by', 'the usual spelling in game text', [('Nall', 'one line of game dialogue')]),
    ('Thuri', 'my overlord', 'the usual spelling in game text', [('Thurri', 'game dialogue')]),
    ('Nid', 'no', 'the usual spelling in game text', [('Niid', 'one line of game dialogue')]),
    ('Balaan', 'worthy', 'the usual spelling in game text', [('Bahlaan', 'one line of game dialogue; the Fifth Edition calls it a misspelling or an archaic form')]),
    ("Thu'um", 'voice, shout', 'the usual spelling in game text', [('Tuum', 'one banner inscription')]),
    ('Miiraad', 'doorway', 'the Fifth Edition calls miraad a misspelling; each occurs once', [('Miraad', 'one line of game dialogue')]),
]
out_cases = []
for std, meaning, basis, variants in CASES:
    out_cases.append({'standard': std, 'meaning': meaning, 'basis': basis, 'standard_occurs_in_game_text': occ(std),
                      'variants': [{'form': v, 'from': where, 'occurs_in_game_text': occ(v)} for v, where in variants]})
out = {
    'meta': {'what': 'Standard spellings and their recorded variants, under the ruling recorded as proposal 5 in docs/decisions-log.md.',
             'rule': ['Each word has one standard spelling: the one the developer notes or the guide give, or failing that the most frequent in game text.',
                      'The course teaches only the standard, and the forge checker accepts only the standard in new writing.',
                      'Game texts are never altered. They are shown as written, and a rare spelling is marked as a variant of its standard word.',
                      'A variant is not a separate word.'],
             'counts': 'Occurrences are whole-word counts over the game texts in canon-corpus.json with duplicate records left out.'},
    'cases': out_cases,
    'unexplained_forms': [{'form': 'hinde', 'occurs_in_game_text': occ('hinde'),
                           'note': 'A plural of hin ("your") in one line of dialogue. The regular plural would be hinne, which does not occur. Left unexplained and not taught.'}],
    'further_cases_reported_by_the_fifth_edition': [
        'dohaviin for dovahkiin', 'uznahgar for uznahgaar', 'sindungahvon for sindugahvon', 'hadrimme as a plural of hahdrim',
        'vonmindoraan, possibly for vomindoraan', 'aan in the sense "slave", possibly for aar', 'rok in the sense "word", for rot', 'jun in the sense "light", for kun',
    ],
    'further_cases_note': 'These fall under the same rule. Each is to be checked against the game text before it is recorded as a variant.',
}
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(sys.argv[2], 'a').write('\n')
for c in out_cases: print("%-10s %2d | %s" % (c['standard'], c['standard_occurs_in_game_text'], ', '.join("%s %d" % (v['form'], v['occurs_in_game_text']) for v in c['variants'])))
