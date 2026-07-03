import os
import logging
import pandas as pd

# =====================================================
# Configuration
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "dataset",
    "Processed",
    "customer_churn_raw_copy.csv"
)

OUTPUT_FOLDER = os.path.join(
    BASE_DIR,
    "dataset",
    "Processed"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_FOLDER,
    "customer_churn_feature_engineered.csv"
)

REPORT_FILE = os.path.join(
    BASE_DIR,
    "reports",
    "feature_engineering_report.csv"
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


def create_tenure_group(df):

    bins = [0,12,24,48,72]

    labels = [
        "0-1 Year",
        "1-2 Years",
        "2-4 Years",
        "4-6 Years"
    ]

    df["TenureGroup"] = pd.cut(
        df["tenure"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    return df


def create_total_services(df):

    service_columns = [
        "PhoneService",
        "MultipleLines",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]

    df["TotalServices"] = (
        df[service_columns] == "Yes"
    ).sum(axis=1)

    return df


def create_average_monthly_spending(df):

    df["AvgMonthlySpend"] = (
        df["TotalCharges"] /
        (df["tenure"] + 1)
    )

    return df


def create_contract_risk(df):

    risk_map = {
        "Month-to-month":"High",
        "One year":"Medium",
        "Two year":"Low"
    }

    df["ContractRisk"] = (
        df["Contract"]
        .map(risk_map)
    )

    return df


def create_family_size(df):

    df["FamilySize"] = (
        (df["Partner"]=="Yes").astype(int) +
        (df["Dependents"]=="Yes").astype(int)
    )

    return df


def create_senior_flag(df):

    df["SeniorFlag"] = (
        df["SeniorCitizen"]
    )

    return df

def create_clv_feature(df):

    df["EstimatedCLV"] = (
        df["MonthlyCharges"] *
        df["tenure"]
    )

    return df


def create_payment_risk(df):

    df["PaymentRisk"] = df["PaymentMethod"].apply(
        lambda x: "High"
        if x == "Electronic check"
        else "Low"
    )

    return df


def create_report(df):

    report = pd.DataFrame({
        "Feature": df.columns,
        "DataType": df.dtypes.astype(str),
        "MissingValues": df.isnull().sum().values
    })

    os.makedirs(
        os.path.dirname(REPORT_FILE),
        exist_ok=True
    )

    report.to_csv(
        REPORT_FILE,
        index=False
    )


def save_dataset(df):

    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    logger.info(
        "Feature Engineered Dataset Saved Successfully."
    )


def main():

    df = load_dataset()

    df = clean_total_charges(df)

    df = create_tenure_group(df)

    df = create_total_services(df)

    df = create_average_monthly_spending(df)

    df = create_contract_risk(df)

    df = create_family_size(df)

    df = create_senior_flag(df)

    df = create_clv_feature(df)

    df = create_payment_risk(df)

    save_dataset(df)

    create_report(df)

    print("\nFeature Engineering Completed Successfully.")

    print("\nNew Features Created:")

    print("--------------------------------")

    print("TenureGroup")

    print("TotalServices")

    print("AvgMonthlySpend")

    print("ContractRisk")

    print("FamilySize")

    print("SeniorFlag")

    print("EstimatedCLV")

    print("PaymentRisk")


if __name__ == "__main__":
    main()