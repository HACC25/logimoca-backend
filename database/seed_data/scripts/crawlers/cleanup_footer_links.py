#!/usr/bin/env python3
"""
Remove footer links from subcontent entries in hi_careers JSON files.

The last 5 links on each subcontent page are footer links that are duplicated
across all pages and not relevant to the page content. This script removes them.

Usage:
  python cleanup_footer_links.py --input hi_careers_pages_cleaned_with_links.json
  python cleanup_footer_links.py --in-place  # overwrites input file
"""

import argparse
import json
import sys
from typing import List


def cleanup_subcontent_links(entry: dict, *, num_footer_links: int = 5) -> dict:
    """Remove the last N links from all subcontent entries."""
    subcontent = entry.get("subcontent")
    
    if not subcontent or not isinstance(subcontent, list):
        return entry
    
    cleaned_subcontent = []
    for sub_entry in subcontent:
        if sub_entry is None or not isinstance(sub_entry, dict):
            cleaned_subcontent.append(sub_entry)
            continue
        
        links = sub_entry.get("links")
        if isinstance(links, list) and len(links) > num_footer_links:
            # Remove last N links (footer links)
            sub_entry["links"] = links[:-num_footer_links]
        
        cleaned_subcontent.append(sub_entry)
    
    entry["subcontent"] = cleaned_subcontent
    return entry


def load_json(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: list) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove footer links from subcontent entries in JSON file."
    )
    parser.add_argument(
        "--input",
        "-i",
        default="hi_careers_pages_cleaned_with_links.json",
        help="Path to input JSON file (default: hi_careers_pages_cleaned_with_links.json)",
    )
    out = parser.add_mutually_exclusive_group()
    out.add_argument(
        "--output",
        "-o",
        default=None,
        help="Path to output JSON. If omitted, creates a new file with _cleaned suffix.",
    )
    out.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite the input JSON file in place.",
    )
    parser.add_argument(
        "--num-footer-links",
        type=int,
        default=5,
        help="Number of footer links to remove from end of each links list (default: 5)",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    
    data = load_json(args.input)
    if not isinstance(data, list):
        print("Error: Input JSON must be a list of page entries.", file=sys.stderr)
        return 2
    
    if args.in_place:
        output_path = args.input
    else:
        output_path = args.output or args.input.replace(".json", "_cleaned.json")
    
    # Process all entries
    cleaned_data = []
    total_removed = 0
    for entry in data:
        cleaned_entry = cleanup_subcontent_links(entry, num_footer_links=args.num_footer_links)
        
        # Count how many links were removed
        subcontent = entry.get("subcontent", [])
        for sub in subcontent:
            if isinstance(sub, dict) and isinstance(sub.get("links"), list):
                original_count = len(sub.get("links", []))
                if original_count > args.num_footer_links:
                    total_removed += args.num_footer_links
        
        cleaned_data.append(cleaned_entry)
    
    save_json(output_path, cleaned_data)
    print(f"Processed {len(cleaned_data)} entries")
    print(f"Removed approximately {total_removed} footer links")
    print(f"Wrote cleaned JSON: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
