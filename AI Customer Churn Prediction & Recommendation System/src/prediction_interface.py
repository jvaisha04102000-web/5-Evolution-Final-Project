import os
import joblib
import pandas as pd

# ==========================================
# Configuration
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_FILE = os.path.join(
    BASE_DIR,
    "models",
    "Best_RandomForest.pkl"
)

SCALER_FILE = os.path.join(
    BASE_DIR,
    "models",
    "scaler.pkl"
)

ENCODER_FILE = os.path.join(
    BASE_DIR,
    "models",
    "label_encoders.pkl"
)

OUTPUT_FOLDER = os.path.join(
    BASE_DIR,
    "outputs"
)


def load_resources():

    model = joblib.load(MODEL_FILE)

    scaler = joblib.load(SCALER_FILE)

    encoders = joblib.load(ENCODER_FILE)

    return model, scaler, encoders


def preprocess_input(data, scaler):

    df = pd.DataFrame([data])

    df = scaler.transform(df)

    return df

def predict_customer(data):

    model, scaler, encoders = load_resources()

    processed = preprocess_input(data, scaler)

    prediction = model.predict(processed)[0]

    probability = model.predict_proba(processed)[0][1]

    if probability >= 0.70:
        risk = "High Risk"

    elif probability >= 0.40:
        risk = "Medium Risk"

    else:
        risk = "Low Risk"

    print("\nPrediction Result")

    print("-------------------------")

    print(f"Predicted Churn : {prediction}")

    print(f"Probability     : {probability:.2%}")

    print(f"Risk Category   : {risk}")


if __name__ == "__main__":

    sample_customer = {

        "gender":1,
        "SeniorCitizen":0,
        "Partner":1,
        "Dependents":0,
        "tenure":24,
        "PhoneService":1,
        "MultipleLines":1,
        "InternetService":1,
        "OnlineSecurity":0,
        "OnlineBackup":1,
        "DeviceProtection":1,
        "TechSupport":0,
        "StreamingTV":1,
        "StreamingMovies":1,
        "Contract":0,
        "PaperlessBilling":1,
        "PaymentMethod":2,
        "MonthlyCharges":75.50,
        "TotalCharges":1812.00,
        "TenureGroup":2,
        "TotalServices":6,
        "AvgMonthlySpend":75.50,
        "ContractRisk":1,
        "FamilySize":1,
        "SeniorFlag":0,
        "EstimatedCLV":1812,
        "PaymentRisk":0

    }

    predict_customer(sample_customer)