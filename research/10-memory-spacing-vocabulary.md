# Track 10: Memory science and vocabulary acquisition, down to the algorithm

† marks a figure recalled from the cited source and not re-read this session (full texts could not be fetched). Unmarked figures were confirmed in search-result text, the registry, Track 9 or the repository data. "Inference" marks my reasoning. Depth: a, b and the specification in full; c moderately; d and e briefly, because Track 9 covers grammar practice and session-design evidence is thin.

## 1. Bottom line

- **Schedule every item with FSRS-6** (defaults in 3.2), desired retention 0.90, behind a scheduler interface. It alone combines a peer-reviewed lineage (Ye et al. 2022; Su et al. 2023), a recall-probability output, usable defaults for a learner with no history, and small open ports. Its proven edge is predictive; no randomised trial shows it yields more learning than SM-2.
- **Every exposure after the first is a recall attempt followed by the answer.** Testing beats restudy by g = 0.50 (Rowland 2014); spaced beats massed retrieval by g = 0.74 (Latimier et al. 2021).
- **Do not claim optimal intervals.** Expanding and equal spacing do not differ (g = 0.034, Latimier et al. 2021). What matters is gaps of days to weeks and relearning to criterion on several separate days (Rawson & Dunlosky 2011).
- **Two cards per word, receptive first, productive unlocked later, typed recall.** The direction practised is the direction learned (Webb 2009).
- **Cards are one strand.** Deliberate study leaves 39.4% (meaning) and 25.1% (form) of words on delayed tests (Webb et al. 2020) and teaches little about use (Nation 2007).
- **Separate confusable words at first, contrast them later.** Semantic sets do not hurt posttests (g = 0.01) but slow learning to criterion (Li et al. 2026).
- **Short daily sessions, one mixed queue, new items throttled by review load, no penalty for a missed day.**
- **Log every review with its predicted recall,** so calibration can be checked and parameters refitted on the device.

## 2. Findings by sub-question

### a. Spacing and retrieval practice

**Spacing.** Across 317† experiments spaced study beats massed at every retention interval, and the best gap grows with the interval (Cepeda et al. 2006). With tests up to a year out, the optimal gap falls from about 20 to 40%† of a one-week delay to 5 to 10%† of a one-year delay, and too short a gap costs more than too long (Cepeda et al. 2008). An online replication with L2 vocabulary found the effect, with scores 10 to 20% below the laboratory original (Rogers et al. 2025). In L2 learning, spacing has medium-to-large effects across 48 experiments, longer gaps win only on delayed tests, and equal and expanding schedules do not differ (Kim & Webb 2022). Over years, 13 relearning sessions 56 days apart matched 26 sessions 14 days apart† (Bahrick et al. 1993).

**Retrieval practice.** Testing versus restudy gives g = 0.50, more for recall than recognition and more with feedback (Rowland 2014); g = 0.61† against all comparison conditions (Adesope et al. 2017); g = 0.499† in 222† classroom studies (Yang et al. 2021). Transfer beyond practised items is smaller, d = 0.40† (Pan & Rickard 2018). The classic demonstrations used foreign vocabulary: repeated retrieval gave about 80%† recall after a week against about 35%† without it (Karpicke & Roediger 2008; Roediger & Karpicke 2006). Practice testing and distributed practice are the two techniques rated high utility (Dunlosky et al. 2013; reviewed by Carpenter et al. 2022).

**Expanding versus equal.** Expanding schedules raise early success, but equal spacing matched or beat them at a delay (Karpicke & Roediger 2007); absolute spacing, not its pattern, drove retention (Karpicke & Bauernschmidt 2011); the two were equivalent after four weeks (Kang et al. 2014); in L2 vocabulary the expanding advantage was small (Nakata 2015a). Pooled, the difference is null (Latimier et al. 2021).

**Successive relearning and criterion.** Retrieve to criterion, then relearn to criterion on later days. Rawson & Dunlosky (2011) recommend three correct recalls initially and three relearning sessions†, and show that relearning washes out most of the initial-criterion effect; classroom trials confirm the gains (Rawson et al. 2013; Rawson & Dunlosky 2022). Harder successful retrievals are worth more, with diminishing returns to extra correct recalls (Pyc & Rawson 2009; Nakata 2017 for L2 words); overlearning in one sitting fades within weeks (Rohrer et al. 2005).

**Feedback.** The correct answer after an error multiplied final retention about fivefold (494%†); feedback after correct answers added little (Pashler et al. 2005). Delayed feedback beat immediate on multiple-choice material (Butler et al. 2007), but timing made little difference for L2 vocabulary (Nakata 2015b).

**Pretesting.** Guessing before being told helps memory for the guessed item, including meanings of unknown words, if feedback follows (Kornell et al. 2009; Potts & Shanks 2014). The benefit is item-specific and mostly laboratory evidence (Pan & Carpenter 2023).

**Interleaving and desirable difficulties.** Interleaving helps discrimination among similar categories (overall g = 0.42†) and hurts for word lists (g = -0.39†) (Brunmair & Richter 2019). For grammar it helps on delayed tests after a blocked introduction (Pan et al. 2019; Nakata & Suzuki 2019a). Conditions that depress training performance often raise retention (Soderstrom & Bjork 2015), and learners misjudge this: spacing won for 90%† of learners while 72%† believed massing worked better (Kornell 2009).

### b. Scheduling algorithms

| Scheduler | Model and output | Data needed | Evidence |
|---|---|---|---|
| Leitner boxes | promote or demote; no probability | none | analysed as a queueing network (Reddy et al. 2016) |
| SM-2 (Wozniak 1990) | I(1)=1, I(2)=6, I(n)=I(n-1)·EF; EF starts 2.5, floor 1.3; a grade below 3 restarts; no probability | none | one author's own data |
| Half-life regression | p = 2^(-Δ/h), h from log-linear features | training corpus | error 45%†+ below Leitner; 12%† engagement gain; no learning outcome (Settles & Meeder 2016) |
| MEMORIZE | point process with optimal control; review rate proportional to 1 - recall | fitted forgetting rates | natural experiment on app logs (Tabibian et al. 2019) |
| ACT-R family, DASH | activation decay per learner and item; probability | per-learner fitting | laboratory and classroom experiments (Pavlik & Anderson 2005, 2008; Lindsey et al. 2014) |
| SSP-MMC, FSRS | difficulty, stability, retrievability; probability and interval | none with defaults; own log to refit | Ye et al. 2022; Su et al. 2023; open benchmark |

**What experiments support.** Adaptive, model-based scheduling beats fixed schedules: personalised review raised end-of-semester retention 16.5%† over massed and 10.0%† over generic spaced review (Lindsey et al. 2014); response-time-adaptive scheduling beat fixed expanding and equal schedules (Mettler et al. 2016); tracking each item against an efficiency threshold beat conventional schedules once time costs were counted (Eglington & Pavlik 2020); a large randomised trial in a commercial app found machine-learned item selection improved memorisation (Upadhyay et al. 2021). Competing models can fit the same data and disagree about the best schedule (Walsh et al. 2018). A learner's forgetting rate is stable over time but differs by material (Sense et al. 2016), and difficulty priors from earlier learners ease the cold start (van der Velde et al. 2021).

**FSRS.** The model descends from the two-component account of memory, retrievability and stability (Wozniak & Gorzelanczyk 1994; Wozniak et al. 1995), plus item difficulty. Su et al. (2023) fitted these dynamics to a commercial vocabulary app's logs; Ye et al. (2022) derived cost-minimising schedules from them. FSRS-6 uses a power forgetting curve, the form the data favour (Wixted & Ebbesen 1991), with trainable decay. The developers' open benchmark (reproducible, not peer-reviewed) on about 10,000† Anki users reports for FSRS-6 log loss 0.3460, RMSE(bins) 0.0653 and AUC 0.7034, against 0.4694, 0.1275 and 0.6369 for half-life regression; its August 2025 table gave original SM-2 0.722, 0.203 and 0.603, though SM-2 emits no probability and had to be converted (srs-benchmark 2026). Ports exist in TypeScript, Python, Rust, Go and Kotlin (FSRS repository 2026). The optimiser needed 1,000 reviews in early Anki releases, 400 in 24.04 and none since 24.06 (FSRS4Anki documentation, via search). FSRS-7 (34 parameters, two memory traces, sub-day intervals) appeared in 2026; ts-fsrs 6.0.0 defaults to it and keeps FSRS-6 selectable (ts-fsrs 2026). In the one independent comparison found, a 27-learner study, a neural content-aware scheduler matched FSRS on accuracy (Shu et al. 2024); it needs a language model, so it is out of scope.

**Recommendation: FSRS-6.** Leitner and SM-2 give no probability, so they cannot be calibrated, simulated or personalised. Half-life regression and MEMORIZE need a trained population model the project lacks. ACT-R-family models need per-learner fitting and have no maintained offline library. FSRS-6 ships population defaults, is small enough to port and test by hand, and refits from the local log. FSRS-7 is too new to pin (inference).

### c. Vocabulary learning

- **Deliberate versus incidental.** Incidental uptake is 9 to 18% of target words on immediate tests (Webb et al. 2023) and correlates r = .34 with encounters, with no threshold count (Uchihara et al. 2019). Deliberate study yields far more per word but decays to 39.4% (meaning recall) and 25.1% (form recall) on delayed tests; flashcards ranked highest on immediate meaning recall among four activities (Webb et al. 2020, 22 studies). Deliberately learned words do enter the working lexicon, producing form and semantic priming (Elgort 2011); spaced contextual encounters built explicit but not tacit knowledge (Nakata & Elgort 2021).
- **Involvement load.** Need, search and evaluation (Laufer & Hulstijn 2001) explain about 29%† of variance in immediate learning; evaluation carries most weight and search none (Yanagisawa & Webb 2021); adding frequency, mode and test format predicts better (Yanagisawa & Webb 2022). Technique feature analysis, which also scores retrieval, generation and interference, out-predicted it in one study (Hu & Nassaji 2016; Nation 2022).
- **Direction.** Receptive practice yields receptive knowledge and productive practice productive knowledge; productive practice transfers better (Griffin & Harley 1996; Mondria & Wiersma 2004; Webb 2009). Difficulty runs form recall > meaning recall > form recognition > meaning recognition (Laufer & Goldstein 2004). Software should move from recognition to recall and from receptive to productive (Nakata 2011).
- **Glosses.** Glossed reading beats unglossed (45.3%† against 26.6%† immediately), and L1 glosses beat L2 glosses (Yanagisawa et al. 2020; Kim et al. 2024; Laufer & Shmueli 1997). Dovahzul has no monolingual dictionary, so translation is the only option anyway.
- **Mnemonics.** The keyword method gives large immediate gains (Atkinson & Raugh 1975) that fade faster than rote-learned pairs (Wang & Thomas 1995); it is rated low utility (Dunlosky et al. 2013). One study found mnemonics cut interference in semantic sets (Sarıoğlu & Karatepe 2024).
- **Word knowledge and multiword units.** Knowing a word spans form, meaning and use, receptive and productive (Nation 2022); cards reach little of use. Formulaic sequences are retained when deliberately targeted, poorly from exposure alone (Boers & Lindstromberg 2012).
- **Semantic sets.** Early studies found related sets needed more trials (Tinkham 1993; Waring 1997). Nakata & Suzuki (2019b) found more cross-association errors but no reliable posttest cost, and summarise earlier posttest effects at -0.24, 95% CI [-0.71, 0.23]. Li et al. (2026; 21 studies) find g = 0.01 [-0.25, 0.26] on immediate posttests, with all 13 trials-to-criterion effects negative.
- **Formats that teach.** Recall teaches more than recognition (Rowland 2014). Multiple choice teaches, but can plant a lure as knowledge (Roediger & Marsh 2005; Little et al. 2012). Retrieving during learning beats copying or repeating aloud (Barcroft 2007; Kang et al. 2013).

### d. Beyond single words (brief)

**Grammar.** Spacing is less consistent here: a 14-day† gap beat a 3-day† gap on a long-term test (Bird 2010); massed practice was as accurate as distributed and possibly faster (Suzuki & DeKeyser 2017); 3.5-day and 7-day gaps were about equal for children (Kasprowicz et al. 2019). Retrieval practice transfers only moderately to non-identical items (Pan & Rickard 2018), so a card that repeats one sentence trains that sentence. Inference: schedule the pattern, vary the exemplar.

**Script.** Adults learning an unfamiliar alphabet (N = 42†) learned letters faster and transferred better to reading and spelling after handwriting than after typing or watching (Wiley & Rapp 2021).

**Cloze cards and limits.** Gap-fill ranked below flashcards for the form-meaning link (Webb et al. 2020); other evidence on sentence cards is thin. Deliberate study should be about a quarter of a balanced programme (Nation 2007). In a semester course, use of a spaced-repetition app predicted gains, but students disliked it and compliance was low (Seibert Hanson & Brown 2020).

### e. Session design (brief)

No experiment fixes a session length or new-item rate; these are workload decisions. Large mixed sets are at least as good as small blocks because they create spacing (Nakata & Webb 2016; Kornell 2009). Learners left to decide drop cards too early (Kornell & Bjork 2008). The same time spread over days beats one sitting (Cepeda et al. 2006; Kim & Webb 2022). Habit automaticity took a median 66† days (range 18 to 254†), and one missed day did not matter (Lally et al. 2010). Leech thresholds are software convention, not research.

## 3. What this means for the app

### 3.1 Items and cards

Counts are from the repository's UESP snapshot: word forms and word-wall text are canon; most glosses on dialogue and names are wiki editors' readings (semi-canon).

| Item type | Source in the data | Cards |
|---|---|---|
| Rune | 34 runes used by the language (25 single-letter, 9 two-letter); the unused C and the font-only glyph are excluded | R: rune to Latin, typed. P: Latin to rune, pick then trace. Decode: rune word to transliteration |
| Word | 657 dictionary entries; only 15 carry a part-of-speech tag, so tags must be added before any card depends on them | R: Dovahzul to meaning, typed against an accepted-answer list. P: English to Dovahzul, typed |
| Chunk | 29 phrases, 67 shouts | R and P as for words |
| Sentence cloze | canon lines (131 word-wall, 6 song, 269 dialogue records) | one known word blanked, translation shown; released only when every other word in the line is in review |
| Pattern | grammar rules from Track 1 | scheduler state sits on the pattern; each review draws a different exemplar from a pool of at least 6 |

Rules, with confidence:

1. Typed recall by default; multiple choice only for first exposure to runes, with visually similar lures. [high: Rowland 2014; Roediger & Marsh 2005]
2. First exposure is guess-then-reveal. [medium: Potts & Shanks 2014]
3. The P card unlocks after two consecutive correct R reviews on different days; sibling cards never share a session. [medium: Nakata 2011; Webb 2009; separation is inference]
4. The answer is shown after every attempt; an error brings the item back later in the session. [high: Pashler et al. 2005]
5. No two new items in a session from one semantic field or within edit distance 1; when both reach 7 days' stability, schedule one contrast drill. [medium: Li et al. 2026; Brunmair & Richter 2019]
6. Rune P cards require tracing. [medium: Wiley & Rapp 2021, extended from pen to finger by inference]
7. No audio cards until a sourced pronunciation guide exists.

### 3.2 Scheduler

FSRS-6; state per card {D, S, last_review}; grades 1 Again, 2 Hard, 3 Good, 4 Easy. Formulas are restated from the project's algorithm notes†: port from a pinned reference implementation and test against its vectors, not from this page.

- Retrievability: R(t) = (1 + F·t/S)^(-w20), with F = 0.9^(-1/w20) - 1. Interval for desired retention r: I = (S/F)·(r^(-1/w20) - 1).
- First grade: S0 = w[G-1]; D0 = w4 - e^(w5·(G-1)) + 1, clamped to 1..10.
- Difficulty: D' = D - w6·(G-3)·(10-D)/9, then D'' = w7·D0(4) + (1-w7)·D'.
- Recall: S' = S·(1 + e^w8·(11-D)·S^(-w9)·(e^(w10·(1-R)) - 1)·h·b), with h = w15 on Hard, b = w16 on Easy, otherwise 1.
- Lapse: S' = min(S, w11·D^(-w12)·((S+1)^w13 - 1)·e^(w14·(1-R))).
- Same-day review: S' = S·e^(w17·(G-3+w18))·S^(-w19).

Default w0 to w20 (srs-benchmark 2026; fsrs4anki 2026):
`0.212, 1.2931, 2.3065, 8.2956, 6.4133, 0.8334, 3.0194, 0.001, 1.8722, 0.1666, 0.796, 1.4835, 0.0614, 0.2629, 1.6483, 0.6014, 1.8729, 0.5425, 0.0912, 0.0658, 0.1542`

Settings:

- **Desired retention 0.90**, user range 0.80 to 0.95. With default w20, intervals relative to 0.90 are 0.40 times at 0.95, 1.91 times at 0.85 and 3.32 times at 0.80 (computed here). First intervals at 0.90: about 1.3 days after Hard, 2.3 after Good, 8.3 after Easy. [medium: the FSRS documentation finds a per-user optimum by simulation (FSRS wiki 2026); high success rates are efficient once failure time is counted (Eglington & Pavlik 2020)]
- **Maximum interval 365 days**; 5% interval fuzz. [low: convention]
- **In-session steps.** First graded retrieval after at least 3 other items; that grade sets S0 and D0. Repeat after at least 8 other items until 2 correct recalls in the session (Again resets the count), using the same-day update. [medium: Rawson & Dunlosky 2011; 2 rather than 3 because relearning overrides the initial criterion and extra same-session recalls show diminishing returns (Nakata 2017)]
- **Derived grades.** Wrong is Again; correct with a hint or one-edit typo is Hard; correct is Good; Easy only for a correct first-ever guess. Log response time, which carries scheduling signal (Mettler et al. 2016). [low: inference]
- **Overdue cards** are graded with their real elapsed time; nothing resets after an absence.

Personalisation on the device:

1. No reviews: defaults.
2. From 400 first-interval reviews: refit only w0 to w3 by one-dimensional log-loss minimisation per first grade, shrunk toward defaults by sample size. This also corrects for derived grades differing from the self-rated grades behind the defaults. [medium: inference from the optimiser's staging]
3. From 1,000 reviews: full gradient-descent refit in a background worker, accepted only if log loss on the newest 20% of reviews improves. [medium]
4. Always: plot predicted against observed recall in ten bins; flag RMSE(bins) above 0.05 after 1,000 reviews. [threshold is inference]

### 3.3 Sessions and workload

- One mixed queue: due cards in ascending predicted recall, then new items, in-session repeats interleaved. [medium: Nakata & Webb 2016; ordering is inference]
- Defaults: 10 minutes or 60 reviews, up to 8 new items. new_today = min(8, floor((60 - due_today)/6)); the 6 stands for a new item's first-month review cost and is replaced by the measured value after 30 days of log. [low: inference]
- At 8 a day the 657 canon words are introduced receptively in about 12 weeks; show that projection before the learner changes the rate.
- Leech: 4 lapses in the last 8 reviews, or 8 in all. The card leaves the queue for a re-encoding screen (nearest neighbours by spelling and meaning, a free-text mnemonic field) and re-enters as new next day. [low: convention; Sarıoğlu & Karatepe 2024]
- Streaks count days with one completed review; a missed day carries no penalty. [medium: Lally et al. 2010]
- Graduation: "known (receptive)" at R-card S of 21 days; "known (productive)" at P-card S of 21 days; "mastered" when both reach 90. Reading and composing lessons unlock on receptive status, since cards do not build use (Nation 2007). [thresholds are inference]

### 3.4 Local log

One row per review: card_id, item_id, item_type, direction, timestamp, session_id, position, state_before, elapsed_days, scheduled_days, R_predicted, D_before, S_before, grade, correct, response_ms, typed_answer, edit_distance, confused_with (item id when the answer matched another entry), hint_used, exemplar_id, D_after, S_after, scheduler_version, parameter_set_id.

Derived metrics: true retention by item type, direction and stability band; log loss and RMSE(bins); reviews and minutes per day; new items per day; lapse rate; leech count; items at S of 21 and 90 days; days studied in the last 30; confusion pairs. Everything stays on the device and exports as JSON.

## 4. Contested or weak evidence

- **FSRS against SM-2 on learning** is untested by randomised trial. The benchmark is run by FSRS's developers on self-selected Anki users, and SM-2's log loss partly reflects a conversion it was never designed for.
- **Precise intervals.** The ridgeline (Cepeda et al. 2008) comes from one relearning session with factual material; it licenses no gap formula for repeated relearning.
- **Target difficulty.** Harder retrievals are more potent (Pyc & Rawson 2009), yet high success is more efficient per minute (Eglington & Pavlik 2020); 0.90 is convention.
- **Test format.** Rowland (2014) and Adesope et al. (2017) disagree on whether short-answer or multiple-choice practice gives the larger effect.
- **Semantic sets.** The pooled posttest effect is null with a wide interval (Li et al. 2026).
- **Keyword mnemonics** are strong immediately and disputed at a delay.
- **Industry evidence.** Half-life regression and MEMORIZE were evaluated on company logs; the one A/B test measured engagement (Settles & Meeder 2016).
- **Engineering defaults.** The two-correct criterion, derived grades, session size, new-item formula, leech and graduation thresholds are defaults to tune, not findings.

## 5. Gaps, and anything that was blocked

- No study covers spaced retrieval for a constructed language, adult touch tracing of a 34-rune script, or a 657-headword lexicon.
- No peer-reviewed validation of FSRS-6 or FSRS-7 as such exists; FSRS-7's benchmark rows were cut off in search results.
- WebFetch was unavailable: † figures and the FSRS formulas were not re-read at source, and the default vector and benchmark figures were confirmed only through search-result text.
- One search found no pooled effect size for the keyword method.
- The data lacks a pronunciation guide, rune images and nearly all part-of-speech tags, so audio, rune-image and tag-dependent cards wait on other tracks.

## 6. References

Checked with tools/research/check_refs.py; final result: manual: 6, verified: 92. The six manual entries are web sources whose URLs appeared in search results.

- Adesope, O. O.; Trevisan, D. A.; Sundararajan, N. (2017). Rethinking the use of tests: A meta-analysis of practice testing. *Review of Educational Research*. https://doi.org/10.3102/0034654316689306
- Atkinson, R. C.; Raugh, M. R. (1975). An application of the mnemonic keyword method to the acquisition of a Russian vocabulary. *Journal of Experimental Psychology: Human Learning and Memory*. https://doi.org/10.1037/0278-7393.1.2.126
- Bahrick, H. P.; Bahrick, L. E.; Bahrick, A. S.; Bahrick, P. E. (1993). Maintenance of foreign language vocabulary and the spacing effect. *Psychological Science*. https://doi.org/10.1111/j.1467-9280.1993.tb00571.x
- Barcroft, J. (2007). Effects of opportunities for word retrieval during second language vocabulary learning. *Language Learning*. https://doi.org/10.1111/j.1467-9922.2007.00398.x
- Bird, S. (2010). Effects of distributed practice on the acquisition of second language English syntax. *Applied Psycholinguistics*. https://doi.org/10.1017/s0142716410000172
- Boers, F.; Lindstromberg, S. (2012). Experimental and intervention studies on formulaic sequences in a second language. *Annual Review of Applied Linguistics*. https://doi.org/10.1017/S0267190512000050
- Brunmair, M.; Richter, T. (2019). Similarity matters: A meta-analysis of interleaved learning and its moderators. *Psychological Bulletin*. https://doi.org/10.1037/bul0000209
- Butler, A. C.; Karpicke, J. D.; Roediger, H. L. (2007). The effect of type and timing of feedback on learning from multiple-choice tests. *Journal of Experimental Psychology: Applied*. https://doi.org/10.1037/1076-898X.13.4.273
- Carpenter, S. K.; Pan, S. C.; Butler, A. C. (2022). The science of effective learning with spacing and retrieval practice. *Nature Reviews Psychology*. https://doi.org/10.1038/s44159-022-00089-1
- Cepeda, N. J.; Pashler, H.; Vul, E.; Wixted, J. T.; Rohrer, D. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin*. https://doi.org/10.1037/0033-2909.132.3.354
- Cepeda, N. J.; Vul, E.; Rohrer, D.; Wixted, J. T.; Pashler, H. (2008). Spacing effects in learning: A temporal ridgeline of optimal retention. *Psychological Science*. https://doi.org/10.1111/j.1467-9280.2008.02209.x
- Dunlosky, J.; Rawson, K. A.; Marsh, E. J.; Nathan, M. J.; Willingham, D. T. (2013). Improving students' learning with effective learning techniques: Promising directions from cognitive and educational psychology. *Psychological Science in the Public Interest*. https://doi.org/10.1177/1529100612453266
- Eglington, L. G.; Pavlik, P. I. (2020). Optimizing practice scheduling requires quantitative tracking of individual item performance. *npj Science of Learning*. https://doi.org/10.1038/s41539-020-00074-4
- Elgort, I. (2011). Deliberate learning and vocabulary acquisition in a second language. *Language Learning*. https://doi.org/10.1111/j.1467-9922.2010.00613.x
- open-spaced-repetition (Ye, J.; contributors) (2026). free-spaced-repetition-scheduler: A spaced repetition algorithm based on DSR model. *GitHub repository*. https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler [cited as FSRS repository 2026]
- open-spaced-repetition (Ye, J.; contributors) (2026). The optimal retention. *fsrs4anki wiki, GitHub*. https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-optimal-retention [cited as FSRS wiki 2026]
- open-spaced-repetition (Ye, J.; contributors) (2026). fsrs4anki: fsrs4anki_scheduler.js (reference scheduler with FSRS-6 default parameters). *GitHub repository*. https://github.com/open-spaced-repetition/fsrs4anki/blob/main/fsrs4anki_scheduler.js [cited as fsrs4anki 2026]
- Griffin, G.; Harley, T. A. (1996). List learning of second language vocabulary. *Applied Psycholinguistics*. https://doi.org/10.1017/S0142716400008195
- Hu, H. M.; Nassaji, H. (2016). Effective vocabulary learning tasks: Involvement Load Hypothesis versus Technique Feature Analysis. *System*. https://doi.org/10.1016/j.system.2015.11.001
- Kang, S. H. K.; Gollan, T. H.; Pashler, H. (2013). Don't just repeat after me: Retrieval practice is better than imitation for foreign vocabulary learning. *Psychonomic Bulletin & Review*. https://doi.org/10.3758/s13423-013-0450-z
- Kang, S. H. K.; Lindsey, R. V.; Mozer, M. C.; Pashler, H. (2014). Retrieval practice over the long term: Should spacing be expanding or equal-interval? *Psychonomic Bulletin & Review*. https://doi.org/10.3758/s13423-014-0636-z
- Karpicke, J. D.; Bauernschmidt, A. (2011). Spaced retrieval: Absolute spacing enhances learning regardless of relative spacing. *Journal of Experimental Psychology: Learning, Memory, and Cognition*. https://doi.org/10.1037/a0023436
- Karpicke, J. D.; Roediger, H. L. (2007). Expanding retrieval practice promotes short-term retention, but equally spaced retrieval enhances long-term retention. *Journal of Experimental Psychology: Learning, Memory, and Cognition*. https://doi.org/10.1037/0278-7393.33.4.704
- Karpicke, J. D.; Roediger, H. L. (2008). The critical importance of retrieval for learning. *Science*. https://doi.org/10.1126/science.1152408
- Kasprowicz, R. E.; Marsden, E.; Sephton, N. (2019). Investigating distribution of practice effects for the learning of foreign language verb morphology in the young learner classroom. *The Modern Language Journal*. https://doi.org/10.1111/modl.12586
- Kim, S. K.; Webb, S. (2022). The effects of spaced practice on second language learning: A meta-analysis. *Language Learning*. https://doi.org/10.1111/lang.12479
- Kim, H. S.; Lee, J. H.; Lee, H. (2024). The relative effects of L1 and L2 glosses on L2 learning: A meta-analysis. *Language Teaching Research*. https://doi.org/10.1177/1362168820981394
- Kornell, N.; Bjork, R. A. (2008). Optimising self-regulated study: The benefits—and costs—of dropping flashcards. *Memory*. https://doi.org/10.1080/09658210701763899
- Kornell, N. (2009). Optimising learning using flashcards: Spacing is more effective than cramming. *Applied Cognitive Psychology*. https://doi.org/10.1002/acp.1537 [cited as Kornell 2009]
- Kornell, N.; Hays, M. J.; Bjork, R. A. (2009). Unsuccessful retrieval attempts enhance subsequent learning. *Journal of Experimental Psychology: Learning, Memory, and Cognition*. https://doi.org/10.1037/a0015729 [cited as Kornell et al. 2009]
- Lally, P.; van Jaarsveld, C. H. M.; Potts, H. W. W.; Wardle, J. (2010). How are habits formed: Modelling habit formation in the real world. *European Journal of Social Psychology*. https://doi.org/10.1002/ejsp.674
- Latimier, A.; Peyre, H.; Ramus, F. (2021). A meta-analytic review of the benefit of spacing out retrieval practice episodes on retention. *Educational Psychology Review*. https://doi.org/10.1007/s10648-020-09572-8
- Laufer, B.; Goldstein, Z. (2004). Testing vocabulary knowledge: Size, strength, and computer adaptiveness. *Language Learning*. https://doi.org/10.1111/j.0023-8333.2004.00260.x
- Laufer, B.; Hulstijn, J. (2001). Incidental vocabulary acquisition in a second language: The construct of task-induced involvement. *Applied Linguistics*. https://doi.org/10.1093/applin/22.1.1
- Laufer, B.; Shmueli, K. (1997). Memorizing new words: Does teaching have anything to do with it? *RELC Journal*. https://doi.org/10.1177/003368829702800106
- Li, M.; Uchihara, T.; Nakata, T.; Murphy, V. (2026). The effectiveness of semantic clustering on vocabulary learning: A multilevel meta-analysis. *System*. https://doi.org/10.1016/j.system.2026.104141
- Lindsey, R. V.; Shroyer, J. D.; Pashler, H.; Mozer, M. C. (2014). Improving students' long-term knowledge retention through personalized review. *Psychological Science*. https://doi.org/10.1177/0956797613504302
- Little, J. L.; Bjork, E. L.; Bjork, R. A.; Angello, G. (2012). Multiple-choice tests exonerated, at least of some charges: Fostering test-induced learning and avoiding test-induced forgetting. *Psychological Science*. https://doi.org/10.1177/0956797612443370
- Mettler, E.; Massey, C. M.; Kellman, P. J. (2016). A comparison of adaptive and fixed schedules of practice. *Journal of Experimental Psychology: General*. https://doi.org/10.1037/xge0000170
- Mondria, J.-A.; Wiersma, B. (2004). Receptive, productive, and receptive + productive L2 vocabulary learning: What difference does it make? *Vocabulary in a Second Language (John Benjamins)*. https://doi.org/10.1075/lllt.10.08mon
- Nakata, T.; Elgort, I. (2021). Effects of spacing on contextual vocabulary learning: Spacing facilitates the acquisition of explicit, but not tacit, vocabulary knowledge. *Second Language Research*. https://doi.org/10.1177/0267658320927764
- Nakata, T.; Suzuki, Y. (2019). Mixing grammar exercises facilitates long-term retention: Effects of blocking, interleaving, and increasing practice. *The Modern Language Journal*. https://doi.org/10.1111/modl.12581 [cited as Nakata & Suzuki 2019a]
- Nakata, T.; Suzuki, Y. (2019). Effects of massing and spacing on the learning of semantically related and unrelated words. *Studies in Second Language Acquisition*. https://doi.org/10.1017/S0272263118000219 [cited as Nakata & Suzuki 2019b]
- Nakata, T.; Webb, S. (2016). Does studying vocabulary in smaller sets increase learning? The effects of part and whole learning on second language vocabulary acquisition. *Studies in Second Language Acquisition*. https://doi.org/10.1017/S0272263115000236
- Nakata, T. (2011). Computer-assisted second language vocabulary learning in a paired-associate paradigm: A critical investigation of flashcard software. *Computer Assisted Language Learning*. https://doi.org/10.1080/09588221.2010.520675
- Nakata, T. (2015). Effects of expanding and equal spacing on second language vocabulary learning: Does gradually increasing spacing increase vocabulary learning? *Studies in Second Language Acquisition*. https://doi.org/10.1017/S0272263114000825 [cited as Nakata 2015a]
- Nakata, T. (2015). Effects of feedback timing on second language vocabulary learning: Does delaying feedback increase learning? *Language Teaching Research*. https://doi.org/10.1177/1362168814541721 [cited as Nakata 2015b]
- Nakata, T. (2017). Does repeated practice make perfect? The effects of within-session repeated retrieval on second language vocabulary learning. *Studies in Second Language Acquisition*. https://doi.org/10.1017/S0272263116000280
- Nation, P. (2007). The four strands. *Innovation in Language Learning and Teaching*. https://doi.org/10.2167/illt039.0
- Nation, I. S. P. (2022). Learning Vocabulary in Another Language. *Cambridge University Press (3rd ed.)*. https://doi.org/10.1017/9781009093873
- Pan, S. C.; Carpenter, S. K. (2023). Prequestioning and pretesting effects: A review of empirical research, theoretical perspectives, and implications for educational practice. *Educational Psychology Review*. https://doi.org/10.1007/s10648-023-09814-5
- Pan, S. C.; Rickard, T. C. (2018). Transfer of test-enhanced learning: Meta-analytic review and synthesis. *Psychological Bulletin*. https://doi.org/10.1037/bul0000151
- Pan, S. C.; Tajran, J.; Lovelett, J.; Osuna, J.; Rickard, T. C. (2019). Does interleaved practice enhance foreign language learning? The effects of training schedule on Spanish verb conjugation skills. *Journal of Educational Psychology*. https://doi.org/10.1037/edu0000336
- Pashler, H.; Cepeda, N. J.; Wixted, J. T.; Rohrer, D. (2005). When does feedback facilitate learning of words? *Journal of Experimental Psychology: Learning, Memory, and Cognition*. https://doi.org/10.1037/0278-7393.31.1.3
- Pavlik, P. I.; Anderson, J. R. (2005). Practice and forgetting effects on vocabulary memory: An activation-based model of the spacing effect. *Cognitive Science*. https://doi.org/10.1207/s15516709cog0000_14
- Pavlik, P. I.; Anderson, J. R. (2008). Using a model to compute the optimal schedule of practice. *Journal of Experimental Psychology: Applied*. https://doi.org/10.1037/1076-898X.14.2.101
- Potts, R.; Shanks, D. R. (2014). The benefit of generating errors during learning. *Journal of Experimental Psychology: General*. https://doi.org/10.1037/a0033194
- Pyc, M. A.; Rawson, K. A. (2009). Testing the retrieval effort hypothesis: Does greater difficulty correctly recalling information lead to higher levels of memory? *Journal of Memory and Language*. https://doi.org/10.1016/j.jml.2009.01.004
- Rawson, K. A.; Dunlosky, J. (2011). Optimizing schedules of retrieval practice for durable and efficient learning: How much is enough? *Journal of Experimental Psychology: General*. https://doi.org/10.1037/a0023956
- Rawson, K. A.; Dunlosky, J. (2022). Successive relearning: An underexplored but potent technique for obtaining and maintaining knowledge. *Current Directions in Psychological Science*. https://doi.org/10.1177/09637214221100484
- Rawson, K. A.; Dunlosky, J.; Sciartelli, S. M. (2013). The power of successive relearning: Improving performance on course exams and long-term retention. *Educational Psychology Review*. https://doi.org/10.1007/s10648-013-9240-4
- Reddy, S.; Labutov, I.; Banerjee, S.; Joachims, T. (2016). Unbounded human learning: Optimal scheduling for spaced repetition. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*. https://doi.org/10.1145/2939672.2939850
- Roediger, H. L.; Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science*. https://doi.org/10.1111/j.1467-9280.2006.01693.x
- Roediger, H. L.; Marsh, E. J. (2005). The positive and negative consequences of multiple-choice testing. *Journal of Experimental Psychology: Learning, Memory, and Cognition*. https://doi.org/10.1037/0278-7393.31.5.1155
- Rogers, J.; Nakata, T.; Chiu (2025). Optimizing distributed practice online: A conceptual replication of Cepeda et al. (2009). *Studies in Second Language Acquisition*. https://doi.org/10.1017/S0272263124000706
- Rohrer, D.; Taylor, K.; Pashler, H.; Wixted, J. T.; Cepeda, N. J. (2005). The effect of overlearning on long-term retention. *Applied Cognitive Psychology*. https://doi.org/10.1002/acp.1083
- Rowland, C. A. (2014). The effect of testing versus restudy on retention: A meta-analytic review of the testing effect. *Psychological Bulletin*. https://doi.org/10.1037/a0037559
- Sarıoğlu, M.; Karatepe (2024). The Use of Mnemonics to Minimize the Interfering Effects of Teaching New Words in Semantic Sets to Learners of English as a Foreign Language. *Applied Cognitive Psychology*. https://doi.org/10.1002/acp.4251
- Seibert Hanson, A. E.; Brown, C. M. (2020). Enhancing L2 learning through a mobile assisted spaced-repetition tool: an effective but bitter pill? *Computer Assisted Language Learning*. https://doi.org/10.1080/09588221.2018.1552975
- Sense, F.; Behrens, F.; Meijer, R. R.; van Rijn, H. (2016). An individual's rate of forgetting is stable over time but differs across materials. *Topics in Cognitive Science*. https://doi.org/10.1111/tops.12183
- Settles, B.; Meeder, B. (2016). A trainable spaced repetition model for language learning. *Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics*. https://doi.org/10.18653/v1/P16-1174
- Shu, M.; Balepur, N.; Feng, S.; Boyd-Graber, J. (2024). KARL: Knowledge-Aware Retrieval and Representations aid Retention and Learning in Students. *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing*. https://doi.org/10.18653/v1/2024.emnlp-main.784
- Soderstrom, N. C.; Bjork, R. A. (2015). Learning versus performance: An integrative review. *Perspectives on Psychological Science*. https://doi.org/10.1177/1745691615569000
- open-spaced-repetition (Ye, J.; contributors) (2026). srs-benchmark: A benchmark for spaced repetition schedulers/algorithms. *GitHub repository*. https://github.com/open-spaced-repetition/srs-benchmark [cited as srs-benchmark 2026]
- Su, J.; Ye, J.; Nie, L.; Cao, Y.; Chen, Y. (2023). Optimizing spaced repetition schedule by capturing the dynamics of memory. *IEEE Transactions on Knowledge and Data Engineering*. https://doi.org/10.1109/TKDE.2023.3251721
- Suzuki, Y.; DeKeyser, R. (2017). Effects of distributed practice on the proceduralization of morphology. *Language Teaching Research*. https://doi.org/10.1177/1362168815617334 [cited as Suzuki & DeKeyser 2017]
- Tabibian, B.; Upadhyay, U.; De, A.; Zarezade, A.; Schölkopf, B.; Gomez-Rodriguez, M. (2019). Enhancing human learning via spaced repetition optimization. *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.1815156116
- Tinkham, T. (1993). The effect of semantic clustering on the learning of second language vocabulary. *System*. https://doi.org/10.1016/0346-251X(93)90027-E
- open-spaced-repetition (contributors) (2026). ts-fsrs updates (release feed). *Project documentation site*. https://open-spaced-repetition.github.io/ts-fsrs/rss/updates.xml [cited as ts-fsrs 2026]
- Uchihara, T.; Webb, S.; Yanagisawa, A. (2019). The effects of repetition on incidental vocabulary learning: A meta-analysis of correlational studies. *Language Learning*. https://doi.org/10.1111/lang.12343
- Upadhyay, U.; Lancashire, G.; Moser, C.; Gomez-Rodriguez, M. (2021). Large-scale randomized experiments reveals that machine learning-based instruction helps people memorize more effectively. *npj Science of Learning*. https://doi.org/10.1038/s41539-021-00105-8
- van der Velde, M.; Sense, F.; Borst, J.; van Rijn, H. (2021). Alleviating the cold start problem in adaptive learning using data-driven difficulty estimates. *Computational Brain & Behavior*. https://doi.org/10.1007/s42113-021-00101-6
- Walsh, M. M.; Gluck, K. A.; Gunzelmann, G.; Jastrzembski, T.; Krusmark, M. (2018). Evaluating the theoretic adequacy and applied potential of computational models of the spacing effect. *Cognitive Science*. https://doi.org/10.1111/cogs.12602
- Wang, A. Y.; Thomas, M. H. (1995). Effect of keywords on long-term retention: Help or hindrance? *Journal of Educational Psychology*. https://doi.org/10.1037/0022-0663.87.3.468
- Waring, R. (1997). The negative effects of learning words in semantic sets: A replication. *System*. https://doi.org/10.1016/S0346-251X(97)00013-4
- Webb, S. (2009). The effects of receptive and productive learning of word pairs on vocabulary knowledge. *RELC Journal*. https://doi.org/10.1177/0033688209343854
- Webb, S.; Yanagisawa, A.; Uchihara, T. (2020). How effective are intentional vocabulary-learning activities? A meta-analysis. *The Modern Language Journal*. https://doi.org/10.1111/modl.12671
- Webb, S.; Uchihara, T.; Yanagisawa, A. (2023). How effective is second language incidental vocabulary learning? A meta-analysis. *Language Teaching*. https://doi.org/10.1017/s0261444822000507
- Wiley, R. W.; Rapp, B. (2021). The effects of handwriting experience on literacy learning. *Psychological Science*. https://doi.org/10.1177/0956797621993111
- Wixted, J. T.; Ebbesen, E. B. (1991). On the form of forgetting. *Psychological Science*. https://doi.org/10.1111/j.1467-9280.1991.tb00175.x
- Wozniak, P. A.; Gorzelanczyk, E. J. (1994). Optimization of repetition spacing in the practice of learning. *Acta Neurobiologiae Experimentalis*. https://doi.org/10.55782/ane-1994-1003
- Wozniak, P. A. (1990). Application of a computer to improve the results obtained in working with the SuperMemo method (Algorithm SM-2). *SuperMemo archive (adapted from the author's 1990 master's thesis)*. https://www-v1.supermemo.com/archives1990-2015/english/ol/sm2
- Wozniak, P. A.; Gorzelanczyk, E. J.; Murakowski, J. A. (1995). Two components of long-term memory. *Acta Neurobiologiae Experimentalis*. https://doi.org/10.55782/ane-1995-1090
- Yanagisawa, A.; Webb, S. (2021). To what extent does the involvement load hypothesis predict incidental L2 vocabulary learning? A meta-analysis. *Language Learning*. https://doi.org/10.1111/lang.12444
- Yanagisawa, A.; Webb, S. (2022). Involvement Load Hypothesis Plus: Creating an improved predictive model of incidental vocabulary learning. *Studies in Second Language Acquisition*. https://doi.org/10.1017/S0272263121000577
- Yanagisawa, A.; Webb, S.; Uchihara, T. (2020). How do different forms of glossing contribute to L2 vocabulary learning from reading? A meta-regression analysis. *Studies in Second Language Acquisition*. https://doi.org/10.1017/S0272263119000688
- Yang, C.; Luo, L.; Vadillo, M. A.; Yu, R.; Shanks, D. R. (2021). Testing (quizzing) boosts classroom learning: A systematic and meta-analytic review. *Psychological Bulletin*. https://doi.org/10.1037/bul0000309
- Ye, J.; Su, J.; Cao, Y. (2022). A stochastic shortest path algorithm for optimizing spaced repetition scheduling. *Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*. https://doi.org/10.1145/3534678.3539081
