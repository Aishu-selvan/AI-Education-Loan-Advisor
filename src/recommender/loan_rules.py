

# ==========================================================
# PERSONA THRESHOLDS
# ==========================================================

PERSONA_RULES = {

    # Foreign students needing high funding
    "large_foreign_loan": 8000000,      # 80 lakh

    # Small domestic loan
    "small_domestic_loan": 2500000,     # 25 lakh

    # Government subsidy income limit
    "subsidy_income_limit": 450000

}


# ==========================================================
# SPECIALIZATION BONUS
# ==========================================================

SPECIALIZATION_BONUS = {

    "foreign": 3,

    "indian": 3,

    "both": 1,

    "subsidy": 2

}


# ==========================================================
# LOAN AMOUNT FIT
# ==========================================================

LOAN_AMOUNT_RULES = {

    # Bank fully satisfies requested amount
    "full_match": 1.0,

    # Bank covers at least 80%
    "partial_match": 0.8,

    # Bank covers at least 50%
    "minimum_match": 0.5

}


# ==========================================================
# COLLATERAL
# ==========================================================

COLLATERAL_RULES = {

    "full_without_collateral": 1.0,

    "partial_without_collateral": 0.8,

    "collateral_required": 0.2

}


# ==========================================================
# INTEREST RATE
# ==========================================================

INTEREST_RULES = {

    "excellent": 8,

    "good": 10,

    "average": 11.5

}


# ==========================================================
# TENURE
# ==========================================================

TENURE_RULES = {

    "excellent": 15,

    "good": 10,

    "average": 5

}


# ==========================================================
# SUBSIDY
# ==========================================================

SUBSIDY_RULES = {

    "max_income":450000

}


# ==========================================================
# PRODUCT PRIORITY
# ==========================================================

PRODUCT_PRIORITY = {

    "foreign": [

        "Foreign Education Loan",

        "Education Loan"

    ],

    "domestic": [

        "Education Loan for Indian Education",

        "Education Loan"

    ]

}
