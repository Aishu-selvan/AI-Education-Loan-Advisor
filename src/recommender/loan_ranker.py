from .persona_engine import detect_persona
from .dynamic_weights import get_weights

from .candidate_filter import (
    filter_candidate_loans,
    detect_loan_category
)

from .feature_scoring import (
    score_study_type,
    score_loan_amount,
    score_degree,
    score_collateral,
    score_expense_coverage,
    score_interest,
    score_benefits,
    score_tenure,
    score_moratorium,
    score_processing_fee,
    specialization_bonus
)


def calculate_score(profile, loan):

    persona = detect_persona(profile)

    weights = get_weights(persona)

    category = detect_loan_category(loan)

    features = []

    features.append(

        score_study_type(
            profile,
            loan,
            weights["study_type"],
            category
        )

    )

    features.append(

        score_loan_amount(
            profile,
            loan,
            weights["loan_amount"]
        )

    )

    features.append(

        score_degree(
            profile,
            loan,
            weights["degree"]
        )

    )

    features.append(

        score_collateral(
            profile,
            loan,
            weights["collateral"]
        )

    )

    features.append(

        score_expense_coverage(
            profile,
            loan,
            weights["expense_coverage"]
        )

    )

    features.append(

        score_interest(
            loan,
            weights["interest"]
        )

    )

    features.append(

        score_benefits(
            loan,
            weights["benefits"]
        )

    )

    features.append(

        score_tenure(
            loan,
            weights["tenure"]
        )

    )

    features.append(

        score_moratorium(
            loan,
            weights["moratorium"]
        )

    )

    features.append(

        score_processing_fee(
            loan,
            weights["fees"]
        )

    )

    # -----------------------------------
    # Aggregate Score
    # -----------------------------------

    earned = 0

    possible = 0

    reasons = []

    for item in features:

        if item["available"]:

            earned += (
                item["fitness"]
                * item["weight"]
            )

            possible += item["weight"]

        reasons.append(
            item["reason"]
        )

    # -----------------------------------
    # Product Bonus
    # -----------------------------------

    earned += specialization_bonus(
        profile,
        category
    )

    # -----------------------------------
    # Normalize
    # -----------------------------------

    if possible:

        final = round(
            earned / possible * 100,
            1
        )

    else:

        final = 0

    return final, reasons


def rank_loans(profile, loans):

    candidates = filter_candidate_loans(profile, loans)

    loan_candidates = candidates["loans"]
    subsidy_candidates = candidates["subsidies"]
    

    ranked = []

    for loan in loan_candidates:

        score, reasons = calculate_score(
            profile,
            loan
        )

        ranked.append({

            "loan": loan,

            "score": score,

            "reasons": reasons

        })

    ranked.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return {
    "ranked_loans": ranked,
    "eligible_subsidies": subsidy_candidates
}    



# import re

# # ==========================================================
# # WEIGHTS
# # ==========================================================

# WEIGHTS = {
#     "study_type": 25,
#     "loan_amount": 20,
#     "course": 15,
#     "expenses": 15,
#     "collateral": 10,
#     "eligibility": 5,
#     "interest": 5,
#     "benefits": 5
# }


# # ==========================================================
# # MONEY HELPERS
# # ==========================================================

# def money_to_number(value):

#     if value is None:
#         return 0

#     if isinstance(value, (int, float)):
#         return value

#     value = str(value).lower().replace(",", "")

#     number = re.findall(r"\d+\.?\d*", value)

#     if not number:
#         return 0

#     number = float(number[0])

#     if "crore" in value:
#         return int(number * 10000000)

#     if "lakh" in value:
#         return int(number * 100000)

#     return int(number)


# # ==========================================================
# # LOAN HELPERS
# # ==========================================================

# def get_max_loan_amount(loan):

#     amount = loan.get("loan_amount", {})

#     if amount.get("maximum"):
#         return money_to_number(amount["maximum"])

#     if amount.get("secured"):

#         if "no upper" in str(amount["secured"]).lower():
#             return 999999999

#         return money_to_number(amount["secured"])

#     if amount.get("unsecured"):
#         return money_to_number(amount["unsecured"])

#     return 0


# def get_without_collateral_amount(loan):

#     amount = loan.get("loan_amount", {})

#     if amount.get("without_collateral"):
#         return money_to_number(amount["without_collateral"])

#     if amount.get("unsecured"):
#         return money_to_number(amount["unsecured"])

#     return 0


# # ==========================================================
# # NORMALIZATION
# # ==========================================================

# def normalize_text(text):

#     if text is None:
#         return ""

#     if isinstance(text, list):
#         text = " ".join(map(str, text))

#     return str(text).lower()


# # ==========================================================
# # SCORE HELPER
# # ==========================================================

# def add_score(score, possible, earned, possible_points):

#     score += earned
#     possible += possible_points

#     return score, possible


# # ==========================================================
# # STUDY TYPE
# # ==========================================================
# def score_study_type(profile, loan):

#     study = profile.get("study_type")

#     if not study:
#         return 0, 0, "Study type not provided"

#     loan_name = normalize_text(loan.get("loan_name"))
#     sub = normalize_text(loan.get("sub_category"))

#     if study == "abroad":

#         if "foreign" in loan_name:
#             return 25, 25, "Designed for foreign education"

#         elif "domestic" in sub and "international" in sub:
#             return 23, 25, "Supports both domestic and international education"

#         elif "international" in sub:
#             return 22, 25, "Supports international education"

#     return 5, 25, "Primarily Indian education loan"

#     if study == "domestic":

#         if "indian" in loan_name:
#             return 25, 25, "Designed for Indian education"

#         elif "domestic" in sub and "international" in sub:
#             return 23, 25, "Supports both domestic and international education"

#         elif "domestic" in sub:
#             return 24, 25, "Supports Indian education"

#     return 10, 25, "General education loan"


# # ==========================================================
# # LOAN AMOUNT
# # ==========================================================

# def score_loan_amount(profile, loan):

#     required = profile.get("loan_amount")

#     if not required:
#         return 0, 0, "Loan amount not provided"

#     maximum = get_max_loan_amount(loan)

#     if maximum == 0:
#         return 0, 0, "Loan amount not disclosed"

#     coverage = maximum / required

#     if coverage >= 5:
#         return 20, 20, "Excellent loan coverage"

#     elif coverage >= 3:
#         return 18, 20, "Very high loan limit"

#     elif coverage >= 2:
#         return 16, 20, "High loan amount"

#     elif coverage >= 1:
#         return 14, 20, "Requested amount fully covered"

#     elif coverage >= 0.8:
#         return 10, 20, "Most expenses covered"

#     elif coverage >= 0.5:
#         return 6, 20, "Partially covers requirement"

#     return 2, 20, "Loan amount insufficient"

# # ==========================================================
# # COURSE MATCH
# # ==========================================================

# def score_course(profile, loan):

#     degree = normalize_text(profile.get("degree"))

#     if not degree:
#         return 0, 0, "Degree not provided"

#     courses = normalize_text(
#         loan.get("covered_courses")
#     )

#     if degree in courses:
#         return 15, 15, "Degree supported"

#     if (
#         "graduate" in courses
#         and any(x in degree for x in [
#             "btech",
#             "b.e",
#             "be",
#             "bsc",
#             "ba",
#             "bcom",
#             "bca"
#         ])
#     ):
#         return 12, 15, "Graduate course supported"

#     if (
#         "postgraduate" in courses
#         and any(x in degree for x in [
#             "msc",
#             "mba",
#             "mtech",
#             "ma",
#             "mcom",
#             "mca"
#         ])
#     ):
#         return 12, 15, "Postgraduate course supported"

#     if "phd" in degree and "phd" in courses:
#         return 15, 15, "PhD supported"

#     return 5, 15, "Course not explicitly mentioned"

# # ==========================================================
# # EXPENSE MATCH
# # ==========================================================

# def score_expenses(profile, loan):

#     needed = profile.get(
#         "expenses_needed",
#         []
#     )

#     if not needed:
#         return 0,0, "Expense details not provided"

#     covered = normalize_text(
#         loan.get("expenses_covered")
#     )

#     matches = 0

#     for item in needed:

#         if item.lower() in covered:
#             matches += 1

#     ratio = matches / len(needed)

#     earned = round(ratio * 15)

#     return earned,15,f"Covers {matches}/{len(needed)} expenses"


# # ==========================================================
# # COLLATERAL
# # ==========================================================

# def score_collateral(profile, loan):

#     amount = profile.get("loan_amount")

#     # User didn't specify loan amount
#     if not amount:
#         return 0, 0, "Loan amount not provided"

#     collateral_free = get_without_collateral_amount(loan)

#     # Bank doesn't disclose collateral-free limit
#     if collateral_free == 0:
#         return 0, 0, "Collateral-free limit not disclosed"

#     if collateral_free >= amount:
#         return 10, 10, "No collateral required"

#     if collateral_free > 0:
#         return 7, 10, "Partial collateral-free support"

#     return 4, 10, "Collateral likely required"

# # ==========================================================
# # ELIGIBILITY
# # ==========================================================

# def score_eligibility(profile, loan):

#     eligibility = normalize_text(
#         loan.get("eligibility")
#     )

#     # -----------------------------
#     # Missing eligibility
#     # -----------------------------
#     if not eligibility:
#         return 0, 0, "Eligibility not disclosed"

#     score = 0
#     reasons = []

#     study = profile.get("study_type")

#     if study == "abroad":

#         if (
#             "overseas" in eligibility
#             or "abroad" in eligibility
#             or "international" in eligibility
#         ):
#             score += 2
#             reasons.append("Supports overseas education")

#     elif study == "domestic":

#         if (
#             "india" in eligibility
#             or "indian" in eligibility
#         ):
#             score += 2
#             reasons.append("Supports Indian education")

#     if "co-applicant" in eligibility:
#         score += 1
#         reasons.append("Co-applicant supported")

#     if "recognised" in eligibility:
#         score += 2
#         reasons.append("Recognised institutes accepted")

#     score = min(score, 5)

#     return score, 5, ", ".join(reasons)

# #---------------------------------------------------------
# #-------MORATORIUM SCORE----------------------------------
# #---------------------------------------------------------

# def score_moratorium(loan):

#     moratorium = loan.get("moratorium")

#     if isinstance(moratorium, dict):

#         status = normalize_text(
#             moratorium.get("status")
#         )

#         if status == "not_disclosed":
#             return 0, 0, "Moratorium not disclosed"

#     if not moratorium:
#         return 0, 0, "Moratorium unavailable"

#     return 2, 2, "Moratorium available"

# # ==========================================================
# # INTEREST RATE
# # ==========================================================

# def score_interest(loan):

#     interest = loan.get("interest_rate", {})

#     value = interest.get("starting_from")
#     status = normalize_text(
#         interest.get("status")
#     )

#     # -----------------------------
#     # Profile based
#     # Don't affect ranking
#     # -----------------------------

#     if status == "profile_based":
#         return 0, 0, "Interest depends on applicant profile"

#     # -----------------------------
#     # Not disclosed
#     # -----------------------------

#     if status == "not_disclosed":
#         return 0, 0, "Interest not disclosed"

#     if not value:
#         return 0, 0, "Interest unavailable"

#     numbers = re.findall(
#         r"\d+\.?\d*",
#         str(value)
#     )

#     if not numbers:
#         return 0, 0, "Interest information unavailable"

#     rate = float(numbers[0])

#     if rate <= 8:
#         return 5, 5, f"Very low interest ({rate}%)"

#     elif rate <= 10:
#         return 4, 5, f"Competitive interest ({rate}%)"

#     elif rate <= 12:
#         return 3, 5, f"Average interest ({rate}%)"

#     else:
#         return 2, 5, f"Higher interest ({rate}%)"
# # ==========================================================
# # BENEFITS
# # ==========================================================

# def score_benefits(loan):

#     benefits = normalize_text(
#         loan.get("benefits")
#     )

#     if not benefits:
#         return 0, 0, "Benefits unavailable"

#     score = 0

#     keywords = {

#         "instant":1,

#         "pre-admission":1,

#         "insurance":1,

#         "tax":1,

#         "zero margin":1,

#         "no foreclosure":1,

#         "flexible":1,

#         "zero tcs":1

#     }

#     found = []

#     for word, pts in keywords.items():

#         if word in benefits:

#             score += pts
#             found.append(word)

#     score = min(score,5)

#     return score,5,"Benefits: " + ", ".join(found)



# # ==========================================================
# # CONFIDENCE SCORE
# # ==========================================================

# def confidence_score(loan):

#     filled = 0
#     total = 6

#     # Loan Amount
#     if loan.get("loan_amount"):
#         filled += 1

#     # Interest
#     interest = loan.get("interest_rate", {})

#     if interest.get("starting_from"):
#         filled += 1
#     elif interest.get("status") == "profile_based":
#         filled += 0.5

#     # Benefits
#     if loan.get("benefits"):
#         filled += 1

#     # Expenses
#     if loan.get("expenses_covered"):
#         filled += 1

#     # Courses
#     if loan.get("covered_courses"):
#         filled += 1

#     # Eligibility
#     if loan.get("eligibility"):
#         filled += 1

#     return round((filled / total) * 100)


# # ==========================================================
# # MAIN SCORE
# # ==========================================================

# def calculate_score(profile, loan):

#     score = 0
#     possible = 0

#     reasons = []

#     # -----------------------------
#     # Study Type
#     # -----------------------------

#     earned,weight, reason = score_study_type(profile, loan)

#     score, possible = add_score(
#         score,
#         possible,
#         earned,
#         weight
#     )

#     reasons.append(reason)

#     # -----------------------------
#     # Loan Amount
#     # -----------------------------

#     earned, weight, reason = score_loan_amount(profile, loan)

#     score, possible = add_score(
#         score,
#         possible,
#         earned,
#         weight
#     )

#     reasons.append(reason)

#     # -----------------------------
#     # Course
#     # -----------------------------

#     earned,weight, reason = score_course(profile, loan)

#     score, possible = add_score(
#         score,
#         possible,
#         earned,
#         weight
#     )

#     reasons.append(reason)

#     # -----------------------------
#     # Expenses
#     # -----------------------------

#     earned,weight, reason = score_expenses(profile, loan)

#     score, possible = add_score(
#         score,
#         possible,
#         earned,
#         weight
#     )

#     reasons.append(reason)

#     #-----------------------------
#     #---moratorium----------------
#     #-----------------------------

#     earned, weight, reason = score_moratorium(loan)

#     score, possible = add_score(
#         score,
#         possible,
#         earned,
#         weight
#     )

#     reasons.append(reason)

#     # -----------------------------
#     # Collateral
#     # -----------------------------

#     earned,weight, reason = score_collateral(profile, loan)

#     score, possible = add_score(
#         score,
#         possible,
#         earned,
#         weight
#     )

#     reasons.append(reason)

#     # -----------------------------
#     # Eligibility
#     # -----------------------------

#     earned, weight, reason = score_eligibility(profile, loan)

#     score, possible = add_score(
#         score,
#         possible,
#         earned,
#         weight
#     )

#     reasons.append(reason)

#     # -----------------------------
#     # Interest
#     # -----------------------------

#     earned, weight, reason = score_interest(loan)

#     score, possible = add_score(
#         score,
#         possible,
#         earned,
#         weight
#     )

#     reasons.append(reason)

#     # -----------------------------
#     # Benefits
#     # -----------------------------

#     earned, weight, reason = score_benefits(loan)

#     score, possible = add_score(
#         score,
#         possible,
#         earned,
#         weight
#     )

#     reasons.append(reason)

#     # -----------------------------
#     # Final Fitness
#     # -----------------------------

#     # fitness = round(score / possible * 100)
#     if possible == 0:
#         fitness = 0
#     else:
#         fitness = round(score / possible * 100)

#     return {

#         "score": fitness,

#         "confidence": confidence_score(loan),

#         "reasons": reasons

#     }


# # ==========================================================
# # RANKING
# # ==========================================================

# def rank_loans(profile, loans):

#     ranked = []

#     for loan in loans:

#         result = calculate_score(
#             profile,
#             loan
#         )

#         ranked.append({

#             "loan": loan,

#             "score": result["score"],

#             "confidence": result["confidence"],

#             "reasons": result["reasons"]

#         })

#     ranked.sort(

#         key=lambda x: (

#             x["score"]

#         ),

#         reverse=True

#     )

#     return ranked