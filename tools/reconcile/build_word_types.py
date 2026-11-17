"""Write the project's word types, under the ruling recorded as proposal 7 in
docs/decisions-log.md (accepted 2026-11-17).

    python3 -I tools/reconcile/build_word_types.py research/data/fifth-edition.json \
        research/data/word-status.json research/data/word-types.json

The ruling. The Fifth Edition's word types are adopted as the project's
starting types, credited to Thuum.org. Each word has a class and, for verbs
and adjectives, a note of whether it can also serve as a noun ("strong") or
not ("weak", because a separate noun exists). The owner chose flexibility: a
word may be used in every role the system allows, whether or not the game
shows that use. Uses attested in game text are information, not a limit. In
the forge a new verb or adjective is strong unless a separate noun for the
same idea exists.
"""
import collections, json, re, sys
F = json.load(open(sys.argv[1], encoding='utf-8'))
W = json.load(open(sys.argv[2], encoding='utf-8'))
ABBR = {'adj': 'adjective', 'adv': 'adverb', 'art': 'article', 'conj': 'conjunction', 'interj': 'interjection', 'n': 'noun',
        'pref': 'prefix', 'prep': 'preposition', 'pron': 'pronoun', 'suff': 'suffix', 'v': 'verb'}
FIX = {"Zu'u": ('pronoun', 'printed as a verb in the copy; the entry itself defines a pronoun')}
rows = []; tally = collections.Counter()
for e in F['entries']:
    t = e['word_type']; note = None
    if e['word'] in FIX: t, note = FIX[e['word']]
    cls = 'verb' if t.endswith('verb') and t != 'adverb' else ('adjective' if t.endswith('adjective') else t)
    also_noun = True if t.startswith('strong') else (False if t.startswith('weak') else None)
    listed = []
    for m in re.finditer(r'(?<![A-Za-z])(adj|adv|art|conj|interj|n|pref|prep|pron|suff|v)\.(?![a-z])', e['expanded_definition']):
        r = ABBR[m.group(1)]
        if r not in listed: listed.append(r)
    allowed = [cls] if cls else []
    if also_noun and 'noun' not in allowed: allowed.append('noun')
    if cls == 'adjective' and 'adverb' not in allowed: allowed.append('adverb')   # the dictionary: all adjectives can be used as adverbs
    for r in listed:
        if r not in allowed: allowed.append(r)
    row = {'word': e['word'], 'meaning': e['official_definition'], 'type_as_printed': e['word_type'], 'class': cls, 'can_also_be_a_noun': also_noun,
           'roles_the_dictionary_lists': listed, 'roles_allowed': allowed, 'roles_attested_in_game_text': 'not yet determined'}
    if note: row['note'] = note
    rows.append(row); tally[cls] += 1
have = {re.sub(r"[^a-z]", "", r['word'].lower()) for r in rows}
pending = [w['word'] for w in W['words'] if w.get('meaning_grade') in ('game', 'guide', 'guide_website', 'unconfirmed')
           and not w['in_fifth_edition'] and not any(re.sub(r"[^a-z]", "", f.lower()) in have for f in re.split(r'[,(]', w['word']))]
out = {'meta': {'what': 'The project\'s word types, under the ruling recorded as proposal 7 in docs/decisions-log.md.',
                'credit': 'The classification is Thuum.org\'s, from its Fifth Edition dictionary (non-commercial use; see research/sources/thuum/ATTRIBUTION.md). The dictionary calls it unofficial.',
                'ruling': ['The Fifth Edition\'s types are the starting types.',
                           'A word may be used in every role the system allows, whether or not the game shows that use.',
                           'Uses attested in game text are information, not a limit.',
                           'In the forge a new verb or adjective is strong unless a separate noun for the same idea exists.'],
                'fields': {'class': 'noun, verb, adjective, pronoun, adverb, conjunction, preposition, article, interjection or prefix',
                           'can_also_be_a_noun': 'true for a strong verb or adjective, false for a weak one, null where the dictionary does not say or the question does not arise',
                           'roles_the_dictionary_lists': 'the parts of speech named in the entry\'s expanded definition',
                           'roles_allowed': 'the class, plus noun if strong, plus adverb for an adjective, plus every role the dictionary lists',
                           'roles_attested_in_game_text': 'to be filled when the sentence checker is built'},
                'counts_by_class': dict(sorted(tally.items())),
                'words_with_no_type_yet': pending,
                'words_with_no_type_yet_note': 'Vocabulary the Fifth Edition does not cover. The project assigns these types.'},
       'words': rows}
json.dump(out, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(sys.argv[3], 'a').write('\n')
print(dict(sorted(tally.items())), '| no type yet:', len(pending), pending)
print('strong', sum(1 for r in rows if r['can_also_be_a_noun'] is True), 'weak', sum(1 for r in rows if r['can_also_be_a_noun'] is False),
      '| avg roles allowed', round(sum(len(r['roles_allowed']) for r in rows) / len(rows), 2), '| words with 3+ roles', sum(1 for r in rows if len(r['roles_allowed']) >= 3))
for w in ['Dwiin', 'Aam', "Zu'u", 'Dovah', 'Kogaan']:
    print([{k: r[k] for k in ('word', 'class', 'can_also_be_a_noun', 'roles_allowed')} for r in rows if r['word'] == w][0])
