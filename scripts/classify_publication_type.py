#!/usr/bin/env python3
import argparse
import json
import re


PREPRINT_HOSTS = {"arxiv.org", "ssrn.com", "biorxiv.org", "medrxiv.org"}
CONFERENCE_HINTS = [
    "proceedings",
    "conference",
    "symposium",
    "workshop",
    "neurips",
    "icml",
    "iclr",
    "cvpr",
    "eccv",
    "iccv",
    "acl",
    "emnlp",
    "naacl",
    "aaai",
    "ijcai",
    "kdd",
]
JOURNAL_HINTS = [
    "journal",
    "transactions",
    "letters",
    "review",
    "quarterly",
]


def classify(url: str, venue: str, notes: str):
    text = " ".join([url or "", venue or "", notes or ""]).lower()
    reasons = []

    for host in PREPRINT_HOSTS:
        if host in text:
            reasons.append(f"matched preprint host: {host}")
            return "preprint", "high", reasons

    if "openreview.net" in text:
        if any(k in text for k in CONFERENCE_HINTS):
            reasons.append("OpenReview record with conference-like hints")
            return "conference", "medium", reasons
        reasons.append("OpenReview record without confirmed proceedings signal")
        return "preprint", "medium", reasons

    if any(k in text for k in JOURNAL_HINTS):
        reasons.append("matched journal-style venue keywords")
        return "journal", "medium", reasons

    if any(k in text for k in CONFERENCE_HINTS):
        reasons.append("matched conference-style venue keywords")
        return "conference", "medium", reasons

    if re.search(r"\bvol\.|\bissue\b|\bissn\b", text):
        reasons.append("matched volume/issue style metadata")
        return "journal", "medium", reasons

    return "unknown", "low", ["no strong classification signal found"]


def main():
    parser = argparse.ArgumentParser(description="Heuristic publication type classifier.")
    parser.add_argument("--url", default="")
    parser.add_argument("--venue", default="")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    publication_type, confidence, reasons = classify(args.url, args.venue, args.notes)
    print(
        json.dumps(
            {
                "publication_type": publication_type,
                "confidence": confidence,
                "reasons": reasons,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
