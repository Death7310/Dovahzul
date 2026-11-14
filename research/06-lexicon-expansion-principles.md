# Track 6: Principles for growing the lexicon, and the forge rules that follow

Date: 2026-11-14. Data: `research/data/core-concept-gaps.json`, built by `tools/analysis/core_concept_gaps.py`. Language facts are labelled canon (game text), semi-canon (official but not game text, as defined in `research/data/README.md`) or fan (wiki editors' readings).

## 1. Bottom line

- **Canon covers about half of any core-concept list.** Exact gloss matching finds 47% of Swadesh 207, 48% of Leipzig-Jakarta 100 and 51% of the 65 NSM primes; only 32%, 34% and 46% rest on words with a game-text reference. Missing: *what, where, how, if, because, other, thing, three* to *five*, most body parts, and basic verbs such as *drink, bite, laugh, pull, throw*.
- **The priority order must depend on the concept class.** Languages give basic concepts short, old, unanalysable roots and build the rest by compounding and derivation. "Compound before coining" is right for general and specialised vocabulary and wrong for the roughly 300 core concepts.
- **Canon already behaves like a natural lexicon, so its own statistics can be the forge's limits.** Frequent canon words are shorter (Spearman rho = -0.32; 3.2 letters at 20 or more tokens, 5.5 for single-occurrence words), about 10% of spellings split into other dictionary words, and all 136 words of power are monosyllabic (canon).
- **Coherent constructed languages share three things:** an immutable base, a tier label on every word, and one final authority that rules in batches. Drift followed reforms of the base (Ido), an unclear baseline (Lojban) and competing reconstructions (Cornish).
- **Approval does not create use.** Hebrew, Irish, Maori and Hawaiian committees all coined terms that speakers ignored. The forge needs a trial tier and a usage measure.
- **Most checks are mechanical.** Form legality, collisions, neighbour distance, length band, part resolution, tier computation and slot occupancy run offline. Semantic fit, transparency, lore fit and extensions of meaning need a person.
- **Name the tiers unambiguously.** Thuum.org uses "semi-canon" for fan words derived from canon roots; this repository uses it for official non-game sources.

## 2. Findings

### a. How much vocabulary, and which

Coverage research is on English. Reading comfortably needs about 98% of running words known, which takes 8,000 to 9,000 word families; unscripted speech at 98% takes 6,000 to 7,000 (Nation 2006). Laufer and Ravenhorst-Kalovski (2010) set a minimal threshold at 95% (4,000 to 5,000 families) and an optimal one at 98% (8,000). Schmitt, Jiang and Grabe (2011, n = 661) found comprehension rises linearly with coverage, with no threshold. Listening tolerates less: 95% sufficed for informal narratives (van Zeeland and Schmitt 2013; 36 native and 40 non-native listeners), and about 3,000 families reach roughly 95 to 96% of conversation (Adolphs and Schmitt 2003). Nation (2022) is the standard synthesis.

Core lists differ in basis:

| List | Basis | Use here |
|---|---|---|
| Swadesh 100 and 200 (Swadesh 1955) | Intuition about universal, stable meanings | Familiar checklist |
| Leipzig-Jakarta 100 (Tadmor 2009; Tadmor, Haspelmath and Taylor 2010) | Empirical: 41 languages, 1,460 meanings, scored on resistance to borrowing, representation, unanalysability and age | Best definition of "needs its own root" |
| NSM primes, 65 (Goddard and Wierzbicka 2014) | Claimed indefinable and universal | Defining vocabulary for a monolingual dictionary |
| New General Service Lists (Brezina and Gablasova 2015: 2,494 lemmas, about 80% coverage; Browne 2014: about 2,800 words, about 92%, developer-reported) | English corpus frequency | Ordering what to fill next |
| Basic English, 850 words (Ogden 1930 [UNVERIFIED]; Okrent 2009) | Engineered; depends on idiomatic verb phrases | Warning: a tiny root set hides complexity in phrases |
| Concepticon (List, Cysouw and Forkel 2016) | Links published lists to stable concept sets | Ready-made concept-ID scheme |

Borrowing data show where languages invent and where they import: loanwords average about 24% across the 41 languages, about 31% of nouns against 14% of verbs, and about 41% in religion and belief against 11 to 15% for sense perception, spatial relations, the body and kinship (Tadmor 2009).

### b. Gap analysis

Method: each concept has hand-written `accept` glosses (the concept itself) and `near` glosses (hyponym, other word class); the 725 normalised dictionary glosses are compared for exact equality. "Covered" means an accept hit, "partial" a near hit only.

| List | n | Covered | Partial | Missing | Covered by a game-referenced word |
|---|---|---|---|---|---|
| Swadesh 207 | 207 | 97 (46.9%) | 29 (14.0%) | 81 (39.1%) | 66 (31.9%) |
| Leipzig-Jakarta 100 | 100 | 48 (48.0%) | 11 (11.0%) | 41 (41.0%) | 34 (34.0%) |
| NSM primes | 65 | 33 (50.8%) | 15 (23.1%) | 17 (26.2%) | 30 (46.2%) |

- **Missing NSM primes:** SOMEONE, SOMETHING, KIND, PART, THE SAME, OTHER, DON'T WANT, FEEL, HAPPEN, FOR SOME TIME, MOMENT, WHERE/PLACE, ABOVE, NEAR, SIDE, BECAUSE, IF.
- **Missing from Swadesh:** *what, where, how; three, four, five*; 16 body parts (*ear, nose, foot, leg, knee, belly, neck, back, breast, heart, liver, skin, tail, horn, feather, guts*); 21 everyday verbs; *star, lake, salt, smoke, ash, dust, fog, fish, egg, leaf, root, seed*; *wide, thick, heavy, wet, dry, full, near, left, right*.
- **Partial cases need a ruling:** *mal* "little" (size or quantity?), *lot* "great" for BIG, *jot* "maw" for MOUTH, *nok* "lie", which a wiki remark (fan) says covers both "lie down" and "tell a lie", an English homonymy.
- **Canon is rich where core lists are silent:** war, death, honour, rule, the sky.

**List provenance and reliability.** All three lists were typed from my knowledge of the published lists, not downloaded: Concepticon and the World Loanword Database are outside this container's allow-list. Counts were checked (207, 100, 65). Membership reliability is high; label wording is unchecked. Diff against Concepticon's Swadesh-1952-200, Swadesh-1955-100, Tadmor-2009-100 and Goddard-2014-65 before freezing. Matching is conservative.

### c. How natural lexicons grow, and what they look like

**Processes.** In a 55-language survey, suffixation and compounding are the most widespread word-formation processes (Štekauer, Valera and Körtvélyessy 2012). Canon uses compounding heavily, head first: *zeymahzin* "companion" is *zeymah* "brother" + *zin* "honor" (canon words; fan analysis from UESP's Lore:Dragon Language page), and *maltiid* "brief" is glossed "little-time" (semi-canon). Sixty-nine of about 667 spellings split mechanically into other entries. The prefix *vo-* pairs with ten entries and the ending *-aan* with seven (string evidence only). Canon also extends meanings: *bo* is "flow, fly, move"; *jun* is "king" and "light".

**Length.** Frequent words are shorter in almost a thousand languages (Bentz and Ferrer-i-Cancho 2016; Petrini et al. 2023), and speakers shorten frequent items in a miniature lexicon only when under both time and accuracy pressure (Kanwal et al. 2017). Canon: rho = -0.32 over 594 types and 2,342 tokens, an indicative figure because word walls repeat formulas.

**Homophony and neighbours.** Reusing short forms is efficient (Piantadosi, Tily and Gibson 2012), yet real lexicons hold fewer homophones than their phonotactics predict (Trott and Bergen 2020), and sound mergers are resisted where they would collapse many minimal pairs (Wedel, Kaplan and Jackson 2013). Lexicons are also clumpier than chance (Dautriche, Mahowald, Gibson, Christophe and Piantadosi 2017); frequent words are more phonotactically typical with more minimal pairs across 96 languages (Mahowald et al. 2018); similar meanings have slightly similar forms across 100 languages (Dautriche, Mahowald, Gibson and Piantadosi 2017). Dense neighbourhoods slow recognition (Luce and Pisoni 1998; Vitevitch and Luce 1999) but helped adults learn new words (Storkel, Armbrüster and Hogan 2006). Wordlikeness judgements depend on both phonotactic probability and neighbours (Bailey and Hahn 2001) and can be modelled from the lexicon alone (Hayes and Wilson 2008). Canon three-letter spellings average 8.4 one-edit neighbours, four-letter 4.1, five-letter 0.8.

**Meaning structure.** Languages reuse a word for related concepts (François 2008), predictably from conceptual relatedness (Xu et al. 2020; Youn et al. 2016; Rzymski et al. 2020), most often for meanings that are related but not confusable (Brochhagen and Boleda 2022) and less when speakers need the distinction (Karjus et al. 2021). Canon has 32 English glosses shared by two or more entries (*aan, aar, zaam* all "slave"), so near-synonym sets are already canon.

**Sound symbolism.** Associations are real but probabilistic: 'small' with *i*, 'tongue' with *l*, 'nose' with *n*, 'round' with *r* across nearly two-thirds of the world's languages (Blasi et al. 2016); the bouba/kiki match holds for about seven in ten of 917 speakers of 25 languages, though not reliably in every language (Ćwiek et al. 2022); trilled /r/ marks 'rough' against 'smooth' (Winter et al. 2022). Iconicity concentrates in sensory, early-learned words (Winter et al. 2024; Monaghan et al. 2014); arbitrariness keeps words distinct (Dingemanse et al. 2015; Sidhu and Pexman 2018). The efficiency framing is reviewed in Gibson et al. (2019).

### d. Corpus planning in practice

Haugen (1966) and Cooper (1989) frame the cycle: select a norm, codify it, elaborate it, get it accepted. Acceptance is where committees fail.

- **Hebrew.** The Language Committee drew on Hebrew of all periods first, then Aramaic in Hebrew form, then new forms on Hebrew roots, then other Semitic roots (Fellman 1973). The Academy's committees propose and the plenum approves; most new words are a root in a pattern (Academy of the Hebrew Language, "How a Word is Born"; "Plenum And Committees"). Zuckermann (2003) documents coinages that lost to internationalisms and the camouflaged borrowing that succeeded; Cooper (1989) reviews studies where approved terms were known but unused. Revival came from ideology and transmission, not word supply (Spolsky 1995); Zuckermann and Walsh (2011) call purism counterproductive.
- **Icelandic.** Policy prefers native compounds, derivation and revived words given new senses (*sími* "telephone"), with adapted loans last; specialist word committees feed a public term bank (Hilmarsson-Dunn and Kristinsson 2010; Vikør 2010). Icelandic newspapers show the lowest share of imported words in the Nordic comparison (Graedler and Kvaran 2010), but English pressure in computing is rising (Jökulsdóttir et al. 2019).
- **Maori.** The Language Commission favoured native resources over transliterations (Harlow 2007). The mathematics lexicon shows the costs: competing terms, thin consultation, opaque coinages, and teachers who were themselves learners (Trinick and May 2013; Krägeloh and Neha 2014).
- **Hawaiian.** The Lexicon Committee (1987) combines existing words or adapts foreign ones; a neologism needs approval at two separate meetings (Walker et al. 2025). Its coinages are contested by some speakers (Hawai'i Public Radio 2020). Kimura and Counceller (2009) [UNVERIFIED: not in Crossref, not read] describe the methods.
- **Cornish and Irish.** Rival reconstructions split Cornish for two decades until an externally brokered Standard Written Form (Sayers 2012; Sayers and Renkó-Michelsén 2015). Official Irish terms estranged native speakers who saw them as artificial (Ní Ghearáin 2011).
- **Measuring uptake.** Terminometrics counts an approved term against all competitors for the same notion (Quirion 2003).

### e. Constructed-language governance

Peer-reviewed work is thin (Schreyer 2011, 2021); most of this is documentary.

| Language | Authority and process | Outcome |
|---|---|---|
| Klingon | Only Okrand's words are canon; the institute publishes each new word with its source (Klingon Language Institute, "New Klingon Words"; klingonska.org, "Archive of Okrandian Canon") | High coherence, slow growth, long-standing gaps (Okrent 2009) |
| Na'vi | Community Lexical Expansion Project submits anonymised proposals; Frommer accepts, edits or rejects (Kelutral.org; Schreyer 2011) | Faster growth, single voice |
| Esperanto | Untouchable *Fundamento* (1905); the Akademio officialises roots after use (Fiedler 2006; Blanke 2009) | Stable for over a century; the Ido reform schism weakened both sides (Garvía 2015) |
| Lojban | Baseline frozen in 1997, restated in 2002; closed root list, rule-built compounds, shape-marked loans; roots generated by a scoring algorithm (Logical Language Group 1997, 2002; Okrent 2009) | Scope and expiry of the freeze stayed disputed |
| Toki Pona | 120-word base (Lang 2014); the 2021 dictionary ratified community words by a usage survey with a 41 to 60% threshold (Lang 2021; sona pona wiki, "nimi ku") | Usage-based ratification works; new-word proliferation strains minimalism |
| Dothraki, High Valyrian | Sole creator derives words from a proto-language (Peterson 2015) | Coherent; depends on one person |
| Dovahzul fan practice | Thuum.org tiers: canon, semi-canon (derived from canon roots), non-canon (new roots); submissions cite a source or parts (Thuum.org manual, search summary only) | Precedent for tiers; terminology clash |

## 3. What this means for the app

**R1. Concept registry (confidence: high).** Every entry points to concept IDs: Concepticon IDs where they exist, local `DZ-` IDs for Elder Scrolls concepts. Fields: `id, gloss, definition, semantic_field, word_class, core_lists[], class (A|B|C), band`. Seed with the roughly 265 distinct concepts of the three lists, then a frequency list mapped to concepts. Evidence: List et al. 2016; the gap file.

**R2. Concept class sets the strategy ladder (high for the principle, medium for cut-offs).**
- **Class A (core lists, function words):** (1) existing word; (2) attested sense extension; (3) new short root. Compounds are rejected. Evidence: Tadmor et al. 2010; the length law.
- **Class B (general):** (1) existing word; (2) set phrase; (3) sense extension; (4) head-first compound of two or three approved roots; (5) derivation with a whitelisted affix; (6) new root, with written justification.
- **Class C (specialised, modern):** as B, new roots barred; borrowing only for in-universe proper names respelled to canon phonotactics. Evidence: Icelandic and Hebrew practice; Štekauer et al. 2012.
- Clipping only shortens an approved compound whose use has grown; both forms stay linked.

**R3. Root coinage (medium).** Generate candidates deterministically from a seed hashed from the concept ID, so every offline copy proposes the same list. Draw syllables from the "core" tier of `forge_profile` in `canon-phonotactics.json`. Accept if (a) every onset, nucleus and coda is game-attested; (b) the wordlikeness score is at or above the 25th percentile of non-decomposable canon words; (c) no collision with any word, inflected form or rune spelling in any tier; (d) at least two units from every word of the same class and field; (e) neighbour count within the canon maximum for its length (21 at two or three letters, 14 at four, 5 at five). Sound symbolism only breaks ties, from a short whitelist (*i* small, *r* rough or round, *l* tongue, *n* nose). First candidates for new meanings could be the 11 dictionary words with no recorded meaning; that is an inference for the owner. Evidence: Bailey and Hahn 2001; Hayes and Wilson 2008; Trott and Bergen 2020; Blasi et al. 2016.

**R4. Length by band (high for direction, medium for numbers).** Band 1 (class A): one syllable, at most 4 letters. Band 2: at most 2 syllables and 6 letters. Band 3: up to canon's 4 syllables and 12 letters. Words of power: one syllable. Recompute canon band means each build.

**R5. Duplicates and near-synonyms (medium).** Reject an identical form. If the concept already has an approved word at an equal or higher tier, the submission must name a differentiator (register, speaker, narrower sense); at most two forms per concept and register. A new sense for an existing word needs an edge in an offline colexification table or a canon precedent, plus human approval. Evidence: Xu et al. 2020; Brochhagen and Boleda 2022; canon's 32 shared glosses.

**R6. Tiers (high).** `game` (attested in game text); `official` (licensed guide, Bethesda list, developer statements); `derived` (approved, built only from higher-tier parts by listed rules); `coined` (approved new root); `proposed` (passed automatic checks, on trial); `local` (unsubmitted). A word's tier is the lowest of its parts. The forge never promotes into the first two. Approved words may be deprecated, never deleted or reassigned. Evidence: Klingon, Esperanto, Lojban.

**R7. Submission record (high).** Concept ID or new-concept request with definition; form and generated rune spelling; word class and inflection; strategy and parts by lexicon ID; literal gloss; the ladder steps tried and why they failed (pre-filled); two example sentences that parse using approved words; band; register; rule-set version; content hash; attached check report.

**R8. Process (medium).** Automatic validation; export as a file; trial as `proposed`, visibly marked; owner rulings in batches with a published reason and a second confirmation in a later batch (the Hawaiian two-meeting rule); a per-release usage ratio over the bundled corpus of contributed texts (Quirion 2003), with unused words flagged for deprecation.

**R9. Sequencing (medium; coverage figures transferred from English are inference).** Fill the 17 missing primes plus *what, how* and the numerals above one; then the remaining Leipzig-Jakarta and Swadesh gaps; then a 1,000-concept conversation core; then 3,000.

| Automatable offline | Needs human judgment |
|---|---|
| Phonotactic legality, wordlikeness, collisions (inflected and rune forms), neighbour distance, length against band, part resolution, compound order, tier computation, slot occupancy, example parsing, coverage dashboard, mirror-of-English flag | Whether the concept is needed, semantic fit and transparency, sense-extension plausibility, lore and register fit, synonym differentiators, taste |

## 4. Contested or weak evidence

- **Length and predictability.** Piantadosi, Tily and Gibson (2011) argued predictability beats frequency; Meylan and Griffiths (2021) found this depends on corpus and preprocessing, and Pimentel et al. (2023) found frequency predicts better in 13 languages. R4 uses frequency.
- **Coverage thresholds** are English-only and correlational; a 95% or 98% target is a convention.
- **NSM universality** is disputed, and the inventory has changed over time.
- **Neighbourhood effects** point both ways (recognition against learning), from small English-speaking samples. R3's distances are judgement calls anchored to canon.
- **Homophony avoidance** rests on simulated baselines; Piantadosi et al. (2012) argue ambiguity is functional.
- **Sound symbolism** effects are tendencies, absent in some languages.
- **Language-planning evidence** is case description without controlled comparison. One search result reported a 2023 German study in which borrowed neologisms were accepted more readily than native ones by younger speakers; I could not verify it and it is not in the references.
- **The canon statistics** rest on about 2,300 tokens and wiki spellings.

## 5. Gaps, and what was blocked

- Concepticon, the World Loanword Database and the colexification database are not reachable here. The lists were typed from memory; the colexification table for R5 must be downloaded and its licence checked.
- Thuum.org refuses automated requests; only a search summary was used.
- Not read in full: Kimura and Counceller (2009), the *Māmaka Kaiao* front matter, Harlow (1993, not in Crossref, dropped). No adoption-rate data for Icelandic committee coinages was found. Ogden (1930) and the Toki Pona books are not in Crossref.
- From memory, not re-verified: the borrowing percentages from Tadmor (2009).
- Treated briefly: Cornish, Dothraki and High Valyrian, Basic English, clipping, borrowing, calquing.
- The affix whitelist in R2 depends on Track 1's ruling on which canon endings are productive.

## 6. References

Generated from `research/refs/lexicon-expansion.json`; each line ends with its checker status. Checker result: verified 66, doi_resolves 1, manual 11, not_found 7. The seven not found are four books (Okrent 2009 and Peterson 2015, each with a registry-listed review; Lang 2014 and 2021, named in search results), Ogden 1930 and Kimura and Counceller 2009, both tagged [UNVERIFIED], and Walker et al. 2025, read from the ACL Anthology record. The eleven manual entries are web pages whose addresses appeared in search results; thuum.org was not fetched.

- Academy of the Hebrew Language (n.d.). How a Word is Born. en.hebrew-academy.org.il. https://en.hebrew-academy.org.il/?p=78 `ahl_word: manual`
- Academy of the Hebrew Language (n.d.). Plenum And Committees. en.hebrew-academy.org.il. https://en.hebrew-academy.org.il/?p=182 `ahl_plenum: manual`
- Adolphs, S.; Schmitt, N. (2003). Lexical coverage of spoken discourse. Applied Linguistics. doi:10.1093/applin/24.4.425 `adolphs2003: verified`
- Bailey, T. M.; Hahn, U. (2001). Determinants of Wordlikeness: Phonotactics or Lexical Neighborhoods?. Journal of Memory and Language. doi:10.1006/jmla.2000.2756 `bailey2001: verified`
- Bentz, C.; Ferrer-i-Cancho, R. (2016). Zipf's law of abbreviation as a language universal. Proceedings of the Leiden Workshop on Capturing Phylogenetic Algorithms for Linguistics. University of Tübingen. doi:10.15496/publikation-10057 `bentz2016: doi_resolves`
- Blanke, D. (2009). Causes of the relative success of Esperanto. Language Problems and Language Planning. doi:10.1075/lplp.33.3.04bla `blanke2009: verified`
- Blasi, D. E.; Wichmann, S.; Hammarström, H.; Stadler, P. F.; Christiansen, M. H. (2016). Sound-meaning association biases evidenced across thousands of languages. Proceedings of the National Academy of Sciences. doi:10.1073/pnas.1605782113 `blasi2016: verified`
- Brezina, V.; Gablasova, D. (2015). Is there a core general vocabulary? Introducing the New General Service List. Applied Linguistics. doi:10.1093/applin/amt018 `brezina2015: verified`
- Brochhagen, T.; Boleda, G. (2022). When do languages use the same word for different meanings? The Goldilocks principle in colexification. Cognition. doi:10.1016/j.cognition.2022.105179 `brochhagen2022: verified`
- Browne, C. (2014). A New General Service List: The better mousetrap we've been looking for?. Vocabulary Learning and Instruction. doi:10.7820/vli.v03.2.browne `browne2014: verified`
- Cooper, R. L. (1989). Language Planning and Social Change. Cambridge University Press. doi:10.1017/CBO9780511620812 `cooper1989: verified`
- Ćwiek, A.; Fuchs, S.; Draxler, C.; Asu, E. L.; Dediu, D.; Hiovain, K.; Kawahara, S.; Koutalidis, S.; Krifka, M.; Lippus, P.; Lupyan, G.; Oh, G. E.; Paul, J.; Petrone, C.; Ridouane, R.; Reiter, S.; Schümchen, N.; Szalontai, Á.; Ünal-Logacev, Ö.; Zeller, J.; Perlman, M.; Winter, B. (2022). The bouba/kiki effect is robust across cultures and writing systems. Philosophical Transactions of the Royal Society B. doi:10.1098/rstb.2020.0390 `cwiek2022: verified`
- Dautriche, I.; Mahowald, K.; Gibson, E.; Christophe, A.; Piantadosi, S. T. (2017). Words cluster phonetically beyond phonotactic regularities. Cognition. doi:10.1016/j.cognition.2017.02.001 `dautriche2017a: verified`
- Dautriche, I.; Mahowald, K.; Gibson, E.; Piantadosi, S. T. (2017). Wordform Similarity Increases With Semantic Similarity: An Analysis of 100 Languages. Cognitive Science. doi:10.1111/cogs.12453 `dautriche2017b: verified`
- Dingemanse, M.; Blasi, D. E.; Lupyan, G.; Christiansen, M. H.; Monaghan, P. (2015). Arbitrariness, Iconicity, and Systematicity in Language. Trends in Cognitive Sciences. doi:10.1016/j.tics.2015.07.013 `dingemanse2015: verified`
- Fellman, J. (1973). The Revival of a Classical Tongue: Eliezer Ben Yehuda and the Modern Hebrew Language. Mouton. doi:10.1515/9783110879100 `fellman1973: verified`
- Fiedler, S. (2006). Standardization and self-regulation in an international speech community: the case of Esperanto. International Journal of the Sociology of Language. doi:10.1515/IJSL.2006.005 `fiedler2006: verified`
- François, A. (2008). Semantic maps and the typology of colexification: Intertwining polysemous networks across languages. In Vanhove, M. (ed.), From Polysemy to Semantic Change. John Benjamins. doi:10.1075/slcs.106.09fra `francois2008: verified`
- Garvía, R. (2015). Esperanto and Its Rivals: The Struggle for an International Language. University of Pennsylvania Press. doi:10.9783/9780812291278 `garvia2015: verified`
- Gibson, E.; Futrell, R.; Piantadosi, S. T.; Dautriche, I.; Mahowald, K.; Bergen, L.; Levy, R. (2019). How Efficiency Shapes Human Language. Trends in Cognitive Sciences. doi:10.1016/j.tics.2019.02.003 `gibson2019: verified`
- Goddard, C.; Wierzbicka, A. (2014). Words and Meanings: Lexical Semantics across Domains, Languages, and Cultures. Oxford University Press. doi:10.1093/acprof:oso/9780199668434.001.0001 `goddard2014: verified`
- Graedler, A.-L.; Kvaran, G. (2010). Foreign influence on the written language in the Nordic language communities. International Journal of the Sociology of Language. doi:10.1515/ijsl.2010.029 `graedler2010: verified`
- Harlow, R. (2007). Māori: A Linguistic Introduction. Cambridge University Press. doi:10.1017/CBO9780511618697 `harlow2007: verified`
- Haugen, E. (1966). Dialect, Language, Nation. American Anthropologist. doi:10.1525/aa.1966.68.4.02a00040 `haugen1966: verified`
- Hawai'i Public Radio (2020). There's craft, conflict in creating new 'ōlelo Hawai'i words. Hawai'i Public Radio, 5 February 2020. https://www.hawaiipublicradio.org/general-assignment/2020-02-05/theres-craft-conflict-in-creating-new-lelo-hawai-i-words `hpr2020: manual`
- Hayes, B.; Wilson, C. (2008). A Maximum Entropy Model of Phonotactics and Phonotactic Learning. Linguistic Inquiry. doi:10.1162/ling.2008.39.3.379 `hayes2008: verified`
- Hilmarsson-Dunn, A.; Kristinsson, A. P. (2010). The language situation in Iceland. Current Issues in Language Planning. doi:10.1080/14664208.2010.538008 `hilmarsson2010: verified`
- Jökulsdóttir, T. F.; Ingason, A. K.; Sigurjónsdóttir, S.; Rögnvaldsson, E. (2019). Um nýyrði sem tengjast tölvum og tækni. Orð og tunga. doi:10.33112/ordogtunga.21.6 `jokulsdottir2019: verified`
- Kanwal, J.; Smith, K.; Culbertson, J.; Kirby, S. (2017). Zipf's Law of Abbreviation and the Principle of Least Effort: Language users optimise a miniature lexicon for efficient communication. Cognition. doi:10.1016/j.cognition.2017.05.001 `kanwal2017: verified`
- Karjus, A.; Blythe, R. A.; Kirby, S.; Wang, T.; Smith, K. (2021). Conceptual Similarity and Communicative Need Shape Colexification: An Experimental Study. Cognitive Science. doi:10.1111/cogs.13035 `karjus2021: verified`
- Kelutral.org (n.d.). kelutral.org: About (describes the Lexical Expansion Project). kelutral.org. https://kelutral.org/about `kelutral_about: manual`
- Kimura, L.; Counceller, A. G. L. (2009). Indigenous new words creation: Perspectives from Alaska and Hawai'i. In Reyhner, J. & Lockard, L. (eds.), Indigenous Language Revitalization: Encouragement, Guidance & Lessons Learned. Northern Arizona University. https://listserv.linguistlist.org/pipermail/ilat/2014-August/009090.html `kimura2009: not_found` [UNVERIFIED: not in Crossref and not read; title and authors seen in a search result]
- Klingon Language Institute (n.d.). New Klingon Words. kli.org. https://www.kli.org/about-klingon/new-klingon-words/e/ `kli_newwords: manual`
- klingonska.org (n.d.). Archive of Okrandian Canon. klingonska.org. https://klingonska.org/canon/ `klingonska_canon: manual`
- Krägeloh, C. U.; Neha, T. N. (2014). Lexical expansion and terminological planning in indigenous and planned languages: Comparisons between Te Reo Māori and Esperanto. Language Problems and Language Planning. doi:10.1075/lplp.38.1.04kra `krageloh2014: verified`
- Lang, S. (2014). Toki Pona: The Language of Good. Tawhid. `lang2014: not_found` [book, not in Crossref; named in search results]
- Lang, S. (2021). Toki Pona Dictionary. Tawhid. `lang2021: not_found` [book, not in Crossref; named in search results]
- Laufer, B.; Ravenhorst-Kalovski, G. C. (2010). Lexical threshold revisited: Lexical text coverage, learners' vocabulary size and reading comprehension. Reading in a Foreign Language. doi:10.64152/10125/66648 `laufer2010: verified`
- List, J.-M.; Cysouw, M.; Forkel, R. (2016). Concepticon: A resource for the linking of concept lists. Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC 2016). doi:10.63317/2kc62t62893m https://aclanthology.org/L16-1379/ `list2016: verified`
- Logical Language Group (1997). 1997 Baseline Announcement. lojban.org wiki. https://tiki.lojban.org/1997+Baseline+Announcement `lojban_baseline1997: manual`
- Logical Language Group (2002). Official Baseline Statement. lojban.org wiki. https://tiki.lojban.org/Official+Baseline+Statement `lojban_baseline2002: manual`
- Luce, P. A.; Pisoni, D. B. (1998). Recognizing spoken words: The neighborhood activation model. Ear and Hearing. doi:10.1097/00003446-199802000-00001 `luce1998: verified`
- Mahowald, K.; Dautriche, I.; Gibson, E.; Piantadosi, S. T. (2018). Word Forms Are Structured for Efficient Use. Cognitive Science. doi:10.1111/cogs.12689 `mahowald2018: verified`
- Meylan, S. C.; Griffiths, T. L. (2021). The Challenges of Large-Scale, Web-Based Language Datasets: Word Length and Predictability Revisited. Cognitive Science. doi:10.1111/cogs.12983 `meylan2021: verified`
- Monaghan, P.; Shillcock, R. C.; Christiansen, M. H.; Kirby, S. (2014). How arbitrary is language?. Philosophical Transactions of the Royal Society B. doi:10.1098/rstb.2013.0299 `monaghan2014: verified`
- Nation, I. S. P. (2006). How large a vocabulary is needed for reading and listening?. Canadian Modern Language Review. doi:10.3138/cmlr.63.1.59 `nation2006: verified`
- Nation, I. S. P. (2022). Learning Vocabulary in Another Language. Cambridge University Press (3rd ed.). doi:10.1017/9781009093873 `nation2022: verified`
- Ní Ghearáin, H. (2011). The problematic relationship between institutionalised Irish terminology development and the Gaeltacht speech community: dynamics of acceptance and estrangement. Language Policy. doi:10.1007/s10993-011-9216-5 `nighearain2011: verified`
- Ogden, C. K. (1930). Basic English: A General Introduction with Rules and Grammar. Kegan Paul, Trench, Trubner. `ogden1930: not_found` [UNVERIFIED: book, not in Crossref, not confirmed by search]
- Okrent, A. (2009). In the Land of Invented Languages. Spiegel & Grau. `okrent2009: not_found` [book, not in Crossref; the checker's nearest match is a published review of it, doi:10.1111/j.1548-1395.2012.01128.x]
- Peterson, D. J. (2015). The Art of Language Invention: From Horse-Lords to Dark Elves, the Words Behind World-Building. Penguin Books. `peterson2015: not_found` [book, not in Crossref; the checker's nearest match is a published review of it, doi:10.1075/lplp.00008.gob]
- Petrini, S.; Casas-i-Muñoz, A.; Cluet-i-Martinell, J.; Wang, M.; Bentz, C.; Ferrer-i-Cancho, R. (2023). Direct and indirect evidence of compression of word lengths. Zipf's law of abbreviation revisited. Glottometrics. doi:10.53482/2023_54_407 `petrini2023: verified`
- Piantadosi, S. T.; Tily, H.; Gibson, E. (2011). Word lengths are optimized for efficient communication. Proceedings of the National Academy of Sciences. doi:10.1073/pnas.1012551108 `piantadosi2011: verified`
- Piantadosi, S. T.; Tily, H.; Gibson, E. (2012). The communicative function of ambiguity in language. Cognition. doi:10.1016/j.cognition.2011.10.004 `piantadosi2012: verified`
- Pimentel, T.; Meister, C.; Wilcox, E. G.; Mahowald, K.; Cotterell, R. (2023). Revisiting the Optimality of Word Lengths. Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing. doi:10.18653/v1/2023.emnlp-main.137 `pimentel2023: verified`
- Quirion, J. (2003). Methodology for the design of a standard research protocol for measuring terminology usage. Terminology. doi:10.1075/term.9.1.03qui `quirion2003: verified`
- Rzymski, C.; Tresoldi, T.; Greenhill, S. J.; Wu, M.-S.; Schweikhard, N. E.; Koptjevskaja-Tamm, M.; Gast, V.; Bodt, T. A.; Hantgan, A.; Kaiping, G. A.; Chang, S.; Lai, Y.; Morozova, N.; Arjava, H.; Hübler, N.; Koile, E.; Pepper, S.; Proos, M.; Van Epps, B.; Blanco, I.; Hundt, C.; Monakhov, S.; Pianykh, K.; Ramesh, S.; Gray, R. D.; Forkel, R.; List, J.-M. (2020). The Database of Cross-Linguistic Colexifications, reproducible analysis of cross-linguistic polysemies. Scientific Data. doi:10.1038/s41597-019-0341-x `rzymski2020: verified`
- Sayers, D. (2012). Standardising Cornish: The politics of a new minority language. Language Problems and Language Planning. doi:10.1075/lplp.36.2.01say `sayers2012: verified`
- Sayers, D.; Renkó-Michelsén, Z. (2015). Phoenix from the Ashes: Reconstructed Cornish in relation to Einar Haugen's four-step model of language standardisation. Sociolinguistica. doi:10.1515/soci-2015-0004 `sayers2015: verified`
- Schmitt, N.; Jiang, X.; Grabe, W. (2011). The percentage of words known in a text and reading comprehension. The Modern Language Journal. doi:10.1111/j.1540-4781.2011.01146.x `schmitt2011: verified`
- Schreyer, C. (2011). Media, information technology, and language planning: what can endangered language communities learn from created language communities?. Current Issues in Language Planning. doi:10.1080/14664208.2011.604965 `schreyer2011: verified`
- Schreyer, C. (2021). Constructed Languages. Annual Review of Anthropology. doi:10.1146/annurev-anthro-101819-110152 `schreyer2021: verified`
- Sidhu, D. M.; Pexman, P. M. (2018). Five mechanisms of sound symbolic association. Psychonomic Bulletin & Review. doi:10.3758/s13423-017-1361-1 `sidhu2018: verified`
- sona pona wiki contributors (n.d.). nimi ku. sona.pona.la. https://sona.pona.la/wiki/nimi_ku `sona_nimiku: manual`
- Spolsky, B. (1995). Conditions for Language Revitalization: A Comparison of the Cases of Hebrew and Maori. Current Issues in Language and Society. doi:10.1080/13520529509615444 `spolsky1995: verified`
- Štekauer, P.; Valera, S.; Körtvélyessy, L. (2012). Word-Formation in the World's Languages: A Typological Survey. Cambridge University Press. doi:10.1017/CBO9780511895005 `stekauer2012: verified`
- Storkel, H. L.; Armbrüster, J.; Hogan, T. P. (2006). Differentiating phonotactic probability and neighborhood density in adult word learning. Journal of Speech, Language, and Hearing Research. doi:10.1044/1092-4388(2006/085) `storkel2006: verified`
- Swadesh, M. (1955). Towards greater accuracy in lexicostatistic dating. International Journal of American Linguistics. doi:10.1086/464321 `swadesh1955: verified`
- Tadmor, U. (2009). Loanwords in the world's languages: Findings and results. In Haspelmath, M. & Tadmor, U. (eds.), Loanwords in the World's Languages: A Comparative Handbook. De Gruyter Mouton. doi:10.1515/9783110218442.55 `tadmor2009: verified`
- Tadmor, U.; Haspelmath, M.; Taylor, B. (2010). Borrowability and the notion of basic vocabulary. Diachronica. doi:10.1075/dia.27.2.04tad `tadmor2010: verified`
- Thuum.org (n.d.). Contributor's manual (thuum.org, a community for the dragon language of The Elder Scrolls V: Skyrim). thuum.org; seen only as a search-result summary, the site refuses automated requests. https://www.thuum.org/manual.php `thuum_manual: manual`
- Trinick, T.; May, S. (2013). Developing a Māori language mathematics lexicon: challenges for corpus planning in indigenous language contexts. Current Issues in Language Planning. doi:10.1080/14664208.2013.835149 `trinick2013: verified`
- Trott, S.; Bergen, B. (2020). Why do human languages have homophones?. Cognition. doi:10.1016/j.cognition.2020.104449 `trott2020: verified`
- UESP contributors (2026). Lore:Dragon Language (revision 3619598 of 2026-08-24). The Unofficial Elder Scrolls Pages (UESP). https://en.uesp.net/wiki/Lore:Dragon_Language `uesp_dragon_language: manual`
- van Zeeland, H.; Schmitt, N. (2013). Lexical coverage in L1 and L2 listening comprehension: The same or different from reading comprehension?. Applied Linguistics. doi:10.1093/applin/ams074 `vanzeeland2013: verified`
- Vikør, L. S. (2010). Language purism in the Nordic countries. International Journal of the Sociology of Language. doi:10.1515/ijsl.2010.028 `vikor2010: verified`
- Vitevitch, M. S.; Luce, P. A. (1999). Probabilistic Phonotactics and Neighborhood Activation in Spoken Word Recognition. Journal of Memory and Language. doi:10.1006/jmla.1998.2618 `vitevitch1999: verified`
- Walker, S.; Wu, W.; Torres Fischer, B.; Kimura, L. (2025). Kuene: A Web Platform for Facilitating Hawaiian Word Neologism. Proceedings of the Eight Workshop on the Use of Computational Methods in the Study of Endangered Languages (ComputEL-8), pp. 182-187. Association for Computational Linguistics. https://aclanthology.org/2025.computel-main.21/ `walker2025: not_found` [not in Crossref; record read from the ACL Anthology]
- Wedel, A.; Kaplan, A.; Jackson, S. (2013). High functional load inhibits phonological contrast loss: A corpus study. Cognition. doi:10.1016/j.cognition.2013.03.002 `wedel2013: verified`
- Winter, B.; Lupyan, G.; Perry, L. K.; Dingemanse, M.; Perlman, M. (2024). Iconicity ratings for 14,000+ English words. Behavior Research Methods. doi:10.3758/s13428-023-02112-6 `winter2024: verified`
- Winter, B.; Sóskuthy, M.; Perlman, M.; Dingemanse, M. (2022). Trilled /r/ is associated with roughness, linking sound and touch across spoken languages. Scientific Reports. doi:10.1038/s41598-021-04311-7 `winter2022: verified`
- Xu, Y.; Duong, K.; Malt, B. C.; Jiang, S.; Srinivasan, M. (2020). Conceptual relations predict colexification across languages. Cognition. doi:10.1016/j.cognition.2020.104280 `xu2020: verified`
- Youn, H.; Sutton, L.; Smith, E.; Moore, C.; Wilkins, J. F.; Maddieson, I.; Croft, W.; Bhattacharya, T. (2016). On the universal structure of human lexical semantics. Proceedings of the National Academy of Sciences. doi:10.1073/pnas.1520752113 `youn2016: verified`
- Zuckermann, G. (2003). Language Contact and Lexical Enrichment in Israeli Hebrew. Palgrave Macmillan. doi:10.1057/9781403938695 `zuckermann2003: verified`
- Zuckermann, G.; Walsh, M. (2011). Stop, Revive, Survive: Lessons from the Hebrew Revival Applicable to the Reclamation, Maintenance and Empowerment of Aboriginal Languages and Cultures. Australian Journal of Linguistics. doi:10.1080/07268602.2011.532859 `zuckermann2011: verified`
