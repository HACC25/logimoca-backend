import json
import re
import os

# Input file: Scraped and cleaned JSON data from Hawaii Career Pathways
# Each entry has 'url', 'title', 'text', and 'subcontent' (list of dicts)

root_dir = os.path.dirname(os.path.abspath(__file__))

# Load the scraped data
file_path = os.path.join(root_dir, "hi_careers_pages_cleaned_with_links.json")
with open(file_path, 'r') as f:
    data = json.load(f)

# 1. Define the Canonical Sectors and their URL code mapping
# These are the 9 umbrella career pathways from Hawaii Career Pathways.
SECTOR_MAP = {
    "AFNRM": {
        "name": "Agriculture, Food, and Natural Resources", 
        "id": "AFNRM",
        "sector_page": "https://hawaiicareerpathways.org/pathways/programs/AFNRM/afnrm.html"
    },
    "architecture_engineering": {
        "name": "Architectural Design and Engineering Technology", 
        "id": "ADET",
        "sector_page": "https://hawaiicareerpathways.org/pathways/programs/architecture_engineering/arch_eng.html"
    },
    "buildingandconstruction": {
        "name": "Building and Construction", 
        "id": "BC",
        "sector_page": "https://hawaiicareerpathways.org/pathways/programs/buildingandconstruction/building_construction.html"
    },
    "creativemedia": {
        "name": "Culture Arts, Media, and Entertainment", 
        "id": "CAME",
        "sector_page": "https://hawaiicareerpathways.org/pathways/programs/creativemedia/cultureartsmediaentertainment.html"
    },
    "education": {
        "name": "Education", 
        "id": "ED",
        "sector_page": "https://hawaiicareerpathways.org/pathways/programs/education/education.html"
    },
    "health": {
        "name": "Health Services", 
        "id": "HS",
        "sector_page": "https://hawaiicareerpathways.org/pathways/programs/health/healthservices.html"
    },
    "hospitality_tourism": {
        "name": "Hospitality, Tourism, and Recreation", 
        "id": "HTR",
        "sector_page": "https://hawaiicareerpathways.org/pathways/programs/hospitality_tourism/hosp_tourism_recreation.html"
    },
    "IT": {
        "name": "Information Technology and Digital Transformation", 
        "id": "IT",
        "sector_page": "https://hawaiicareerpathways.org/pathways/programs/IT/infotechanddigitaltransformation.html"
    },
    "transportation": {
        "name": "Transportation Services", 
        "id": "TS",
        "sector_page": "https://hawaiicareerpathways.org/pathways/programs/transportation/transportation.html"
    },
}

# Invert the map for easier lookup by name later, and create the structure
structured_data = {
    sector_code: {
        "sector_name": entity["name"],
        "pathway_url": entity["sector_page"],  # URL for sector landing page
        "pathways": [],  # List of pathway objects; each contains programs
        "id": entity["id"],
    }
    for sector_code, entity in SECTOR_MAP.items()
}

# 2. Helpers to extract the sector key from the URL
def extract_sector_key(url: str) -> str | None:
    """Return the sector key as used in SECTOR_MAP/structured_data.

    Supports both uppercase short codes (e.g., AFNRM, IT) and slug folders
    (e.g., architecture_engineering, education, transportation).
    """
    if not url:
        return None
    m = re.search(r"/pathways/programs/([^/]+)/", url)
    if not m:
        return None
    segment = m.group(1)

    # direct match (e.g., 'architecture_engineering')
    if segment in structured_data:
        return segment
    # uppercase code match (e.g., 'AFNRM', 'IT')
    upper = segment.upper()
    if upper in structured_data:
        return upper
    return None

def extract_filename_id(url: str) -> str:
    """Extract a safe id base from the last path component of a URL.

    Example: '.../agandfoodproduction.html' -> 'agandfoodproduction'
    Falls back to a sanitized placeholder if no match.
    """
    if not url:
        return "unknown"
    m = re.search(r"([A-Za-z0-9_-]+)\.html$", url)
    if m:
        return m.group(1)
    # fallback: strip trailing slash and take last segment
    tail = url.rstrip('/').split('/')[-1]
    return re.sub(r"[^A-Za-z0-9_-]", "_", tail or "unknown")


def normalize_name(raw_title: str | None) -> str:
    """Normalize a page title to a concise pathway/program name.

    - Drops the site suffix after ' | ' if present
    - Removes trailing phrases like 'Pathway', 'Pathways', 'Pathway Map to Employment'
    """
    t = (raw_title or "").strip()
    # Remove site branding or anything after first ' | '
    if " | " in t:
        t = t.split(" | ", 1)[0].strip()
    # Remove common trailing phrases
    t = re.sub(r"\s*(Pathway Map to Employment)$", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s*(Pathway|Pathways)$", "", t, flags=re.IGNORECASE)
    return t.strip()

# 3. Processing Logic
for item in data:
    if not isinstance(item, dict):
        continue
    url = item.get('url')
    if not url:
        continue

    sector_key = extract_sector_key(url)
    if not sector_key or sector_key not in structured_data:
        # Skip entries that don't map to a known sector
        continue

    sector_entry = structured_data[sector_key]

    # Determine the pathway info from this top-level item
    raw_title = item.get('title') or ''
    pathway_name = normalize_name(raw_title) or 'N/A'
    pathway_description = item.get('text') or ''
    pathway_url = url

    # Use filename for id base when available
    pathway_id_base = extract_filename_id(pathway_url)

    # A. Treat this top-level page as a pathway, unless it is the sector landing page
    # Treat the configured sector landing page as not-a-pathway
    is_sector_landing_page = (pathway_url == sector_entry["pathway_url"])  # robust across slug vs code pages

    pathway_obj = None
    if not is_sector_landing_page:
        pathway_obj = {
            "id": f"{sector_key}-{pathway_id_base}",
            "sector_id": sector_key,
            "name": pathway_name,
            "description": pathway_description,
            "pathway_url": pathway_url,
            "programs": [],
            "source": "Top-Level Page",
        }
        if not any(p.get('id') == pathway_obj['id'] for p in sector_entry['pathways']):
            sector_entry['pathways'].append(pathway_obj)
        else:
            # retrieve existing to append programs
            for p in sector_entry['pathways']:
                if p.get('id') == pathway_obj['id']:
                    pathway_obj = p
                    break

    # B. Process 'subcontent' as individual programs under this pathway
    # Only attach programs if we created/identified a pathway for this entry.
    if pathway_obj is not None:
        for sub_item in item.get('subcontent', []) or []:
            if not isinstance(sub_item, dict):
                continue

            sub_program_name = normalize_name(sub_item.get('title')) or 'N/A'
            sub_program_description = sub_item.get('text') or 'No description.'
            sub_program_url = sub_item.get('url') or pathway_url

            sub_program_id = extract_filename_id(sub_program_url)
            sub_links = sub_item.get('links') or []

            program_data = {
                "id": f"{sector_key}-SUB-{sub_program_id}",
                "sector_id": sector_key,
                "name": sub_program_name,
                "description": sub_program_description,
                "program_url": sub_program_url,
                "source": "Subcontent",
                "program_links": sub_links,
            }
            if not any(p.get('id') == program_data['id'] for p in pathway_obj['programs']):
                pathway_obj['programs'].append(program_data)


# Convert the dictionary of sectors back into a list and save
final_output = list(structured_data.values())

# Save the structured data
output_file_path = "structured_career_pathways.json"
with open(output_file_path, 'w') as f:
    json.dump(final_output, f, indent=2)

print(f"\nSuccessfully processed and saved structured data to: {output_file_path}")
print("\n--- Example of Structured Output (First Sector and its Pathways/Programs) ---")

# Print a formatted snippet of the first sector's data
example_output = final_output[0]
print(f"Sector Name: {example_output['sector_name']} ({list(SECTOR_MAP.keys())[0]})")
print(f"Total Pathways: {len(example_output['pathways'])}")
print("\nExample Pathways and first program:")
for i, pathway in enumerate(example_output['pathways'][:3]):
    print(f"  {i+1}. Pathway ID: {pathway['id']}")
    print(f"     Name: {pathway['name'][:60]}...")
    print(f"     URL: {pathway['pathway_url']}")
    if pathway.get('programs'):
        p = pathway['programs'][0]
        print(f"       ↳ First Program: {p['name'][:60]}... ({p['program_url']})")

# Provide the file to the user
print(f"\nFile available: {output_file_path}")