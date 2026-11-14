# Track 3: What the fan community has already built

Research date: 2026-11-14. Method: ten web searches, the repository's UESP snapshot, and the checked reference lists of tracks 02, 04, 06, 08 and 14. **Thuum.org refuses automated requests and was not opened; every statement about it below comes from search-result summaries of its pages, unless marked otherwise.** Web sources are cited as (Author, `ref-id`); scholarship as (Author Year). Language facts are labelled canon, semi-canon or fan. Checker result for the reference list: `manual: 36, not_found: 1, verified: 13`.

## 1. Bottom line

- **The fan standard has already retreated to canon.** Thuum.org began as a crowd-sourced dictionary of fan coinages, reached about 6,000 fan words, found revising them unsustainable, moved them to an unmaintained "Legacy" section in February 2016, and on 28 March 2026 removed the links to them. Its current Fifth Edition dictionary covers 647 canon words only (Thuum.org, `thuum_dict5`; `thuum_home`; `thuum_news2016`).
- **So the forge would not compete with a live expansion standard; it would revive an approach the main hub abandoned.** That is an opportunity (the vacancy is real) and a warning (the hub tried it and stopped).
- **No licence, terms of reuse or API for Thuum.org's dictionary surfaced.** Treat its text as all rights reserved until the administrator says otherwise. Contact route: private message to the user "paarthurnax" or the address admin@thuum.org given on its Library page; a 2021 forum reply called him rarely active (Thuum.org, `thuum_library`; `thuum_faq2021`).
- **Build the canon layer from the repository's UESP data (CC BY-SA 2.5) and reconcile it against Thuum.org's 647 by hand.** UESP lists 657 headwords; the two lists differ by at least ten entries and probably by tier definitions.
- **Keep forge output visibly separate, separately named and versioned, with a "canon only" switch.** Every successful constructed-language community studied had one accepted source of norms; the failures kept reforming (Garvía 2015; Gordin 2015).
- **Freeze what is accepted.** Thuum.org's stated reason for abandoning expansion was the energy spent revising fan words; Ido and Lojban show the same pattern and the same cure (Thuum.org, `thuum_dict5`; Garvía 2015; Logical Language Group 1997).
- **The teaching side has no real competitor.** The only app found is an Android dictionary last updated in 2015; courses are community Memrise decks. Nothing found combines lessons, spaced practice, rune reading and composition offline.
- **Talk to the community before release**: the administrator first, then the Discord server run by former members (Thuum.org, `thuum_home`).

## 2. Findings by sub-question

### 2.1 Thuum.org: history and who runs it

A personal portfolio page says its author started Thuum.org as a side project near the end of his studies at the University of Wisconsin-Stevens Point (Luckow, `luckow`). The site's administrator and developer signs as "paarthurnax", and a Tumblr blog, "Diary of a Dragonborn", says it is run by the site's owner (Diary of a Dragonborn, `tumblr_diary`). That these are one person is my inference. The site existed by 2013, the year of the first Android app thread (Thuum.org forum, `thuum_app2013`).

Its history has three phases, all seen second-hand:

1. **Expansion (to about 2016).** "A simple crowd-sourced dictionary to which fans could submit new words" (Thuum.org, `thuum_about`, or Luckow, `luckow`; the summary did not say which page). Print dictionaries ran to a Fourth Edition reporting over 11,500 entries and over 5,000 Dovahzul words (Thuum.org, `thuum_dict4`, as reported in track 14). A lesson book and Memrise courses were issued (2.4).
2. **Reset (February 2016).** The "largest update to date" added a new dictionary and a new translator; the old dictionary, translator and search became a "Legacy Dictionary" that is "no longer maintained or supported" (Thuum.org, `thuum_news2016`). A forum thread titled "Starting Anew" exists; only its title was seen (Thuum.org forum, `thuum_startinganew`). The Fifth Edition preface gives the reason: "a lot of energy being put toward revising the 6,000 fanmade words" (Thuum.org, `thuum_dict5`, wording as rendered by the search summary).
3. **Canon reference (2026).** A home-page notice dated 28 March 2026 says the owner will keep hosting the site as a reference for the official canon, will add vocabulary from The Elder Scrolls Online, and has removed the links to the fan-made parts, which had been "retired about 10 years ago" but kept for reference. Older dictionaries with fan vocabulary remain in the Library (Thuum.org, `thuum_home`; `thuum_library`).

Membership numbers were not found. Forum threads surfaced date mostly from 2013 to 2016, with a few from 2021; the 2026 notice and the Fifth Edition show the site is maintained but quiet (my reading of the dates).

### 2.2 Dictionary size and tiers

- **Current:** 647 words "attested in the canonical language", each with a detailed entry, "compiled by examining the entirety of the corpus"; sourced "entirely from official content" (Thuum.org, `thuum_dict5`). The edition's date was not confirmed; one summary called it the 2026 dictionary.
- **Repository comparison (canon data):** the UESP dictionary has 657 headwords. By the wiki's own citations, 163 rest only on the Prima guide and 91 only on a fan-hosted list of untraced origin (UESP contributors, `uesp2026lang`; my count from `canon-lexicon.json`). A 2016 forum post says a canon word submitted to Thuum.org must cite a source "in Skyrim or the Prima Games guide" (Thuum.org forum, `thuum_canon_thread` or `thuum_canon_question`; the summary did not say which). Thuum.org therefore seems to count the Prima guide as canon, where this project calls it semi-canon (inference).
- **Legacy tiers (fan):** the manual defines *semi-canon* as a word derived from a canon word and *non-canon* as a word with no relation to canon or semi-canon words. A canon affix does not raise the tier: *Vokorah* "disbelieve" is non-canon because its root *Korah* is non-canon, although *vo-* is canon (Thuum.org, `thuum_manual`). The Legacy Dictionary address carries a `canon=3` parameter, which suggests a three-level filter (inference from the address; Thuum.org, `thuum_legacy`).

### 2.3 Rules and process for inventing words (fan, legacy)

What surfaced (Thuum.org, `thuum_manual`; forum threads `thuum_canon_thread`, `thuum_canon_question`):

- New words "must remain rooted to Skyrim and The Elder Scrolls universe".
- Words for modern concepts must be built from existing words.
- Non-canon roots could be made up freely but had to follow the language's spelling conventions.
- Submission was open to members. No voting or review mechanism was confirmed by any summary.

No phonotactic test, no check for clashes with existing forms and no freeze rule were visible. The outcome, by the site's own account, was a revision burden heavy enough to end the programme.

### 2.4 Grammar conventions and lessons

Canon side (canon data): the UESP grammar notes give plural by doubling the last letter and adding *e* (*kel*, *kelle*), possessive *-i* (or *-l* after *ii*) and *-u* "our", perfect *-aan*, heavy compounding and head-initial order. Track 02 found these notes to be an editor's analysis, not developer statements.

Thuum.org side (fan): *Learning Dovahzul: The Unofficial Guide to the Dragon Language of Skyrim* is a 53-page printable book covering pronunciation, the alphabet, grammar, verbs and tense, reading and exercises. **Each topic is tagged canon or non-canon.** Non-canon affixes are marked, among them the suffixes *-o* and *-a* and the prefix *ni-* "non-" (Thuum.org, `thuum_lessonbook`; `thuum_news_lessonbook`). I could not see what *-o* and *-a* mean, how tense is taught, or the lesson order. A third-party 2026 guide calls the site's grammar "a fan hypothesis layered on top of a small official base" (LearningElvish.com, `learningelvish_phrases`).

### 2.5 Downloads, API, licence, contact

- **Downloads:** print dictionaries (Third to Fifth Editions as PDF), the lesson book, and a Dragon Alphabet font, which UESP links as the source of its own sample (Thuum.org, `thuum_library`; `thuum_downloads`; `thuum_dict3`; UESP contributors, `uesp2026fonts`). A spreadsheet export was not confirmed.
- **API:** none found. The "Thuum Translator API" at Fun Translations is a separate paid commercial service (Fun Translations, `funtranslations`).
- **Licence:** none found on any page summarised. The print dictionary states that the dragon language is a creation of Bethesda Softworks LLC; that is an attribution, not a licence. The Android app's code is Apache 2.0, with a lexicon "kindly powered by" Thuum.org (zolianmawia, `github_dict_app`; Thuum.org forum, `thuum_app_official`); a licence on the code does not clearly cover the word list (inference; see track 04).
- **Contact:** private message to "paarthurnax" or admin@thuum.org (Thuum.org, `thuum_library`; `thuum_faq2021`).

### 2.6 Everything else

| Resource | What it offers | Activity | As a learning tool |
|---|---|---|---|
| Dovahzul Dictionary, Android (zolianmawia, `github_dict_app`; APKPure, `apkpure_dict_app`; Thuum.org forum, `thuum_app_official`) | Offline dictionary of 3,500+ words, sentence translator; open source | Version 2.1.0, last updated 2015; a forum user calls it out of date | Lookup only; mixes canon and legacy fan words; no iOS version (a 2013 post said none was planned) |
| Memrise community courses (Memrise, `memrise_dovahzul`; Thuum.org, `thuum_news_memrise`; forum `thuum_memrise_runes`, `thuum_memrise_shouts`) | A canon course, a non-canon course, a shouts course (2016), a runes-to-English variant (August 2021) | No activity seen after 2021 | The only spaced practice available; word-pair recall only; depends on a third-party platform |
| Thuum.org Discord server (Thuum.org, `thuum_home`; forum `thuum_faq2021`) | Chat for "learning and chatting"; made by former community members, not the owner | Unknown; not seen | Probably the only live conversation venue |
| Fun Translations Thuum translator (Fun Translations, `funtranslations`) | English to dragon-language conversion, paid API | Commercial | Vocabulary source undisclosed in what I saw |
| Hobby translators on GitHub (Ankit-Nag, `github_ankit`; cat16, `github_cat16`) | One wraps the Fun Translations API; one goes dragon to English | Roughly six years old | Demonstrations |
| LearningElvish.com posts (LearningElvish.com, `learningelvish2026`; `learningelvish_phrases`) | Word and phrase lists, dated 2026 | New | Article, not a course |
| Fonts (track 02; UESP contributors, `uesp2026fonts`) | Thuum.org's Dragon Alphabet font and a numbered variant; older fan fonts | Static | Licences unclear; see tracks 02 and 08 |

Not surfaced in ten searches: a subreddit, an Anki shared deck, a video course, an iOS app, a keyboard app, a LingoJam translator. Absence from my searches is not evidence that they do not exist. A forum thread titled "Dragon Runes Unicode" exists; only its title was seen (Thuum.org forum, `thuum_unicode`).

### 2.7 Where community norms diverge from canon

1. **The name.** "Dovahzul" is a fan term (track 02; canon data README). Thuum.org's own Fifth Edition is now titled *Dragon Language Dictionary*, where the Third and Fourth were *Dovahzul* dictionaries (titles as listed in search results).
2. **Tier words.** "Semi-canon" means *derived from canon* at Thuum.org and *official but not in a game* in this repository; "canon" seems to include the Prima guide there and not here.
3. **Counts.** 647 (Thuum.org), 657 (UESP), "about 640" (Thuum.org translator page, per track 02).
4. **Legacy vocabulary still circulates.** The 2015 app, the non-canon Memrise course, the Third and Fourth Edition PDFs and copies of the lesson book on document-sharing sites all carry fan words and fan affixes. A learner searching today meets a mixture with no reliable labels.
5. **Grammar.** Fan analyses (on UESP and in the lesson book) read as rules, though no developer has confirmed them.

### 2.8 The risk of a rival standard: what the scholarship shows

- **Esperanto and Ido.** In 1907 a reform project, Ido, split the Esperanto movement, drawing off several prominent leaders while most ordinary members stayed (Forster 1982; Garvía 2015). Garvía's comparative history credits Esperanto's survival to an untouchable core (the *Fundamento*, 1905) and to its inventor giving up personal control, and attributes Ido's decline, among other causes, to continuous reform, which kept making learners' knowledge and materials obsolete; Volapük had collapsed earlier in a fight between its inventor's claim of ownership and a reforming academy (Garvía 2015; Gordin 2015). Esperanto norms have since been kept by an academy plus speakers policing themselves (Fiedler 2006; Blanke 2009).
- **Loglan and Lojban.** A dispute over the inventor's claimed ownership led a group to rebuild the vocabulary from nothing as Lojban; a US appeals court cancelled the *Loglan* trademark as generic in 1992 (Okrent 2009 [book not in the registry; confirmed in track 14]; Loglan Institute v. Logical Language Group 1992, holding seen in secondary commentary). Lojban's body then declared a baseline with a multi-year freeze (Logical Language Group 1997).
- **Klingon and Na'vi.** Both communities stay unified by accepting new words only from the creator; Na'vi fans organised a project to submit proposals for his approval (Okrent 2009; Schreyer 2011; Schreyer 2015). The cost is slow growth and lasting gaps.
- **Tolkien's Elvish.** With the creator dead, students divided between scholarship on attested forms and "Neo-Elvish" composition, with lasting friction (Hostetter 2007).
- **Standardisation theory.** A standard needs selection, codification, elaboration and acceptance (Haugen 1966); its authority rests on users' belief in its legitimacy more than on any property of the forms (Milroy 2001).

Inference for Dovahzul: its position is the Elvish one (no engaged creator) with a Klingon-style community preference (canon only), reached after a failed Ido-style phase of open reform. A forge that presents its output as "Dovahzul" invites the schism; a forge that presents a named, optional, frozen extension on top of an agreed canon does not compete for the same ground. Research on software forks, a looser analogy, adds that the freedom to fork works as a check on those who govern a project, and that forks commonly follow disputes over direction or a project going quiet (Nyman and Lindman 2013; Robles and González-Barahona 2012).

## 3. What this means for the app

1. **Canon reconciliation table (confidence: high).** Add `canon-reconciliation.json`: one row per headword with `uesp` (bool), `thuum5` (bool), `sources[]`, `note`. The owner fills `thuum5` by reading the Fifth Edition PDF in person; do not scrape. Release gate: zero unexplained differences. Evidence: 657 against 647.
2. **Provenance with unambiguous names (high).** Every lexeme and grammar rule carries `tier` in {`game`, `official_print`, `fan_legacy`, `forge`}. Never show a bare "semi-canon". A global "canon only" setting hides the last two tiers in dictionary, lessons, drills and translator. Evidence: Thuum.org's lesson book tags every topic; the terminology clash in 2.7.
3. **Teach canon first (high).** The default course uses only `game` and `official_print` material and the fan-analysed grammar marked as analysis. Forge vocabulary enters in a separate, opt-in track. Evidence: the hub's current stance; Klingon and Na'vi practice.
4. **Name and version the extension (medium).** Call forge output by its own name and release tag, never plain "Dovahzul". Show the tag on every forge word.
5. **Immutability rule (high for the rule; the numbers are my proposal).** An accepted forge entry never changes form or meaning. The only later operation is `deprecated_by: <id>`. Publish at most one release per quarter, capped at about 50 entries, starting with the conversation kit from track 14. Evidence: Thuum.org's 6,000-word revision burden; Ido; the Lojban baseline.
6. **Stricter validation than the legacy process (high).** Thuum.org required only Elder Scrolls rootedness, building modern terms from existing words and spelling conventions. The forge validator should add what was missing: phonotactic conformance (track 01 data), a homograph check against all tiers, a derivation record (`parts[]`), and a gap justification.
7. **Legacy collision and adoption check, only with permission (medium).** If the administrator licenses the legacy list, load it as `fan_legacy` reference data: reject a proposal whose form matches a legacy word with a different meaning; where a legacy word for the same meaning passes the forge's rules, adopt it with credit. Without permission, do not bundle the list.
8. **Outreach sequence (high).** (a) Write to the administrator: ask for reuse terms for the Fifth Edition and the legacy list, and ask about the name and linking. (b) Introduce the project on the Discord server. (c) If there is no answer after 30 days, ship with UESP-derived data only, copy nothing from Thuum.org, and link to it as the canon reference. Legal analysis is in track 04.
9. **Open, exportable data (medium).** Publish the lexicon as JSON and CSV with stable ids, tiers and a clear licence. Nothing of the kind exists: no API, no licensed data set. Evidence: 2.5; fork research on openness as a governance check.
10. **Honest translator (medium).** Output word by word with tier badges; mark words with no entry as untranslatable; never coin silently.
11. **Decision log (medium).** Publish every forge ruling with rule citations, and state plainly that the owner decides. Legitimacy has to come from visible process, since no creator stands behind the forge (Haugen 1966; Milroy 2001; inference).

## 4. Contested or weak evidence

- Everything about Thuum.org rests on search summaries. Quoted phrases are the summaries' renderings and may not be exact.
- Dates are loose: the Fifth Edition is undated in what I saw; "retired about 10 years ago" fits the February 2016 update but the "Starting Anew" thread was not read.
- The link between the portfolio page, the administrator name and the Tumblr blog is an inference.
- Whether Thuum.org counts Prima-only words as canon is inferred from one forum post.
- Whether the Discord community still coins words is unknown. If it does, a second fan standard already exists.
- The schism literature is historical case study, without measurement. Applying it to a 650-word game language is analogy. The fork studies concern software.
- Okrent (2009) is a trade book and is not in the registry.
- My recollection, not checked in this run: Memrise moved community-made courses off its main apps in 2024, which would make those decks harder to reach.

## 5. Gaps, and anything blocked

- Thuum.org returns 403 to automated clients; this was respected. WebFetch does not work in this environment.
- Not established: any licence or terms; membership; the legacy voting or approval mechanism; a spreadsheet export; the full lesson sequence; the meaning of the non-canon affixes; the exact difference between the 647 and 657 lists.
- Treated briefly: other translators, fonts and keyboards (tracks 02 and 08 cover fonts), video courses, forums other than Thuum.org.
- Not surfaced: Reddit, Anki, YouTube, iOS, keyboards, LingoJam.
- No scholarship on the Dovahzul community was found. Windsor (2026), a handbook chapter on constructed languages in games that track 02's checker verified, was not read and is listed only as a lead.

## 6. References

Generated from `research/refs/community-landscape.json`; each line ends with its checker status. Checker result: `manual: 36, not_found: 1, verified: 13`. All 36 manual entries are web or legal sources; every thuum.org address appeared in this run's search results and none was fetched.

**Scholarship**

- Blanke, D. (2009). Causes of the relative success of Esperanto. Language Problems and Language Planning. doi:10.1075/lplp.33.3.04bla `blanke2009: verified`
- Fiedler, S. (2006). Standardization and self-regulation in an international speech community: the case of Esperanto. International Journal of the Sociology of Language. doi:10.1515/IJSL.2006.005 `fiedler2006: verified`
- Forster, P. G. (1982). The Esperanto Movement. Mouton (De Gruyter). doi:10.1515/9783110824568 `forster1982: verified`
- Garvía, R. (2015). Esperanto and Its Rivals: The Struggle for an International Language. University of Pennsylvania Press. doi:10.9783/9780812291278 `garvia2015: verified`
- Gordin, M. D. (2015). Scientific Babel: How Science Was Done Before and After Global English. University of Chicago Press. doi:10.7208/chicago/9780226000329.001.0001 `gordin2015: verified`
- Haugen, E. (1966). Dialect, Language, Nation. American Anthropologist. doi:10.1525/aa.1966.68.4.02a00040 `haugen1966: verified`
- Hostetter, C. F. (2007). Tolkienian Linguistics: The First Fifty Years. Tolkien Studies. doi:10.1353/tks.2007.0022 `hostetter2007: verified`
- Milroy, J. (2001). Language ideologies and the consequences of standardization. Journal of Sociolinguistics. doi:10.1111/1467-9481.00163 `milroy2001: verified`
- Nyman, L.; Lindman, J. (2013). Code Forking, Governance, and Sustainability in Open Source Software. Technology Innovation Management Review. doi:10.22215/timreview/644 `nyman2013: verified`
- Okrent, A. (2009). In the Land of Invented Languages. Spiegel & Grau. `okrent2009: not_found` [UNVERIFIED by registry: trade book, Spiegel & Grau; the registry lists a 2012 review of it, doi:10.1111/j.1548-1395.2012.01128.x; confirmed by search in track 14, not re-searched here]
- Robles, G.; González-Barahona, J. M. (2012). A Comprehensive Study of Software Forks: Dates, Reasons and Outcomes. Open Source Systems: Long-Term Sustainability (IFIP AICT 378), Springer. doi:10.1007/978-3-642-33442-9_1 `robles2012: verified`
- Schreyer, C. (2011). Media, information technology, and language planning: what can endangered language communities learn from created language communities?. Current Issues in Language Planning. doi:10.1080/14664208.2011.604965 `schreyer2011: verified`
- Schreyer, C. (2015). The digital fandom of Na'vi speakers. Transformative Works and Cultures. doi:10.3983/twc.2015.0610 `schreyer2015: verified`
- Windsor, J. W. (2026). Conlangs in Video and Table-Top Gaming. The Palgrave Handbook of Constructed Languages (Springer Nature Switzerland). doi:10.1007/978-3-032-03277-5_10 `windsor2026: verified` [not read; listed as a lead only]

**Web, legal and community sources**

- Ankit-Nag (GitHub user) (n.d.). dovahzul-translator. GitHub. https://github.com/Ankit-Nag/dovahzul-translator `github_ankit: manual` [search summary only]
- APKPure (n.d.). Dovahzul Dictionary APK for Android Download [store mirror listing, version 2.1.0]. APKPure. https://apkpure.com/dovahzul-dictionary/net.fernandezgodinho.pedro.dovahzuldictionary `apkpure_dict_app: manual` [search summary only]
- cat16 (GitHub user) (n.d.). dovahzul-translator. GitHub. https://github.com/cat16/dovahzul-translator `github_cat16: manual` [search summary only]
- Diary of a Dragonborn (n.d.). Diary of a Dragonborn [Tumblr blog that says it is run by the owner of Thuum.org]. Tumblr. https://www.tumblr.com/diaryofadragonborn `tumblr_diary: manual` [search summary only]
- Fun Translations (n.d.). Thuum Translator API. funtranslations.com. https://funtranslations.com/api/thuum `funtranslations: manual` [search summary only]
- LearningElvish.com (2026). Dovahzul Dictionary: Common Dragon Language Words (2026). learningelvish.com blog. https://learningelvish.com/blog/dovahzul-dictionary-common-words `learningelvish2026: manual` [search summary only]
- LearningElvish.com (n.d.). Dovahzul Words & Phrases: Skyrim Dragon Language Guide. learningelvish.com blog. https://learningelvish.com/blog/dovahzul-words-phrases-skyrim `learningelvish_phrases: manual` [search summary only]
- Logical Language Group (1997). 1997 Baseline Announcement. tiki.lojban.org. https://tiki.lojban.org/1997%2BBaseline%2BAnnouncement `lojban1997: manual` [URL taken from track 14, not seen in this run]
- Luckow, M. (n.d.). Thuum.org [project page on a personal portfolio site]. matthewluckow.com. https://matthewluckow.com/project/thuum-org/ `luckow: manual` [search summary only]
- Memrise (n.d.). Learn Dovahzul with Memrise. memrise.com. https://www.memrise.com/en/learn-dovahzul `memrise_dovahzul: manual` [search summary only]
- Thuum.org (2016). Site Update, February 6, 2016. thuum.org news. https://www.thuum.org/viewnews.php?thread=181 `thuum_news2016: manual` [search summary only]
- Thuum.org (2026). Thuum.org - The Dragon Language Dictionary [home page; carries a site notice dated 28 March 2026]. thuum.org. https://www.thuum.org/ `thuum_home: manual` [search summary only]
- Thuum.org (n.d.). About. thuum.org. https://www.thuum.org/about.php `thuum_about: manual` [search summary only]
- Thuum.org (n.d.). Dovahzul Dictionary: Dovahzul-English, English-Dovahzul, Third Edition. thuum.org (PDF). https://www.thuum.org/assets/Dovahzul%20Print%20Dictionary%203rd%20Edition.pdf `thuum_dict3: manual` [search summary only]
- Thuum.org (n.d.). Dovahzul Print Dictionary, 4th Edition. thuum.org Library (PDF). https://www.thuum.org/library/Dovahzul%20Print%20Dictionary%204th%20Edition.pdf `thuum_dict4: manual` [figures as reported in track 14]
- Thuum.org (n.d.). Downloads. thuum.org. https://www.thuum.org/downloads.php `thuum_downloads: manual` [search summary only]
- Thuum.org (n.d.). Dragon Language Dictionary: Dragon-English, English-Dragon, Fifth Edition. thuum.org Library (PDF). https://www.thuum.org/library/Dragon_Language_Print_Dictionary_5th_Edition.pdf `thuum_dict5: manual` [search summary only]
- Thuum.org (n.d.). Learning Dovahzul: The Unofficial Guide to the Dragon Language of Skyrim. thuum.org (PDF). https://www.thuum.org/assets/Learning%20Dovahzul.pdf `thuum_lessonbook: manual` [search summary only]
- Thuum.org (n.d.). Legacy Dictionary. thuum.org. https://www.thuum.org/dictionary-legacy.php?letter=S&mode=english&canon=3 `thuum_legacy: manual` [search summary only]
- Thuum.org (n.d.). Lesson Book & Second Edition Print Dictionary. thuum.org news. https://www.thuum.org/viewnews.php?thread=101 `thuum_news_lessonbook: manual` [search summary only]
- Thuum.org (n.d.). Library. thuum.org. https://www.thuum.org/library.php `thuum_library: manual` [search summary only]
- Thuum.org (n.d.). Manual [contributor guidance: canon, semi-canon and non-canon words]. thuum.org. https://www.thuum.org/manual.php `thuum_manual: manual` [search summary only]
- Thuum.org (n.d.). Non-Canon Memrise Course. thuum.org news. https://www.thuum.org/viewnews.php?page=1&thread=141 `thuum_news_memrise: manual` [search summary only]
- Thuum.org forum members (2013). Dovahzul Dictionary -- Android app [forum thread]. thuum.org forum. https://www.thuum.org/viewthread.php?thread=137 `thuum_app2013: manual` [search summary only]
- Thuum.org forum members (2016). Memrise: "Dovahzul: Dragon Shouts" [forum thread]. thuum.org forum. https://www.thuum.org/viewthread.php?thread=1387 `thuum_memrise_shouts: manual` [search summary only]
- Thuum.org forum members (2021). An Updated FAQ [forum thread]. thuum.org forum. https://www.thuum.org/viewthread.php?thread=2078 `thuum_faq2021: manual` [search summary only]
- Thuum.org forum members (2021). New Memrise course for translating from runes to English [forum thread]. thuum.org forum. https://www.thuum.org/viewthread.php?thread=2049 `thuum_memrise_runes: manual` [search summary only]
- Thuum.org forum members (n.d.). Canon, Non-Canon and Semi-Canon Words [forum thread]. thuum.org forum. https://www.thuum.org/viewthread.php?thread=1319 `thuum_canon_thread: manual` [search summary only]
- Thuum.org forum members (n.d.). Canon, Semi-Canon and Non-Canon [question thread]. thuum.org forum. https://www.thuum.org/viewquestion.php?question=193 `thuum_canon_question: manual` [search summary only]
- Thuum.org forum members (n.d.). Dragon Runes Unicode [forum thread; title only seen]. thuum.org forum. https://www.thuum.org/viewthread.php?thread=2050 `thuum_unicode: manual`
- Thuum.org forum members (n.d.). Starting Anew [forum thread; title only seen]. thuum.org forum. https://www.thuum.org/viewthread.php?thread=1191 `thuum_startinganew: manual`
- Thuum.org forum members (n.d.). The official Dovahzul Dictionary Android App [forum thread]. thuum.org forum. https://www.thuum.org/viewthread.php?thread=223 `thuum_app_official: manual` [search summary only]
- UESP contributors (2026). General:Fonts. UESP, The Unofficial Elder Scrolls Pages (CC BY-SA 2.5). https://uesp.net/wiki/General:Fonts `uesp2026fonts: manual` [in the repository snapshot]
- UESP contributors (2026). Lore:Dragon Language (revision 3619598, 24 August 2026). UESP, The Unofficial Elder Scrolls Pages (CC BY-SA 2.5). https://en.uesp.net/wiki/Lore:Dragon_Language `uesp2026lang: manual` [in the repository snapshot; source of canon-lexicon.json]
- United States Court of Appeals for the Federal Circuit (1992). Loglan Institute, Inc. v. Logical Language Group, Inc., 962 F.2d 1038 (Fed. Cir. 1992). Federal Reporter, Second Series. https://technollama.co.uk/can-you-copyright-the-klingon-language `loglan1992: manual` [reporter citation recalled; the URL is secondary commentary taken from track 14, not seen in this run]
- zolianmawia (GitHub user) (n.d.). Dovahzul-Dictionary [source repository of the Android dictionary app]. GitHub. https://github.com/zolianmawia/Dovahzul-Dictionary `github_dict_app: manual` [search summary only]
