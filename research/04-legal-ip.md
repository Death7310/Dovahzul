# Track 4: The intellectual-property landscape

Research date: 2026-11-14. **This is research, not legal advice.** It was written without a lawyer and without full-text access to most primary documents (see section 5). Before public release the owner should have a qualified lawyer review the name, the licence files and the canon-text policy.

Labels used for language facts: **canon** (game text, official publications), **semi-canon** (official but not game text, such as the Prima guide word list), **fan** (wiki editors' glosses, fan-site coinages, the name "Dovahzul" itself).

## 1. Bottom line

- **The language as a system is very probably free to teach and extend; the game's texts are not free to copy.** US copyright excludes systems and methods (17 U.S.C. § 102(b); Baker v. Selden 1880) and single words (37 C.F.R. § 202.1(a)). No court has ever ruled on a constructed language, so this is a strong argument, not a settled rule.
- **The real copyright exposure is quotation**: the 131 word walls, 269 dialogue records and 6 songs in the corpus are ordinary protected writing. Ship them as a detachable pack, always with analysis, never as bulk text.
- **Draw the font from scratch.** Typeface designs are not copyrightable in the US, font software is. Never extract the game font or bundle a fan font without a licence.
- **Keep every ZeniMax trademark out of the app's own name.** Refer to the game only in a plain-text descriptive line with an "unofficial" disclaimer (nominative fair use).
- **No published Bethesda, ZeniMax or Microsoft policy covers a fan language app.** The project would run on tolerated use. Tolerance is real for free fan work but is not a licence and can be withdrawn.
- **UESP data is CC BY-SA 2.5**: attribute each article, link its history, keep derived data under share-alike. The largest fan dictionary states no licence in anything found: do not import it without written permission.
- **Licence stack**: copyleft code, CC BY-SA 4.0 for project-original content, SIL OFL with a reserved font name. Owner authority comes from the project name and signed rule-set releases, not from restricting copying.
- **Build for takedown from day one**: per-record provenance, a build that works with canon quotations removed, a contact address and a fixed response routine.

## 2. Findings by sub-question

### a. Can a constructed language be protected?

**Doctrine.** Copyright protects expression and not any "idea, procedure, process, system, method of operation" (17 U.S.C. § 102(b)). Baker v. Selden (1880) is the root case: a book explaining a bookkeeping system is protected, the system is not. Samuelson (2015) argues, reviewing the case law, that this exclusion is a substantive limit on scope. Words and short phrases are not registrable (37 C.F.R. § 202.1(a)), and facts and unoriginal compilations get no protection, with only thin protection for an original selection or arrangement (Feist 1991). A language therefore splits into layers with different status:

| Layer | Status (US) | Confidence |
|---|---|---|
| Phonology, grammar, word-formation rules | Unprotected system | High |
| Single words and their short meanings | Unprotected individually | High |
| The whole invented lexicon as a set | Unsettled; at most thin | Low to medium |
| Texts written in the language by the studio | Protected literary works | High |
| New sentences composed by users | The user's own work | High |

**Paramount v. Axanar.** Paramount and CBS listed the Klingon language among the copyrighted elements a fan film had taken. The Language Creation Society filed an amicus brief arguing that a language is an unprotectable system (LCS 2016). In May 2016 Judge Klausner denied the motion to dismiss without deciding the language question (Techdirt 2016). In January 2017 the court rejected the fair-use defence on summary judgment and the case then settled (Paramount v. Axanar 2017). The Klingon question was never decided. The same case shows the real danger: the fair-use defence failed over characters, settings and plot, not over the language.

**Loglan Institute v. Logical Language Group (Fed. Cir. 1992)** was a trademark case. The court upheld cancellation of the registration of "Loglan" because the word had become the generic name of the language. The Institute's separate copyright claim over the vocabulary was never tested; the breakaway group rebuilt the vocabulary as Lojban to avoid it (Adelman 2014 [UNVERIFIED]; Guadamuz 2016). The lesson is double: the name of a language cannot be monopolised once it is generic, and a threatened community may choose to rebuild instead of litigate.

**Scholarship.** Adelman (2014 [UNVERIFIED in the DOI registry; publisher PDF seen in search results]) reviews Loglan, Tolkien and Klingon and proposes that constructed languages get minimal or no copyright, with most uses fair in any case. Allen-Franks (2024, published 2018) examines whether individual invented words can be protected; only its abstract was read. Guadamuz (2016) argues by analogy from SAS Institute v World Programming (CJEU 2012), which held that a programming language is not a form of expression protected under the Software Directive, while leaving open protection as a work under general copyright. In the UK, Exxon (1982) held that a single invented word is not a literary work. I found no peer-reviewed article after 2018 on this question.

**Rights holders' positions.** Paramount asserted ownership of Klingon in litigation. The Tolkien Estate is reported on fan forums to hold that the Elvish languages are under copyright (Parf Edhellen forum, n.d.), while the Elvish Linguistic Fellowship, which studies Tolkien's linguistic papers, treats new fan compositions as a kind of fan fiction (ELF FAQ, n.d.). This evidence is second-hand. The dragon language was written in-house by Bethesda Game Studios staff (Wilhelm 2021), so whatever is protectable belongs to the employer as a work made for hire (inference).

**Other jurisdictions.** The EU has no open-ended fair use; quotation and teaching exceptions are narrower. The idea and expression divide exists everywhere, and SAS and Exxon point the same way as US law for the system and for single words. Treated briefly.

### b. Typefaces and glyphs

"Typeface as typeface" is not subject to US copyright (37 C.F.R. § 202.1(e)), and Eltra v. Ringer (1978) upheld the refusal to register a typeface design. Since 1992 the Copyright Office has accepted that the computer program that generates a font can be protected (Monotype n.d.; Fordham IPLJ 2021). Adobe v. Southern Software (1998) is the usual authority that font software is protected; secondary sources disagree about its procedural history, so it is cited with caution. Fry (2009) documents that type design thrives in the US without copyright in the designs.

Inference: the 34 runes plus two font-only glyphs are a notational system, so their shapes fall under the typeface rule in the US. The game's font file, fan-made font files (Thuum.org Downloads) and word-wall textures are protected as software or artwork. An original font drawn from the abstract letter shapes is the project's own software, and invented glyphs are wholly the project's. Outside the US, typeface designs can be protected as designs or artistic works; this was not verified in this session.

### c. The rights holder's policies in 2026

- **Bethesda Video Policy** (2017): supports fan videos made with game assets, including let's-plays, mod-tool tutorials and tributes. It covers video only.
- **Bethesda Softworks Community Standards**: rules for mods and Creations hosted on Bethesda.net (credit, permissions, no third-party IP).
- **ZeniMax Terms of Service**: the binding document for accounts, mods and user content. Not read in full.
- **Microsoft Game Content Usage Rules** (copy found dated January 2015): a personal, non-commercial licence for fan items, which bars game content in an app sold in a store and requires permission for commercial ventures. By its own text it applies to games "published and owned by Microsoft Studios". Nothing found extends it to Bethesda titles.

No policy addressing fan apps, lore projects or the dragon language was found. Practice is mixed but coherent. Bethesda has long supported modding of Skyrim, tried and withdrew paid Skyrim mods in 2015 after community backlash (Joseph 2018), and in 2025 let the Skyblivion remake continue beside its own Oblivion remaster (PC Gamer 2025). It acts when a project looks like a product or an official release: the "Scrolls" trademark suit against Mojang (Game Developer 2012) and, per October 2026 press reports, a cease-and-desist against an AI-generated "Fallout: New York" (GamesRadar+ 2026). Research on modding finds the same pattern across publishers: tolerance while fan work adds value to the game, enforcement when it brings in third-party IP, money or confusion, with ownership of fan-made work left to the publisher's terms (Postigo 2008; Kow & Nardi 2010; Kretzschmar & Stanfill 2019). Wu (2008) calls this "tolerated use": infringing or arguably infringing use that the owner knows of and allows. Thuum.org has long published a community-expanded dictionary (over 4,000 words by its third edition, per search snippets), lessons and fonts (Thuum.org dictionary, n.d.; Thuum.org Downloads); I found no report of action against it (inference from absence of evidence; low to medium confidence).

### d. Trademark

UESP's own notice lists The Elder Scrolls, Skyrim, Bethesda Softworks and ZeniMax as ZeniMax trademarks (UESP 2026). Nominative fair use allows naming another's product when (1) the product is not readily identifiable without the mark, (2) no more of the mark is used than necessary and (3) nothing suggests sponsorship or endorsement (New Kids on the Block 1992; Toyota v. Tabari 2010; Ninth Circuit Model Instruction 15.26). Circuits differ on how the test fits with likelihood of confusion. The defence covers referring to the game. It does not cover adopting the mark as the app's own brand: Jack Daniel's v. VIP Products (2023) confirms that using another's mark as a source identifier for your own product gets ordinary confusion analysis. "Dovahzul" is a **fan** term (it occurs once in the 331-page wiki snapshot, in a fan's question). As the common name of the language it is probably nobody's to own (Loglan 1992, by analogy), but no trademark register search was possible here.

### e. Data sources

**UESP.** The policy page (revision 3529700, read through the API) licenses content under CC BY-SA 2.5 and sets three reuse conditions: license derived material under the same by-sa licence, credit the source article, and give access to it, which a link to the article and its history page satisfies (UESP 2026). Copyright in each edit stays with the editor. The licence text allows adaptations under a later version with the same elements (CC BY-SA 2.5 legal code, clause 4(b), from memory of the text). The licence covers what editors wrote: glosses, translations, commentary (**fan**). It cannot license the game text the wiki quotes (**canon**). Of the 657 lexicon entries, 166 rest only on the Prima guide or a Bethesda article and 91 only on a dictionary hosted at The Imperial Library (**semi-canon**); the provenance field should keep these distinguishable, because a third-party publication is involved.

**Fan dictionary with no stated licence.** Search snippets show the Thuum.org dictionary describing itself as unofficial, non-commercial and educational, with canon and community-invented words marked separately (Thuum.org dictionary, n.d.). No licence was found. Silence means all rights reserved for whatever is protectable: definition prose, selection and arrangement, lessons, fonts. Individual coined words are probably unprotectable, but bulk import would copy the compilation and damage relations with the only existing community.

**Facts and databases.** In the US, facts and unoriginal compilations are free (Feist 1991; Carroll 2015). The EU adds a 15-year sui generis right for databases made with substantial investment by EU makers (Directive 96/9/EC; Derclaye 2008). Treated briefly; relevant only if a source's maker is in the EU or UK.

### f. Licence choices

Non-commercial clauses are ambiguous and block reuse by share-alike projects (Hagedorn et al. 2011), so "free for everyone" is better served by share-alike without NC. Users rarely understand the copyright terms they accept (Fiesler et al. 2016), so contributor terms need a plain-language summary. Lojban's frozen baseline shows a community keeping an authoritative language definition while the material stays free (Logical Language Group 1997). Statements here about the OFL, GPL family and CC 4.0 come from my knowledge of the licence texts, not from a source read this session.

### g. Risk assessment

| Risk | Likelihood | Mitigation |
|---|---|---|
| Objection to bulk canon text | Low to medium | Detachable pack; quote with analysis |
| Trademark complaint about name or look | Low if name is clean | Distinctive name; plain-text reference; disclaimer |
| Game assets or audio | High if used | Use none |
| Fan-site complaint | Medium if data imported | Do not import; ask permission |
| Share-alike breach | Medium if careless | Automated attribution screen |
| Tolerance withdrawn | Low; unpredictable | Takedown routine; modular data |

## 3. What this means for the app

1. **Tier the data and record provenance per record** (confidence: high as engineering, medium as legal necessity). Every lexicon, corpus and lesson record carries `origin` (`game`, `official_publication`, `uesp_editor`, `fan_site`, `project`), `canon_label`, `licence`, `source_page`, `source_revision`. Tier A: canon word forms with project-written short glosses. Tier B: canon quotations. Tier C: UESP-derived editor text. Tier D: project-original lessons and forged words. Evidence: the layer table above; UESP 2026.
2. **Make Tier B a removable pack** (medium). The build and every lesson must pass tests with the canon-texts pack absent, falling back to project-written example sentences. Evidence: Axanar and Warner Bros. v. RDR Books (2008), where a fan reference work was a legitimate purpose but lost on fair use because of how much it copied verbatim.
3. **Quotation rule** (medium). A canon quotation may appear only inside a unit that adds a parse, gloss or exercise. No screen lists canon texts back to back without analysis; song lyrics are shown line by line with interlinear analysis. Fair use weighs purpose and amount (17 U.S.C. § 107).
4. **Prefer project-written glosses to copied wiki prose** (medium). Where editor text is kept, generate an in-app "Sources and licences" screen from `ATTRIBUTION.md` with article and history links, readable offline. Keep UESP-derived files as separate data files marked CC BY-SA, not compiled into source code.
5. **Do not ingest fan-site dictionaries, lessons or fonts** (medium to high). Ask the maintainers for a written licence. Until then the forge may record only that a form is `attested_elsewhere`, entered by hand with a citation.
6. **Original font** (high for US). Draw all 34 runes and any new glyphs from scratch, keep the source outlines and commit history as evidence of independent creation, never open the game's font in the font editor. Release under SIL OFL 1.1 with a Reserved Font Name.
7. **Name and presentation** (high). The name contains no "Skyrim", "Elder Scrolls", "Bethesda" or character names. One descriptive line: "An unofficial guide to the dragon language of The Elder Scrolls V: Skyrim". No logos, no game typeface for titles, no dragon emblem. Run USPTO and EUIPO searches on the chosen name and on "Dovahzul" before launch.
8. **No game assets** (high): no audio, music, textures, screenshots, icons or strings extracted from game files. Pronunciation audio is recorded by the project or produced by rule.
9. **Stay non-commercial in conduct** (medium): no ads, no paid tier, no sale in app stores; distribute as a free web app from the project's own repository. Evidence: Wu 2008; Kretzschmar & Stanfill 2019; the Microsoft rules as a benchmark.
10. **Licence stack** (medium; owner's decision): code under AGPL-3.0-or-later or GPL-3.0-or-later; lessons, rule-set text and forged vocabulary under CC BY-SA 4.0; font under OFL. A `NOTICE` file states that the licences cover only the project's original contributions and that no rights are claimed in the game's material or in the language as such.
11. **Authority by name and signature** (medium; design inference). Each rule-set release is a versioned file with a hash and an Ed25519 signature; the app verifies it offline against the owner's public key and shows "official" only for words validated under a signed version. Forks are free but must rename and may not call their rules official (trademark policy plus the OFL reserved name). A `GOVERNANCE.md` names the owner as final authority.
12. **Contributor terms in the forge** (medium). A submission stores `coined_by`, `derivation` (the rule path from canon roots), `date` and a sign-off that it is the submitter's own coinage, licensed under the project's content licence. The validator rejects forms on a blocklist of third-party marks and names. The derivation log is also evidence of independent creation.
13. **Takedown routine** (high). A public contact address, a commitment to respond within 48 hours, a one-command build without Tier B and C, and a private log of notices.
14. **Disclaimer** on first run, the About screen and the README: "Unofficial fan project. Not affiliated with, endorsed or sponsored by Bethesda Softworks, ZeniMax Media or Microsoft. The Elder Scrolls and Skyrim are trademarks of ZeniMax Media Inc. Dragon-language text from the games belongs to its owners and is quoted for teaching and commentary."

Sequencing: items 1, 7, 8, 10 and 14 before the first public commit; 4, 6 and 13 before the first release; 11 and 12 before the forge accepts outside submissions.

## 4. Contested or weak evidence

- **No precedent on constructed languages.** Axanar was not decided on this point and Loglan was a trademark case. Scholarly opinion favours no or minimal protection, but it is a small literature, and rights holders assert the opposite.
- **The lexicon as a whole is the weak point of the "languages are free" argument.** Every word-meaning pair in an invented language is someone's invention, unlike facts about a natural language. RDR Books treated invented fictional facts as protected expression. A court could see a full dictionary as closer to that than to a phone book.
- **Is a constructed script a "typeface"?** Untested. A rights holder could argue the runes are artwork.
- **Fair use is fact-specific** and does not exist in that form in the EU or UK.
- **Tolkien Estate position**: fan-forum reports only.
- **Microsoft's rules and Bethesda titles**: applicability unconfirmed; the copy found is dated 2015.
- **2026 enforcement**: press reports of one incident, not a policy statement.
- **Allen-Franks** was read in abstract only. **Monotype** is an industry source with a commercial interest in strong font protection.
- **Mod studies** (Postigo, Kow & Nardi, Joseph) are qualitative case studies, not measurements of enforcement rates.

## 5. Gaps, and anything that was blocked

- Page fetching was unavailable, so the Bethesda Video Policy, Community Standards, ZeniMax Terms of Service, Microsoft rules, court orders and law-review full texts were **not read in full**. Statements about them rest on search summaries and prior knowledge.
- Thuum.org refuses automated requests; only search snippets were used. Its footer or terms may state conditions not seen here.
- No trademark register search (USPTO, EUIPO, UKIPO) was possible.
- Nine legal citations have no URL confirmed in this session and are given by official citation only: 17 U.S.C. §§ 102(b) and 107, Baker v. Selden, Feist, Warner Bros. v. RDR Books, Adobe v. Southern Software, Jack Daniel's v. VIP Products, Exxon, Directive 96/9/EC.
- Five law-review articles I wished to cite were not in the DOI registry and were dropped. Adelman (2014) is kept and tagged [UNVERIFIED].
- The licence texts (OFL 1.1, GPL and AGPL 3.0, CC BY-SA 4.0) and non-US typeface law were not re-read.
- Treated briefly: other jurisdictions, database rights, the Tolkien Estate, studio ownership of commissioned languages other than Klingon.

## 6. References

Checked with `tools/research/check_refs.py`; the status of each entry is shown in brackets. "manual" means a legal or web source that a registry cannot check; where such an entry has no address, none was confirmed in this session. The list matches `research/refs/legal-ip.json` entry for entry.

- **Adelman 2014** (`adelman2014`). Adelman, M. (2014). Constructed Languages and Copyright: A Brief History and Proposal for Divorce. Harvard Journal of Law & Technology, 27(2), 543-562. <https://jolt.law.harvard.edu/articles/pdf/v27/27HarvJLTech543.pdf>. [UNVERIFIED: not in the DOI registry; publisher PDF address seen in search results]
- **Allen-Franks 2024** (`allenfranks2024`). Allen-Franks, A. (2024). Copyright Protection for Individual Words of an Invented Language. SSRN (author posting of the article published in European Intellectual Property Review, 40(5), 311-318, 2018). doi:10.2139/ssrn.4936745. <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4936745>. [registry: verified]
- **Samuelson 2015** (`samuelson2015`). Samuelson, P. (2015). Functionality and Expression in Computer Programs: Refining the Tests for Software Copyright Infringement. SSRN (published 2016 in Berkeley Technology Law Journal, 31(2), 1215-1300). doi:10.2139/ssrn.2667740. [registry: verified]
- **Wu 2008** (`wu2008`). Wu, T. (2008). Tolerated Use. Columbia Journal of Law & the Arts, 31(4), 617-635 (DOI is the SSRN registration). doi:10.2139/ssrn.1132247. [registry: verified]
- **Fry 2009** (`fry2009`). Fry, B. (2009). Why Typefaces Proliferate Without Copyright Protection. SSRN (published 2010 in Journal on Telecommunications and High Technology Law, 8(2), 425-490). doi:10.2139/ssrn.1443491. [registry: verified]
- **Kretzschmar & Stanfill 2019** (`kretzschmar2019`). Kretzschmar, M.; Stanfill, M. (2019). Mods as Lightning Rods: A Typology of Video Game Mods, Intellectual Property, and Social Benefit/Harm. Social & Legal Studies, 28(4), 517-536. doi:10.1177/0964663918787221. [registry: verified]
- **Postigo 2008** (`postigo2008`). Postigo, H. (2008). Video Game Appropriation through Modifications: Attitudes Concerning Intellectual Property among Modders and Fans. Convergence, 14(1), 59-74. doi:10.1177/1354856507084419. [registry: verified]
- **Joseph 2018** (`joseph2018`). Joseph, D. (2018). The Discourse of Digital Dispossession: Paid Modifications and Community Crisis on Steam. Games and Culture, 13(7), 690-707. doi:10.1177/1555412018756488. [registry: verified]
- **Kow & Nardi 2010** (`kow2010`). Kow, Y. M.; Nardi, B. (2010). Who owns the mods?. First Monday, 15(5). doi:10.5210/fm.v15i5.2971. [registry: verified]
- **Carroll 2015** (`carroll2015`). Carroll, M. W. (2015). Sharing Research Data and Intellectual Property Law: A Primer. PLOS Biology, 13(8), e1002235. doi:10.1371/journal.pbio.1002235. [registry: verified]
- **Hagedorn et al. 2011** (`hagedorn2011`). Hagedorn, G.; Mietchen, D.; Morris, R. A.; Agosti, D.; Penev, L.; Berendsohn, W. G.; Hobern, D. (2011). Creative Commons licenses and the non-commercial condition: Implications for the re-use of biodiversity information. ZooKeys, 150, 127-149. doi:10.3897/zookeys.150.2189. [registry: verified]
- **Fiesler et al. 2016** (`fiesler2016`). Fiesler, C.; Lampe, C.; Bruckman, A. S. (2016). Reality and Perception of Copyright Terms of Service for Online Content Creation. Proceedings of the 19th ACM Conference on Computer-Supported Cooperative Work & Social Computing (CSCW '16). doi:10.1145/2818048.2819931. [registry: verified]
- **Derclaye 2008** (`derclaye2008`). Derclaye, E. (2008). The Legal Protection of Databases: A Comparative Analysis. Edward Elgar Publishing. doi:10.4337/9781847209986. [registry: verified]
- **Paramount v. Axanar 2017** (`axanar_case`). United States District Court for the Central District of California (2017). Paramount Pictures Corp. v. Axanar Productions, Inc., No. 2:15-cv-09938-RGK-E (C.D. Cal.): orders of 9 May 2016 (motion to dismiss) and 3 January 2017 (summary judgment). U.S. District Court docket; summary-judgment order as reported by The Hollywood Reporter. <https://www.hollywoodreporter.com/thr-esq/judge-makes-big-ruling-sending-star-trek-fan-film-dispute-jury-trial-960703>. [manual]
- **LCS 2016** (`lcs_axanar`). Language Creation Society (2016). Axanar [the Society's amicus brief in Paramount v. Axanar, with updates]. conlang.org. <https://conlang.org/axanar/>. [manual]
- **Techdirt 2016** (`techdirt2016`). Techdirt (2016). Judge Says Copyright Case Against Star Trek Fan Film Can 'Live Long' And Possibly 'Prosper'. techdirt.com. <https://www.techdirt.com/articles/20160510/11113034401/judge-says-copyright-case-against-star-trek-fan-film-can-live-long-possibly-prosper.shtml>. [manual]
- **Guadamuz 2016** (`guadamuz2016`). Guadamuz, A. (2016). Can you copyright the Klingon language?. TechnoLlama (academic blog). <https://www.technollama.co.uk/can-you-copyright-the-klingon-language>. [manual]
- **Loglan 1992** (`loglan1992`). United States Court of Appeals for the Federal Circuit (1992). Loglan Institute, Inc. v. Logical Language Group, Inc., 962 F.2d 1038 (Fed. Cir. 1992). Federal Reporter, Second Series. <https://technollama.co.uk/can-you-copyright-the-klingon-language>. [manual]
- **17 U.S.C. § 102(b)** (`usc102b`). United States Congress (1976). 17 U.S.C. § 102(b) (ideas, procedures, processes, systems and methods of operation excluded from copyright). United States Code, Title 17. [manual; official citation only, no address confirmed this session]
- **17 U.S.C. § 107** (`usc107`). United States Congress (1976). 17 U.S.C. § 107 (fair use). United States Code, Title 17. [manual; official citation only, no address confirmed this session]
- **Baker v. Selden 1880** (`baker1880`). Supreme Court of the United States (1880). Baker v. Selden, 101 U.S. 99 (1880). United States Reports. [manual; official citation only, no address confirmed this session]
- **Feist 1991** (`feist1991`). Supreme Court of the United States (1991). Feist Publications, Inc. v. Rural Telephone Service Co., 499 U.S. 340 (1991). United States Reports. [manual; official citation only, no address confirmed this session]
- **Warner Bros. v. RDR Books 2008** (`rdr2008`). United States District Court for the Southern District of New York (2008). Warner Bros. Entertainment Inc. v. RDR Books, 575 F. Supp. 2d 513 (S.D.N.Y. 2008). Federal Supplement, Second Series. [manual; official citation only, no address confirmed this session]
- **37 C.F.R. § 202.1** (`cfr202`). United States Copyright Office (1992). 37 C.F.R. § 202.1 Material not subject to copyright: (a) words and short phrases; (e) typeface as typeface. Code of Federal Regulations. <https://www.ecfr.gov/current/title-37/chapter-II/subchapter-A/part-202/section-202.1>. [manual]
- **Eltra v. Ringer 1978** (`eltra1978`). United States Court of Appeals for the Fourth Circuit (1978). Eltra Corp. v. Ringer, 579 F.2d 294 (4th Cir. 1978). Federal Reporter, Second Series (URL is an encyclopedia mirror that summarises the case). <https://wiki.riteme.site/wiki/Eltra_Corp._v._Ringer>. [manual]
- **Adobe v. Southern Software 1998** (`adobe1998`). United States District Court for the Northern District of California (1998). Adobe Systems Inc. v. Southern Software Inc., No. C 95-20710 RMW, 1998 WL 104303 (N.D. Cal. 1998). Unreported district court decision. [manual; official citation only, no address confirmed this session]
- **Monotype n.d.** (`monotype_update`). Monotype (n.d.). Update on the application of copyright law to typeface design and font software. monotype.com (industry source). <https://www.monotype.com/resources/update-application-copyright-law-typeface-design-and-font-software>. [manual]
- **Fordham IPLJ 2021** (`fordham2021`). Fordham Intellectual Property, Media & Entertainment Law Journal (2021). Open Type Questions: Issues in Copyright Law and Protecting Typeface Design. fordhamiplj.org (law journal blog). <https://fordhamiplj.org/2021/12/11/open-type-questions-issues-in-copyright-law-and-protecting-typeface-design/>. [manual]
- **Toyota v. Tabari 2010** (`tabari2010`). United States Court of Appeals for the Ninth Circuit (2010). Toyota Motor Sales, U.S.A., Inc. v. Tabari, 610 F.3d 1171 (9th Cir. 2010). Federal Reporter, Third Series. <https://cases.justia.com/federal/appellate-courts/ca9/07-55344/920100708/0.pdf>. [manual]
- **Ninth Circuit Model Instruction 15.26** (`ninth1526`). Ninth Circuit Jury Instructions Committee (n.d.). Manual of Model Civil Jury Instructions, 15.26 Defenses: Nominative Fair Use. United States Courts for the Ninth Circuit. <https://www.ce9.uscourts.gov/jury-instructions/civil/chapter-15/15-26-defenses-nominative-fair-use/>. [manual]
- **New Kids on the Block 1992** (`newkids1992`). United States Court of Appeals for the Ninth Circuit (1992). New Kids on the Block v. News America Publishing, Inc., 971 F.2d 302 (9th Cir. 1992). Federal Reporter, Second Series (URL is a law-firm overview that discusses the case). <https://www.fr.com/third-party-trademarks-fair-use-or-foul/>. [manual]
- **Jack Daniel's v. VIP Products 2023** (`jackdaniels2023`). Supreme Court of the United States (2023). Jack Daniel's Properties, Inc. v. VIP Products LLC, 599 U.S. 140 (2023). United States Reports. [manual; official citation only, no address confirmed this session]
- **SAS Institute v World Programming, CJEU 2012** (`sas2012`). Court of Justice of the European Union (2012). SAS Institute Inc. v World Programming Ltd, Case C-406/10 (Grand Chamber, 2 May 2012); Press Release No 53/12. curia.europa.eu. <https://curia.europa.eu/site/upload/docs/application/pdf/2012-05/cp120053en.pdf>. [manual]
- **Exxon 1982** (`exxon1982`). Court of Appeal of England and Wales (1982). Exxon Corp. v Exxon Insurance Consultants International Ltd [1982] Ch 119. Law Reports, Chancery Division. [manual; official citation only, no address confirmed this session]
- **Directive 96/9/EC** (`dbdirective1996`). European Parliament; Council of the European Union (1996). Directive 96/9/EC of 11 March 1996 on the legal protection of databases. Official Journal of the European Communities, L 77. [manual; official citation only, no address confirmed this session]
- **UESP 2026** (`uesp_copyright`). Unofficial Elder Scrolls Pages (UESP) (2026). UESPWiki:Copyright and Ownership (revision 3529700 of 26 March 2026, read through the MediaWiki API). en.uesp.net. <https://en.uesp.net/wiki/UESPWiki:Copyright_and_Ownership>. [manual]
- **CC BY-SA 2.5 legal code** (`ccbysa25`). Creative Commons (2005). Attribution-ShareAlike 2.5 Generic: Legal Code. creativecommons.org (address as linked from the UESP policy page). <http://creativecommons.org/licenses/by-sa/2.5/legalcode>. [manual]
- **Bethesda Video Policy** (`bethesda_video`). Bethesda Softworks (2017). Bethesda Video Policy. bethesda.net. <https://bethesda.net/en-US/news/bethesda-video-policy>. [manual]
- **Bethesda Softworks Community Standards** (`bethesda_standards`). Bethesda Softworks (n.d.). Bethesda Softworks Community Standards. bethesda.net. <https://bethesda.net/en-US/news/bethesda-softworks-community-standards>. [manual]
- **ZeniMax Terms of Service** (`zenimax_tos`). ZeniMax Media Inc. (n.d.). Terms of Service. bethesda.net. <https://bethesda.net/data/tos/en.html>. [manual]
- **Microsoft Game Content Usage Rules** (`xbox_rules`). Microsoft (2015). Game Content Usage Rules. xbox.com. <https://www.xbox.com/en-US/developers/rules>. [manual]
- **PC Gamer 2025** (`pcgamer2025`). PC Gamer (2025). Credit where it's due: Bethesda is being admirably normal by letting modders carry on with their competing Oblivion remaster. pcgamer.com. <https://www.pcgamer.com/games/rpg/credit-where-its-due-bethesda-is-being-admirably-normal-by-letting-modders-carry-on-with-their-competing-oblivion-remaster>. [manual]
- **GamesRadar+ 2026** (`gamesradar2026`). GamesRadar+ (2026). Bethesda kills AI fan's viral Fallout game, much to their chagrin. gamesradar.com. <https://www.gamesradar.com/games/fallout/bethesda-kills-ai-fans-viral-fallout-game-much-to-their-chagrin-how-about-you-make-a-fallout-game-instead-so-i-dont-have-to/>. [manual]
- **Game Developer 2012** (`scrolls2012`). Game Developer (2012). ZeniMax settlement blocks Mojang from making more Scrolls games. gamedeveloper.com. <https://gamedeveloper.com/business/zenimax-settlement-blocks-mojang-from-making-more-em-scrolls-em-games>. [manual]
- **Thuum.org dictionary, n.d.** (`thuum_dict4`). Thuum.org (n.d.). Dovahzul Print Dictionary, 4th Edition. thuum.org (fan site; search snippet only). <https://www.thuum.org/library/Dovahzul%20Print%20Dictionary%204th%20Edition.pdf>. [manual]
- **Thuum.org Downloads** (`thuum_downloads`). Thuum.org (n.d.). Downloads. thuum.org (fan site; search snippet only). <https://thuum.org/downloads.php>. [manual]
- **Parf Edhellen forum, n.d.** (`elfdict_forum`). Parf Edhellen (elfdict.com) discussion board (n.d.). Question about copyright. elfdict.com (fan forum; search snippet only). <https://elfdict.com/discuss/5-general_conversation/1072-question_about_copyright>. [manual]
- **ELF FAQ, n.d.** (`elvish_faq`). Elvish Linguistic Fellowship (n.d.). FAQ. elvish.org (search snippet only). <https://elvish.org/FAQ.html>. [manual]
- **Wilhelm 2021** (`bethesda_dragon_language`). Wilhelm, P. (2021). How Bethesda Game Studios made Skyrim's Dragon language. elderscrolls.bethesda.net (Bethesda Softworks). <https://elderscrolls.bethesda.net/en-AU/news/1rL4bCScN6RYXaXQb4ownj/how-bethesda-game-studios-made-skyrims-dragon-language>. [manual]
- **Logical Language Group 1997** (`lojban1997`). Logical Language Group (1997). 1997 Baseline Announcement. tiki.lojban.org. <https://tiki.lojban.org/1997%2BBaseline%2BAnnouncement>. [manual]
