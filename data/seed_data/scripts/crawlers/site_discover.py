import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import json
import time
from typing import List

# optional import helper for Playwright-based slide rendering
# try:
from slides_extractor import extract_links_from_slides
# except Exception:
#     # slides_extractor is optional; we'll fall back to static iframe fetch when not available
#     extract_links_from_slides = None

def discover_links(start_url, max_depth=3, max_pages=100):
    # Only process the start_url, do not crawl further
    def normalize_url(u):
        p = urlparse(u)
        p = p._replace(fragment="")
        netloc = p.netloc.lower()
        if netloc.endswith(':80') and p.scheme == 'http':
            netloc = netloc[:-3]
        if netloc.endswith(':443') and p.scheme == 'https':
            netloc = netloc[:-4]
        path = p.path or ''
        if path.endswith('/') and path != '/':
            path = path.rstrip('/')
        p = p._replace(netloc=netloc, path=path)
        return urlunparse(p)

    url = normalize_url(start_url)
    domain = urlparse(url).netloc
    discovered = []
    visited = set()
    visited.add(url)
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200 or "text/html" not in r.headers.get("content-type", ""):
            return discovered
        # print(f"[1] {url}")
        soup = BeautifulSoup(r.text, "html.parser")

        # Only extract links from Google Slides embeds
        for iframe in soup.find_all("iframe", src=True):
            src = iframe["src"]
            # print(src)
            if "docs.google.com/presentation" not in src:
                continue

            extracted: List[str] = []
            if extract_links_from_slides:
                try:
                    extracted = extract_links_from_slides(src)
                except Exception as e:
                    print(f"Playwright extractor failed: {e}")

            if not extracted:
                print('not extracted')
                try:
                    r2 = requests.get(src, timeout=10)
                    if r2.status_code == 200 and "text/html" in r2.headers.get("content-type", ""):
                        soup2 = BeautifulSoup(r2.text, "html.parser")
                        extracted = [a.get("href") for a in soup2.find_all("a", href=True)]
                except Exception as e:
                    print(f"Error fetching iframe src: {e}")

            for href in extracted:
                if not href:
                    continue
                full = urljoin(url, href)
                full = normalize_url(full)
                # Only add if not a root-level link (not in program_links)
                if urlparse(full).netloc == domain and full not in visited:
                    discovered.append({"url": full, "depth": 1})
                    visited.add(full)
        time.sleep(0.5)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    print(f"Discovered {len(discovered)} links from {url}")
    return discovered

if __name__ == "__main__":
    program_links = [
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/AFNRM/afnrm.html",
      "depth": 0
    },
    {
      "url": "https://hawaiicareerpathways.org/index.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathwaysandprograms.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/AFNRM/animalsystems.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/AFNRM/foodsystems.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/AFNRM/agandfoodproduction.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/AFNRM/naturalresourcesmanagement.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/architecture_engineering/arch_eng.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/architecture_engineering/architecture.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/architecture_engineering/engineering.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/buildingandconstruction/building_construction.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/buildingandconstruction/mechanical_electrical_plumbing.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/buildingandconstruction/residential_commercial_construction.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/creativemedia/cultureartsmediaentertainment.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/creativemedia/digitaldesign.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/creativemedia/fashionandartisan.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/creativemedia/filmandmedia.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/education/education.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/education/learningsupportprofession.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/education/teachingasaprofession.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/health/healthservices.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/health/publichealth.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/health/diagnosticsvcs.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/health/ems.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/health/hpts.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/health/nursing.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/hospitality_tourism/hosp_tourism_recreation.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/hospitality_tourism/culinaryarts.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/hospitality_tourism/shtm.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/IT/infotechanddigitaltransformation.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/IT/artificialintelligence.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/IT/programming.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/IT/networking.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/IT/cybersecurity.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/IT/webdev.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/transportation/transportation.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/transportation/automaintenancerepair.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/transportation/autocollisionrepair.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/transportation/aviationmaintenancetech.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/pathways/programs/transportation/marinemaintenancetech.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/resources.html",
      "depth": 1
    },
    {
      "url": "https://hawaiicareerpathways.org/contactus.html",
      "depth": 1
    }
  ]
    program_directory = {}

    for link in program_links:
        print(f"\n🔍 Discovering links from: {link['url']}")
        sitemap = discover_links(link['url'], max_depth=3, max_pages=50)
        program_directory[link['url']] = sitemap

    with open("site_sitemap.json", "w") as f:
        json.dump(program_directory, f, indent=2)
    print(f"\n✅ Discovered {len(program_directory)} pages. Saved to site_sitemap.json")
