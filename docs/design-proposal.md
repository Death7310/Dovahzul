# Design proposal: a teaching app and language forge for Dovahzul

Status: draft for the owner's decision. No app code has been written.
Date: 2026-11-14. Evidence: the fifteen reports in `research/` and the data in `research/data/`.

This document says what the research found, where the original plan has to change, what I propose to build, in what order, and which decisions are yours. Section 9 lists those decisions with a recommended answer for each.

---

## 1. What the research found

These are the findings the whole design rests on. Each names the report it comes from.

**1. Canon is a skeleton, not a language you can yet speak.** The game material holds 657 dictionary entries and about 2,400 words of connected text (word walls, dialogue, songs). About half of the roughly 720 distinct word forms occur exactly once. (`research/data/`, reports 01 and 15.)

**2. About half of everyday vocabulary is missing.** Measured against three standard lists of basic concepts used in linguistics, canon covers 47 to 51 percent. There is no word for *what, where, why, how, if, because, me, two, three, hello* or *thank you*. The gaps are in ordinary words, not epic ones. (Report 06; I re-checked the missing words against the dictionary.)

**3. Grammar has 34 undecided areas, seven of which block teaching.** The seven: sound values, numbers, pronouns, possession, tense, questions, core vocabulary. Until someone rules on them, no lesson beyond the first stage can be written. (Report 01, `research/data/grammar-gaps.json`.)

**4. The most similar natural language is modern English.** On 30 standard grammatical features, canon scores 0.82 against English, 0.80 against Afrikaans, 0.62 against Old Norse. In the one canon text that has an independent official English version (the Song of the Dragonborn), word order matches English almost exactly. The designers put invented words into English sentence structure. Old Norse and Old English supplied the *style* (memorial inscriptions, compound names, heroic register), not the grammar. (Report 05. The Old English, Old Norse and Afrikaans scores were coded by one analyst and should be read as approximate.)

**5. Canon departs from English in seven places, and those are the language's identity.** Tense is optional. Articles are optional. Possession uses suffixes (*thuri*, "my overlord"). There is no *'s*. *Ni* ("not") goes before the verb with no "do". Plural is optional. Subjects can be dropped. (Report 05.)

**6. There is no official pronunciation and no usable description of the rune shapes in the data.** Every published sound value is a fan convention. An in-game book itself says an old song lacks "a sure pronunciation". (Reports 01, 08, 11.)

**7. Canon's sound patterns are tight enough to check by rule.** Four in five syllables are consonant-vowel or consonant-vowel-consonant. Clusters such as *tr, bl, fl, gl, pl, sk, sn* never begin a word. A test on held-out canon words showed that hard rules on permitted word beginnings and endings accept 97.5 percent of real canon words and reject two thirds of scrambled ones. Statistical "sounds right" scores were much weaker and can only advise. (Reports 01 and 07.)

**8. What teaching research supports.** Short explicit rules followed by practice where the form decides the meaning. Retrieval practice with feedback, spaced over days. Separate practice for each skill, because reading practice does not produce writing ability. Large amounts of easy reading with words repeated ten or more times. (Reports 09, 10, 15.) The same research is clear about its limits: published effects are inflated, studies of language apps are small or company-run, and no study exists of anyone learning a fictional language from software.

**9. What made other constructed languages last.** Esperanto, Klingon, Na'vi and Toki Pona produced real speakers. All four had one written reference grammar and dictionary, a known final authority, a fixed core that is never changed, productive word-building, and somewhere to use the language. The projects that failed did so through a founder asserting ownership against the users (Volapük, Loglan), endless reform (Ido), or no authority at all (Tolkien's Elvish). (Reports 06, 14.)

**10. A fan standard already exists.** Thuum.org's dictionary holds more than 5,000 words, most invented by its community. Its site refuses automated access and states no licence. (Reports 03, 14.)

**11. The only route that is free on every platform is an installable web app.** Signed installers cost money on macOS (99 US dollars a year) and now carry identity checks on Android. Unsigned installers trigger warnings on all three systems. (Report 13.)

---

## 2. Where the plan has to change

You asked me to point out flaws. There are seven. None of them stops the project.

**1. The forge is not one feature among several. It is the critical path.** Half the basic vocabulary and seven areas of grammar are missing, so the language has to be finished before it can be taught to fluency. Your rulings come first, and lessons are generated from them. The design below is built around that order.

**2. Borrowing structure from the "most similar language" gives less than you hoped.** The most similar language is English, which you already speak. Borrowing its structure where canon is silent is correct and is what canon itself does. Borrowing grammar from Old Norse (case endings, gender, verb agreement) would contradict canon in every sentence. So the rule is: canon first, then analogy inside the language, then English structure, then Old Norse or Old English *patterns* for word-building and style only. Word forms are never borrowed.

**3. "As long as it fits the structure, it can be added" is not enough.** A rule can check that a word sounds right, collides with nothing and is built from approved parts. It cannot check whether the meaning is needed, whether the word is a good fit, or whether a second word for the same thing is justified. Unchecked, a forge produces thousands of near-duplicates. So: rules decide what may be *proposed*; you decide what is *ratified*.

**4. "Nobody else can change the rules" needs a written form, or it will not hold.** In every case studied, the lasting pattern was a fixed core, growth through use, and ratification afterwards. Founders who simply asserted control lost their communities. You are also not the language's creator, so your authority will rest on being transparent and consistent. The remedy is a short written constitution (section 4.1) that makes you the only ratifier and binds you to publish reasons.

**5. Fluency from an app alone is not supported by evidence.** Duolingo's Klingon course had over 400,000 starts; credible estimates of fluent Klingon speakers are in the tens. The app can deliver unaided reading of all canon, rule-correct writing, the script, a consistent pronunciation, and scripted conversation. Open conversation needs other people. The app should prepare learners for that and hand them on, and it should say so.

**6. Offline plus community plus free means no server.** Submissions therefore travel through the public GitHub repository, and progress cannot sync between a learner's devices except by exporting and importing a file.

**7. The largest cost is content, not code.** Teaching to conversation level needs roughly 60,000 words of graded reading text and several hundred dialogue lines, about 24 times the size of canon. That figure is a rough estimate. Someone has to write it. Section 9 asks how.

---

## 3. What the app is

One installable app with four parts that share one rulebook.

| Part | What the learner does |
|---|---|
| **Learn** | Staged course: runes and sounds, words of power, reading word walls, questions and answers, reading all canon, composing, scripted conversation |
| **Read** | Library of canon texts and graded stories with tap-to-gloss, rune and Latin-letter views |
| **Forge** | Propose words, see them checked against the rules, export proposals; browse rulings and the open gaps |
| **Reference** | Dictionary with a status label on every word, grammar, rune converter, pronunciation guide |

Every word, rule and sentence in the app carries a visible status label, so canon and invention are never confused.

---

## 4. The rulebook and the forge

### 4.1 The constitution

A one-page document in the repository, which the app also displays.

1. **Game text is the immutable base.** No ruling may contradict something attested in the games.
2. **Layers.** Every word and rule belongs to one layer:

   | Layer | Meaning | Who can change it |
   |---|---|---|
   | Game | Attested in game text | Nobody |
   | Official | Official guide, developer statements | Nobody; you rule on whether the forge may build on it |
   | Ratified | Approved by you | You, by deprecating; never deleted or given a new meaning |
   | Trial | Passed all automatic checks, in use, awaiting your ruling | Proposer may withdraw |
   | Local | On one person's device | That person |
   | Community pack | Imported fan dictionary, labelled as such | Its own maintainers |

3. **Checks gate, the owner judges.** Automatic checks decide what may be proposed. Only you ratify.
4. **Use before ratification.** A trial word needs example sentences that pass the grammar checker before it can be ratified.
5. **Numbered releases with a public log.** Each ruling records its evidence and your reason.
6. **Only you can change the rules,** enforced by repository permissions, and every rule change is versioned.
7. **Succession.** One sentence naming what happens to the project if you step away.

### 4.2 The rulebook as data

The language is stored as plain data files, not buried in code: spelling units, permitted word beginnings and endings, word-building patterns, the dictionary, grammar patterns, known learner errors, and your rulings. One small rule engine reads those files. The same engine runs inside the app, offline, and in the repository's automated checks, so a word that passes on someone's phone gets the same verdict when submitted.

A rule carries its status, its evidence, examples that must pass and examples that must fail. Those examples run as tests on every change. If a rule change would flip the verdict on any existing word or canon text, the system reports it before you approve.

### 4.3 What the word checker tests

In order, with the first failure reported in plain language:

1. **Spelling.** Only the letters and letter-pairs canon uses; converts cleanly to runes and back.
2. **Sound pattern, hard rules.** The word must begin and end with a pattern attested in canon. Patterns found in five or more canon words pass. Rare ones pass with a note. Patterns found once or never need your override. Words of power must be one syllable.
3. **Sound pattern, advisory score.** How typical the word looks. This never rejects by itself, because one in five genuine canon words would fail it.
4. **Collisions.** Not identical to any existing word, inflected form or rune spelling; flagged if one letter away from a word in the same field.
5. **Structure.** A compound must name its parts, and the parts must be approved words.
6. **Meaning slot.** Each proposal points to a numbered concept. If the concept already has a word, the proposal must say how the new one differs. At most two words per concept.
7. **Word-building route by concept type.** Basic concepts get short new roots. Everything else must first try an existing word, a phrase, an extension of meaning, a compound or an approved affix before a new root is allowed. New roots are barred for modern or technical concepts.

### 4.4 How a proposal travels

1. A person coins a word in the app. The checker runs on their device.
2. If it passes, the app produces a proposal file and a pre-filled submission link to the GitHub repository.
3. The repository's automated check re-runs the same engine. It never accepts anything by itself.
4. Passing proposals enter the Trial layer and appear in the next data release, visibly marked.
5. You rule in batches. Each ruling is published with its reason.
6. The app picks up new releases when it is next online. Offline, it keeps working with what it has.

### 4.5 Filling the grammar

For each of the 34 open areas I prepare a short brief: what canon shows, the options, what each option does to existing texts, and a recommendation using the donor order in section 2. You choose. The ruling becomes a numbered entry in the rulebook that lessons and the checker both read, so a later change regenerates both.

First batch, because everything else waits on it: sound values, spelling norms, part of speech for the 642 untagged dictionary entries, pronouns, possession, tense, questions, numbers, and a closed "conversation kit" of the missing basic words.

---

## 5. Teaching design

### 5.1 Stages

Each stage ends in a task the app can check, not in a self-rating.

| Stage | The learner can | Words | Depends on |
|---|---|---|---|
| 0 | Read and write all 34 runes; say the words of power; use set greetings | about 40 | Sound ruling |
| 1 | Read formula word walls; make first sentences | 100 | Pronouns, possession, tense rulings |
| 2 | Ask and answer questions | 300 | Questions, numbers, conversation kit |
| 3 | Read all canon text unaided | about 650 | Part-of-speech tags |
| 4 | Compose and hold scripted conversation | 1,000 to 1,200 | Ratified vocabulary beyond canon |
| 5 | Contribute to the forge | | Forge open |

Four or five opening formulas cover about nine in ten word walls, and sixteen runes cover 83 percent of wall text, so reading real inscriptions can start early.

### 5.2 How each thing is taught

- **Grammar:** one card per pattern. A rule of about 60 words with canon examples, then items where only the target form separates right from wrong, then production. Explicit teaching time goes to the seven places canon differs from English, since learners will otherwise write English habits (*'s*, *-s* plurals, "do not").
- **Vocabulary and runes:** spaced retrieval using the FSRS scheduling method, with typed answers. Each word gets a recognition card first and a production card later. Grades come from what the learner did, not from self-rating.
- **Reading:** graded stories in which nearly all words are already known, each new word returning about ten times across later texts. Every authored line is labelled as not canon.
- **Writing:** from word tiles, to filling slots in canon formulas, to free composition. The grammar checker returns one of three verdicts: conforms to the rulebook, a specific named error, or "cannot analyse". It never guesses at meaning.
- **Conversation:** branching scripted scenes with five response modes of rising difficulty, from choosing a line to typing one that the checker validates. Scenes are replayed with less support and with roles swapped. The app also exports scene kits for tabletop play and correspondence with other people.
- **Pronunciation:** section 7.
- **Mastery:** a pattern counts as learned only on a test at least seven days after the last practice. Reading, rune reading, writing and speaking are tracked separately.

### 5.3 What the app will not do

No streaks that punish a missed day, no lives, leaderboards, currencies or timed drills by default. The research finds these buy small, fragile gains and that this audience arrives already motivated. Progress is shown as real capability: "you can read 40 of 131 word walls unaided". No claim of time to fluency. Accessibility to the WCAG 2.2 AA standard is a release requirement: runes are real text with a Latin-letter alternative, and nothing depends on colour or dragging alone.

---

## 6. The script

Every Latin letter the language uses already has a rune, so new *letter* symbols have no job to do. The real gaps are **numerals** and **punctuation**: canon has neither, and the official font uses the digit keys for double-vowel runes.

Proposed order:

1. **Measure the 34 canon runes first.** Record each one's strokes, dots and angles. The only official description is "one to three talon scratches, sometimes a dewclaw dot". This step needs the rune images, which are not yet in the data.
2. **Derive new signs the way real scripts did:** add or drop a stroke, add a dot, fuse two signs, simplify for fast writing. Each new sign must differ from every existing one by at least two features and stay within canon's range of complexity.
3. **Release in this order:** digits and sentence marks; then a word divider; then an everyday handwriting style. Fused runes for *th, sh, ng* only as an optional layer that never replaces canon spelling.
4. **Draw original outlines.** The project ships its own font, drawn from measurement, and does not copy or convert the game's font file.

The app offers three display settings: canon only, classical (canon plus digits and punctuation), extended.

---

## 7. Pronunciation

1. **A written standard, owned by you.** One record per spelling unit: a core sound, tolerated variants, and the evidence. The app labels it "this project's reading convention".
2. **A listening pass before you rule.** Someone with a legally owned copy of the game logs how the voice actors say the disputed sounds (*j*, *r*, vowel plus *h*, doubled vowels, stress). I cannot hear audio; this is a task for you or a volunteer.
3. **Reference audio.** Generated when the app is built, from sound-by-sound instructions, in several synthetic voices. Volunteer recordings replace synthetic clips over time under an open licence. No game audio is shipped.
4. **Training.** Listening discrimination with immediate feedback and several voices is the best-supported method and can be scored offline. Speaking practice is listen, shadow, record, compare, and check against a list.
5. **No pronunciation score.** Honest automatic scoring needs speech models trained on native speakers, and none exist for this language. The app shows the learner's recording beside the reference and says plainly that it is a comparison, not a grade.

---

## 8. Platform, delivery and legal posture

### 8.1 Platform

A static, installable web app, hosted free on GitHub Pages.

- **Install:** open the site once, choose "install". After that it runs with no connection on Android, macOS, Windows, and also iPhone and Linux.
- **Your Mac:** every MacBook Pro since 2007 is 64-bit, and this route does not depend on it either way.
- **Data:** the full dictionary is a few kilobytes compressed. Progress is stored on the device. There are no accounts and no tracking. A one-file export and import moves progress between devices.
- **Updates:** fetched when the device is next online.
- **Native installers later, if wanted.** A free Microsoft Store listing is the cleanest Windows route. macOS installers without a paid Apple account show a security warning. Android installers face Google's new developer identity checks.

Technology: TypeScript, a small interface framework, a service worker for offline use, and one rule engine shared by the app and the repository checks.

### 8.2 Legal posture

*This section will be completed from report 04 and is not legal advice.*

- The project is unofficial and says so. It uses no game audio, art or font files.
- Wiki-derived data comes from the UESP under a Creative Commons Attribution-ShareAlike licence, which requires attribution and requires the derived data to carry the same kind of licence.
- Forge contributions are licensed openly at submission so that nobody, including a later maintainer, can close them off.
- Thuum.org's dictionary is included only with its maintainers' permission, as a labelled community pack.

---

## 9. Decisions that are yours

Each has my recommendation. Reply "tap" to accept all recommendations, or name the numbers you want to change.

| # | Decision | Recommendation |
|---|---|---|
| 1 | Accept the constitution in section 4.1 as the governance model | Yes |
| 2 | Status of words that rest only on the official guide (166) or only on the dictionary hosted by a fan archive (91) | Guide words: Official layer, usable as building parts. Archive-only words: held as unconfirmed until traced |
| 3 | Relationship to Thuum.org's existing fan vocabulary | Ask permission; where their word for a concept passes the rules, prefer it over coining a rival |
| 4 | Who writes the graded stories and dialogue | I draft them during development, the rule engine checks every line, you approve, and all are labelled non-canon. The app itself stays free of any live AI |
| 5 | Submission channel | A free GitHub account for submitters in the first version, plus a proposal file that anyone can pass on |
| 6 | Licences | Code under an open-source licence that keeps derivatives open; data under Creative Commons Attribution-ShareAlike |
| 7 | First release as an installable web app only | Yes; native installers after the course exists |
| 8 | A name for the forged variety, so it does not claim to be the official language | You choose; avoid the game's trademarks in the app's name |
| 9 | Who does the pronunciation listening pass | You or a volunteer, using a short checklist I prepare |

Two things I need from you whatever you decide: written permission from Thuum.org's administrators together with their downloadable dictionary file, and the version of macOS on your MacBook.

---

## 10. Build order

Each stage ends with something you can install and test.

| Stage | Delivers | Done when |
|---|---|---|
| A. Foundations | Rulebook format, rule engine, rune converter, canon data pack, installable app shell with dictionary and reference | Installs and runs offline on all three systems; every canon word passes the checker; every canon wall text converts to runes and back |
| B. Rulings, round one | Briefs and your rulings on the first batch in section 4.5 | Rulebook version 1.0 published |
| C. Learn, first part | Stages 0 and 1: runes, sounds, words of power, word-wall formulas, first sentences, scheduler, delayed tests | A new learner goes from nothing to reading formula word walls |
| D. Forge | In-app coining and checking, proposal export, repository checks, trial layer, ratification, numbered releases | A proposal travels end to end and appears in a release |
| E. Learn, second part | Stages 2 and 3: questions, full canon reading, grammar checker, first dialogue scenes | A learner reads all canon unaided |
| F. Composition and conversation | Stage 4, script extensions, human recordings, optional native installers | Scripted conversation within ratified vocabulary |

B runs alongside A, since it is a conversation between us and needs no code.

---

## 11. How far to trust this

- **Citations.** Every reference list was checked by script against the scholarly registry. Of the first 797 references, 648 matched on title, year and author; none mismatched. The rest are books, web pages and conference papers the registry does not hold.
- **What was not read.** Full texts could not be fetched in the research environment. Figures come from abstracts, search summaries and the analysts' prior knowledge, and each report marks which are which. Before any figure is quoted publicly it should be checked against the paper.
- **Canon data.** Counts in this document were recomputed from the data files. English meanings of most canon texts are wiki editors' readings, not game text.
- **Transfer.** All teaching evidence comes from natural languages. Its application to a constructed language with 650 words is inference. The app should log its own delayed-test results so the design can be corrected by its own data.
- **Numbers that are starting values, not findings:** stage sizes, the 60,000-word content estimate, pass thresholds, repetition counts, the seven-day delay.
