import json
import re

def clean_text(text):
    # Remove repeating "Home ... Home" sections (menu bar duplicates)
    cleaned = re.sub(r'Home.*?Home', 'Home', text, flags=re.DOTALL)
    # Remove redundant menu items repeated at the top
    cleaned = re.sub(r'(Pathways & Programs.*?Resources Contact Us)', '', cleaned, flags=re.DOTALL)
    # Collapse whitespace
    return re.sub(r'\s+', ' ', cleaned).strip()

with open("hi_careers_pages.json", "r") as f:
    data = json.load(f)

for page in data:
    page["text"] = clean_text(page["text"])
    print(type(page["subcontent"]))
    if isinstance(page["subcontent"], list):
        for sub in page["subcontent"]:
            if sub:
                sub["text"] = clean_text(sub["text"])
    else: print(page["subcontent"])

with open("hi_careers_pages_cleaned.json", "w") as f:
    json.dump(data, f, indent=2)