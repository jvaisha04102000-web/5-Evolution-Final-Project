# ==========================================
# Project 2 - Enterprise Customer Data Engineering Platform
# File Name : 01_load_data.py
# Purpose   : Load CSV, Excel, JSON and API data
# ==========================================

import pandas as pd
import requests


# -------------------------------
# Load CSV File
# -------------------------------
def load_csv(file_path):
    df = pd.read_csv(file_path)
    print("CSV Loaded Successfully")
    print(df.head())
    return df


# -------------------------------
# Load Excel File
# -------------------------------
def load_excel(file_path):
    df = pd.read_excel(file_path)
    print("Excel Loaded Successfully")
    print(df.head())
    return df


# -------------------------------
# Load JSON File
# -------------------------------
def load_json(file_path):
    df = pd.read_json(file_path)
    print("JSON Loaded Successfully")
    print(df.head())
    return df


# -------------------------------
# Load API Data
# -------------------------------
def load_api():

    url = "https://randomuser.me/api/?results=100"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        api_df = pd.json_normalize(data["results"])

        print("API Loaded Successfully")
        print(api_df.head())

        return api_df

    else:
        print("API Loading Failed")
        return None


# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":

    csv_file = "../dataset/Customer_Dataset.csv"
    excel_file = "../dataset/Customer_Dataset.xlsx"
    json_file = "../dataset/Customer_Dataset.json"

    csv_df = load_csv(csv_file)

    excel_df = load_excel(excel_file)

    json_df = load_json(json_file)

    api_df = load_api()

# -----------------------------
# Merge Multiple Datasets
# -----------------------------

# Combine CSV, Excel and JSON datasets
merged_df = pd.concat(
    [csv_df, excel_df, json_df],
    ignore_index=True
)

print("\nCSV + Excel + JSON Merged Successfully")
print("Total Records :", len(merged_df))

# Save merged dataset
merged_df.to_csv(
    "../Output/Merged_Customer_Dataset.csv",
    index=False
)

print("Merged Dataset Saved Successfully")