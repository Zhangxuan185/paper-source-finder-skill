#!/usr/bin/env python3
import argparse
import os
import sys
import urllib.request
from urllib.error import HTTPError, URLError


def main():
    parser = argparse.ArgumentParser(description="Download a directly accessible PDF.")
    parser.add_argument("--url", required=True)
    parser.add_argument("--output-dir", default="./papers")
    parser.add_argument("--filename", default="")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    filename = args.filename or os.path.basename(args.url.split("?")[0]) or "paper.pdf"
    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"
    output_path = os.path.join(args.output_dir, filename)

    req = urllib.request.Request(args.url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            content_type = (resp.headers.get("Content-Type") or "").lower()
            if "pdf" not in content_type and not args.url.lower().endswith(".pdf"):
                print("Refusing download: URL does not appear to be a PDF.", file=sys.stderr)
                sys.exit(2)
            with open(output_path, "wb") as f:
                f.write(resp.read())
    except HTTPError as e:
        print(f"HTTP error: {e.code}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"URL error: {e}", file=sys.stderr)
        sys.exit(1)

    print(output_path)


if __name__ == "__main__":
    main()
