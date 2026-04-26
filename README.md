# paper-source-finder-skill

A Codex skill for finding academic papers, identifying whether each paper is a
journal article, conference paper, preprint, or another publication type, and
recording venue ranking information when available.

## What It Does

- Search for papers by topic, title, DOI, author, or venue.
- Classify publication source types such as journal, conference, preprint, and workshop.
- Look up venue ranking frameworks such as CCF, CORE, JCR, ABS/AJG, and related lists.
- Export structured paper results to Markdown, CSV, or JSON.
- Download openly accessible PDFs when the user explicitly asks and the source is legal to access.

## Usage

After installing this skill into `~/.codex/skills`, restart Codex and use:

```text
Use paper-source-finder for this task.

Please find papers about:
[topic]

Requirements:
1. Identify whether each paper is a journal article, conference paper, or preprint.
2. Include venue name and ranking framework where available.
3. Return a structured table with title, authors, year, DOI, source URL, and PDF URL.
```

## Install From GitHub

```bash
python /mnt/c/Users/DELL/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Zhangxuan185/paper-source-finder-skill \
  --path . \
  --name paper-source-finder \
  --dest ~/.codex/skills
```

## Notes

This skill does not include private API keys or account credentials. If a search
service requires authentication, configure credentials separately in your local
environment.
