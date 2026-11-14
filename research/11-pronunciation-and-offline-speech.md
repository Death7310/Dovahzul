# Track 11. Pronunciation and listening for a language with no native speakers, fully offline

*Research report, 2026-11-14. Language facts are labelled **canon**, **semi-canon** or **fan**. "Inference" is my own reasoning. "NRV" is a technical fact from my own knowledge that this run's ten searches did not re-verify. "Recalled" is a study result known from the paper but not re-read here. Lexicon figures were computed for this report from `research/data/canon-phonotactics.json` (666 word forms, canon and semi-canon tiers together).*

## 1. Bottom line

- **The pronunciation standard must be a written project convention, set by the project owner.** No official guide exists (Track 1), the game audio cannot be shipped, and the game's own book says an ancient song lacks "a sure pronunciation" (canon, *Songs of Skyrim*). Klingon, Na'vi, Dothraki and Esperanto all anchor pronunciation in a written description by a named authority and treat performances as evidence.
- **Define each sound as a core value plus tolerated variants, and aim at intelligibility inside the system:** keeping the lexicon's words apart, not copying an actor. The canon lexicon has 1,143 minimal pairs, and the spelled length contrasts carry few of them (i/ii 6, a/ah 3, a/aa 2, ei/ey 2, k/q 2, aa/ah 1, o/oo 1, u/uu 0).
- **Train perception first, and score only perception.** Identification training with feedback over several voices is the best-supported technique (g = 0.92 pre to post, g = 0.67 against controls; Uchihara et al. 2025). It carries over partly to speaking (d = 0.54; Sakai & Moorman 2018) and can be scored offline by rule.
- **Do not ship an automatic pronunciation score.** Every known method needs speech and human ratings in the target language, and none exist. Use record, compare and self-rate against explicit criteria, with descriptive displays and export for human review.
- **Pre-render reference audio at build time from phoneme strings** with eSpeak NG (GPL v3, accepts phoneme input) in several synthetic voices (my estimate: under 25 MB for all word forms and canon sentences in four voices). Offer on-device synthesis only as an optional pack for forge-coined words.
- **Do not use the platform speech-synthesis interface for Dovahzul.** It takes no phoneme input and would read the words by another language's spelling rules.
- **Human audio should come from volunteers under CC0 or CC BY**, recorded against the written standard, checked by two reviewers, several talkers per item.

## 2. Findings

Treated in depth: the standard (c), offline technology and scoring (d), perception training (a). Treated briefly: prosody, articulatory visual feedback, extensive listening.

### a. Pronunciation instruction

**Instruction works, mostly where measurement is narrow.** Lee et al. (2015) pooled 86 studies and found d = 0.89 within groups and 0.80 between groups (recalled). Saito and Plonsky (2019) recoded 77 studies: instruction is most effective for monitored production of specific features, and evidence for spontaneous speech is thinner. Thomson and Derwing (2015) agree and note how few studies test retention.

**Intelligibility, not nativeness.** Accent, comprehensibility and intelligibility are partly independent: heavily accented speech can be fully understood (Munro & Derwing 1995; Isaacs & Trofimovich 2012). Levis (2005) named the two competing goals, and the field has settled on intelligibility (Derwing & Munro 2015). Jenkins (2002) derived a core of features needed for mutual understanding among non-native speakers and left the rest free, and errors on contrasts that distinguish many words hurt comprehensibility more than errors on low-load contrasts (Munro & Derwing 2006). Both ideas suit a language whose every speaker is a learner.

**Segments and prosody both matter.** Prosody-focused teaching improved comprehensibility in free speech where segment-only teaching did not (Derwing et al. 1998), and misplaced stress lowers intelligibility (Hahn 2004; Field 2005). Stress in Dovahzul is unattested (Track 1), so it needs a ruling before it can be taught.

**High-variability phonetic training (HVPT).** Learners identify sounds spoken by several talkers in several contexts, with feedback (Logan et al. 1991; Lively et al. 1993). A 79-study meta-analysis gives g = 0.92 pre to post and g = 0.67 against controls, with retention and some generalisation; talker number, training time, response labels and task type moderate the effect (Uchihara et al. 2025). The specific benefit of many talkers over one is small (g = 0.46, 18 studies, 549 learners; Zhang et al. 2021), and a replication did not clearly reproduce it (Brekelmans et al. 2022; recalled). Low-aptitude learners did better with talkers blocked than mixed (Perrachione et al. 2011; recalled). Training also works with signal-processed or partly synthetic stimuli (Iverson et al. 2005; Wang & Munro 2004) and suits self-study software (Thomson 2011, 2018).

**Perception before production.** Perception-only training improved speech (Bradlow et al. 1997). Across 25 years of studies, perception gains were d = 0.92 and production gains d = 0.54 (Sakai & Moorman 2018). For HVPT, production gains averaged 10.5 points on trained items and 4.5 on untrained ones, with no firm evidence of retention or generalisation (Uchihara et al. 2024). The link is real but hard to characterise (Nagle & Baese-Berk 2022). Two cautions: speaking during perceptual training disrupted perceptual learning (Baese-Berk & Samuel 2016), and in 38 learners of Mandarin tone words each skill improved mainly through its own practice (Li & DeKeyser 2017).

**Shadowing.** Nine lessons improved phoneme perception in 43 learners (Hamada 2016; results recalled). Eight weeks of mobile shadowing improved imitation, comprehensibility and fluency but not accent in 16 learners with no control group (Foote & McDonough 2017; results recalled). One search found no meta-analysis.

**Explicit articulatory instruction.** With 95 learners of Spanish, explicit phonetics lessons gave no advantage over the same input, practice and feedback (Kissling 2013; result recalled). With 49 learners of English, adding explicit information helped gains generalise to new words (Saito 2013; result recalled).

**Visual feedback.** Seeing one's own acoustic output beside a model improves segments such as voice onset time, more with longer treatment (Olson & Offerman 2021). Pitch displays have long been used to teach intonation (Levis & Pickering 2004).

**Self-assessment.** Learners judge their own pronunciation poorly. Among 134 speakers, weak ones overrated and strong ones underrated themselves (Trofimovich et al. 2016). Advanced learners of German found fewer than half of the sounds raters marked wrong (Dlaska & Krekeler 2008; recalled). Across language skills self-assessment correlates .466 with performance, more with explicit criteria and training (Li & Zhang 2021).

**Computer-assisted training.** A meta-analysis of 20 studies (1,014 learners) found a moderate advantage over conventional teaching (Mahdi & Al Khateeb 2019; size recalled). Speech-recognition feedback gave g = 0.69 over 15 studies, large for segments, small for prosody, nil for short treatments (Ngo et al. 2024). All of this concerns English, with recognisers trained on English. Standing criticisms: tools follow what the technology can do, not what learners need, and recognisers misjudge accented speech (Neri et al. 2002; Derwing et al. 2000; Rogerson-Revell 2021).

### b. Speech-learning theory for adults

The revised Speech Learning Model holds that adults keep the capacity to form new categories, that success depends on how different a sound is perceived to be from the nearest first-language category and on the input received, and that perception and production develop together (Flege & Bohn 2021). The Perceptual Assimilation Model predicts which contrasts are hard from how the two sounds map onto first-language categories (Best & Tyler 2007). Early commitment to first-language categories warps later perception (Kuhl et al. 2008; Iverson et al. 2003).

*Inference for Dovahzul.* The language was written in Latin letters by English speakers and voiced by English-speaking actors, and nothing in the data points to a sound English lacks. For English speakers the load is spelling-to-sound mapping (aa, ah, ei, ey, ii, ir, oo, uu, ur) and stress, not new categories. For other learners it depends on what the standard chooses for *th*, *sh*, *j*, *r* and vowel length. Tolerated variants should be widest where the theory predicts trouble and the lexicon shows no contrast at stake.

### c. The standard: what it should be and who sets it

**What the record holds.** The data contain no sound values (canon gap). The in-game book *Songs of Skyrim* presents a song as lost "without a tune or a sure pronunciation" (canon). The wiki notes that *j* is voiced in two ways and that one shout word is voiced differently from its spelling (UESP 2026; fan observation of game audio, via Track 1). The largest fan site publishes "typical IPA" for the runes, and its own forum disputes the *r* (tap or trill against the English sound) and some vowels (Thuum.org n.d.; Thuum.org forum n.d.; fan, seen only as search summaries).

**How other communities handled it.**

| Language | Where the norm lives | Actors' or speakers' departures |
|---|---|---|
| Klingon | Okrand's published description; the Klingon Language Institute treats his works as canon (Okrand 1985; KLI n.d.) | Okrand coached actors, then amended the language to match their mispronunciations (KLI n.d.). Okrand (1997) describes regional dialects with their own pronunciations, which members read as back-fitted actor idiosyncrasies (mailing-list posts in search results; fan reading) |
| Na'vi | Frommer's description and recordings; he taught the cast, recorded lines for them and monitored them on set (NPR 2009) | He remains the authority, with organised fan input on vocabulary (Schreyer 2011, 2015) |
| Dothraki | Peterson's published course (Peterson 2014; its audio component NRV) | The description, not the screen performance, is taught (NRV) |
| Esperanto | A written foundation, model usage and an academy, in a self-regulating community (Fiedler 2006) | Native speakers exist but do not define correctness; children's speech departs from the standard (Bergen 2001; small sample, recalled) |

**The pattern (inference).** One named authority publishes a written description. Performances are evidence. Each inconsistency is adopted, tolerated as a variant, or declared an error. Dovahzul has no participating creator, so the project owner fills that role for this project and should say so openly: the standard is "this project's reading convention", not "the correct pronunciation". Volunteers may listen to their own copy of the game and log what they hear; describing a sound copies nothing, while shipping clips would (not legal advice).

### d. Offline technology in 2026

| Option | Phoneme input | Licence | Size | Verdict |
|---|---|---|---|---|
| eSpeak NG (formant synthesis in the tradition of Klatt 1980) | Yes, inside `[[ ]]` (search-verified) | GPL v3 | A few MB with one language's data (NRV) | Build-time tool; optional on-device pack |
| Its WebAssembly builds | Same | GPL v3 | NRV | Exist: an npm package with voice data (text2wav n.d.), a ChromeOS engine (Chromium n.d.), a 2026 phonemiser-only build (Stericker 2026), the older meSpeak.js (Landsteiner 2019) |
| Piper (neural) | Via eSpeak NG phonemes; direct input NRV | Original MIT repository reported archived in October 2025 (secondary sources in search results); successor is GPL-3.0 (AUR 2026; piper-plus 2026) | About 10 to 50 MB per voice (third-party figure) | Runs in a browser through sherpa-onnx (sherpa-onnx 2024); voices trained on one natural language |
| Kokoro-82M (neural) | NRV | Weights Apache-2.0; browser phonemiser derives from eSpeak NG | About 82 MB, then cached (kokoro-js 2025; a guide's figure) | Too large by default; English-trained |
| Platform `speechSynthesis` | No; phoneme markup is not honoured (search summaries) | System voices | 0 | Not usable for Dovahzul |

**Platform speech synthesis.** Each voice carries a `localService` flag marking offline voices (MDN n.d.). Voice sets differ by browser and system (Readium n.d.); Firefox on Android lacks synthesis, and voices may be missing inside an Android web view (search summaries of library documentation). On macOS and Windows the system voices work offline while some browser-added voices need a connection (NRV). The decisive point: the interface accepts text only, so a Dovahzul word would be read by whatever spelling rules the voice has.

**Pre-render or synthesise on the device.** Pre-rendering wins for the fixed lexicon and corpus: every clip can be heard and approved before release, output is identical everywhere, and no synthesiser ships in the app. About 800 word forms at 0.7 s and 24 kbit/s is under 2 MB per voice; four voices with the canon sentences stay under 25 MB (my estimate, in line with Track 13). On-device synthesis is needed only for forge-coined words and learners' own sentences.

**Is a formant voice good enough?** Formant synthesis was less intelligible than concatenative synthesis, and both fell below natural speech in noise (Venkatagiri 2003). An older machine voice reduced learning against a human voice (Atkinson et al. 2005); a modern engine did not (Craig & Schroeder 2017; recalled). Learners handled modern synthetic speech about as well as human speech and practised pronunciation with it successfully (Cardoso et al. 2015; Liakin et al. 2017; both recalled). A formant voice is an honest floor, not the goal.

**Recording, pitch, spectrogram.** Browsers record through `getUserMedia` and `MediaRecorder`; the container differs by engine, so capture raw samples through the Web Audio interface for analysis (NRV). Pitch tracking by the YIN algorithm (de Cheveigné & Kawahara 2002) and a short-time Fourier spectrogram each need about a hundred lines of code and no dependency (inference).

**Can pronunciation be scored honestly offline? No.** Goodness-of-pronunciation scoring compares a learner's sounds with acoustic models trained on native speech, with thresholds calibrated against human judges (Witt & Young 2000). Methods that align a learner's recording to a teacher's still need reference speakers and labelled errors (Lee & Glass 2012). Dovahzul has no speech corpus and no rated learner speech, and its reference would be a synthetic voice, so any number shown would be unvalidated; a wrong score misleads or discourages. A recogniser built for English would mark the standard's own choices as errors (inference). The substitute has four parts: scored perception; record, compare and self-rate with criteria; descriptive displays; human review outside the app.

### e. Listening

Much of a beginner's listening difficulty lies in decoding, which targeted practice trains (Field 2008); planning, monitoring and evaluating one's listening adds to it (Vandergrift & Goh 2012). Frequent dictation improved listening comprehension in one study of 60 elementary learners (Kiany & Shiramiry 2002). Reconstructing a heard text and comparing it with the original is proposed as a way to show learners their own decoding errors (Wilson 2003; a method paper). Reading while listening built listening fluency more than listening alone (Chang & Millett 2014; recalled).

The listening material is small: the canon corpus is a few thousand running words (Track 15). Minimal pairs can be generated from the lexicon: 276 vowel pairs and 860 consonant pairs, led by o/u (19), aa/o (16), l/n (27) and n/r (21).

Open-licensed volunteer audio has working models. Common Voice collects read sentences and releases them as CC0 (Ardila et al. 2020; Mozilla 2019). Lingua Libre records word lists in the browser, lets each speaker choose CC0, CC BY or CC BY-SA 4.0, and uploads to Wikimedia Commons (Lingua Libre n.d.; Wikimedia n.d.).

## 3. What this means for the app

1. **Pronunciation standard as versioned data.** One record per spelling unit: `{unit, ipa_core, tolerated[], basis: "spelling" | "observed-in-game" | "owner-ruling", evidence[], confidence, since}`. Evidence entries are written notes (who heard what, where), never audio. The owner rules; changes go through the forge's rule process. First rulings: *j*, *r*, vowel + *h*, whether doubled vowels are long, the apostrophe, and one fixed stress rule. *Evidence: 2c; Fiedler 2006; Jenkins 2002. Confidence: high for the structure; the values are low-confidence until ruled.*
2. **One spelling-to-sound function.** Lower-case, longest match over the unit list already used by `phonotactics.py`, table lookup. It returns IPA for display, the eSpeak phoneme string for the build, and syllables for stress marking. *Confidence: high.*
3. **Contrast table built from the lexicon.** For every pair of units, list the minimal pairs and the homophones a merger would create. Use it to order drills by load (Munro & Derwing 2006) and to show the owner what each tolerance costs: merging all spelled length distinctions creates only 14 homophone sets in 666 forms. *Confidence: high.*
4. **Perception trainer.** Play one clip, show two to four spelled choices, give immediate feedback and replay both words. Sessions of about ten minutes, at least four voices, one voice held out per contrast to test generalisation. Block trials by voice at first and for anyone under 70% correct, then mix. Pass a contrast at 90% of 20 trials on the held-out voice, then hand it to the spacing scheduler. *Evidence: Uchihara et al. 2025; Perrachione et al. 2011. Confidence: high for the method; thresholds are my defaults.*
5. **Production loop without a score.** Listen, shadow three times, record, hear model, self, model, then tick a checklist (each vowel unit; *th*, *j*, *r*; stress on the marked syllable; no added vowels). Start it for a contrast only after the perception pass, never inside identification trials. Point the checklist at contrasts the learner still confuses by ear. *Evidence: Foote & McDonough 2017; Baese-Berk & Samuel 2016; Li & DeKeyser 2017; Li & Zhang 2021. Confidence: medium.*
6. **Descriptive displays.** Waveform, pitch contour and spectrogram of model and learner, aligned at onset, labelled "for comparison, not a score". Starting parameters: 16 kHz, pitch search 60 to 500 Hz, 40 ms window, 10 ms hop, spectrogram to 5 kHz. *Evidence: Olson & Offerman 2021; Levis & Pickering 2004. Confidence: medium; parameters are engineering defaults.*
7. **Build-time audio.** Feed phoneme strings to a pinned eSpeak NG version in four voice settings (pitch, rate, variant), encode, pack one sprite per voice, and write a manifest: `{clip, voice, kind: "synthetic" | "human", phonemes, standard_version, sprite, start, dur, licence, sha256}`. A change to the standard regenerates only affected clips. Confirm the licence position of synthesiser output before release. No platform speech synthesis for Dovahzul text. *Confidence: high for pre-rendering; medium that four synthetic settings give useful variability.*
8. **Optional synthesis pack** for forge words: the WebAssembly build loaded on demand, which obliges a GPL-compatible app licence. Until it is installed, show IPA and syllables only. *Confidence: medium.*
9. **Listening and dictation.** Rule-checked dictation of words, then canon lines, normalising case and apostrophes, with a character-level diff as feedback and a variant answered in runes. Canon texts with synchronised highlighting. *Evidence: Field 2008; Kiany & Shiramiry 2002; Chang & Millett 2014. Confidence: medium.*
10. **Volunteer recording tool.** Prompts from the lexicon; record in the app; export a package with a CC0 or CC BY declaration; accept a clip when two reviewers tick the same checklist against the standard; store talker, standard version and licence in the manifest. *Evidence: Ardila et al. 2020; Lingua Libre n.d. Confidence: medium.*

**Staged plan.** Stage 0: rulings, spelling-to-sound function, IPA display, contrast table. Stage 1: synthetic audio, perception trainer, dictation, record and compare, displays. Stage 2: volunteer recordings replace synthetic voices item by item and become the held-out test voices. Stage 3: optional synthesis pack, sentence-level listening and shadowing, prosody conventions. Stage 4: revisit automatic feedback only if a reviewed, rated corpus of learner speech exists.

**Honest limits.** The standard is a convention. The first voices are robotic. Self-rating is unreliable even with criteria. Nothing here has been tested on learners of a constructed language.

## 4. Contested or weak evidence

- The many-talker advantage is small and failed one replication; the case for HVPT rests on training with feedback, not on variability alone.
- Shadowing, dictation and synthetic-voice findings each rest on one or two small studies; several results are recalled, not re-read.
- Nearly all pronunciation research concerns English with native-speaker norms; applying it here is inference.
- Using synthetic settings as "talkers" is untested; the supporting studies used human talkers or manipulated human speech.

## 5. Gaps, and anything blocked

- No official pronunciation guide was found; game audio was not consulted, so no sound value here is checked against it.
- Not verified by search: WebAssembly build sizes, Piper's direct phoneme input, Kokoro's quantised sizes and phoneme input, recorder containers by browser, the licence status of synthesiser output, and newer small neural synthesisers (not searched, for lack of budget).
- thuum.org was not fetched (it refuses automated requests); it is cited from search summaries only. WebFetch was unavailable.
- Not in Crossref: Okrand (1985, 1997) and Peterson (2014), confirmed from search results; Ardila et al. (2020), confirmed on the ACL Anthology.
- No study of pronunciation teaching for any constructed language was found.

## 6. References

Checked with `tools/research/check_refs.py`; 86 sources. Status: manual 18, not_found 4, verified 64.

- Arch User Repository (2026). Package details: piper-tts 1.8.0-1. aur.archlinux.org. https://aur.archlinux.org/packages/piper-tts [web source, cited as "AUR 2026"; URL seen in search results]
- Ardila, R.; Branson, M.; Davis, K.; Kohler, M.; Meyer, J.; Henretty, M.; Morais, R.; Saunders, L.; Tyers, F.; Weber, G. (2020). Common Voice: A Massively-Multilingual Speech Corpus. Proceedings of the Twelfth Language Resources and Evaluation Conference (LREC 2020), 4218-4222. European Language Resources Association. https://aclanthology.org/2020.lrec-1.520/ [not in Crossref; confirmed against the ACL Anthology record]
- Atkinson, R. K.; Mayer, R. E.; Merrill, M. M. (2005). Fostering social agency in multimedia learning: Examining the impact of an animated agent's voice. Contemporary Educational Psychology. https://doi.org/10.1016/j.cedpsych.2004.07.001
- Baese-Berk, M. M.; Samuel, A. G. (2016). Listeners beware: Speech production may be bad for learning speech sounds. Journal of Memory and Language. https://doi.org/10.1016/j.jml.2015.10.008
- Bergen, B. K. (2001). Nativization processes in L1 Esperanto. Journal of Child Language. https://doi.org/10.1017/S0305000901004779
- Best, C. T.; Tyler, M. D. (2007). Nonnative and second-language speech perception: Commonalities and complementarities. In Bohn, O.-S.; Munro, M. J. (eds.), Language Experience in Second Language Speech Learning. John Benjamins. https://doi.org/10.1075/lllt.17.07bes
- Bradlow, A. R.; Pisoni, D. B.; Akahane-Yamada, R.; Tohkura, Y. (1997). Training Japanese listeners to identify English /r/ and /l/: IV. Some effects of perceptual learning on speech production. The Journal of the Acoustical Society of America. https://doi.org/10.1121/1.418276
- Brekelmans, G.; Lavan, N.; Saito, H.; Clayards, M.; Wonnacott, E. (2022). Does high variability training improve the learning of non-native phoneme contrasts over low variability training? A replication. Journal of Memory and Language. https://doi.org/10.1016/j.jml.2022.104352
- Cardoso, W.; Smith, G.; Garcia Fuentes, C. (2015). Evaluating text-to-speech synthesizers. Critical CALL - Proceedings of the 2015 EUROCALL Conference, Padova, Italy. https://doi.org/10.14705/rpnet.2015.000318
- Chang, A. C.-S.; Millett, S. (2014). The effect of extensive listening on developing L2 listening fluency: some hard evidence. ELT Journal. https://doi.org/10.1093/elt/cct052
- Craig, S. D.; Schroeder, N. L. (2017). Reconsidering the voice effect when learning from a virtual human. Computers & Education. https://doi.org/10.1016/j.compedu.2017.07.003
- de Cheveigné, A.; Kawahara, H. (2002). YIN, a fundamental frequency estimator for speech and music. The Journal of the Acoustical Society of America. https://doi.org/10.1121/1.1458024
- Derwing, T. M.; Munro, M. J. (2015). Pronunciation Fundamentals: Evidence-based perspectives for L2 teaching and research. John Benjamins. https://doi.org/10.1075/lllt.42
- Derwing, T. M.; Munro, M. J.; Carbonaro, M. (2000). Does popular speech recognition software work with ESL speech?. TESOL Quarterly. https://doi.org/10.2307/3587748
- Derwing, T. M.; Munro, M. J.; Wiebe, G. (1998). Evidence in favor of a broad framework for pronunciation instruction. Language Learning. https://doi.org/10.1111/0023-8333.00047
- Dlaska, A.; Krekeler, C. (2008). Self-assessment of pronunciation. System. https://doi.org/10.1016/j.system.2008.03.003
- Fiedler, S. (2006). Standardization and self-regulation in an international speech community: the case of Esperanto. International Journal of the Sociology of Language. https://doi.org/10.1515/IJSL.2006.005
- Field, J. (2005). Intelligibility and the listener: The role of lexical stress. TESOL Quarterly. https://doi.org/10.2307/3588487
- Field, J. (2008). Listening in the Language Classroom. Cambridge University Press. https://doi.org/10.1017/CBO9780511575945
- Flege, J. E.; Bohn, O.-S. (2021). The revised Speech Learning Model (SLM-r). In Wayland, R. (ed.), Second Language Speech Learning: Theoretical and Empirical Progress. Cambridge University Press. https://doi.org/10.1017/9781108886901.002
- Foote, J. A.; McDonough, K. (2017). Using shadowing with mobile technology to improve L2 pronunciation. Journal of Second Language Pronunciation. https://doi.org/10.1075/jslp.3.1.02foo
- Hahn, L. D. (2004). Primary stress and intelligibility: Research to motivate the teaching of suprasegmentals. TESOL Quarterly. https://doi.org/10.2307/3588378
- Hamada, Y. (2016). Shadowing: Who benefits and how? Uncovering a booming EFL teaching technique for listening comprehension. Language Teaching Research. https://doi.org/10.1177/1362168815597504
- Isaacs, T.; Trofimovich, P. (2012). Deconstructing comprehensibility: Identifying the linguistic influences on listeners' L2 comprehensibility ratings. Studies in Second Language Acquisition. https://doi.org/10.1017/S0272263112000150
- Iverson, P.; Hazan, V.; Bannister, K. (2005). Phonetic training with acoustic cue manipulations: A comparison of methods for teaching English /r/-/l/ to Japanese adults. The Journal of the Acoustical Society of America. https://doi.org/10.1121/1.2062307
- Iverson, P.; Kuhl, P. K.; Akahane-Yamada, R.; Diesch, E.; Tohkura, Y.; Kettermann, A.; Siebert, C. (2003). A perceptual interference account of acquisition difficulties for non-native phonemes. Cognition. https://doi.org/10.1016/S0010-0277(02)00198-1
- Jenkins, J. (2002). A sociolinguistically based, empirically researched pronunciation syllabus for English as an international language. Applied Linguistics. https://doi.org/10.1093/applin/23.1.83
- k2-fsa/sherpa-onnx contributors (2024). Issue 846 (WebAssembly text-to-speech with Piper models). GitHub. https://github.com/k2-fsa/sherpa-onnx/issues/846 [web source, cited as "sherpa-onnx 2024"; URL seen in search results]
- Kiany, G. R.; Shiramiry, E. (2002). The effect of frequent dictation on the listening comprehension ability of elementary EFL learners. TESL Canada Journal. https://doi.org/10.18806/tesl.v20i1.938
- Kissling, E. M. (2013). Teaching pronunciation: Is explicit phonetics instruction beneficial for FL learners?. The Modern Language Journal. https://doi.org/10.1111/j.1540-4781.2013.12029.x
- Klatt, D. H. (1980). Software for a cascade/parallel formant synthesizer. The Journal of the Acoustical Society of America. https://doi.org/10.1121/1.383940
- Klingon Language Institute (n.d.). Development and Use of the Klingon Language. kli.org. https://www.kli.org/?p=139 [web source, cited as "KLI n.d."; URL seen in search results]
- kokoro-js contributors (2025). kokoro-js (npm package README). npm. https://www.npmjs.com/package/kokoro-js [web source, cited as "kokoro-js 2025"; URL seen in search results]
- Kuhl, P. K.; Conboy, B. T.; Coffey-Corina, S.; Padden, D.; Rivera-Gaxiola, M.; Nelson, T. (2008). Phonetic learning as a pathway to language: new data and native language magnet theory expanded (NLM-e). Philosophical Transactions of the Royal Society B: Biological Sciences. https://doi.org/10.1098/rstb.2007.2154
- Landsteiner, N. (2019). Announcing meSpeak.js 2.0. masswerk.at. https://masswerk.at/nowgobang/2019/mespeak_2_0 [web source, cited as "Landsteiner 2019"; URL seen in search results]
- Lee, A.; Glass, J. (2012). A comparison-based approach to mispronunciation detection. 2012 IEEE Spoken Language Technology Workshop (SLT). https://doi.org/10.1109/SLT.2012.6424254
- Lee, J.; Jang, J.; Plonsky, L. (2015). The effectiveness of second language pronunciation instruction: A meta-analysis. Applied Linguistics. https://doi.org/10.1093/applin/amu040
- Levis, J. M. (2005). Changing contexts and shifting paradigms in pronunciation teaching. TESOL Quarterly. https://doi.org/10.2307/3588485
- Levis, J.; Pickering, L. (2004). Teaching intonation in discourse using speech visualization technology. System. https://doi.org/10.1016/j.system.2004.09.009
- Li, M.; DeKeyser, R. (2017). Perception practice, production practice, and musical ability in L2 Mandarin tone-word learning. Studies in Second Language Acquisition. https://doi.org/10.1017/s0272263116000358
- Li, M.; Zhang, X. (2021). A meta-analysis of self-assessment and language performance in language testing and assessment. Language Testing 38(2), 189-218. https://doi.org/10.1177/0265532220932481
- Liakin, D.; Cardoso, W.; Liakina, N. (2017). The pedagogical use of mobile speech synthesis (TTS): focus on French liaison. Computer Assisted Language Learning. https://doi.org/10.1080/09588221.2017.1312463
- Lingua Libre contributors (n.d.). Help:RecordWizard manual. lingualibre.org. https://www.lingualibre.org/wiki/Help:RecordWizard_manual [web source, cited as "Lingua Libre n.d."; URL seen in search results]
- Lively, S. E.; Logan, J. S.; Pisoni, D. B. (1993). Training Japanese listeners to identify English /r/ and /l/. II: The role of phonetic environment and talker variability in learning new perceptual categories. The Journal of the Acoustical Society of America. https://doi.org/10.1121/1.408177
- Logan, J. S.; Lively, S. E.; Pisoni, D. B. (1991). Training Japanese listeners to identify English /r/ and /l/: A first report. The Journal of the Acoustical Society of America. https://doi.org/10.1121/1.1894649
- Mahdi, H. S.; Al Khateeb, A. A. (2019). The effectiveness of computer-assisted pronunciation training: A meta-analysis. Review of Education. https://doi.org/10.1002/rev3.3165
- MDN contributors (n.d.). SpeechSynthesisVoice: localService property. MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisVoice/localService [web source, cited as "MDN n.d."; URL seen in search results]
- Mozilla (2019). Sharing our Common Voices: Mozilla releases the largest to-date public domain transcribed voice dataset. The Mozilla Blog, 28 February 2019. https://blog.mozilla.org/en/mozilla/news/sharing-our-common-voices-mozilla-releases-the-largest-to-date-public-domain-transcribed-voice-dataset/ [web source, cited as "Mozilla 2019"; URL seen in search results]
- Munro, M. J.; Derwing, T. M. (1995). Foreign accent, comprehensibility, and intelligibility in the speech of second language learners. Language Learning. https://doi.org/10.1111/j.1467-1770.1995.tb00963.x
- Munro, M. J.; Derwing, T. M. (2006). The functional load principle in ESL pronunciation instruction: An exploratory study. System. https://doi.org/10.1016/j.system.2006.09.004
- Nagle, C. L.; Baese-Berk, M. M. (2022). Advancing the state of the art in L2 speech perception-production research: Revisiting theoretical assumptions and methodological practices. Studies in Second Language Acquisition. https://doi.org/10.1017/S0272263121000371
- Neri, A.; Cucchiarini, C.; Strik, H.; Boves, L. (2002). The pedagogy-technology interface in computer assisted pronunciation training. Computer Assisted Language Learning. https://doi.org/10.1076/call.15.5.441.13473
- Ngo, T. T.-N.; Chen, H. H.-J.; Lai, K. K.-W. (2024). The effectiveness of automatic speech recognition in ESL/EFL pronunciation: A meta-analysis. ReCALL. https://doi.org/10.1017/S0958344023000113
- NPR (2009). Do You Speak Na'vi? Giving Voice To 'Avatar' Aliens. NPR, 15 December 2009. https://www.npr.org/2009/12/15/121350582/do-you-speak-navi-giving-voice-to-avatar-aliens [web source, cited as "NPR 2009"; URL seen in search results]
- Okrand, M. (1985). The Klingon Dictionary. Pocket Books. https://en.wikiversity.org/wiki/Klingon/Canon [book, not in Crossref; confirmed from search results listing it as Klingon canon]
- Okrand, M. (1997). Klingon for the Galactic Traveler. Pocket Books. https://klingonska.org/canon/1997-11-01-kgt.txt [book, not in Crossref; confirmed from search results]
- Olson, D. J.; Offerman, H. M. (2021). Maximizing the effect of visual feedback for pronunciation instruction: A comparative analysis of three approaches. Journal of Second Language Pronunciation. https://doi.org/10.1075/jslp.20005.ols
- Perrachione, T. K.; Lee, J.; Ha, L. Y. Y.; Wong, P. C. M. (2011). Learning a novel phonological contrast depends on interactions between individual differences and training paradigm design. The Journal of the Acoustical Society of America. https://doi.org/10.1121/1.3593366
- Peterson, D. J. (2014). Living Language Dothraki: A Conversational Language Course Based on the Hit Original HBO Series Game of Thrones. Living Language (Random House). [book, not in Crossref; title confirmed from a search summary]
- piper-plus contributors (2026). piper-plus (README and comparison table). GitHub. https://github.com/ayutaz/piper-plus/ [web source, cited as "piper-plus 2026"; URL seen in search results]
- Readium Foundation (n.d.). SpeechSynthesis in browsers and OSes. readium.org. https://readium.org/speech/docs/WebSpeech.html [web source, cited as "Readium n.d."; URL seen in search results]
- Rogerson-Revell, P. M. (2021). Computer-Assisted Pronunciation Training (CAPT): Current issues and future directions. RELC Journal. https://doi.org/10.1177/0033688220977406
- Saito, K. (2013). Reexamining effects of form-focused instruction on L2 pronunciation development: The role of explicit phonetic information. Studies in Second Language Acquisition. https://doi.org/10.1017/S0272263112000666
- Saito, K.; Plonsky, L. (2019). Effects of second language pronunciation teaching revisited: A proposed measurement framework and meta-analysis. Language Learning. https://doi.org/10.1111/lang.12345
- Sakai, M.; Moorman, C. (2018). Can perception training improve the production of second language phonemes? A meta-analytic review of 25 years of perception training research. Applied Psycholinguistics. https://doi.org/10.1017/S0142716417000418
- Schreyer, C. (2011). Media, information technology, and language planning: what can endangered language communities learn from created language communities?. Current Issues in Language Planning. https://doi.org/10.1080/14664208.2011.604965
- Schreyer, C. (2015). The digital fandom of Na'vi speakers. Transformative Works and Cultures. https://doi.org/10.3983/twc.2015.0610
- Stericker, J. (2026). espeak-phonemes: English text to IPA phonemes using eSpeak NG, WASM-based, fast, offline. Codeberg. https://codeberg.org/jocelyn-stericker/espeak-phonemes [web source, cited as "Stericker 2026"; URL seen in search results]
- text2wav contributors (n.d.). text2wav (npm package: eSpeak NG compiled to JavaScript and WebAssembly). npm. https://npmjs.com/package/text2wav [web source, cited as "text2wav n.d."; URL seen in search results]
- The Chromium Authors (n.d.). The eSpeak-NG speech synthesis engine on ChromeOS. Chromium source documentation. https://chromium.googlesource.com/chromium/src/+/798e59c5275d4131797e8ea2e96e6c6000256b58/docs/accessibility/os/espeak.md [web source, cited as "Chromium n.d."; URL seen in search results]
- Thomson, R. I. (2011). Computer assisted pronunciation training: Targeting second language vowel perception improves pronunciation. CALICO Journal. https://doi.org/10.11139/cj.28.3.744-765
- Thomson, R. I. (2018). High Variability [Pronunciation] Training (HVPT): A proven technique about which every language teacher and learner ought to know. Journal of Second Language Pronunciation. https://doi.org/10.1075/jslp.17038.tho
- Thomson, R. I.; Derwing, T. M. (2015). The effectiveness of L2 pronunciation instruction: A narrative review. Applied Linguistics. https://doi.org/10.1093/applin/amu076
- Thuum.org (n.d.). Alphabet & Pronunciation (fan site; seen as a search summary only). thuum.org. https://www.thuum.org/learn/grammar/alphabet.php [web source, cited as "Thuum.org n.d."; URL seen in search results]
- Thuum.org forum (n.d.). Forum thread 310 (fan discussion of IPA values and the r sound; seen as a search summary only). thuum.org. https://www.thuum.org/viewthread.php?thread=310 [web source, cited as "Thuum.org forum n.d."; URL seen in search results]
- Trofimovich, P.; Isaacs, T.; Kennedy, S.; Saito, K.; Crowther, D. (2016). Flawed self-assessment: Investigating self- and other-perception of second language speech. Bilingualism: Language and Cognition. https://doi.org/10.1017/S1366728914000832
- Uchihara, T.; Karas, M.; Thomson, R. I. (2024). Does perceptual high variability phonetic training improve L2 speech production? A meta-analysis of perception-production connection. Applied Psycholinguistics. https://doi.org/10.1017/S0142716424000195
- Uchihara, T.; Karas, M.; Thomson, R. I. (2025). High variability phonetic training (HVPT): A meta-analysis of L2 perceptual training studies. Studies in Second Language Acquisition. https://doi.org/10.1017/S0272263125100879
- UESP contributors (2026). Lore:Dragon Language (revision 3619598 of 2026-08-24, read from the repository snapshot). The Unofficial Elder Scrolls Pages (UESP). https://en.uesp.net/wiki/Lore:Dragon_Language [web source, cited as "UESP 2026"; read from the repository snapshot]
- Vandergrift, L.; Goh, C. C. M. (2012). Teaching and Learning Second Language Listening: Metacognition in Action. Routledge. https://doi.org/10.4324/9780203843376
- Venkatagiri, H. S. (2003). Segmental intelligibility of four currently used text-to-speech synthesis methods. The Journal of the Acoustical Society of America. https://doi.org/10.1121/1.1558356
- Wang, X.; Munro, M. J. (2004). Computer-based training for learning English vowel contrasts. System. https://doi.org/10.1016/j.system.2004.09.011
- Wikimedia contributors (n.d.). Lingua Libre. Meta-Wiki (Wikimedia). https://meta.wikimedia.org/wiki/Lingua_Libre [web source, cited as "Wikimedia n.d."; URL seen in search results]
- Wilson, M. (2003). Discovery listening - improving perceptual processing. ELT Journal. https://doi.org/10.1093/elt/57.4.335
- Witt, S. M.; Young, S. J. (2000). Phone-level pronunciation scoring and assessment for interactive language learning. Speech Communication. https://doi.org/10.1016/S0167-6393(99)00044-8
- Zhang, X.; Cheng, B.; Zhang, Y. (2021). The role of talker variability in nonnative phonetic learning: A systematic review and meta-analysis. Journal of Speech, Language, and Hearing Research. https://doi.org/10.1044/2021_JSLHR-21-00181
