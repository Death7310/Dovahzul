# Constitution

The rules about who decides. Accepted by the project owner on 2026-11-22.

## The rules

1. **Game text is the base.** It is always shown as the game wrote it, and no ruling removes anything the game shows.
2. **Every word carries a visible label of where it comes from.** The labels are: game, guide, guide website, source untraced, later game, and coined for this project.
3. **Checks decide what may be proposed. Only the owner ratifies.**
4. **A new word needs a sentence it is used in.** The founding batch is exempt, because nothing can be written without it.
5. **Each ruling is published with its reason,** in numbered releases. `docs/decisions-log.md` is that record.
6. **Grammar rulings stay provisional until they have been through one release in use.** After that they are frozen.
7. **A ratified word never changes its form or meaning.** It can only be retired.
8. **Only the owner can change the rules of the official edition.**

## Not yet written

9. **Succession.** The project will name a second person who can keep it running if the owner cannot. This is to be written before the first release.

## What follows from these rules

- Until the first numbered release, everything decided so far can still be changed, including the words coined for the project.
- After the first release, a ratified word cannot be quietly corrected. It can be retired and another coined, in public, with a reason.
- A standard spelling or pronunciation set by the owner does not alter a game text. The game's own form is shown as written and marked as a variant.

## Where the rules are applied

| Rule | Where |
|---|---|
| 1 | `research/data/spelling.json`: game texts are never altered; rare spellings are marked as variants |
| 2 | `research/data/word-status.json`: the label of every dictionary entry |
| 3, 4 | `research/data/forge-policy.json`: how a new word is made |
| 5 | `docs/decisions-log.md` |
| 6 | `research/data/grammar-rulings.json`: each ruling carries its status |
| 7 | `research/data/forge-words.json`: the words coined so far |
