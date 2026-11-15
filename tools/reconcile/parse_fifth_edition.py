"""Parse a plain-text conversion of the Dragon Language Dictionary, Fifth
Edition (Thuum.org) into one record per entry.

The dictionary is kept in research/sources/thuum/ (see ATTRIBUTION.md there
for its terms: non-commercial use, with credit). To re-run:

    pandoc -t plain --wrap=none \
        research/sources/thuum/Dragon_Language_Print_Dictionary_5th_Edition.docx \
        -o /tmp/dictionary.txt
    python3 -I tools/reconcile/parse_fifth_edition.py /tmp/dictionary.txt \
        research/data/fifth-edition.json

Method. Every entry carries a "Word Type" line, which is used as the anchor.
The heading above it is recognised by matching the word against its rune
spelling, in which the digits 1-9 stand for the two-letter runes
(1 aa, 2 ei, 3 ii, 4 ah, 5 uu, 6 ur, 7 ir, 8 oo, 9 ey).

Limits. The copy used was a PDF converted to Word, so columns are sometimes
interleaved. One region (Kras, Krasnovaar, Krasaar) is patched by hand below.
The copy holds 646 entries; the dictionary's introduction says 647. An
independent second parser found the same 646 headings. The word type is blank
for 26 entries whose heading is laid out as a table. The copy itself misprints
a few definitions (for example Krah, Krii, Sosaal, Gron), which this script
records as printed.
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
SECTION = re.compile(r'\b(Official Definition|Expanded Definition|Usage|Connotations|Etymology|Notes|See Also)\b')
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
    # The copy spells the dialogue tag three ways ("Dialogue File", "Dialogue FIle",
    # "Dialogue") and sometimes drops a closing bracket; accept all of them.
    paren = re.findall(r'\(([^()]{2,80})\)', od) + re.findall(r'\((POGGLE, p\. \d+)(?![\d)])', od)
    cites = []; remarks = []; kinds = set()
    for c in paren:
        if re.match(r'Dialogue(\s+F[Ii]le)?\s*,', c): kinds.add('dialogue_file'); cites.append(c)
        elif c.startswith('POGGLE'): kinds.add('prima_guide'); cites.append(c)
        elif c.startswith('PrimaGames'): kinds.add('primagames_com'); cites.append(c)
        elif c.startswith('Book'): kinds.add('book'); cites.append(c)
        elif c.endswith('Shout'): kinds.add('shout_menu'); cites.append(c)
        else: remarks.append(c)   # a bracketed remark inside the definition, not a source
    od_text = re.sub(r'\((?:Dialogue|POGGLE|PrimaGames|Book)[^()]*\)?|\([^()]*Shout\)', '', od).strip(' ;')
    od_text = re.sub(r'\s+', ' ', od_text)
    parts = SECTION.split(text)
    sec = {}
    for q in range(1, len(parts) - 1, 2):
        sec.setdefault(parts[q], []).append(parts[q + 1].strip())
    def S(name): return ' '.join(x for x in sec.get(name, []) if x)
    prons = [x.strip() for x in re.findall(r'/[^/]{1,80}/', parts[0])]
    if wt == 'adjective' and 'trong adjective' in after: wt = 'strong adjective'
    only_attested = bool(re.search(r'[Aa]ttested only in', text))
    misspell = bool(re.search(r'[Mm]isspelling of', text))
    entries.append({'word': word, 'runes': runes, 'word_type': wt, 'ipa': [x.strip() for x in ipa[:1]],
                    'pronunciations_as_printed': prons,
                    'official_definition': od_text, 'citations': cites, 'remarks_in_definition': remarks, 'source_kinds': sorted(kinds),
                    'expanded_definition': S('Expanded Definition'), 'usage': S('Usage'), 'connotations': S('Connotations'),
                    'etymology': S('Etymology'), 'notes': S('Notes'), 'see_also': S('See Also'),
                    'says_attested_only_in': only_attested, 'mentions_misspelling': misspell,
                    'line': a + 1, 'n_lines': nxt - a})
    prev = a
# Hand patch for the one garbled region.
for e in entries:
    if e['word'] == 'Kras':
        e.update({'official_definition': 'Sick', 'citations': ['PrimaGames.com'], 'source_kinds': ['primagames_com'], 'manual_patch': True})
    if e['word'] == 'Krasaar':
        e.update({'official_definition': 'Sickness', 'citations': ['Book, Dragon Language: Myth No More', 'POGGLE, p. 1096', 'PrimaGames.com'],
                  'source_kinds': ['book', 'prima_guide', 'primagames_com'], 'says_attested_only_in': False, 'manual_patch': True})
if not any(e['word'] == 'Krasnovaar' for e in entries):
    entries.append({'word': 'Krasnovaar', 'runes': 'KRASNOV1R', 'word_type': 'noun', 'ipa': ['/\u02c8kr\u00e6s no v\u0251r/'],
                    'official_definition': 'Disease', 'citations': ['PrimaGames.com'], 'source_kinds': ['primagames_com'],
                    'says_attested_only_in': True, 'mentions_misspelling': False, 'line': 0, 'n_lines': 0, 'manual_patch': True})
    unresolved = [u for u in unresolved if 'KRASNOV1R' not in ' '.join(u[1])]
# The text between two "Word Type" lines ends with the next entry's heading; cut it off.
SECTIONS_OUT = ['see_also', 'notes', 'etymology', 'connotations', 'usage', 'expanded_definition']
for k in range(len(entries) - 1):
    nw, nr = entries[k + 1]['word'], entries[k + 1]['runes']
    tail = re.compile(r'\s*' + re.escape(nw) + r'\s+' + r'\s*'.join(re.escape(x) for x in nr.split()) + r'\s*$')
    tail2 = re.compile(r'\s*' + re.escape(nw) + r'\s*$')
    for f in SECTIONS_OUT:
        v = entries[k].get(f)
        if v:
            v2 = tail.sub('', v)
            if v2 == v and nr and v.rstrip().endswith(nr): v2 = tail2.sub('', v[:v.rstrip().rfind(nr)])
            entries[k][f] = v2.strip()
            break
for e in entries:
    for f in ['pronunciations_as_printed', 'remarks_in_definition']: e.setdefault(f, [])
    for f in ['expanded_definition', 'usage', 'connotations', 'etymology', 'notes', 'see_also']: e.setdefault(f, '')
DOUBTS = {
    'Kras': 'this region of the copy is interleaved; only the definition and source were read, by hand',
    'Krasaar': 'this region of the copy is interleaved; only the definition and source were read, by hand',
    'Krasnovaar': 'this region of the copy is interleaved; only the definition and source were read, by hand',

    "Zu'u": 'word type is printed as a verb; the entry itself defines a pronoun',
    'Krah': 'definition is misprinted in the copy (it repeats the previous entry); the expanded definition has "cold"',
    'Krii': 'definition is misprinted in the copy (it repeats the previous entry); the expanded definition has "to kill"',
    'Sosaal': 'definition is misprinted in the copy (it repeats the previous entry); the expanded definition has "to bleed"',
    'Gron': 'definition is cut short in the copy; the expanded definition has "to bind"',
    'Unslaad': 'definition is printed identically to that of Unahzaal',
    'Niid': 'definition is printed as "Niid No"',
    'Hofkiin': 'pronunciation is printed identically to that of Hofkah',
    'Thaarn': 'cites a book and the guide, but its usage note says it is attested only on the guide website',
    'Kun': 'cites a dialogue line, but the entry says the word is inferred and the line reads jun',
}
for e in entries:
    if e['word'] in DOUBTS: e['doubt'] = DOUBTS[e['word']]
    if not e['word_type']: e['doubt_word_type'] = 'not read: the heading is laid out as a table in the copy'
META = {
    'title': 'Dragon Language Dictionary, Dragon-English and English-Dragon, Fifth Edition',
    'publisher': 'Thuum.org',
    'original': 'https://www.thuum.org/library/Dragon_Language_Print_Dictionary_5th_Edition.pdf',
    'copy_used': 'research/sources/thuum/Dragon_Language_Print_Dictionary_5th_Edition.docx, a Word conversion of the PDF supplied by the project owner on 2026-11-15',
    'terms': 'Non-commercial use, with credit to Thuum.org. See research/sources/thuum/ATTRIBUTION.md for the basis.',
    'what_is_official': 'By the dictionary\'s own statement only the official definition and the usage quotations come from official sources. Word type, pronunciation, expanded definition, connotations, etymology and notes are its authors\' analysis.',
    'limits': 'The copy is a PDF converted to Word, so columns are sometimes interleaved and section text can carry stray words from a neighbouring entry. It holds 646 entries; the introduction says 647. One region was read by hand. Word type is blank for 26 entries. Entries with a known misprint or doubt carry a "doubt" field. Section text is as printed and was not proofread.',
    'fields': {'word': 'heading as printed', 'runes': 'rune spelling in the font\'s key codes (1 aa, 2 ei, 3 ii, 4 ah, 5 uu, 6 ur, 7 ir, 8 oo, 9 ey)',
               'word_type': 'the dictionary\'s own class', 'ipa': 'first pronunciation', 'pronunciations_as_printed': 'all pronunciations in the heading',
               'official_definition': 'definition quoted from an official source', 'citations': 'sources cited for that definition',
               'remarks_in_definition': 'bracketed remarks that are part of the definition', 'source_kinds': 'dialogue_file, book, shout_menu, prima_guide, primagames_com',
               'expanded_definition, usage, connotations, etymology, notes, see_also': 'the other sections of the entry, as printed'},
}
json.dump({'meta': META, 'n': len(entries), 'unresolved': unresolved, 'entries': entries}, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('entries', len(entries), 'unresolved', len(unresolved))
for u in unresolved: print('  ', u)
