from typing import Dict

from workflows.langchain_pipeline import LangChainPipeline
from src.logger import logger


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

        logger.info("HR Chatbot initialized")

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

        # Log AI interaction
        logger.log_ai_interaction(
            module="HR Chatbot",
            question=question,
            answer=response["answer"]
        )

        # Log activity
        logger.log_activity(
            module="HR Chatbot",
            action="Question Answered",
            status="Success",
            details={
                "question": question,
                "sources": interaction["sources"]
            }
        )

        return interaction

    def get_chat_history(self):

        return self.chat_history

    def clear_chat_history(self):

        self.chat_history.clear()

        logger.log_activity(
            module="HR Chatbot",
            action="Clear Chat History",
            status="Success"
        )


if __name__ == "__main__":

    chatbot = HRChatbot()

    print("=" * 70)
    print("Enterprise HR AI Chatbot")
    print("Type 'exit' to quit")
    print("=" * 70)

    while True:

        question = input("\nYou : ")

        if question.lower() == "exit":

            logger.info("HR Chatbot closed")

            break

        response = chatbot.ask(question)

        print("\nBot :")

        print(response["answer"])

        print("\nSources :")

        for source in response["sources"]:

            print("-", source)

        print("-" * 70)