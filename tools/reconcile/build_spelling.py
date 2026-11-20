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
    'apostrophe': {
        'ruling': 'Proposal 9, the owner\'s ruling of 2026-11-18. The apostrophe between two u\'s writes a break in the voice, a glottal stop. Where that sound is made the standard spelling has the apostrophe, whether or not the game or an inscription writes it. Writing the word without it is accepted, but it is not the standard. Two u\'s with no break between them are one long u and are written uu.',
        'standard_with_apostrophe': [{'word': w, 'meaning': m} for w, m in [("Zu'u", 'I'), ("Thu'um", 'voice, shout'), ("Su'um", 'breath'), ("Du'ul", 'crown'), ("Strundu'ul", 'stormcrown'), ("Tu'um", 'no official definition')]],
        'long_u_without_apostrophe': [{'word': 'Gravuun', 'meaning': 'autumn', 'basis': 'the Fifth Edition says it should not be spoken as three syllables or with a glottal stop'},
                                      {'word': 'Volunruud', 'meaning': 'a place name', 'basis': 'the reading convention gives one long u'},
                                      {'word': 'Sigruuf', 'meaning': 'a personal name on a word wall', 'basis': 'no evidence of a break'}],
        'in_runes': ['A break is written with two separate U runes. The single double-U rune stands for one long u.',
                     'The runes have no sign for the apostrophe. A break mark is to be designed with the other new signs; once it exists the standard rune spelling carries it between the two U runes.',
                     'Game inscriptions are shown as written. The Throw Voice word wall writes thu\'um with the double-U rune, and a High Hrothgar banner writes tu\'um the same way; both are recorded variants.'],
        'possessive_endings': 'By the owner\'s ruling of 2026-11-20 the same stop separates the two i\'s of the possessive endings, which are written -i\'i (his, her, its) and -i\'il (your). This applies to the endings only; inside a word the doubled i is one long vowel. See grammar-rulings.json, G07-possessive-endings.',
        'in_new_words': 'The forge accepts an apostrophe in two places only: between two u\'s where the coiner declares a break, and in the possessive endings -i\'i and -i\'il. Elsewhere it is rejected.',
        'not_decided': 'Whether a break may be written between other vowels inside a word (a\'a, or i\'i other than in the endings). The games have no such word.',
        'variants_without_apostrophe_in_game_material': [{'form': f, 'occurs_in_game_text': occ(f)} for f in ['thuum', 'tuum']],
    },
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
