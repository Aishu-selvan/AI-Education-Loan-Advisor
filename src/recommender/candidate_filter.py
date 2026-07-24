"""
Candidate Loan Filter

This module removes loans that are not
relevant to the student's profile.

Example

Foreign student

↓

Compare

HDFC Foreign
ICICI Education

NOT

HDFC Indian
CGISS
"""


def detect_loan_category(loan):
    """
    Classifies loan products.

    Returns

    foreign
    indian
    subsidy
    both
    general
    """

    loan_name = loan.get(
        "loan_name",
        ""
    ).lower()

    sub_category = loan.get(
        "sub_category",
        ""
    ).lower()

    category = loan.get(
        "category",
        ""
    ).lower()

    text = " ".join([
        loan_name,
        sub_category,
        category
    ])

    # -------------------------
    # HDFC Foreign
    # -------------------------

    if (
        "foreign" in text
        or "international" in text
    ):
        return "foreign"

    # -------------------------
    # HDFC Indian
    # -------------------------

    if (
        "indian" in text
        or "domestic" in text
    ):
        return "indian"

    # -------------------------
    # Subsidy
    # -------------------------

    if (
        "subsidy" in text
        or "cgiss" in text
    ):
        return "subsidy"

    # -------------------------
    # ICICI
    # -------------------------

    return "both"

def filter_candidate_loans(profile, loans):
    """
    Returns only the loans relevant
    for the student.
    """

    study_type = profile.get(
        "study_type"
    )

    family_income = (
        profile.get(
            "family_income"
        )
        or 0
    )

    loan_candidates = []

    subsidy_candidates = []

    for loan in loans:

        category = detect_loan_category(
            loan
        )

        # ==================================
        # Foreign
        # ==================================

        if study_type == "abroad":

            if category in [
                "foreign",
                "both"
            ]:

                loan_candidates.append(
                    loan
                )

            continue

        # ==================================
        # Domestic
        # ==================================

        if study_type == "domestic":

            if category in [
                "indian",
                "both"
            ]:

                loan_candidates.append(
                    loan
                )

            elif (
                category == "subsidy"
                and family_income <= 450000
            ):

                subsidy_candidates.append(
                    loan
                )

            continue

        # ==================================
        # Unknown
        # ==================================

        loan_candidates.append(
            loan
        )

    return {

    "loans": loan_candidates,

    "subsidies": subsidy_candidates

}