import json
import re
from datetime import date

# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------

def clean(text):
    """Remove extra spaces and trailing periods."""
    if not text:
        return ""

    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = text.rstrip(".")
    return text


def unique(items):
    """Remove duplicates while preserving order."""
    seen = set()
    output = []

    for item in items:
        item = clean(item)

        if item and item not in seen:
            seen.add(item)
            output.append(item)

    return output


# ---------------------------------------------------
# Load Raw JSON
# ---------------------------------------------------

with open(
    "Data/raw/hdfc_indian_education.json",
    encoding="utf-8"
) as f:
    raw = json.load(f)


# ---------------------------------------------------
# Merge Duplicate Headings
# ---------------------------------------------------

sections = {}

for sec in raw["sections"]:

    heading = clean(sec["heading"]).lower()

    if heading not in sections:
        sections[heading] = []

    sections[heading].extend(sec["content"])


# Remove duplicate contents inside every section

for heading in sections:
    sections[heading] = unique(sections[heading])


# ---------------------------------------------------
# Output Schema
# ---------------------------------------------------

normalized = {

    "bank": raw["bank"],

    "loan_name": raw["loan_scheme"],

    "category": "Education Loan",

    "sub_category": "Indian Education",

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

# ---------------------------------------------------
# Loan Amount
# ---------------------------------------------------

loan_details = sections.get("loan benefits", [])

for item in loan_details:

    lower = item.lower()

    # Maximum Loan Amount
    if "1.5 crore" in lower or "1.5 cr" in lower:
        normalized["loan_amount"]["maximum"] = "₹1.5 crore"

    # Loan without collateral
    if "50 lakh" in lower and "collateral" in lower:
        normalized["loan_amount"]["without_collateral"] = "₹50 lakh"


# ---------------------------------------------------
# Interest Rate
# ---------------------------------------------------

fees = sections.get("fees & charges", [])

for item in fees:

    lower = item.lower()

    # Fixed interest
    if "starting from" in lower:

        rate = re.search(r"(\d+(\.\d+)?)\s*%", item)

        if rate:

            normalized["interest_rate"] = {
                "type": "Fixed",
                "starting_from": rate.group(1) + "% p.a."
            }


# ---------------------------------------------------
# Loan Tenure
# ---------------------------------------------------

details = sections.get("loan details", [])

for item in details:

    lower = item.lower()

    tenure = re.search(r'(\d+)\s*years?', lower)

    if tenure:

        normalized["loan_tenure"] = tenure.group(1) + " years"


# ---------------------------------------------------
# Collateral
# ---------------------------------------------------

for item in details:

    lower = item.lower()

    if "fixed deposit" in lower:
        normalized["collateral"].append("Fixed Deposit")

    if "insurance" in lower:
        normalized["collateral"].append("Insurance Policy")

    if "mutual fund" in lower:
        normalized["collateral"].append("Mutual Fund")

    if "nsc" in lower or "kvp" in lower:
        normalized["collateral"].append("NSC/KVP")


normalized["collateral"] = unique(normalized["collateral"])


# ---------------------------------------------------
# Moratorium
# ---------------------------------------------------

for item in details:

    lower = item.lower()

    if "course period" in lower:

        normalized["moratorium"] = clean(item)

# ---------------------------------------------------
# Eligibility
# ---------------------------------------------------

normalized["eligibility"] = unique(
    sections.get("wondering if you’re eligible?", [])
)

# ---------------------------------------------------
# ---------------------------------------------------
# Documents
# ---------------------------------------------------

docs = sections.get("documents required to get you started", [])

for item in docs:

    lower = item.lower()

    # ---------------- Identity ----------------

    if (
        "identity proof" in lower
        or "kyc" in lower
        or "pan" in lower
        or "passport" in lower
        or "aadhaar" in lower
        or "driving" in lower
        or "voter" in lower
    ):
        normalized["documents"]["identity"].append(clean(item))

    # ---------------- Address ----------------

    elif (
        "residence proof" in lower
        or "address proof" in lower
    ):
        normalized["documents"]["address"].append(clean(item))

    # ---------------- Academic ----------------

    elif (
        "admission" in lower
        or "marksheet" in lower
        or "10th" in lower
        or "12th" in lower
        or "degree" in lower
    ):
        normalized["documents"]["academic"].append(clean(item))

    # ---------------- Financial ----------------

    elif (
        "salary slip" in lower
        or "bank statement" in lower
        or "itr" in lower
        or "balance sheet" in lower
        or "income documents" in lower
    ):
        normalized["documents"]["academic"].append(clean(item))

    # ---------------- Others ----------------

    elif (
        "application form" in lower
        or "photograph" in lower
        or "signature proof" in lower
        or "age proof" in lower
    ):
        normalized["documents"]["academic"].append(clean(item))


normalized["documents"]["identity"] = unique(
    normalized["documents"]["identity"]
)

normalized["documents"]["address"] = unique(
    normalized["documents"]["address"]
)

normalized["documents"]["academic"] = unique(
    normalized["documents"]["academic"]
)

# ---------------------------------------------------
# Fees
# ---------------------------------------------------

for item in fees:

    lower = item.lower()

    if "processing" in lower:

        if "nil" in lower and "7,50,000" in lower:

            normalized["fees"]["processing_fee"] = \
                "Nil up to ₹7.5 lakh, otherwise 1%"

    if "legal" in lower:
        normalized["fees"]["legal_charges"] = "At actual"

    if "delayed" in lower:
        normalized["fees"]["delayed_payment"] = \
            "Interest on overdue installment"

    if "cheque" in lower or "ach" in lower:
        normalized["fees"]["cheque_swap"] = "NIL"

# ---------------------------------------------------
# Benefits
# ---------------------------------------------------

benefit_sections = (
    sections.get("loan benefits", [])
    + sections.get("convenience", [])
    + sections.get("benefits of education loan", [])
)

for item in benefit_sections:

    lower = item.lower()

    if "1.5 crore" in lower:
        normalized["benefits"].append(
            "Loan up to ₹1.5 crore"
        )

    elif "50 lakh" in lower:
        normalized["benefits"].append(
            "Up to ₹50 lakh without collateral"
        )

    elif "transparent" in lower:
        normalized["benefits"].append(
            "Transparent process"
        )

    elif "minimal" in lower:
        normalized["benefits"].append(
            "Minimal documentation"
        )

    elif "emi" in lower:
        normalized["benefits"].append(
            "Pocket-friendly EMI"
        )

    elif "tax" in lower:
        normalized["benefits"].append(
            "Tax benefit under Section 80E"
        )

    elif "insurance" in lower:
        normalized["benefits"].append(
            "Insurance protection available"
        )

    elif "institution" in lower:
        normalized["benefits"].append(
            "Direct disbursement to institution"
        )

normalized["benefits"] = unique(
    normalized["benefits"]
)

# ---------------------------------------------------
# Expenses Covered
# ---------------------------------------------------

expense_source = (
    sections.get("benefits of education loan", [])
    + sections.get("how does an education loan work?", [])
)

for item in expense_source:

    lower = item.lower()

    if "tuition" in lower:
        normalized["expenses_covered"].append(
            "Tuition Fees"
        )

    if "accommodation" in lower:
        normalized["expenses_covered"].append(
            "Accommodation"
        )

    if "educational expenses" in lower:
        normalized["expenses_covered"].append(
            "Educational Expenses"
        )

normalized["expenses_covered"] = unique(
    normalized["expenses_covered"]
)

# ---------------------------------------------------
# Covered Courses
# ---------------------------------------------------

# ---------------------------------------------------
# Covered Courses
# ---------------------------------------------------

course_sections = sections.get("wondering if you’re eligible?", [])

for item in course_sections:

    lower = item.lower()

    if "graduate" in lower:
        normalized["covered_courses"].append("Graduate Degree")

    if "pg" in lower or "post graduate" in lower:
        normalized["covered_courses"].append("Postgraduate Degree")

    if "diploma" in lower:
        normalized["covered_courses"].append("Diploma")

normalized["covered_courses"] = unique(
    normalized["covered_courses"]
)

# ---------------------------------------------------
# Application Process
# ---------------------------------------------------

normalized["application_process"] = unique(
    sections.get("how to apply for an education loan?", [])
)

# ---------------------------------------------------
# FAQ
# ---------------------------------------------------

faq_ignore = {
    "why choose us?",
    "loan benefits",
    "fees & charges",
    "loan details",
    "convenience"
}

for heading, content in sections.items():

    if heading.endswith("?") and heading not in faq_ignore:

        normalized["faq"].append({

            "question": clean(heading),

            "answer": clean(
                " ".join(content)
            )

        })

# ---------------------------------------------------
# Remove Empty FAQ Answers
# ---------------------------------------------------

normalized["faq"] = [
    x for x in normalized["faq"]
    if x["answer"]
]

# ---------------------------------------------------
# Save JSON
# ---------------------------------------------------

with open(
    "Data/processed/hdfc_indian_normalized.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        normalized,
        f,
        indent=4,
        ensure_ascii=False
    )

print("✅ Normalization Complete")