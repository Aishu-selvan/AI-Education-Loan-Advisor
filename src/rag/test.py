from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


db = FAISS.load_local(
    "loan_faiss_db",
    embedding,
    allow_dangerous_deserialization=True
)


question = """
I am from a low income family.
My family income is 3 lakh.
I need education loan for engineering.
Which loan is suitable?
"""


results = db.similarity_search(
    question,
    k=2
)


for i,doc in enumerate(results):

    print("\n========== RESULT",i+1,"==========")

    print(doc.page_content[:1000])