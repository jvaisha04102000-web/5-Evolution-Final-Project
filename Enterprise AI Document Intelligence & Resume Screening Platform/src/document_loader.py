from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict
from pypdf import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


@dataclass
class DocumentData:
    file_name: str
    file_path: str
    file_type: str
    text: str
    metadata: Dict


class DocumentLoader:
    """
    Enterprise Document Loader

    Supports:
    - PDF
    - DOCX
    - TXT
    """

    def __init__(self, data_directory: str):
        self.data_directory = Path(data_directory)

    def load_documents(self) -> List[DocumentData]:
        documents = []

        for file_path in self.data_directory.rglob("*"):

            if not file_path.is_file():
                continue

            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            try:
                text = self.extract_text(file_path)

                if not text.strip():
                    continue

                documents.append(
                    DocumentData(
                        file_name=file_path.name,
                        file_path=str(file_path),
                        file_type=file_path.suffix.lower(),
                        text=text,
                        metadata={
                            "parent_folder": file_path.parent.name,
                            "file_size_kb": round(file_path.stat().st_size / 1024, 2)
                        }
                    )
                )

            except Exception as e:
                print(f"Failed: {file_path.name} -> {e}")

        return documents

    def extract_text(self, file_path: Path) -> str:

        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            return self._read_pdf(file_path)

        elif suffix == ".docx":
            return self._read_docx(file_path)

        elif suffix == ".txt":
            return self._read_txt(file_path)

        return ""

    @staticmethod
    def _read_pdf(file_path: Path) -> str:
        reader = PdfReader(str(file_path))

        pages = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                pages.append(page_text)

        return "\n".join(pages)

    @staticmethod
    def _read_docx(file_path: Path) -> str:
        document = Document(str(file_path))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)

    @staticmethod
    def _read_txt(file_path: Path) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()


if __name__ == "__main__":

    loader = DocumentLoader("data/raw_docs")

    documents = loader.load_documents()

    print("=" * 60)
    print(f"Total Documents Loaded : {len(documents)}")
    print("=" * 60)

    for document in documents:
        print(document.file_name)
        print(document.metadata)
        print("-" * 60)