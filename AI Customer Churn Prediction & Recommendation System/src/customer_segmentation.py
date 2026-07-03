import os
import logging
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# =====================================================
# Configuration
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "dataset",
    "Processed",
    "customer_churn_cleaned.csv"
)

OUTPUT_FOLDER = os.path.join(
    BASE_DIR,
    "outputs"
)

REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "reports"
)

MODEL_FOLDER = os.path.join(
    BASE_DIR,
    "models"
)

SEGMENT_DATASET = os.path.join(
    OUTPUT_FOLDER,
    "customer_segments.csv"
)

ELBOW_CHART = os.path.join(
    REPORT_FOLDER,
    "elbow_method.png"
)

MODEL_FILE = os.path.join(
    MODEL_FOLDER,
    "kmeans_model.pkl"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def load_dataset():

    df = pd.read_csv(INPUT_FILE)

    logger.info("Dataset Loaded Successfully")

    return df


def prepare_features(df):

    X = df.drop("Churn", axis=1)

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    return X_scaled, df


def elbow_method(X):

    inertia = []

    for i in range(2,11):

        model = KMeans(
            n_clusters=i,
            random_state=42,
            n_init=10
        )

        model.fit(X)

        inertia.append(model.inertia_)

    plt.figure(figsize=(8,5))

    plt.plot(range(2,11), inertia, marker="o")

    plt.title("Elbow Method")

    plt.xlabel("Clusters")

    plt.ylabel("Inertia")

    plt.grid(True)

    os.makedirs(REPORT_FOLDER, exist_ok=True)

    plt.savefig(ELBOW_CHART)

    plt.close()

def train_kmeans(X, df):

    model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    df["CustomerSegment"] = model.fit_predict(X)

    return model, df


def segment_summary(df):

    summary = (
        df.groupby("CustomerSegment")
        .mean(numeric_only=True)
    )

    return summary


def save_outputs(model, df, summary):

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(REPORT_FOLDER, exist_ok=True)
    os.makedirs(MODEL_FOLDER, exist_ok=True)

    df.to_csv(
        SEGMENT_DATASET,
        index=False
    )

    summary.to_csv(
        os.path.join(
            REPORT_FOLDER,
            "segment_summary.csv"
        )
    )

    joblib.dump(
        model,
        MODEL_FILE
    )

    logger.info("Customer Segmentation Completed Successfully.")


def main():

    df = load_dataset()

    X, df = prepare_features(df)

    elbow_method(X)

    model, df = train_kmeans(X, df)

    summary = segment_summary(df)

    save_outputs(
        model,
        df,
        summary
    )

    print("\nCustomer Segmentation Completed Successfully.")

    print("\nGenerated Files")

    print("----------------------------")

    print("customer_segments.csv")

    print("segment_summary.csv")

    print("elbow_method.png")

    print("kmeans_model.pkl")


if __name__ == "__main__":
    main()