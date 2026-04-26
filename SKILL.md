---
name: paper-source-finder
description: Find academic papers across the web, determine whether each result is a journal paper, conference paper, or preprint, verify venue information, check venue ranking using the appropriate ranking framework, return structured paper metadata and source URLs, and download accessible PDF files when the user requests them.
argument-hint: "[topic, paper title, DOI, venue, author, or ranking-focused query]"
---

# paper-source-finder

## Purpose

Use this skill when the user wants help finding papers, verifying where they were published, distinguishing between journal papers, conference papers, and preprints, checking venue quality, and optionally downloading open-access or otherwise directly accessible PDFs.

This skill is for **paper discovery plus verification**, not just casual search.

## Use When

- The user asks for papers on a topic
- The user wants to know whether a paper is a journal paper, conference paper, or preprint
- The user wants to know the venue name and venue ranking
- The user wants structured paper metadata with links
- The user wants directly accessible PDF files downloaded
- The user wants a shortlist of high-quality papers only

## Do Not Use When

- The user only wants a general web search with no paper verification
- The user already has complete, trusted metadata and only wants a summary
- The task would require bypassing paywalls, captchas, login restrictions, or anti-bot controls
- The user wants a full literature review or thematic synthesis rather than a source-finding and verification workflow

For literature synthesis after discovery, hand off to `deep-research`.

## Core Principles

1. Prefer primary and structured sources over secondary summaries.
2. Never guess publication type or venue ranking.
3. If the ranking framework does not fit the field, say so explicitly.
4. If metadata conflicts across sources, report the conflict instead of silently resolving it.
5. Only download PDFs that are directly and lawfully accessible.

## Inputs To Clarify

Before doing work, clarify the minimum necessary details:

- Search mode:
  - exact paper
  - topic search
  - venue search
  - author search
- Desired count:
  - top 5
  - top 10
  - exhaustive list
- Quality filter:
  - all results
  - high-ranked venues only
  - journal only
  - conference only
  - preprints included or excluded
- Ranking filter:
  - minimum journal tier or quartile
  - minimum conference rank
  - preferred framework only
  - exact venue allowlist / denylist
- Other constraints:
  - year range
  - specific subfield
  - author inclusion or exclusion
  - only papers with DOI
  - only papers with directly accessible PDF
  - language or publisher preferences
- Output needs:
  - metadata only
  - metadata plus links
  - metadata plus PDF download
  - export as Markdown table / CSV / JSON

If the user did not specify these, make a reasonable assumption and say so.

## Source Priority

Load `references/source_priority.md` when you need to decide which source is more trustworthy.

Default source priority:

1. Publisher or official venue page
2. DOI landing page and Crossref-style metadata
3. Official proceedings page
4. DBLP / OpenAlex / Semantic Scholar / OpenReview / arXiv
5. Institutional repository
6. Aggregator pages and blogs

## Publication Type Rules

Load `references/publication_type_rules.md` when classification is non-trivial.

Default labels:

- `journal`
- `conference`
- `preprint`
- `workshop`
- `thesis`
- `other`
- `unknown`

Never collapse `preprint` into `journal` or `conference` unless you have explicit evidence of formal publication.

## Venue Ranking Rules

Load `references/ranking_systems.md` before assigning a venue rank.

Use the ranking system that matches the field:

- Computer science: `CCF`, `CORE`
- Management / information systems / business: `ABS`, `FT50`
- General journal metrics when applicable: `JCR quartile`, `Scopus / CiteScore quartile`, or other field-appropriate systems

If the field is unclear:

1. state that ranking framework selection is uncertain
2. give the venue name
3. return `ranking = unknown` unless you can verify an appropriate framework

## Download Policy

Load `references/download_policy.md` before downloading PDFs.

Allowed:

- direct publisher PDF links with open access
- arXiv PDFs
- institutional repository PDFs
- author-hosted lawful copies when clearly accessible

Not allowed:

- bypassing paywalls
- using leaked mirrors
- using credentials or session tricks without explicit user instruction and lawful access

## Core Workflow

### Step 0: Understand the request

Classify the request into one of:

- exact lookup
- topic discovery
- venue-filtered discovery
- ranking-constrained discovery
- author-focused discovery
- ranking-only verification
- PDF acquisition

### Step 0.5: Normalize user constraints

Translate the user's request into explicit filters:

- topic or exact title
- paper type filter
- ranking threshold
- framework preference
- year range
- open-access / downloadable-only requirement
- desired export format

If the user says things like:

- "只要顶会"
- "只要 Q1 期刊"
- "CCF A 以上"
- "CORE A* 或 A"
- "ABS 3 以上"
- "只要正式发表，不要预印本"

convert them into explicit retrieval constraints and repeat them back briefly before searching.

### Step 1: Search for candidate papers

Preferred search approach:

- Exact title / DOI / known venue:
  - search by exact title first
  - search DOI second
  - verify against official venue or DOI source
- Topic search:
  - start broad
  - narrow by field, venue, and year
  - keep only likely academic papers

For ranking-constrained searches:

- first gather candidate papers broadly enough to avoid missing obvious results
- then filter by verified publication type and verified ranking
- never filter purely on unverified venue strings

### Step 1.5: Apply requirement filters

After collecting candidates but before final output, apply:

- publication-type filter
- venue allowlist / denylist
- ranking threshold
- year constraints
- DOI requirement
- downloadable-PDF requirement

If a filter removes many otherwise relevant papers, say so explicitly.

Use existing browsing/search capabilities available in the environment. If web browsing is needed, coordinate with the installed web-oriented skills rather than inventing ad hoc scraping logic.

### Step 2: Normalize candidate metadata

For each candidate, collect:

- title
- authors
- year
- venue
- DOI
- source URL
- PDF URL if any
- abstract or short description if available

Use `scripts/classify_publication_type.py` if you need fast heuristic classification help.

### Step 3: Verify publication type

For each paper, decide:

- journal
- conference
- preprint
- other / unknown

Use at least one strong signal:

- official journal article page
- official conference proceedings page
- arXiv / SSRN / bioRxiv / medRxiv / OpenReview classification
- DOI metadata

If signals conflict, return:

- `publication_type = conflicting`
- add a short note in `verification_notes`

### Step 4: Determine venue ranking

Use the correct framework for the field and return:

- `ranking_framework`
- `ranking_value`
- `ranking_notes`

Examples:

- `CCF A`
- `CORE A*`
- `ABS 4`
- `JCR Q1`
- `unknown`

Use `scripts/venue_rank_lookup.py` as a helper only. It is a seed lookup, not a complete authority. Final ranking claims must still be verified from the chosen framework.

If the user specified a ranking threshold, explicitly compare each paper against that threshold:

- `passes_filter = yes / no`
- explain why when a paper fails

### Step 4.5: Handle conference-vs-journal quality requests

When the user asks for "high-quality papers" without saying journal or conference:

1. ask or infer whether journal, conference, or both are acceptable
2. use separate ranking logic for conferences and journals
3. do not compare `CCF A` and `JCR Q1` as if they were the same scale
4. if both are included, return the framework for each row

### Step 5: Return structured output

Default output per paper:

- Title
- Authors
- Year
- Publication type
- Venue
- Venue ranking
- Ranking framework
- DOI
- Source page URL
- PDF URL
- Verification notes

If the user asked for multiple papers, provide a compact comparison table first, then short notes below it.

### Step 6: Download PDFs when requested

If the user asked for downloads:

1. verify the PDF is directly accessible
2. download only lawful/open-access or otherwise clearly accessible files
3. save them to a user-specified path if given
4. otherwise save them into a local folder such as `./papers/`
5. report file paths back to the user

Use `scripts/download_pdf.py` for straightforward downloads.

### Step 7: Export when requested

If the user wants export:

- Markdown table
- CSV
- JSON

Use `scripts/export_results.py`.

For topic-search-plus-export requests, prefer:

- Markdown table for quick review
- CSV for spreadsheet workflows
- JSON for downstream automation

## Ready-Made Templates

If the user wants a direct copy-paste prompt, point them to:

- `templates/topic-search-export.md`
- `templates/ranking-filter-search.md`

## Output Contract

### For a small set of papers

Use this structure:

```text
Search scope:
- topic / query
- filters
- assumptions

Results:
1. Title
   - Authors:
   - Year:
   - Type:
   - Venue:
   - Ranking:
   - Ranking framework:
   - DOI:
   - Source URL:
   - PDF URL:
   - Notes:
```

### For a larger set of papers

Use a Markdown table with columns:

| Title | Year | Type | Venue | Ranking | Framework | DOI | Source URL | PDF |

Then add:

- ranking notes
- conflicts
- download summary
- export file path if generated

## Quality Rules

- Never mark a preprint as a journal paper just because the title appears in multiple places.
- Never assign venue ranking without naming the ranking framework.
- If ranking is unavailable, return `unknown` and explain why.
- If a result is likely duplicated across arXiv and a journal/conference page, note both and distinguish preprint from formal publication.
- Prefer one verified paper over five ambiguous papers.

## When To Load References

- `references/source_priority.md`
  - when source trustworthiness is unclear
- `references/publication_type_rules.md`
  - when deciding journal vs conference vs preprint
- `references/ranking_systems.md`
  - when selecting the ranking framework
- `references/download_policy.md`
  - before downloading PDFs

## When To Use Scripts

- `scripts/classify_publication_type.py`
  - for quick local classification support
- `scripts/venue_rank_lookup.py`
  - for seed ranking lookup support
- `scripts/download_pdf.py`
  - for direct PDF downloads
- `scripts/export_results.py`
  - for Markdown / CSV / JSON export

## Example Invocations

```text
Use paper-source-finder to find 10 strong papers on retrieval-augmented generation, identify whether each is journal / conference / preprint, and keep only high-quality venues.
```

```text
Use paper-source-finder to verify whether this paper is formally published or only a preprint, tell me the venue ranking, and give me the source page URL.
```

```text
Use paper-source-finder to search this topic, return a structured table, and download all open-access PDFs into ./papers/.
```

```text
Use paper-source-finder to search a topic, keep only conference papers ranked CCF A or CORE A* / A, return a CSV table, and save it locally.
```

```text
Use paper-source-finder to find journal papers on this topic, keep only Q1 or ABS 3+ venues, exclude preprints, and download directly accessible PDFs.
```
