import os
import logging
import pandas as pd

# ==============================
# Configuration
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "Raw",
    "WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

PROCESSED_FOLDER = os.path.join(
    BASE_DIR,
    "dataset",
    "Processed"
)

PROCESSED_FILE = os.path.join(
    PROCESSED_FOLDER,
    "customer_churn_raw_copy.csv"
)
# ==============================
# Logging Configuration
# ==============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def load_dataset(file_path):
    """
    Load customer churn dataset.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    df = pd.read_csv(file_path)

    logger.info("Dataset loaded successfully.")
    return df


def dataset_summary(df):
    """
    Display dataset summary.
    """

    print("\n" + "=" * 60)
    print("DATASET SHAPE")
    print("=" * 60)
    print(df.shape)

    print("\n" + "=" * 60)
    print("FIRST 5 ROWS")
    print("=" * 60)
    print(df.head())

    print("\n" + "=" * 60)
    print("COLUMN NAMES")
    print("=" * 60)
    print(df.columns.tolist())

    print("\n" + "=" * 60)
    print("DATA TYPES")
    print("=" * 60)
    print(df.dtypes)

    print("\n" + "=" * 60)
    print("MISSING VALUES")
    print("=" * 60)
    print(df.isnull().sum())

    print("\n" + "=" * 60)
    print("DUPLICATE ROWS")
    print("=" * 60)
    print(df.duplicated().sum())

    print("\n" + "=" * 60)
    print("STATISTICAL SUMMARY")
    print("=" * 60)
    print(df.describe(include="all"))


def save_processed_copy(df):
    """
    Save a copy into processed folder.
    """
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)

    df.to_csv(PROCESSED_FILE, index=False)

    logger.info(f"Dataset copy saved to: {PROCESSED_FILE}")


def main():

    try:
        df = load_dataset(RAW_DATA_PATH)

        dataset_summary(df)

        save_processed_copy(df)

        print("\nDataset loading completed successfully.")

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()