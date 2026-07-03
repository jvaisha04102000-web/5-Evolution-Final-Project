USE customer_data_engineering;

CREATE TABLE IF NOT EXISTS customers (

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

);