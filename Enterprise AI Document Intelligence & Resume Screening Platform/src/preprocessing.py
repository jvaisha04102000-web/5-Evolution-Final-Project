from typing import List
from dataclasses import dataclass
from src.document_loader import DocumentData


@dataclass
class TextChunk:
    chunk_id: int
    file_name: str
    file_path: str
    file_type: str
    text: str
    metadata: dict


class DocumentPreprocessor:
    """
    Enterprise Document Chunking Engine

    Features
    --------
    ✔ Fixed-size chunking
    ✔ Chunk overlap
    ✔ Metadata preservation
    ✔ Ready for Embeddings
    ✔ Ready for LangChain
    """

    def __init__(self,
                 chunk_size: int = 500,
                 chunk_overlap: int = 100):

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def create_chunks(
        self,
        documents: List[DocumentData]
    ) -> List[TextChunk]:

        chunks = []

        chunk_counter = 1

        for document in documents:

            words = document.text.split()

            start = 0

            while start < len(words):

                end = start + self.chunk_size

                chunk_text = " ".join(words[start:end])

                chunks.append(

                    TextChunk(
                        chunk_id=chunk_counter,
                        file_name=document.file_name,
                        file_path=document.file_path,
                        file_type=document.file_type,
                        text=chunk_text,
                        metadata={
                            **document.metadata,
                            "chunk_number": chunk_counter,
                            "start_word": start,
                            "end_word": min(end, len(words))
                        }
                    )

                )

                chunk_counter += 1

                start += self.chunk_size - self.chunk_overlap

        return chunks


if __name__ == "__main__":

    from src.document_loader import DocumentLoader
    from src.text_extractor import TextExtractor

    loader = DocumentLoader("data/raw_docs")

    documents = loader.load_documents()

    extractor = TextExtractor()

    cleaned_documents = extractor.clean_documents(documents)

    preprocessor = DocumentPreprocessor(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = preprocessor.create_chunks(cleaned_documents)

    print("=" * 70)
    print(f"Total Documents : {len(cleaned_documents)}")
    print(f"Total Chunks    : {len(chunks)}")
    print("=" * 70)

    for chunk in chunks[:5]:

        print(f"Chunk ID : {chunk.chunk_id}")
        print(chunk.file_name)
        print(chunk.metadata)
        print(chunk.text[:250])
        print("-" * 70)

    from workflows.langchain_pipeline import LangChainPipeline

    print("\nCreating FAISS Vector Store...")

    pipeline = LangChainPipeline()
    pipeline.create_vector_store(chunks)

    print("Vector Store Created Successfully!")