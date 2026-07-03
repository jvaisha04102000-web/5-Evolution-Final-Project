USE customer_data_engineering;

-- Total Customers
SELECT COUNT(*) AS Total_Customers
FROM customers;

-- Average Purchase
SELECT AVG(Purchase_Amount) AS Average_Purchase
FROM customers;

-- Highest Purchase
SELECT MAX(Purchase_Amount) AS Highest_Purchase
FROM customers;

-- Lowest Purchase
SELECT MIN(Purchase_Amount) AS Lowest_Purchase
FROM customers;

-- Customer Segment Summary
SELECT Customer_Segment, COUNT(*) AS Total_Customers
FROM customers
GROUP BY Customer_Segment;

-- Purchase Category Summary
SELECT Purchase_Category, COUNT(*) AS Total_Customers
FROM customers
GROUP BY Purchase_Category;

-- High Value Customers
SELECT *
FROM customers
WHERE High_Value_Customer='Yes';

-- Revenue by Customer Segment
SELECT Customer_Segment,
SUM(Purchase_Amount) AS Revenue
FROM customers
GROUP BY Customer_Segment;

-- Top 10 Customers
SELECT Customer_Name,
Purchase_Amount
FROM customers
ORDER BY Purchase_Amount DESC
LIMIT 10;

-- Top 5 Cities
SELECT City,
COUNT(*) AS Customers
FROM customers
GROUP BY City
ORDER BY Customers DESC
LIMIT 5;