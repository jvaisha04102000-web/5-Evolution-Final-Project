import numpy as np

from sklearn.metrics.pairwise import cosine_similarity


class SimilarityUtils:
    """
    Enterprise Similarity Utility Functions
    """

    @staticmethod
    def cosine_similarity_score(
        embedding1,
        embedding2
    ) -> float:

        embedding1 = np.array(
            embedding1
        ).reshape(1, -1)

        embedding2 = np.array(
            embedding2
        ).reshape(1, -1)

        return float(

            cosine_similarity(
                embedding1,
                embedding2
            )[0][0]

        )

    @staticmethod
    def similarity_matrix(
        embeddings
    ):

        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        return cosine_similarity(
            embeddings
        )

    @staticmethod
    def is_duplicate(
        score: float,
        threshold: float = 0.95
    ) -> bool:

        return score >= threshold

    @staticmethod
    def is_similar(
        score: float,
        threshold: float = 0.85
    ) -> bool:

        return score >= threshold

    @staticmethod
    def percentage(score: float):

        return round(
            score * 100,
            2
        )