import json
import re
from datetime import date

# -----------------------------
# Helper Functions
# -----------------------------

def clean(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = text.rstrip(".")
    return text

def unique(seq):
    seen = set()
    out = []
    for item in seq:
        item = clean(item)
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out

# -----------------------------
# Load JSON
# -----------------------------

with open("Data/raw/hdfc_foreign_education.json", encoding="utf-8") as f:
    raw = json.load(f)

# Merge duplicate headings
sections = {}

for sec in raw["sections"]:
    heading = clean(sec["heading"]).lower()

    if heading not in sections:
        sections[heading] = []

    sections[heading].extend(sec["content"])

# -----------------------------
# Output Schema
# -----------------------------

normalized = {
    "bank": raw["bank"],
    "loan_name": raw["loan_scheme"],
    "category": "Education Loan",
    "sub_category": "Foreign Education",

    "loan_amount": {},

    "interest_rate": {},

    "loan_tenure": "",

    "collateral": [],

    "moratorium": "",

    "eligibility": [],

    "documents": {
        "identity": [],
        "address": [],
        "academic": []
    },

    "fees": {},

    "benefits": [],

    "covered_courses": [],

    "expenses_covered": [],

    "application_process": [],

    "faq": [],

    "source_url": raw["url"],

    "last_updated": str(date.today())
}

# -----------------------------
# Loan Details
# -----------------------------

for item in sections.get("loan details", []):

    t = item.lower()

    if "75 lakh" in t:
        normalized["loan_amount"]["unsecured"] = "₹75 lakh"

    if "no limit" in t:
        normalized["loan_amount"]["secured"] = "No upper limit"

    if "14 years" in t:
        normalized["loan_tenure"] = "14 years"

    if "cblr" in t:
        normalized["interest_rate"] = {
            "type": "Floating",
            "formula": "CBLR + Spread"
        }

# -----------------------------
# Collateral
# -----------------------------

for item in sections.get("collateral & moratorium", []):

    t = item.lower()

    if "fixed deposit" in t:
        normalized["collateral"].append("Fixed Deposit")

    if "house" in t:
        normalized["collateral"].append("House")

    if "insurance" in t:
        normalized["collateral"].append("Insurance Policy")

    if "mutual" in t:
        normalized["collateral"].append("Mutual Fund")

    if "nsc" in t:
        normalized["collateral"].append("NSC/KVP")

    if "course period" in t:
        normalized["moratorium"] = clean(item)

normalized["collateral"] = unique(normalized["collateral"])

# -----------------------------
# Eligibility
# -----------------------------

normalized["eligibility"] = unique(
    sections.get("wondering if you are eligible?", [])
)

# -----------------------------
# Documents
# -----------------------------

docs = sections.get("documents required to get you started", [])

for item in docs:

    t = item.lower()

    if "pan" in t:
        normalized["documents"]["identity"].append("PAN Card")

    elif "passport" in t:
        normalized["documents"]["identity"].append("Passport")

    elif "driving" in t:
        normalized["documents"]["identity"].append("Driving Licence")

    elif "aadhaar" in t:
        normalized["documents"]["identity"].append("Aadhaar Card")

    elif "voter" in t:
        normalized["documents"]["identity"].append("Voter ID Card")

    elif "address proof" in t:
        normalized["documents"]["address"].append("Address Proof")

    elif (
        "marksheet" in t
        or "gre" in t
        or "gmat" in t
        or "toefl" in t
        or "ielts" in t
    ):
        normalized["documents"]["academic"].append(clean(item))

normalized["documents"]["identity"] = unique(normalized["documents"]["identity"])
normalized["documents"]["address"] = unique(normalized["documents"]["address"])
normalized["documents"]["academic"] = unique(normalized["documents"]["academic"])

# -----------------------------
# Fees
# -----------------------------

for item in sections.get("fees & charges", []):

    t = item.lower()

    if "pre-payment" in t:
        normalized["fees"]["prepayment"] = clean(item)

    elif "noc" in t:
        normalized["fees"]["noc"] = clean(item)

    elif "delayed" in t:
        normalized["fees"]["delayed_payment"] = clean(item)

    elif "500" in t:
        normalized["fees"]["cheque_swap"] = clean(item)

# -----------------------------
# Benefits
# -----------------------------

normalized["benefits"] = unique(
    sections.get("loan benefits", [])
)

# -----------------------------
# Covered Courses
# -----------------------------

courses = [
    "MS",
    "MBA",
    "MBBS/MD – Only India Colleges",
    "Executive Management Courses (Working Executives)",
    "All Other Courses – Cases to Case Basis"
]

for item in sections.get("benefits of overseas education loan", []):

    if clean(item) in courses:
        normalized["covered_courses"].append(clean(item))

normalized["covered_courses"] = unique(normalized["covered_courses"])

# -----------------------------
# Expenses Covered
# -----------------------------

keywords = [
    "tuition",
    "living",
    "hostel",
    "travel",
    "books",
    "library",
    "laboratory",
    "computer",
    "laptop"
]

for item in (
    sections.get("benefits of overseas education loan", [])
    + sections.get("why avail of a foreign education loan?", [])
):

    lower = item.lower()

    for keyword in keywords:
        if keyword in lower:
            normalized["expenses_covered"].append(clean(item))
            break

normalized["expenses_covered"] = unique(normalized["expenses_covered"])

# -----------------------------
# Application Process
# -----------------------------

normalized["application_process"] = unique(
    sections.get("how to apply for overseas education loan", [])
)

# -----------------------------
# FAQ
# -----------------------------

faq_ignore = {
    "why choose us?",
    "why avail of a foreign education loan?"
}

for heading, content in sections.items():

    if heading.endswith("?") and heading not in faq_ignore:

        normalized["faq"].append({
            "question": clean(heading),
            "answer": clean(" ".join(content))
        })

# -----------------------------
# Save
# -----------------------------

with open(
    "Data/processed/hdfc_foreign_normalized.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(normalized, f, indent=4, ensure_ascii=False)

print("✅ Normalization Complete")