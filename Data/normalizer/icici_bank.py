import json
import re
from datetime import datetime

# ---------------------------------------------------
# Load Raw JSON
# ---------------------------------------------------

INPUT_FILE = "Data/raw/icici_education.json"
OUTPUT_FILE = "Data/processed/icici_education.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw = json.load(f)

sections = raw.get("sections", [])

# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------

def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)
    text = text.replace("\u00a0", " ")
    text = text.strip()

    return text


def unique_list(items):
    seen = set()
    result = []

    for item in items:
        item = clean_text(item)

        if not item:
            continue

        if item.lower() in seen:
            continue

        seen.add(item.lower())
        result.append(item)

    return result


def find_section(keyword):

    keyword = keyword.lower()

    for section in sections:

        heading = section.get("heading", "").lower()

        if keyword in heading:
            return section

    return None


def section_text(section):

    if not section:
        return ""

    return " ".join(section.get("content", []))


def extract(pattern, text):

    m = re.search(pattern, text, re.I)

    if m:
        return m.group(1).strip()

    return ""


# ---------------------------------------------------
# Collect Full Text
# ---------------------------------------------------

all_text = ""

for sec in sections:

    all_text += " "

    all_text += sec.get("heading", "")

    all_text += " "

    all_text += " ".join(sec.get("content", []))

all_text = clean_text(all_text)

# ---------------------------------------------------
# Basic Fields
# ---------------------------------------------------

bank = raw.get("bank", "")

loan_name = raw.get("loan_scheme", "")

category = "Education Loan"

sub_category = "Domestic & International"

source_url = raw.get("url", "")

last_updated = datetime.today().strftime("%Y-%m-%d")

# ---------------------------------------------------
# Loan Amount
# ---------------------------------------------------
loan_amount = {
    "maximum": "",
    "without_collateral": ""
}

for sec in sections:

    for line in sec.get("content", []):

        line = clean_text(line)

        # Maximum loan
        if re.search(r"Loan[s]?\s+up\s+to\s+(?:₹|Rs\.?)\s*3\s*Crore", line, re.I):
            loan_amount["maximum"] = "₹3 crore"

        # Collateral-free loan
        if re.search(
            r"Collateral[- ]free loan up to\s+(?:₹|Rs\.?)\s*1\s*Crore",
            line,
            re.I
        ):
            loan_amount["without_collateral"] = "₹1 crore"
# ---------------------------------------------------
# Interest Rate
# ---------------------------------------------------

interest_rate = {
    "type": "",
    "starting_from": ""
}

rate = re.search(r"(\d+\.\d+\s*%)", all_text)

if rate:
    interest_rate["starting_from"] = rate.group(1)

# ---------------------------------------------------
# Loan Tenure
# ---------------------------------------------------

loan_tenure = ""

m = re.search(
    r"Loan tenure up to\s*([\d]+\s*years?)",
    all_text,
    re.I
)

if m:
    loan_tenure = m.group(1)

# ---------------------------------------------------
# Collateral
# ---------------------------------------------------

collateral = []

if "Property" in all_text:
    collateral.append("Property")

if "Fixed Deposit" in all_text:
    collateral.append("Fixed Deposit")

if "existing ICICI Bank Home Loan" in all_text:
    collateral.append("Existing ICICI Bank Home Loan")

if "Mortgage Loan" in all_text:
    collateral.append("Mortgage Loan")

collateral = unique_list(collateral)

# ---------------------------------------------------
# Moratorium
# ---------------------------------------------------

moratorium = ""

m = re.search(
    r"principal moratorium period",
    all_text,
    re.I
)

if m:
    moratorium = ""
# ---------------------------------------------------
# Eligibility
# ---------------------------------------------------
eligibility = []

section = find_section("What are the eligibility criteria")

if section:

    for line in section.get("content", []):

        line = clean_text(line)

        if len(line) > 250:
            continue

        if line.endswith(":"):
            continue

        if ":" not in line:
            continue

        eligibility.append(line)

eligibility = unique_list(eligibility)

# ---------------------------------------------------
# Documents
# ---------------------------------------------------

documents = {
    "identity": [],
    "address": [],
    "academic": []
}

section = find_section("Required Documents")

if section:

    text = section_text(section)

    # Identity

    ids = [
        "Aadhaar Card",
        "Voter ID",
        "Driving Licence"
    ]

    for i in ids:

        if i.lower() in text.lower():

            documents["identity"].append(i)

    # Address

    if "Proof of Current Address" in text:

        documents["address"].append("Current Address Proof")

    # Academic

    academic = [

        "Marksheets",

        "Degree Certificate",

        "Entrance Scores",

        "Admission Letter",

        "Confirmation of Acceptance",

        "I20",

        "Salary Slip",

        "Bank Statement",

        "ITR",

        "GST Documents"

    ]

    mapping = {

        "Marksheets":"Marksheets",

        "Degree Certificate":"Degree Certificate",

        "Entrance Scores":"Entrance Scores",

        "Admission Letter":"Admission Proof",

        "Confirmation of Acceptance":"Confirmation of Acceptance",

        "I20":"I20",

        "Salary Slip":"Salary slip",

        "Bank Statement":"Bank statement",

        "ITR":"ITR",

        "GST Documents":"GST"

    }

    for final, search in mapping.items():

        if search.lower() in text.lower():

            documents["academic"].append(final)

documents["identity"] = unique_list(documents["identity"])
documents["address"] = unique_list(documents["address"])
documents["academic"] = unique_list(documents["academic"])

# ---------------------------------------------------
# Fees
# ---------------------------------------------------

fees = {
    "processing_fee": "",
    "legal_charges": "",
    "delayed_payment": "",
    "cheque_swap": ""
}

# ---------------------------------------------------
# Benefits
# ---------------------------------------------------

benefits = []

mapping = {
    "Loan up to ₹3 crore": r"Loan[s]?\s+up\s+to\s+₹3\s*crore",
    "Collateral-free loan up to ₹1 crore": r"Collateral[- ]free loan up to\s+₹1\s*crore",
    "Flexible repayment options": r"Flexible repayment",
    "Pre-admission sanction": r"Pre-admission sanction",
    "No foreclosure charges": r"No foreclosure",
    "Competitive interest rates": r"Competitive interest",
    "Zero margin for selected institutes": r"Zero margin",
    "Wide network for loan servicing": r"Wide network",
    "Instant Education Loan": r"Instant Education Loan",
    "Loan tenure up to 15 years": r"Loan tenure up to 15 years",
    "Zero TCS": r"Zero TCS"
}

for final, pattern in mapping.items():

    if re.search(pattern, all_text, re.I):

        benefits.append(final)

benefits = unique_list(benefits)


# ---------------------------------------------------
# Covered Courses
# ---------------------------------------------------
covered_courses = []

text = all_text

courses = {

    "Graduation":"Graduation",

    "Postgraduate Degree":"Postgraduate Degree",

    "Postgraduate Diploma":"Postgraduate Diploma",

    "Professional Education":"Professional Education",

    "PhD":"PhD"

}

for final, search in courses.items():

    if search.lower() in text.lower():

        covered_courses.append(final)

covered_courses = unique_list(covered_courses)



# ---------------------------------------------------
# Expenses Covered
# ---------------------------------------------------

expenses_covered = []

expense_section = find_section("expenses")

if expense_section:

    text = section_text(expense_section)

    keywords = [

        "Tuition Fees",

        "Hostel Fees",

        "Examination Fees",

        "Library Fees",

        "Laboratory Fees",

        "Insurance Premium",

        "Travel Expenses",

        "Books",

        "Computer",

        "Uniform",

        "Project Expenses",

        "Study Tour"

    ]

    mapping = {
        "Tuition Fees":"Fees payable at the college or hostel",
        "Hostel Fees":"hostel",
        "Examination Fees":"Examination",
        "Library Fees":"library",
        "Laboratory Fees":"laboratory",
        "Insurance Premium":"Insurance premium",
        "Travel Expenses":"travel",
        "Books":"books",
        "Computer":"computer",
        "Uniform":"uniform",
        "Project Expenses":"project",
        "Study Tour":"study tour"
    }

    for final_name, search in mapping.items():

        if search.lower() in text.lower():

            expenses_covered.append(final_name)

expenses_covered = unique_list(expenses_covered)

# ---------------------------------------------------
# Application Process
# ---------------------------------------------------

application_process = []

apply_section = find_section("How to apply")

if apply_section:

    text = section_text(apply_section)

    steps = [

        "Scan the QR Code and enter the basic details",

        "Application submission",

        "Document submission",

        "Loan assessment",

        "Sanction letter, disbursement"

    ]

    for step in steps:

        if step.lower() in text.lower():

            application_process.append(step)

application_process = unique_list(application_process)


# ---------------------------------------------------
# FAQ Extraction
# ---------------------------------------------------


faq = []

faq_section = find_section("Education Loan FAQs")

if faq_section:

    text = section_text(faq_section)

    # Remove duplicate whitespace
    text = re.sub(r"\s+", " ", text)

    # Split whenever a question starts with common question words
    parts = re.split(
        r'(?=(?:What|Who|How|Can|Does|Is|Why)\s[^?]+\?)',
        text
    )

    for part in parts:

        part = part.strip()

        if "?" not in part:
            continue

        q, a = part.split("?", 1)

        question = q.strip() + "?"

        answer = a.strip()

        if len(answer) > 20:

            faq.append({
                "question": question,
                "answer": answer
            })


# ---------------------------------------------------
# Final Cleanup
# ---------------------------------------------------

eligibility = unique_list(eligibility)
benefits = unique_list(benefits)
covered_courses = unique_list(covered_courses)
expenses_covered = unique_list(expenses_covered)
application_process = unique_list(application_process)

# ---------------------------------------------------
# Final JSON
# ---------------------------------------------------

normalized = {

    "bank": bank,

    "loan_name": loan_name,

    "category": category,

    "sub_category": sub_category,

    "loan_amount": loan_amount,

    "interest_rate": interest_rate,

    "loan_tenure": loan_tenure,

    "collateral": collateral,

    "moratorium": moratorium,

    "eligibility": eligibility,

    "documents": documents,

    "fees": fees,

    "benefits": benefits,

    "covered_courses": covered_courses,

    "expenses_covered": expenses_covered,

    "application_process": application_process,

    "faq": faq,

    "source_url": source_url,

    "last_updated": last_updated
}

# ---------------------------------------------------
# Save
# ---------------------------------------------------

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        normalized,
        f,
        indent=4,
        ensure_ascii=False
    )

print("✅ ICICI Education Loan normalized successfully.")

# ---------------------------------------------------
# Preview
# ---------------------------------------------------

print(json.dumps(normalized, indent=4, ensure_ascii=False))