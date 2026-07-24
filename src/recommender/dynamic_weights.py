
# --------------------------------------------------
# Default Weights
# --------------------------------------------------

DEFAULT_WEIGHTS = {

    "study_type": 20,

    "loan_amount": 20,

    "degree": 10,

    "expense_coverage": 10,

    "collateral": 10,

    "benefits": 10,

    "interest": 8,

    "tenure": 7,

    "moratorium": 3,

    "fees": 2,

    "subsidy": 0
}

# --------------------------------------------------
# Persona Weights
# --------------------------------------------------

PERSONA_WEIGHTS = {

    # ---------------------------------------
    # Foreign Study
    # ---------------------------------------

    "regular_foreign": {

        "study_type": 25,

        "loan_amount": 20,

        "expense_coverage": 15,

        "collateral": 15,

        "degree": 10,

        "benefits": 10,

        "interest": 3,

        "tenure": 2

    },

    "large_foreign": {

        "study_type": 15,

        "loan_amount": 30,

        "expense_coverage": 15,

        "collateral": 15,

        "degree": 5,

        "benefits": 10,

        "interest": 3,

        "tenure": 2

    },

    # ---------------------------------------
    # Domestic
    # ---------------------------------------

    "small_domestic": {

        "study_type": 30,

        "loan_amount": 15,

        "degree": 15,

        "interest": 12,

        "fees": 8,

        "benefits": 8,

        "collateral": 7,

        "tenure": 5

    },

    "regular_domestic": {

        "study_type": 25,

        "loan_amount": 20,

        "degree": 15,

        "interest": 10,

        "benefits": 10,

        "collateral": 10,

        "expense_coverage": 5,

        "tenure": 3,

        "fees": 2

    },

    # ---------------------------------------
    # Subsidy Candidate
    # ---------------------------------------

    "subsidy": {

        "study_type": 20,

        "loan_amount": 15,

        "subsidy": 25,

        "interest": 15,

        "benefits": 10,

        "collateral": 10,

        "degree": 5

    }

}


def get_weights(persona):
    """
    Returns weights for a persona.

    Missing features automatically
    fall back to DEFAULT_WEIGHTS.
    """

    weights = DEFAULT_WEIGHTS.copy()

    if persona in PERSONA_WEIGHTS:

        weights.update(
            PERSONA_WEIGHTS[persona]
        )

    return weights
