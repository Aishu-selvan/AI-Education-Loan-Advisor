from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings

from src.loader.json_loader import load_loan_documents



documents = load_loan_documents()


embedding = HuggingFaceEmbeddings(
model_name=
"sentence-transformers/all-MiniLM-L6-v2"
)


db = FAISS.from_texts(
documents,
embedding
)


db.save_local(
"loan_faiss_db"
)


print("Loan Knowledge Base Created")