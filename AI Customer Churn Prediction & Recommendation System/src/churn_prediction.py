import os
import joblib
import logging
import pandas as pd

# =====================================================
# Configuration
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEST_FILE = os.path.join(
    BASE_DIR,
    "dataset",
    "Processed",
    "test_dataset.csv"
)

MODEL_FILE = os.path.join(
    BASE_DIR,
    "models",
    "Best_RandomForest.pkl"
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


def load_resources():

    df = pd.read_csv(TEST_FILE)

    model = joblib.load(MODEL_FILE)

    X = df.drop("Churn", axis=1)

    y = df["Churn"]

    return df, X, y, model

def classify_risk(probability):

    if probability >= 0.70:
        return "High Risk"

    elif probability >= 0.40:
        return "Medium Risk"

    return "Low Risk"


def predict(df, X, model):

    probabilities = model.predict_proba(X)[:, 1]

    predictions = model.predict(X)

    df["PredictedChurn"] = predictions

    df["ChurnProbability"] = probabilities

    df["RiskCategory"] = df["ChurnProbability"].apply(
        classify_risk
    )

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    output = os.path.join(
        OUTPUT_FOLDER,
        "churn_predictions.csv"
    )

    df.to_csv(output, index=False)

    logger.info("Prediction completed successfully.")

    print(df[
        [
            "PredictedChurn",
            "ChurnProbability",
            "RiskCategory"
        ]
    ].head())


def main():

    df, X, y, model = load_resources()

    predict(
        df,
        X,
        model
    )


if __name__ == "__main__":
    main()