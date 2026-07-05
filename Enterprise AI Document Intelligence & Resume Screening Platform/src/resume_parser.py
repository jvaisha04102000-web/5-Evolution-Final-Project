import re
from typing import Dict, List

from src.document_loader import DocumentData


class ResumeParser:
    """
    Enterprise Resume Parser

    Features
    --------
    ✔ Skill Extraction
    ✔ Education Extraction
    ✔ Experience Extraction
    ✔ Candidate Name Extraction
    ✔ Email Extraction
    ✔ Phone Extraction
    """

    SKILLS = {
        "python", "java", "sql", "excel", "power bi",
        "machine learning", "deep learning", "nlp",
        "pandas", "numpy", "scikit-learn",
        "tensorflow", "pytorch",
        "flask", "django",
        "aws", "azure", "docker",
        "git", "linux", "mysql",
        "postgresql", "mongodb",
        "tableau", "spark", "hadoop",
        "rest api", "microservices"
    }

    EDUCATION = [
        "b.tech", "b.e", "b.sc", "bca",
        "m.tech", "m.e", "m.sc", "mca",
        "mba", "phd"
    ]

    EXPERIENCE_PATTERN = r"(\d+)\+?\s*(?:years|year)"

    EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    PHONE_PATTERN = r"(\+91[- ]?)?[6-9]\d{9}"

    def parse_resume(self, document: DocumentData) -> Dict:

        text = document.text.lower()

        return {
            "file_name": document.file_name,
            "candidate_name": self.extract_name(document.text),
            "email": self.extract_email(document.text),
            "phone": self.extract_phone(document.text),
            "skills": self.extract_skills(text),
            "education": self.extract_education(text),
            "experience_years": self.extract_experience(text)
        }

    def extract_name(self, text: str) -> str:

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if not lines:
            return "Unknown"

        first_line = lines[0]

        # Email iruntha athukku munnadi irukkara text mattum edukkum
        first_line = first_line.split("@")[0]

        # Phone number remove pannum
        first_line = re.sub(r"\+?\d[\d\s-]{8,}", "", first_line)

        # Maximum first 2 words name-nu assume pannuvom
        words = first_line.split()

        return " ".join(words[:2])

    def extract_email(self, text: str):

        match = re.search(self.EMAIL_PATTERN, text)

        return match.group() if match else ""

    def extract_phone(self, text: str):

        match = re.search(self.PHONE_PATTERN, text)

        return match.group() if match else ""

    def extract_skills(self, text: str) -> List[str]:

        skills = []

        for skill in self.SKILLS:

            if skill in text:
                skills.append(skill.title())

        return sorted(list(set(skills)))

    def extract_education(self, text: str):

        education = []

        for degree in self.EDUCATION:

            if degree in text:
                education.append(degree.upper())

        return education

    def extract_experience(self, text: str):

        match = re.search(
            self.EXPERIENCE_PATTERN,
            text
        )

        if match:
            return int(match.group(1))

        return 0


if __name__ == "__main__":

    from src.document_loader import DocumentLoader
    from src.text_extractor import TextExtractor

    loader = DocumentLoader("data/raw_docs/resumes")

    documents = loader.load_documents()

    extractor = TextExtractor()

    documents = extractor.clean_documents(documents)

    parser = ResumeParser()

    print("=" * 70)

    for document in documents:

        parsed = parser.parse_resume(document)

        print(parsed)

        print("-" * 70)