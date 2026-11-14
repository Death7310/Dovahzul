# Track 7: Encoding Dovahzul as a machine-checkable, offline rule system

Evidence base: peer-reviewed computational linguistics and language-learning technology, checked against Crossref; the canon data in `research/data/`; one new measurement on that data (section 2a). Tool facts rest on documentation, not scholarship: **[docs]** means a search result showed it, **[unchecked]** means it is my recollection only. In depth: a, c, f and the architecture. Briefly: b, d, e, g.

## 1. Bottom line

- **Ship a rulebook, not a framework.** Put every rule in versioned, hashed JSON and interpret it with small deterministic TypeScript engines, mirrored by a Python reference implementation in CI. No third-party grammar runtime is needed at launch.
- **Hard rules decide; scores advise.** In 10-fold cross-validation on the 597 canon roots, requiring an attested word-initial onset and word-final coda kept 97.5% of unseen canon roots and rejected 65% of scrambled ones. The bigram score separates the two well on average (AUC 0.90), yet a cut-off that keeps 95% of real roots still passes 45% of scrambles.
- **Simple models win at this size.** An add-k unit bigram matched or beat Witten-Bell, interpolated, trigram and positional scores. Keep the existing model, train it on canon roots only, and freeze it.
- **Morphology needs a table, not a transducer.** A few suffix rules, a full-form table generated at build time and a guarded compound splitter cover the language.
- **The composition checker judges form against the rulebook and nothing else.** Three tiers (tokens, local patterns, chart parse with error rules) and three verdicts (conforms, specific error, cannot analyse). It cannot judge meaning, style, or anything the owner has not ruled on.
- **Borrow Grammatical Framework's design, not its runtime.** One abstract syntax with Dovahzul and English linearisations gives generation, graded exercises and translation checking with many right answers. The GF TypeScript runtime is a credible alternative that needs a short trial first.
- **Duplicates are caught by concept identifiers that a person picks and a machine compares:** Concepticon first, Open English WordNet second, local identifiers for Tamriel.
- **Blocking prerequisite.** Only 15 of 657 dictionary rows state a part of speech (`research/data/README.md`; UESP 2026). Syntax checking needs an owner-ruled word class for every entry.

## 2. Findings

### a. Phonotactic well-formedness

**What the literature shows.** Wordlikeness judgments track the probability of a word's parts. Coleman and Pierrehumbert (1997) found that a whole-word probability predicts acceptability better than the worst single part; Frisch, Large and Pisoni (2000) added an independent effect of length. Vitevitch and Luce (2004) supply the standard psycholinguistic measure, position-specific segment and biphone probabilities; Mayer, Kondur and Sundara (2025) extend it to any word list. Bailey and Hahn (2001) found that phonotactic probability and lexical neighbourhood (Luce and Pisoni 1998) each explain variance the other does not, and that much stays unexplained. Hayes and Wilson (2008) learn weighted constraints over feature classes by maximum entropy and report a close fit to English onset ratings; Albright (2009) found bigrams over feature classes the best of the models he compared. Daland et al. (2011) showed that segment n-gram models without features and syllable structure cannot grade unattested clusters. Wilson and Gallagher (2018) address the small-lexicon problem directly: a learner must separate systematic gaps from accidental ones. Rogers and Pullum (2011) describe the strictly local class, defined by permitted factors of length k: the formal home for hard constraints.

Chen and Goodman (1999) found interpolated and Kneser-Ney smoothing better than additive smoothing for word n-grams. That result concerns vocabularies of thousands of types and need not transfer to 41 spelling units.

**New measurement (mine, this session).** I ran a 10-fold cross-validation over the 597 non-decomposable canon roots, reusing the segmentation of `tools/analysis/phonotactics.py`. Each held-out root was scored by a model trained on the other folds and compared with shuffles of its own units and with uniform random unit strings of the same length.

| Score | AUC vs shuffles | AUC vs random |
|---|---|---|
| Unit bigram, add-k (k from 0.01 to 1), mean log2 per transition | 0.89 to 0.91 | 0.97 |
| Same, summed instead of averaged | 0.78 | 0.82 |
| Bigram, Witten-Bell or Jelinek-Mercer | 0.81 to 0.88 | 0.97 |
| Trigram, Witten-Bell | 0.90 | 0.97 |
| Positional unit plus biphone (Vitevitch-Luce style) | 0.75 | 0.91 |
| Count of unseen bigrams | 0.82 | 0.96 |
| Worst single transition | 0.81 | 0.93 |
| Neighbourhood density (edit distance 1) | 0.72 | 0.74 |

Also, 20% of held-out canon roots contain a bigram absent from the training folds (65% with 100 training words, 46% with 200, 26% with 400), which confirms Track 1: an unattested bigram cannot be an error. Bigram AUC against shuffles rises from 0.83 at 100 training words to 0.90 at 537.

Limits: the negatives are synthetic, there are no human judgments, no confidence intervals were computed, and differences of 0.01 mean nothing.

Maximum entropy is not worth its cost here (inference). It needs a feature system, and the language has no official phonemic description, so every feature would be a project convention.

### b. Morphology

Two-level morphology (Koskenniemi 1984) and the proof that rewrite rules denote regular relations (Kaplan and Kay 1994) underlie the finite-state toolkits foma (Hulden 2009) and HFST (Lindén et al. 2011), built for languages with large paradigms and interacting alternations. The paradigm tradition instead writes inflection as functions from a lemma to a table (Forsberg and Ranta 2004), with "smart paradigms" that infer the class from the form (Détrez and Ranta 2012), and exports a full-form lexicon.

Dovahzul's attested morphology is a plural (double the final letter, add *e*), possessive suffixes, a perfect in *-aan*, two prefixes and head-initial compounding (wiki grammar notes, semi-canon; Track 1). At five to ten forms per lemma, 5,000 lemmas give a table under 50,000 rows (my estimate). A table lookup is exact and easy to test; a transducer adds a build dependency and no capability.

Compounds are the hard part. The string test in `phonotactics.py` finds 69 "decomposable" words and over-detects (*bahlok* = *bah* + *lok*). Koehn and Knight (2003) met the same problem in German: splitting into every known part over-splits, and candidates must be ranked. With no usable frequency data, the ranking here has to be by rule.

### c. Syntax checking for learner text

**Formalisms.** Earley's algorithm (1970) parses any context-free grammar, including ambiguous and left-recursive ones, and its chart keeps partial analyses. Constraint Grammar (Karlsson 1990; Bick and Didriksen 2015) removes wrong readings from morphologically ambiguous running text by contextual rules. It pays off where morphology is rich and coverage must be broad, which is not this case. Grammatical Framework (GF) separates an abstract syntax from per-language linearisations and compiles to a portable format that small runtimes interpret (Ranta 2004; Angelov, Bringert and Ranta 2010; Ranta et al. 2020). Controlled natural languages show that a precisely defined subset of a language can have an exact grammar (Kuhn 2014).

**Error feedback.** LanguageTool gives useful feedback without full parsing: tokenise, tag, match declarative patterns, emit a message tied to a rule; rules are tested against corpora for false alarms (Miłkowski 2010). Parser-based learner systems add mal-rules, productions that describe a known error and carry its diagnosis (Schneider and McCoy 1998; Foster and Vogel 2004; Heift and Schulze 2007). Feedback that names the error helps: Nagata (1993) found metalinguistic parser feedback better than "wrong word here" feedback for Japanese particles in a small classroom study, and Heift (2004) found that the most explicit feedback type produced the most learner uptake. Amaral and Meurers (2011) argue from deployment that analysis is reliable only when the activity constrains what the learner may write.

**Many right answers.** Katinskaia, Ivanova and Yangarber (2019) document "multiple admissibility" in a learning system built on rule-based analysis: answers that differ from the expected one and are still correct. Duolingo's shared task treats the whole set of acceptable translations as the thing to model (Mayhew et al. 2020). A language with optional tense and plural marking makes this worse (inference).

**What a rule-based checker can and cannot judge** (my synthesis):

| Reliable | Reliable only in closed tasks | Not judgeable |
|---|---|---|
| Every token is a lexicon form, a licensed inflection or a registered compound | Meaning equals a target (compare abstract trees) | Meaning of free text |
| Rune and Latin spellings agree | Tense, number or possessor matches a prompt | Plausibility, idiom, register |
| Suffix formation follows the rule | | Whether an unparsed sentence is wrong or only beyond the grammar |
| Word order matches a codified rule; known error patterns | | Anything in the 34 unruled gap areas of `grammar-gaps.json` |

### d. Generating practice material

Reiter and Dale (2000) place templates and grammar-based realisation on one continuum; Gatt and Krahmer (2018) confirm that rule-based generation remains the choice where control matters more than variety. Three precedents fit.

- **Exercises from a grammar.** Perez-Beltrachini, Gardent and Kruszewski (2012) generate sentences from a grammar and use the derivation to select those that meet a teaching constraint, then turn them into gap-fill and word-order items.
- **Level control by grammar fragment.** MULLE gives each lesson its own GF grammar and lexicon. Learners build translations by editing through word menus, so every reachable state is grammatical and no free-text diagnosis is needed (Lange and Ljunglöf 2018).
- **Sense through semantic typing.** The MOLTO phrasebook avoids nonsense by giving its abstract syntax semantic types (Ranta, Enache and Détrez 2012).

Template-based item generation is also standard in assessment (Gierl, Lai and Turner 2012). None of these papers reports learning outcomes; they establish feasibility only.

### e. Semantic duplicates without AI

WordNet groups word senses into synsets linked by relations (Miller 1995). Open English WordNet is its open successor (McCrae et al. 2019); the 2024 edition has 120,630 synsets under CC BY 4.0 (Open English WordNet Community 2024 [docs]). Concepticon links published concept lists to stable concept sets, 2,495 in its first release (List, Cysouw and Forkel 2016); version 3.4.0 is CC BY 4.0 (List et al. 2025 [docs]) and uses the CLDF format (Forkel et al. 2018). The colexification database (Rzymski et al. 2020) records which concept pairs languages express with one word, which is evidence for extending an existing word instead of coining one.

No rule can reliably pick the right sense of an English gloss (inference from the fineness of WordNet senses). A person must choose the identifier; the machine's job is the comparison.

### f. Governance as engineering

- **Reproducibility.** A build is verifiable when identical inputs give bit-identical outputs; timestamps, ordering and locale are the usual leaks (Lamb and Zacchiroli 2022).
- **Versioning.** In Maven Central about one third of releases broke compatibility, minor releases as often as major ones (Raemaekers, van Deursen and Visser 2017). A version number means something only if a machine enforces it.
- **Regression.** Grammar engineering uses test suites of grammatical and ungrammatical items, profiled again after every change (Oepen and Flickinger 1998). Continuous integration is associated with faster integration in open-source projects (Hilton et al. 2016; observational).
- **Exceptions.** Catala encodes law as general rules plus explicit, prioritised exceptions, so the code keeps the shape of the text and every exception is traceable (Merigoux, Chataing and Protzenko 2021).
- **Rationale.** Decision records capture issue, decision, status, alternatives and consequences (Tyree and Akerman 2005).

### g. Tools that run offline in a browser (documentation, not scholarship)

| Tool | Kind | Licence | Status found | Fit |
|---|---|---|---|---|
| gf-typescript | GF runtime in pure TypeScript, no server | Not confirmed for this repository. GF runtime and resource library: LGPL and BSD; compiler: GPL (Grammatical Framework developers 2025, licence file [docs]) | Replaces the JavaScript runtime deprecated in GF 3.12 of 2025-08-08 (Grammatical Framework developers 2025, release notes); repository last updated February 2024 (Grammatical Framework developers 2024) [docs] | Strong for generation and translation; weak error diagnosis; needs the GF compiler at build time |
| Ohm | PEG parser | MIT [unchecked] | v17.4.0 listed 2026-02; active (Ohm developers 2026 [docs]) | Good for a rule-file notation. A PEG returns one parse, so not for the language itself |
| nearley | Earley parser | MIT [unchecked] | 2.20.1, about four years without a release (Cloudsmith 2026 [docs]) | Right algorithm, stale package |
| foma | Finite-state compiler in C | Apache-2.0 per Wikipedia contributors (2026), GPLv2 per an older ACL wiki page: read the LICENSE file (Hulden 2026) [docs] | JavaScript runtime published (Hulden, Silfverberg and Francom 2013); a browser port of pyfoma exists (foma developers 2026 [docs]) | Only if morphology outgrows a table |
| CG-3 | Constraint grammar in C++ | GPL version 3 or later; other licences need an exception (GrammarSoft 2024 [docs]) | No WebAssembly build found | Licence and need both argue against |

## 3. What this means for the app

**R1. Rulebook as data (confidence: high).** One directory of JSON files, each validated by a JSON Schema: orthography, phonotactic profile (generated by `phonotactics.py`), morphology, lexicon, grammar, mal-rules, patterns, concepts, overrides. Every rule carries `id`, `status` (canon, semi-canon, owner-ruling, convention), `evidence` (corpus ids), `since`, `supersedes`, `examples.ok`, `examples.bad` and `message_id`. Evidence: Miłkowski 2010; Merigoux et al. 2021; Tyree and Akerman 2005.

**R2. Verdicts are pure functions (high).** `validate(submission, rulebook, overrides)` returns a verdict that records the rulebook version and SHA-256, the input hash, each finding (rule, severity, evidence) and the overrides applied. No clock, no locale-dependent sorting, no floating point in decisions: the build writes transition scores as integers, round(1000 × log2 p), because floating-point logarithms can differ between engines (engineering knowledge, uncited). Evidence: Lamb and Zacchiroli 2022.

**R3. Forge validator stages (high for 0 to 2, 4, 5; medium for 3 and 6).**

0. Schema.
1. Orthography: units from the inventory, no *c*, apostrophe only in *u'u*; Latin-to-rune round trip; fail if the rune spelling equals that of another word.
2. Hard phonotactics: the word syllabifies, and every onset, nucleus and coda is in the canon profile. Tier `core` (5 or more roots) passes; `marginal` (2 to 4) passes with a note; `single` and unattested need an owner override. A word of power must be one syllable (canon: all 136 are).
3. Advisory score: the existing add-0.5 unit bigram, shown as a percentile band against leave-one-out canon scores, plus the list of neighbours at edit distance 1 as a confusability warning. It never blocks.
4. Collisions: homograph; equal to an inflected form of an existing word; splittable into existing words without being declared a compound.
5. Declared structure: a compound or derivation must rebuild exactly from listed parts by a listed rule.
6. Concept: an identifier is required. Fail on the same identifier and word class as an approved word unless declared a synonym with a register tag; warn on a neighbouring synset or a colexified concept.

Output: pass, fail or needs-review. Evidence: section 2a; Rogers and Pullum 2011; Daland et al. 2011.

**R4. Freeze the phonotactic training set (medium; inference).** Train on canon roots only. If approved coinages feed back, the model drifts toward its own output.

**R5. Morphology engine (high).** Build-time paradigm functions emit a full-form table (form to lemma, features, rule id). The compound splitter is dynamic programming over that table: parts of at least three letters, at most four parts, linker *se*, registered compounds before computed splits, fewest parts first. An unregistered split is reported as "possible new compound", never as an error. Evidence: Forsberg and Ranta 2004; Koehn and Knight 2003.

**R6. Composition checker (medium).** Tier 1: every token analysed by R5. Tier 2: local pattern rules over tagged tokens, including predicted transfer errors such as an English plural *-s* or possessive *'s*. Tier 3: an Earley parser over a context-free grammar with atomic features expanded at load time, plus mal-rules. Write the parser in-house (300 to 500 lines, my estimate) to avoid a stale dependency. Verdicts: conforms to rulebook vX; specific error (rule, span, message, example); cannot analyse, which is never shown as "wrong". Each message shows the rule's status, so learners see whether they broke canon or an owner ruling. Evidence: Miłkowski 2010; Schneider and McCoy 1998; Heift and Schulze 2007; Nagata 1993; Heift 2004.

**R7. Two composition modes (medium).** Guided: an editor that offers only the next words the grammar allows. Free: text checked afterwards by R6. Start beginners in guided mode. Evidence: Lange and Ljunglöf 2018; Amaral and Meurers 2011; Kuhn 2014.

**R8. Abstract syntax for generation and answer matching (medium).** Each grammar rule is a typed constructor with a Dovahzul and an English linearisation. Generation is seeded top-down expansion limited to rules and lexemes at or below the learner's level, with semantic classes on nouns and verb frames to block nonsense. Every generated sentence carries its rule and lexeme ids for the scheduler. For translation items, parse the answer and accept it if any parse equals the target tree once features the rulebook marks optional are ignored. Evidence: Ranta 2004; Ranta, Enache and Détrez 2012; Perez-Beltrachini et al. 2012; Katinskaia et al. 2019.

**R9. Concept registry (medium).** Use a Concepticon identifier where one exists, otherwise an Open English WordNet synset, otherwise a local `DZ-` identifier (as in Track 6). Gloss normalisation is deterministic: lower-case, strip parentheses and leading *to*, *a*, *the*, lemmatise by suffix rules plus an exception list, look up candidates. The submitter picks; the reviewer confirms. Ship a slim index in the forge only. Keep CC BY 4.0 data and the wiki-derived CC BY-SA 2.5 data in separate files with their own notices.

**R10. Version by verdict flip (high).** CI re-validates the whole approved lexicon, all canon corpus records and the test suites under the candidate rulebook. An approved word that now fails, or a changed parse of a canon sentence, makes the release major and must be listed. Rules that flip nothing are minor; message text is a patch. Evidence: Raemaekers et al. 2017; Oepen and Flickinger 1998.

**R11. Overrides are records (high).** An append-only log holds submission hash, rules waived, rationale, rulebook version, signer and date; only the owner signs. The validator reads the log, so an overridden verdict is as reproducible as any other. An override never edits a rule; repeated overrides of one rule should open a rule-change proposal. Evidence: Merigoux et al. 2021.

**R12. CI gates (high).** Each rule has at least one passing and one failing example, run as tests. Canon tokens must be 100% analysable after names and listed misspellings. Canon-sentence parse coverage is reported, not required. Python and TypeScript verdicts must be byte-identical on a conformance set.

**R13. Try GF before fixing the grammar format (medium).** Two to three days: 30 rules compiled to PGF JSON and loaded in gf-typescript; measure bundle size, parse time and failure information; read the licence. Adopt it only if errors can be tied to specific rules.

**Order of work.** Part-of-speech ruling; R1 to R3 (stages 0 to 5); R10 to R12; R9 and stage 6; R5; R6 tiers 1 and 2; R8 and tier 3; R7.

**Limits.** A pass means "conforms to rulebook vX", not "good Dovahzul". The edge filter wrongly stops about one canon-like root in forty, which is what overrides are for. In free composition, silence is not approval. Duplicate detection is only as good as the human's choice of sense.

## 4. Contested or weak evidence

- Whether phonotactic knowledge is gradient or categorical is unsettled (Daland et al. 2011), and my cross-validation, one small data set, has no human ratings and runs against Chen and Goodman (1999) on smoothing.
- No study of phonotactic modelling on a constructed language was found. Hayes and Wilson (2008) and Albright (2009) tested on English.
- The feedback studies are old, small and single-language (Nagata 1993; Heift 2004). I quote no effect sizes because I could not re-read the papers here; Track 9 covers the wider feedback literature.
- Raemaekers et al. (2017) studied Java libraries and Merigoux et al. (2021) studied law; applying them to a language rulebook is analogy.
- Tool status comes from search summaries, not from reading the repositories.

## 5. Gaps, and anything that was blocked

- The search budget (10 of 10) ran out before Peggy, Chevrotain, Lezer, tree-sitter, HFST and in-browser Prolog systems (an option for unification grammars) could be checked; these parser generators target programming languages and are not recommended here. The licence of gf-typescript was not found; sources disagree on foma's.
- A paper on a North Sámi constraint-grammar checker was dropped because it could not be confirmed.
- Six ACL Anthology papers have no DOI and are absent from Crossref. Their records were confirmed at aclanthology.org; they are tagged in the reference list.
- Concepticon and the colexification data cannot be downloaded here; the current number of concept sets is unverified.
- No learner error corpus exists for Dovahzul. Mal-rules must start from predicted English transfer errors, and an offline app collects no data unless learners export it.
- Generation of connected graded texts by rule was not reviewed. Hand-written texts checked by R6 are the safe course.
- The cross-validation script is outside the repository at `/tmp/claude-0/-home-user-Dovahzul/1c946a51-f492-50bd-a1e0-30c6c0c49ea4/scratchpad/cv_phonotactics.py`, because this task could write only its two output files. It should become a `--cv` option of `phonotactics.py`.

## 6. References

Status after each entry is from `research/refs/formal-rules.check.json`.

- Albright, A. (2009). Feature-based generalisation as a source of gradient acceptability. Phonology. doi:10.1017/S0952675709001705 `albright2009: verified`
- Amaral, L. A.; Meurers, D. (2011). On using intelligent computer-assisted language learning in real-life foreign language teaching and learning. ReCALL. doi:10.1017/S0958344010000261 `amaral2011: verified`
- Angelov, K.; Bringert, B.; Ranta, A. (2010). PGF: A portable run-time format for type-theoretical grammars. Journal of Logic, Language and Information. doi:10.1007/s10849-009-9112-y `angelov2010: verified`
- Bailey, T. M.; Hahn, U. (2001). Determinants of wordlikeness: Phonotactics or lexical neighborhoods?. Journal of Memory and Language. doi:10.1006/jmla.2000.2756 `bailey2001: verified`
- Bick, E.; Didriksen, T. (2015). CG-3 — Beyond classical constraint grammar. Proceedings of the 20th Nordic Conference of Computational Linguistics (NODALIDA 2015). https://aclanthology.org/W15-1807/ `bick2015: not_found` [UNVERIFIED by Crossref; record confirmed at aclanthology.org]
- Chen, S. F.; Goodman, J. (1999). An empirical study of smoothing techniques for language modeling. Computer Speech & Language. doi:10.1006/csla.1999.0128 `chen1999: verified`
- Cloudsmith (2026). nearley npm package listing (2.20.1, last stable release about four years old). Cloudsmith Navigator. https://cloudsmith.com/navigator/npm/nearley `nearley_npm: manual`
- Coleman, J.; Pierrehumbert, J. (1997). Stochastic phonological grammars and acceptability. Computational Phonology: Third Meeting of the ACL Special Interest Group in Computational Phonology. https://aclanthology.org/W97-1107/ `coleman1997: not_found` [UNVERIFIED by Crossref; record confirmed at aclanthology.org]
- Daland, R.; Hayes, B.; White, J.; Garellek, M.; Davis, A.; Norrmann, I. (2011). Explaining sonority projection effects. Phonology. doi:10.1017/S0952675711000145 `daland2011: verified`
- Détrez, G.; Ranta, A. (2012). Smart paradigms and the predictability and complexity of inflectional morphology. Proceedings of the 13th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2012). https://aclanthology.org/E12-1066/ `detrez2012: not_found` [UNVERIFIED by Crossref; record confirmed at aclanthology.org]
- Earley, J. (1970). An efficient context-free parsing algorithm. Communications of the ACM. doi:10.1145/362007.362035 `earley1970: verified`
- foma developers (2026). pyfoma JavaScript port (runs in the browser). fomafst.github.io. https://fomafst.github.io/pyfomajs `pyfoma_js: manual`
- Forkel, R.; List, J.-M.; Greenhill, S. J.; Rzymski, C.; Bank, S.; Cysouw, M.; Hammarström, H.; Haspelmath, M.; Kaiping, G. A.; Gray, R. D. (2018). Cross-Linguistic Data Formats, advancing data sharing and re-use in comparative linguistics. Scientific Data. doi:10.1038/sdata.2018.205 `forkel2018: verified`
- Forsberg, M.; Ranta, A. (2004). Functional morphology. Proceedings of the Ninth ACM SIGPLAN International Conference on Functional Programming (ICFP 2004). doi:10.1145/1016850.1016879 `forsberg2004: verified`
- Foster, J.; Vogel, C. (2004). Parsing ill-formed text using an error grammar. Artificial Intelligence Review. doi:10.1023/B:AIRE.0000036259.68818.1e `foster2004: verified`
- Frisch, S. A.; Large, N. R.; Pisoni, D. B. (2000). Perception of wordlikeness: Effects of segment probability and length on the processing of nonwords. Journal of Memory and Language. doi:10.1006/jmla.1999.2692 `frisch2000: verified`
- Gatt, A.; Krahmer, E. (2018). Survey of the state of the art in natural language generation: Core tasks, applications and evaluation. Journal of Artificial Intelligence Research. doi:10.1613/jair.5477 `gatt2018: verified`
- Gierl, M. J.; Lai, H.; Turner, S. R. (2012). Using automatic item generation to create multiple-choice test items. Medical Education. doi:10.1111/j.1365-2923.2012.04289.x `gierl2012: verified`
- GrammarSoft ApS (2024). Constraint Grammar Manual (CG-3), Chapter 2: License. edu.visl.dk. https://edu.visl.dk/cg3/chunked/license.html `cg3_license: manual`
- Grammatical Framework developers (2024). gf-typescript: TypeScript runtime for Grammatical Framework (repository README). GitHub. https://github.com/GrammaticalFramework/gf-typescript `gf_typescript: manual`
- Grammatical Framework developers (2025). gf-core releases (GF 3.12, 2025-08-08). GitHub. https://github.com/GrammaticalFramework/gf-core/releases `gf_releases: manual`
- Grammatical Framework developers (2025). GF Resource Grammar Library LICENSE and GF licence summary. grammaticalframework.org. https://www.grammaticalframework.org/lib/LICENSE `gf_license: manual`
- Hayes, B.; Wilson, C. (2008). A maximum entropy model of phonotactics and phonotactic learning. Linguistic Inquiry. doi:10.1162/ling.2008.39.3.379 `hayes2008: verified`
- Heift, T. (2004). Corrective feedback and learner uptake in CALL. ReCALL. doi:10.1017/S0958344004001120 `heift2004: verified`
- Heift, T.; Schulze, M. (2007). Errors and Intelligence in Computer-Assisted Language Learning: Parsers and Pedagogues. Routledge. doi:10.4324/9780203012215 `heift2007: verified`
- Hilton, M.; Tunnell, T.; Huang, K.; Marinov, D.; Dig, D. (2016). Usage, costs, and benefits of continuous integration in open-source projects. Proceedings of the 31st IEEE/ACM International Conference on Automated Software Engineering (ASE 2016). doi:10.1145/2970276.2970358 `hilton2016: verified`
- Hulden, M. (2009). Foma: a finite-state compiler and library. Proceedings of the Demonstrations Session at EACL 2009. doi:10.3115/1609049.1609057 `hulden2009: verified`
- Hulden, M. (2026). foma: finite-state compiler and C library (repository). GitHub. https://github.com/mhulden/foma `foma_repo: manual`
- Hulden, M.; Silfverberg, M.; Francom, J. (2013). Finite state applications with Javascript. Proceedings of the 19th Nordic Conference of Computational Linguistics (NODALIDA 2013). https://aclanthology.org/W13-5641/ `hulden2013: not_found` [UNVERIFIED by Crossref; record confirmed at aclanthology.org]
- Kaplan, R. M.; Kay, M. (1994). Regular models of phonological rule systems. Computational Linguistics. https://aclanthology.org/J94-3001/ `kaplan1994: not_found` [UNVERIFIED by Crossref; record confirmed at aclanthology.org]
- Karlsson, F. (1990). Constraint grammar as a framework for parsing running text. COLING 1990 Volume 3: Papers presented to the 13th International Conference on Computational Linguistics. doi:10.3115/991146.991176 `karlsson1990: verified`
- Katinskaia, A.; Ivanova, S.; Yangarber, R. (2019). Multiple admissibility: Judging grammaticality using unlabeled data in language learning. Proceedings of the 7th Workshop on Balto-Slavic Natural Language Processing. doi:10.18653/v1/w19-3702 `katinskaia2019: verified`
- Koehn, P.; Knight, K. (2003). Empirical methods for compound splitting. Proceedings of the 10th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2003). doi:10.3115/1067807.1067833 `koehn2003: verified`
- Koskenniemi, K. (1984). A general computational model for word-form recognition and production. Proceedings of the 10th International Conference on Computational Linguistics (COLING 1984). doi:10.3115/980431.980529 `koskenniemi1984: verified`
- Kuhn, T. (2014). A survey and classification of controlled natural languages. Computational Linguistics. doi:10.1162/COLI_a_00168 `kuhn2014: verified`
- Lamb, C.; Zacchiroli, S. (2022). Reproducible builds: Increasing the integrity of software supply chains. IEEE Software. doi:10.1109/MS.2021.3073045 `lamb2022: verified`
- Lange, H.; Ljunglöf, P. (2018). MULLE: A grammar-based Latin language learning tool to supplement the classroom setting. Proceedings of the 5th Workshop on Natural Language Processing Techniques for Educational Applications. doi:10.18653/v1/w18-3715 `lange2018: verified`
- Lindén, K.; Axelson, E.; Hardwick, S.; Pirinen, T. A.; Silfverberg, M. (2011). HFST—Framework for compiling and applying morphologies. Systems and Frameworks for Computational Morphology (Communications in Computer and Information Science 100). doi:10.1007/978-3-642-23138-4_5 `linden2011: verified`
- List, J.-M.; Cysouw, M.; Forkel, R. (2016). Concepticon: A resource for the linking of concept lists. Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC 2016). doi:10.63317/2kc62t62893m https://aclanthology.org/L16-1379 `list2016: verified`
- List, J.-M.; Tjuka, A.; Blum, F.; Kučerová, A.; Barrientos Ugarte, C.; Rzymski, C.; Greenhill, S.; Forkel, R. (eds.) (2025). CLLD Concepticon 3.4.0 (licence statement in the site footer). concepticon.clld.org. https://concepticon.clld.org/contributors/tjukaannika `concepticon_site: manual`
- Luce, P. A.; Pisoni, D. B. (1998). Recognizing spoken words: The neighborhood activation model. Ear and Hearing. doi:10.1097/00003446-199802000-00001 `luce1998: verified`
- Mayer, C.; Kondur, A.; Sundara, M. (2025). UCI Phonotactic Calculator: An online tool for computing phonotactic metrics. Behavior Research Methods. doi:10.3758/s13428-025-02725-z https://phonotactics.socsci.uci.edu `mayer2025: verified`
- Mayhew, S.; Bicknell, K.; Brust, C.; McDowell, B.; Monroe, W.; Settles, B. (2020). Simultaneous translation and paraphrase for language education. Proceedings of the Fourth Workshop on Neural Generation and Translation. doi:10.18653/v1/2020.ngt-1.28 `mayhew2020: verified`
- McCrae, J. P.; Rademaker, A.; Bond, F.; Rudnicka, E.; Fellbaum, C. (2019). English WordNet 2019 – An open-source WordNet for English. Proceedings of the 10th Global Wordnet Conference. doi:10.18653/v1/2019.gwc-1.31 `mccrae2019: verified`
- Merigoux, D.; Chataing, N.; Protzenko, J. (2021). Catala: A programming language for the law. Proceedings of the ACM on Programming Languages. doi:10.1145/3473582 `merigoux2021: verified`
- Miller, G. A. (1995). WordNet: A lexical database for English. Communications of the ACM. doi:10.1145/219717.219748 `miller1995: verified`
- Miłkowski, M. (2010). Developing an open-source, rule-based proofreading tool. Software: Practice and Experience. doi:10.1002/spe.971 `milkowski2010: verified`
- Nagata, N. (1993). Intelligent computer feedback for second language instruction. The Modern Language Journal. doi:10.1111/j.1540-4781.1993.tb01980.x `nagata1993: verified`
- Oepen, S.; Flickinger, D. P. (1998). Towards systematic grammar profiling. Test suite technology 10 years after. Computer Speech & Language. doi:10.1006/csla.1998.0105 `oepen1998: verified`
- Ohm developers (2026). Ohm release files (v17.4.0, listing dated 2026-02-12; v17.5.0 named as latest). SourceForge mirror of the Ohm GitHub releases. https://sourceforge.net/projects/ohm.mirror/files/v17.4.0/ `ohm_mirror: manual`
- Open English WordNet Community (2024). Open English WordNet 2024 (lexicon metadata and licence). en-word.net. https://en-word.net/xml/lemma/license `oewn_license: manual`
- Perez-Beltrachini, L.; Gardent, C.; Kruszewski, G. (2012). Generating grammar exercises. Proceedings of the Seventh Workshop on Building Educational Applications Using NLP. https://aclanthology.org/W12-2017/ `perez2012: not_found` [UNVERIFIED by Crossref; record confirmed at aclanthology.org]
- Raemaekers, S.; van Deursen, A.; Visser, J. (2017). Semantic versioning and impact of breaking changes in the Maven repository. Journal of Systems and Software. doi:10.1016/j.jss.2016.04.008 `raemaekers2017: verified`
- Ranta, A. (2004). Grammatical Framework. Journal of Functional Programming. doi:10.1017/S0956796803004738 `ranta2004: verified`
- Ranta, A.; Angelov, K.; Gruzitis, N.; Kolachina, P. (2020). Abstract syntax as interlingua: Scaling up the Grammatical Framework from controlled languages to robust pipelines. Computational Linguistics. doi:10.1162/coli_a_00378 `ranta2020: verified`
- Ranta, A.; Enache, R.; Détrez, G. (2012). Controlled language for everyday use: The MOLTO phrasebook. Controlled Natural Language (CNL 2010), Lecture Notes in Computer Science 7175. doi:10.1007/978-3-642-31175-8_7 `ranta2012: verified`
- Reiter, E.; Dale, R. (2000). Building Natural Language Generation Systems. Cambridge University Press. doi:10.1017/CBO9780511519857 `reiter2000: verified`
- Rogers, J.; Pullum, G. K. (2011). Aural pattern recognition experiments and the subregular hierarchy. Journal of Logic, Language and Information. doi:10.1007/s10849-011-9140-2 `rogers2011: verified`
- Rzymski, C.; Tresoldi, T.; Greenhill, S. J.; Wu, M.-S.; Schweikhard, N. E.; Koptjevskaja-Tamm, M.; Gast, V.; Bodt, T. A.; Hantgan, A.; Kaiping, G. A.; Chang, S.; Lai, Y.; Morozova, N.; Arjava, H.; Hübler, N.; Koile, E.; Pepper, S.; Proos, M.; Van Epps, B.; Blanco, I.; Hundt, C.; Monakhov, S.; Pianykh, K.; Ramesh, S.; Gray, R. D.; Forkel, R.; List, J.-M. (2020). The Database of Cross-Linguistic Colexifications, reproducible analysis of cross-linguistic polysemies. Scientific Data. doi:10.1038/s41597-019-0341-x `rzymski2020: verified`
- Schneider, D.; McCoy, K. F. (1998). Recognizing syntactic errors in the writing of second language learners. Proceedings of the 36th Annual Meeting of the Association for Computational Linguistics and 17th International Conference on Computational Linguistics (COLING-ACL 1998). doi:10.3115/980432.980765 `schneider1998: verified`
- Tyree, J.; Akerman, A. (2005). Architecture decisions: Demystifying architecture. IEEE Software. doi:10.1109/MS.2005.27 `tyree2005: verified`
- UESP contributors (2026). Lore:Dragon Language (revision 3619598 of 2026-08-24, read from the repository snapshot). The Unofficial Elder Scrolls Pages. https://en.uesp.net/wiki/Lore:Dragon_Language `uesp2026: manual`
- Vitevitch, M. S.; Luce, P. A. (2004). A Web-based interface to calculate phonotactic probability for words and nonwords in English. Behavior Research Methods, Instruments, & Computers. doi:10.3758/BF03195594 `vitevitch2004: verified`
- Wikipedia contributors (2026). Foma (software). Wikipedia. https://en.wikipedia.org/wiki/Foma_(software) `foma_wikipedia: manual`
- Wilson, C.; Gallagher, G. (2018). Accidental gaps and surface-based phonotactic learning: A case study of South Bolivian Quechua. Linguistic Inquiry. doi:10.1162/ling_a_00285 `wilson2018: verified`
