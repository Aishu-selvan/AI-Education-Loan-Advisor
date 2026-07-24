import re

# ---------------------------------------------------------
# Money Conversion
# ---------------------------------------------------------

def money_to_number(value):

    if not value:
        return 0

    value = str(value).lower().replace(",", "")

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
        return money_to_number(
            amount["maximum"]
        )

    if "secured" in amount:

        secured = amount["secured"]

        if (
            isinstance(secured, str)
            and
            "no upper limit" in secured.lower()
        ):
            return 999999999

        return money_to_number(
            secured
        )

    if "unsecured" in amount:

        return money_to_number(
            amount["unsecured"]
        )

    return 0


def get_without_collateral_amount(loan):

    amount = loan.get(
        "loan_amount",
        {}
    )

    if "without_collateral" in amount:

        return money_to_number(
            amount["without_collateral"]
        )

    if "unsecured" in amount:

        return money_to_number(
            amount["unsecured"]
        )

    return 0

def feature_result(
    fitness,
    weight,
    reason,
    available=True
):
    """
    Returns one feature result.

    fitness

    0 to 1

    available

    False means

    do not include
    in normalization.
    """

    return {

        "feature": "loan_amount",

        "fitness": fitness,

        "weight": weight,

        "reason": reason,

        "available": available

    }



def score_loan_amount(
    profile,
    loan,
    weight
):

    required = (
        profile.get(
            "loan_amount"
        )
        or 0
    )

    maximum = get_max_loan_amount(
        loan
    )

    if required == 0:

        return feature_result(

            0.5,

            weight,

            "Requested amount not specified"

        )

    # -----------------------------------
    # Enough is enough
    # -----------------------------------

    if maximum >= required:

        return feature_result(

            1,

            weight,

            "Fully supports requested loan amount"

        )

    ratio = maximum / required

    return feature_result(

        ratio,

        weight,

        "Maximum loan amount is lower than requested"

    )



def score_study_type(
    profile,
    loan,
    weight,
    category
):

    study = profile.get(
        "study_type"
    )

    if not study:

        return feature_result(

            0.5,

            weight,

            "Study type not specified"

        )

    if study == "abroad":

        if category == "foreign":

            return feature_result(

                1,

                weight,

                "Dedicated foreign education loan"

            )

        if category == "both":

            return feature_result(

                0.9,

                weight,

                "Supports foreign education"

            )

        return feature_result(

            0,

            weight,

            "Not suitable for foreign education"

        )

    if study == "domestic":

        if category == "indian":

            return feature_result(

                1,

                weight,

                "Dedicated Indian education loan"

            )

        if category == "both":

            return feature_result(

                0.9,

                weight,

                "Supports Indian education"

            )

        return feature_result(

            0,

            weight,

            "Not suitable for domestic education"

        )

    return feature_result(
        0.5,
        weight,
        "Unknown study type"
    )


# ---------------------------------------------------------
# Degree Score
# ---------------------------------------------------------

def score_degree(profile, loan, weight):

    course = (profile.get("course") or "").lower()

    covered = " ".join(
        loan.get(
            "covered_courses",
            []
        )
    ).lower()

    if not course:

        return feature_result(
            0.5,
            weight,
            "Course not specified"
        )

    # Direct Match

    if course in covered:

        return feature_result(
            1,
            weight,
            f"{course.upper()} is supported"
        )

    # Graduate Mapping

    graduate = [
        "btech",
        "engineering",
        "mbbs"
    ]

    postgraduate = [
        "mba",
        "ms",
        "mtech"
    ]

    if (
        course in graduate
        and "graduate" in covered
    ):

        return feature_result(
            1,
            weight,
            "Graduate course supported"
        )

    if (
        course in postgraduate
        and "postgraduate" in covered
    ):

        return feature_result(
            1,
            weight,
            "Postgraduate course supported"
        )

    return feature_result(
        0.3,
        weight,
        "Course not explicitly mentioned"
    )


def score_collateral(
    profile,
    loan,
    weight
):

    has_collateral = profile.get(
        "has_collateral"
    )

    required = profile.get(
        "loan_amount"
    ) or 0

    without = get_without_collateral_amount(
        loan
    )

    # ----------------------------
    # User never mentioned
    # ----------------------------

    if has_collateral is None:

        return feature_result(
            0.6,
            weight,
            "Collateral preference unknown"
        )

    # ----------------------------
    # User HAS collateral
    # ----------------------------

    if has_collateral:

        return feature_result(
            1,
            weight,
            "Collateral available"
        )

    # ----------------------------
    # User has NO collateral
    # ----------------------------

    if required <= without:

        return feature_result(
            1,
            weight,
            "Collateral-free loan available"
        )

    if without > 0:

        ratio = without / required

        return feature_result(
            ratio,
            weight,
            "Partial collateral-free support"
        )

    return feature_result(
        0,
        weight,
        "Collateral required"
    )


def score_expense_coverage(
    profile,
    loan,
    weight
):

    required = profile.get(
        "required_expenses",
        []
    )

    covered = " ".join(
        loan.get(
            "expenses_covered",
            []
        )
    ).lower()

    if not required:

        return feature_result(
            0.5,
            weight,
            "Expense preferences not specified"
        )

    matched = 0

    for expense in required:

        if expense.lower() in covered:

            matched += 1

    fitness = matched / len(required)

    return feature_result(

        fitness,

        weight,

        f"Covers {matched} of {len(required)} requested expenses"

    )


def score_interest(
    loan,
    weight
):

    interest = loan.get(
        "interest_rate",
        {}
    ).get(
        "starting_from",
        ""
    )

    if not interest:

        return feature_result(
            0,
            weight,
            "Interest not disclosed",
            available=False
        )

    numbers = re.findall(
        r"\d+\.?\d*",
        interest
    )

    if not numbers:

        return feature_result(
            0,
            weight,
            "Interest depends on profile",
            available=False
        )

    rate = float(numbers[0])

    if rate <= 8:

        fitness = 1

    elif rate <= 10:

        fitness = 0.8

    elif rate <= 11:

        fitness = 0.6

    else:

        fitness = 0.3

    return feature_result(
        fitness,
        weight,
        f"Interest starts from {rate}%"
    )



BENEFITS = {

    "tax":2,

    "insurance":2,

    "emi":2,

    "pre-admission":2,

    "instant":2,

    "no foreclosure":2,

    "zero margin":2,

    "zero tcs":1,

    "flexible repayment":2

}

def score_benefits(
    loan,
    weight
):

    text = " ".join(
        loan.get(
            "benefits",
            []
        )
    ).lower()

    earned = 0

    maximum = sum(
        BENEFITS.values()
    )

    for key, value in BENEFITS.items():

        if key in text:

            earned += value

    return feature_result(

        earned / maximum,

        weight,

        "Borrower benefits evaluated"

    )


# def score_tenure(loan, weight):

#     tenure = loan.get("loan_tenure")

#     # -----------------------
#     # Missing
#     # -----------------------

#     if tenure is None:

#         return feature_result(
#             0,
#             weight,
#             "Loan tenure unavailable",
#             available=False
#         )

#     tenure = str(tenure)

#     numbers = re.findall(r"\d+", tenure)

#     if not numbers:

#         return feature_result(
#             0,
#             weight,
#             "Loan tenure unavailable",
#             available=False
#         )

#     years = int(numbers[0])

#     fitness = min(years / 15, 1)

#     return feature_result(
#         fitness,
#         weight,
#         f"{years}-year repayment period"
#     )


def score_tenure(loan, weight):

    tenure = loan.get("loan_tenure")

    print("=" * 60)
    print("Bank:", loan.get("bank"))
    print("Loan:", loan.get("loan_name"))
    print("Loan tenure value:", tenure)
    print("Type:", type(tenure))
    print("=" * 60)

    if tenure is None:
        return feature_result(
            0,
            weight,
            "Loan tenure unavailable",
            available=False
        )

    tenure = str(tenure)

    numbers = re.findall(r"\d+", tenure)

    if not numbers:
        return feature_result(
            0,
            weight,
            "Loan tenure unavailable",
            available=False
        )

    years = int(numbers[0])

    fitness = min(years / 15, 1)

    return feature_result(
        fitness,
        weight,
        f"{years}-year repayment period"
    )

    print("TENURE =", repr(tenure), type(tenure))

# def score_tenure(
#     loan,
#     weight
# ):

#     tenure = loan.get(
#         "loan_tenure",
#         ""
#     )

#     numbers = re.findall(
#         r"\d+",
#         tenure
#     )

#     if not numbers:

#         return feature_result(
#             0,
#             weight,
#             "Tenure unavailable",
#             available=False
#         )

#     years = int(numbers[0])

#     fitness = min(
#         years / 15,
#         1
#     )

#     return feature_result(
#         fitness,
#         weight,
#         f"{years}-year repayment period"
#     )


def score_moratorium(
    loan,
    weight
):

    if not loan.get("moratorium"):

        return feature_result(
            0,
            weight,
            "Moratorium not disclosed",
            available=False
        )

    return feature_result(
        1,
        weight,
        "Moratorium available"
    )


def score_processing_fee(
    loan,
    weight
):

    fee = loan.get(
        "fees",
        {}
    ).get(
        "processing_fee",
        ""
    )

    if not fee:

        return feature_result(
            0,
            weight,
            "Fee not disclosed",
            available=False
        )

    fee = fee.lower()

    if "nil" in fee:

        return feature_result(
            1,
            weight,
            "No processing fee"
        )

    return feature_result(
        0.6,
        weight,
        fee
    )


def specialization_bonus(
    profile,
    category
):
    """
    Small bonus for dedicated products.

    HDFC Foreign

    vs

    ICICI General

    NOT a huge bonus.
    """

    study = profile.get(
        "study_type"
    )

    if study == "abroad":

        if category == "foreign":
            return 3

        if category == "both":
            return 1

    if study == "domestic":

        if category == "indian":
            return 3

        if category == "both":
            return 1

    return 0