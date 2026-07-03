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
    "retention_recommendations.csv"
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

    logger.info("Dataset Loaded Successfully.")

    return df


def calculate_clv(df):

    if "MonthlyCharges" not in df.columns:
        raise ValueError("MonthlyCharges column not found.")

    if "tenure" not in df.columns:
        raise ValueError("tenure column not found.")

    df["PredictedCLV"] = (
        df["MonthlyCharges"] *
        df["tenure"] * 1.2
    )

    return df

def categorize_clv(df):

    def category(value):

        if value >= 5000:
            return "High Value"

        elif value >= 2000:
            return "Medium Value"

        return "Low Value"

    df["CustomerValue"] = df["PredictedCLV"].apply(category)

    return df


def save_dataset(df):

    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )

    output = os.path.join(
        OUTPUT_FOLDER,
        "customer_clv_predictions.csv"
    )

    df.to_csv(
        output,
        index=False
    )

    logger.info("CLV Prediction Completed Successfully.")

    print(
        df[
            [
                "PredictedCLV",
                "CustomerValue"
            ]
        ].head()
    )


def main():

    df = load_dataset()

    df = calculate_clv(df)

    df = categorize_clv(df)

    save_dataset(df)


if __name__ == "__main__":
    main()