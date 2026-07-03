import os
import joblib
import logging
import pandas as pd

from sklearn.model_selection import GridSearchCV
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

MODEL_FOLDER = os.path.join(BASE_DIR, "models")

REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def load_data():

    train = pd.read_csv(TRAIN_FILE)

    X = train.drop("Churn", axis=1)

    y = train["Churn"]

    return X, y


def get_models():

    return {

        "LogisticRegression": (

            LogisticRegression(max_iter=1000),

            {
                "C": [0.01, 0.1, 1, 10]
            }

        ),

        "DecisionTree": (

            DecisionTreeClassifier(random_state=42),

            {
                "max_depth": [3,5,10,None],
                "min_samples_split":[2,5,10]
            }

        ),

        "RandomForest": (

            RandomForestClassifier(random_state=42),

            {
                "n_estimators":[100,200],
                "max_depth":[5,10,None]
            }

        ),

        "GradientBoosting": (

            GradientBoostingClassifier(random_state=42),

            {
                "learning_rate":[0.01,0.1],
                "n_estimators":[100,200]
            }

        )

    }

def tune_models(X, y):

    os.makedirs(MODEL_FOLDER, exist_ok=True)

    os.makedirs(REPORT_FOLDER, exist_ok=True)

    results = []

    models = get_models()

    for name, (model, params) in models.items():

        grid = GridSearchCV(

            estimator=model,

            param_grid=params,

            cv=5,

            scoring="accuracy",

            n_jobs=-1

        )

        grid.fit(X, y)

        best_model = grid.best_estimator_

        joblib.dump(

            best_model,

            os.path.join(

                MODEL_FOLDER,

                f"Best_{name}.pkl"

            )

        )

        results.append({

            "Model": name,

            "Best Score": grid.best_score_,

            "Best Parameters": grid.best_params_

        })

        logger.info(f"{name} Tuned Successfully")

    report = pd.DataFrame(results)

    report.to_csv(

        os.path.join(

            REPORT_FOLDER,

            "hyperparameter_tuning_report.csv"

        ),

        index=False

    )

    print(report)


def main():

    X, y = load_data()

    tune_models(X, y)


if __name__ == "__main__":

    main()