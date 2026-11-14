# Design proposal: a teaching app and language forge for the dragon language

**Status:** second draft, for the owner's decision. No app code has been written.
**Date:** 2026-11-14.
**Evidence:** the fifteen reports in `research/` and the data in `research/data/`.
**Review:** the first draft was checked by four independent reviewers against the canon data, the teaching research, the platform facts and the owner's original request. They found three places where it would have misled you and about thirty where it was imprecise. This draft incorporates their findings. Section 13 says what is still unverified.

A note on the name: "Dovahzul" is a fan name. Official text says "Dragon Language" or "Dragon tongue". This document says "the dragon language" for what the games contain.

---

## 0. The short version

**What I propose.** One free app with four parts: a course, a reading library, a word forge, and a reference (dictionary, grammar, rune converter). Everything runs on the device with no connection and no live AI.

**What you would get first.** A reader and reference for what the games already contain: dictionary, rune chart and converter, and the word walls with every word explained. It needs none of your rulings and can be released while the language is being finished.

**The four things you most need to know.**

1. **The language has to be finished before it can be taught to conversation.** The games contain about 650 words and a few thousand words of text. There is no word for *what, where, why, how, if, because, two* or *thank you*. The forge is therefore the main line of work, and your rulings come before most lessons.
2. **Thuum.org already tried open fan expansion and gave it up.** As far as I could establish without reading the site directly, it reached about 6,000 fan words, found revising them unsustainable, retired them in 2016, and in March 2026 removed the links to them. Its current dictionary is canon only. Your instinct for firm rules and one authority is what that history calls for.
3. **"Installable web app" is not quite the downloadable file you asked for.** It installs from a web page on first visit and then runs offline. True installers are possible; on Mac they cost 99 US dollars a year. This is your decision (section 12).
4. **The work is large and rests on you.** I estimate 50 to 125 hours of your time for rulings and review over the life of the build, and the content to be written is about twenty times the size of everything in the games.

**What I need from you:** answers to the decisions in section 12. Nothing else is blocked on you today.

---

## 1. What the research found

**1. The makers built a game device, not a full language, and said so.** The designer who wrote it told the press in 2011: "you're not developing it as an actual language. It's much more word based." Anything beyond individual attested words is this project's design, not recovery of something hidden. (Report 02.)

**2. The game material is small.** The wiki dictionary has 657 entries. Connected text (word walls, dialogue, songs) comes to between 2,200 and 2,600 words depending on how duplicates and names are counted, with 700 to 750 distinct word forms, about half of which occur once. There are 64 distinct word-wall inscriptions. (Data files; recounted for this document.)

**3. Not all 657 entries stand on the same ground.** 392 cite game text. 163 rest only on the official strategy guide. 91 rest only on a word list hosted by a fan archive, whose origin could not be traced. Most English meanings are wiki editors' readings; only four sources carry English that appears in the game itself. (Reports 01, 02.)

**4. About half of everyday vocabulary is missing.** Against three standard lists of basic concepts, the dictionary covers 47 to 51 percent. Counting only words attested in game text, it covers 32 to 46 percent. Missing: *what, where, why, how, if, because, two, three, thank you*, and most body parts and basic verbs. A greeting exists as a set phrase (*Drem Yol Lok*). (Report 06. The concept lists were typed from memory and must be checked against the published lists.)

**5. Grammar has 34 undecided areas.** Seven block teaching outright: sound values, numbers, pronouns, possession, tense, questions, core vocabulary. Sixteen must be ruled before the first three course stages can be written. (Reports 01, 15.)

**6. The most similar natural language, of ten compared, is modern English.** On 30 standard grammatical features the dragon language scores 0.82 against English (1.0 would be identical), 0.80 against Afrikaans and 0.62 against Old Norse. The designers put invented words into English sentence structure. Old Norse and Old English supplied the *style*: memorial inscriptions, compound names, a heroic tone. (Report 05. The older languages were scored by one analyst and the figures are approximate.)

**7. Where it differs from English, it does so by leaving things out, and not consistently.** Tense is optional. Articles and plural endings are usually omitted. "Is" is often dropped. Possession is marked by a suffix (*thuri*, "my overlord") about as often as by a separate word (*dii*, "my"). *Ni* ("not") stands before the verb without "do" in 25 of 27 cases and with it in two. These are tendencies that need your ruling, not rules already fixed. (Reports 01, 05; counter-examples found in review.)

**8. There is no official pronunciation, and the project has no drawings of the runes yet.** Every published sound value is a fan convention. An in-game book says an old song lacks "a sure pronunciation". The data holds the 34 runes as letters, not shapes. (Reports 01, 08, 11.)

**9. Sound patterns can be checked by rule, up to a point.** Four in five syllables are consonant-vowel or consonant-vowel-consonant. No dictionary word begins with *tr, bl, fl, gl, pl* or *sn*. Requiring a new word to begin and end like existing words keeps 97.5 percent of real words in a test, but still lets through a third of scrambled words. Rules narrow the field; they do not replace judgement. (Reports 01, 07; test re-run in review.)

**10. What teaching research supports, and its limits.** Short explicit rules followed by practice. Recalling from memory with feedback, spread over days. Practice in each skill separately, because skill in reading transfers only partly to writing. A lot of easy reading in which new words recur. The limits: published effects are inflated, studies of language apps are small or company-run and show beginner-level gains in people who keep going, and all of it comes from natural languages. Computer-taught miniature artificial languages have been learned in experiments, but with a few dozen words. (Reports 09, 10, 12, 15.)

**11. What made other constructed languages last.** Esperanto, Klingon, Na'vi and Toki Pona produced real speakers. Each had one written reference, a known final authority, a core that never changes, and somewhere to use the language. Projects failed through endless reform (Ido), a founder fighting the users over ownership (Volapük, Loglan), or no authority at all (Tolkien's Elvish). (Reports 03, 06, 14.)

**12. The fan hub retreated to canon.** See point 2 of section 0. No licence for its material was found. No other app combines lessons, spaced practice, rune reading and writing offline. (Report 03, from search summaries only; the site refuses automated access and I did not work around that.)

**13. The legal position.** A language as a system is very probably free to teach and extend; no court has ruled on a constructed language. The game's *texts* are ordinary protected writing. No published policy from the rights holder covers a project like this, so it would run on tolerated use, which can be withdrawn. (Report 04. Research, not legal advice.)

---

## 2. What you asked for, and what this design gives you

| You asked for | This design gives | Why | To get exactly what you asked |
|---|---|---|---|
| A thing that can be downloaded and runs standalone, offline, on Android, Mac and Windows | A web app you install from a web page. After the first visit it runs with no connection | It is the only route with no fees, identity checks or security warnings | True installers: free on Windows through the Microsoft Store (identity check); on Android an identity-verified developer account; on Mac 99 dollars a year, or users click through a security warning |
| Free for everyone; you make no money | Yes | | Note: the licences that keep it free also let anyone copy it, change it, or sell copies. That cannot be avoided, because the wiki data requires the same open terms to be passed on |
| Thuum.org's fan expansion built in | Its retired fan vocabulary used as a reference: where one of its words passes the rules, it is adopted with credit instead of coining a rival. Nothing is copied without written permission | The maintainers retired that vocabulary; it has no licence; much of it predates any sound rules | Their permission. I draft the request; you send it. If there is no answer in 30 days the project proceeds without their material and says so |
| People can add words as long as they fit the structure | People can *propose* any word that passes the rules. You ratify | A rule cannot judge whether a meaning is needed or a word is a good fit. Thuum.org's open process produced 6,000 words nobody could maintain | You could ratify everything that passes. I advise against it |
| You are the ultimate authority; nobody can change the rules | True for the official edition. Others may publish a changed copy under another name | Open licences allow copies. Your control is over the official name and releases | A closed licence, which the wiki data's terms rule out |
| Fill the gaps by borrowing from the most similar language | English structure is used where the games are silent, after the games' own patterns | The most similar language is English. Borrowing Old Norse grammar would contradict the games in every sentence | Not advisable |
| Fluency: reading, composing, conversation, role play, script, pronunciation | Checked targets for reading, writing, script and listening. Speaking is practised and self-assessed. Conversation is scripted | No offline program can judge free conversation or score pronunciation in a language with no speakers | Other people. The app prepares learners and provides material for play and correspondence with them |
| New script symbols that look like relatives of the claw marks | Numerals, punctuation and a handwriting style first; fused letter-runes as an optional layer | Every letter already has a rune. Numbers and punctuation are what the script lacks | New letter-runes can be added if you want them; they would have no sound of their own to carry |
| No live AI tutor; rules standalone and offline | Yes | | Note: I would draft lesson texts during development. Nothing in the installed app calls an AI |
| Research at the edge of the field, scholarly sources only | 939 references, machine-checked for existence. Full texts could not be opened in the research environment | Network limits | A second pass with library access before any figure is quoted publicly |

---

## 3. The app

| Part | What the user does |
|---|---|
| **Learn** | A staged course: runes and sounds, first words, reading inscriptions, questions and answers, composing, scripted conversation |
| **Read** | Game texts and graded stories, each word tappable for its meaning, in runes or Latin letters |
| **Forge** | Propose words and see them checked; browse rulings and open gaps |
| **Reference** | Dictionary, grammar, rune converter, pronunciation guide |

Every word, rule and sentence carries a visible label saying where it comes from. A "games only" switch hides everything invented.

---

## 4. The rulebook and the forge

### 4.1 The constitution

A one-page document, published with the app.

1. **Game text is the base and is never contradicted.** Where game text and the strategy guide disagree, game text wins.
2. **Every word has a status, recorded separately for its form and its meaning,** because most meanings are wiki readers' interpretations.

   | Status | Meaning | Who can change it |
   |---|---|---|
   | Game | Attested in game text | Nobody |
   | Official | From the strategy guide or the makers' statements | Nobody |
   | Unconfirmed | From the untraced word list, or with no recorded meaning | You, by ruling on each |
   | Ratified | Approved by you | You, only by retiring it. Form and meaning never change |
   | Trial | Passed the checks, screened by you, awaiting ruling | Its proposer may withdraw it |
   | Local | On one person's device | That person |
   | Fan legacy | From Thuum.org's retired vocabulary, with permission | Reference only |

3. **Checks decide what may be proposed. Only you ratify.**
4. **Use before ratification.** A Trial word needs example sentences that pass the checks. The first founding batch of basic words is exempt, since nothing can be written without them.
5. **Small numbered releases with a public log** of each ruling and your reason. Suggested limit: about 50 new words per release after the founding batch.
6. **Rulings start provisional and are frozen after one release in use.** Freezing too early and reforming endlessly both sank other projects.
7. **Only you can change the rules of the official edition.** Copies made by others must use another name.
8. **Succession.** The project names a second person who can keep it running if you cannot. To be written before first release.

One thing to be plain about: I prepare each ruling with a recommendation, and you are not a linguist. Where you cannot evaluate a ruling, the recommendation becomes the language in practice. The safeguards are that every brief shows the game evidence in full with example sentences for each option, briefs are published, and rulings stay provisional while they are tried.

### 4.2 The rulebook as data

The language is stored as plain files: spelling units, permitted sound patterns, word-building patterns, the dictionary, grammar patterns, and your rulings. One small program reads them. The same program runs in the app and in the project's automated checks, so a word gets the same verdict everywhere.

Each rule carries examples that must pass and examples that must fail. If a rule change would alter the verdict on any existing word or game text, you see that list before approving.

### 4.3 What the word checker tests

1. **Spelling.** Only letters and letter-pairs the language uses.
2. **Sound pattern.** Every syllable must begin, centre and end in a way found in game words. Patterns found in five or more words pass; rarer ones pass with a note; patterns found once or never need your approval. Words of power must be one syllable (all 136 in the games are).
3. **Typicality score.** Advisory only. It cannot reject, because many genuine game words score poorly.
4. **Collisions.** Not identical to any existing word, inflected form or rune spelling. Words one letter apart are listed for information; the games themselves pair related words that way (*jun* "king", *jud* "queen").
5. **Structure.** A compound must name its parts and say which part is the main one. The games use two orders (*Dovahkiin*, "dragon-born"; *Qethsegol*, "bone-of-earth").
6. **Meaning.** Each proposal points to a numbered concept from the project's own list. If the concept has a word already, the proposal must say how it differs.
7. **Route.** Before a new root is allowed, the proposer must try an existing word, a phrase, an extension by analogy (the games have *wo* "who" and *wen* "whose", so question words should follow that series), or a compound.

About 20 existing game words break these tests (rare endings such as *ahrk* "and", apostrophes as in *Thu'um*). They are listed as named exceptions. Proper names are exempt.

Two limits are proposals for you to decide: at most two words per concept, and no new roots for modern or technical concepts.

### 4.4 How a proposal travels

1. A person coins a word in the app. The checker runs on their device.
2. If it passes, the app produces a proposal file and a link that opens a pre-filled submission on GitHub, the public site that hosts the project.
3. An automated check re-runs the same program. It never accepts anything.
4. **You screen it:** one click to confirm the English meaning is acceptable. Until then it is not published and holds no place in the dictionary.
5. Screened proposals enter Trial, labelled, hidden by the "games only" switch. Lessons use Ratified words only.
6. You rule in batches. Each ruling is published with its reason.

Safeguards built in from the start: a limit per contributor, meanings capped in length and shown as plain text, the automated check given the least access it needs, and a test of the whole path with hostile input before it opens.

Submitting needs a free GitHub account, and the submitter's account name is public. A person without one can pass their proposal file to someone who has.

### 4.5 Filling the grammar

For each open area I prepare a brief: what the games show, the options with example sentences, what each does to existing texts, and a recommendation. Sources are consulted in this order:

1. **Game text.** An attested pattern is the default. Where the games show two patterns, both stay valid until you rule.
2. **Analogy inside the language.**
3. **The retired fan vocabulary,** where a word passes the rules and permission exists.
4. **English structure, simplified.** Each such ruling is checked for copying an English quirk the games lack.
5. **Old Norse and Old English patterns,** for word-building and style only.

Word forms are not borrowed from real languages. This is project policy.

For the features the games leave optional (tense, plural, articles, "is"), each ruling states the form the course teaches by default. The checker accepts every form the games allow and never marks one wrong.

Rulings needed, by course stage:

| Before stage | Areas to rule |
|---|---|
| 0 | Sound values; rune spelling; Latin-letter spelling; set phrases |
| 1 | Pronouns; possession; tense; "is"; negation; articles; plural; first verbs |
| 2 | Questions; numbers; "can/must/should"; linking words; the founding batch of missing basic words; rare sound patterns; compound order; word-building suffixes |
| 3 and 4 | Word types for the 642 dictionary entries that state none; authority of meanings; eleven remaining areas |

---

## 5. Teaching design

### 5.1 What "fluent" means here

Three targets the app can check, and one it cannot.

1. **Read** the glossed game texts with the glosses hidden, answering typed comprehension questions.
2. **Write** text that the grammar checker accepts, within the ratified vocabulary.
3. **Understand by ear** words and sentences in the project's pronunciation.
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

Sixteen runes cover 83 percent of inscription text, and five recurring formulas account for 57 of the 64 inscriptions. But a formula is only its opening words: with a well-chosen 100 words about 14 inscriptions are fully readable, and with 300 about 47.

Gates advise; they do not lock. A learner may move ahead.

### 5.3 How each thing is taught

- **Grammar.** One card per pattern: a short rule with game examples, then practice, then production. Most explicit attention goes to the places where an English speaker's habits mislead (*'s*, *-s*, "do not"). The design assumes English-speaking learners.
- **Vocabulary and runes.** Recall from memory with feedback, on a schedule that spaces reviews over days. The scheduling method (called FSRS) is chosen because it is open and well documented. It predicts forgetting well; no trial shows it produces more learning than simpler schedules.
- **Reading.** Graded stories in which most words are known and each new word recurs about ten times. The research does not fix either number. Every authored line is labelled as not from the games.
- **Writing.** Word tiles, then filling slots in game formulas, then free composition. The checker answers "accepted", "this specific error", or "cannot analyse". It checks form, not meaning: a well-formed sentence that says the wrong thing passes.
- **Conversation.** Scripted branching scenes, answered first by choosing a line and later by typing one. The app also produces scene sheets and phrase cards for tabletop play and letters between people.
- **Speed.** An optional timed strand on material already mastered. Nothing is timed by default.
- **Mastery.** An item counts as known after correct recall on three separate days, the last at least a week after the one before. These are starting values.

### 5.4 Minimum workload for a learner

From the scheduler's default of eight new words a day in ten-minute sessions: about twelve weeks to meet all the game words once, and four to five months to reach stage 4's vocabulary for recognition alone, longer for recall. That is card time only, before any reading. These are floors computed from starting values, not promises.

### 5.5 What is left out, and why

No lives, leaderboards, currencies, or streaks that punish a missed day. This is a choice, with a cost: streak incentives do raise persistence in recent studies, and dropping out is the main way self-study fails. The replacement is a weekly target the learner sets, with nothing lost for a missed day. Progress is shown as real capability ("you can read 14 of 64 inscriptions unaided").

The app is built to the WCAG 2.2 AA accessibility standard. Runes are real text with a Latin-letter alternative; nothing depends on colour or dragging alone; typed answers have a tile alternative.

### 5.6 How we find out whether it works

The app sends nothing anywhere, so it cannot report results by itself. Two measures: a small pilot at each build stage with a stated pass mark (for example, three new testers read an unseen inscription with glosses hidden a week after finishing stage 1), and an optional button that saves an anonymous results file a learner can choose to send.

### 5.7 Content

The course needs roughly 45,000 to 65,000 words of graded text and several hundred dialogue lines, about twenty times the game corpus. The estimate rests on one assumed multiplier and could be well off.

I would draft it; the checker would verify form; you would approve. Two cautions. Text drafted this way is untested as reading material in any study. And because this text will dwarf the games', its habits (how often tense is marked, for instance) will in effect set the norm, so it has to follow the rulings exactly.

---

## 6. The script

All 34 runes exist, and every letter the language uses has one. The gaps are numerals and punctuation.

1. **Obtain reference images of the 34 runes and measure them:** strokes, dots, angles. The makers' only description is "three talons plus a dewclaw dot".
2. **Draw an original font from those measurements.** The game's font file is never opened or copied. Letter shapes are not protected in the United States; font files are. This font is needed for the first release.
3. **Derive new signs the way real scripts did:** add or drop a stroke, add a dot, fuse two signs, simplify for speed. Each new sign must differ from every existing one by at least two features.
4. **Order:** digits and sentence marks; a word divider; a handwriting style; fused runes for *th, sh, ng* as an option that never replaces game spelling.

The inscriptions do not spell consistently: the pair *ah* is one rune 225 times and two runes 15 times. Game text is therefore stored rune by rune as written, and the strict spelling rule applies only to new words.

---

## 7. Pronunciation

1. **A written standard that you rule on:** one entry per spelling unit, with a core sound, tolerated variants and the evidence. The app calls it "this project's reading convention".
2. **A listening pass first.** Someone with a copy of the game notes how the voice actors say the disputed sounds. I cannot hear audio.
3. **Reference audio is machine-made at first, and will sound robotic.** It is generated during development from sound-by-sound instructions. Volunteer recordings replace it over time. No game audio is used.
4. **Listening practice with feedback** can be scored offline. Its research support comes from human voices; with synthetic voices it is untested, so it stays provisional until human recordings exist.
5. **Speaking practice** is listen, repeat, record, compare. There is no score. An honest one needs speech models built from native speakers, and none exist.

---

## 8. Platform

A web app made of fixed files, hosted free on GitHub Pages, installed from the browser.

| Device | How it installs | Needs |
|---|---|---|
| Android | Chrome: "Install app" | A current Chrome |
| Windows | Edge or Chrome: "Install" | Windows 10 or 11 |
| Mac | Safari: "Add to Dock" | macOS 14 or later. Current Chrome needs macOS 13 or later |
| iPhone | Safari: "Add to Home Screen" | |

**Your Mac.** Whether it is 64-bit does not matter (every MacBook Pro since 2007 is). What matters is its macOS version. On an older system the app still runs offline in a browser tab but cannot be installed as its own app, and Safari may delete its saved data after a week without use. I need your macOS version before this table is final.

**What the web app route does not give you.**

- The first visit must be online.
- There is no file to hand someone on a memory stick.
- The app and the learner's progress live in the browser's storage, which the browser or the user can clear. The app will ask the browser to protect its storage, prompt for a backup file on a schedule, and offer "restore from backup" on its first screen.
- Progress moves between devices only by that backup file.

**Size.** Text data is under 200 KB compressed. Audio is the bulk, about 25 MB, downloaded separately with an "offline ready" indicator.

**The address must never change.** An installed copy is tied to its web address. Renaming the account or project later would strand every installed copy. The address, and a second person able to recover the account, must be fixed before the first public release.

**None of this has been tested on real devices.** I cannot run Safari or an Android phone; you would do those checks by hand. Section 11 begins with a one-day test for exactly this.

---

## 9. Legal position

Research, not legal advice. Report 04 recommends a lawyer's review of the name, licences and text policy before public release.

- **The language itself** (words, grammar) is very probably free to teach and extend. That is a strong argument, not a settled rule.
- **The game's texts** are the real exposure. They ship as a separate pack that can be removed, always shown with word-by-word analysis and never as bare text. The app must work with that pack absent.
- **No game assets:** no audio, art, screenshots or font files.
- **The name** contains no trademark of the rights holder. One plain line says what the app is, with an "unofficial" notice.
- **The wiki data** is under a Creative Commons licence that requires credit and requires anything built from it to carry the same licence.
- **Thuum.org's material** is not copied without written permission.
- **Tolerated use.** The project has no licence from the rights holder. A complaint could remove the site. The repository, the hosting and the Microsoft Store all belong to the company that owns the game's publisher. Installed copies would keep working; updates and submissions would stop. A written routine for responding to a complaint is part of the first release.

The repository is public now and already holds the wiki snapshot of the game texts, with attribution. The wiki publishes the same texts. I recommend adding the notice and licence files next; you may prefer to make the repository private until then.

---

## 10. What this costs

**Money.** Nothing is required. Optional: Mac installers (99 dollars a year), an Android developer account (25 dollars and identity documents), a web address of your own (roughly 10 to 15 dollars a year, my estimate), which would let the project move hosts without stranding anyone.

**Your time.** Rough estimate, 50 to 125 hours across the build: 34 rulings at 20 to 40 minutes; 350 to 550 word decisions at 5 to 10 minutes; reading the authored texts; the listening pass; testing each release on your devices.

**Dependence on one person.** You are the only one who can rule, and you cannot read the program code you approve. Your real control is the report showing which verdicts a change would alter.

**Dependence on me.** I would write the program, the briefs and the content. That work is limited by your usage allowance: the research alone took three allowance periods. The files are plain and documented so another person or assistant could continue.

---

## 11. Build order

**Before committing: three small tests.**

1. A one-page offline test on GitHub Pages, installed on your actual phone, PC and Mac: switch the network off, leave it ten days, publish an update, clear the browser once, restore from backup.
2. Twenty words rendered as synthetic audio, including the disputed sounds, for you to hear.
3. The submission path run on a throwaway project with hostile input.

| Stage | Delivers | Done when | Needs from you |
|---|---|---|---|
| A. Reader and reference (first public release) | Rune font, rune chart and converter, dictionary with status labels, the 64 inscriptions with every word explained, rune recognition practice, backup and restore | Installs and runs offline on your three devices; an update arrives without losing data; every game word passes the checker or is on the named exception list | Rune reference images; device tests; decisions in section 12 |
| B. Rulings, round one | Briefs and rulings for stages 0 to 2; the founding batch of basic words | Rulebook 1.0 published | Listening pass; your rulings |
| C. Course, first part | Stages 0 and 1; scheduler; first audio; sentence checking at word and pattern level | Pilot testers meet the stage 1 pass mark | Pilot testers |
| D. Forge | Coining, checking, proposal files, automated checks, screening, Trial, ratification, releases | A proposal travels end to end; hostile-input test passes | Screening and rulings |
| E. Course, second part | Stages 2 and 3; full grammar checker; first scenes; graded texts | Pilot testers meet the stage 3 pass mark | Approving texts |
| F. Composition and conversation | Stage 4; numerals and punctuation; human recordings; installers if chosen | Pilot testers complete a scripted scene by typing | |

Stopping after A still leaves a usable reader. Stopping after C leaves a course for runes and first inscriptions.

**Not in the first version:** digitally signed data files, a second copy of the checker in another programming language, outside concept databases, automatic tuning of the review schedule. Each adds upkeep for little gain at this size.

---

## 12. Decisions

### A. Decisions that define the project. Please answer each.

**A1. The constitution in section 4.1.** It makes you the only ratifier. It also binds you: reasons are published, and a ratified word's form and meaning never change. *Recommendation: accept.*

**A2. Licences.** Program code under the GPL (anyone may use and change it; changed versions must stay open). Project-written content and ratified words under Creative Commons Attribution-ShareAlike 4.0. The font under the Open Font License with the name reserved. These cannot be withdrawn later, and they allow others to copy and to sell. The share-alike term is required by the wiki data and is not a free choice. *Recommendation: accept.*

**A3. Words that rest only on the strategy guide (163) or the untraced list (91).** If neither counts, coverage of basic concepts falls from about half to about a third and the forge has more to coin. *Recommendation: guide words count as Official and may be built on; untraced words stay Unconfirmed until you rule on each.*

**A4. The retired fan vocabulary.** *Recommendation: ask permission; where a fan word passes the rules, adopt it with credit; proceed without it after 30 days of silence.* The alternative is to coin independently from the start, which is simpler and loses continuity with what some fans already know.

**A5. Installers and spending.** *Recommendation: web app only for the first release; decide on installers once it exists.*

**A6. The game texts pack.** *Recommendation: include it, removable, always with analysis.* The alternative is a first release with words only and no inscriptions, which is safer and much less useful.

**A7. Names.** A name for the app with no trademarked term, and a name for the invented extension so it never claims to be the official language. *I will bring a shortlist once you tell me the tone you want.*

### B. Defaults you can accept together

- B1. I draft lesson texts and dialogue; the checker verifies form; you approve; all labelled as not from the games.
- B2. Submissions need a free GitHub account, with the file route for those without one.
- B3. A weekly target in place of streaks, lives and leaderboards.
- B4. At most two words per concept; no new roots for modern or technical concepts.
- B5. The items in "not in the first version" stay out.
- B6. The repository stays public, with notice and licence files added next.

### C. Things only you can do

- C1. Tell me the macOS version on your MacBook, and your phone's Android version.
- C2. Send the request to Thuum.org's administrator (I draft it), and read their March 2026 home-page notice to confirm what I could only see second-hand.
- C3. The listening pass: about one to two hours with a checklist I prepare.
- C4. Rune reference images: approve access to the wiki's image server when I ask, or send me a screenshot of the alphabet.
- C5. Name a second person who could recover the project.
- C6. Run the three tests in section 11 on your devices.

---

## 13. How far to trust this

- **Citations.** 939 references were run through a script against the scholarly registry. 685 matched on title, year and first author. None mismatched. 201 are web pages, legal sources and other items a registry cannot check; 42 are books and conference papers it does not hold, most confirmed by search; 11 were confirmed by other means.
- **What was not read.** Full texts could not be opened. Figures come from abstracts, search summaries and the analysts' prior knowledge. In review, 17 sources were re-checked against their abstracts: none was invented, and four had been read more loosely than the source supports; those claims are corrected here.
- **Thuum.org.** Everything said about it comes from search summaries. Confirm it yourself (C2).
- **Game data.** Counts were recomputed from the data files, which come from one wiki snapshot. English meanings are mostly wiki editors' readings. Rune spellings follow the wiki's transcription and were not checked against the game.
- **Platform facts** were checked by search in November 2026 but not on devices. Whether an installed Mac web app is protected from Safari's seven-day deletion could not be confirmed either way.
- **Transfer.** All teaching evidence comes from natural languages.
- **Starting values, not findings:** stage sizes, the content estimate, pass marks, repetition counts, mastery rule, release size, hours.

---

## Words used in this document

| Term | Meaning here |
|---|---|
| Canon, game text | What appears in the games themselves |
| Rulebook | The files that define the language for this project |
| Ruling | Your decision on an open question, recorded with its reason |
| Ratify | Your approval that makes a proposed word part of the language |
| Checker | The program that tests a word or sentence against the rulebook |
| Gloss | The meaning shown for a word |
| Graded text | A story written so that nearly all its words are already known |
| Web app | An app delivered through a browser that can be installed and run offline |
| Repository, GitHub | The public online folder holding the project, and the site that hosts it |
| Open licence | Terms that let anyone use and copy the work under stated conditions |
| Share-alike | A condition that copies and adaptations carry the same licence |
