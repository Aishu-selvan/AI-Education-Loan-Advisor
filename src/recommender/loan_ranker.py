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

#     return ranked
