import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.hdfc.bank.in/education-loan/foreign-education"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "lxml")

# Remove unwanted sections
for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
    tag.decompose()

sections = []

current_section = None

for tag in soup.find_all(["h1", "h2", "h3", "h4", "p", "ul"]):

    # New section
    if tag.name in ["h1", "h2", "h3", "h4"]:

        heading = tag.get_text(" ", strip=True)

        if len(heading) < 2:
            continue

        current_section = {
            "heading": heading,
            "content": []
        }

        sections.append(current_section)

    # Paragraph
    elif tag.name == "p":

        text = tag.get_text(" ", strip=True)

        if current_section and text:
            current_section["content"].append(text)

    # List
    elif tag.name == "ul":

        items = []

        for li in tag.find_all("li", recursive=False):

            txt = li.get_text(" ", strip=True)

            if txt:
                items.append(txt)

        if current_section and items:
            current_section["content"].extend(items)

# Save JSON
output = {
    "bank": "HDFC Bank",
    "loan_scheme": "Foreign Education Loan",
    "url": URL,
    "sections": sections
}

with open("hdfc_foreign_education.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print("Saved to hdfc_foreign_education.json")

# Preview
for section in sections:
    print("=" * 60)
    print(section["heading"])
    for item in section["content"]:
        print("-", item)