"""Derive a spelling-to-sound rule from the Fifth Edition's pronunciations and
measure how well it reproduces them.

    python3 -I tools/analysis/pronunciation_rule.py research/data/fifth-edition.json \
        research/data/pronunciation.json

Under the ruling recorded as proposal 8 in docs/decisions-log.md, the Fifth
Edition's per-word pronunciations are this project's reading convention. For
new words the pronunciation is worked out from the spelling. This script
learns, for each spelling unit, the sound the dictionary most often gives it
(separately for stressed and unstressed syllables), tries simple stress rules,
and reports by five-fold cross-validation how often the rule reproduces the
dictionary's own first pronunciation. Deterministic; standard library only.
"""
import collections, importlib.util, json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ph", os.path.join(HERE, "phonotactics.py"))
ph = importlib.util.module_from_spec(spec); spec.loader.exec_module(ph)
F = json.load(open(sys.argv[1], encoding='utf-8'))
FIX_TYPE = {"Zu'u": 'pronoun'}

def variants(e):
    out = []
    for p in e.get('pronunciations_as_printed') or []:
        for v in p.strip('/').split(','):
            v = v.strip().strip('/').strip()
            v = re.sub(r'\s*(strong|weak)?\s*(verb|adjective|noun|pronoun|adverb)\s*', '', v).strip()   # stray word type in four entries
            if v: out.append(v)
    return out
def parse_ipa(v):
    """-> (chars, syllable index of each char, stress of each syllable: 2 primary, 1 secondary, 0 none)"""
    # a syllable starts after a space and also at a stress mark (the dictionary writes /əˈrol/ with no space)
    sylls = [x for x in re.split(r"\s+|(?=[ˈˌ])", v.replace('’', '')) if x]
    chars, where, stress = [], [], []
    for k, s in enumerate(sylls):
        st = 2 if 'ˈ' in s else (1 if 'ˌ' in s else 0)
        stress.append(st)
        for ch in s:
            if ch in 'ˈˌ': continue
            chars.append(ch); where.append(k)
    if len(sylls) == 1: stress = [2]
    return chars, where, stress
def spell_units(word):
    return [(u, c) for u, c in ph.units(word.lower()) if c not in ("'",) and u != '-' and u != ' ']
items = []
for e in F['entries']:
    vs = variants(e)
    if not vs: continue
    us = spell_units(e['word'])
    chars, where, stress = parse_ipa(vs[0])
    items.append({'word': e['word'], 'units': us, 'chars': chars, 'where': where, 'stress': stress, 'first': vs[0], 'all': vs})

# --- alignment by expectation-maximisation: each unit emits 0 to 3 sound symbols
def align(item, prob):
    us, ch = item['units'], item['chars']
    n, m = len(us), len(ch)
    NEG = -1e9
    best = [[NEG] * (m + 1) for _ in range(n + 1)]; back = [[0] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0.0
    for i in range(1, n + 1):
        u = us[i - 1][0]
        for j in range(m + 1):
            for L in range(0, 4):
                if j - L < 0 or best[i - 1][j - L] <= NEG / 2: continue
                piece = ''.join(ch[j - L:j])
                sc = best[i - 1][j - L] + prob(u, piece)
                if sc > best[i][j]: best[i][j] = sc; back[i][j] = L
    if best[n][m] <= NEG / 2: return None
    out = []; j = m
    for i in range(n, 0, -1):
        L = back[i][j]; out.append((j - L, j)); j -= L
    return out[::-1]
VSYM = set('ɑæəɛɪɔʊɒʌeaiou')
def prior(u, piece):
    uv = u[0] in 'aeiou'
    if piece == '': return math.log(0.02 if u != 'h' else 0.3)
    pv = [ch in VSYM for ch in piece]
    if uv:                                   # a vowel unit emits vowel symbols only (r allowed after, for ir and ur)
        if all(pv): return math.log(0.6 / len(piece))
        if u in ('ir', 'ur') and all(pv[:-1]) and piece[-1] == 'r': return math.log(0.6 / len(piece))
        return math.log(1e-4)
    if any(pv): return math.log(1e-4)        # a consonant unit does not emit a vowel
    return math.log((0.6 if piece[0] == u[0] else 0.05) / len(piece))
def train(data, rounds=4):
    table = None
    for _ in range(rounds):
        counts = collections.defaultdict(collections.Counter)
        for it in data:
            def prob(u, piece, t=table):
                if t is None: return prior(u, piece)
                c = t.get(u)
                if not c: return prior(u, piece)
                tot = sum(c.values())
                return math.log((c.get(piece, 0) + 0.05 * math.exp(prior(u, piece))) / (tot + 0.05))
            al = align(it, prob)
            if al is None: continue
            it['_al'] = al
            for (u, c), (a, b) in zip(it['units'], al):
                counts[u][''.join(it['chars'][a:b])] += 1
        table = counts
    return table
def contexts(it):
    """context of each unit: for vowels, 'S' stressed (primary or the only syllable), 'U' other; consonants 'C'"""
    al = it.get('_al'); out = []
    nuclei = [k for k, (u, c) in enumerate(it['units']) if ph.is_vowel(c)]
    for k, ((u, c), (a, b)) in enumerate(zip(it['units'], al)):
        if not ph.is_vowel(c): out.append('C'); continue
        syl = it['where'][a] if a < len(it['where']) and b > a else None
        st = it['stress'][syl] if syl is not None else 0
        final = (k == len(it['units']) - 1)
        out.append('S' if st == 2 else ('Ufinal' if final else 'U'))
    return out
def learn(data):
    train(data)
    rule = collections.defaultdict(collections.Counter)
    for it in data:
        if '_al' not in it: continue
        for (u, c), (a, b), ctx in zip(it['units'], it['_al'], contexts(it)):
            rule[(u, ctx)][''.join(it['chars'][a:b])] += 1
    return rule
def predict(units, stressed_nucleus, rule, fallback):
    out = []; nucleus = -1
    for k, (u, c) in enumerate(units):
        if ph.is_vowel(c):
            nucleus += 1
            ctx = 'S' if nucleus == stressed_nucleus else ('Ufinal' if k == len(units) - 1 else 'U')
        else: ctx = 'C'
        c1 = rule.get((u, ctx)) or (rule.get((u, 'U')) if ctx == 'Ufinal' else None) or fallback.get(u)
        out.append(c1.most_common(1)[0][0] if c1 else u)
    return ''.join(out)
def true_stressed_nucleus(it):
    # index among vowel units of the one whose sound lies in the primary-stressed syllable
    idx = -1
    for (u, c), (a, b) in zip(it['units'], it['_al']):
        if ph.is_vowel(c):
            idx += 1
            if b > a and it['stress'][it['where'][a]] == 2: return idx
    return 0
STRESS_RULES = {
    'first syllable': lambda us: 0,
    'last syllable': lambda us: sum(1 for u, c in us if ph.is_vowel(c)) - 1,
    'last syllable with aa or ii, else first': lambda us: max([k for k, u in enumerate([u for u, c in us if ph.is_vowel(c)]) if u in ('aa', 'ii')] or [0]),
    'first syllable with aa or ii, else first': lambda us: min([k for k, u in enumerate([u for u, c in us if ph.is_vowel(c)]) if u in ('aa', 'ii')] or [0]),
    'last syllable with a two-letter vowel, else first': lambda us: max([k for k, (u, c) in enumerate([(u, c) for u, c in us if ph.is_vowel(c)]) if c == 'VV'] or [0]),
    'in a two-syllable word the last if it has aa, ii, ei or ey; otherwise the first': lambda us: (
        1 if (sum(1 for u, c in us if ph.is_vowel(c)) == 2 and [u for u, c in us if ph.is_vowel(c)][-1] in ('aa', 'ii', 'ei', 'ey')) else 0),
}
def listed_stress_positions(it):
    n = sum(1 for u, c in it['units'] if ph.is_vowel(c)); out = set()
    for v in it['all']:
        st = parse_ipa(v)[2]
        if len(st) == n and 2 in st: out.add(st.index(2))
    return out
# --- whole-data rule
rule_all = learn(items)
fallback_all = collections.defaultdict(collections.Counter)
for (u, ctx), c in rule_all.items(): fallback_all[u].update(c)
aligned = [it for it in items if '_al' in it]
poly = [it for it in aligned if sum(1 for u, c in it['units'] if ph.is_vowel(c)) >= 2 and len(it['stress']) >= 2]
poly = [it for it in poly if listed_stress_positions(it)]
stress_acc = {}
for name, fn in STRESS_RULES.items():
    stress_acc[name] = {'matches_the_first_pronunciation': round(sum(1 for it in poly if fn(it['units']) == true_stressed_nucleus(it)) / len(poly), 3),
                        'matches_any_listed_pronunciation': round(sum(1 for it in poly if fn(it['units']) in listed_stress_positions(it)) / len(poly), 3)}
best_stress = 'first syllable'   # the simplest rule; none tried is more than three points better
# --- five-fold cross-validation
K = 5; res = {'given_stress': 0, 'with_stress_rule': 0, 'n': 0, 'any_variant': 0}
miss = collections.Counter(); miss_examples = collections.defaultdict(list)
for f in range(K):
    test = [it for i, it in enumerate(items) if i % K == f]
    tr = [dict(it) for i, it in enumerate(items) if i % K != f]
    for it in tr: it.pop('_al', None)
    r = learn(tr); fb = collections.defaultdict(collections.Counter)
    for (u, ctx), c in r.items(): fb[u].update(c)
    for it in test:
        if '_al' not in it: continue
        res['n'] += 1
        truth = ''.join(it['chars'])
        p1 = predict(it['units'], true_stressed_nucleus(it), r, fb)
        p2 = predict(it['units'], STRESS_RULES[best_stress](it['units']), r, fb)
        res['given_stress'] += (p1 == truth)
        res['with_stress_rule'] += (p2 == truth)
        allv = {''.join(parse_ipa(v)[0]) for v in it['all']}
        res['any_variant'] += (p2 in allv)
        if p1 != truth:
            for (u, c), (a, b), ctx in zip(it['units'], it['_al'], contexts(it)):
                got = ''.join(it['chars'][a:b]); exp = (r.get((u, ctx)) or fb.get(u) or collections.Counter({u: 1})).most_common(1)[0][0]
                if got != exp:
                    miss[(u, ctx, exp, got)] += 1
                    if len(miss_examples[(u, ctx, exp, got)]) < 3: miss_examples[(u, ctx, exp, got)].append(it['word'])
n = res['n']
table = {}
for (u, ctx), c in sorted(rule_all.items()):
    table.setdefault(u, {})[ctx] = {'sound': c.most_common(1)[0][0], 'share': round(c.most_common(1)[0][1] / sum(c.values()), 2), 'n': sum(c.values()),
                                    'others': {k: v for k, v in c.most_common(4)[1:]}}
def n_syll(v): return len(parse_ipa(v)[2])
words = []
for e in F['entries']:
    vs = variants(e)
    row = {'word': e['word'], 'taught': vs[0] if vs else None, 'also_accepted': vs[1:], 'heard_in_game': []}
    if "u'u" in e['word'].lower() and vs:
        # Proposal 9: the apostrophe marks a break between the two u's, so the form with the break is the one taught.
        longer = [v for v in vs if n_syll(v) > n_syll(vs[0])]
        if longer:
            row['taught'] = longer[0]; row['also_accepted'] = [v for v in vs if v != longer[0]]
            row['break_between_the_two_u'] = 'a light catch in the throat (a glottal stop), which the apostrophe writes'
            row['note'] = 'Taught with the break by the ruling on proposal 9. The dictionary lists the one-syllable form first; it stays accepted.'
    words.append(row)
if "u'u" in table:
    table["u'u"] = {'S': {'sound': 'uʔu', 'by': 'owner\'s ruling, proposal 9: two syllables with a catch between them',
                          'dictionary_first_form': table["u'u"].get('S', {}).get('sound')}}
out = {
    'meta': {
        'what': 'The project\'s reading convention, under the ruling recorded as proposal 8 in docs/decisions-log.md.',
        'credit': 'The pronunciations are Thuum.org\'s, from its Fifth Edition dictionary (non-commercial use; see research/sources/thuum/ATTRIBUTION.md). The dictionary calls them recommended, not official.',
        'ruling': ['The Fifth Edition\'s per-word pronunciations are the reading convention.', 'Where its table and its entries disagree, the entries are followed.',
                   'Where an entry lists several pronunciations, the first is taught and the rest are accepted.', 'Stress is taught as marked and described as a tendency.',
                   'It is labelled everywhere as a convention, not official.', 'For new words the pronunciation is worked out from the spelling by the rule below.',
                   'Owner\'s ruling on proposal 9: the apostrophe between two u\'s writes a break (a glottal stop). A word spelt with it is taught with the break; uu without it is one long u.',
                   'Owner\'s condition: people will at some point listen to the game. The convention stays open to that evidence. What is heard in the game is recorded per word under heard_in_game, with the speaker and line; a form heard in the game is accepted, and where the game consistently contradicts the taught form, the taught form changes in a numbered release.'],
        'notation': 'International Phonetic Alphabet. A space separates syllables; ˈ marks primary stress and ˌ secondary stress on the syllable that follows.',
    },
    'rule_for_new_words': {
        'method': 'Each spelling unit takes the sound the dictionary most often gives it, separately for a stressed syllable (S), an unstressed one (U), an unstressed one at the end of the word (Ufinal) and for consonants (C).',
        'sound_table': table,
        'stress_rules_tried': stress_acc, 'stress_rule_used': best_stress, 'words_of_two_or_more_syllables': len(poly),
        'words_listing_more_than_one_stress_position': sum(1 for it in poly if len(listed_stress_positions(it)) > 1),
        'stress_finding': 'Stress cannot be worked out from spelling alone: the best simple rule matches about two words in three. The dictionary ties stress to the root of a word, which spelling does not show. In the forge the coiner declares the parts of a new word, so stress is placed on the root; for a new root the default is the first syllable.',
        'how_well_it_reproduces_the_dictionary': {
            'test': 'five-fold cross-validation over %d entries: the rule is learned from four fifths and tried on the rest' % n,
            'sounds_right_when_the_stress_is_known': round(res['given_stress'] / n, 3),
            'sounds_right_with_the_stress_rule': round(res['with_stress_rule'] / n, 3),
            'matches_any_listed_pronunciation_with_the_stress_rule': round(res['any_variant'] / n, 3),
            'note': 'A match means every sound is the same as in the dictionary\'s pronunciation; stress marks and syllable breaks are not compared.'},
        'commonest_misses': [{'unit': u, 'where': ctx, 'rule_gives': exp, 'dictionary_has': got, 'times': k, 'examples': miss_examples[(u, ctx, exp, got)]} for (u, ctx, exp, got), k in miss.most_common(14)],
    },
    'words': words,
}
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(sys.argv[2], 'a').write('\n')
print('entries', len(items), 'aligned', len(aligned), 'polysyllabic', len(poly))
print('stress rules', stress_acc)
print(out['rule_for_new_words']['how_well_it_reproduces_the_dictionary'])
for m in out['rule_for_new_words']['commonest_misses'][:12]: print('  ', m)
print({u: {ctx: (v['sound'], v.get('share'), v.get('n')) for ctx, v in d.items()} for u, d in table.items() if u in ('a', 'aa', 'ah', 'e', 'ei', 'ey', 'i', 'ii', 'o', 'oo', 'u', 'uu', "u'u", 'q', 'j', 'x', 'y', 'th', 'h', 'ir', 'ur', 'au', 'ae')})
