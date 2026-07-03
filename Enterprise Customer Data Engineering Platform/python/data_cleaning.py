# ==========================================================
# Project 2 : Enterprise Customer Data Engineering Platform
# File Name : 02_data_cleaning.py
# Purpose   : Validate and Clean Customer Dataset
# ==========================================================

import pandas as pd
from datetime import datetime


# -----------------------------
# Project Logger
# -----------------------------
def write_log(message):

    with open("../Output/Project_Log.txt", "a") as file:

        file.write(
            f"{datetime.now()} : {message}\n"
        )


# -----------------------------
# Validate Incoming Records
# -----------------------------
def validate_records(df):

    required_columns = [
        "Customer_ID",
        "Customer_Name",
        "Age",
        "Email",
        "Phone",
        "Purchase_Amount"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        print("\nMissing Required Columns :", missing_columns)
    else:
        print("\nAll Required Columns Available")

    before = len(df)

    df = df.dropna(subset=required_columns)

    after = len(df)

    print("Invalid Records Removed :", before - after)

    return df


# -----------------------------
# Remove Duplicate Records
# -----------------------------
def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    print("Duplicate Records Removed :", before - after)

    return df


# -----------------------------
# Handle Missing Values
# -----------------------------
def handle_missing_values(df):

    df["Email"] = df["Email"].fillna("Not Available")

    df["Phone"] = df["Phone"].fillna("Not Available")

    df["Address"] = df["Address"].fillna("Not Available")

    print("Missing Values Handled")

    return df


# -----------------------------
# Standardize Customer Names
# -----------------------------
def standardize_names(df):

    df["Customer_Name"] = df["Customer_Name"].str.title()

    print("Customer Names Standardized")

    return df


# -----------------------------
# Validate Email
# -----------------------------
def validate_email(df):

    invalid = ~df["Email"].astype(str).str.contains("@", na=False)

    print("Invalid Emails Found :", invalid.sum())

    return df


# -----------------------------
# Validate Phone Number
# -----------------------------
def validate_phone(df):

    invalid = df["Phone"].astype(str).str.len() < 10

    print("Invalid Phone Numbers :", invalid.sum())

    return df


# -----------------------------
# Generate Data Quality Report
# -----------------------------
def generate_data_quality_report(df):

    report = pd.DataFrame({

        "Metric": [
            "Total Records",
            "Duplicate Records",
            "Missing Emails",
            "Missing Phones",
            "Invalid Emails",
            "Invalid Phone Numbers"
        ],

        "Count": [

            len(df),

            df.duplicated().sum(),

            df["Email"].isnull().sum(),

            df["Phone"].isnull().sum(),

            (~df["Email"].astype(str).str.contains("@")).sum(),

            (df["Phone"].astype(str).str.len() < 10).sum()

        ]

    })

    report.to_csv(
        "../Output/Data_Quality_Report.csv",
        index=False
    )

    print("Data Quality Report Generated Successfully")

    return 

# -----------------------------
# Validation Report
# -----------------------------
def generate_validation_report(df):

    report = pd.DataFrame({

        "Validation": [
            "Total Records",
            "Valid Records",
            "Invalid Emails",
            "Invalid Phones"
        ],

        "Count": [

            len(df),

            len(df),

            (~df["Email"].astype(str).str.contains("@")).sum(),

            (df["Phone"].astype(str).str.len() < 10).sum()

        ]

    })

    report.to_csv(
        "../Output/Validation_Report.csv",
        index=False
    )

    print("Validation Report Generated Successfully")
    
    return

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    df = pd.read_csv("../Output/Merged_Customer_Dataset.csv")

    print("\nOriginal Records :", len(df))

    df = validate_records(df)
    write_log("Validation Completed")

    df = remove_duplicates(df)
    write_log("Duplicate Removal Completed")

    df = handle_missing_values(df)
    write_log("Missing Values Handled")

    df = standardize_names(df)
    write_log("Customer Name Standardization Completed")

    df = validate_email(df)
    write_log("Email Validation Completed")

    df = validate_phone(df)
    write_log("Phone Validation Completed")

    generate_data_quality_report(df)
    write_log("Data Quality Report Generated")

    generate_validation_report(df)
    write_log("Validation Report Generated")

    output_path = "../Output/Cleaned_Customer_Dataset.csv"

    df.to_csv(output_path, index=False)
    write_log("Cleaned Dataset Saved")

    print("\nCleaned Dataset Saved Successfully")
    print("Location :", output_path)

    print("\nCleaning Completed Successfully")
    print(df.head())

   