import os
import logging
import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

# =====================================================
# Configuration
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRAIN_FILE = os.path.join(
    BASE_DIR,
    "dataset",
    "Processed",
    "train_dataset.csv"
)

TEST_FILE = os.path.join(
    BASE_DIR,
    "dataset",
    "Processed",
    "test_dataset.csv"
)

MODEL_FOLDER = os.path.join(
    BASE_DIR,
    "models"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def load_data():

    train = pd.read_csv(TRAIN_FILE)
    test = pd.read_csv(TEST_FILE)

    X_train = train.drop("Churn", axis=1)
    y_train = train["Churn"]

    X_test = test.drop("Churn", axis=1)
    y_test = test["Churn"]

    return X_train, X_test, y_train, y_test


def build_models():

    models = {

        "LogisticRegression":
        LogisticRegression(max_iter=1000),

        "DecisionTree":
        DecisionTreeClassifier(random_state=42),

        "RandomForest":
        RandomForestClassifier(
            random_state=42
        ),

        "GradientBoosting":
        GradientBoostingClassifier(
            random_state=42
        )

    }

    return models

def train_models(models, X_train, y_train):

    trained_models = {}

    os.makedirs(MODEL_FOLDER, exist_ok=True)

    for name, model in models.items():

        model.fit(X_train, y_train)

        trained_models[name] = model

        joblib.dump(
            model,
            os.path.join(
                MODEL_FOLDER,
                f"{name}.pkl"
            )
        )

        logger.info(f"{name} trained successfully.")

    return trained_models


def main():

    X_train, X_test, y_train, y_test = load_data()

    models = build_models()

    train_models(
        models,
        X_train,
        y_train
    )

    print("\nModel Training Completed Successfully.")

    print("\nModels Saved:")

    print("--------------------------")

    print("LogisticRegression.pkl")

    print("DecisionTree.pkl")

    print("RandomForest.pkl")

    print("GradientBoosting.pkl")


if __name__ == "__main__":
    main()