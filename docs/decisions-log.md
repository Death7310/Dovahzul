# Decisions log

Proposals are put to the project owner one at a time. Each is recorded here with its outcome. "Tap" means the owner accepted the recommendation as written.

## Queue

Items 1 to 15 arise from the Dragon Language Dictionary, Fifth Edition (Thuum.org), which the owner supplied on 2026-11-15. The rest are the decisions still open from section 12 of `docs/design-proposal.md`.

| # | Proposal | Status |
|---|---|---|
| 1 | Where the dictionary is kept, and the public repository (replaces A0) | Decided 2026-11-15 |
| 2 | Re-grade each word's status from the official sources the dictionary cites (replaces A3) | Accepted 2026-11-15 |
| 3 | Words to add that the wiki dictionary lacks | Accepted 2026-11-15 |
| 4 | Words only the wiki has: keep, re-file or mark unconfirmed | Put to the owner 2026-11-15 |
| 5 | Spelling conflicts | Queued |
| 6 | Meanings: official definitions in place of wiki readings | Queued |
| 7 | Word types | Queued |
| 8 | Pronunciation convention | Queued |
| 9 | The apostrophe and the UU rune | Queued |
| 10 | Pronouns | Queued |
| 11 | Possessive endings | Queued |
| 12 | Verb forms | Queued |
| 13 | Articles, plurals and adjectives | Queued |
| 14 | A guard against English-centred gap-filling | Queued |
| 15 | Corrections to the design proposal | Queued |
| 16 on | A1, A2, A4 to A10, then B1 to B7 and C1 to C8 from the design proposal | Queued |

## 1. Where the dictionary is kept, and the public repository

**Facts.** The dictionary states no licence. This repository is public. The design proposal says nothing of Thuum.org's is copied without a written licence, and its administrator is the person the project will be asking for one.

**Done before the answer.** The dictionary was read and compared entry by entry with the wiki data, and only the comparison was stored (`research/data/fifth-edition-reconciliation.json`).

**Options.**

- (a) The owner makes the repository private. The dictionary file and its full parsed contents are then stored in it as a working reference. Nothing of its authors' own writing goes into the app until a licence is granted.
- (b) The repository stays public. The dictionary stays out of it and only checked facts are kept.
- (c) Everything is added to the public repository now. Not advised: it publishes someone else's unlicensed work, against the legal report.

**Recommendation.** (a).

**Outcome, 2026-11-15.** The owner stated that Thuum.org claims no intellectual property over the dictionary and that it is free for anyone to use for any non-commercial purpose, as stated on its website and by its administrator personally. On that basis the dictionary and its parsed contents were added to the repository, with credit and marked for non-commercial use. The basis is recorded in `research/sources/thuum/ATTRIBUTION.md`. Repository visibility was left as it is.

Two things follow. The administrator's own wording is to be added to the attribution file when the owner has it. And the non-commercial condition must be carried into the licence decision (A2), because the open licences recommended there allow selling: Thuum.org's material has to stay in its own files under its own terms, or the project's content licence has to be non-commercial too.

## 2. How each word's standing is graded

**Ruling, accepted 2026-11-15 ("tap").** A word's meaning has one of four grades, by where its official definition comes from:

1. **Game**: the game's own material (developer notes in the game files, in-game books, the Shouts menu).
2. **Guide**: the printed official guide, with no game source.
3. **Guide website**: only the guide publisher's online word list. Official, but marked as resting on a single source.
4. **Unconfirmed**: no official definition found.

Grades 1 to 3 may be used as building parts in the forge. Grade 4 may not until the owner rules on each word. Words from later games keep the wiki's reading and are labelled by game. No cited definition replaces a wiki meaning until the game source has been checked (proposal 6).

**Applied.** `research/data/word-status.json`, built by `tools/reconcile/grade_words.py`: 378 game, 166 guide, 54 guide website, 21 unconfirmed, 26 later game, 12 waiting on proposal 4. This replaces decision A3 of the design proposal.

## 3. Words the dictionary has that the wiki lacks

**Ruling, accepted 2026-11-15 ("tap").** Of the 36 Fifth Edition entries missing from the wiki dictionary:

- 10 compounds and set forms defined in the game's developer notes are added as vocabulary, graded Game, with their parts recorded.
- 2 words from the printed guide are added, graded Guide.
- 6 words found only on the guide's website are added, graded Guide website, with the single-source mark.
- 11 place names go to the list of names, not the vocabulary.
- 4 spelling variants wait for proposal 5, and 3 entries with no printed definition are recorded as forms seen, with no meaning.

**Applied.** `research/data/lexicon-additions.json`, built by `tools/reconcile/build_additions.py`. Each added word was checked against a game text where it occurs; the readings agree, except Vosaraan, noted under proposal 6.

## Evidence notes for the queued proposals

Checked on 2026-11-15 by an independent second parse of the dictionary and by testing its grammar summary against the game texts. These are facts about what the dictionary contains, in this project's own words.

**2. Status.** Of the wiki's 657 entries, 598 have a Fifth Edition heading. For the definition, the Fifth Edition cites: game files, in-game books or the Shouts menu for 378; the printed guide but no game source for 166; only the guide publisher's website for 54. By wiki class: of 392 game-text entries, 321 / 23 / 14, with 34 absent; of 163 guide-only entries, 41 / 115 / 4, with 3 absent; of 91 untraced-list entries, 11 / 25 / 34, with 21 absent. The Fifth Edition treats the printed guide and the guide website as official.

**3. Words to add.** 36 Fifth Edition headings are not wiki dictionary rows. Eleven are names of places (eight from the in-game book Holdings of Jarl Gjalund, plus Alikr, Oblivion and Sovngarde; six are already in the wiki's place list). Ten are compounds or set forms defined in the game's developer notes (Alok-Dilon, Bormahu, Dovahsebrom, Gaaffesejul, Sossedov, Tiid-Ahraan, Ulse, Vomir, Vosaraan, Wuldsetiid). Eight are words from the guide or its website (Rahgron and Suleykaar in the printed guide; Kras, Saan, Sahsun, Sik, Viidost and Vu on the website only). Four are spelling variants of wiki words (Daniik, Krivaan, Tiiraaz, Tovitaan) and belong to proposal 5. Three print no official definition (Dohaviin, Sadonvum, Tu'um).

**4. Wiki-only words.** 59, in six groups.

- Forms of words the project already has, 21: Dezu, Dinokii, Dovahzin, Fenjuntiid, Gronsezin, Juntiid, Nikrent, Sosmir (later games); Briinahii, Duaan, Frini, Junnesejer, Ziil, Zindro (Skyrim and the guide); Funta, Stinselok, Voqostiid, Naaktiid, Pelaan, Fahlah, Qahnaaran (untraced list). Sixteen occur in game text; Juntiid, Naaktiid, Pelaan, Fahlah and Qahnaaran do not occur as spelt.
- Later-game words with a meaning given in game material, 11: Dey, Fey, Jiid, Jol, On, Ron, Roth, Wiix (the in-game book Wisdom of the Flying Gods, The Elder Scrolls Online), and Laar, Miir, Nihnzey, which the wiki cites only to the untraced list but which occur with translations in that book, in a dragon's shout and in a name.
- Later-game words with no recorded meaning, 10: Han, Hof, Jaag, Kohg, Liik, Moh, Nel, Riis, Thaan, Tosh.
- Untraced words with nothing else behind them, 7: Naas, Raal, Um, Unraak, Viint, Vindahlheim, Vos. None occurs in any game text.
- Singles, 4: Au (occurs once in an in-game book, where the line is translated "on"; possibly a misprint of nau), Shor (a god's name), Ros (from a Bethesda article), Vun (cited to the printed guide; the Fifth Edition says the word for voice was once vun and is now zul).
- Spelling variants and errors, 6, for proposal 5: Kriivaan, Tovinaan, Tiiraz, Quethsegol, Nall, Thurri.

**5. Spelling.** Four pairs one letter apart, wiki form first: Kriivaan/Krivaan, Tiiraz/Tiiraaz, Tovinaan/Tovitaan, Daanik/Daniik (the Fifth Edition's own examples under Daniik are spelt daanik). The Fifth Edition also marks as errors: quethsegol (for qethsegol), nall, thurri, hinde, dohaviin, miraad, niid, bahlaan, tu'um, aan in the sense "slave", rok in the sense "word", jun in the sense "light".

**6. Meanings.** Six real differences between a wiki meaning and the cited official definition: Bel, Mindol, Mindoraan, Mindok, Kun, Sov. The copy misprints some definitions (Krah, Krii, Sosaal, Gron, Unslaad, Niid), so no cited definition should replace a wiki meaning without a look at the game source. Kogaan carries the developer gloss "blessings (thankfully)", which bears on "thank you". Vosaraan is defined in the developer notes as "do not wait / do not delay", while the wiki reads the same line as "(your) opposite awaits".

**7. Word types.** A type is printed on nearly every entry under the dictionary's own strong and weak system, which it calls unofficial. Zu'u is printed as a verb in this copy, which is an error.

**8. Pronunciation.** A table of 34 runes with typical values, and a pronunciation on 644 entries. The dictionary calls them recommended, says most words have no recording and that voice actors vary greatly. The table and the entries disagree on e, ei, q and u'u. Entries also use th, sh, ng and a reduced vowel that the table lacks. Stress is given as a tendency: root stressed, endings not.

**9. Apostrophe.** The table gives one rune for "uu or u'u". The dictionary's own headings spell those words with two U runes and an apostrophe. Game inscriptions use the single rune and no apostrophe.

**10. Pronouns.** The summary table makes object equal subject except nust/niin. In game text: zu'u, mu, rok and rek are never objects; hi is an object in Skyrim and a subject once, in Blades; no reflexive use of any pronoun is attested; nimaar occurs once as an emphatic.

**11. Possessive endings.** -i "my" 20 tokens, no counter-example; -ii "his" or "her" 15 tokens, "its" unattested; -iil "your" one token; -u "our" five tokens, one glossed differently by the wiki.

**12. Verbs.** fen plus verb (future) and drey plus verb (past) are well attested. The perfect is made three ways: -aan, lost plus verb, and both together. The -a or -ha infinitive rests on two tokens that do not show the same construction; the four example forms in the summary are unattested.

**13. Articles, plurals, adjectives.** Articles are usually omitted; faal goes with proper names. Plural by doubling the last letter plus e in 14 types, with exceptions (muz, hinde, bruniike) and unchanged plurals. Adjectives stand before the noun about five times as often as after.

**14. English-centred gap-filling.** The introduction gives two reasons for abandoning about 6,000 fan words: the cost of constant revision, and a submission system that "promoted finding missing English translations", with a word-for-word translator, which bred an English-centred approach. It also says the fan vocabulary was built before the language was understood. This bears on the forge's concept list, on English structure as a source, and on reusing the retired fan vocabulary.

**15. Corrections to the design proposal.** The retirement is now confirmed first-hand, with no year given (the text says six years after Skyrim). The dictionary states no licence and gives no contact address. Listening to the game cannot settle most sound values. "No word for thank you" needs qualifying.
