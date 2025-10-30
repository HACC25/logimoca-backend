import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import time
import pathlib

JSON_OUTPUT_PATH = pathlib.Path(__file__).parent / "hi_careers_sitemap.json"
PAGES_JSON = pathlib.Path(__file__).parent / "hi_careers_pages.json"

def extract_page_data(url):
    """Extract title, text content, and internal links from a single page."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")

        # Get title
        title = soup.title.string.strip() if soup.title else ""

        # Extract visible text
        for script in soup(["script", "style", "noscript"]):
            script.decompose()
        text = " ".join(soup.stripped_strings)

        # Find internal links
        base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        links = [
            urljoin(base, a.get("href"))
            for a in soup.find_all("a", href=True)
            if a.get("href").startswith("/") or a.get("href").startswith(base)
        ]
        links = list(set(links))  # Deduplicate

        return {"url": url, "title": title, "text": text, "links": links, "subcontent": []}

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def crawl_site(start_url, max_pages=10):
    """Recursively crawl up to `max_pages` pages within the same domain."""
    visited = set()
    to_visit = [start_url]
    pages = []

    domain = urlparse(start_url).netloc

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        page_data = extract_page_data(url)
        if not page_data:
            continue
        visited.add(url)
        pages.append(page_data)

        # Add internal links
        for link in page_data["links"]:
            if urlparse(link).netloc == domain and link not in visited:
                to_visit.append(link)

        time.sleep(1)  # Be polite to the server

    return pages

def get_pages_from_json(file_path):

    """Load hi careers sitemap JSON file."""
    site_map = {}
    pages = []
    with open(file_path, "r") as f:
        site_map = json.load(f)

    for url in site_map:
        pages.append(extract_page_data(url))
        for page in site_map[url]:
            pages[-1]["subcontent"].append(extract_page_data(page['url']))

    # create a file and write the pages to it
    with open("hi_careers_pages.json", "w") as f:
        json.dump(pages, f, indent=2)
                          
    return pages


def build_knowledge_graph(file):
    """Create a simple JSON knowledge graph from crawled pages."""
    nodes = []
    edges = []
    url_to_node = {}

    pages = []
    with open(file, "r") as f:
        pages = json.load(f)

    # Add root pages and their subcontent as nodes, and create subcontent edges
    for page in pages:
        snippet = page["text"][:300].replace("\n", " ").strip() if page.get("text") else ""
        node = {
            "id": page["url"],
            "title": page.get("title", ""),
            "summary": snippet
        }
        nodes.append(node)
        url_to_node[page["url"]] = node

        # Add subcontent nodes and edges
        for sub in page.get("subcontent", []):
            if not sub or not sub.get("url"):  # skip empty or malformed
                continue
            sub_snippet = sub["text"][:300].replace("\n", " ").strip() if sub.get("text") else ""
            sub_node = {
                "id": sub["url"],
                "title": sub.get("title", ""),
                "summary": sub_snippet
            }
            nodes.append(sub_node)
            url_to_node[sub["url"]] = sub_node
            edges.append({
                "source": page["url"],
                "target": sub["url"],
                "relation": "has_subcontent"
            })

    # Add links_to edges for all nodes (including subcontent)
    all_pages = pages + [sub for page in pages for sub in page.get("subcontent", []) if sub and sub.get("url")]
    for page in all_pages:
        if not page or not page.get("url"):
            continue
        for link in page.get("links", []):
            if link in url_to_node:
                edges.append({
                    "source": page["url"],
                    "target": link,
                    "relation": "links_to"
                })

    return {"nodes": nodes, "edges": edges}


def scrape_site_to_json(start_url, max_pages=10, output_file="site_kg.json"):
    """High-level pipeline: crawl site → build graph → save JSON."""
    pages = crawl_site(start_url, max_pages=max_pages)
    graph = build_knowledge_graph(pages)
    with open(output_file, "w") as f:
        json.dump(graph, f, indent=2)
    print(f"Knowledge graph saved to {output_file}")
    return graph


if __name__ == "__main__":
    knowledge_graph = build_knowledge_graph(PAGES_JSON)
    with open("./hi_careers_knowledge_graph.json", "w") as f:
        json.dump(knowledge_graph, f, indent=2)
    print("Knowledge graph saved to hi_careers_knowledge_graph.json")
