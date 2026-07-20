import json
import requests
from bs4 import BeautifulSoup, Tag

URL = "https://www.hdfc.bank.in/education-loan"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

print("Status:", response.status_code)

with open("indian_education.html", "w", encoding="utf-8") as f:
    f.write(response.text)

soup = BeautifulSoup(response.text, "lxml")

sections = []

headings = soup.find_all(["h1", "h2", "h3", "h4"])


def clean(text):
    return " ".join(text.split())


for heading in headings:

    title = clean(heading.get_text(" ", strip=True))

    if not title:
        continue

    content = []

    # Traverse through all elements after heading
    for elem in heading.next_elements:

        if elem == heading:
            continue

        if isinstance(elem, Tag):

            # Stop when next heading is reached
            if elem.name in ["h1", "h2", "h3", "h4"]:

                if elem != heading:
                    break

            # Paragraphs
            elif elem.name == "p":

                text = clean(elem.get_text(" ", strip=True))

                if text and text not in content:
                    content.append(text)

            # Lists
            elif elem.name == "li":

                text = clean(elem.get_text(" ", strip=True))

                if text and text not in content:
                    content.append(text)

            # Table rows
            elif elem.name == "tr":

                row = [
                    clean(td.get_text(" ", strip=True))
                    for td in elem.find_all(["td", "th"])
                ]

                if row:
                    text = " | ".join(row)

                    if text not in content:
                        content.append(text)

            # Accordion/Card Labels
            elif elem.name in ["span", "strong", "b"]:

                text = clean(elem.get_text(" ", strip=True))

                if (
                    len(text) > 2
                    and len(text) < 120
                    and text not in content
                ):
                    content.append(text)

    sections.append(
        {
            "heading": title,
            "content": content,
        }
    )


output = {
    "bank": "HDFC Bank",
    "loan_scheme": "Education Loan for Indian Education",
    "url": URL,
    "sections": sections,
}

with open(
    "Data/raw/hdfc_indian_education.json",
    "w",
    encoding="utf-8",
) as f:

    json.dump(output, f, indent=4, ensure_ascii=False)

print("Saved to Data/raw/hdfc_indian_education.json")

print("\nPreview\n")

for sec in sections:

    print("=" * 70)
    print(sec["heading"])

    for item in sec["content"][:8]:
        print("-", item)