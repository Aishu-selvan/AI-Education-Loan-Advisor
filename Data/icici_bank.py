import json
import requests
from bs4 import BeautifulSoup

URL = "https://www.icici.bank.in/personal-banking/loans/education-loan"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

print("Status:", response.status_code)

with open("icici_education.html", "w", encoding="utf-8") as f:
    f.write(response.text)

soup = BeautifulSoup(response.text, "lxml")


def clean(text):
    return " ".join(text.split())


sections = []

# Collect all headings
all_headings = soup.find_all(["h1", "h2", "h3", "h4"])


for i, heading in enumerate(all_headings):

    title = clean(heading.get_text(" ", strip=True))

    # Ignore navigation
    if title in [
        "",
        "Skip to main content",
        "Personal",
        "Accounts",
        "Cards",
        "Loans",
        "Deposits",
        "Payments",
        "Insurance",
        "Investments",
        "Explore",
        "Other",
        "Ways to Bank",
        "Investor Center",
        "Customer Service",
        "Blogs"
    ]:
        continue

    content = []

    # Stop at next heading
    next_heading = all_headings[i + 1] if i + 1 < len(all_headings) else None

    node = heading

    while True:

        node = node.find_next()

        if node is None:
            break

        if next_heading and node == next_heading:
            break

        text = clean(node.get_text(" ", strip=True))

        if (
            text
            and len(text) > 2
            and text not in content
            and text != title
        ):
            content.append(text)

    if content:

        sections.append(
            {
                "heading": title,
                "content": content
            }
        )


output = {
    "bank": "ICICI Bank",
    "loan_scheme": "Education Loan",
    "url": URL,
    "sections": sections
}

with open(
    "Data/raw/icici_education.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print("Saved to Data/raw/icici_education.json")

print("\nPreview\n")

for sec in sections:
    print("=" * 70)
    print(sec["heading"])
    for item in sec["content"][:8]:
        print("-", item)