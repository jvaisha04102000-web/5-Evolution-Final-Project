import re
from typing import List

from src.document_loader import DocumentData
from utils.text_utils import TextUtils


class TextExtractor:
    """
    Enterprise Text Preprocessing Engine

    Features:
    - Remove extra spaces
    - Normalize text
    - Clean unicode characters
    - Generate metadata
    """

    def __init__(self):
        pass

    def clean_documents(
        self,
        documents: List[DocumentData]
    ) -> List[DocumentData]:

        cleaned_documents = []

        for document in documents:

            document.text = self.clean_text(document.text)

            document.metadata["word_count"] = TextUtils.word_count(
                document.text
            )

            document.metadata["character_count"] = TextUtils.character_count(
                document.text
            )

            cleaned_documents.append(document)

        return cleaned_documents

    @staticmethod
    def clean_text(text: str) -> str:

        if not text:
            return ""

        text = TextUtils.normalize_text(text)

        return text


if __name__ == "__main__":

    from src.document_loader import DocumentLoader

    loader = DocumentLoader("data/raw_docs")

    documents = loader.load_documents()

    extractor = TextExtractor()

    cleaned_documents = extractor.clean_documents(documents)

    print("=" * 60)
    print(f"Documents Processed : {len(cleaned_documents)}")
    print("=" * 60)

    for document in cleaned_documents:

        print("File:", document.file_name)
        print("Meta:", document.metadata)
        print("Preview:", TextUtils.preview(document.text))
        print("-" * 80)