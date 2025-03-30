import sys
import json
import os
import fitz  # PyMuPDF for extracting links
import pdfplumber
import requests
import yaml
import re

CONFIG_PATH = "config.yaml"

EXTRACTION_TEMPLATE = """Extract the following ATS fields as JSON:
{
  "name": "Full name",
  "email": "Email address",
  "linkedin": "LinkedIn profile URL",
  "phone": "Phone number",
  "github": "GitHub profile URL",
  "behance": "Behance profile URL",
  "skills": ["list", "of", "skills"],
  "experience": ["Position details"],
  "education": ["Degree details"]
}"""

def load_api_key():
    try:
        with open(CONFIG_PATH) as file:
            data = yaml.safe_load(file)
            api_key = data.get('OPENROUTER_API_KEY') or data.get('openrouter')
            if not api_key:
                raise ValueError("Missing API key in config.yaml")
            return api_key
    except Exception as e:
        print(json.dumps({"error": f"Config error: {str(e)}"}))
        sys.exit(1)

def extract_text(file_path):
    text = ""

    if not os.path.exists(file_path):
        print(json.dumps({"error": "File not found"}))
        sys.exit(1)

    try:
        if file_path.endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text + "\n"

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    return text.strip()

def extract_links(file_path):
    github_links = []
    linkedin_links = []
    
    try:
        doc = fitz.open(file_path)
        for page in doc:
            links = page.get_links()
            for link in links:
                url = link.get("uri", "")
                if "github.com" in url:
                    github_links.append(url)
                elif "linkedin.com/in" in url or "linkedin.com/" in url:
                    linkedin_links.append(url)
    
    except Exception as e:
        print(json.dumps({"error": f"Failed to extract links: {str(e)}"}))
    
    return github_links, linkedin_links

def get_github_profile(github_links):
    """Filters GitHub profile link by removing project links."""
    for link in github_links:
        match = re.match(r"https?://github\.com/([^/]+)$", link)
        if match:
            return link  # Return first valid profile link
    return None  # No valid GitHub profile found

def ats_extractor(resume_data):
    try:
        api_key = load_api_key()

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "YOUR_SITE_URL",
                "X-Title": "ATS Parser"
            },
            json={
                "model": "openai/gpt-4",
                "messages": [
                    {"role": "system", "content": "You are an ATS parser. Return ONLY valid JSON. Do not include explanations."},
                    {"role": "user", "content": f"{EXTRACTION_TEMPLATE}\n\nResume data:\n{resume_data}"}
                ],
                "temperature": 0.1,
                "max_tokens": 2000
            },
            timeout=20
        )

        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        cleaned = content.strip().replace('```json', '').replace('```', '')
        
        return json.loads(cleaned)

    except json.JSONDecodeError:
        return {"error": "API returned invalid JSON"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Processing failed: {str(e)}"}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No file provided"}))
        sys.exit(1)

    file_path = sys.argv[1]
    extracted_text = extract_text(file_path)
    github_links, linkedin_links = extract_links(file_path)
    
    github_profile = get_github_profile(github_links)
    
    if not extracted_text:
        print(json.dumps({"error": "No text extracted"}))
        sys.exit(1)

    parsed_data = ats_extractor(extracted_text)

    # Inject extracted GitHub and LinkedIn links into the parsed data
    parsed_data["github"] = github_profile or "Not found"
    parsed_data["linkedin"] = linkedin_links[0] if linkedin_links else "Not found"

    print(json.dumps(parsed_data, indent=2))
