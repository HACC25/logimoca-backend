#!/usr/bin/env python3
"""
Link crawler for Hawai'i Career Pathways pages.

Reads a JSON file like hi_careers_pages_cleaned.json. For each top-level entry,
crawls the URLs in its "subcontent" list (if present), extracts all http(s) links
from each subcontent page, and updates the "links" list for that subcontent entry.
Top-level entries are not crawled. Writes the updated JSON to an output file
(by default, a new file with a suffix), or in-place with --in-place.

Usage examples:
  python crawl_links.py \
    --input hi_careers_pages_cleaned.json \
    --output hi_careers_pages_with_links.json

  python crawl_links.py --in-place  # overwrites the input JSON

Notes:
- Polite delay between requests is configurable via --delay (seconds).
- Only http(s) links are collected; mailto:, javascript:, tel:, data:, etc. are skipped.
- URL fragments (the portion after '#') are removed.
- Use --domain-only to keep links on the same host as the page URL.
- Use --external-only to keep links that point outside the page's domain.
- Use --max-entries to process only the first N top-level entries for quick tests.
- The last 5 links (footer links) are automatically removed from each subcontent page
  unless --keep-footer-links is specified.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
import os
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Iterable, List, Set
from urllib.parse import urljoin, urldefrag, urlparse

import requests


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (compatible; HCP-LinkCrawler/1.0; +https://hawaiicareerpathways.org)"
)


class AnchorExtractor(HTMLParser):
    """Lightweight HTML anchor tag extractor using stdlib HTMLParser."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hrefs: List[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        if tag.lower() != "a":
            return
        for name, value in attrs:
            if name.lower() == "href" and value:
                self.hrefs.append(value)


def normalize_and_filter_links(
    hrefs: Iterable[str], base_url: str, *, same_domain_only: bool = False, external_only: bool = False
) -> List[str]:
    """Resolve relative URLs, strip fragments, and keep only http(s) links.

    - Relative links are resolved against base_url.
    - Fragments (after '#') are removed to avoid duplicates like page#section.
    - Only http or https schemes are kept.
    - Duplicates are removed preserving original order.
    - If same_domain_only is True, keep only links on the same domain.
    - If external_only is True, keep only links outside the domain.
    """

    seen: Set[str] = set()
    result: List[str] = []
    base_host = urlparse(base_url).netloc.lower()
    for raw in hrefs:
        # Skip obvious non-navigation schemes early
        lower = raw.strip().lower()
        if not lower or lower.startswith(("javascript:", "mailto:", "tel:", "data:", "about:")):
            continue

        absolute = urljoin(base_url, raw)
        absolute, _frag = urldefrag(absolute)
        parsed = urlparse(absolute)
        if parsed.scheme not in ("http", "https"):
            continue
        
        host = (parsed.netloc or "").lower()
        is_same_domain = host == base_host or host.endswith("." + base_host)
        
        if same_domain_only and not is_same_domain:
            continue
        if external_only and is_same_domain:
            continue
            
        if absolute not in seen:
            seen.add(absolute)
            result.append(absolute)
    return result


@dataclass
class CrawlConfig:
    delay_seconds: float = 0.5
    timeout_seconds: float = 15.0
    user_agent: str = DEFAULT_USER_AGENT
    num_footer_links: int = 5  # Number of footer links to remove from each page


def fetch_html(url: str, cfg: CrawlConfig) -> str | None:
    headers = {"User-Agent": cfg.user_agent, "Accept": "text/html,application/xhtml+xml"}
    try:
        resp = requests.get(url, headers=headers, timeout=cfg.timeout_seconds)
        resp.raise_for_status()
        # Only accept text/html-like content
        ctype = resp.headers.get("content-type", "").lower()
        if "text/html" not in ctype and "application/xhtml+xml" not in ctype:
            logging.warning("Skipping non-HTML content at %s (Content-Type: %s)", url, ctype)
            return None
        return resp.text
    except requests.RequestException as exc:
        logging.error("Request failed for %s: %s", url, exc)
        return None


def extract_links_from_html(html: str, base_url: str, *, same_domain_only: bool = False, external_only: bool = False) -> List[str]:
    parser = AnchorExtractor()
    parser.feed(html)
    return normalize_and_filter_links(parser.hrefs, base_url, same_domain_only=same_domain_only, external_only=external_only)


def process_subcontent_entry(entry: dict, cfg: CrawlConfig, *, domain_only: bool, external_only: bool) -> dict:
    """Process a single subcontent entry by fetching its URL and extracting links."""
    url = entry.get("url")
    if not url:
        logging.debug("Subcontent entry missing 'url'; skipping")
        return entry

    logging.info("Crawling subcontent: %s", url)
    html = fetch_html(url, cfg)
    links: List[str] = []
    if html:
        links = extract_links_from_html(html, url, same_domain_only=domain_only, external_only=external_only)
        
        # Remove footer links (last N links that are duplicated across all pages)
        if cfg.num_footer_links > 0 and len(links) > cfg.num_footer_links:
            original_count = len(links)
            links = links[:-cfg.num_footer_links]
            logging.debug("Removed %d footer links from %s (%d -> %d)", 
                         cfg.num_footer_links, url, original_count, len(links))
        
        logging.info("Found %d links at %s", len(links), url)

    # Merge with existing links if present
    existing = entry.get("links")
    if isinstance(existing, list) and existing:
        merged = list(dict.fromkeys([*(existing or []), *links]))  # preserve order, dedupe
    else:
        merged = links

    entry["links"] = merged
    return entry


def process_entry(entry: dict, cfg: CrawlConfig, *, domain_only: bool, external_only: bool) -> dict:
    """Process a top-level entry by crawling all URLs in its subcontent list."""
    subcontent = entry.get("subcontent")
    
    # Skip entries without subcontent or with empty/non-list subcontent
    if not subcontent or not isinstance(subcontent, list):
        logging.debug("Entry has no subcontent list; skipping")
        return entry
    
    # Process each subcontent entry
    updated_subcontent = []
    for sub_entry in subcontent:
        if sub_entry is None or not isinstance(sub_entry, dict):
            # Keep null or non-dict entries as-is
            updated_subcontent.append(sub_entry)
            continue
        
        updated_sub = process_subcontent_entry(sub_entry, cfg, domain_only=domain_only, external_only=external_only)
        updated_subcontent.append(updated_sub)
        time.sleep(cfg.delay_seconds)
    
    entry["subcontent"] = updated_subcontent
    return entry


def load_json(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crawl links for pages listed in a JSON file.")
    root = os.path.dirname(os.path.abspath(__file__))
    parser.add_argument(
        "--input",
        "-i",
        default=f"{root}/hi_careers_pages_cleaned.json",
        help="Path to input JSON file (default: hi_careers_pages_cleaned.json)",
    )
    out = parser.add_mutually_exclusive_group()
    out.add_argument(
        "--output",
        "-o",
        default=None,
        help=(
            "Path to output JSON. If omitted, a new file with suffix _with_links.json"
            " will be created next to the input."
        ),
    )
    out.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite the input JSON file in place.",
    )
    filter_group = parser.add_mutually_exclusive_group()
    filter_group.add_argument(
        "--domain-only",
        action="store_true",
        help="Only keep links on the same domain as each page URL.",
    )
    filter_group.add_argument(
        "--external-only",
        action="store_true",
        help="Only keep links that point outside the page's domain.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay in seconds between requests (default: 0.5)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=15.0,
        help="Request timeout in seconds (default: 15)",
    )
    parser.add_argument(
        "--max-entries",
        type=int,
        default=None,
        help="Process only the first N top-level entries (useful for quick tests).",
    )
    parser.add_argument(
        "--keep-footer-links",
        action="store_true",
        help="Keep all links including footer links (by default, last 5 links are removed).",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Increase logging verbosity (-v, -vv)",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    level = logging.WARNING
    if args.verbose == 1:
        level = logging.INFO
    elif args.verbose >= 2:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    data = load_json(args.input)
    if not isinstance(data, list):
        logging.error("Input JSON must be a list of page entries.")
        return 2

    if args.in_place:
        output_path = args.input
    else:
        output_path = args.output or args.input.replace(
            ".json", "_with_links.json"
        )

    cfg = CrawlConfig(
        delay_seconds=args.delay,
        timeout_seconds=args.timeout,
        num_footer_links=0 if args.keep_footer_links else 5,
    )

    updated: list[dict] = []
    total = len(data) if args.max_entries is None else min(len(data), args.max_entries)
    for idx, entry in enumerate(data[:total], start=1):
        top_url = entry.get("url", "unknown")
        logging.info("Processing top-level entry %d/%d: %s", idx, total, top_url)
        updated.append(process_entry(entry, cfg, domain_only=args.domain_only, external_only=args.external_only))

    # If max-entries was used, append untouched remainder of input
    if total < len(data):
        updated.extend(data[total:])

    save_json(output_path, updated)
    logging.info("Wrote updated JSON: %s", output_path)
    print(f"Updated {len(updated)} entries -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
