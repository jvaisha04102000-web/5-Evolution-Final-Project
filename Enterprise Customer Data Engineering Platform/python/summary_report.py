# ==========================================================
# Project 2 : Enterprise Customer Data Engineering Platform
# File Name : summary_report.py
# Purpose   : Summary Statistics & Business Insights
# ==========================================================

import pandas as pd

# Load Feature Engineered Dataset
df = pd.read_csv("../Output/Feature_Engineered_Customer_Dataset.csv")

print("\n========== CUSTOMER SUMMARY REPORT ==========\n")

# -----------------------------
# Basic Statistics
# -----------------------------
total_customers = len(df)
average_purchase = round(df["Purchase_Amount"].mean(), 2)
highest_purchase = df["Purchase_Amount"].max()
lowest_purchase = df["Purchase_Amount"].min()
average_age = round(df["Age"].mean(), 2)

print(f"Total Customers           : {total_customers}")
print(f"Average Purchase Amount   : {average_purchase}")
print(f"Highest Purchase Amount   : {highest_purchase}")
print(f"Lowest Purchase Amount    : {lowest_purchase}")
print(f"Average Customer Age      : {average_age}")

# -----------------------------
# Customer Behaviour Analysis
# -----------------------------
print("\n========== CUSTOMER SEGMENTS ==========")
print(df["Customer_Segment"].value_counts())

print("\n========== AGE GROUP ==========")
print(df["Age_Group"].value_counts())

print("\n========== HIGH VALUE CUSTOMERS ==========")
print(df["High_Value_Customer"].value_counts())

print("\n========== RECENT CUSTOMERS ==========")
print(df["Recent_Customer"].value_counts())

print("\n========== PURCHASE CATEGORY ==========")
print(df["Purchase_Category"].value_counts())

# -----------------------------
# Business Insights
# -----------------------------
print("\n========== TOP 5 CITIES ==========")
print(df["City"].value_counts().head())

print("\n========== GENDER DISTRIBUTION ==========")
print(df["Gender"].value_counts())

print("\n========== TOP 5 STATES ==========")
print(df["State"].value_counts().head())

print("\n========== REVENUE BY CUSTOMER SEGMENT ==========")
print(df.groupby("Customer_Segment")["Purchase_Amount"].sum())

print("\n========== REVENUE BY PURCHASE CATEGORY ==========")
print(df.groupby("Purchase_Category")["Purchase_Amount"].sum())

# -----------------------------
# Save Summary Report
# -----------------------------
summary = pd.DataFrame({

    "Metric":[
        "Total Customers",
        "Average Purchase",
        "Highest Purchase",
        "Lowest Purchase",
        "Average Age"
    ],

    "Value":[
        total_customers,
        average_purchase,
        highest_purchase,
        lowest_purchase,
        average_age
    ]

})

summary.to_csv(
    "../Output/Summary_Report.csv",
    index=False
)

print("\nSummary Report Saved Successfully")
print("../Output/Summary_Report.csv")