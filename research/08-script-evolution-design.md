# Track 8: How writing systems evolve, and how to extend the dragon script by natural descent

Date: 2026-11-14. Language facts are labelled **canon** (game text or official publication, as reported in the UESP snapshot), **semi-canon** (developer statements, font implementation) or **fan**. Inferences are marked *Inference*.

## 1. Bottom line

- **No rune shape could be inspected in this session**: the repository has no glyph outlines or descriptions and none could be fetched under the access rules. Shape claims rest on one developer statement (semi-canon): one to three talon scratches, sometimes a dewclaw dot. A person must annotate the 34 glyphs (about an hour) before any distinctiveness rule can be calibrated; the schema is in section 3.
- **The canon script already behaves like a natural script in three ways:** at most three scratches per sign (the cross-script average is about three), a skewed frequency profile (8 runes cover 55% of wall text), and two-letter runes that cover almost every vowel-letter sequence in the lexicon while ignoring consonant clusters.
- **The real gaps are numerals and punctuation, not letters.** The dictionary has one number word (*gein*, "one"); wall text has no punctuation; the official font spends the digit keys on two-letter runes. Add digits and four or five marks first, and no letter runes in the first release.
- **Derive every new glyph from an old one by a named operator** (dot, add or drop a stroke, fuse, shorten, repeat), record its parent, and reject it if it is closer to any existing glyph than the closest pair of canon runes are to each other. That threshold calibrates itself from canon.
- **Test every stroke constraint against the 34 canon glyphs**; relax any that canon breaks in more than about 10% of runes.
- **Teach the runes with tracing and writing from memory, not recognition alone.** Across 50 experiments handwriting training improved recognition of new graphs by g = 0.58, or g = 0.37 against visual-only controls (Araújo et al. 2022).
- **Store text as rune tokens, render through Basic Multilingual Plane private-use code points, and add a Latin-letter ligature path for typing.** Automatic ligatures cannot be trusted for correctness: canon writes the same letter pair both ways.
- **Build an original typeface from the project's own stroke skeletons** with open tooling (FontForge 2025-10-09 confirmed current).

## 2. Findings by sub-question

### a. How scripts change (treated in depth for cuneiform and runes; briefly for ogham and borrowing)

**Tool and surface dictate the stroke.** Mesopotamian writing began with impressed number marks and signs drawn into clay with a point; within a few centuries scribes built every sign from impressions of a cut reed, each leaving a deep head and a tapering tail, the wedge (Schmandt-Besserat 1992; Taylor 2011). Signs lost their pictorial shape and later lost wedges. In the standard handbook account, stone-cutters then reproduced a wedge that only clay and reed naturally make (Taylor 2011; Coulmas 2003). *Inference:* a claw dragged across stone gives a tapered slash, and once mortals carve or pen the script the taper survives as style.

**Runes show both shrinking and regrowth.** The 24-rune older fuþark was cut to 16 runes around the eighth century although the sound inventory had grown, leaving one rune for pairs such as k/g and t/d; the causes are debated (Barnes 2012; Schulte 2015). The staveless runes later dropped the main vertical and kept only the distinguishing marks. From about 1000 CE carvers repaired the ambiguity with dotted runes: a dot turned i into e, k into g, u into y. Anglo-Saxon carvers instead enlarged the row by modifying existing runes. Bind-runes fuse two runes on one stave, and dividers (dots, small crosses) were used irregularly (Barnes 2012).

**Ogham** builds 20 letters from one to five strokes in four positions relative to a stone's edge, and later added five supplementary letters (*forfeda*) of a different design, several for vowel pairs (McManus 1991). It is the limiting case of a systematic script: economical, but letters differ only by stroke count.

**General mechanisms**, each with a design use here (Coulmas 2003; Houston 2012; Meletis and Dürscheid 2022):

| Mechanism | Real example | Use in the forge |
|---|---|---|
| Cursivisation | hieroglyphic to hieratic to demotic | everyday hand derived from monumental skeletons |
| Simplification with use | Vai script, 1830s onward (Kelly et al. 2021) | frequent new signs must be simplest |
| Diacritic | dotted runes; Arabic consonant dots | DOT operator with the dewclaw mark |
| Modification, splitting | G from C; J from I; W from VV | ADD and DROP operators |
| Ligature becoming a letter | &, æ; bind-runes | FUSE operator for optional digraph runes |
| Borrowing | runes from a Mediterranean alphabet | disallowed: no Latin shapes |

**Numerals** are usually a separate system. Chrisomalis (2010) classifies over a hundred notations by whether signs within a power are repeated (cumulative) or distinct (ciphered) and whether powers are summed or positional; tally-like systems group repeated strokes in small sets. **Punctuation and word separation** arrive late and serve readers: Roman interpuncts, then unseparated script, then spaces spread by insular scribes from the late seventh century (Saenger 1997); pause marks began as readers' aids (Parkes 2016).

### b. Quantitative and cognitive findings on letter shapes

- **Stroke count.** Across more than 100 writing systems characters average about three strokes whatever the inventory size, with about 50% redundancy; numeral systems average about two (Changizi and Shimojo 2005). The developers' "one to three scratches" rule (semi-canon) sits inside that band.
- **Topology.** Stroke junction types (L, T, X) occur across scripts in the proportions found in natural scenes (Changizi et al. 2006), in line with the view that scripts adapt to the visual system (Dehaene and Cohen 2007).
- **Complexity and inventory size.** In over 47,000 characters from 133 scripts, larger inventories have more complex characters, and there was no cross-script evidence that older scripts are simpler (Miton and Morin 2021). GraphCom offers a four-part complexity measure applied to 131 written languages (Chang et al. 2018). Letter identification efficiency falls as perimetric complexity rises (Pelli et al. 2006).
- **Change over time.** Vai letters simplified over 170 years, the complex ones most (Kelly et al. 2021), but Chinese characters grew more complex on the authors' measures (Han et al. 2022). In the laboratory, signs simplify when copied from memory along a chain (Tamariz and Kirby 2015) or used interactively (Garrod et al. 2007).
- **Frequency.** More frequent characters are graphically simpler across a broad range of scripts (Koshevoy et al. 2023).
- **Systematicity is low in real scripts.** From 19,591 letter classifications across 43 scripts, Kim et al. (2025) found that letters reuse features less economically than phoneme inventories do. Shape-sound correlations are small in evolved scripts (Jee et al. 2022), though naive observers guess some vowel glyphs above chance (Turoman and Styles 2017), and Roman letters are only partly featural (Primus 2004). *Inference:* a fully regular extension would look engineered, not inherited.
- **Orientation.** In 116 scripts cardinal strokes are over-represented and letters rarely mix cardinal with oblique strokes (Morin 2018); obliques are also discriminated less well (Appelle 1972). A claw script is oblique-heavy, so its angles should be few and far apart.
- **Confusability.** Letter confusions follow shared features (Mueller and Weidemann 2012; Wiley et al. 2016), and within-script similarity, mirror pairs especially, slows learners (Treiman and Kessler 2011).

### c. Featural analysis of the canon runes

**Verified from the repository data:**

- 34 runes: 25 single letters and 9 two-letter runes AA, AH, EI, EY, II, IR, OO, UU, UR (canon; UESP contributors 2026). A glyph for C and one on the "0" key exist in the font but not in the language (semi-canon). In Gnanadesikan's (2017) terms it is a fully vowelled alphabet with some single graphs for letter pairs.
- Construction rule (semi-canon; Miller 2011, archived on UESP): "combinations of one to three scratches, and sometimes the dot, which is like the dewclaw". A fan summary returned by search says "three or more slashes and dots"; the conflict cannot be settled without the glyphs.
- No case distinction (semi-canon).
- **Usage statistics, computed for this report** from 64 unique word-wall inscriptions (1,122 words, 4,453 rune tokens, mean 3.97 runes per word; about 1% of letters were not in rune-case and were skipped): O 11.6%, N 9.7, R 7.4, K 6.3, L 5.4, AH 5.1, D 5.1, AA 4.3, S 4.2, U 4.1, E 3.9, T 3.6, I 3.6, V 3.4, M 2.7, H 2.7, G 2.1, F 2.1, II 2.0, W 1.9, A 1.8, Z 1.8, B 1.2, P 0.9, Q 0.8, EY 0.6, EI 0.6, J 0.3, Y 0.3, IR 0.2, UU 0.1, OO 0.1, X 0.1, UR under 0.1. The top 8 cover 54.9%, the top 16 cover 83.1%. Two-letter runes are 13.0% of tokens.
- **The digraph runes are phonologically motivated, unevenly.** Among 646 dictionary headwords, the pairs with runes occur in 145 (aa), 116 (ah), 87 (ii), 31 (ey), 20 (ei), 14 (ir), 9 (oo), 6 (uu) and 4 (ur) headwords. Vowel pairs without a rune barely exist: au 4, ae 1, ia 1; ee, ai, oi, ie, ou none. Consonant pairs with no rune are common: ro 42, ar 31, kr 31, or 23, th 20, st 14.
- **Canon is inconsistent.** 14 wall tokens write a rune-eligible pair as two runes (IR 6, AH 4, OO 2, UR 1, EY 1; for example WAH, DIR, BORMAH and several names) against 578 written with the two-letter rune (2.4%). The wiki notes the same for SAH.
- The apostrophe of *Thu'um* is not written on walls (the wall spelling uses the UU rune).

**Not verifiable here:** strokes and dots per rune, stroke orientations, whether any two-letter rune is visually built from its component letters, mirror pairs, and whether the simplest runes are the frequent ones. My recollection (tapered slashes, mostly upright or oblique, small angular dots, two-letter runes not obvious compounds) is unverified and must not be relied on.

### d. Functional gaps

| Gap | Evidence | Priority |
|---|---|---|
| Numerals | only *gein* "one" in the dictionary; no numeral glyph; digit keys taken by digraph runes (semi-canon). A fan "Numbered" font with number runes exists (Thuum.org 2026; fan; shapes not seen) | 1 |
| Sentence and pause marks | wall text has none (14 hyphens, 2 commas, 1 full stop in 64 inscriptions, probably transcription artefacts); Latin-letter dialogue uses . ! , ? | 1 |
| Word divider | walls rely on gaps and line breaks | 2 (optional carved-style dot) |
| Emphasis | walls highlight the taught word by glow, not by a mark | 2 |
| Letters | every Latin letter has a rune; th (20 headwords), ng (5), sh (4) lack one; sound values are not in the data | 3, optional only |
| Faster hand | none attested | 3 |

### e. Design proposal

**Stroke grammar.** `Glyph := Slash{1..3} Dot{0..Dmax}`. A slash has orientation (upright, right-leaning, left-leaning, level), length (long, short), bend (straight, hooked) and an anchor in a 3 by 3 zone grid, and tapers from entry to exit. A dot occupies one zone. `Dmax` and the permitted angles are read off the canon annotation, not assumed.

**Operators**, in descending order of historical frequency: DOT (add or move one dot), ADD or DROP one slash, FUSE two glyphs that share a slash, SHORTEN, REPEAT (numerals only). Mirroring and rotation are not operators.

**Constraints.**

1. Claw budget: at most three slashes (semi-canon rule).
2. Distance: at least two feature edits from every existing glyph, and raster similarity (64 by 64 pixels, best overlap under shifts of up to 2 pixels) below the highest similarity found between any two canon runes.
3. No glyph may equal an existing one under reflection or half-turn (Treiman and Kessler 2011).
4. Complexity within the canon range on the GraphCom measures (Chang et al. 2018); marks and digits at or below the canon median (Pelli et al. 2006).
5. Frequency fit: the sign expected to be most frequent in a class is the simplest (Koshevoy et al. 2023).
6. Orientation: no new angle; a glyph does not mix more than two orientations (*inference* from Morin 2018, to be tested on canon).
7. Family resemblance without uniformity: signs of a class share one trait but differ from each other in at least two features (Kim et al. 2025; the ogham caution).

**Proposed additions (illustrative; none has been tested against canon shapes).** Tier I is the 34 canon runes, untouched.

| Tier and fictional era | Signs | Derivation | Precedent |
|---|---|---|---|
| II. Chisel (cult carvers keeping tallies and dates) | digits 1 to 9 as rakes of one, two or three short parallel slashes with zero, one or two dots (value = slashes + 3 x dots); a word-divider dot | REPEAT, DOT | tally numerals (Chrisomalis 2010); interpuncts (Saenger 1997) |
| III. Quill (mortal scribes) | zero; sentence end (two stacked dots); pause (one low tick); question and shout marks (sentence end plus a hooked or a long slash); emphasis ticks flanking a word; the everyday hand | DOT, ADD, SHORTEN | runic dividers and dotted runes (Barnes 2012); pause marks (Parkes 2016) |
| IV. Revival (the community) | optional fused runes TH, then NG, SH, AU | FUSE or DOT | bind-runes; ogham *forfeda* (McManus 1991) |

*Inference:* rakes of at most three strokes stay within what people count at a glance and suit the three-talon lore. This transparent scheme costs up to five marks per digit against a cross-script average of about two for numerals (Changizi and Shimojo 2005); a variant using dot position instead of dot count caps it at four. Tier IV signs never replace canon spellings.

**Everyday hand.** Define it as a deterministic transform of the monumental skeleton: a single-width line along each slash, strokes joined in stroke order where pen travel is short, dots as ticks, uniform slant, no joining between glyphs at first. Re-run constraint 2 on the result, because cursive forms lose distinctiveness.

### f. Learning a new script

- **Handwriting.** Araújo et al. (2022): 50 experiments, 1,525 participants, g = 0.58 for graph recognition after handwriting training; 0.78 against motor controls and 0.37 against visual controls; 0.93 for fine-grained and 0.19 for coarse discrimination. Handwriting beat typing for telling letters from their mirror images in older preschoolers (Longcamp et al. 2005) and in adults (Longcamp et al. 2008). Adults learning Arabic letters by writing, typing or watching all learned to recognise them, but the writers needed fewer sessions and did better on naming, spelling and word reading (Wiley and Rapp 2021). A small 2025 child study with unfamiliar alphabets agrees (Ibaibarriaga et al. 2025).
- **Why.** Part of the benefit comes from seeing variable forms: children shown variable exemplars categorised symbols as well as those who wrote them (Li and James 2016). The app can supply variation without writing.
- **Stroke order and animation.** For learners of Chinese, handwriting and stroke animation each beat passive reading on measures of character form (Xu et al. 2013); stroke-order instruction with handwriting improved recognition and production (Hsiung et al. 2017); writing strengthens form knowledge while sound-based typing strengthens phonology (Guan et al. 2011).
- **Mnemonics.** Pictures that embed the letter shape speed letter-sound learning in preschoolers (Ehri et al. 1984; Shmidman and Ehri 2010). There is no adult evidence for an invented script.
- **Time.** Adults trained for eight to ten days on small artificial scripts learned to read trained words accurately, and generalisation depended heavily on explicit teaching of the code (Taylor et al. 2017; Rastle et al. 2021). *Inference:* because 25 runes map one-to-one to known Latin letters, expect 90% recognition of 34 runes after roughly two to four hours spread over one to two weeks, and fluent word reading only after weeks of reading rune text.

### g. Font engineering

- **Outlines.** Draw original vectors; do not convert or trace an existing font file. In the United States typeface designs as such are not copyrightable, though font software may be (37 CFR 202.1(e)); other jurisdictions differ. Not legal advice.
- **Tooling.** FontForge's latest release is 2025-10-09 (FontForge project 2025). fontTools compiles OpenType feature files and fontmake builds from UFO sources; both appear in current practitioner threads, but their versions were not confirmed here.
- **Encoding option A, Latin letters with ligatures.** Runes sit on A to Z and a rule such as `sub a a by aa_rune;` forms the two-letter runes (Cozens 2026). Text stays searchable and degrades to readable Latin. Canon's split spellings then need a zero-width non-joiner, and the digit keys must be freed for numerals, as the fan Numbered font did.
- **Encoding option B, Private Use Area.** One code point per rune is unambiguous but shows empty boxes without the font. No registration of this script in the Under-ConScript Unicode Registry turned up (Wikipedia contributors 2026; absence not confirmed). Ligature rules over supplementary-plane private-use glyphs reportedly fail in Microsoft Word; the Basic Multilingual Plane area avoids this (TypeDrawers 2026).

## 3. What this means for the app

1. **Skeleton JSON is the single source of truth** (high confidence). One record per glyph: `{id, tier, class, value, slashes:[{orient, length, bend, zone_from, zone_to}], dots:[zone], parents:[], operator, era, precedent, status}`. The font, tracing templates, feature vectors and everyday hand are generated from it.
2. **Annotate canon first, then calibrate** (high). From the 34 annotated glyphs compute stroke and dot histograms, pairwise feature distance, raster similarity, GraphCom complexity, and the rank correlation between complexity and the frequencies in section 2c. Set `Dmax`, the angle set and the similarity threshold from these.
3. **Forge validator** (medium; thresholds need a small human confusion test). Run constraints 1 to 7; report pass or fail, the three nearest glyphs and the complexity percentile. The owner approves; the canon tier is immutable; each release adds few signs, since complexity grows with inventory (Miton and Morin 2021).
4. **Release order** (medium): digits and sentence marks; then divider and emphasis; everyday hand; fused letter runes as an opt-in tier. Offer display tiers "canon only", "classical" and "extended".
5. **Teaching sequence** (medium-high): batches of five or six runes in frequency order (O N R K L, then AH D AA S U), with any pair above the 90th similarity percentile split across batches. Sixteen runes unlock 83% of wall text.
6. **Practice loop** (medium-high): animated stroke order, trace, write from memory on a canvas, then read in words. Check strokes by rule, comparing resampled direction and endpoints to the template as in the $1 recogniser (Wobbrock et al. 2007). Keep a typing fallback and show two or three renderings of each rune. Stroke order (top to bottom, left to right, dots last) is a project convention, not canon.
7. **Mnemonics optional** (low-medium), built on Dovahzul words.
8. **Encoding** (high for the web): store rune token arrays; render with code points from U+E000 plus an `aria-label` transliteration; offer the Latin ligature path for typing; tokenise two-letter runes in app code with an explicit split flag.
9. **Build** (high): a scripted, reproducible pipeline from skeleton JSON to WOFF2, with two families (monumental, everyday) on the same code points.

## 4. Contested or weak evidence

- Universal stroke-count claims (Changizi and Shimojo 2005) are challenged by lineage-aware data (Miton and Morin 2021). Simplification over time holds for Vai, not for Chinese.
- The handwriting advantage is modest against visual controls, most studies involve children, the adult second-script evidence is essentially one study, and the mechanism is disputed.
- Mnemonic evidence is from preschoolers. The time-to-mastery figures are my inference.
- Schmandt-Besserat's token account is disputed in detail; only the tool-and-clay sequence is used here. The cause of the fuþark reduction is debated.
- Four books lack a registry record of their own (see references); the search budget did not allow separate confirmation.

## 5. Gaps and blocked items

- Rune shapes: absent from the repository and not obtainable under the access rules, so sub-question c is partial.
- thuum.org was not contacted; its fonts and number runes are known only from search summaries.
- Not confirmed: current versions of fontTools and fontmake, and the absence of a registry entry for the script.
- Pronunciation is not in the data, so sound-based arguments for TH, SH or NG runes are open. Only United States law on typefaces was checked.
- Treated briefly: ogham, borrowing, orientation preferences, mnemonics, law.

## 6. References

Checker result: `found: 2, manual: 8, not_found: 2, verified: 42`. "Found" and "not found" entries are books; the registry holds only reviews of them, whose DOIs are given as corroboration.

- Appelle, S. (1972). Perception and discrimination as a function of stimulus orientation: The "oblique effect" in man and animals. *Psychological Bulletin*. doi:10.1037/h0033117
- Araújo, S.; Domingues, M.; Fernandes, T. (2022). From hand to eye: A meta-analysis of the benefit from handwriting training in visual graph recognition. *Educational Psychology Review*. doi:10.1007/s10648-021-09651-4
- Barnes, M. P. (2012). *Runes: A Handbook*. Boydell Press. [UNVERIFIED: no registry record of the book; reviews of it are registered, e.g. doi:10.1515/anglia-2013-0012]
- Chang, L.-Y.; Chen, Y.-C.; Perfetti, C. A. (2018). GraphCom: A multidimensional measure of graphic complexity applied to 131 written languages. *Behavior Research Methods*. doi:10.3758/s13428-017-0881-y
- Changizi, M. A.; Shimojo, S. (2005). Character complexity and redundancy in writing systems over human history. *Proceedings of the Royal Society B: Biological Sciences*. doi:10.1098/rspb.2004.2942
- Changizi, M. A.; Zhang, Q.; Ye, H.; Shimojo, S. (2006). The structures of letters and symbols throughout human history are selected to match those found in objects in natural scenes. *The American Naturalist*. doi:10.1086/502806
- Chrisomalis, S. (2010). *Numerical Notation: A Comparative History*. Cambridge University Press. doi:10.1017/CBO9780511676062
- Coulmas, F. (2003). *Writing Systems: An Introduction to Their Linguistic Analysis*. Cambridge University Press. doi:10.1017/CBO9781139164597
- Cozens, S. (2026, accessed). Fonts and Layout for Global Scripts: OpenType features, part 2. https://simoncozens.github.io/fonts-and-layout/features-2.html
- Dehaene, S.; Cohen, L. (2007). Cultural recycling of cortical maps. *Neuron*. doi:10.1016/j.neuron.2007.10.004
- Ehri, L. C.; Deffner, N. D.; Wilce, L. S. (1984). Pictorial mnemonics for phonics. *Journal of Educational Psychology*. doi:10.1037/0022-0663.76.5.880
- FontForge project (2025). FontForge downloads page (release 2025-10-09). https://fontforge.org/en-US/downloads/gnulinux-dl/
- Garrod, S.; Fay, N.; Lee, J.; Oberlander, J.; MacLeod, T. (2007). Foundations of representation: Where might graphical symbol systems come from? *Cognitive Science*. doi:10.1080/03640210701703659
- Gnanadesikan, A. E. (2017). Towards a typology of phonemic scripts. *Writing Systems Research*. doi:10.1080/17586801.2017.1308239
- Guan, C. Q.; Liu, Y.; Chan, D. H. L.; Ye, F.; Perfetti, C. A. (2011). Writing strengthens orthography and alphabetic-coding strengthens phonology in learning to read Chinese. *Journal of Educational Psychology*. doi:10.1037/a0023730
- Han, S. J.; Kelly, P.; Winters, J.; Kemp, C. (2022). Simplification is not dominant in the evolution of Chinese characters. *Open Mind*. doi:10.1162/opmi_a_00064
- Houston, S. D. (ed.) (2012). *The Shape of Script: How and Why Writing Systems Change*. School for Advanced Research Press. [UNVERIFIED: no registry record of the book; a review is registered at doi:10.1017/s0047404514000864]
- Hsiung, H.-Y.; Chang, Y.-L.; Chen, H.-C.; Sung, Y.-T. (2017). Effect of stroke-order learning and handwriting exercises on recognizing and writing Chinese characters by Chinese as a foreign language learners. *Computers in Human Behavior*. doi:10.1016/j.chb.2017.04.022
- Ibaibarriaga, G.; Acha, J.; Perea, M. (2025). The impact of handwriting and typing practice in children's letter and word learning: Implications for literacy development. *Journal of Experimental Child Psychology*. doi:10.1016/j.jecp.2025.106195
- Jee, H.; Tamariz, M.; Shillcock, R. (2022). Systematicity in language and the fast and slow creation of writing systems: Understanding two types of non-arbitrary relations between orthographic characters and their canonical pronunciation. *Cognition*. doi:10.1016/j.cognition.2022.105197
- Kelly, P.; Winters, J.; Miton, H.; Morin, O. (2021). The predictable evolution of letter shapes: An emergent script of West Africa recapitulates historical change in writing systems. *Current Anthropology*. doi:10.1086/717779
- Kim, Y.; Allassonnière-Tang, M.; Miton, H.; Morin, O. (2025). The phonology of letter shapes: Feature economy and informativeness in 43 writing systems. *Journal of Memory and Language*. doi:10.1016/j.jml.2025.104620
- Koshevoy, A.; Miton, H.; Morin, O. (2023). Zipf's law of abbreviation holds for individual characters across a broad range of writing systems. *Cognition*. doi:10.1016/j.cognition.2023.105527
- Li, J. X.; James, K. H. (2016). Handwriting generates variable visual output to facilitate symbol learning. *Journal of Experimental Psychology: General*. doi:10.1037/xge0000134
- Longcamp, M.; Zerbato-Poudou, M.-T.; Velay, J.-L. (2005). The influence of writing practice on letter recognition in preschool children: A comparison between handwriting and typing. *Acta Psychologica*. doi:10.1016/j.actpsy.2004.10.019
- Longcamp, M.; Boucard, C.; Gilhodes, J.-C.; Anton, J.-L.; Roth, M.; Nazarian, B.; Velay, J.-L. (2008). Learning through hand- or typewriting influences visual recognition of new graphic shapes: Behavioral and functional imaging evidence. *Journal of Cognitive Neuroscience*. doi:10.1162/jocn.2008.20504
- McManus, D. (1991). *A Guide to Ogam*. An Sagart (Maynooth Monographs 4). [Book; checker status "found" points to a review of it, doi:10.2307/25571631, not to the book]
- Meletis, D.; Dürscheid, C. (2022). *Writing Systems and Their Use: An Overview of Grapholinguistics*. De Gruyter Mouton. doi:10.1515/9783110757835
- Miller, M. (2011). Skyrim's Dragon Shouts. Game Informer feature, as archived on UESP page General:Skyrim's Dragon Shouts, revision 3187192; read from the repository snapshot (no URL).
- Miton, H.; Morin, O. (2021). Graphic complexity in writing systems. *Cognition*. doi:10.1016/j.cognition.2021.104771
- Morin, O. (2018). Spontaneous emergence of legibility in writing systems: The case of orientation anisotropy. *Cognitive Science*. doi:10.1111/cogs.12550
- Mueller, S. T.; Weidemann, C. T. (2012). Alphabetic letter identification: Effects of perceivability, similarity, and bias. *Acta Psychologica*. doi:10.1016/j.actpsy.2011.09.014
- Parkes, M. B. (2016; first published 1992, Scolar Press). *Pause and Effect: An Introduction to the History of Punctuation in the West*. Routledge. doi:10.4324/9781315247243
- Pelli, D. G.; Burns, C. W.; Farell, B.; Moore-Page, D. C. (2006). Feature detection and letter identification. *Vision Research*. doi:10.1016/j.visres.2006.04.023
- Primus, B. (2004). A featural analysis of the Modern Roman Alphabet. *Written Language & Literacy*. doi:10.1075/wll.7.2.06pri
- Rastle, K.; Lally, C.; Davis, M. H.; Taylor, J. S. H. (2021). The dramatic impact of explicit instruction on learning to read in a new writing system. *Psychological Science*. doi:10.1177/0956797620968790
- Saenger, P. (1997). *Space Between Words: The Origins of Silent Reading*. Stanford University Press. doi:10.1515/9781503619081
- Schmandt-Besserat, D. (1992). *Before Writing, Volume I: From Counting to Cuneiform*. University of Texas Press. [Book; checker status "found" points to a review of it, doi:10.2307/530080, not to the book]
- Schulte, M. (2015). Runology and historical sociolinguistics: On runic writing and its social history in the first millennium. *Journal of Historical Sociolinguistics*. doi:10.1515/jhsl-2015-0004
- Shmidman, A.; Ehri, L. (2010). Embedded picture mnemonics to learn letters. *Scientific Studies of Reading*. doi:10.1080/10888430903117492
- Tamariz, M.; Kirby, S. (2015). Culture: Copying, compression, and conventionality. *Cognitive Science*. doi:10.1111/cogs.12144
- Taylor, J. (2011). Tablets as Artefacts, Scribes as Artisans. In *The Oxford Handbook of Cuneiform Culture*. Oxford University Press. doi:10.1093/oxfordhb/9780199557301.013.0001
- Taylor, J. S. H.; Davis, M. H.; Rastle, K. (2017). Comparing and validating methods of reading instruction using behavioural and neural findings in an artificial orthography. *Journal of Experimental Psychology: General*. doi:10.1037/xge0000301
- Thuum.org (2026, accessed via search summaries only). Downloads: fan fonts, including a Numbered Dragon Alphabet font and a printable alphabet sheet. https://www.thuum.org/downloads.php (fan)
- Treiman, R.; Kessler, B. (2011). Similarities among the shapes of writing and their effects on learning. *Written Language & Literacy*. doi:10.1075/wll.14.1.03tre
- Turoman, N.; Styles, S. J. (2017). Glyph guessing for 'oo' and 'ee': spatial frequency information in sound symbolic matching for ancient and unfamiliar scripts. *Royal Society Open Science*. doi:10.1098/rsos.170882
- TypeDrawers forum contributors (2026, accessed). DirectWrite and the Unicode PUA: can they work together? https://typedrawers.com/discussion/comment/65533
- UESP contributors (2026). Lore:Dragon Alphabet, revision 3495681 (snapshot in `research/sources/uesp/`). https://en.uesp.net/wiki/Lore:Dragon_Alphabet
- United States Copyright Office (1992). 37 CFR 202.1, Material not subject to copyright, paragraph (e). https://www.ecfr.gov/current/title-37/chapter-II/subchapter-A/part-202/section-202.1
- Wikipedia contributors (2026, accessed). ConScript Unicode Registry (and its successor, the Under-ConScript Unicode Registry). https://en.wikipedia.org/wiki/ConScript_Unicode_Registry
- Wiley, R. W.; Rapp, B. (2021). The effects of handwriting experience on literacy learning. *Psychological Science*. doi:10.1177/0956797621993111
- Wiley, R. W.; Wilson, C.; Rapp, B. (2016). The effects of alphabet and expertise on letter perception. *Journal of Experimental Psychology: Human Perception and Performance*. doi:10.1037/xhp0000213
- Wobbrock, J. O.; Wilson, A. D.; Li, Y. (2007). Gestures without libraries, toolkits or training: a $1 recognizer for user interface prototypes. *Proceedings of UIST 2007*. doi:10.1145/1294211.1294238
- Xu, Y.; Chang, L.-Y.; Zhang, J.; Perfetti, C. A. (2013). Reading, writing, and animation in character learning in Chinese as a foreign language. *Foreign Language Annals*. doi:10.1111/flan.12040
