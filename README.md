# 🎓 AI Education Loan Advisor

An AI-powered Education Loan Recommendation System that helps students identify the most suitable education loan based on their academic profile, financial requirements, and study destination.

Unlike traditional rule-based systems, this project focuses on **student fitness** rather than simply comparing loan features.

---

## Features

- AI-powered education loan recommendation
- Student profile extraction using LLM
- Rule-based student fitness scoring
- Retrieval-Augmented Generation (RAG)
- Loan comparison with explainable recommendations
- Domestic and International education loan support
- Interactive Streamlit chatbot
- Loan ranking with confidence score
- Detailed pros and cons for each recommendation

---

## Supported Banks

- HDFC Bank
  - Education Loan for Indian Education
  - Foreign Education Loan
  - Central Government Interest Subsidy Scheme (CGISS)

- ICICI Bank
  - Education Loan

---

## Tech Stack

### Backend

- Python
- LangChain
- FAISS
- HuggingFace Embeddings
- Groq Llama 3
- Streamlit

### AI Components

- Retrieval Augmented Generation (RAG)
- Rule-Based Recommendation Engine
- Student Fitness Scoring
- Prompt Engineering

### Data Processing

- BeautifulSoup
- Playwright
- JSON Normalization

---

## Project Structure

```
fin_ai/
│
├── app.py
├── README.md
│
├── data/
│   ├── raw/
│   ├── processed/
│
├── src/
│   ├── rag/
│   ├── recommender/
│   ├── scraper/
│   ├── normalization/
│
├── requirements.txt
└── .env
```

---

## How It Works

### 1. User Query

Example:

```
I want to pursue an MBA in Germany.

Loan amount: ₹50 lakh

No collateral.
```

↓

### 2. Profile Extraction

The chatbot extracts

- Study Destination
- Degree
- Loan Amount
- Family Income
- Collateral Availability
- Required Expenses

↓

### 3. Loan Ranking

Each loan is evaluated using a Student Fitness Score based on

- Study Type
- Degree Match
- Loan Amount Coverage
- Expenses Covered
- Collateral Requirement
- Eligibility
- Interest Rate
- Benefits
- Moratorium

↓

### 4. AI Recommendation

The chatbot explains

- Best Loan
- Why it matches
- Pros
- Cons
- Eligibility
- Required Documents
- Final Recommendation

---

## Student Fitness Scoring

The recommendation engine evaluates loans using weighted scoring.

| Feature | Weight |
|----------|---------|
| Study Type | 25 |
| Loan Amount Coverage | 20 |
| Course Match | 15 |
| Expenses Covered | 15 |
| Collateral Fit | 10 |
| Eligibility | 5 |
| Interest Rate | 5 |
| Benefits | 5 |

The engine avoids bias by treating unavailable information (for example, profile-based interest rates) as **unknown** rather than assigning a penalty.

---

## Run Locally

Clone the repository

```bash
git clone https://github.com/Aishu-selvan/AI-Education-Loan-Advisor.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env`

```
GROQ_API_KEY=YOUR_KEY
```

Run

```bash
streamlit run app.py
```

---

## Example Queries

- I want to pursue MBA in Germany with a loan of ₹50 lakh.
- I want to study M.Tech in Chennai and need ₹15 lakh.
- I have no collateral and need an education loan.
- Compare HDFC and ICICI education loans.
- Which education loan is best for studying abroad?

---

## Future Improvements

- Add SBI, Axis Bank, PNB, and Canara Bank loans
- Hybrid Retrieval + Rule-Based Ranking
- Institute ranking integration
- Credit score analysis
- EMI calculator
- Loan eligibility prediction using ML
- Loan comparison dashboard

---

## Author

**Aiswarya T**

- IIT Madras BS in Data Science and Applications
- AI / Machine Learning Enthusiast
- Generative AI Developer
