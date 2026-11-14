# Track 1: Canon Dovahzul — descriptive grammar, empirical phonotactics, gap map

Evidence base: the UESP snapshot in `research/data/` (657 dictionary rows, 704 corpus records, 2,442 running tokens after duplicates and names are removed). Labels: **canon** = game or in-game book text; **semi-canon** = Prima guide, Imperial Library list, developer statements; **fan** = wiki editors' English, community sites. Corpus ids are given in `code`. Treated in depth: c, d, e, the relex test, h. Treated briefly: b (text cannot settle it), f, g.

## 1. Bottom line

- **Canon gives a skeleton, not a language.** Word order and the function-word set are English; morphology is a handful of suffixes and two prefixes; 34 areas need a ruling before anyone can converse (section 2h, `research/data/grammar-gaps.json`).
- **"English with different words" is right about order, wrong about obligatoriness.** In six hand-aligned texts (221 tokens) no word is out of English order. The differences are all omissions or suffixes: articles, tense, plural, copula, pronouns, possessive `'s`.
- **There is no official pronunciation.** Neither the snapshot nor six web searches found one. Every IPA value the app ships is a project convention and must be labelled so.
- **Phonotactics are tight and learnable by rule.** CVC and CV make up 82% of syllables; 27 onsets and 16 codas each occur in five or more root words; all 136 shout words are monosyllables.
- **A validator must be two-stage.** 19% of canon root words contain a unit transition found in no other word, so "unattested bigram" cannot be a hard error. Inventory checks are hard rules; the bigram score is advisory.
- **The wiki's grammar summary under-describes the corpus.** Possessive suffixes split by person (-i "my", -ii "his/her", -iil "your") where the wiki gives one rule; plural and tense marking are optional in practice.
- **Most English in the data is fan gloss.** Only four sources carry in-game English. Exercises must show which translations are official.
- **No peer-reviewed study of this language was found.** The scholarly sources below support method (phonotactic modelling, productivity, typology), not facts about Dovahzul.

## 2. Findings

### a. Orthography and romanisation

Canon/semi-canon. The script has 34 runes: 25 single letters and nine two-letter runes AA AH EI EY II IR OO UU UR (Miller 2011; UESP 2026). There is no C, one case, and no apostrophe rune: 0 apostrophes in 1,138 rune-case tokens, with Thu'um written through the UU rune. TH and SH are two runes each.

Measured on the wiki's rune-case transcriptions (fan transcription of canon text): `aa` is one rune in 196 of 196 cases; `ah` in 225 of 240, split A+H in 15 (shout word SAH, Phantom Form); `ii` wins over `ir` (Viir = V-II-R). Rune frequency is led by O 538, N 454, R 361, K 293; UR occurs once.

Romanised-to-rune mapping (my inference from those counts): lower-case, delete apostrophes, then scan left to right taking the longest of the nine pairs, with a per-word exception list for split `ah`. Capitalisation and punctuation in Latin text are wiki practice, not canon (G34).

### b. Phonology

The data hold no sound values. The only remarks are fan notes: Alduin says the *j* of Vuljotnaak "as in Jon", unlike the *j* of Bromjunaar; the voice acting of Throw Voice suggests *Vun*, not *Zul*. Thuum.org publishes "typical IPA" for the runes (seen only as a search summary; fan). The table is therefore a **working proposal**: spelling-based inference plus my recollection of the voice acting, not checked against audio here.

| Units | Proposed value | Basis | Uncertainty |
|---|---|---|---|
| b d f g k l m n p s t v w z | as IPA | spelling | low |
| th, sh, y (consonant) | θ, ʃ, j | spelling; Thu'um, Shul in voice acting (recalled) | low |
| h before a vowel | h | spelling | low |
| j | dʒ or j | fan note records both in voice acting | high, contested |
| r | r or ɹ | voice acting varies (recalled) | medium |
| q, x | k (or kw), ks | spelling | high (q), medium (x) |
| aa, ii, uu | ɑː, iː, uː | spelling | medium |
| ah (eh, ih, oh) | ɑ(ː); h not sounded | voice acting (recalled); could be vowel + x | high |
| a, e, i, o, u | a~æ, ɛ, ɪ, o~ɔ, u~ʊ | spelling | high |
| ei, ey | aɪ, eɪ | community convention | high |
| oo | oː or uː | none | high |
| ir, ur, au, ae | ɪr, ur, aʊ, unknown | spelling | high |
| u'u | uʔu or uː | none | high |

Stress is unattested (G02).

### c. Empirical phonotactics

Script: `tools/analysis/phonotactics.py` (v1.1.0, extended in this pass with a `forge_profile` section); output: `research/data/canon-phonotactics.json`. All counts are over **spelling**, on 666 dictionary spellings; 597 are "root" words that cannot be cut into other entries.

- **Length.** Mean 4.88 letters, 4.22 runes. Syllables: one 53.6%, two 36.3%, three 8.7%, four 1.4%. Shout words: 136 of 136 monosyllabic. Translated dragon names: 38 of 41 trisyllabic.
- **Syllable shapes** (1,051 syllables): CVC 48.0%, CV 33.9%, CCVC 5.0%, VC 3.7%, CCV 3.6%, V 2.9%, CVCC 1.8%; CCCVC only in *strun* and its two compounds. Commonest whole words: CVC 205, CV.CVC 116.
- **Onsets** (36 types). 69 words are vowel-initial. Singles: v 53, n 44, d 41, m 39, k 37, s 37, f 34, r 34, h 30, l 28, z 24, t 19, b 18, g 17, p 14, w 13, j 12, q 12, th 5, y 5, sh 3. Clusters: kr 24, gr 13, br 11, dr 6, fr 5, pr 5, st 3, str 3, dw 2, kl 2, qu, sl, sm, sp 1 each. Obstruent + r is 64 of 77 cluster-initial words. Absent: tr, bl, fl, gl, pl, sk, sn, thr.
- **Codas** (29 types). n 157, none 121, l 67, k 61, r 46, s 41, d 33, t 23, m 22, v 18, z 17, th 12, g 8, nt 7, st 6, x 6, nd 4, f 3; one or two words each: lz, p, rn, ft, kt, ld, ll, lt, ng, rk, sh.
- **Nuclei.** o 257, aa 152, u 134, ah 121, i 114, ii 91, e 64, a 39, ey 30, ei 20, oo 9. Plain *a* is rarer than *aa* or *ah*.
- **Positional restrictions.** Never word-initial: x, ei, ey, oo, uu, u'u. Never word-final: aa, oo, uu, b, j, q, w, y. Vowel hiatus occurs in five words and doubled consonants in six, all but *nall* and *thurri* at a morpheme join.
- **Rime.** Final clusters follow a short vowel in 19 root words and a long one in 6; vowel + h is followed by a coda in 5 of 45. Vowel and coda are not independent, as in English (Kessler & Treiman 1997).
- **Letters.** a 14.4%, n 9.8%, i 9.7%, o 8.5%, r 6.7%, h 5.8%; e only 3.7%; c absent. 298 letter-bigram types; top: aa 152, ah 121, ii 91, in 84.
- **Tiers.** Onsets dw, sp and codas ft, ll, lt, lz occur only in semi-canon words.
- **Wordlikeness model** (new). A unit-bigram model with boundaries, add-0.5 smoothing, leave-one-out over the 597 roots: median −3.65 bits per transition, 5th percentile −4.90, 1st percentile −5.67. 113 roots (18.9%) contain a transition seen in no other word. English strings are not reliably separated by score alone (*strength* −4.41) but fail the coda inventory.

### d. Morphology

| Pattern | Evidence | Types | Label |
|---|---|---|---|
| Plural: double last letter + e | sille, meyye, drogge, dovahhe; kelle, joorre | 14 in corpus (22 tokens, 9 hapaxes) + 2 headwords | canon |
| Plural exceptions | hinde, bruniike (no doubling); mun/muz | 3 | canon |
| -i "my" | thuri (12), suleyki, bahloki, zini, viiki | 10 (25 tokens, 6 hapaxes) | canon form, fan gloss |
| -ii "his/her" | aarii, bormahii, kulii, monii, judii, zeymahii | 8 + briinahii | canon form, fan gloss |
| -iil "your"; -il | zaamiil (`dlg-skyrim-dragon-riding-13`); bormahil (`ww-slow-time-1`) | 1; 1 | canon form, fan gloss |
| -u "our" | bormahu, thu'umu | 2 | canon |
| -aan perfect/participle | boaan, duaan, kriaan, mahlaan, wahlaan, pelaan | 6 | canon + semi-canon |
| vo- "opposite" | vobalaan, vokiin, vomindok, vothaarn, vomir | 11 secure | Prima states the prefix |
| ni- "not" | nikrent, nivahriin, nikriin, nifaas | 4 | canon |
| -maar; -hus/-us | deinmaar, geinmaar; inhus, zaamhus | 4; 3 | mixed |
| agent -iik, -iid | wunduniik, saviik; kriid, kroniid | 2; 2 | mixed |
| linker *se* in compounds | sossedov, dovahsebrom, qethsegol | about 15 | canon |

Baayen's (1992) hapax-based index (hapaxes over tokens, counted from `corpus-oov.json`) gives 0.41 for the plural and 0.24 for -i, but on 22 and 25 tokens it is unstable; type counts alone do not show that a pattern is available for new words (Bauer 2001). -aan is not uniform: it attaches directly (bo-aan), drops a vowel (kri-aan) or inserts *l* (mah-l-aan), and also forms nouns (kulaan "prince"). Conversion is free: *mul* "strong, strength", *kron* "victory, win, conquer". The wiki's possessive rule (one -i for all persons, -l after ii) does not predict -iil, -il or the person split; the split is my reading of the wiki's glosses.

Compounds go both ways: head-first with *se* (the wiki's "head-initial" claim), head-last in bynames and solid compounds (Gaaf-Kodaav "Ghost-Bear", Dovahkiin, maltiid "little-time").

### e. Syntax

- **Order.** Subject, auxiliary, verb, object: *Hin sil fen nahkip bahloki* "Your soul will feed my hunger" (`dlg-skyrim-alduin-5`). Prepositions, noun before *do*-genitive, noun before relative clause, adjective before noun. The first three fit the verb-object type; adjective order does not correlate with it in Dryer's (1992) sample, so it is no counter-evidence.
- **Tense, aspect.** Bare verbs serve any tense (Miller 2011): *Het mah* "Here fell" (`ww-kyne-s-peace-3`). Future *fen* (16), *fent* (4). Perfect *lost* + verb: *Zu'u lost daal* (`dlg-skyrim-alduin-24`); with -aan: *Zu'u lost kriaan hi ont* (`dlg-skyrim-alduin-31`). *Drey* "did": *rok drey kod* (song). Passive: *fen kos duaan* (`dlg-skyrim-alduin-6`).
- **Mood.** *aal* "may", *nis* "cannot" (`dlg-skyrim-alduin-34`). Infinitive *wah* + verb. Imperative bare: *Aav uv dir* (`dlg-skyrim-alduin-15`).
- **Negation.** *ni* before the predicate: *Zu'u ni faas gaaffesejul* (`dlg-skyrim-alduin-33`); after an auxiliary: *Kel drey ni viik* (`dlg-skyrim-alduin-26`); after the verb on walls: *faas ni* (`ww-dismay-1`); with *dreh* once: *Dreh ni nahkip* (`dlg-skyrim-paarthurnax-dragon-8`). *nid* "no" + noun (9).
- **Questions.** Five question marks in all dialogue. *Wo meyz wah dii vul junaar?* (`dlg-skyrim-morokei-creature-1`); *Ful, losei Dovahkiin?* (`dlg-skyrim-alduin-10`), statement order.
- **Copula.** *los* 37, *kos* 8, *lost* 9, or nothing: *Zu'u Alduin, zok sahrot do naan ko Lein* (`dlg-skyrim-alduin-30`); *Mu ni meyye* (`dlg-skyrim-odahviing-4`). Zero copula is possible in 175 of 386 sampled languages (Stassen 2013); it is not English.
- **Articles.** *fin* 31, *faal* 9, *aan* 6, against 111 determiners the wiki had to add in brackets to 64 wall translations (1,108 tokens).
- **Pronouns** (count; — = unattested):

| | Subject | Object | Possessive word | Suffix |
|---|---|---|---|---|
| 1 sg | zu'u 23 | — | dii 10 | -i |
| 2 sg | hi 4 | hi | hin 20, him 1 | -iil (1) |
| 3 sg m / f | rok 13 / rek 7 | — | ok 22 / ek 4 | -ii |
| 3 sg n | nii 3 | nii | — | — |
| 1 pl | mu 8 | — | un 1 | -u |
| 2 pl | — | — | hin | — |
| 3 pl | nust 3 | niin 1 | — | — |

- **Prepositions.** do 82, wah 37, ko 28, naal 17, voth 15, se 10; also nau, au, ahst, nol, fah, zeim, kotin, us.
- **Conjunctions.** ahrk 36, nuz, uv, ol, fod, rul, fah, ful, ruz, erei. No "if" or "because".
- **Relative clauses.** *wo* 24, *wen* 18 after the noun: *wo drey yah moro* (`ww-aura-whisper-2`); *wen zul los sahlo* (`ww-throw-voice-1`).
- **Comparison.** *zok* "most": *Mulaagi zok lot* (`dlg-skyrim-alduin-19`). No comparative, no "than".

### f. Lexicon shape (brief)

657 entries, 725 glosses; 61 entries have several senses; 33 English glosses are shared by two or more headwords (the = faal/fin, of = do/se, on = au/nau, when = fod/rul, most = zok/zol). Homographs: *aan* a/idea/slave, *jun* king/light, *lok* sky/rise, *zol* most/zombie. Part of speech is stated on 15 rows; about 82 entries are function words by gloss. Running text: 658 types, 273 hapaxes; the top 100 forms cover 53% of tokens, the top 200 cover 71%. Field probe by exact gloss: elements 18 of 18, kin 11 of 13, numerals 3, question words 3 of 9, modals 3 of 9. No full part-of-speech tagging was done.

### g. Word Wall conventions (brief)

64 distinct inscriptions. Five openings begin 57 of them: *Qethsegol vahrukiv …* "(This) stone commemorates" (14); *Het nok …* "Here lies" (13); *X wahlaan qethsegol Y-ii vahrukt Z* "X raised (this) stone in memory of his/her Y, Z" (12); *Nonvul Bron, dahmaan daar rot do fin fodiiz bormah …* (10); *Het mah …* "Here fell" (8). Shared features: article-less register, epithet as *Name fin/faal Adjective* (Hrodmir fin Krent), hyphenated bynames, a *wo*/*wen* clause after the name, third-person -ii on kin terms, one highlighted word of power per wall.

### The "English with different words" test

A relex keeps a source language's grammar and swaps the words (Peterson 2015). Six texts were aligned by hand.

| Text | Tokens | Out of English order | Departures |
|---|---|---|---|
| Song of the Dragonborn, lines 1–10 (`song-of-the-dragonborn-songs-of-skyrim-1`; in-game English) | 159 | 0 | 6 unmarked plurals, 3 genitives by juxtaposition (*Alduin jot*), about 6 unmarked pasts, 1 unmarked superlative |
| `ww-unrelenting-force-1` | 15 | 0 | 1 article absent |
| `ww-aura-whisper-2` | 18 | 0 | 1 article absent |
| `dlg-skyrim-alduin-31` | 11 | 0 | "my power" = suleyk-i |
| `dlg-skyrim-alduin-11` | 10 | 0 | two clauses without copula |
| `dlg-skyrim-odahviing-2` | 8 | 0 | no possessor, no infinitive marker, no object pronoun |

**Holds:** order; the auxiliaries (*fen/fent* = will/shall, *lost* = have and was, *drey/dreh* = did/do, including do-support in *drey ni viik*); *wah* covering both English "to"s; *ol … ol* "as … as"; even the song's fronted phrases copy the English lyric, which was written to rhyme in both languages (Wilhelm 2021). **Fails:** articles optional; tense and plural optional; possession by suffix or juxtaposition; zero copula; dropped pronouns; usual negation without *do*; *se* compounds. The press claim that prepositional phrases come earlier (UESP 2026, citing Game Informer) is not visible in these texts. Conclusion (inference): canon Dovahzul is a reduced English relex plus a handful of suffixes.

### h. The gap map

Full records are in `grammar-gaps.json`. Severity: B blocking, H high, M medium, L low.

1. Sound values (B) 2. Stress, prosody (H) 3. Apostrophe (M) 4. Rune spelling rules (H) 5. Numerals (B) 6. Pronoun holes (B) 7. Possession (B) 8. Plural (H) 9. Tense, aspect (B) 10. Modality (H) 11. Questions (B) 12. Negation placement (H) 13. Copula (H) 14. Articles (M) 15. Comparison (H) 16. Relative and complement clauses (M) 17. Subordinators (H) 18. Prepositions (M) 19. Word-order freedom (M) 20. Commands, wishes (M) 21. Passive, participles (M) 22. Derivation (H) 23. Compound order (H) 24. Word classes (H) 25. Core vocabulary (B) 26. Rare and absent clusters (H) 27. Spelling variants (M) 28. Authority of glosses (H) 29. Semi-canon tiers (H) 30. Conversation formulas (H) 31. Shout formation (L) 32. Name formation (L) 33. Time and measures (M) 34. Romanisation norms (L).

## 3. What this means for the app

1. **One tokeniser everywhere.** Use the script's unit rules for lessons, validator and rune converter. Confidence: high.
2. **Rune converter.** Longest-match over nine pairs, `ii` before `ir`, apostrophes deleted, exception table for split `ah`. Confidence: high for aa/ii; medium for ah/ir/ur (G04).
3. **Validator stage 1, hard rules** from `forge_profile`: onset and coda must be attested; core items (27 onsets, 16 codas) pass; marginal ones (sh, dw, kl, st; nd, f, rn) pass with a flag; single-word ones go to the owner; no hiatus or doubled consonant inside a root; no c; shout words one syllable. Confidence: high as description; the tier cut-offs (5, 2) are my choice.
4. **Stage 2, advisory score.** Pass at or above −4.90, warn down to −5.67, send lower to the owner. Gradient scores of this kind track human wordlikeness ratings (Frisch et al. 2000; Vitevitch & Luce 2004; Hayes & Wilson 2008), but this model is untested on human judgments of Dovahzul. Confidence: medium.
5. **Stage 3, lexicon check.** Block exact homographs by default; warn at edit distance 1, since neighbours shape wordlikeness independently of phonotactics (Bailey & Hahn 2001). Confidence: medium.
6. **Absent clusters need a ruling, not a guess.** A lexicon-trained model can rank unattested clusters only if it encodes sonority and syllable position (Daland et al. 2011); a bigram table cannot. Until G26 is ruled, reject. Confidence: high.
7. **Morphology as data.** Each rule is a record with pattern, exceptions, tier and evidence ids. Ship -i/-ii/-iil as "attested, ruling pending".
8. **Rulings as versioned objects.** Each of the 34 gaps becomes a ruling id; forge rules and lessons cite the ids they depend on. A fan community that routes proposals to one authority is a documented, working model (Schreyer 2015). Confidence: medium.
9. **Teach the skeleton as "English order, optional marking".** Start with the five wall templates and the 100 most frequent forms. Confidence: high for the counts; the pedagogy belongs to other tracks.
10. **Word classes by behaviour.** Assign classes from distribution in the corpus, not from the English gloss (Haspelmath 2010). Confidence: medium.
11. **Pronunciation as labelled convention**, each value carrying its basis; verify against game audio before recording. Confidence: high that this is needed.
12. **Sequence.** Rule on G01, G05, G06, G07, G09, G11, G25 first.

## 4. Contested or weak evidence

- All IPA values; *j* is contested by the wiki's own note.
- Person values of -i/-ii/-iil rest on fan glosses and one or two tokens for -iil and -il.
- Some glosses contradict the words: *Zu'u ni bo nol het* is given as "I will be here" (`dlg-skyrim-odahviing-10`).
- The Prima guide (Hodgson 2011) was not read; its content is known through the wiki's 176 citations. Thuum.org (n.d.) reports that Prima confirmed its list came from Bethesda: fan report.
- Productivity indices on about 20 tokens are indicative only.
- The alignment covers 221 tokens chosen by hand, not a sample.
- "Syllable", "onset", "coda" are constructs over spelling.
- Schreyer (2015) is cited from memory of its content.

## 5. Gaps, and anything that was blocked

- No peer-reviewed or academic-press study of the dragon language was found in two extended searches.
- No official pronunciation guide was found; the Prima guide's alphabet section could not be inspected.
- thuum.org was not accessed (it refuses automated requests); only search summaries were used.
- Game audio was not available, so no voice-acting claim is verified.
- Not done: full part-of-speech tagging, a count of zero-copula clauses, alignment of all 64 walls.
- Reference checker: 11 verified, 2 not_found (both books, confirmed by web search: Peterson 2015 on the publisher's page; the Prima guide on catalogue pages, credited there to David Hodgson for the 2011 edition), 5 manual.

## 6. References

- Baayen, H. (1992). Quantitative aspects of morphological productivity. *Yearbook of Morphology 1991*. doi:10.1007/978-94-011-2516-1_8
- Bailey, T. M.; Hahn, U. (2001). Determinants of Wordlikeness: Phonotactics or Lexical Neighborhoods? *Journal of Memory and Language*. doi:10.1006/jmla.2000.2756
- Bauer, L. (2001). *Morphological Productivity*. Cambridge University Press. doi:10.1017/CBO9780511486210
- Daland, R.; Hayes, B.; White, J.; Garellek, M.; Davis, A.; Norrmann, I. (2011). Explaining sonority projection effects. *Phonology*. doi:10.1017/S0952675711000145
- Dryer, M. S. (1992). The Greenbergian Word Order Correlations. *Language*. doi:10.2307/416370
- Frisch, S. A.; Large, N. R.; Pisoni, D. B. (2000). Perception of Wordlikeness: Effects of Segment Probability and Length on the Processing of Nonwords. *Journal of Memory and Language*. doi:10.1006/jmla.1999.2692
- Haspelmath, M. (2010). Comparative concepts and descriptive categories in crosslinguistic studies. *Language*. doi:10.1353/lan.2010.0021
- Hayes, B.; Wilson, C. (2008). A Maximum Entropy Model of Phonotactics and Phonotactic Learning. *Linguistic Inquiry*. doi:10.1162/ling.2008.39.3.379
- Hodgson, D. (2011). *The Elder Scrolls V: Skyrim: Prima Official Game Guide*. Prima Games. https://en.m.uesp.net/wiki/Books:The_Elder_Scrolls_V:_Skyrim:_Prima_Official_Game_Guide [book; not in Crossref; confirmed by web search; not read]
- Kessler, B.; Treiman, R. (1997). Syllable Structure and the Distribution of Phonemes in English Syllables. *Journal of Memory and Language*. doi:10.1006/jmla.1997.2522
- Miller, M. (2011). Skyrim's Dragon Shouts. *Game Informer*. https://gameinformer.com/b/features/archive/2011/01/20/skyrim-s-dragon-shouts?PostPageIndex=1 [read as archived on UESP]
- Peterson, D. J. (2015). *The Art of Language Invention: From Horse-Lords to Dark Elves, the Words Behind World-Building*. Penguin Books. https://www.penguinrandomhouse.com/books/isbn/9780143126461 [book; not in Crossref; confirmed by web search]
- Schreyer, C. (2015). The digital fandom of Na'vi speakers. *Transformative Works and Cultures*. doi:10.3983/twc.2015.0610
- Stassen, L. (2013). Zero Copula for Predicate Nominals. *The World Atlas of Language Structures Online (WALS)*, chapter 120. https://wals.info/chapter/120
- Thuum.org (n.d.). About (thuum.org, a community for the dragon language of The Elder Scrolls V: Skyrim). https://thuum.org/about.php [fan; search summary only]
- UESP contributors (2026). Lore:Dragon Language (revision 3619598 of 2026-08-24). *The Unofficial Elder Scrolls Pages (UESP)*. https://en.m.uesp.net/wiki/Lore:Dragon_Language
- Vitevitch, M. S.; Luce, P. A. (2004). A Web-based interface to calculate phonotactic probability for words and nonwords in English. *Behavior Research Methods, Instruments, & Computers*. doi:10.3758/BF03195594
- Wilhelm, P. (2021). How Bethesda Game Studios made Skyrim's Dragon language. elderscrolls.bethesda.net (Bethesda Softworks), 26 August 2021. https://elderscrolls.bethesda.net/en-AU/news/1rL4bCScN6RYXaXQb4ownj/how-bethesda-game-studios-made-skyrims-dragon-language
