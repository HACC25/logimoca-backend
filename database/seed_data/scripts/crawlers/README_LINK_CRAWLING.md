# Link Crawling Scripts

This directory contains scripts for crawling and extracting links from Hawaii Career Pathways web pages.

## Scripts

### `crawl_links.py`
Main crawler that extracts links from subcontent pages in the Hawaii Career Pathways JSON data.

**Features:**
- Crawls only URLs found in `subcontent` lists (not top-level entries)
- Automatically removes the last 5 footer links from each page (configurable)
- Supports domain filtering (internal-only or external-only)
- Polite rate limiting with configurable delays
- Progress tracking and verbose logging

**Usage:**
```bash
# Basic usage - crawls all subcontent pages
python3 crawl_links.py \
  --input hi_careers_pages_cleaned.json \
  --output hi_careers_pages_with_links.json \
  -v

# Test with first 5 entries only
python3 crawl_links.py --max-entries 5 -v

# Keep footer links (don't remove last 5)
python3 crawl_links.py --keep-footer-links -v

# Only capture external links
python3 crawl_links.py --external-only -v

# Only capture internal links
python3 crawl_links.py --domain-only -v

# Overwrite input file in-place (careful!)
python3 crawl_links.py --in-place -v
```

**Options:**
- `--input, -i`: Input JSON file (default: hi_careers_pages_cleaned.json)
- `--output, -o`: Output JSON file (default: adds _with_links suffix)
- `--in-place`: Overwrite input file
- `--domain-only`: Only keep links on same domain
- `--external-only`: Only keep external links
- `--delay`: Delay between requests in seconds (default: 0.5)
- `--timeout`: Request timeout in seconds (default: 15)
- `--max-entries`: Process only first N top-level entries
- `--keep-footer-links`: Don't remove footer links
- `--verbose, -v`: Increase logging verbosity

### `cleanup_footer_links.py`
Utility script to remove footer links from an already-crawled JSON file.

**Purpose:**
Remove the last 5 links from each subcontent entry's `links` array. These are typically footer links that appear on every page (e.g., "Contact Us", "Privacy Policy", etc.).

**Usage:**
```bash
# Create a new cleaned file
python3 cleanup_footer_links.py \
  --input hi_careers_pages_cleaned_with_links.json \
  --output hi_careers_pages_final.json

# Clean in-place
python3 cleanup_footer_links.py --in-place

# Remove a different number of footer links
python3 cleanup_footer_links.py --num-footer-links 3 --in-place
```

**Options:**
- `--input, -i`: Input JSON file (default: hi_careers_pages_cleaned_with_links.json)
- `--output, -o`: Output JSON file (default: adds _cleaned suffix)
- `--in-place`: Overwrite input file
- `--num-footer-links`: Number of footer links to remove (default: 5)

## Workflow

### Initial Crawl
```bash
# 1. Crawl subcontent pages and extract links (footer links removed automatically)
python3 crawl_links.py \
  --input hi_careers_pages_cleaned.json \
  --output hi_careers_pages_with_links.json \
  -v
```

### If You Already Have Links (Cleanup Existing Data)
```bash
# Remove footer links from existing crawled data
python3 cleanup_footer_links.py \
  --input hi_careers_pages_with_links.json \
  --in-place
```

## Data Structure

**Input structure:**
```json
[
  {
    "url": "https://example.com/page.html",
    "title": "Page Title",
    "text": "Page content...",
    "links": [],
    "subcontent": [
      {
        "url": "https://example.com/subpage.html",
        "title": "Subpage Title",
        "text": "Subpage content...",
        "links": [],
        "subcontent": []
      }
    ]
  }
]
```

**After crawling:**
- Top-level `links` remain empty
- Each subcontent entry's `links` array is populated with extracted URLs
- Footer links (last 5) are automatically removed

## Notes

- The crawler uses Python's built-in `HTMLParser` (no external HTML parsing dependencies)
- Requires `requests` library for HTTP requests
- Only http/https links are collected
- URL fragments (#anchor) are removed to avoid duplicates
- Relative URLs are resolved to absolute URLs
- Duplicate links within each page are removed
