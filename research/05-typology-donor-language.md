# 05. Typology and donor language: what Dovahzul is most like, and what the forge should borrow

Scope. Sub-questions (a), (b), (c) and (e) are treated in depth; (d) and pragmatics briefly. Dovahzul counts come from `research/data/` (UESP contributors 2026) and were computed in this session. Labels: game text is **canon**; developer statements quoted by the wiki are **semi-canon**; English glosses are mostly wiki editors' readings (**fan**); every starred form is a **forge-tier (fan)** proposal.

## 1. Bottom line

- On 30 parameters framed by the World Atlas of Language Structures (WALS), canon Dovahzul is closest to **Modern English (0.82)** and **Afrikaans (0.80)**, far from Old English (0.66), Icelandic (0.65), Old Norse (0.62) and mainland Scandinavian (0.58), and farther still from Mandarin, Indonesian, Vietnamese and Yoruba (0.45 to 0.55). Its grammar is analytic West Germanic, not Norse.
- The "relexified English" hypothesis holds for word order and function-word meaning: across 66 canon texts the order of Dovahzul words and of their English renderings agrees at a pooled Kendall tau of 0.989; for the Song of the Dragonborn, whose English lyric is an independent text, tau is 0.975.
- It is not a pure relex. Seven departures from English are attested in canon (no obligatory tense, optional articles, possessive suffixes, no 's-genitive, `ni` negation without do-support, optional plural, subject drop). These are the language's identity; the forge should lock them.
- Old Norse and Old English are the costume, not the skeleton: runestone-style memorial formulas, bynames, kenning-like compounds. Canon has no alliterative verse (the Song rhymes) and its sound system is not Old Norse.
- Donor precedence for every gap: canon attestation, then language-internal analogy, then Modern English structure, then Old English or Old Norse pattern as an archaising tie-breaker. Borrow patterns, never word forms.
- Never import case endings, grammatical gender, verb agreement, a suffixed article, verb-second order, umlaut or ablaut, question particles, polite pronouns, or onsets absent from canon (`hr-`, `sk-`, `kn-`, `tr-`).
- Build a machine-readable typology profile and make the forge validator reject any rule that flips a locked parameter.

## 2. Findings

### 2a. Canon Dovahzul coded on WALS parameters

Evidence base: 2,296 tokens in non-duplicate dialogue, word-wall, song and proverb records; 657 dictionary rows; `canon-phonotactics.json`. Feature definitions follow WALS (Dryer & Haspelmath 2013).

**Order.** SVO (81A): `Zu'u koraav nid nol dov do hi` "I see no dragon in you"; `Hin sil fen nahkip bahloki` "Your soul will feed my hunger". Prepositions only (85A): all 19 adposition entries precede the noun (`ko Sovngarde`, `voth ahkrin`). Lexical possessor follows (86A): `drog do lot nir` "lord of the great hunt", `do` 82 tokens; 15 fused `-se-` types (`sillesejoor` "souls of mortals"); the wiki's grammar note records the developers' statement that there is no equivalent of the English apostrophe. Adjective, demonstrative and quantifier precede the noun (87A, 88A): `dii vul junaar` "my dark kingdom", `daar rot` "these words", `pogaan kiir` "many children". Relative clauses follow, introduced by `wo`/`wen` (90A): `Vahlok wo kron pogaas moro` "the Guardian who gained much glory". Interrogative phrase initial (93A): `Wo meyz wah dii vul junaar?` Negator before the lexical verb (143A): `Zu'u ni faas gaaffesejul` "I do not fear mortal ghosts", `Kel drey ni viik`, `Fent ni filok`; one imperative has the reverse (`Faas ni brendon do dinok` "Fear not the specter of death"). No question particle in the five attested questions (92A): `Ful, losei Dovahkiin?`

**Nominal.** No noun case (49A). Plural by suffix, doubling the last Latin letter and adding `e` (33A): 17 types (`kelle`, `sille`, `joorre`, `dovahhe`, `meyye`), but plural reference is often unmarked (`ok hokoron` "his enemies"). The rule works on Latin letters, not runes: `dovahhe` doubles only the `h` of the `ah` rune. Definite `fin`/`faal` (40 tokens) distinct from demonstrative `daar` (37A); indefinite `aan` (6) distinct from `gein` "one" (38A). Possessive suffixes exist beside preposed possessives (57A): `thuri` "my lord" (12 tokens), `zeymahi`, `bormahu`, `kulii`, `zaamiil`, against `hin sil`, `ok zin`. Gender only in third-person singular pronouns `rok`/`rek`/`nii` (44A). One second-person pronoun, `hi` (45A).

**Verbal.** No person or number marking (102A): `los`, `kos`, `fen` are invariant. No obligatory past (66A): the wiki quotes the developers that "verb tense is often ignored", and walls use bare verbs for past events (`Het dir...` "Here died..."). Periphrastic future `fen`/`fent` (67A); perfect with `lost` plus verb, optionally with `-aan` (68A): `Zu'u lost kriaan hi` "I have killed you". Passive with `kos` plus participle and `naal` "by" (107A): `fen kos duaan` "will be devoured". Bare-stem imperative (70A). The only inflection-like affixes are plural, possessive and `-aan` (20A, 26A).

**Sound (from spelling only; the data holds no pronunciation guide).** About 20 to 22 consonants (1A, "average"); voicing contrast in plosives and fricatives (4A); `th` written in 20 headwords (19A); complex syllables (12A): onsets to `str-`, codas `-nd -nt -st -rk -lz -kt`; CVC is the commonest syllable (504 of about 1,050); 136 of 136 shout words are monosyllables. No tone (13A). Vowel-quality count (2A) cannot be coded.

Confidence: high for order, case, agreement and negation; medium for tense, articles and plural (optional marking); low for the phonological codings and for questions (five tokens).

### 2b. Comparison and similarity score

Values for English, Mandarin, Vietnamese, Indonesian and Yoruba are WALS v2020.6 values fetched today (Mandarin articles from Li & Thompson 1981; Vietnamese profile cross-checked with Nguyễn 1997). Icelandic and mainland Scandinavian (Swedish value, else Danish or Norwegian) use WALS where it has a value and Thráinsson (2007) and Holmes & Hinchliffe (2013) otherwise. Old English and Old Norse are not in WALS: I coded them from Fischer et al. (2000), Mitchell & Robinson (1982), Faarlund (2007) and Harbert (2007). WALS has only the tense features for Afrikaans; the rest is my coding from Donaldson (1993). `?` means not coded. 68A is recoded by construction type.

| WALS | Feature | Dov | Eng | OE | ON | Ice | MSc | Afr | Man | Vie | Ind | Yor |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 81A | S/O/V order | SVO | SVO | SOV/SVO | SVO | SVO | SVO | SOV/SVO | SVO | SVO | SVO | SVO |
| 85A | Adposition | Prep | Prep | Prep | Prep | Prep | Prep | Prep | Post/Prep | Prep | Prep | Prep |
| 86A | Genitive, noun | NGen | both | both | NGen | NGen | GenN | both | GenN | NGen | NGen | NGen |
| 87A | Adjective, noun | AdjN | AdjN | AdjN | AdjN | AdjN | AdjN | AdjN | AdjN | NAdj | NAdj | NAdj |
| 88A | Demonstrative, noun | DemN | DemN | DemN | both | DemN | DemN | DemN | DemN | NDem | NDem | NDem |
| 90A | Relative clause, noun | NRel | NRel | NRel | NRel | NRel | NRel | NRel | RelN | NRel | NRel | NRel |
| 143A | Negation, verb | NegV | NegV | NegV | both | both | both | both | NegV | NegV | NegV | NegV |
| 92A | Polar question particle | none | none | none | none | none | none | none | final | final | particle | none |
| 93A | Wh-phrase | initial | initial | initial | initial | initial | initial | initial | in situ | in situ | both | initial |
| 37A | Definite article | word | word | dem | affix | affix | affix | word | none | word | dem | none |
| 38A | Indefinite article | word | word | none | none | none | =one | word | ? | ? | none | none |
| 33A | Plural coding | suffix | suffix | suffix | suffix | suffix | suffix | suffix | suffix | word | redup | word |
| 49A | Noun cases | 0 | 2 | 4 | 4 | 4 | 2 | 0 | 0 | 0 | 0 | 0 |
| 44A | Pronoun gender | 3sg | 3sg | 3sg | 3sg+pl | 3sg+pl | 3sg | 3sg | 3sg | none | none | none |
| 57A | Possessive affixes | suffix | none | none | none | none | none | none | none | none | none | none |
| 66A | Past tense | no | yes | yes | yes | yes | yes | yes | no | no | no | no |
| 67A | Inflectional future | no | no | no | no | no | no | no | no | no | no | no |
| 68A | Perfect | aux+ptcp | aux+ptcp | aux+ptcp | aux+ptcp | aux+ptcp | aux+ptcp | aux+ptcp | none | other | other | other |
| 102A | Verbal person marking | none | A | A | A | A | none | none | none | none | P | none |
| 26A | Affix position | little/suffix | suffix | suffix | suffix | suffix | suffix | ? | suffix | little | suffix | little |
| 20A | Fusion | isol/concat | concat | concat | concat | concat | concat | isol/concat | isol/concat | isol | isol | isol/tonal |
| 112A | Negative morpheme | particle | particle | particle | particle | particle | particle | particle | particle | particle/verb | particle/verb | particle/verb |
| 107A | Passive | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | no |
| 70A | Morphological imperative | none | none | sg+pl | sg | sg | neutral | none | none | none | none | none |
| 12A | Syllable structure | complex | complex | complex | complex | complex | complex | complex | moderate | moderate | complex | simple |
| 13A | Tone | none | none | none | none | none | simple | none | complex | complex | none | complex |
| 19A | Th sounds | th | th | th | th | th | none | none | none | none | none | other |
| 1A | Consonant inventory | average | average | ? | ? | ? | average | ? | average | average | average | mod. small |
| 4A | Voicing contrast | both | both | plosives | plosives | ? | plosives | ? | fricatives | fricatives | both | plosives |
| 45A | Pronoun politeness | none | none | none | none | ? | binary | binary | binary | avoid | avoid | binary |

Score: unweighted mean agreement over comparable features, in the manner of Gower (1971): 1 for the same value, 0.5 where one side is a mixed value containing the other, 0 otherwise. Unweighted feature profiles of this kind have been used for planned languages by Parkvall (2010) and Brosch (2024) [UNVERIFIED: not in Crossref; publisher PDF seen in search results].

| | Eng | Afr | OE | Ice | ON | MSc | Man | Ind | Vie | Yor |
|---|---|---|---|---|---|---|---|---|---|---|
| All (features compared) | 0.82 (30) | 0.80 (27) | 0.66 (29) | 0.65 (27) | 0.62 (29) | 0.58 (30) | 0.55 (29) | 0.53 (30) | 0.50 (29) | 0.45 (30) |
| Order (9) | 0.94 | 0.83 | 0.89 | 0.94 | 0.89 | 0.83 | 0.50 | 0.61 | 0.56 | 0.78 |
| Nominal (6) | 0.67 | 0.83 | 0.33 | 0.17 | 0.17 | 0.33 | 0.60 | 0.17 | 0.40 | 0.17 |
| Verbal (9) | 0.67 | 0.88 | 0.56 | 0.56 | 0.56 | 0.67 | 0.83 | 0.61 | 0.72 | 0.61 |
| Without phonology | 0.78 | 0.81 | 0.64 | 0.60 | 0.60 | 0.62 | 0.62 | 0.48 | 0.56 | 0.54 |

Reading. English and Afrikaans are indistinguishable at this resolution (one feature is worth 0.03). What separates them from Old English, Old Norse and Icelandic is nominal and verbal inflection, exactly what Dovahzul lacks. Where Dovahzul leaves English it moves toward the isolating type (verbal score with Mandarin 0.83), not toward Norse.

Limits. (1) Features are not independent: word-order features correlate (Dryer 1992), so the nine order rows overstate agreement among verb-object languages. (2) The 30 features are my selection. (3) Old English, Old Norse and most Afrikaans cells have one coder and no reliability check. (4) Dovahzul is coded from a small formulaic corpus. (5) WALS categories cannot see do-periphrasis or polysemy, hence 2c.

### 2c. The "relexified English" hypothesis

**What linguists mean.** Relexification was defined in contact linguistics: Media Lengua keeps Quechua grammar while replacing lexical shapes with Spanish ones (Muysken 1997); Lefebvre (1998) made the copying of a first-language lexical entry under a new phonological label the central mechanism of creole genesis, a claim DeGraff (2002) [UNVERIFIED by the registry; confirmed on the journal's contents page] contests in detail. Conlang makers use "relex" for an invented vocabulary laid over the maker's native grammar; Peterson (2015) is the standard practitioner reference (book confirmed to exist; wording not checked). Recent reviews treat conlangs as serious objects of study (Schreyer 2021; Goodall 2023), and Peterson & Peterson (2024) argue that a conlang must be evaluated against its intended purpose. Parkvall (2010) found Esperanto "somewhat European in character, but considerably less so than the European languages themselves": a designer's native type leaks into a planned language only in part. On Dovahzul itself, Novikov (2022) calls the system Anglocentric and points to the calqued idiom "keep at bay" (search summary only; full text not read). Bethesda's own account (Bethesda Game Studios n.d.), as quoted in search results, calls the language much simpler than Tolkien's and built with "smoke and mirrors".

**Test 1: order isomorphism (this session).** For 64 distinct word walls and 2 songs I aligned each Dovahzul token that occurs once and whose dictionary gloss matches exactly one word of the English text (873 of 1,292 tokens), then compared orders. Pooled Kendall tau is 0.989 (47 discordant pairs of 8,313); 60 of 64 walls score 1.00; the Song scores 0.975 over 84 tokens. Caveat: wall translations are literal glosses, so agreement is partly built in; the Song is the fairer test.

**Test 2: English-specific calques (canon text, fan glosses).** Do-periphrasis: `rok drey kod` "he did wield", `wo drey yah moro` "who did seek glory" (`drey` 6, `dreh` 2); among Germanic languages this auxiliary use is a hallmark of English (Huddleston & Pullum 2002; Harbert 2007). `wah` is both the preposition "to" and the infinitive marker (38 tokens). `lost` covers "was, have, has, had, were" and builds the perfect. `tol` "that" is demonstrative and complementiser (`ful tol` "so that"). `wo`, `wen` are both interrogative and relative. Phrasal and idiom calques: `nos tum` "strike down"; `dein ... ahst vaal`, where the dictionary glosses `vaal` as 'Bay. As in "hold at bay"'.

**Test 3: the residue that is not English.**

| Departure | Evidence | Nearest natural parallel (my inference) |
|---|---|---|
| Tense optional | developer statement; bare past verbs on walls | isolating languages; WALS 66A |
| Articles optional | in the 66 texts translators supplied 74 "(the)" and 7 "(a)" against 45 overt articles: about 64% of English article slots are empty | article-poor Old English and Old Norse (Harbert 2007) |
| Possessive suffixes | `thuri`, `zeymahi`, `bormahu`, `kulii` | no Germanic language has them (57A); closest is the postposed possessive of Old Norse and Icelandic (Faarlund 2007; Thráinsson 2007) |
| No 's-genitive; `do`, `-se-` | 82 + 15 types | Icelandic and Old Norse noun-genitive order |
| `ni` before the verb, no do-support | `Zu'u ni faas` | Old English `ne` + finite verb (Fischer et al. 2000; Mitchell & Robinson 1982) |
| Plural by letter doubling + `e`, optional | 17 types | spelling pattern of Afrikaans `kat/katte`, `pen/penne` (Donaldson 1993) |
| Subject drop | `Fen du hin sille ko Sovngarde!`, `Lost funt.` | none among the Germanic candidates |

Verdict: Dovahzul is English syntax and English lexical semantics, simplified toward the isolating type and decorated with a few deliberate exoticisms. Confidence: high for syntax and function words; the word shapes themselves are a priori, not English.

### 2d. The aesthetic and cultural model

- **Memorial formula.** Viking-Age rune-stones follow a sponsor formula, "X raised this stone in memory of Y", plus a kin term and optional praise (Sawyer 2000). Of 64 distinct walls, 12 use `X wahlaan qethsegol [kin]-ii vahrukt Y` (`Nafni wahlaan qethsegol bormahii vahrukt Rognvald`), 14 open `Qethsegol vahrukiv` "this stone commemorates", 24 open `Het nok/dir/mah` (the English epitaph "Here lies", not a Norse pattern), and 10 open `Nonvul Bron, dahmaan daar rot do fin Fodiiz Bormah`. Sixty of 64 walls are four formulas.
- **Compounds and kennings.** Old English poetry builds much of its diction from two-member nominal compounds (Kastovsky 1992; Davis-Secord 2016); a skaldic kenning joins a base word to a determinant (Clunies Ross 2005); whether the strict kenning is characteristic of Old English at all is disputed (Gardner 1969). Canon has both Germanic right-headed compounds (`Dovahkiin` dragon+born, `Dovahkriid` dragon+slayer, `bronjun` Nord+king "jarl"; bynames `Gaaf-Kodaav` "Ghost-Bear", `Keyn-Haal` "Anvil-Hand") and left-headed ones (`zeymahzin` brother+honor "companion", `juntiid` king+time, `Qethsegol`, literally "bone of earth", a true kenning). Germanic compounds are right-headed (Bauer 2017; Harbert 2007), so the wiki's "head-initial" note describes only half of canon.
- **Verse.** Old English and Old Norse verse is organised by alliteration across half-lines, any vowel alliterating with any vowel (Russom 1998; Minkova 2003; Terasawa 2011). The Song of the Dragonborn instead uses end rhyme (`vaal/draal`, `gein/krein`, `kein/rein`, `fundein/lein`, `ruz/muz`). Alliterative verse would be a forge addition, not canon.
- **Sound.** Consonant clusters and stressed CVC monosyllables give a Germanic colour, but `z` and `v` (75 of 657 headwords begin with them) are un-Norse: Old English had [v] and [z] only as allophones (Mitchell & Robinson 1982), and neither language had /z/ (Harbert 2007). Inference: the phonology is English-based with exotic letters.

### 2e. Donor strategy by subsystem

| Subsystem | Donor | Borrow | Must not borrow |
|---|---|---|---|
| Syntax | Modern English; Old English as tie-breaker | SVO, prepositions, auxiliary + bare verb, `wo/wen` relatives, `kos` passive; `ni` after an auxiliary and before the verb | obligatory do-support, 's-genitive, verb-second or verb-final clauses, question particles, wh-in-situ |
| Morphology | none (closed set); Afrikaans shows how an invariant-verb Germanic system works (Donaldson 1993) | only canon affixes: plural, possessive suffixes, `-aan`, `vo-`, `-maar` | case, gender, agreement, suffixed article, umlaut, ablaut, dual, double negation |
| Word formation | Old English and Old Norse compounding | two templates: T1 modifier+head (`Dovahkiin`), T2 head-`se`-modifier (`Qethsegol`); kenning = base + determinant in T2 | Norse or English loan roots; new linking elements |
| Phonology | canon only | the 36 attested onsets, 29 codas, 34 runes | `hr- sk- kn- tr- bl- fl- thr-` (unattested), new letters, tone |
| Poetics | Old Norse and Old English | the four wall formulas, bynames, kennings; end rhyme (canon); alliteration as optional ornament | calling alliteration canon; skaldic word-order scrambling |
| Pragmatics | canon formulas, heroic register | title address `thuri`, greeting `Drem Yol Lok`, apology `krosis`, thanks `kogaan`, boast `Zu'u Alduin, zok sahrot do naan ko Lein` | polite second-person pronouns (45A); Kowli (2023) [UNVERIFIED: not in Crossref] reads game conlangs as speech acts, which fits shouts as performatives |

**Worked gaps** (`grammar-gaps.json` did not exist; gaps found from the data).

1. *Content questions.* The dictionary has `wo` "who", `wen` "whose", `kolos` "in which" but no what, where, why, how. Structure from canon and English: wh-word first. Forms: coin one root "what" inside the `w-` series from free CVC shapes (illustration: `*wed`), then derive the rest phrasally from canon prepositions, as English "for what": `fah *wed` "why".
2. *Yes/no questions.* Canon has only particle-less questions: `Ful, losei Dovahkiin?` (fused `losei` "you are") and the elliptical `Boaan tiid vokriiha suleyksejun kruziik?`. Proposed rule: declarative order plus question mark, or fronting of `los/lost/fen/fent/kos`; no `drey` support, no particle.
3. *Numerals.* Only `gein` "one". Borrow structure (decimal, numeral before noun, as `pogaan kiir`), never Norse number words.
4. *Abstract nouns.* `fahdon` "friend" + `-maar` (dictionary: "as suffix: -hood, -self"; `briinahmaar` "sisterhood") gives `*fahdonmaar` "friendship"; Old English `-hād`, `-scipe` arose the same way (Kastovsky 1992).
5. *Poetic synonym.* "Ship" is `veysun`; a kenning on T2 from canon roots is `*keyseokaaz` "horse of the sea", tagged poetic, never replacing the plain word.
6. *Object pronouns.* No entry means "me". Keep `zu'u` invariant (49A = 0); do not import case forms.

## 3. What this means for the app

1. **`typology-profile.json`** (high confidence): one record per parameter `{wals_id, value, evidence_ids[], confidence, locked}`. Lock the high-confidence rows; leave questions, numerals, pronoun case and subject drop `open` for the owner.
2. **Forge validator** (high): each submitted rule declares `{subsystem, wals_ids_affected, donor: canon|internal|eng|oe|on, template, tier}`. Reject automatically if it changes a locked value, uses an unattested onset or coda, or names a donor outside the precedence list in section 1.
3. **Compound engine** (high for templates, medium for productivity): two templates with a mandatory `head` field; juncture check against `medial_consonant_runs`; kennings restricted to T2 and tagged `register: poetic`.
4. **Morphology on the Latin layer** (medium): implement plural and possessive rules on transliteration letters and derive rune spelling afterwards, since `dovahhe` and `meyye` double a letter inside a two-letter rune. Check rune-case spellings first.
5. **Contrastive curriculum** (medium): cross-linguistic similarity supports positive transfer (Ringbom 2007), and typological distance predicts additional-language attainment in a large observational exam study (Schepens et al. 2016). Teach order by exposure; spend explicit instruction and error detection on the seven departures (flag 's, `-s` plurals, tense endings, `dreh ni`, missing possessive suffix).
6. **Formula templates** (high): ship the four wall formulas as slot grammars for the first composition exercises.
7. **Poetics checker** (medium; alliteration is forge-tier): end-rhyme detector on final rune units; optional alliteration detector on word-initial onsets, with all vowels equivalent.
8. **Phrasebook with speech-act tags** (medium): greeting, boast, threat, apology, blessing; one second-person pronoun; address by title.
9. **Drift meter** (medium): keep the matrix and scoring script so the owner can re-score after each rule batch.

## 4. Contested or weak evidence

- Relexification as a theory of creole genesis is disputed (Lefebvre 1998 against DeGraff 2002); I use the term descriptively.
- Gardner (1969) disputes the kenning as a general Germanic device.
- The possessive paradigm: the wiki says `-i` serves all singular persons, yet attested forms (`-i`, `-ii`, `-iil`, `-u`) suggest person distinctions. Unresolved.
- Tau is inflated by literal glossing; glosses are fan readings.
- Novikov (2022), Kowli (2023), Brosch (2024), Goodall (2023) and the Bethesda page were seen only as search summaries; Peterson (2015) was not consulted directly.
- The 68A recoding is mine; under the literal WALS value Dovahzul's `lost` perfect would match no Germanic language.
- Phonological codings rest on spelling.

## 5. Gaps, and what was blocked

- No pronunciation guide or audio: vowel inventory, `th` and `q` values are unknown.
- Polar-question strategy (116A) and subject expression (101A) could not be coded.
- Old English and Old Norse are absent from WALS; Afrikaans is nearly absent.
- thuum.org was not consulted (it refuses automated requests), so existing fan coinages for these gaps were not compared.
- Full texts could not be fetched; scholarly content rests on prior knowledge plus registry verification.
- Reference checker, final run: manual 3, not_found 4, verified 30.

## 6. References

Registry status in brackets where it is not "verified".

- Bauer, L. (2017). *Compounds and Compounding*. Cambridge University Press. doi:10.1017/9781108235679
- Bethesda Game Studios (n.d.). How Bethesda Game Studios made Skyrim's Dragon language. https://elderscrolls.bethesda.net/en-EU/news/how-bethesda-game-studios-made-skyrims-dragon-language [manual]
- Brosch (2024). Warum sind internationale Plansprachen typologisch so, wie sie sind? *Jahrbuch der Gesellschaft für Interlinguistik* 2024. https://media.interlinguistik-gil.de/beihefte/JGI2024/brosch-JGI2024.pdf [not_found; UNVERIFIED]
- Clunies Ross, M. (2005). *A History of Old Norse Poetry and Poetics*. D. S. Brewer. doi:10.1515/9781846154010
- Davis-Secord, J. (2016). *Joinings: Compound Words in Old English Literature*. University of Toronto Press. doi:10.3138/9781442625259
- DeGraff, M. (2002). Relexification: A reevaluation. *Anthropological Linguistics* 44(4), 321-414. [not_found; UNVERIFIED by the registry, confirmed by search]
- Donaldson, B. C. (1993). *A Grammar of Afrikaans*. Mouton de Gruyter. doi:10.1515/9783110863154
- Dryer, M. S. (1992). The Greenbergian word order correlations. *Language* 68(1). doi:10.2307/416370
- Dryer, M. S., & Haspelmath, M. (eds.) (2013). *The World Atlas of Language Structures Online* (v2020.6). https://wals.info [manual]
- Faarlund, J. T. (2007; first published 2004). *The Syntax of Old Norse*. Oxford University Press. doi:10.1093/acprof:oso/9780199235599.001.0001
- Fischer, O., van Kemenade, A., Koopman, W., & van der Wurff, W. (2000). *The Syntax of Early English*. Cambridge University Press. doi:10.1017/CBO9780511612312
- Gardner, T. (1969). The Old English kenning: A characteristic feature of Germanic poetical diction? *Modern Philology* 67(2). doi:10.1086/390147
- Goodall, G. (2023). Constructed languages. *Annual Review of Linguistics* 9. doi:10.1146/annurev-linguistics-030421-064707
- Gower, J. C. (1971). A general coefficient of similarity and some of its properties. *Biometrics* 27(4). doi:10.2307/2528823
- Harbert, W. (2007). *The Germanic Languages*. Cambridge University Press. doi:10.1017/CBO9780511755071
- Holmes, P., & Hinchliffe, I. (2013). *Swedish: A Comprehensive Grammar* (3rd ed.). Routledge. doi:10.4324/9780203381670
- Huddleston, R., & Pullum, G. K. (2002). *The Cambridge Grammar of the English Language*. Cambridge University Press. doi:10.1017/9781316423530
- Kastovsky, D. (1992). Semantics and vocabulary. In R. M. Hogg (ed.), *The Cambridge History of the English Language*, vol. 1. Cambridge University Press. doi:10.1017/CHOL9780521264747.006
- Kowli, G. (2023). Conlangs as speech actions: Studying the pragmatics of constructed languages in video games. *Proceedings of DiGRA Australia 2023*. https://digraa.org/wp-content/uploads/2023/01/2023-CAMERA-READY_Gargi-Kowli.pdf [not_found; UNVERIFIED]
- Lefebvre, C. (1998). *Creole Genesis and the Acquisition of Grammar: The Case of Haitian Creole*. Cambridge University Press. doi:10.1017/CBO9780511519826
- Li, C. N., & Thompson, S. A. (1981). *Mandarin Chinese: A Functional Reference Grammar*. University of California Press. doi:10.1525/9780520352858
- Minkova, D. (2003). *Alliteration and Sound Change in Early English*. Cambridge University Press. doi:10.1017/CBO9780511486968
- Mitchell, B., & Robinson, F. C. (1982). *A Guide to Old English: Revised with Texts and Glossary*. University of Toronto Press. doi:10.3138/9781487586102
- Muysken, P. (1997). Media Lengua. In S. G. Thomason (ed.), *Contact Languages: A Wider Perspective*. John Benjamins. doi:10.1075/cll.17.13muy
- Nguyễn, Đ.-H. (1997). *Vietnamese* (Tiếng Việt không son phấn). John Benjamins. doi:10.1075/loall.9
- Novikov (2022). Constructed languages as semantic and semiotic systems. *RUDN Journal of Language Studies, Semiotics and Semantics* 13(2), 455-467. doi:10.22363/2313-2299-2022-13-2-455-467
- Parkvall, M. (2010). How European is Esperanto? A typological study. *Language Problems and Language Planning* 34(1). doi:10.1075/lplp.34.1.04par
- Peterson, D. J. (2015). *The Art of Language Invention*. Penguin Books. [not_found in Crossref, as is usual for books; existence confirmed by web search and by a registry record of a 2017 review of the book]
- Peterson, D., & Peterson, J. (2024). A methodological proposal for conlang evaluation. *Annual Review of Applied Linguistics*. doi:10.1017/S0267190524000084
- Ringbom, H. (2007). *Cross-linguistic Similarity in Foreign Language Learning*. Multilingual Matters. doi:10.21832/9781853599361
- Russom, G. (1998). *Beowulf and Old Germanic Metre*. Cambridge University Press. doi:10.1017/CBO9780511582981
- Sawyer, B. (2000). *The Viking-Age Rune-Stones: Custom and Commemoration in Early Medieval Scandinavia*. Oxford University Press. doi:10.1093/oso/9780198206439.001.0001
- Schepens, J., van der Slik, F., & van Hout, R. (2016). L1 and L2 distance effects in learning L3 Dutch. *Language Learning* 66(1). doi:10.1111/lang.12150
- Schreyer, C. (2021). Constructed languages. *Annual Review of Anthropology* 50. doi:10.1146/annurev-anthro-101819-110152
- Terasawa, J. (2011). *Old English Metre: An Introduction*. University of Toronto Press. doi:10.3138/9781442693838
- Thráinsson, H. (2007). *The Syntax of Icelandic*. Cambridge University Press. doi:10.1017/CBO9780511619441
- UESP contributors (2026). Lore:Dragon Language (revision 3619598). https://en.uesp.net/wiki/Lore:Dragon_Language [manual]
