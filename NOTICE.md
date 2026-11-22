# Notice: what terms cover what

**Unofficial fan project.** Not affiliated with, endorsed or sponsored by Bethesda Softworks, ZeniMax Media or Microsoft. The Elder Scrolls and Skyrim are trademarks of ZeniMax Media Inc. Dragon-language text from the games belongs to its owners. It is quoted here for study and commentary, and no licence in it is claimed or granted.

The project owner chose these terms on 2026-11-22 (see `docs/decisions-log.md`). This is not legal advice.

## The project's own work

| What | Where | Terms |
|---|---|---|
| Program code | `tools/` | GNU General Public License, version 3 or later (`LICENSES/GPL-3.0-or-later.txt`) |
| The project's writing: design, rulings, research reports, reference lists | `docs/`, `research/*.md`, `research/refs/` | Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (`LICENSES/CC-BY-NC-SA-4.0.txt`) |
| The project's rulings and coined words as data | `research/data/grammar-rulings.json`, `forge-words.json`, `forge-policy.json`, `spelling.json`, `grammar-gaps.json` | Creative Commons Attribution-NonCommercial-ShareAlike 4.0 |
| The font | not yet made | SIL Open Font License 1.1, with the font's name reserved |

In plain words, for the writing, rulings and coined words: anyone may copy, share and adapt them for free, must give credit, must pass on the same terms, and may not sell them.

## Material from other sources

| Source | Where | Terms |
|---|---|---|
| The Unofficial Elder Scrolls Pages (UESP) | `research/sources/uesp/`; and built from it: `research/data/canon-lexicon.json`, `canon-corpus.json`, `canon-shouts.json`, `dragon-alphabet.json`, `corpus-oov.json`, `canon-phonotactics.json`, `core-concept-gaps.json` | Creative Commons Attribution-ShareAlike 2.5 (`LICENSES/CC-BY-SA-2.5.txt`). Credit and page revisions are in `research/sources/uesp/ATTRIBUTION.md`. This covers what the wiki's editors wrote, not the game text they quote |
| Thuum.org, *Dragon Language Dictionary, Fifth Edition* | `research/sources/thuum/`; and built from it: `research/data/fifth-edition.json`, `word-types.json`, `lexicon-additions.json`, and the pronunciations in `pronunciation.json` | Non-commercial use only, with credit to Thuum.org. The basis is set out in `research/sources/thuum/ATTRIBUTION.md` |

## Files that draw on more than one source

| File | What comes from where |
|---|---|
| `research/data/meanings.json` | Official definitions as compiled and cited by Thuum.org (non-commercial, with credit). The field `wiki_wording` is from UESP (share-alike 2.5). The rulings recorded in it are the project's |
| `research/data/pronunciation.json` | The per-word pronunciations are Thuum.org's (non-commercial, with credit). The rule for new words and its test results are the project's |
| `research/data/word-status.json`, `fifth-edition-reconciliation.json` | Facts about which source lists and defines each word, drawn from both sources; the arrangement is the project's |

When the app is built, each kind of material goes into its own data pack, so that each keeps its own terms.

## Removal

To ask for material to be removed, open an issue on this repository. Requests will be answered promptly.
