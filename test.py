from src.rag.chatbot import ask_advisor

while True:

    question = input("You: ")

    print()

    print(
        ask_advisor(question)
    )

    print()