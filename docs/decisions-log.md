# Decisions log

Proposals are put to the project owner one at a time. Each is recorded here with its outcome. "Tap" means the owner accepted the recommendation as written.

## Queue

Items 1 to 15 arise from the Dragon Language Dictionary, Fifth Edition (Thuum.org), which the owner supplied on 2026-11-15. The rest are the decisions still open from section 12 of `docs/design-proposal.md`.

| # | Proposal | Status |
|---|---|---|
| 1 | Where the dictionary is kept, and the public repository (replaces A0) | Put to the owner 2026-11-15 |
| 2 | Re-grade each word's status from the official sources the dictionary cites (replaces A3) | Queued |
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

**Done already, whatever the answer.** The dictionary was read and compared entry by entry with the wiki data. Only facts were stored: which words each source lists, what kind of official source the dictionary cites for each definition, and likely spelling variants (`research/data/fifth-edition-reconciliation.json`). The file itself and everything its authors wrote stayed out of the repository.

**Options.**

- (a) The owner makes the repository private. The dictionary file and its full parsed contents are then stored in it as a working reference. Nothing of its authors' own writing goes into the app until a licence is granted.
- (b) The repository stays public. The dictionary stays out of it and only checked facts are kept.
- (c) Everything is added to the public repository now. Not advised: it publishes someone else's unlicensed work, against the legal report.

**Recommendation.** (a).

**Outcome.** Pending.
