import os
import json


def load_loan_documents():

    folder="Data/processed"

    documents=[]


    for filename in os.listdir(folder):

        if filename.endswith(".json"):

            path=os.path.join(
                folder,
                filename
            )


            with open(
                path,
                encoding="utf-8"
            ) as f:

                loan=json.load(f)



            text=f"""

Bank Name:
{loan.get('bank')}


Loan Name:
{loan.get('loan_name')}


Loan Category:
{loan.get('category')}


Loan Amount:
{loan.get('loan_amount')}


Interest Rate:
{loan.get('interest_rate')}


Tenure:
{loan.get('loan_tenure')}


Collateral Requirement:
{loan.get('collateral')}


Moratorium:
{loan.get('moratorium')}


Eligibility:
{loan.get('eligibility')}


Documents Required:
{loan.get('documents')}


Benefits:
{loan.get('benefits')}


Courses Covered:
{loan.get('covered_courses')}


Fees:
{loan.get('fees')}


FAQs:
{loan.get('faq')}

"""


            documents.append(text)


    return documents