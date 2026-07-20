import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL = "https://indianbank.bank.in/en/pm-vidyalaxmi-scheme"


def clean(text):
    return " ".join(text.split())


# -----------------------------
# Download page using Playwright
# -----------------------------
with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(URL, wait_until="networkidle")

    html = page.content()

    browser.close()


# Save HTML
with open("pm_vidyalaxmi.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML Saved")


# -----------------------------
# Parse HTML
# -----------------------------
soup = BeautifulSoup(html, "lxml")

sections = []


# -----------------------------
# Find Main Content
# -----------------------------
container = soup.select_one("div.contentDetail")

if container is None:
    raise Exception("Could not find main content.")


# -----------------------------
# Heading
# -----------------------------
heading = container.find(["h1", "h2", "h3"])

if heading:
    title = clean(heading.get_text())
else:
    title = "PM – Vidyalaxmi Scheme"

content = []


# -----------------------------
# Paragraphs
# -----------------------------
for p in container.find_all("p"):

    text = clean(p.get_text(" ", strip=True))

    if text and text not in content:
        content.append(text)


# -----------------------------
# Tables
# -----------------------------
tables = container.find_all("table")

print("Tables Found:", len(tables))

for table in tables:

    rows = table.find_all("tr")

    print("Rows:", len(rows))

    for row in rows:

        cols = row.find_all(["td", "th"])

        cols = [
            clean(col.get_text(" ", strip=True))
            for col in cols
        ]

        cols = [c for c in cols if c]

        # Skip empty rows
        if len(cols) < 2:
            continue

        # Skip table header
        if "Parameters" in cols[0]:
            continue

        if len(cols) >= 3:

            parameter = cols[1]

            details = " ".join(cols[2:])

        else:

            parameter = cols[0]

            details = cols[1]

        text = f"{parameter} | {details}"

        if text not in content:
            content.append(text)


# -----------------------------
# Bullet Lists
# -----------------------------
for li in container.find_all("li"):

    text = clean(li.get_text(" ", strip=True))

    if text and text not in content:
        content.append(text)


# -----------------------------
# Links
# -----------------------------
for a in container.find_all("a"):

    text = clean(a.get_text())

    href = a.get("href")

    if not text:
        continue

    if href:

        if href.startswith("/"):
            href = "https://indianbank.bank.in" + href

        item = f"{text} | {href}"

    else:
        item = text

    if item not in content:
        content.append(item)


# -----------------------------
# Output
# -----------------------------
sections.append(
    {
        "heading": title,
        "content": content
    }
)

output = {
    "bank": "Indian Bank",
    "loan_scheme": "PM – Vidyalaxmi Scheme",
    "url": URL,
    "sections": sections
}


with open(
    "Data/raw/indian_pm_vidyalaxmi.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(output, f, indent=4, ensure_ascii=False)


print("\nSaved to Data/raw/indian_pm_vidyalaxmi.json")


# -----------------------------
# Preview
# -----------------------------
print("\nPreview\n")

for sec in sections:

    print("=" * 70)
    print(sec["heading"])

    for item in sec["content"][:20]:
        print("-", item)