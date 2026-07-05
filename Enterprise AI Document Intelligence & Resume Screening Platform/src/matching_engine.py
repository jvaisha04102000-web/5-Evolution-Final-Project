from typing import Dict, List

from src.resume_parser import ResumeParser
from src.job_parser import JobDescriptionParser
from src.document_loader import DocumentData

class ResumeMatchingEngine:
    """
    Enterprise Resume Matching Engine

    Features
    --------
    ✔ Resume Screening
    ✔ Resume-Job Matching Score
    ✔ Candidate Ranking
    ✔ Skill Matching
    ✔ Experience Matching
    """

    def __init__(self):

        self.resume_parser = ResumeParser()
        self.job_parser = JobDescriptionParser()

    def rank_candidates(
        self,
        resumes: List[DocumentData],
        job_description: DocumentData
    ) -> List[Dict]:

        jd = self.job_parser.parse_job_description(job_description)

        ranked_candidates = []

        for resume in resumes:

            parsed_resume = self.resume_parser.parse_resume(resume)

            result = self.calculate_match_score(
                parsed_resume,
                jd
            )

            ranked_candidates.append(result)

        ranked_candidates.sort(
            key=lambda x: x["matching_score"],
            reverse=True
        )

        for rank, candidate in enumerate(
                ranked_candidates,
                start=1):

            candidate["rank"] = rank

        return ranked_candidates

    def calculate_match_score(
        self,
        resume: Dict,
        job: Dict
    ) -> Dict:

        resume_skills = {
            skill.lower()
            for skill in resume["skills"]
        }

        job_skills = {
            skill.lower()
            for skill in job["skills"]
        }

        matched_skills = sorted(
            resume_skills.intersection(job_skills)
        )

        missing_skills = sorted(
            job_skills.difference(resume_skills)
        )

        if len(job_skills) == 0:
            skill_score = 0
        else:
            skill_score = (
                len(matched_skills)
                / len(job_skills)
            ) * 100

        experience_score = min(
            resume["experience_years"] * 10,
            100
        )

        final_score = round(
            (skill_score * 0.8) +
            (experience_score * 0.2),
            2
        )

        return {

            "candidate_name":
                resume["candidate_name"],

            "email":
                resume["email"],

            "phone":
                resume["phone"],

            "matching_score":
                final_score,

            "matched_skills":
                matched_skills,

            "missing_skills":
                missing_skills,

            "experience_years":
                resume["experience_years"]

        }


if __name__ == "__main__":

    from src.document_loader import DocumentLoader
    from src.text_extractor import TextExtractor

    resume_loader = DocumentLoader(
        "data/raw_docs/resumes"
    )

    jd_loader = DocumentLoader(
        "data/raw_docs/job_descriptions"
    )

    extractor = TextExtractor()

    resumes = extractor.clean_documents(
        resume_loader.load_documents()
    )

    job = extractor.clean_documents(
        jd_loader.load_documents()
    )[0]

    matcher = ResumeMatchingEngine()

    results = matcher.rank_candidates(
        resumes,
        job
    )

    print("=" * 80)

    print("Candidate Ranking")

    print("=" * 80)

    for candidate in results:

        print(
            f"Rank : {candidate['rank']}"
        )

        print(
            f"Candidate : {candidate['candidate_name']}"
        )

        print(
            f"Score : {candidate['matching_score']}"
        )

        print(
            f"Matched Skills : "
            f"{', '.join(candidate['matched_skills'])}"
        )

        print(
            f"Missing Skills : "
            f"{', '.join(candidate['missing_skills'])}"
        )

        print("-" * 80)