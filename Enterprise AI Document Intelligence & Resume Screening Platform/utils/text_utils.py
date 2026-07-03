import re


class TextUtils:
    """
    Enterprise Text Utility Functions
    """

    @staticmethod
    def remove_extra_spaces(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def remove_special_characters(text: str) -> str:
        return re.sub(r"[^\w\s.,!?@%:/()-]", "", text)

    @staticmethod
    def normalize_text(text: str) -> str:

        text = text.replace("\r", " ")
        text = text.replace("\n", " ")

        text = TextUtils.remove_special_characters(text)

        text = TextUtils.remove_extra_spaces(text)

        return text

    @staticmethod
    def remove_empty_lines(text: str) -> str:

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        return "\n".join(lines)

    @staticmethod
    def word_count(text: str) -> int:
        return len(text.split())

    @staticmethod
    def character_count(text: str) -> int:
        return len(text)

    @staticmethod
    def preview(text: str, length: int = 200) -> str:

        if len(text) <= length:
            return text

        return text[:length] + "..."

    @staticmethod
    def lowercase(text: str) -> str:
        return text.lower()