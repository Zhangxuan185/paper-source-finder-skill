#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path


FIELDS = [
    "title",
    "authors",
    "year",
    "publication_type",
    "venue",
    "ranking",
    "ranking_framework",
    "doi",
    "source_url",
    "pdf_url",
    "verification_notes",
]


def load_records(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return [data]
    return data


def to_markdown(records):
    header = "| " + " | ".join(FIELDS) + " |"
    sep = "| " + " | ".join(["---"] * len(FIELDS)) + " |"
    rows = []
    for record in records:
        rows.append("| " + " | ".join(str(record.get(f, "")).replace("\n", " ") for f in FIELDS) + " |")
    return "\n".join([header, sep] + rows)


def to_csv(records, path: Path):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for record in records:
            writer.writerow({k: record.get(k, "") for k in FIELDS})


def main():
    parser = argparse.ArgumentParser(description="Export normalized paper records.")
    parser.add_argument("--input", required=True, help="Input JSON file")
    parser.add_argument("--format", choices=["markdown", "csv", "json"], required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    records = load_records(Path(args.input))
    output = Path(args.output)

    if args.format == "markdown":
        output.write_text(to_markdown(records), encoding="utf-8")
    elif args.format == "csv":
        to_csv(records, output)
    else:
        output.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    print(str(output))


if __name__ == "__main__":
    main()
