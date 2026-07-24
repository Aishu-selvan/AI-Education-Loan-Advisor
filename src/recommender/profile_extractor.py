
import re

# -----------------------------------------
# Countries
# -----------------------------------------

COUNTRIES = [
    "usa",
    "united states",
    "uk",
    "canada",
    "germany",
    "australia",
    "france",
    "japan",
    "singapore"
]

# -----------------------------------------
# Indian Cities
# -----------------------------------------

INDIAN_CITIES = [
    "chennai",
    "bangalore",
    "bengaluru",
    "hyderabad",
    "mumbai",
    "delhi",
    "pune",
    "kolkata",
    "coimbatore",
    "madurai",
    "tiruvannamalai",
    "trichy",
    "salem",
    "vellore"
]

# -----------------------------------------
# Courses
# -----------------------------------------

COURSES = [
    "ms",
    "mba",
    "btech",
    "mtech",
    "phd",
    "mbbs",
    "engineering",
    "graduate",
    "postgraduate",
    "diploma"
]

# -----------------------------------------
# Premium Institutes
# -----------------------------------------

PREMIUM_INSTITUTES = [
    "iit",
    "iim",
    "nit",
    "bits",
    "isb",
    "mit",
    "stanford",
    "oxford",
    "cambridge"
]

# -----------------------------------------
# Expense Keywords
# -----------------------------------------

EXPENSES = [
    "tuition",
    "hostel",
    "accommodation",
    "living",
    "travel",
    "books",
    "laptop",
    "computer",
    "insurance",
    "project",
    "library",
    "laboratory",
    "lab",
    "study tour"
]

# -----------------------------------------
# Collateral Keywords
# -----------------------------------------

NO_COLLATERAL = [
    "no collateral",
    "without collateral",
    "dont have collateral",
    "don't have collateral",
    "no security",
    "without security"
]

HAS_COLLATERAL = [
    "property",
    "house",
    "land",
    "fixed deposit",
    "fd",
    "insurance policy"
]



def extract_profile(text):

    text_lower = text.lower()

    # IMPORTANT:
    # Keep everything as None.
    # Profile memory will fill in missing values.
    profile = {

    "course": None,

    "study_location": None,

    "study_type": None,

    "loan_amount": None,

    "family_income": None,

    "has_collateral": None,

    "required_expenses": [],

    "profile_tier": "premium",

    "admission_status": None

}

    # ------------------------
    # Course
    # ------------------------

    for course in COURSES:

        if course in text_lower:

            profile["course"] = course.upper()

            break
    
    for city in INDIAN_CITIES:

        if city in text_lower:

            profile["study_location"] = city.title()
            profile["study_type"] = "domestic"
            break

# -----------------------------------------
# Required Expenses
# -----------------------------------------

    for expense in EXPENSES:

        if expense in text_lower:

            profile["required_expenses"].append(
                expense
            )

# -----------------------------------------
# Premium Institute
# -----------------------------------------

    for institute in PREMIUM_INSTITUTES:

        if institute in text_lower:

            profile["profile_tier"] = "premium"
            break


    # ------------------------
    # Country
    # ------------------------

    for country in COUNTRIES:

        if country in text_lower:

            profile["study_location"] = country.title()

            profile["study_type"] = "abroad"

            break


# -----------------------------------------
# Admission Status
# -----------------------------------------

    if any(word in text_lower for word in [
        "got admission",
        "confirmed admission",
        "offer letter",
        "admitted"
    ]):

        profile["admission_status"] = "confirmed"

    elif any(word in text_lower for word in [
        "planning",
        "will apply",
        "want to apply"
    ]):

        profile["admission_status"] = "planning"

    # ------------------------
    # Domestic Study
    # ------------------------

    if (
        "india" in text_lower
        or "indian" in text_lower
    ):

        profile["study_location"] = "India"

        profile["study_type"] = "domestic"

    # ------------------------
    # Loan Amount
    # Examples:
    # Need 50 lakh loan
    # Loan of 40 lakh
    # Borrow 30 lakh
    # ------------------------

    loan_match = re.search(
        r"(need|loan|borrow|require).*?(\d+(?:\.\d+)?)\s*lakh",
        text_lower
    )

    if loan_match:

        profile["loan_amount"] = (
            float(loan_match.group(2))
            * 100000
        )

    crore_match = re.search(
        r"(need|loan|borrow|require).*?(\d+(?:\.\d+)?)\s*crore",
        text_lower
    )

    if crore_match:

        profile["loan_amount"] = (
            float(crore_match.group(2))
            * 10000000
        )

    # ------------------------
    # Family Income
    # Examples:
    # Family income is 8 lakh
    # Income 4 lakh
    # Annual income 6 lakh
    # ------------------------

    income_match = re.search(
        r"(family income|annual income|income).*?(\d+(?:\.\d+)?)\s*lakh",
        text_lower
    )

    if income_match:

        profile["family_income"] = (
            float(income_match.group(2))
            * 100000
        )

    income_crore = re.search(
        r"(family income|annual income|income).*?(\d+(?:\.\d+)?)\s*crore",
        text_lower
    )

    if income_crore:

        profile["family_income"] = (
            float(income_crore.group(2))
            * 10000000
        )

    return profile