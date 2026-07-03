import os
import csv
from datetime import datetime
from typing import List, Dict

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


class ReportGenerator:
    """
    Enterprise Business Report Generator

    Features
    --------
    ✔ Resume Screening Report
    ✔ Candidate Ranking Report
    ✔ AI Summary Export
    ✔ CSV Export
    ✔ PDF Export
    """

    def __init__(self,
                 output_directory="reports"):

        self.output_directory = output_directory

        os.makedirs(
            output_directory,
            exist_ok=True
        )

        self.styles = getSampleStyleSheet()

    def export_candidate_report(
            self,
            candidates: List[Dict]
    ):

        pdf_path = os.path.join(
            self.output_directory,
            "Candidate_Ranking_Report.pdf"
        )

        csv_path = os.path.join(
            self.output_directory,
            "Candidate_Ranking_Report.csv"
        )

        self._create_pdf(
            pdf_path,
            candidates
        )

        self._create_csv(
            csv_path,
            candidates
        )

        return {
            "pdf": pdf_path,
            "csv": csv_path
        }

    def export_summary_report(
            self,
            file_name: str,
            summary: str
    ):

        pdf_path = os.path.join(

            self.output_directory,

            f"{file_name}_Summary.pdf"

        )

        document = SimpleDocTemplate(pdf_path)

        story = []

        story.append(

            Paragraph(

                "<b>AI Generated Summary</b>",

                self.styles["Heading1"]

            )

        )

        story.append(Spacer(1, 12))

        story.append(

            Paragraph(

                summary,

                self.styles["BodyText"]

            )

        )

        document.build(story)

        return pdf_path

    def _create_pdf(
            self,
            pdf_path,
            candidates
    ):

        document = SimpleDocTemplate(pdf_path)

        story = []

        story.append(

            Paragraph(

                "Enterprise Resume Screening Report",

                self.styles["Heading1"]

            )

        )

        story.append(

            Paragraph(

                datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),

                self.styles["BodyText"]

            )

        )

        story.append(Spacer(1, 20))

        data = [[

            "Rank",

            "Candidate",

            "Score",

            "Experience"

        ]]

        for candidate in candidates:

            data.append([

                candidate["rank"],

                candidate["candidate_name"],

                f"{candidate['matching_score']}%",

                candidate["experience_years"]

            ])

        table = Table(data)

        table.setStyle(

            TableStyle([

                ("BACKGROUND",
                 (0, 0),
                 (-1, 0),
                 colors.grey),

                ("TEXTCOLOR",
                 (0, 0),
                 (-1, 0),
                 colors.whitesmoke),

                ("GRID",
                 (0, 0),
                 (-1, -1),
                 1,
                 colors.black),

                ("BACKGROUND",
                 (0, 1),
                 (-1, -1),
                 colors.beige)

            ])

        )

        story.append(table)

        document.build(story)

    def _create_csv(
            self,
            csv_path,
            candidates
    ):

        with open(
                csv_path,
                "w",
                newline="",
                encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([

                "Rank",

                "Candidate",

                "Score",

                "Experience"

            ])

            for candidate in candidates:

                writer.writerow([

                    candidate["rank"],

                    candidate["candidate_name"],

                    candidate["matching_score"],

                    candidate["experience_years"]

                ])


if __name__ == "__main__":

    sample = [

        {

            "rank": 1,

            "candidate_name": "Rahul",

            "matching_score": 94.5,

            "experience_years": 5

        },

        {

            "rank": 2,

            "candidate_name": "Priya",

            "matching_score": 91,

            "experience_years": 4

        }

    ]

    generator = ReportGenerator()

    files = generator.export_candidate_report(sample)

    print(files)

    summary = generator.export_summary_report(

        "Resume_01",

        "This candidate is highly suitable for the role."

    )

    print(summary)