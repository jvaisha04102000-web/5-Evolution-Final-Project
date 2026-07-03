from typing import List, Dict

import numpy as np
from utils.similarity_utils import SimilarityUtils

from document_loader import DocumentData
from workflows.langchain_pipeline import LangChainPipeline


class DuplicateDocumentDetector:
    """
    Enterprise Duplicate Document Detector

    Features
    --------
    ✔ Uses shared LangChain embedding model
    ✔ Cosine similarity
    ✔ Duplicate detection
    ✔ Similar document detection
    """

    def __init__(self):

        self.pipeline = LangChainPipeline()

        self.embedding_model = self.pipeline.embedding_model

    def detect_duplicates(
        self,
        documents: List[DocumentData],
        threshold: float = 0.85
    ) -> List[Dict]:

        texts = [
            document.text
            for document in documents
        ]

        embeddings = self.embedding_model.embed_documents(
            texts
        )

        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        similarity_matrix = SimilarityUtils.similarity_matrix(
            embeddings
        )
        

        duplicates = []

        total_documents = len(documents)

        for i in range(total_documents):

            for j in range(i + 1, total_documents):

                similarity = float(
                    similarity_matrix[i][j]
                )

                if similarity >= threshold:

                    duplicates.append({

                        "document_1":
                            documents[i].file_name,

                        "document_2":
                            documents[j].file_name,

                        "similarity_score":
                            round(
                                similarity * 100,
                                2
                            ),

                        "status":
                            (
                                "Duplicate"
                                if similarity >= 0.95
                                else "Highly Similar"
                            )

                    })

        duplicates.sort(

            key=lambda x: x["similarity_score"],

            reverse=True

        )

        return duplicates


if __name__ == "__main__":

    from document_loader import DocumentLoader
    from text_extractor import TextExtractor

    loader = DocumentLoader(
        "data/raw_docs"
    )

    extractor = TextExtractor()

    documents = extractor.clean_documents(
        loader.load_documents()
    )

    detector = DuplicateDocumentDetector()

    results = detector.detect_duplicates(
        documents
    )

    print("=" * 80)
    print("Duplicate Document Report")
    print("=" * 80)

    if not results:

        print("No duplicate documents found.")

    else:

        for result in results:

            print(result)

            print("-" * 80)