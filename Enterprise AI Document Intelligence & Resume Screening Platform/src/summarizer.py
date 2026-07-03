from langchain_core.prompts import ChatPromptTemplate
from workflows.langchain_pipeline import LangChainPipeline


class DocumentSummarizer:
    """
    Enterprise AI Document Summarizer

    Features
    --------
    ✔ Executive Summary
    ✔ Detailed Summary
    ✔ Bullet Summary
    ✔ Uses Shared LangChain Pipeline
    """

    def __init__(self):

        self.pipeline = LangChainPipeline()

    def summarize(
            self,
            document_text: str,
            summary_type: str = "executive"
    ):

        prompts = {

            "executive":
                """
                You are an enterprise AI assistant.

                Generate an executive summary of the document.

                Keep it concise.

                Document:

                {document}
                """,

            "detailed":
                """
                Summarize the document.

                Include all important information.

                Document:

                {document}
                """,

            "bullet":
                """
                Summarize the document into bullet points.

                Document:

                {document}
                """

        }

        prompt = ChatPromptTemplate.from_template(
            prompts[summary_type]
        )

        chain = prompt | self.pipeline.llm

        response = chain.invoke({

            "document": document_text

        })

        return response.content


if __name__ == "__main__":

    from document_loader import DocumentLoader
    from text_extractor import TextExtractor

    loader = DocumentLoader("data/raw_docs")

    docs = loader.load_documents()

    extractor = TextExtractor()

    docs = extractor.clean_documents(docs)

    summarizer = DocumentSummarizer()

    summary = summarizer.summarize(

        docs[0].text,

        summary_type="executive"

    )

    print("=" * 70)

    print(summary)

    print("=" * 70)