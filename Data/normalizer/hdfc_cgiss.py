import json
import re
from datetime import date


# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------

def clean(text):

    if not text:
        return ""

    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = text.rstrip(".")

    return text


def unique(items):

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
    "Data/raw/hdfc_cgiss.json",
    encoding="utf-8"
) as f:

    raw = json.load(f)


# ---------------------------------------------------
# Merge Sections
# ---------------------------------------------------

sections = {}

for sec in raw["sections"]:

    heading = clean(sec["heading"]).lower()

    if heading not in sections:
        sections[heading] = []

    sections[heading].extend(
        sec["content"]
    )


for key in sections:

    sections[key] = unique(
        sections[key]
    )


# Flatten all text for robust extraction

all_content = []

for values in sections.values():

    all_content.extend(values)


all_content = unique(all_content)


# ---------------------------------------------------
# Final Schema
# ---------------------------------------------------

normalized = {

    "bank": raw["bank"],

    "loan_name": raw["loan_scheme"],

    "category": "Education Loan",

    "sub_category":
        "Government Interest Subsidy",

    "product_type":
        "Subsidy Scheme",


    "loan_amount": {},


    "interest_rate": {

        "actual_rate":
        "As per linked education loan",

        "subsidy":
        "",

        "effective_interest_during_moratorium":
        ""

    },


    "subsidy": {

        "available": True,

        "scheme":
        "Central Government Interest Subsidy Scheme",

        "coverage": "",

        "period": "",

        "income_limit": "",

        "applicable_amount": ""

    },


    "income_criteria": {},


    "loan_tenure": {

    "duration": "",

    "note":
    "Tenure depends on underlying education loan"

},


    "repayment": {

        "start": "",

        "moratorium": ""

    },


    "collateral": {

        "required": None,

        "note":
        "Collateral depends on underlying education loan"

    },


    "study_location": {

        "india": True,

        "abroad": False

    },


    "eligibility": [],


    "documents": {

        "identity": [],

        "address": [],

        "academic": [],

        "income": []

    },


    "fees": {},


    "benefits": [],


    "covered_courses": [],


    "expenses_covered": [],


    "application_process": [],


    "faq": [],


    "metadata": {

        "is_actual_loan": False,

        "linked_product":
        "Education Loan",

        "keywords":[
            "CGISS",
            "interest subsidy",
            "government education loan",
            "EWS education loan"
        ]

    },


    "source_url": raw["url"],

    "last_updated":
        str(date.today())

}



# ---------------------------------------------------
# Loan Amount
# ---------------------------------------------------

for item in all_content:

    lower = item.lower()


    if (
        "10 lakh" in lower
        or "10 lakhs" in lower
    ):

        normalized["loan_amount"]["maximum"] = (
            "₹10 lakh"
        )

        normalized["subsidy"]["applicable_amount"] = (
            "Education loan up to ₹10 lakh"
        )


    if "7.5 lakh" in lower:

        normalized["loan_amount"]["without_collateral"] = (
            "₹7.5 lakh"
        )
# ---------------------------------------------------
# Loan Tenure
# ---------------------------------------------------

for item in all_content:

    lower = item.lower()

    if (
        "years" in lower
        or "year" in lower
        or "repayment period" in lower
        or "tenure" in lower
    ):

        normalized["loan_tenure"]["duration"] = clean(item)

        normalized["repayment"]["maximum_tenure"] = clean(item)

        break


# ---------------------------------------------------
# Interest + Subsidy
# ---------------------------------------------------

for item in all_content:

    lower = item.lower()


    if "interest subsidy" in lower:

        normalized["interest_rate"]["subsidy"] = (
            "100% interest subsidy"
        )

        normalized["interest_rate"][
            "effective_interest_during_moratorium"
        ] = "0%"


        normalized["subsidy"]["coverage"] = (
            "Full interest subsidy"
        )


    if "moratorium" in lower:

        normalized["subsidy"]["period"] = (
            "Moratorium period"
        )

        normalized["repayment"]["moratorium"] = clean(item)



# ---------------------------------------------------
# Income Criteria
# ---------------------------------------------------

for item in all_content:

    lower = item.lower()


    if (
        "income" in lower
        or "4.5 lakh" in lower
    ):

        normalized["income_criteria"][
            "family_income"
        ] = clean(item)


        normalized["subsidy"][
            "income_limit"
        ] = clean(item)



# ---------------------------------------------------
# Eligibility
# ---------------------------------------------------

eligibility_keywords = [

    "student",
    "indian",
    "income",
    "ews",
    "economically",
    "weaker",
    "approved",
    "course",
    "admission"

]


for item in all_content:

    lower = item.lower()


    if any(
        word in lower
        for word in eligibility_keywords
    ):

        normalized["eligibility"].append(
            clean(item)
        )


normalized["eligibility"] = unique(
    normalized["eligibility"]
)



# ---------------------------------------------------
# Documents
# ---------------------------------------------------

for item in all_content:

    lower = item.lower()


    if (
        "aadhaar" in lower
        or "passport" in lower
        or "identity" in lower
        or "voter" in lower
    ):

        normalized["documents"]["identity"].append(
            clean(item)
        )


    elif (
        "address" in lower
        or "residence" in lower
    ):

        normalized["documents"]["address"].append(
            clean(item)
        )


    elif (
        "admission" in lower
        or "marksheet" in lower
        or "academic" in lower
    ):

        normalized["documents"]["academic"].append(
            clean(item)
        )


    elif (
        "income certificate" in lower
        or "income proof" in lower
    ):

        normalized["documents"]["income"].append(
            clean(item)
        )


for key in normalized["documents"]:

    normalized["documents"][key] = unique(
        normalized["documents"][key]
    )



# ---------------------------------------------------
# Benefits
# ---------------------------------------------------

for item in all_content:

    lower=item.lower()


    if "subsidy" in lower:

        normalized["benefits"].append(
            "Government interest subsidy benefit"
        )


    if "moratorium" in lower:

        normalized["benefits"].append(
            "No interest burden during moratorium"
        )


    if "higher education" in lower:

        normalized["benefits"].append(
            "Supports higher education"
        )


normalized["benefits"]=unique(
    normalized["benefits"]
)



# ---------------------------------------------------
# Expenses Covered
# ---------------------------------------------------

for item in all_content:

    if "interest" in item.lower():

        normalized[
            "expenses_covered"
        ].append(
            "Interest during moratorium period"
        )


normalized["expenses_covered"]=unique(
    normalized["expenses_covered"]
)



# ---------------------------------------------------
# Courses
# ---------------------------------------------------

for item in all_content:

    lower=item.lower()


    if "technical" in lower:

        normalized["covered_courses"].append(
            "Technical Courses"
        )


    if "professional" in lower:

        normalized["covered_courses"].append(
            "Professional Courses"
        )


normalized["covered_courses"]=unique(
    normalized["covered_courses"]
)



# ---------------------------------------------------
# Application Process
# ---------------------------------------------------

for heading, content in sections.items():

    if "apply" in heading:

        normalized["application_process"] = unique(
            content
        )



# ---------------------------------------------------
# FAQ
# ---------------------------------------------------

ignore = [
    "feature",
    "benefit",
    "document",
    "eligible"
]


for heading, content in sections.items():

    if (
        heading.endswith("?")
        and not any(
            x in heading
            for x in ignore
        )
    ):

        answer = clean(
            " ".join(content)
        )


        if answer:

            normalized["faq"].append(
                {
                    "question":
                    clean(heading),

                    "answer":
                    answer
                }
            )



# ---------------------------------------------------
# Save
# ---------------------------------------------------

with open(
    "Data/processed/hdfc_cgiss_normalized.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        normalized,
        f,
        indent=4,
        ensure_ascii=False
    )


print(
    "✅ CGISS Normalization Complete"
)