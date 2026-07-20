import re

def money_to_number(value):
    """
    Converts:
    ₹75 lakh -> 7500000
    ₹1.5 crore -> 15000000
    ₹3 crore -> 30000000
    """

    if not value:
        return 0

    value = value.lower().replace(",", "")

    number = re.findall(r"\d+\.?\d*", value)

    if not number:
        return 0

    number = float(number[0])

    if "crore" in value:
        return int(number * 10000000)

    if "lakh" in value:
        return int(number * 100000)

    return int(number)

def get_max_loan_amount(loan):

    amount = loan.get("loan_amount", {})

    if "maximum" in amount:
        return money_to_number(amount["maximum"])

    elif "secured" in amount:

        secured = amount["secured"]

        if "no upper limit" in secured.lower():
            return 999999999

        return money_to_number(secured)

    elif "unsecured" in amount:
        return money_to_number(amount["unsecured"])

    return 0

def get_without_collateral_amount(loan):

    amount = loan.get("loan_amount", {})

    if "without_collateral" in amount:
        return money_to_number(amount["without_collateral"])

    if "unsecured" in amount:
        return money_to_number(amount["unsecured"])

    return 0


def calculate_score(profile, loan):

    score = 0
    reasons = []

    loan_name = loan.get("loan_name", "").lower()
    sub_category = loan.get("sub_category", "").lower()

    eligibility = " ".join(
        loan.get("eligibility", [])
    ).lower()

    benefits = " ".join(
        loan.get("benefits", [])
    ).lower()

    covered_courses = " ".join(
        loan.get("covered_courses", [])
    ).lower()

    expenses = " ".join(
        loan.get("expenses_covered", [])
    ).lower()

    maximum = get_max_loan_amount(loan)

    without_collateral = get_without_collateral_amount(loan)

    interest = loan.get(
        "interest_rate",
        {}
    ).get(
        "starting_from",
        ""
    )

    # ----------------------------------------------------
    # STUDY LOCATION
    # ----------------------------------------------------

    if profile["study_type"] == "abroad":

        if "foreign" in loan_name:

            score += 100
            reasons.append("Designed specifically for foreign education")

        elif "international" in sub_category:

            score += 80
            reasons.append("Supports international education")

        elif "overseas" in covered_courses:

            score += 80
            reasons.append("Supports overseas education")

        else:

            score += 20
            reasons.append("General education loan")

    else:

        if "indian" in loan_name:

            score += 20

            reasons.append(
                "Designed for studies in India"
            )

    # ----------------------------------------------------
    # LOAN AMOUNT
    # ----------------------------------------------------

    required = profile.get(
        "loan_amount"
    )

    if required:

        if maximum >= required:

            score += 35

            reasons.append(
                "Loan amount is sufficient"
            )

        else:

            score -= 50

            reasons.append(
                "Loan amount may not be sufficient"
            )

    # ----------------------------------------------------
    # COLLATERAL
    # ----------------------------------------------------

    if without_collateral > 0:

        score += 20

        reasons.append(
            "Without collateral option available"
        )

    # ----------------------------------------------------
    # LOW INCOME
    # ----------------------------------------------------

    income = profile.get(
        "family_income"
    )

    if income:

        if income <= 450000:

            if (
                "economically weaker"
                in eligibility
            ):

                score += 60

                reasons.append(
                    "Eligible for EWS subsidy"
                )

        else:

            if (
                "economically weaker"
                in eligibility
            ):

                score -= 20

                reasons.append(
                    "Income exceeds subsidy limit"
                )

    # ----------------------------------------------------
    # MORATORIUM
    # ----------------------------------------------------

    if loan.get("moratorium"):

        score += 10

        reasons.append(
            "Moratorium available"
        )

    # ----------------------------------------------------
    # BENEFITS
    # ----------------------------------------------------

    if "interest subsidy" in benefits:

        score += 30

        reasons.append(
            "Interest subsidy available"
        )

    # ----------------------------------------------------
    # INTEREST RATE
    # ----------------------------------------------------

    if interest:

        score += 10

        reasons.append(
            "Interest rate available"
        )

    return score, reasons


def rank_loans(profile, loans):

    ranked = []

    for loan in loans:

        score, reasons = calculate_score(
            profile,
            loan
        )

        ranked.append(
            {
                "score": score,
                "loan": loan,
                "reasons": reasons
            }
        )

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked


