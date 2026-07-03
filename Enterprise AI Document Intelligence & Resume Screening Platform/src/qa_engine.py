from workflows.langchain_pipeline import LangChainPipeline


class DocumentQAEngine:
    """
    Enterprise Document Question Answering Engine

    Features
    --------
    ✔ Question Answering over uploaded documents
    ✔ Retrieval-Augmented Generation (RAG)
    ✔ Semantic document retrieval
    ✔ Source document tracking
    """

    def __init__(self):
        self.pipeline = LangChainPipeline()
        self.pipeline.initialize_qa()

    def ask_question(self, question: str) -> dict:
        """
        Ask a question against the uploaded document knowledge base.

        Returns:
            {
                "answer": "...",
                "sources": [...]
            }
        """
        return self.pipeline.ask(question)

    def semantic_search(self, query: str, top_k: int = 5):
        """
        Perform semantic search without generating an answer.
        """
        return self.pipeline.similarity_search(
            query=query,
            top_k=top_k
        )


if __name__ == "__main__":

    qa = DocumentQAEngine()

    while True:

        question = input("\nAsk Question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        response = qa.ask_question(question)

        print("\nAnswer")
        print("-" * 60)
        print(response["answer"])

        print("\nSource Documents")
        print("-" * 60)

        for index, source in enumerate(response["sources"], start=1):

            metadata = source.metadata

            print(f"\nSource {index}")
            print(f"File : {metadata.get('file_name', 'Unknown')}")
            print(f"Chunk : {metadata.get('chunk_id', '-')}")
            print(source.page_content[:250])