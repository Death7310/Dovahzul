"""Parse a plain-text conversion of the Dragon Language Dictionary, Fifth
Edition (Thuum.org) into one record per entry.

The dictionary itself is NOT part of this repository. It has no stated
licence, so only facts checked against it are kept here (see
research/data/fifth-edition-reconciliation.json). To re-run, convert your own
copy to text first:

    pandoc -t plain --wrap=none dictionary.docx -o dictionary.txt
    python3 -I tools/reconcile/parse_fifth_edition.py dictionary.txt parsed.json

Method. Every entry carries a "Word Type" line, which is used as the anchor.
The heading above it is recognised by matching the word against its rune
spelling, in which the digits 1-9 stand for the two-letter runes
(1 aa, 2 ei, 3 ii, 4 ah, 5 uu, 6 ur, 7 ir, 8 oo, 9 ey).

Limits. The copy used was a PDF converted to Word, so columns are sometimes
interleaved. One region (Kras, Krasnovaar, Krasaar) is patched by hand below.
646 of the 647 entries the dictionary says it has were identified.
"""
import json, re, sys
src, dst = sys.argv[1], sys.argv[2]
lines = open(src, encoding='utf-8').read().split('\n')
start = [i for i, l in enumerate(lines) if l.strip().startswith('Aak 1K')][0]
end = [i for i, l in enumerate(lines) if i > start + 15000 and l.strip() == 'A'][0]
DEC = {'1': 'aa', '2': 'ei', '3': 'ii', '4': 'ah', '5': 'uu', '6': 'ur', '7': 'ir', '8': 'oo', '9': 'ey'}
def dec(r): return ''.join(DEC.get(c, c.lower()) for c in r if c not in "-'’ ")
def norm(w): return re.sub(r"[^a-z]", "", w.lower())
RUNE = re.compile(r"[A-Z1-9][A-Z1-9\-'’]*$")
TYPES = ['strong verb', 'weak verb', 'strong adjective', 'weak adjective', 'noun', 'pronoun', 'adverb',
         'conjunction', 'preposition', 'article', 'interjection', 'prefix', 'suffix', 'adjective', 'verb', 'particle', 'numeral']
anchors = [i for i in range(start, end) if 'Word Type' in lines[i]]
def find_head(a, lo):
    cand = [j for j in range(a, max(lo, a - 9), -1) if lines[j].strip()]
    for j in cand:
        t = lines[j].strip()
        if 'Word Type' in t: t = t.split('Word Type')[0].strip()
        toks = t.split()
        if not toks: continue
        # roman + runes (runes may be split by a stray space)
        for a_i in range(len(toks)):
            w = toks[a_i]
            if not w[0].isupper(): continue
            for b in range(a_i + 1, len(toks) + 1):
                r = ''.join(toks[a_i + 1:b])
                if r and all(RUNE.match(x) for x in toks[a_i + 1:b]) and dec(r) == norm(w) and norm(w):
                    return j, w, r
        # multiword heading: N roman words then N rune words
        if len(toks) % 2 == 0 and len(toks) >= 4:
            h = len(toks) // 2
            if dec(''.join(toks[h:])) == norm(''.join(toks[:h])):
                return j, ' '.join(toks[:h]), ' '.join(toks[h:])
        # runes alone; the word is on the previous non-empty line
        if len(toks) == 1 and RUNE.match(toks[0]):
            k = j - 1
            while k > lo and not lines[k].strip(): k -= 1
            pw = lines[k].strip().split()
            if pw and dec(toks[0]) == norm(pw[-1]):
                return k, pw[-1], toks[0]
            if pw and dec(toks[0]) == norm(''.join(pw)):
                return k, ''.join(pw), toks[0]
    return None
entries = []; unresolved = []
prev = start - 1
for n, a in enumerate(anchors):
    h = find_head(a, prev)
    nxt = anchors[n + 1] if n + 1 < len(anchors) else end
    if not h:
        unresolved.append((a, [l.strip()[:70] for l in lines[a - 5:a + 1] if l.strip()]))
        prev = a; continue
    hl, word, runes = h
    block = [l.strip() for l in lines[a:nxt]]
    text = ' '.join(x for x in block if x)
    head4 = ' '.join(x for x in block[:6] if x)
    ipa = re.findall(r'/[^/]{1,60}/', head4)
    after = head4.split('Pronunciation', 1)[-1] if 'Pronunciation' in head4 else head4
    wt = ''
    pos_best = 10 ** 9
    for t in TYPES:
        m = re.search(r'\b' + t + r'\b', after)
        if m and m.start() < pos_best and m.start() < 160:
            pos_best = m.start(); wt = t
    # official definition: between "Official Definition" and "Expanded Definition"
    od = ''
    m = re.search(r'Official Definition(.*?)(?:Expanded Definition|Usage|Connotations|Etymology|Notes|See Also|$)', text)
    if m: od = m.group(1).strip()
    cites = re.findall(r'\(([^()]{2,80})\)', od)
    kinds = set()
    for c in cites:
        if c.startswith('Dialogue File'): kinds.add('dialogue_file')
        elif c.startswith('POGGLE'): kinds.add('prima_guide')
        elif c.startswith('PrimaGames'): kinds.add('primagames_com')
        elif c.startswith('Book'): kinds.add('book')
        elif 'Shout' in c: kinds.add('shout_menu')
        else: kinds.add('other')
    od_text = re.sub(r'\((?:Dialogue File|POGGLE|PrimaGames|Book)[^()]*\)|\([^()]*Shout\)', '', od).strip(' ;')
    od_text = re.sub(r'\s+', ' ', od_text)
    only_attested = bool(re.search(r'[Aa]ttested only in', text))
    misspell = bool(re.search(r'[Mm]isspelling of', text))
    entries.append({'word': word, 'runes': runes, 'word_type': wt, 'ipa': [x.strip() for x in ipa[:1]],
                    'official_definition': od_text, 'citations': cites, 'source_kinds': sorted(kinds),
                    'says_attested_only_in': only_attested, 'mentions_misspelling': misspell,
                    'line': a + 1, 'n_lines': nxt - a})
    prev = a
# Hand patch for the one garbled region.
for e in entries:
    if e['word'] == 'Kras':
        e.update({'official_definition': 'Sick', 'citations': ['PrimaGames.com'], 'source_kinds': ['primagames_com'], 'manual_patch': True})
if not any(e['word'] == 'Krasnovaar' for e in entries):
    entries.append({'word': 'Krasnovaar', 'runes': 'KRASNOV1R', 'word_type': 'noun', 'ipa': ['/\u02c8kr\u00e6s no v\u0251r/'],
                    'official_definition': 'Disease', 'citations': ['PrimaGames.com'], 'source_kinds': ['primagames_com'],
                    'says_attested_only_in': False, 'mentions_misspelling': False, 'line': 0, 'n_lines': 0, 'manual_patch': True})
    unresolved = [u for u in unresolved if 'KRASNOV1R' not in ' '.join(u[1])]
json.dump({'n': len(entries), 'unresolved': unresolved, 'entries': entries}, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('entries', len(entries), 'unresolved', len(unresolved))
for u in unresolved: print('  ', u)
