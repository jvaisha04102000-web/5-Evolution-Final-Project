import os
import logging
import pandas as pd

# =====================================================
# Configuration
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "outputs",
    "churn_predictions.csv"
)

OUTPUT_FOLDER = os.path.join(
    BASE_DIR,
    "outputs"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def load_dataset():

    df = pd.read_csv(INPUT_FILE)

    logger.info("Prediction file loaded successfully.")

    return df


def recommend_action(row):

    if row["RiskCategory"] == "High Risk":

        return (
            "Immediate Call, Loyalty Discount, "
            "Premium Support, Personal Follow-up"
        )

    elif row["RiskCategory"] == "Medium Risk":

        return (
            "Offer Discount, Email Campaign, "
            "Service Upgrade"
        )

    return (
        "Regular Engagement, Rewards Program"
    )

def generate_recommendations(df):

    df["RetentionStrategy"] = df.apply(
        recommend_action,
        axis=1
    )

    output = os.path.join(
        OUTPUT_FOLDER,
        "retention_recommendations.csv"
    )

    df.to_csv(
        output,
        index=False
    )

    logger.info(
        "Retention recommendations generated."
    )

    print(
        df[
            [
                "RiskCategory",
                "RetentionStrategy"
            ]
        ].head()
    )


def main():

    df = load_dataset()

    generate_recommendations(df)


if __name__ == "__main__":
    main()