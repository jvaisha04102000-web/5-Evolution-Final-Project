import os
import logging
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# ======================================================
# Configuration
# ======================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "dataset",
    "Processed",
    "customer_churn_feature_engineered.csv"
)

PROCESSED_FOLDER = os.path.join(BASE_DIR, "dataset", "Processed")
MODELS_FOLDER = os.path.join(BASE_DIR, "models")

CLEANED_DATASET = os.path.join(
    PROCESSED_FOLDER,
    "customer_churn_cleaned.csv"
)

TRAIN_DATA = os.path.join(
    PROCESSED_FOLDER,
    "train_dataset.csv"
)

TEST_DATA = os.path.join(
    PROCESSED_FOLDER,
    "test_dataset.csv"
)

SCALER_FILE = os.path.join(
    MODELS_FOLDER,
    "scaler.pkl"
)

ENCODER_FILE = os.path.join(
    MODELS_FOLDER,
    "label_encoders.pkl"
)

# ======================================================
# Logging
# ======================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def load_dataset():
    df = pd.read_csv(INPUT_FILE)
    logger.info("Dataset Loaded Successfully.")
    return df


def clean_total_charges(df):

    df["TotalCharges"] = df["TotalCharges"].replace(" ", pd.NA)

    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )

    df["TotalCharges"] = df["TotalCharges"].fillna(
        df["TotalCharges"].median()
    )

    return df


def drop_unwanted_columns(df):

    if "customerID" in df.columns:
        df.drop(columns=["customerID"], inplace=True)

    return df


def encode_target(df):

    target_encoder = LabelEncoder()

    df["Churn"] = target_encoder.fit_transform(df["Churn"])

    return df, target_encoder


def encode_categorical(df):

    encoders = {}

    categorical_columns = df.select_dtypes(
        include="object"
    ).columns

    for column in categorical_columns:

        encoder = LabelEncoder()

        df[column] = encoder.fit_transform(df[column])

        encoders[column] = encoder

    return df, encoders


def scale_features(df):

    X = df.drop("Churn", axis=1)

    y = df["Churn"]

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    X = pd.DataFrame(
        X_scaled,
        columns=X.columns
    )

    return X, y, scaler


def split_dataset(X, y):

    return train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )


def save_outputs(
    df,
    X_train,
    X_test,
    y_train,
    y_test,
    scaler,
    encoders
):

    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    os.makedirs(MODELS_FOLDER, exist_ok=True)

    df.to_csv(
        CLEANED_DATASET,
        index=False
    )

    train_df = X_train.copy()
    train_df["Churn"] = y_train.values

    train_df.to_csv(
        TRAIN_DATA,
        index=False
    )

    test_df = X_test.copy()
    test_df["Churn"] = y_test.values

    test_df.to_csv(
        TEST_DATA,
        index=False
    )

    joblib.dump(
        scaler,
        SCALER_FILE
    )

    joblib.dump(
        encoders,
        ENCODER_FILE
    )

    logger.info("All processed files saved successfully.")


def main():

    df = load_dataset()

    df = clean_total_charges(df)

    df = drop_unwanted_columns(df)

    df, target_encoder = encode_target(df)

    df, encoders = encode_categorical(df)

    X, y, scaler = scale_features(df)

    X_train, X_test, y_train, y_test = split_dataset(
        X,
        y
    )

    encoders["Target"] = target_encoder

    save_outputs(
        df,
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
        encoders
    )

    print("\nData Preprocessing Completed Successfully.")


if __name__ == "__main__":
    main()