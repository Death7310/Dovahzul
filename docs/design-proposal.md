# Design proposal: a teaching app and language forge for the dragon language

**Status:** second draft, revised after the owner's rulings. Partly decided: log items 1 to 14 and 16 to 19 are ruled; the rest are open. `docs/decisions-log.md` records each ruling with the owner's words and the evidence ("log item 6" below means entry 6 there). No app code has been written.
**Date:** 2026-11-23.
**Evidence:** the fifteen reports in `research/` and the data in `research/data/`.
**Review:** four independent reviewers checked the first draft and two more the second; their corrections are in. This revision changes what the rulings and the Thuum.org dictionary changed. Section 13 says what is still unverified.

The project's name is *Zu'u Tinvaak Dovah*, "I speak dragon" (log item 19). "Dovahzul" is a fan name; official text says "Dragon Language", and this document says "the dragon language". "The Fifth Edition" is Thuum.org's current dictionary, which the owner supplied on 2026-11-15.

---

## 0. The short version

**What I propose.** One free app with four parts: a course, a reading library, a word forge, and a reference (dictionary, grammar, rune converter). Everything runs on the device with no connection and no live AI.

**What you would get first.** A reader and reference for what the games already contain: dictionary, rune chart and converter, and the word walls with every word explained. It needs no further rulings on the words; only the converter waits on the rune spelling rules (section 4.5).

**The four things you most need to know.**

1. **The language has to be finished before it can be taught to conversation.** The games contain about 650 words and a few thousand words of text, with no word for *if, because* or *two*. Five question words have now been coined and ratified. The forge is the main line of work, and your rulings come before most lessons.
2. **Thuum.org tried open fan expansion and gave it up; this is now confirmed first-hand.** The introduction of its Fifth Edition says the community abandoned about 6,000 fan words, for two causes: the cost of constant revision, and a submission system built around finding missing English translations, with a word-for-word translator. It gives no year. That dictionary is now included here, with credit, for non-commercial use (section 9). The history supports strict checks, never revising an accepted word, and starting from a sentence instead of a list of English words.
3. **Standalone programs for Mac, Windows and Android are the end goal** (decided; log item 18). A web app, which installs from a web page on first visit and then runs offline, may come first as a step. What to spend on the programs, and the permanent address, are still open (sections 8 and 12).
4. **The work is large and rests on you.** Before any ruling I estimated 60 to 150 hours of your time for rulings and review, and I have not re-estimated since. The content to be written is about twenty times the size of everything in the games.

**Decided and open.** Decided: the standing, meaning, spelling, type and pronunciation of the words; ten areas of grammar; the rules for making new words; the constitution; the licences; standalone programs as the end goal. Until the first numbered release, everything decided so far can still be changed (log item 16). Still open (section 12): the permanent address, names, the game texts pack, where invented words appear, a lawyer's review, the order of sources where the game is silent, a set of reversible defaults, some tasks only you can do, and further rulings on the language itself.

---

## 1. What the research found

**1. The makers built a game device, not a full language, and said so.** The designer told the press in 2011: "you're not developing it as an actual language. It's much more word based." Anything beyond the individual words found in the games is this project's design, not recovery of something hidden. (Report 02.)

**2. The game material is small.** The wiki dictionary has 657 entries; the Fifth Edition has 646 in the copy supplied (its introduction says 647); 598 are in both. Connected text (word walls, dialogue, songs) comes to between 2,200 and 2,600 words, with 700 to 750 distinct word forms, about half of which occur once. There are 64 distinct word-wall inscriptions. (Data files.)

**3. Every word's standing is graded by where its definition comes from** (decided; log items 2, 4, 5 and 14). The 657 wiki entries:

| Grade | Entries | What it means |
|---|---|---|
| Game | 390 | Defined in the game's own material: developer notes in the game files, in-game books, the Shouts menu |
| Guide | 168 | Defined in the printed official guide, with no game source |
| Guide website | 54 | Defined only in the guide publisher's online word list; official, but a single source |
| Source untraced | 7 | From a word list whose origin could not be traced; kept and usable, with that label |
| Reserved | 10 | A later-game word with no recorded meaning; never given one, and its spelling not reused |
| Recorded form, Variant, Name | 21, 6, 1 | A form or a spelling variant of another word, or a proper name; not separate words |

618 of the 657 may be used as building parts for new words. A further 21 words were added from the Fifth Edition. Of the 91 words the earlier draft called untraced, 73 now have an official source, 11 proved to be forms or variants of other words, and 7 remain untraced.

**The meaning of record is settled too** (log item 6): the official definition from the best source (the game's own material, then the printed guide, then the guide website), with the wiki's wording kept as a note. Where two games give a word different senses, both are kept, each labelled with its game. Thuum.org's commentary is shown as commentary, credited, never as the meaning of record. For 570 entries the sources agree; 14 took the official wording; seven were ruled one by one; six are misprinted in the dictionary copy, so the wiki reading stands for now. Example: *bel* is "summon"; its older meaning "foul" stays as a second, labelled sense, because you ruled that things created by the community can be kept.

**Word types exist** for all 646 Fifth Edition entries, credited to Thuum.org (log item 7). Twenty-one words it does not cover have none yet.

**4. About half of everyday vocabulary was missing, and most of that still is.** Against three standard lists of basic concepts the wiki dictionary covers 47 to 51 percent; counting only words that occur in game text, 32 to 46 percent. These figures predate the rulings. (Report 06. The concept lists were typed from memory and must be checked against the published lists.) Three corrections:

- *What, where, when, why, how* are coined and ratified: *waar, wil, wuz, wul, wed*, each the game's own answer word with *w* in front (*daar* "this" gives *waar* "what"), beside the game's *wo* "who" (log item 11b).
- "No word for *thank you*" was too strong. The official definition of *kogaan* is "Blessing"; the Fifth Edition's usage section quotes a developer's note on a line of the dragon Paarthurnax: blessings ("thankfully"). A set phrase for thanks is not yet ruled.
- *Me* is not missing: *zu'u* is both "I" and "me" (log item 10).

Still missing: *if, because*, the numbers from two up, and most body parts and basic verbs.

**5. Grammar had 34 undecided areas; about half are now ruled in whole or in part.** Ten grammar rulings are recorded (log items 10 to 13; section 12 gives each in one line, the log in full): pronouns; how a question is formed; the possessive endings; the other rules of possession; verbs and time, with "is"; articles; the plural; where a describing word goes; "not"; and commands. Other rulings settle six more areas: sound values, the apostrophe, spelling variants, which meaning counts, the standing of guide and untraced words, and word types.

Of the seven areas that blocked teaching outright, five are ruled (sound values, pronouns, possession, tense, questions) and two remain (numbers, core vocabulary). Also open, roughly: "can, must, should" and "if"; comparison; linking words; prepositions; longer clauses; word-building and compound order; rare sound patterns; set phrases; time and dates; rune spelling rules; shouts and names. Every grammar ruling is provisional until it has been in use for one release. (Reports 01, 15; `research/data/grammar-gaps.json`.)

**6. The most similar natural language, of ten compared, is modern English.** On 30 grammatical features it scores 0.82 (1.0 would be identical); Old Norse scores 0.62. Old Norse and Old English supplied the *style*: memorial inscriptions, compound names, a heroic tone. (Report 05; approximate figures.)

**7. Where it differs from English, it does so by leaving things out, and not consistently.** Tense is optional; articles and plural endings are usually omitted; "is" is often dropped; possession is marked by an ending on the noun (*thuri*, "my overlord") 41 times in game text and by a separate word (*dii*, "my") 61 times. The rulings so far keep this freedom. (Reports 01, 05; log items 11 to 13.)

**8. There is no official pronunciation, and the project still has no drawings of the runes.** Every published sound value is a fan convention; the project has adopted Thuum.org's and labels it as one (section 7). The data holds the 34 runes as letters, not shapes. (Reports 01, 08, 11.)

**9. Sound patterns can be checked by rule, up to a point.** No dictionary word begins with *tr, bl, fl, gl, pl* or *sn*. Requiring a new word to begin and end like existing words keeps 97.5 percent of real words but lets through a third of scrambled words. Rules narrow the field; they do not replace judgement. (Reports 01, 07.)

**10. What teaching research supports, and its limits.** Short explicit rules followed by practice; recall from memory with feedback, spread over days; separate practice in each skill; much easy reading in which new words recur. But published effects are inflated, and all of it comes from natural languages. (Reports 09, 10, 12, 15.)

**11. What made other constructed languages last.** Esperanto, Klingon, Na'vi and Toki Pona each had one written reference, a known final authority, a core that never changes, and somewhere to use the language. Others failed through endless reform, fights over ownership, or no authority at all. (Reports 03, 06, 14.)

**12. The fan hub retreated to official words.** See point 2 of section 0. Its dictionary states no licence and gives no contact address; section 9 gives the basis on which the project uses it. No other app combines lessons, spaced practice, rune reading and writing offline (Report 03, from search summaries only).

**13. The legal position** is set out in section 9: the language itself is very probably free to teach and extend under United States law, but the game's *texts* are protected and the project runs on tolerated use. (Report 04. Research, not legal advice.)

---

## 2. What you asked for, and what this design gives you

| You asked for | This design gives | Why | To get exactly what you asked |
|---|---|---|---|
| A thing that can be downloaded and runs standalone, offline, on Android, Mac and Windows | That, as the committed end goal: a standalone program for each of the three systems (decided; log item 18). A web app installed from a web page may come first, as a step | The web app is wrapped to make the programs, so the same program is the core of both | Nothing further on the goal (section 8) |
| Free for everyone; you make no money | Yes | | Decided (log item 17): the project's lessons, rulings and coined words may not be sold. The program code is under the GPL, so the code alone could still be sold |
| Thuum.org's fan expansion built in | Its current dictionary is built in, with credit, for non-commercial use. Its retired fan vocabulary is only a source of candidate words, each entering by the same route as any new word (decided; log items 1 and 14) | Thuum.org itself abandoned that vocabulary, for the two causes in section 0 | Nothing further: decided (log item 14) |
| People can add words as long as they fit the structure | People can *propose* any word that passes the rules and comes with the sentence it is needed for. You ratify | A rule cannot judge whether a meaning is needed or a word is a good fit | You could ratify everything that passes. I advise against it |
| You are the ultimate authority; nobody can change the rules | True for the official edition (decided; log item 16). The licences allow sharing, so others may publish a changed copy | What marks your edition is its web address, its name and its release record | Nothing further: the licences are decided (log item 17) |
| Fill the gaps by borrowing from the most similar language | English structure where the games are silent, after the games' own patterns (my practice; not yet ruled), with a guard against copying English (decided; section 4.5) | The most similar language is English | Your ruling on the order of sources (section 12) |
| Fluency: reading, composing, conversation, role play, script, pronunciation | Checked targets for reading, writing, script and listening. Pronunciation follows an adopted reading convention (decided; section 7). Speaking is practised and self-assessed. Conversation is scripted | No offline program can judge free conversation or score pronunciation in a language with no speakers | Other people. The app prepares learners for play and correspondence with them |
| New script symbols that look like relatives of the claw marks | Numerals, punctuation, a break mark for the apostrophe and a handwriting style first; fused letter-runes as an option | Every letter already has a rune; these are what the script lacks | New letter-runes can be added if you want them; they would have no sound of their own to carry |
| No live AI tutor; rules standalone and offline | Yes | | Note: I would draft lesson texts during development. Nothing in the installed app calls an AI |
| Research at the edge of the field, scholarly sources only | 939 references; a script confirmed 685 against the scholarly registry; full texts could not be opened | Network limits | A second pass with library access |

---

## 3. The app

| Part | What the user does |
|---|---|
| **Learn** | A staged course: runes and sounds, first words, reading inscriptions, questions and answers, composing, scripted conversation |
| **Read** | Game texts and graded stories, each word tappable for its meaning, in runes or Latin letters |
| **Forge** | Propose words and see them checked; browse rulings and open gaps |
| **Reference** | Dictionary, grammar, rune converter, pronunciation guide |

Every word, rule and sentence carries a visible label saying where it comes from. Invented words sit in a separate track that the learner switches on (still open; section 12). There is no translator that turns English sentences into dragon ones; dictionary lookup stays (log item 14).

---

## 4. The rulebook and the forge

### 4.1 The constitution

The rules about who decides, published with the app. Decided: you accepted them on 2026-11-22 (log item 16); the accepted text is `docs/constitution.md`. The examples and notes here are mine.

1. **Game text is the base.** It is always shown as the game wrote it, and no ruling removes anything the game shows. Where a ruling sets a different standard, the game's form stays an accepted variant: the game writes *bormahii* ("his father"), and the standard is now *bormahi'i*.
2. **Every word carries a visible label of where it comes from:** game, guide, guide website, source untraced, later game, or coined for this project (section 1, point 3). A proposed word is first Local (on one person's device), then Trial, then Ratified (section 4.4).
3. **Checks decide what may be proposed. Only you ratify.**
4. **A new word needs a sentence it is used in.** The founding batch of basic words is exempt, because nothing can be written without it; it comes from the course's own conversation scenes.
5. **Each ruling is published with its reason,** in numbered releases.
6. **Grammar rulings stay provisional until they have been through one release in use,** then they are frozen.
7. **A ratified word never changes its form or meaning.** It can only be retired.
8. **Only you can change the rules of the official edition.**
9. **Succession: not yet written.** The project will name a second person who can keep it running if you cannot. It is to be written before the first release.

**Until the first numbered release, everything decided so far can still be changed,** including the six coined words. After it, a ratified word cannot be quietly corrected: it can be retired and another coined, in public, with a reason.

Not in the accepted text, and still my suggestions: about 50 new words per release at most; and marking the official edition by its address, its name and the font's reserved name.

One thing to be plain about: I prepare each ruling with a recommendation, and where you cannot evaluate it, the recommendation becomes the language in practice. The safeguards: every brief shows the game evidence with examples for each option, briefs are published, and rulings stay provisional while they are tried. On the apostrophe you ruled differently from my recommendation.

### 4.2 The rulebook as data

The language is stored as plain files that one small program reads, in the app and in the project's automated checks, so a word gets the same verdict everywhere. The rulings so far are already stored as plain files in `research/data/`. In the finished rulebook each rule will carry examples that must pass and examples that must fail, and you will see which verdicts a rule change would alter before approving it.

### 4.3 What the word checker tests

Tests 1, 2, 6, 8, 9 and 10 follow rulings already made (`research/data/forge-policy.json`), as do the reserved spellings in test 5 and *se* in test 7. The rest are proposals; tests 3 and 7 wait on rulings (section 4.5).

1. **Spelling.** Only letters and letter-pairs the language uses, and only a word's standard spelling: *qethsegol* ("stone"), not the variant *quethsegol*.
2. **The apostrophe.** Accepted only between two u's where the coiner declares a break in the voice (as in *thu'um*) and in the possessive endings *-i'i* and *-i'il*. Whether a break may be written between other vowels is not decided.
3. **Sound pattern.** Every syllable must begin, centre and end in a way found in game words: no game word begins with *tr*, so no new word may. Patterns found in five or more words pass; rarer ones pass with a note or need your approval. Words of power must be one syllable (all 136 in the games are).
4. **Typicality score.** How closely a word resembles game words. Advisory only.
5. **Collisions.** Not identical to any existing word, any form of one with an ending, any rune spelling, or any of the ten reserved words (such as *han* and *tosh*). Words one letter apart are only listed; the games pair related words that way (*jun* "king", *jud* "queen").
6. **Building parts.** A new word may be built on Game, Guide and Guide website words and on the seven untraced words; not on a reserved word, a spelling variant, or *vun*, which carries a doubt mark. Recorded forms and the one name are not separate words.
7. **Structure.** A compound names its parts and its main part. The games use two orders (*Dovahkiin*, "dragon-born"; *Qethsegol*, "bone-of-earth"). *Se* joins the parts, as in *sossedov*, "blood of dragonkind".
8. **Word type.** A new verb or adjective is "strong" (it can also serve as a noun) unless a separate noun for the idea exists; then it is "weak". *Faas* is "to fear" and "fear"; *vahzah* ("true") is weak because *vahzen* ("truth") exists.
9. **Need and meaning.** The proposal carries the sentence the word is needed for; the proposer must first try an existing word, a phrase, a form built on an existing family, or a compound; and the meaning is a short explanation with examples, not a single English word. Where English merely has two words for one idea, none is made: no word for "me", because *zu'u* is both.
10. **Pronunciation.** Worked out from the spelling by rule (section 7), with stress on the word stem the coiner declares, or on the first syllable of a new stem.
11. **Names.** Not on a list of other people's names and trademarks.

Game words that break these tests (rare endings such as *ahrk* "and") are listed as named exceptions. Proper names are exempt.

### 4.4 How a proposal travels

1. A person has a sentence they cannot say, and coins a word for it in the app. The checker runs on their device.
2. If it passes, the proposal must carry that sentence and a short explanation of the meaning. The proposer confirms that the word is their own invention and releases it under the project's content licence; for a retired fan word they name its maker instead, and the terms for such words are not yet known (section 12). The app produces a proposal file and a link to a pre-filled submission on GitHub.
3. An automated check re-runs the same program. It never accepts anything.
4. **You screen it:** one click to confirm the explanation is acceptable. Until then it is not published.
5. Screened proposals enter Trial, labelled, and are shown only in the invented-words track. Lessons use Ratified words only.
6. You rule in batches. Each ruling is published with its reason.

Safeguards from the start: a limit per contributor; meanings capped in length and shown as plain text; an automated check that can comment but change nothing; and a trial of the whole path with deliberately malicious submissions. Submitting needs a free GitHub account, whose name is public; a person without one can pass their proposal file to someone who has.

### 4.5 Filling the grammar

For each open area I prepare a brief with the game evidence, the options and a recommendation. The order of sources I work by is below. As a whole it is not yet ruled (log item 18; section 12); only its base, game text, is (log item 16).

1. **Game text.** One occurrence is enough for a pattern to be offered; the majority pattern is the default.
2. **What the language already has,** by analogy: the game has *wo* "who" and *wen* "whose", so the new question words begin with *w*.
3. **English structure, simplified,** under the guard below.
4. **Old Norse and Old English patterns,** for word-building and style only.

The retired fan vocabulary is not a step in this order (section 2). No word is borrowed from English or any other real language; you ruled this (log item 19).

**The guard against copying English** (decided; log item 14). A new word starts from a sentence, not a word list: the question words came from "Why did you do that?", now *Wul drey hi dreh daar?* What the language already has is tried first, and a coined word is defined by how it is used. Lists of basic English concepts are a cross-check only.

Where the games leave a feature optional (tense, plural, articles, "is"), the course teaches a default and the checker accepts every form the games allow: an unmarked verb is never an error.

| Before course stage | Ruled | Still to rule |
|---|---|---|
| 0 | Sound values and stress (the reading convention); one standard spelling per word; the apostrophe; which meanings count | Rune spelling rules beyond the break; a break between other vowels; set phrases |
| 1 | Pronouns; possession; verbs and time; "is"; "not"; articles; plural | The choice of first verbs |
| 2 | How a question is formed; five question words | Numbers; "can, must, should" and "if"; linking words; the rest of the founding batch; rare sound patterns; compound order; word-building endings |
| 3 and 4 | Word types (21 words still lack one); where a describing word goes; commands | The other open areas in section 1, point 5 |

---

## 5. Teaching design

### 5.1 What "fluent" means here

Three targets the app can check, and one it cannot.

1. **Read** the glossed game texts with the glosses hidden, answering typed comprehension questions.
2. **Write** text that the grammar checker accepts, within the ratified vocabulary.
3. **Understand by ear** words and sentences in the project's reading convention. Lessons no longer wait for a listening pass through the game (section 7).
4. **Speak:** practised by listening, repeating, recording and comparing. Self-assessed, and labelled as unverified.

Open conversation needs other people. No study shows it arising from software alone.

### 5.2 Stages

| Stage | The app can test that the learner | Words |
|---|---|---|
| 0 | Converts every rune to its letter and back; recognises a first set of words of power and greetings by sight and by ear | about 40, all from the games |
| 1 | Reads a first set of about a dozen inscriptions with glosses hidden; builds simple sentences the checker accepts | about 100, all from the games |
| 2 | Asks and answers set question types in typed scenes | about 300, including the first ratified words |
| 3 | Reads the glossed game texts with glosses hidden | all of the roughly 650 game words |
| 4 | Composes text the checker accepts; completes scripted scenes by typing | 1,000 to 1,200, of which 350 to 550 newly ratified |
| 5 | Contributes to the forge | |

Sixteen runes cover 83 percent of inscription text. With a well-chosen 100 words roughly a dozen of the 64 inscriptions are fully readable, and with 300 roughly 45.

Gates advise; they do not lock. Stages 0, 1 and 3 use game material only. Stages 2 and 4 need invented words.

### 5.3 How each thing is taught

- **Grammar.** One card per pattern: a short rule with game examples, then exercises that recognise the pattern, then exercises that make the learner produce it. Where a ruling allows more than one form, the card teaches the default and names the others as correct. Most attention goes to the places where an English speaker's habits mislead (English *'s*, plural *-s* and "do not").
- **Word roles.** You chose flexibility (log item 7): a word may be used in every role the word-type system allows, whether or not the game shows that use. *Mul* may serve as "strong", "strength", "strongly" and "to strengthen". The cost, as the log records: the more roles a word may take, the fewer mistakes the sentence checker can catch.
- **Vocabulary and runes.** Recall from memory with feedback, on a schedule that spaces reviews over days. The scheduling method, a free published one called FSRS, is well documented; no trial shows it produces more learning than simpler schedules.
- **Reading.** Graded stories in which most words are known and each new word recurs about ten times. Every authored line is labelled as not from the games.
- **Writing.** Word tiles, then filling slots in game formulas, then free composition. The checker checks form, not meaning: a well-formed sentence that says the wrong thing passes.
- **Conversation.** Scripted branching scenes, answered first by choosing a line and later by typing one. These scenes also supply the first batch of missing words (section 4.5). The app also produces scene sheets and phrase cards for tabletop play.
- **Mastery.** An item counts as known after correct recall on three separate days, the last at least a week after the one before (a starting value).

### 5.4 Minimum workload for a learner

At a ceiling of eight new words a day, falling to about five as reviews build up, a learner meets all the game words in twelve to nineteen weeks and recognises stage 4's vocabulary in four to eight months, before any reading. These are floors computed from starting values, not promises.

### 5.5 What is left out, and why

No lives, leaderboards, currencies, or streaks that punish a missed day, although streak incentives do raise persistence in recent studies. The replacement is a weekly target the learner sets, and progress is shown as real capability ("you can read 12 of 64 inscriptions unaided"). The app is built to the WCAG 2.2 AA accessibility standard: runes are real text with a Latin-letter alternative, and nothing depends on colour or dragging alone.

### 5.6 How we find out whether it works

The app sends nothing anywhere. Two measures: a small pilot at each build stage with a stated pass mark (for example, three new testers read an unseen inscription unaided), and an optional button that saves an anonymous results file a learner can choose to send.

### 5.7 Content

The course needs roughly 45,000 to 65,000 words of graded text and several hundred dialogue lines, about twenty times all the text in the games. The estimate rests on one assumed multiplier and could be well off.

I would draft it, with a line-by-line English version; the checker would verify form; you would read and approve. Nothing but your reading checks the meaning. Text drafted this way is untested as reading material. And because it will dwarf the games' text, its habits (how often tense is marked, for instance) will in effect set the norm, so it has to follow the rulings exactly.

---

## 6. The script

All 34 runes exist, and every letter the language uses has one. The gaps are numerals, punctuation and a sign for the break that the apostrophe writes.

1. **Obtain reference images of the 34 runes and measure them.** They are used for measuring only and are not put in the repository.
2. **Draw an original font from those measurements.** The game's font file is never opened or copied. Letter shapes are not protected in the United States; font files are. This font is needed for the first release.
3. **Derive new signs the way real scripts did:** add or drop a stroke, add a dot, fuse two signs. Each new sign must differ from every existing one by at least two features.
4. **Order:** digits and sentence marks; a word divider; a break mark; a handwriting style; fused runes for *th, sh, ng* as an option that never replaces game spelling.

**How the break is written in runes** (decided; log items 9 and 11). The apostrophe writes a break in the voice, a light catch in the throat. The runes have no sign for it, so one is to be designed.

| In Latin letters | What it is | In runes |
|---|---|---|
| *uu* (*gravuun*, "autumn"); *ii* inside a word (*krii*) | One long vowel | The single double-U or double-I rune |
| *u'u* (*thu'um*); *-i'i* and *-i'il* (*zaami'il*, "your slave") | Two vowels with a break | Two separate U or I runes, with the break mark between them once it exists |

Game inscriptions are shown as written: the Throw Voice word wall writes *thu'um* with the single double-U rune, and that is kept as a variant. The inscriptions are inconsistent in other ways too (the pair *ah* is one rune 225 times and two runes 15 times), so game text is stored rune by rune as written and the strict spelling rule applies only to new words.

---

## 7. Pronunciation

1. **The reading convention is adopted** (log item 8): the Fifth Edition's pronunciations, given for 644 entries and credited to Thuum.org. Where its sound table and its entries disagree, the entries are followed: *e* as in "bed", *ei* as in "eye", *q* as "kw". Where an entry lists several pronunciations, the first is taught and the rest are accepted. It is labelled everywhere as a convention, not official.
2. **The break.** The six words spelt with *u'u* (*zu'u, thu'um, su'um, du'ul, strundu'ul, tu'um*) are taught with a break between the two u's (log item 9); the one-syllable form the dictionary lists first ("thoom") stays accepted. The possessive endings *-i'i* and *-i'il* have the same break (log item 11).
3. **Your condition: at some point people will listen to the game.** So what is heard in the game is recorded per word, with the speaker and the line. A form heard there is accepted, and where the game consistently contradicts the taught form, the taught form changes in a numbered release. A listening pass is no longer needed before lessons are written. The dictionary says voice actors vary greatly, so listening cannot settle most sound values.
4. **New words are pronounced by rule.** Each spelling unit takes the sound the dictionary most often gives it. Tried on dictionary words the rule had not been shown, it got every sound right in 92 percent of words when the stress was known, and 89 percent with the stress put on the first syllable. Example: the coined *niist* comes out as "neest".
5. **Stress cannot be worked out from spelling.** Of 305 words of two or more syllables, the first syllable is stressed in 63 percent, and no simple rule tried does more than three points better. So stress is taught as marked in the entries and described as a tendency. For new words, see section 4.3, test 10.
6. **Reference audio is machine-made at first, and will sound robotic.** Volunteer recordings replace it over time. No game audio is used.
7. **Listening practice with feedback** can be scored offline, but its research support comes from human voices, so it stays provisional until human recordings exist.
8. **Speaking practice** is listen, repeat, record, compare, with no score: an honest one needs speech models built from native speakers, and none exist.

---

## 8. Platform

**Decided** (log item 18): the end goal is a standalone program for Mac, Windows and Android, each running with no connection. A web app may come first as a step; wrapping it (packing it inside a small program for each system) makes the standalone programs. Each system offers two routes; which to take, and what to spend, you choose when the programs are packaged.

| System | Through the system's maker | Without it |
|---|---|---|
| Windows | A free Microsoft Store listing; needs an identity check | An installer that shows a security warning |
| Android | A developer account: identity documents and 25 dollars once | A file the user must allow by hand |
| Mac | 99 dollars a year to Apple; no warning | An installer the user must approve in System Settings |

**The web app step** is served as plain files from GitHub's free website hosting (GitHub Pages) and installed from the browser.

| Device | How it installs | Needs |
|---|---|---|
| Android | Chrome: "Install app" | A current Chrome |
| Windows | Edge or Chrome: "Install" | Windows 10 or 11 |
| Mac | Safari: "Add to Dock" | macOS 14 or later. Current Chrome needs macOS 13 or later |
| iPhone | Safari: "Add to Home Screen" | |

**Your Mac.** What matters is its macOS version: on an older system the app still runs offline in a browser tab but cannot be installed as its own app, and Safari may delete its saved data after a week without use.

**What the web app step does not give you.**

- The first visit must be online.
- There is no file to hand someone on a memory stick.
- The app and the learner's progress live in the browser's storage, which can be cleared. The app will prompt for a backup file on a schedule and offer "restore from backup" on its first screen.
- Progress moves between devices only by that backup file.

**Size.** Text data is under 200 KB compressed; audio, about 25 MB, is downloaded separately.

**The address** of the web app is not yet settled (section 12).

**None of this has been tested on real devices.** Section 11 begins with a one-day test that you would do by hand.

---

## 9. Legal position

Research, not legal advice.

- **The language itself.** Under United States law, grammar, sound rules and single words are very probably free to teach and extend. The complete word list as a set is less certain, and the app ships all of it. Other countries' rules were not researched.
- **The game's texts** are the clearest exposure. They ship as a separate pack that can be removed, and appear only inside a unit that adds analysis or an exercise. The app must work with that pack absent.
- **No game assets:** no audio, art, screenshots or font files.
- **The name** contains no trademark of the rights holder. An "unofficial, not affiliated" notice appears on first run, and a "Sources and licences" screen is readable offline.
- **The wiki data** is under a Creative Commons licence that requires credit and requires anything built from the wiki editors' text to carry the same licence. Most such files are separate; `NOTICE.md` lists the four that draw on more than one source.
- **The project's own work.** Its licences are decided (log item 17; section 12).
- **Thuum.org's dictionary** is included, with credit, for non-commercial use only (decided; log item 1). No formal licence text was found. The basis, recorded in `research/sources/thuum/ATTRIBUTION.md`: the title page says the game material it features is used for non-commercial, educational purposes; a forum answer, seen only through a web search, says the site claims no intellectual property over the dragon language and cannot license commercial use; and you stated on 2026-11-15 that Thuum.org's website, and its administrator personally, say the dictionary is free for any non-commercial use. The administrator's own wording is still to be added. If Thuum.org objects, the file and the data built from it will be removed. Files built from the dictionary keep these terms, so an edition containing them may not be sold.
- **Tolerated use.** The project has no licence from the rights holder. A complaint about any file can take the whole repository offline, and with it the site. The host belongs to Microsoft, which also owns the game's publisher. Installed copies should keep working; updates and submissions would stop. The first release includes a public contact address, a commitment to answer within 48 hours, a one-step way to produce the app without the game texts and wiki-derived text, and a private log of notices.

**This repository today** (decided; log item 1). It stays public, by your decision. It holds 331 complete wiki pages, including English game dialogue and song lyrics, the game texts extracted from them, and now the Thuum.org dictionary and the data built from it. Attribution and an "unofficial" notice are in place. The wiki's licence lets its editors' text be republished with credit; it cannot grant rights in the game text those pages quote.

---

## 10. What this costs

**Money.** Nothing is required to build. The standalone programs are required (log item 18); what they cost depends on routes you have not yet chosen (section 8). Optional: a web address of your own (roughly 10 to 15 dollars a year, my estimate). The cost of a lawyer's review was not researched.

**Your time.** The rough estimate of 60 to 150 hours was made before any ruling and has not been redone. Sections 1 and 12 show how much of that is done; reading the authored texts has not started.

Not included: screening submissions; testing each release on your devices; finding pilot testers.

**Dependence on one person, and on me.** You are the only one who can rule, and you cannot read the program code you approve; your control is the report showing which verdicts a change would alter. I would write the program, the briefs and the content, limited by your usage allowance; the files are plain and documented so another person or assistant could continue.

---

## 11. Build order

**Before committing: five small tests.**

1. A one-page offline test installed on your phone, PC and Mac: switch the network off, leave it ten days, publish an update, clear the browser once, restore from backup.
2. Twenty words rendered as synthetic audio, including words with a break, for you to hear.
3. The submission path run on a throwaway project with deliberately malicious submissions.
4. Five runes drawn as original outlines, for you to compare with the game.
5. A downloadable folder edition for PCs and Macs that runs without installing. This may not be workable.

| Build stage | Delivers | Done when | Needs from you |
|---|---|---|---|
| A. Reader and reference (first public release) | Rune font, rune chart and converter, dictionary with status labels, the 64 inscriptions with every word explained, rune recognition practice, backup and restore, notices and sources screen | Installs and runs offline on your three devices; an update arrives without losing data; every game word passes the checker or is on the named exception list | Rune reference images; device tests; the open decisions in section 12 |
| B. Rulings, round one (partly done) | Done: the rulings listed in section 12. Remaining: see below | Rulebook 1.0 published | Your rulings |
| C. Course, first part | Stages 0 and 1; review scheduler; first audio; a sentence checker that tests words and simple patterns | Pilot testers meet the stage 1 pass mark | Pilot testers |
| D. Forge | Coining, checking, proposal files, automated checks, screening, Trial, ratification, releases | A proposal travels end to end; the malicious-submission trial passes | Screening and rulings |
| B2. Rulings, round two | The areas not needed until stages 3 and 4 | Rulebook 2.0 published | Your rulings |
| E. Course, second part | Stages 2 and 3; full grammar checker; first scenes; graded texts | Pilot testers meet the stage 3 pass mark | Approving texts |
| F. Composition and conversation | Stage 4; numerals and punctuation; human recordings | Pilot testers complete a scripted scene by typing | |
| G. Standalone programs (required: the end goal) | The app wrapped as a program for Mac, Windows and Android | Each installs and runs with the network off on your three devices | Your choice of routes (section 8); device tests |

**What remains of round one.**

- The rulings still to make for course stages 0 to 2 (table in section 4.5).
- The founding batch of words. I draft the first conversation scenes, and the words they cannot be written without come to you.
- Loose ends I can tie up without you: types for the 21 words that have none; eight further spelling cases to check against game text; six misprinted definitions to re-read from the publisher's file; and the cited definitions to check against the game pages.

Stopping after A still leaves a usable reader; stopping after C leaves a course for runes and first inscriptions. The project is not complete before stage G (log item 18). I cannot give dates: pace is set by your usage allowance and your own time.

**Not in the first version,** with what each would have given:

- Digitally signed data files: proof that a word list really came from you.
- A second, independent copy of the checker: a way to catch mistakes in the first.
- Outside concept databases: a standard numbering of meanings. By your ruling, lists of concepts are only a cross-check.
- Automatic tuning of the review schedule to each learner: it needs months of a learner's data.

---

## 12. Decisions

### Decided so far

| Log item | What | The decision in one line |
|---|---|---|
| 1 | Repository; Thuum.org dictionary | The repository stays public; the dictionary is included with credit, for non-commercial use |
| 2 | How a word's standing is graded | By where its definition comes from: game, guide or guide website |
| 3 | Words only the Fifth Edition has | Added as vocabulary; place names go to the list of names |
| 4 | Words only the wiki has | Forms filed under their base word; later-game words kept and labelled; ten reserved |
| 5 | Spelling | One standard spelling per word. Game texts are never altered; rare spellings are variants |
| 6 | Which meaning counts | The official definition from the best source; community meanings kept as labelled second senses |
| 7 | Word types | Thuum.org's types adopted. A word may be used in every role the system allows |
| 8 | Pronunciation | Thuum.org's pronunciations adopted as the reading convention, open to what is heard in the game |
| 9 | The apostrophe | It writes a break between two u's and belongs to the standard spelling: *thu'um*. Writing a word without it is accepted, but is not the standard |
| 10 | Pronouns | One form for subject and object: *zu'u* is "I" and "me". *Nust* "they", *niin* "them" |
| 11 | Possession | A separate word or an ending, both standard: *hin dovah* or *dovahi'il*, "your dragon". *Niist* "their" coined |
| 11b | Questions | Three ways, all correct: a question word first, the verb before the subject, or a questioning tone. *Wil los hi?* "Where are you?" |
| 12 | Verbs and time | One verb form; marking time is optional. *Keizaal fen kos stin*, "Skyrim will be free" |
| 13 | Articles, plural, describing words, "not", commands | Articles and plural optional (*sil*, *sille*, "souls"); describing words before the noun (*vul junaar*, "dark kingdom"), after it accepted; *Zu'u ni faas*, "I do not fear"; a command is the plain verb (*Aam uv dir*, "Serve or die") |
| 14 | New words; community vocabulary | A word starts from a sentence. Fan words enter by the same route, with credit. The seven untraced words are kept |
| 16 | The constitution | Eight rules on who decides (section 4.1). Succession is still to be written |
| 17 | Licences | Lessons, rulings and coined words: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (free to copy and adapt with credit; not to be sold). Program code: the GPL, version 3 or later. Font: the Open Font License. Files built from other sources keep those sources' terms (`NOTICE.md`). Changeable only until someone else contributes |
| 18 | Standalone programs | The end goal for Mac, Windows and Android, running with no connection; a web app may come first (section 8) |
| 19 | The name; borrowing | *Zu'u Tinvaak Dovah*, "I speak dragon", three words of the game's. No word is borrowed from English or any other real language |

**Until the first numbered release, everything decided so far can still be changed** (log item 16).

### Still open: decisions that define the project

In the order of the log's queue.

**The permanent address** (left unanswered; log item 18). An installed copy of the web app is tied to its web address, so the address must be fixed before the web app is first released. A standalone program does not depend on it, so the question matters less than it did. The choice: the free GitHub address (no cost; if the host removes the site, installed copies of the web app lose their update channel for good) or a web address of your own (roughly 10 to 15 dollars a year; it must never lapse). *Working default: the free GitHub address, unless you say you want your own.* Either way the app should live in its own repository, apart from this one. What to spend on the programs is also unanswered; it is chosen when they are packaged (section 8).

**The game texts pack** (put to you on 2026-11-23). *Recommendation: include it, removable, always with analysis.* The alternative is a first release with words only and no inscriptions, which removes the clearest exposure but is much less useful.

**Where invented words appear.** Options: off by default, switched on once with an explanation (this draft); or on by default with a "games only" switch. The community report advises the first, because today's fan hub keeps to official words. Conversation cannot be taught without invented words, and six already exist. Either way an invented word is always labelled. *Recommendation: off by default.*

**A lawyer's review before public release,** of the name, the licences and the text policy, as the legal report advises; I would add the basis for using Thuum.org's dictionary. *Recommendation: yes if you can; at the least before any standalone program is published or listed in a store.*

**The order of sources where the game is silent** (section 4.5). Not yet put to you. *Recommendation: accept it; a brief will set out the evidence first.* The rule against borrowing words from real languages is now ruled (log item 19); whether to borrow from the game world's own languages is undecided.

### Still open: rulings on the language

Further rulings on the language itself are still to come, each as its own brief with a recommendation (table in section 4.5). One is left over from the apostrophe ruling: whether a break may be written between other vowels. *Recommendation: leave it closed until a sentence needs such a word.*

### Still open: defaults you can accept together

These are reversible.

- I draft lesson texts and dialogue; the checker verifies form; you approve.
- Submissions need a free GitHub account, with the file route for those without one.
- A weekly target in place of streaks, lives and leaderboards.
- At most two words per concept; no brand-new word stems for modern or technical concepts.
- The four items listed under "not in the first version" in section 11 stay out.
- The course is written for English-speaking learners.
- No new letter-runes for now; numerals, punctuation, the break mark and a handwriting style come first.

### Still open: things only you can do

- Tell me your MacBook's macOS version, your phone's Android version, and your country (the legal research covers United States law only).
- Get the administrator's own wording on the terms for using Thuum.org's dictionary, and where it is stated, for the attribution file. I suggest asking at the same time about words from the retired fan vocabulary, which that file does not cover.
- Send listening reports whenever you or others listen to the game: the word, the speaker and the line.
- Rune reference images: approve access to the wiki's image server, or send me a screenshot of the alphabet.
- Name a second person who could recover the project.
- Agree to be the public contact for complaints, answering within 48 hours (section 9).
- Run the tests in section 11 on your devices.
- Find three to five pilot testers.

---

## 13. How far to trust this

- **Citations.** 939 references were checked by script against the scholarly registry: 685 matched, 42 were not found, 201 are of kinds the registry does not cover, mostly web pages, and 11 were found by other means. None was flagged as a mismatch. Full texts could not be opened: figures come from abstracts, search summaries and the analysts' prior knowledge.
- **Thuum.org: what is now first-hand.** The Fifth Edition itself, read by program and compared entry by entry with the wiki. First-hand from it: that the fan vocabulary was abandoned, the two causes, that no year is given, and that it states no licence and gives no contact address.
- **Thuum.org: what is still second-hand.** Two of the three grounds for using the dictionary (section 9). The earlier draft's report of a March 2026 home-page notice is unconfirmed.
- **The dictionary copy has known misprints.** It is a PDF converted to Word. Six definitions are misprinted (*krii*, "kill", is printed as "fight"), thirteen entries carry a doubt mark, and *zu'u* is printed as a verb. Its official definitions have not yet been checked against the game pages, and those resting only on the guide or its website are taken on the Fifth Edition's word.
- **The grammar rulings are provisional** until one release in use, and everything decided so far can still be changed until the first numbered release (log item 16). Some rest on thin evidence: each of the three ways of asking a question occurs once in game text, and the break in the possessive endings is this project's convention, with nothing known of how the game's voice actors say them.
- **Game data.** Counts come from the data files, which rest on one wiki snapshot. Rune spellings follow the wiki's transcription and were not checked against the game.
- **Platform facts** were checked by search in November 2026 but not on devices.
- **Starting values, not findings:** stage sizes, the content estimate, pass marks, repetition counts, mastery rule, release size, hours.

---

## Words used in this document

| Term | Meaning here |
|---|---|
| Game text | What appears in the games themselves |
| Rulebook | The files that define the language for this project |
| Ruling | Your decision on an open question, recorded with its reason |
| Ratify | Your approval that makes a proposed word part of the language |
| Meaning of record | The one meaning the project uses for a word |
| Standard spelling, variant | The one spelling the project teaches for a word, and any other spelling of it found in the sources |
| Strong, weak | A verb or adjective that can also serve as a noun (strong), or cannot (weak) |
| Reading convention | The pronunciation this project teaches; not official |
| Break | A light catch in the throat between two vowels (a glottal stop), written with an apostrophe |
| Checker | The program that tests a word or sentence against the rulebook |
| Gloss | The meaning shown for a word |
| Graded text | A story written so that nearly all its words are already known |
| Web app | An app delivered through a browser that can be installed and run offline |
| Repository, GitHub, GitHub Pages | The public online folder holding the project, the site that hosts it, and its free website hosting |
| Open licence | Terms that let anyone use and copy the work under stated conditions |
| Share-alike | A condition that copies and adaptations carry the same licence |
| GPL | A licence for program code: anyone may use and change it, and changed versions must stay open |
| Word stem | The core of a word before any ending is added |
| Trial | A proposed word that passed the checks and your screening and awaits your ruling |
