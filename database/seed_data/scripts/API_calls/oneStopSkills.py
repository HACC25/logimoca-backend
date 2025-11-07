import requests
import urllib.parse
import json
from dotenv import load_dotenv
import os
import ska_values

# Load environment variables from .env file


# --- 1. Your API Credentials ---
# (Get these from CareerOneStop)
API_BASE_URL = "https://api.careeronestop.org/v1/skillsmatcher"


# --- 2. Your User's Skill Data ---
# This is the crucial step. You must map your LLM's JSON skills 
# to the 40 standard skills from the CareerOneStop 'Get Skills' endpoint.
#
# For this example, let's say your user rated these skills highly (5) 
# and all others as zero (0).
#
# '2.A.2.f' = Critical Thinking
# '2.A.4.a' = Programming
# '2.C.3.b' = Active Listening
# '4.A.1.a.1' = Mathematics
#
# The API expects a single string of 40 ratings, separated by '|'.
# The order is defined by the 'Get Skills' endpoint.
#
# Let's pretend for this example of 40 skills, our 4 skills are
# at positions 1, 5, 10, and 20. All others are 0.
# skill_ratings = [0] * 40
# skill_ratings[0] = 5  # Critical Thinking
# skill_ratings[4] = 5  # Programming
# skill_ratings[9] = 5  # Active Listening
# skill_ratings[19] = 5 # Mathematics

# # Convert the list of 40 ratings into the required pipe-delimited string
# skill_string = "|".join(map(str, skill_ratings))

# --- 3. Build and Send the API Request ---

def get_skills_matched_occupations(user_id, api_token, ska_values,
                   sort_column="",
                   sort_order="",
                   edu_filter_value=""):
    
    # build query string params
    qs = {}
    if sort_column or sort_order or edu_filter_value:
        qs = {
            "sortColumn": sort_column,
            "sortOrder": sort_order,
            "eduFilterValue": edu_filter_value
        }
    full_url = f"{API_BASE_URL}/{user_id}"

    if qs:
        full_url = f"{full_url}?{urllib.parse.urlencode(qs)}"

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # convert payload to JSON
    json_payload = json.dumps(ska_values)

    response = requests.post(full_url, headers=headers, data=json_payload)

    if response.ok:
        result = response.text
        return result
    else:
        response.raise_for_status()

# testing & use example
if __name__ == "__main__":
    load_dotenv()
    USER_ID = os.getenv("ONESTOP_USERID")
    API_KEY = os.getenv("ONESTOP_API_KEY")
    ska_values = ska_values.ska_values
    try:
        resp = get_skills_matched_occupations(USER_ID, API_KEY, ska_values)
        print(f"Success: {len(json.loads(resp)['SKARankList'])} results found.")
    except Exception as e:
        print("Error:", e)
