from typing import List, Dict

from src.document_loader import DocumentData


class DocumentClassifier:
    """
    Enterprise Document Classifier

    Categories
    ----------
    ✔ Resume
    ✔ Job Description
    ✔ HR Document
    ✔ Company Policy
    ✔ Other
    """

    CATEGORY_KEYWORDS = {

        "Resume": [
            "skills",
            "education",
            "experience",
            "certification",
            "project",
            "linkedin",
            "resume"
        ],

        "Job Description": [
            "responsibilities",
            "requirements",
            "preferred skills",
            "salary",
            "job title",
            "experience required"
        ],

        "HR Document": [
            "leave policy",
            "employee handbook",
            "working hours",
            "attendance",
            "holiday"
        ],

        "Company Policy": [
            "code of conduct",
            "security policy",
            "privacy policy",
            "confidentiality",
            "compliance",
            "acceptable use"
        ]

    }

    def classify_document(
        self,
        document: DocumentData
    ) -> Dict:

        text = document.text.lower()

        scores = {}

        for category, keywords in self.CATEGORY_KEYWORDS.items():

            score = 0

            for keyword in keywords:

                if keyword.lower() in text:
                    score += 1

            scores[category] = score

        category = max(
            scores,
            key=scores.get
        )

        if scores[category] == 0:
            category = "Other"

        return {

            "file_name": document.file_name,

            "category": category,

            "confidence": round(

                (
                    scores.get(category, 0)
                    /
                    max(
                        len(
                            self.CATEGORY_KEYWORDS.get(
                                category,
                                [1]
                            )
                        ),
                        1
                    )

                ) * 100,

                2

            )

        }

    def classify_documents(
        self,
        documents: List[DocumentData]
    ) -> List[Dict]:

        return [

            self.classify_document(document)

            for document in documents

        ]


if __name__ == "__main__":

    from src.document_loader import DocumentLoader
    from src.text_extractor import TextExtractor

    loader = DocumentLoader(
        "data/raw_docs"
    )

    extractor = TextExtractor()

    docs = extractor.clean_documents(

        loader.load_documents()

    )

    classifier = DocumentClassifier()

    results = classifier.classify_documents(
        docs
    )

    print("=" * 70)

    for result in results:

        print(result)

        print("-" * 70)