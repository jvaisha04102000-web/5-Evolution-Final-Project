import os
import joblib
import logging
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEST_FILE = os.path.join(
    BASE_DIR,
    "dataset",
    "Processed",
    "test_dataset.csv"
)

MODEL_FOLDER = os.path.join(BASE_DIR, "models")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def load_test_data():

    test = pd.read_csv(TEST_FILE)

    X_test = test.drop("Churn", axis=1)

    y_test = test["Churn"]

    return X_test, y_test


def load_models():

    models = {}

    files = [
        "LogisticRegression.pkl",
        "DecisionTree.pkl",
        "RandomForest.pkl",
        "GradientBoosting.pkl"
    ]

    for file in files:

        name = file.replace(".pkl", "")

        models[name] = joblib.load(
            os.path.join(MODEL_FOLDER, file)
        )

    return models

def evaluate_models(models, X_test, y_test):

    results = []

    os.makedirs(REPORT_FOLDER, exist_ok=True)

    for name, model in models.items():

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)

        precision = precision_score(y_test, y_pred)

        recall = recall_score(y_test, y_pred)

        f1 = f1_score(y_test, y_pred)

        roc = roc_auc_score(y_test, y_pred)

        results.append({

            "Model": name,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1,
            "ROC AUC": roc

        })

        cm = confusion_matrix(y_test, y_pred)

        disp = ConfusionMatrixDisplay(cm)

        disp.plot()

        plt.savefig(
            os.path.join(
                REPORT_FOLDER,
                f"{name}_confusion_matrix.png"
            )
        )

        plt.close()

    report = pd.DataFrame(results)

    report.to_csv(

        os.path.join(
            REPORT_FOLDER,
            "model_performance_report.csv"
        ),

        index=False

    )

    print(report)

    logger.info("Evaluation Completed Successfully.")


def main():

    X_test, y_test = load_test_data()

    models = load_models()

    evaluate_models(

        models,

        X_test,

        y_test

    )


if __name__ == "__main__":

    main()