"""Render Google Slides embeds with Playwright and extract link targets.

This module is optional — Playwright is only required if you want to render
JS-driven embeds. If Playwright is not installed, callers should handle ImportError.

Usage:
  from slides_extractor import extract_links_from_slides
  links = extract_links_from_slides(embed_url)
"""
from typing import List

def extract_links_from_slides(embed_url: str, timeout: int = 30, headless: bool = True) -> List[str]:
    """Render the embed URL and return a list of href strings found in the rendered DOM.

    This function uses Playwright (sync API). It will raise ImportError if Playwright
    isn't installed. It will also raise other exceptions from Playwright if the browser
    cannot be launched.
    """
    # Import inside function so callers that don't need Playwright won't fail on import
    from playwright.sync_api import sync_playwright


    import re
    import urllib.parse

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        try:
            page = browser.new_page()
            page.goto(embed_url, wait_until="networkidle", timeout=timeout * 1000)
            page.wait_for_timeout(1000)

            # Inspect all frames for anchor hrefs (keep this for completeness)
            frames = page.frames
            for frame in frames:
                try:
                    anchors = frame.query_selector_all("a[href]")
                    for a in anchors:
                        href = a.get_attribute("href")
                        if href:
                            results.append(href)
                except Exception:
                    continue

            # --- NEW: Extract Google redirect URLs from the full HTML/text ---
            html = page.content()
            # print("HTML:\n", html)
            # Find all google redirect URLs (unicode-escaped or not)
            # Handles both \\u003d and =, \\u0026 and &
            # Regex for both escaped and unescaped
            pattern = re.compile(r'https://www\.google\.com/url\?q(?:\\u003d|=)(https://[\w\-./%]+)(?:\\u0026|&)', re.IGNORECASE)
            matches = pattern.findall(html)
            # Also try to decode unicode escapes in the HTML and search again
            def decode_unicode_escapes(s):
                return s.encode('utf-8').decode('unicode_escape')
            html_decoded = decode_unicode_escapes(html)
            matches += pattern.findall(html_decoded)

            # Add all found google redirect targets
            for m in matches:
                # Unquote in case it's url-encoded
                real_url = urllib.parse.unquote(m)
                results.append(real_url)

        finally:
            browser.close()

    # De-duplicate preserving order
    seen = set()
    ordered = []
    for r in results:
        if r not in seen:
            seen.add(r)
            ordered.append(r)
    return ordered
