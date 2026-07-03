# ==========================================================
# Project 2 : Enterprise Customer Data Engineering Platform
# File Name : 03_feature_engineering.py
# Purpose   : Customer Feature Engineering
# ==========================================================

import pandas as pd


# -----------------------------
# Create Age Group
# -----------------------------
def create_age_group(df):

    bins = [0, 25, 35, 50, 100]
    labels = ["Young", "Adult", "Middle Age", "Senior"]

    df["Age_Group"] = pd.cut(
        df["Age"],
        bins=bins,
        labels=labels
    )

    print("Age Group Created")

    return df


# -----------------------------
# Purchase Category
# -----------------------------
def purchase_category(df):

    def category(amount):

        if amount < 5000:
            return "Low"

        elif amount < 20000:
            return "Medium"

        else:
            return "High"

    df["Purchase_Category"] = df["Purchase_Amount"].apply(category)

    print("Purchase Category Created")

    return df


# -----------------------------
# Customer Segment
# -----------------------------
def customer_segment(df):

    def segment(amount):

        if amount >= 30000:
            return "Premium"

        elif amount >= 10000:
            return "Gold"

        else:
            return "Silver"

    df["Customer_Segment"] = df["Purchase_Amount"].apply(segment)

    print("Customer Segment Created")

    return df


# -----------------------------
# Purchase Frequency
# -----------------------------
def purchase_frequency(df):

    df["Purchase_Frequency"] = 1

    print("Purchase Frequency Created")

    return df


# -----------------------------
# Customer Lifetime Value
# -----------------------------
def lifetime_value(df):

    df["Customer_Lifetime_Value"] = (
        df["Purchase_Amount"] * df["Purchase_Frequency"]
    )

    print("Customer Lifetime Value Created")

    return df


# -----------------------------
# High Value Customer
# -----------------------------
def high_value_customer(df):

    df["High_Value_Customer"] = df["Purchase_Amount"].apply(
        lambda x: "Yes" if x >= 20000 else "No"
    )

    print("High Value Customer Feature Created")

    return df


# -----------------------------
# Customer Tenure
# -----------------------------
def customer_tenure(df):

    df["Purchase_Date"] = pd.to_datetime(df["Purchase_Date"])

    today = pd.Timestamp.today()

    df["Customer_Tenure_Days"] = (
        today - df["Purchase_Date"]
    ).dt.days

    print("Customer Tenure Created")

    return df


# -----------------------------
# Recent Customer
# -----------------------------
def recent_customer(df):

    df["Recent_Customer"] = df["Customer_Tenure_Days"].apply(
        lambda x: "Recent" if x <= 180 else "Old"
    )

    print("Recent Customer Feature Created")

    return df


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    df = pd.read_csv("../Output/Cleaned_Customer_Dataset.csv")

    df = create_age_group(df)

    df = purchase_category(df)

    df = customer_segment(df)

    df = purchase_frequency(df)

    df = lifetime_value(df)

    df = high_value_customer(df)

    df = customer_tenure(df)

    df = recent_customer(df)

    output_file = "../Output/Feature_Engineered_Customer_Dataset.csv"

    df.to_csv(output_file, index=False)

    print("\nFeature Engineering Completed Successfully")

    print(df.head())

    print("\nSaved Successfully")

    print(output_file)