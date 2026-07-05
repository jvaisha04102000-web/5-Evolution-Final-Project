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
    "customer_clv_predictions.csv"
)

REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "reports"
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


def executive_summary(df):

    summary = {

        "Total Customers": len(df),

        "Predicted Churn Customers":
        int(df["PredictedChurn"].sum()),

        "High Risk Customers":
        len(df[df["RiskCategory"] == "High Risk"]),

        "Medium Risk Customers":
        len(df[df["RiskCategory"] == "Medium Risk"]),

        "Low Risk Customers":
        len(df[df["RiskCategory"] == "Low Risk"]),

        "Average CLV":
        round(df["PredictedCLV"].mean(), 2),

        "High Value Customers":
        len(df[df["CustomerValue"] == "High Value"])

    }

    return pd.DataFrame(
        summary.items(),
        columns=["Metric", "Value"]
    )


def churn_trend(df):

    trend = (
        df.groupby("RiskCategory")
        .size()
        .reset_index(name="CustomerCount")
    )

    return trend

def save_reports(summary, trend):

    os.makedirs(
        REPORT_FOLDER,
        exist_ok=True
    )

    summary.to_csv(

        os.path.join(
            REPORT_FOLDER,
            "executive_summary.csv"
        ),

        index=False

    )

    trend.to_csv(

        os.path.join(
            REPORT_FOLDER,
            "historical_vs_predicted_churn.csv"
        ),

        index=False

    )

    logger.info(
        "Business Reports Generated Successfully."
    )


def main():

    df = load_dataset()

    summary = executive_summary(df)

    trend = churn_trend(df)

    save_reports(summary, trend)

    print("\nBusiness Reports Generated Successfully.")

    print("\nGenerated Reports")

    print("-------------------------")

    print("executive_summary.csv")

    print("historical_vs_predicted_churn.csv")


if __name__ == "__main__":
    main()
    