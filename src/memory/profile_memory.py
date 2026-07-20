"""
Stores user profile across the conversation.

Only updates fields that appear in the latest message.
"""

profile_memory = {
    "course": None,
    "study_location": None,
    "study_type": None,
    "loan_amount": None,
    "family_income": None
}


def update_profile(new_profile):
    """
    Merge extracted profile into memory.

    Ignore None values.
    """

    global profile_memory

    for key, value in new_profile.items():

        if value is not None:

            profile_memory[key] = value

    return profile_memory


def get_profile():
    """
    Return current profile.
    """

    return profile_memory


def clear_profile():
    """
    Start a new conversation.
    """

    global profile_memory

    profile_memory = {
        "course": None,
        "study_location": None,
        "study_type": None,
        "loan_amount": None,
        "family_income": None
    }

    return profile_memory