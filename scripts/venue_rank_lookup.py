#!/usr/bin/env python3
import argparse
import json


SEED_RANKS = {
    "neurips": {"framework": "CCF", "rank": "A"},
    "icml": {"framework": "CCF", "rank": "A"},
    "iclr": {"framework": "CCF", "rank": "A"},
    "cvpr": {"framework": "CCF", "rank": "A"},
    "acl": {"framework": "CCF", "rank": "A"},
    "emnlp": {"framework": "CCF", "rank": "B"},
    "aaai": {"framework": "CCF", "rank": "A"},
    "ijcai": {"framework": "CCF", "rank": "A"},
    "kdd": {"framework": "CCF", "rank": "A"},
    "jmlr": {"framework": "CCF", "rank": "B"},
    "ieee transactions on pattern analysis and machine intelligence": {
        "framework": "CCF",
        "rank": "A",
    },
    "mis quarterly": {"framework": "ABS", "rank": "4*"},
    "information systems research": {"framework": "ABS", "rank": "4*"},
    "decision support systems": {"framework": "ABS", "rank": "3"},
}


def lookup(venue: str):
    key = venue.strip().lower()
    if key in SEED_RANKS:
        return {"matched": True, **SEED_RANKS[key], "notes": "matched built-in seed table"}

    for candidate, result in SEED_RANKS.items():
        if candidate in key or key in candidate:
            return {"matched": True, **result, "notes": f"fuzzy match on seed table: {candidate}"}

    return {
        "matched": False,
        "framework": "unknown",
        "rank": "unknown",
        "notes": "not found in built-in seed table; verify externally",
    }


def main():
    parser = argparse.ArgumentParser(description="Seed venue ranking lookup.")
    parser.add_argument("--venue", required=True)
    args = parser.parse_args()
    print(json.dumps(lookup(args.venue), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
