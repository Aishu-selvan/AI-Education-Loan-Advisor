import streamlit as st

from src.rag.chatbot import ask_advisor

st.set_page_config(
    page_title="AI Loan Advisor",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Education Loan Advisor")

st.write(
    "Ask anything about education loans."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

question = st.chat_input(
    "Ask your question..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.spinner("Thinking..."):

        answer = ask_advisor(question)

    with st.chat_message("assistant"):

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )