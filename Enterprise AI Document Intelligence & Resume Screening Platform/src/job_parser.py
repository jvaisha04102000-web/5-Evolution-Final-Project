import re
from typing import Dict, List
from document_loader import DocumentData


class JobDescriptionParser:
    """
    Enterprise Job Description Parser

    Features
    --------
    ✔ Job Title Extraction
    ✔ Skills Extraction
    ✔ Experience Extraction
    ✔ Education Extraction
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

    def parse_job_description(
        self,
        document: DocumentData
    ) -> Dict:

        text = document.text.lower()

        return {

            "job_title": self.extract_job_title(document.text),

            "skills": self.extract_skills(text),

            "education": self.extract_education(text),

            "experience_years": self.extract_experience(text)

        }

    def extract_job_title(self, text):

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        return lines[0] if lines else "Unknown"

    def extract_skills(self, text) -> List[str]:

        skills = []

        for skill in self.SKILLS:

            if skill in text:
                skills.append(skill.title())

        return sorted(set(skills))

    def extract_education(self, text):

        education = []

        for degree in self.EDUCATION:

            if degree in text:
                education.append(degree.upper())

        return education

    def extract_experience(self, text):

        match = re.search(
            self.EXPERIENCE_PATTERN,
            text
        )

        if match:
            return int(match.group(1))

        return 0