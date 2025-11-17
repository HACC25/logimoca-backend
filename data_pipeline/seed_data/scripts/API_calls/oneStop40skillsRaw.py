import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# --- 1. Your API Credentials ---
# (Get these from CareerOneStop)
USER_ID = os.getenv("ONESTOP_USERID")
API_KEY = os.getenv("ONESTOP_API_KEY")
API_BASE_URL = "https://api.careeronestop.org/v1/skillsmatcher"

# --- 2. Build and Send the API Request ---

# This is the endpoint that returns the 40 standard skills
api_url = f"{API_BASE_URL}/{USER_ID}"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Note: This is a GET request, so no payload is needed.
try:
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()  # Check for any request errors

    # --- 3. Process the Results ---
    skill_data = response.json()

    if "Skills" in skill_data:
        print(f"--- Successfully fetched {len(skill_data['Skills'])} standard skills ---")
        
        # This list is what you will save and use for mapping
        skill_list = skill_data['Skills']

        # Save 'skill_list' to your database or a local JSON file
        # to build your user interface and skill-mapping logic.
        with open("oneStop40Skills.json", "w") as f:
            json.dump(skill_list, f, indent=4)
        print("Saved skills to 'oneStop40Skills.json'.")

    else:
        print("Could not find 'Skills' in the API response.")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response content: {response.text}")
except Exception as err:
    print(f"An error occurred: {err}")