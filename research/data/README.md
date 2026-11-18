# Canon data: what is in this folder

These five JSON files are the project's working record of the dragon language as it stands on the UESP wiki. They were built by script from a snapshot of 331 wiki pages taken on 2026-11-14, and checked against that snapshot the same day. They record what the wiki says; they do not rule on what is canon.

| File | What it is | Size |
|---|---|---|
| `canon-lexicon.json` | The dictionary page `Lore:Dragon Language`: 657 word rows, 29 phrases, 46 dragon names, 6 place names | 580 KB |
| `canon-corpus.json` | 704 dragon-language texts from 208 pages: word walls, songs, dialogue, names, shout phrases, inscriptions | 720 KB |
| `canon-shouts.json` | 67 shouts with their words, rune spelling, meanings and game data | 160 KB |
| `dragon-alphabet.json` | The 34 runes of the script, plus two font-only glyphs, and what the wiki says about the script | 27 KB |
| `corpus-oov.json` | Every corpus token that is not a dictionary headword, with a count, the texts it occurs in and a class | 88 KB |

The raw pages are in `research/sources/uesp/`, one `.wikitext` file per page with a provenance record beside it in `manifest.d/`. The scripts are in `tools/ingest/`.

## How far to trust it

- **The data matches the wiki snapshot.** Every one of the 657 dictionary rows agrees with an independent reading of the raw page, and every unit of text in all 704 corpus records was found on the page the record cites. Details are under "Verification" below.
- **The wiki is a fan site.** The dragon text it quotes comes from the games; most of the English beside it was written by wiki editors. See "Canon, semi-canon, fan" below before treating any gloss as official.
- **Three parsing steps are heuristic** (un-glossed words inside English dialogue, speaker names, name meanings read from prose). Records made that way say so.

## canon-lexicon.json

Built by `tools/ingest/parse_lexicon.py` (version 1.0.1) from `Lore:Dragon Language`, revision 3619598 of 2026-08-24T09:44:44Z.

**Top-level keys**

| Key | Content |
|---|---|
| `meta` | Source page, revision, licence, counts, and `field_notes` explaining every field |
| `entries` | One object per dictionary row |
| `phrases`, `names`, `locations` | The page's Phrases, Names and Locations lists |
| `ref_definitions` | The 38 named reference tags: which source each stands for |
| `unnamed_refs`, `refs_used_but_not_defined` | Two unnamed footnotes; no undefined tags |
| `grammar_wikitext`, `lead_wikitext`, `names_section_wikitext`, `notes_wikitext`, `references_wikitext`, `translation_key_intro_wikitext`, `phrases_intro_wikitext` | Exact slices of the page |
| `unparsed` | Lines the parser could not place: empty |

**An entry**

| Field | Meaning |
|---|---|
| `word` | The headword exactly as written. A row with several spellings keeps them in one string (`"Bahlaan, Balaan"`, `"Kel(le)"`) |
| `word_forms` | The same, cut at commas |
| `definitions` | The glosses, cut at commas and slashes. Empty for the 11 words the page lists without a meaning |
| `definition_text` | The gloss text before cutting |
| `senses` | One object per gloss: its text, part of speech, the separator before it and the reference tags placed after it |
| `pos` | Part of speech, only where the page states one (15 rows) |
| `notes`, `remarks`, `literal`, `see_also` | Bracketed and small-print remarks of the row |
| `refs` | Names of the reference tags on the row. Look each up in `ref_definitions` |
| `section`, `line`, `raw` | Letter heading, line number in the wikitext, and the exact source line |
| `flags` | For example `no_definition_in_source`, `template_vn` |

A phrase has `dovahzul`, `english` (null where the page gives only a literal reading), `literal`, `notes`, `refs`, `raw`. A name has `name`, `meaning`, `parts`, `analyses` (every reading the page lists, with its segmentation where stated), `group` (translated or untranslated), `raw`.

**Counts**

| What | Count |
|---|---|
| Entries | 657: A 26, B 28, D 48, E 7, F 39, G 31, H 28, I 3, J 12, K 63, L 28, M 38, N 43, O 21, P 19, Q 13, R 33, S 49, T 24, U 11, V 51, W 13, Y 5, Z 24. The page has no C or X section |
| Glosses | 725; 61 entries have more than one |
| Entries without a meaning | 11 (Dinokii, Han, Hof, Jaag, Kohg, Liik, Moh, Nel, Riis, Thaan, Tosh) |
| Entries without any reference | 2 (Briinahmaar, Golz) |
| Phrases | 29; five have only a literal reading |
| Names | 46: 41 translated, 5 listed as untranslated |
| Locations | 6 |

## canon-corpus.json

Built by `tools/ingest/parse_corpus.py` from 330 pages. 208 of them yielded corpus records. 17 more are used in another way: for a shout record, for the alphabet, or as a second place where a recorded line stands. The other 105 are listed with a reason each in `meta.pages_fetched_but_nothing_extracted`.

**A record**

| Field | Meaning |
|---|---|
| `id` | Stable within one run: `<kind>-<page or work>-<n>` |
| `type` | `word_wall`, `song`, `dialogue`, `name`, `shout` or `other`; `subtype` narrows it |
| `source_page`, `revid` | The wiki page and the revision the text was read from |
| `location_or_speaker` | Where the text stands or who speaks it |
| `dovahzul` | The dragon-language text in the wiki's spelling. A newline is a line break on the wiki. For dialogue it holds only the dragon-language parts of the line |
| `english` | The translation or gloss on the wiki, or null. The parser never supplies one |
| `notes` | Where the gloss comes from, wiki caveats, `sic` notes |
| `canon_status` | Says where the dragon text comes from. It does not vouch for the English |
| `translation_source`, `gloss_source`, `how_stated` | Where the English comes from |
| `segments` | Dialogue only: aligned pairs of dragon text and gloss, each with the kind of gloss |
| `context` | Dialogue only: the full line as the wiki prints it, English included |
| `duplicate_of`, `also_on` | The same text on another record or another page |
| `uncertain` | The wiki itself hedges (may, might, either) |

Word-wall records also carry `shout`, `teaches_word_index`, `teaches_words`, `teaches_meanings`, `highlighted_dovahzul`, `highlighted_english`, `in_game` and `game`. Records from `Lore:Word Walls` carry `wall_word`, `inscription_column` and, where the page's two columns disagree, `transliteration_column`. `meta.schema` and `meta.conventions` describe the rest.

**Spelling convention.** Word-wall and rune-table text keeps the wiki's rune-case: an upper-case letter is one rune, a lower-case pair (`aa ah ei ey ii ir oo uu ur`) is one two-letter rune, as in `DOVahKiiN`. That casing is data. Lower-case the text to get the usual Latin spelling.

**Counts**

| Type | Records | Notes |
|---|---|---|
| `word_wall` | 131 | 63 from the Skyrim shout pages (57 seen in play, 6 found only in the game files), 60 from `Lore:Word Walls`, 5 from the book *Dragon Language: Myth no More*, 2 from lore pages about places, 1 from the E3 2011 wall. 64 are distinct texts |
| `song` | 6 | The full Song of the Dragonborn, four partial copies of it, and the refrain of "Pray to the Hunter" |
| `dialogue` | 269 | Skyrim 216, ESO 29, Blades 12, Legends 10, 2 untagged. 190 have a wiki gloss, 79 have none |
| `name` | 169 | Dragons, dragon priests, places, terms. 14 are marked uncertain |
| `shout` | 108 | 63 shout phrases, 27 lines from Skyrim Very Special Edition, 18 Legends card lines |
| `other` | 21 | 7 proverbs, 7 word glosses from a Game Informer feature, 5 inscriptions, 1 motto, 1 merchandise text |
| **All** | **704** | 627 have dragon text not marked as a duplicate; 77 carry `duplicate_of` |

By the parser's own count the records hold 4,270 dragon-language tokens, 2,766 of them in non-duplicate records.

**Word walls by game.** Of the 63 inscriptions on shout pages, 50 belong to the base game, 3 to Dawnguard (Drain Vitality) and 10 to Dragonborn (Battle Fury, Bend Will, Cyclone, Dragon Aspect). Shouts taught by a character and not by a wall have no inscription on the wiki: Call Dragon, Call of Valor, Clear Skies, Dragonrend, Soul Tear, Summon Durnehviir.

## canon-shouts.json

Built by `parse_corpus.py` in the same run.

| Key | Content |
|---|---|
| `shouts` | 67 records: `name`, `game`, `availability`, `phrase`, `meaning_phrase`, `words`, `form_id`, `in_game_description`, `locations`, `wiki_summary`, `source_page`, `revid`, `also_attested_in` |
| `shouts[].words` | `position`, `word`, `word_wiki_spelling` (rune-case), `runes`, `meaning`; for Skyrim also `word_id`, `effect`, `recharge_seconds`, `location` |
| `lore_thuum_list` | The 61 shouts named in the list on `Lore:Thu'um`, including those with no known words |
| `player_available_per_Skyrim_Dragon_Shouts` | The 27 shouts the wiki lists as available to the player |

Counts: 67 shouts, 63 with words of power, 136 distinct words. Skyrim 28, Dawnguard 4, Dragonborn 5, ESO 30. The Skyrim records come from the `{{Shout Summary}}` infobox of each shout page; the ESO records from the table on `Online:Dragon`, where the wiki marks some meanings "???".

## dragon-alphabet.json

Built by `parse_corpus.py` in the same run, from `Lore:Dragon Alphabet` and `Template:DragonFont/Doc`.

| Key | Content |
|---|---|
| `runes` | 36 records: `latin`, `kind`, `dragonfont_template_code`, `wiki_spelling_in_transcriptions`, `in_main_alphabet_table`, `order_on_wiki`, `shape_description` |
| `statements` | 13 statements about the script, each with its page and revision |
| `dragonfont_template` | The wiki's font codes: digits 1 to 9 stand for `aa ei ii ah uu ur ir oo ey` |
| `non_language_uses_of_the_script` | Three English sentences written in dragon runes on Legends card packs |

The main table has 34 runes: 25 single letters and 9 two-letter runes (AA AH EI EY II IR OO UU UR). C and "0" exist in the font but not in the language. `shape_description` is null for every rune: the wiki shows the glyphs only through a web font and describes no single shape.

## corpus-oov.json

Built by `tools/ingest/build_oov.py` from the three files above.

| Key | Content |
|---|---|
| `oov` | Tokens that are neither a headword nor explained by a documented rule: `token`, `as_written`, `count`, `count_in_unique_texts`, `texts`, `class`, `basis`, and where they apply `possible_compound_readings`, `reading_by_documented_rule`, `meanings_stated_on_the_wiki`, `one_letter_from_headwords` |
| `explained_by_documented_rules` | Tokens that are not headwords but follow a rule from the dictionary page's Grammar section, with the reading |
| `headwords_not_in_corpus` | Dictionary spellings that never occur as a token of their own |
| `meta` | Method, class definitions, the manual readings and their evidence, counts, caveats |

**Method.** Each record's `dovahzul` is lower-cased and cut into runs of letters; an apostrophe inside a word stays, a hyphen separates tokens. A token is explained if it is a headword's plural (last letter doubled plus `e`), possessive (plus `i`, or `l` after `ii`), "our" form (plus `u`), perfect (plus `aan`), or two to four headwords written together. A cut made only of two-letter headwords is not accepted. Names are kept in the list even when they can be cut into headwords.

**Counts**

| | Distinct tokens | Occurrences |
|---|---|---|
| All | 800 | 4,305 |
| Dictionary headwords | 604 | 3,869 |
| Explained by a documented rule | 39 | 72 |
| Out of vocabulary | 157 | 364 |

| Class of the 157 | Tokens | Examples |
|---|---|---|
| Name | 118 | Dragon and place names from the dictionary page; people named on word walls (Yngnavar, Hrefna) |
| Spelling variant or error | 17 | `thuum` for Thu'um in rune text; `krongah` for Krongrah; `Kfir` for Krif on one page |
| Inflected or derived, pattern not in the Grammar section | 13 | Possessives in `-ii` (`Thu'umii`, `bormahii`); plurals without the doubled letter (`hinde`, `bruniike`) |
| Likely lexicon omission | 5 | `ulse`, `fez`, `nihn`, `vu`, `zey`: the wiki states a meaning somewhere but the dictionary has no row |
| Word of another language | 1 | `Dovah's` |
| Unclassified | 3 | `men`, `mere`, `tuum` |

68 of the 672 dictionary spellings never occur in the corpus as a token of their own. They belong to 67 rows; 40 of those rows cite only the Imperial Library dictionary and 11 only the Prima guide.

The classes are best readings, made by fixed tests in a fixed order plus ten manual readings listed with their evidence in `meta.manual_readings`. They are meant as a work list for the language forge, not as rulings.

## Provenance

All text comes from the UESP wiki, <https://en.uesp.net/>, through its MediaWiki API. 331 pages were saved on 2026-11-14: the dictionary page and 330 others. Their revisions date from 2012-07-01 to 2026-11-13.

The pages behind most of the data:

| Page | Revision | Revision date (UTC) | Corpus records |
|---|---|---|---|
| Lore:Dragon Language | 3619598 | 2026-08-24T09:44:44Z | (the lexicon) |
| Skyrim:Paarthurnax (dragon) | 3560525 | 2026-05-17T20:25:18Z | 76 |
| Lore:Word Walls | 3566106 | 2026-05-28T02:50:57Z | 60 |
| Skyrim:Alduin | 3569192 | 2026-06-01T14:52:05Z | 35 |
| Online:Dragon | 3644261 | 2026-10-01T09:14:19Z | 30 |
| SkyrimVSE:Combat | 3140768 | 2024-09-01T02:42:02Z | 27 |
| Skyrim:Odahviing | 3333464 | 2025-05-19T19:22:31Z | 23 |
| Online:Nahfahlaar | 3506351 | 2026-02-19T19:59:54Z | 20 |
| Skyrim:Dragon | 3664266 | 2026-11-01T23:21:03Z | 17 |
| Blades:Facing the Dragon | 3576870 | 2026-06-16T02:50:56Z | 11 |
| Lore:Dragon Priest Masks | 3601996 | 2026-08-02T04:11:28Z | 11 |
| Lore:Holdings of Jarl Gjalund | 3161853 | 2024-10-10T19:43:22Z | 8 |
| Lore:Wisdom of the Flying Gods | 1973685 | 2019-06-22T20:43:45Z | 7 |
| General:Skyrim’s Dragon Shouts | 3187192 | 2024-11-19T18:45:00Z | 7 |
| Lore:Dragon Language: Myth no More | 1764399 | 2018-04-14T00:25:41Z | 5 |
| Skyrim:Dragon Shouts | 3279131 | 2025-04-13T22:39:18Z | 4 |
| Lore:Dragon Alphabet | 3495681 | 2026-02-03T15:22:40Z | 3 (and the alphabet) |
| Skyrim:Songs of Skyrim | 3487697 | 2026-01-20T18:54:25Z | 1 |
| Lore:Thu'um | 3656838 | 2026-10-20T08:34:25Z | (shout list) |
| Template:DragonFont/Doc | 1369290 | 2014-07-18T04:38:24Z | (font codes) |

The 22 shout pages that carry word-wall inscriptions hold 63 wall records between them.

The full list of 331 pages, with revision id, revision date and links, is in `research/sources/uesp/ATTRIBUTION.md`. The same facts, plus SHA-256 and a revision-pinned API address, are in each page's record under `research/sources/uesp/manifest.d/`. Every corpus record names its page and revision; `meta.source_pages` in `canon-corpus.json` lists all 330 with their hashes.

## Canon, semi-canon, fan

No file labels a fact with one of these three words. The files record where each thing comes from, and the label follows from that. The mapping below is this project's proposal for the owner to confirm, not something the wiki states.

| Label | What falls under it | How to find it in the data |
|---|---|---|
| **Canon** | Dragon-language text from a game or an official publication: dialogue, word walls, shouts, in-game books, banners, the official map | Corpus: `canon_status` beginning "canon". Lexicon: `refs` naming game dialogue, `Shout`, `DBShout`, `SOS`, `DL`, `WOTFG`, `HOJG`, word walls, ESO dragons |
| **Semi-canon** | Official in origin but not game text, or never shown in play: the Prima Official Game Guide word list, the "Official Bethesda Dragon dictionary" hosted at The Imperial Library, developer statements in the press, game-file-only word walls, merchandise and promotional songs | Lexicon: `refs` of only `Prima`, `TIL`, `BN`, `DBgamedata`. Corpus: `in_game: false`, `canon_status` naming press, merchandise or promotion |
| **Fan** | English written by wiki editors: hover glosses on dialogue, name analyses, and word-wall translations for which the wiki names no source | Corpus: `gloss_source: "wiki hover gloss"`, `how_stated`, `translation_source: "translation as given on the wiki page"` |

Where the Prima guide belongs is a judgement call. It is a licensed official publication, which by the project's own rule makes it a primary source; it is put under semi-canon here because 163 words rest on it alone.

What this means for the lexicon's 657 entries:

| Sourcing | Entries |
|---|---|
| At least one reference to game dialogue, a shout, a word wall, an in-game book or the official map | 392 |
| Game data only (`DBgamedata`) | 6 |
| Only the Prima guide (163), the Prima guide with the Imperial Library dictionary (2), or a Bethesda article (1) | 166 |
| Only the Imperial Library dictionary | 91 |
| No reference on the page | 2 |

As far as the wiki states its sources, the English in the corpus is from the game or book itself only in four places: *Songs of Skyrim*, *Dragon Language: Myth no More*, *Wisdom of the Flying Gods* (whose in-book author calls his reading imperfect) and Arngeir's rendering of the Greybeards' chant. Everything else in `english` is the wiki's.

The word "Dovahzul" itself occurs in the 331 pages only once, in a fan's question in an ESO developer Q&A of 3 June 2019 (`General:Elsweyr & Update 22 AUA`); the developer's reply speaks of "Dov words". Within this snapshot it is a fan term. The dictionary page calls the language "Dragon Language", "Dragon tongue" or "Draconic language" and cites in-game dialogue and an ESO book for those names.

## Licence and attribution

The wiki's content is under the **Creative Commons Attribution-ShareAlike 2.5 License** (<http://creativecommons.org/licenses/by-sa/2.5/>). The wiki's API reports that licence, and its policy page `UESPWiki:Copyright and Ownership` (revision 3529700) sets three conditions for reuse:

1. Material built from it must be licensed under the same by-sa licence.
2. The article the content came from must be credited.
3. Readers must be given access to that article; the policy says a link to the article and to its history page does this.

What follows for this folder (an inference from those terms, for the owner to confirm):

- These JSON files reproduce wiki text, so they are adaptations and fall under condition 1.
- Any release that includes them needs a notice naming UESP, the licence and the source articles. A suggested wording and the full article list are in `research/sources/uesp/ATTRIBUTION.md`.
- The wiki's licence covers what its editors wrote. The dragon-language text itself is quoted from Bethesda Softworks and ZeniMax games; the wiki cannot license that. Whether the app may redistribute it is a separate question.

## Verification

An independent check was run on 2026-11-14. It had three parts: a script that shares no code with the parsers (`tools/ingest/verify_counts.py`, 23 checks, repeatable), three random samples, and a by-eye review of every record made by a heuristic step. The samples and the by-eye reviews were done once and are not part of the script.

**Random samples (each field compared with the raw wikitext)**

| Sample | Records | With an error |
|---|---|---|
| Lexicon entries, before any fix | 40 | 0 |
| Corpus texts, before any fix | 20 | 0 |
| Corpus texts, after the fixes | 20 | 0 |

A sample of 20 with no errors only shows the error rate is probably below about 15%. The checks below covered every record of each kind and found what the samples could not. The rows on un-glossed words and on names are by-eye reviews; the rest are script checks.

**Checks over every record**

| Check | Result before | After the fixes |
|---|---|---|
| Dictionary rows per letter, raw against JSON | 657 = 657, every letter equal | same |
| Headword, source line, reference tags and gloss text of every row | 657 of 657 agree | same |
| Phrases, names, locations | 29, 46, 6: counts equal; one phrase kept quotation marks in `english` | fixed |
| Word-wall inscriptions on shout pages | 63 of 63 present, text and translation identical | same |
| Inscriptions on `Lore:Word Walls` | 60 of 60 present; 2 records held the wrong one of the page's two columns | fixed |
| Hover glosses on dragon-language phrases, all pages | 322 on the pages; 321 are in the corpus with the same gloss, 1 with another page's wording of it, none absent | same |
| Un-glossed dragon words found by word list | 5 of 87 records cut a phrase short or missed a word | fixed |
| Name records | 2 of 169 wrong (`Dovah's Du'ul Style`, `Jun` as "Aether") | fixed |
| Shout words against the infoboxes; ESO shout table | 87 words on 30 pages and 40 table rows: no difference | same |
| Runes and font codes | 36 of 36 | same |
| Every text unit of every record found on its cited page | 2,569 of 2,569 | 2,588 of 2,588 |

Known wrong records before: 10 of 702 in the corpus (1.4%) and 1 of 738 in the lexicon (0.1%). After: none known in 704 and 738.

**What was changed**

- `parse_corpus.py`: on `Lore:Word Walls`, where the rune column and the Latin column disagree (walls "Diin" and "Zul, Mey, Gut"), the record now takes the column that the shout page and the translation confirm. Six hand-checked words or phrases are accepted on their pages so that five dialogue records are complete. Two name records were corrected. The game's own placeholders such as `<man/woman>` are kept in the English context.
- `parse_lexicon.py`: a phrase with several quoted renderings now has them in `english` without quotation marks.
- `fetch_corpus.py`: two pages added (`Lore:Vundeheim`, `Lore:Korvag Crag`), each quoting a word wall that was already recorded.

## Known limitations

**Coverage**

- The page list came from links, categories and word searches. By the fetch run's own account about 1,040 further titles turned up in discovery and were judged from titles and search snippets, not opened. A dialogue line using only words that no search term matched could be missing.
- A follow-up search on 2026-11-14 found dragon text on pages outside the snapshot only as repeats of lines already recorded (for example `Online:Ra'khajin`, `Online:Caska`, `Online:Aeliah Renmus`, `Online:Moon-Bishop Azin-jo`, `SkyrimVSE:Quests`, `SkyrimVSE:Dungeons`, `Lore:Necromancy`).
- The snapshot holds dragon-language lyrics for one song only, the Song of the Dragonborn (plus the short refrain of "Pray to the Hunter"). The words "Sovngarde Song" occur on none of the 331 pages.
- Nine titles linked from the dictionary page do not exist on the wiki (confirmed through the API on 2026-11-14); they are listed in the corpus `meta`. `Lore:Ma-Tylda`, a dragon name the dictionary page lists as untranslated, redirects to an entry on `Lore:Gods M`, which is not in the snapshot.

**The wiki's own inconsistencies, recorded and not resolved**

- Whirlwind Sprint wall 1 reads "angry Orcs" on the shout page and "gods-bind Orcs" on `Lore:Word Walls`.
- The Dragonstone inscription ends "Alduin revives" on one page and "ALDUIN restore" on another.
- `Lore:Kruziikrel` gives the name as "Dominate-Enlightenment", the meaning of Relonikiv; `Skyrim:Kruziikrel` and the dictionary page give "Ancient Domination".
- *Myth no More* passage 1 prints "moron au" where the wall has MORO NAU.
- `Skyrim:Throw Voice` notes that the first word may be Vun, not Zul.
- The dictionary page has Qethsegol and Quethsegol, Miraad beside Miiraad, and Pahklok beside Pahlok.

**How records are built**

- Where the same dragon text stands on several pages one record is kept. A second gloss or a second English context for it is then lost: "Ceaseless enemy!" for *Unslaad hokoron!* on `Skyrim:Alduin` is not recorded beside "Unending enemy!".
- A dialogue record's `english` joins its segments line by line and writes `[no gloss on the wiki]` for a segment without one (18 records). Use `segments` for aligned pairs.
- Five name records hold a segmentation in `dovahzul`, for example `Mirmulnir (Mir Mul Nir)`.
- Some `english` values are assembled by the parser from the wiki's wording: alternatives joined with " | ", and `Yol (Fire) + Toor (Inferno)`.
- Word-wall records from shout pages list all of the shout's locations. The wiki says the text a wall shows depends on how many words of the shout you already know, not on which wall you visit; it names Throw Voice and Unrelenting Force as the exceptions.
- The wiki's footnotes are not carried into corpus records. The page and revision are, so a footnote can be looked up.
- The lexicon cuts glosses at commas and slashes and attaches a reference tag to the gloss it follows. Whether a tag also covers the glosses before it is not stated on the page; `refs_following` records the guess.

**Not in the data at all**

- Rune shapes. The wiki has none; the glyphs would have to come from another source.
- Pronunciation. The pages give no sound values for runes or words. The only remarks on sound in the snapshot are a note on `Skyrim:Vuljotnaak` about the letter j and the note on `Skyrim:Throw Voice` mentioned above; neither is in the data files.
- Anything from thuum.org, which was not used.

## How to regenerate

Run everything from the repository root. All scripts use only the Python standard library.

```
# 1. Fetch (network; talks only to https://en.uesp.net/w/api.php)
python3 tools/ingest/fetch_lexicon.py --revid 3619598
python3 tools/ingest/fetch_corpus.py

# 2. Parse (offline)
python3 tools/ingest/parse_lexicon.py
python3 tools/ingest/parse_corpus.py
python3 tools/ingest/build_oov.py

# 3. Check, and refresh the page table in ATTRIBUTION.md
python3 tools/ingest/verify_counts.py
python3 tools/ingest/list_sources.py
```

Things to know:

- Step 1 is not needed to rebuild the JSON: the snapshot is already in `research/sources/uesp/`. `fetch_corpus.py` skips pages it already has.
- `fetch_lexicon.py --revid 3619598` returns exactly the dictionary text used here. `fetch_corpus.py --force` fetches the current revision of every page, which will differ from this snapshot. To get an old revision back, use the `api_url` in that page's record under `manifest.d/`.
- Order matters. `parse_corpus.py` reads the dictionary wikitext as a word list, and `build_oov.py` reads the other JSON files.
- `canon-lexicon.json` and `corpus-oov.json` come out byte for byte the same on every run. The three files written by `parse_corpus.py` carry a `generated_at` timestamp and are otherwise stable.
- `verify_counts.py` writes nothing and exits with status 1 if a check fails. `parse_lexicon.py` refuses to write if its own checks fail.
- To add a page: put its title in the `PAGES` list in `fetch_corpus.py`, run that script, then steps 2 and 3. If the parser has no rule for the page it is listed under `pages_fetched_but_nothing_extracted` with a reason.

## fifth-edition.json

The parsed contents of the *Dragon Language Dictionary, Fifth Edition* published by Thuum.org: one record per entry with the heading, rune spelling, word type, pronunciations, the official definition and the sources cited for it, and the entry's other sections (expanded definition, usage, connotations, etymology, notes, see also) as printed. The source file and the terms of use are in `research/sources/thuum/`: non-commercial use, with credit to Thuum.org.

By the dictionary's own statement, only the official definition and the usage quotations come from official sources. Everything else is its authors' analysis.

Limits: the copy is a PDF converted to Word, so columns are sometimes interleaved and a section can carry stray words from a neighbouring entry. It holds 646 entries; its introduction says 647. Word type is blank for 26 entries. Thirteen entries with a known misprint or doubt carry a `doubt` field. Section text was not proofread.

## fifth-edition-reconciliation.json

An entry-by-entry comparison of `canon-lexicon.json` with `fifth-edition.json`.

What the file holds:

- `wiki_entries`: one row per wiki entry, with the wiki's source class, whether the Fifth Edition has the word, and the kind of official source the Fifth Edition cites for its definition (developer notes in the game's dialogue file, an in-game book, the Shouts menu, the printed official guide, or the guide publisher's online word list).
- `only_in_fifth_edition`: its headings that the wiki dictionary lacks, with the same source kinds.
- `likely_spelling_variants`: pairs one letter apart.
- `review_notes`: points found by an independent check.
- `meta.counts` and `meta.wiki_class_by_fifth_edition_source`: the totals.

Source kinds were read by pattern; an independent second parser agreed on all of them after seven were corrected.

To regenerate, see the headers of `tools/reconcile/parse_fifth_edition.py` and `tools/reconcile/compare_fifth_edition.py`.

## word-status.json

The standing of each wiki dictionary entry's meaning under the ruling recorded as proposal 2 in `docs/decisions-log.md`. Each row gives the word, where the wiki says the word itself occurs, whether the Fifth Edition has it, the grade of its meaning (`game`, `guide`, `guide_website`, `unconfirmed`, `later_game`, or none while a ruling is pending), whether it rests on a single source, and whether it may be used as a building part in the forge. Built by `tools/reconcile/grade_words.py`; `meta.counts` has the totals.

## lexicon-additions.json

Words added to the project from the Fifth Edition under the ruling recorded as proposal 3 in `docs/decisions-log.md`: 18 vocabulary entries with their meaning, grade, the sources the Fifth Edition cites, how many game texts they occur in and, for compounds, their parts; 11 place names; and 3 forms the Fifth Edition lists with no definition. Built by `tools/reconcile/build_additions.py`. Credit for the compilation goes to Thuum.org; non-commercial use.

## spelling.json

Standard spellings and their recorded variants under the ruling recorded as proposal 5 in `docs/decisions-log.md`: the rule, eleven words with their standard form, the basis for it, each variant with where it comes from and how often each occurs in game text, one unexplained form, and eight further cases the Fifth Edition reports that are still to be checked. Built by `tools/reconcile/build_spelling.py`.

## meanings.json

The meaning of record for each wiki dictionary entry under the ruling recorded as proposal 6 in `docs/decisions-log.md`. Each row gives the meaning the project uses, the kind of source it rests on, the wiki's wording where it differs, any further senses with a label, which part of the rule applied, and whether the cited source has been or can be checked. Built by `tools/reconcile/build_meanings.py`. Official definitions are quoted as compiled by Thuum.org (non-commercial use, with credit); wiki wordings are from UESP.

## word-types.json

The project's word types under the ruling recorded as proposal 7 in `docs/decisions-log.md`: for each Fifth Edition entry, its class, whether it can also serve as a noun, the roles the dictionary lists for it, and the roles the project allows (by the owner's ruling, every role the system permits). The classification is Thuum.org's, used with credit for non-commercial purposes. Twenty-one words the dictionary does not cover are listed as having no type yet. Built by `tools/reconcile/build_word_types.py`.

## pronunciation.json

The project's reading convention under the ruling recorded as proposal 8 in `docs/decisions-log.md`: for each Fifth Edition entry the pronunciation taught, the others accepted, and an empty `heard_in_game` list for listening reports; and `rule_for_new_words`, a table giving each spelling unit the sound the dictionary most often gives it in stressed and unstressed syllables, with a cross-validated measure of how often the rule reproduces the dictionary's own pronunciations and the result of the stress rules tried. The pronunciations are Thuum.org's, used with credit for non-commercial purposes; the dictionary calls them recommended, not official. Built by `tools/analysis/pronunciation_rule.py`.

## grammar-rulings.json

The owner's rulings on the open areas of grammar listed in `grammar-gaps.json`, one entry per area, each with its rules, the forms it covers, how often each use occurs in game text, which uses are the project's convention, and its status (provisional until one release in use). `docs/decisions-log.md` holds the owner's words and the evidence.

## forge-words.json

Words coined for this project and ratified by the owner. Each entry gives the word, its meaning and class, what it was built from, who coined it and when, the checks it passed (not an existing word, not in any game text, nothing one letter away, an attested sound pattern), how it is said and how it is written in runes. Everything here is invented and is labelled so in the app.
