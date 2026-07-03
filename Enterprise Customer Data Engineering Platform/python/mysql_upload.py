# ==========================================================
# Project 2 : Enterprise Customer Data Engineering Platform
# File Name : 04_mysql_upload.py
# Purpose   : Upload Processed Data to MySQL
# ==========================================================

import pandas as pd
import mysql.connector

# -----------------------------
# MySQL Connection
# -----------------------------
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@123",
    database="customer_data_engineering"
)

cursor = connection.cursor()

# -----------------------------
# Drop Old Table (Optional)
# -----------------------------
cursor.execute("DROP TABLE IF EXISTS customers")

# -----------------------------
# Create Table
# -----------------------------
create_table = """
CREATE TABLE customers (

    Customer_ID INT PRIMARY KEY,
    Customer_Name VARCHAR(100),
    Gender VARCHAR(20),
    Age INT,
    Email VARCHAR(100),
    Phone VARCHAR(20),
    Address VARCHAR(200),
    City VARCHAR(100),
    State VARCHAR(100),
    Country VARCHAR(100),
    Purchase_Amount FLOAT,
    Purchase_Date DATE,

    Age_Group VARCHAR(30),
    Purchase_Category VARCHAR(30),
    Customer_Segment VARCHAR(30),

    Purchase_Frequency INT,
    Customer_Lifetime_Value FLOAT,

    High_Value_Customer VARCHAR(10),
    Customer_Tenure_Days INT,
    Recent_Customer VARCHAR(20)

)
"""

cursor.execute(create_table)

# -----------------------------
# Read Dataset
# -----------------------------
df = pd.read_csv("../Output/Feature_Engineered_Customer_Dataset.csv")

# -----------------------------
# Insert Query
# -----------------------------
insert_query = """
INSERT INTO customers
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

# -----------------------------
# Upload Data
# -----------------------------
for row in df.itertuples(index=False):
    cursor.execute(insert_query, tuple(row))

connection.commit()

print("Data Uploaded Successfully")
print("Total Records :", len(df))

cursor.close()
connection.close()

print("MySQL Connection Closed")