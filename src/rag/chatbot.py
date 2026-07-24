from dotenv import load_dotenv

load_dotenv()

import json
import os

from langchain_groq import ChatGroq

from src.rag.prompt import SYSTEM_PROMPT

from src.recommender.profile_extractor import extract_profile
from src.recommender.loan_ranker import rank_loans
from src.memory.profile_memory import (
    update_profile,
    get_profile,
    clear_profile
)


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


# -----------------------------------------
# Load all processed loans
# -----------------------------------------

loans = []

folder = "Data/processed"

for file in os.listdir(folder):

    with open(
        os.path.join(folder, file),
        encoding="utf-8"
    ) as f:

        loans.append(
            json.load(f)
        )


# -----------------------------------------
# Loan Advisor
# -----------------------------------------

def ask_advisor(question):

    if question.lower() in [
        "reset",
        "new chat",
        "clear"
    ]:

        clear_profile()

        return "Conversation cleared."

    new_profile = extract_profile(question)
    
    profile = update_profile(new_profile)


    result = rank_loans(profile, loans)

    ranked = result["ranked_loans"]

    eligible_subsidies = result["eligible_subsidies"]


        


# ----------------------------
# DEBUG: Show loan ranking
# ----------------------------

    print("\n==============================")
    print("Loan Ranking")
    print("==============================")

    for item in ranked:
        print(
            f"{item['loan']['loan_name']}  --->  Score: {item['score']}"
        )

    print()

    # ----------------------------

    top_loans = ranked[:2]

    context = ""


    top_loans = ranked[:2]

    context = ""

    for item in top_loans:

        loan = item["loan"]

        context += f"""
    


Bank:
{loan['bank']}

Loan:
{loan['loan_name']}

Score:
{item['score']}

Reasons:
{", ".join(item['reasons'])}

Loan Details:

{json.dumps(loan, indent=2)}



"""


    if eligible_subsidies:

        context += "\n===== ELIGIBLE SUBSIDIES =====\n\n"

        for subsidy in eligible_subsidies:

            context += f"""
    Bank:
    {subsidy["bank"]}

    Scheme:
    {subsidy["loan_name"]}

    {subsidy.get("benefits", [])}

-------------------------------------
"""
            



    prompt = f"""

{SYSTEM_PROMPT}

User Profile

{profile}



Top Recommended Loans

{context}



User Question

{question}



Instructions

Compare only these loans.

Explain

1. Which loan is best

2. Why

3. Pros

4. Cons

5. Eligibility

6. Documents

7. Final recommendation

Do not invent information.

"""

    response = llm.invoke(prompt)

    return response.content


if __name__ == "__main__":
    print("=== AI Education Loan Advisor ===")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ")

        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        answer = ask_advisor(question)
        print("\nAdvisor:\n")
        print(answer)
        print("-" * 60)