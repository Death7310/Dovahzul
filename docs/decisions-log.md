# Decisions log

Proposals are put to the project owner one at a time. Each is recorded here with its outcome. "Tap" means the owner accepted the recommendation as written.

## Queue

Items 1 to 15 arise from the Dragon Language Dictionary, Fifth Edition (Thuum.org), which the owner supplied on 2026-11-15. The rest are the decisions still open from section 12 of `docs/design-proposal.md`.

| # | Proposal | Status |
|---|---|---|
| 1 | Where the dictionary is kept, and the public repository (replaces A0) | Decided 2026-11-15 |
| 2 | Re-grade each word's status from the official sources the dictionary cites (replaces A3) | Put to the owner 2026-11-15 |
| 3 | Words to add that the wiki dictionary lacks | Queued |
| 4 | Words only the wiki has: keep, re-file or mark unconfirmed | Queued |
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

## Evidence notes for the queued proposals

Checked on 2026-11-15 by an independent second parse of the dictionary and by testing its grammar summary against the game texts. These are facts about what the dictionary contains, in this project's own words.

**2. Status.** Of the wiki's 657 entries, 598 have a Fifth Edition heading. For the definition, the Fifth Edition cites: game files, in-game books or the Shouts menu for 378; the printed guide but no game source for 166; only the guide publisher's website for 54. By wiki class: of 392 game-text entries, 321 / 23 / 14, with 34 absent; of 163 guide-only entries, 41 / 115 / 4, with 3 absent; of 91 untraced-list entries, 11 / 25 / 34, with 21 absent. The Fifth Edition treats the printed guide and the guide website as official.

**3. Words to add.** 36 Fifth Edition headings are not wiki dictionary rows. Seven are on the wiki page in other lists (six place names, one phrase). The rest are compounds and forms defined in developer notes, words from the guide or its website, and four entries with no official definition.

**4. Wiki-only words.** 59. By wiki source: 21 untraced list, 17 The Elder Scrolls Online, 8 the book Wisdom of the Flying Gods, 1 Blades, 8 Skyrim, 3 printed guide, 1 Bethesda article. Eight occur in the Fifth Edition as inflected or compound forms under another heading; it gives headings to base words only. About 23 can be split into a Fifth Edition heading plus an ending or another heading.

**5. Spelling.** Three pairs one letter apart: Kriivaan/Krivaan, Tiiraz/Tiiraaz, Tovinaan/Tovitaan. The Fifth Edition also marks as errors: quethsegol (for qethsegol), nall, thurri, hinde, dohaviin, miraad, niid, bahlaan, tu'um, aan in the sense "slave", rok in the sense "word", jun in the sense "light".

**6. Meanings.** Six real differences between a wiki meaning and the cited official definition: Bel, Mindol, Mindoraan, Mindok, Kun, Sov. The copy misprints some definitions (Krah, Krii, Sosaal, Gron, Unslaad, Niid), so no cited definition should replace a wiki meaning without a look at the game source. Kogaan carries the developer gloss "blessings (thankfully)", which bears on "thank you".

**7. Word types.** A type is printed on nearly every entry under the dictionary's own strong and weak system, which it calls unofficial. Zu'u is printed as a verb in this copy, which is an error.

**8. Pronunciation.** A table of 34 runes with typical values, and a pronunciation on 644 entries. The dictionary calls them recommended, says most words have no recording and that voice actors vary greatly. The table and the entries disagree on e, ei, q and u'u. Entries also use th, sh, ng and a reduced vowel that the table lacks. Stress is given as a tendency: root stressed, endings not.

**9. Apostrophe.** The table gives one rune for "uu or u'u". The dictionary's own headings spell those words with two U runes and an apostrophe. Game inscriptions use the single rune and no apostrophe.

**10. Pronouns.** The summary table makes object equal subject except nust/niin. In game text: zu'u, mu, rok and rek are never objects; hi is an object in Skyrim and a subject once, in Blades; no reflexive use of any pronoun is attested; nimaar occurs once as an emphatic.

**11. Possessive endings.** -i "my" 20 tokens, no counter-example; -ii "his" or "her" 15 tokens, "its" unattested; -iil "your" one token; -u "our" five tokens, one glossed differently by the wiki.

**12. Verbs.** fen plus verb (future) and drey plus verb (past) are well attested. The perfect is made three ways: -aan, lost plus verb, and both together. The -a or -ha infinitive rests on two tokens that do not show the same construction; the four example forms in the summary are unattested.

**13. Articles, plurals, adjectives.** Articles are usually omitted; faal goes with proper names. Plural by doubling the last letter plus e in 14 types, with exceptions (muz, hinde, bruniike) and unchanged plurals. Adjectives stand before the noun about five times as often as after.

**14. English-centred gap-filling.** The introduction gives two reasons for abandoning about 6,000 fan words: the cost of constant revision, and a submission system that "promoted finding missing English translations", with a word-for-word translator, which bred an English-centred approach. It also says the fan vocabulary was built before the language was understood. This bears on the forge's concept list, on English structure as a source, and on reusing the retired fan vocabulary.

**15. Corrections to the design proposal.** The retirement is now confirmed first-hand, with no year given (the text says six years after Skyrim). The dictionary states no licence and gives no contact address. Listening to the game cannot settle most sound values. "No word for thank you" needs qualifying.
