from typing import List, Dict

from workflows.langchain_pipeline import LangChainPipeline


class HRChatbot:
    """
    Enterprise HR AI Chatbot

    Features
    --------
    ✔ HR Policy QA
    ✔ Company Document QA
    ✔ Resume QA
    ✔ Conversation History
    ✔ AI Interaction Logging
    """

    def __init__(self):

        self.pipeline = LangChainPipeline()

        self.pipeline.initialize_qa()

        self.chat_history = []

    def ask(
        self,
        question: str
    ) -> Dict:

        response = self.pipeline.ask(question)

        interaction = {

            "question": question,

            "answer": response["answer"],

            "sources": [

                doc.metadata.get(
                    "file_name",
                    "Unknown"
                )

                for doc in response["sources"]

            ]

        }

        self.chat_history.append(interaction)

        return interaction

    def get_chat_history(self):

        return self.chat_history

    def clear_chat_history(self):

        self.chat_history.clear()


if __name__ == "__main__":

    chatbot = HRChatbot()

    print("=" * 70)
    print("Enterprise HR AI Chatbot")
    print("Type 'exit' to quit")
    print("=" * 70)

    while True:

        question = input("\nYou : ")

        if question.lower() == "exit":
            break

        response = chatbot.ask(question)

        print("\nBot :")

        print(response["answer"])

        print("\nSources :")

        for source in response["sources"]:

            print("-", source)

        print("-" * 70)