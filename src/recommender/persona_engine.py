def detect_persona(profile):
    """
    Returns one of:

    regular_foreign
    large_foreign

    regular_domestic
    small_domestic

    subsidy

    general
    """

    study_type = profile.get("study_type")

    loan_amount = profile.get("loan_amount") or 0

    family_income = profile.get("family_income") or 0

    has_collateral = profile.get("has_collateral")

    course = (profile.get("course") or "").lower()

    # ======================================
    # Foreign Education
    # ======================================

    if study_type == "abroad":

        # High funding abroad
        if loan_amount >= 8000000:
            return "large_foreign"

        return "regular_foreign"

    # ======================================
    # Domestic Education
    # ======================================

    if study_type == "domestic":

        # Subsidy profile

        if (
            family_income > 0
            and family_income <= 450000
        ):
            return "subsidy"

        # Small domestic loan

        if (
            loan_amount > 0
            and loan_amount <= 2500000
        ):
            return "small_domestic"

        return "regular_domestic"

    # ======================================
    # Fallback
    # ======================================

    return "general"
