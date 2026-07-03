# ==========================================================
# Project : Big Data Supply Chain Analytics
# File    : data_processing/clean_sales.py
# ==========================================================

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

from config.config import SALES_DATA_FILE

spark = (
    SparkSession.builder
    .appName("CleanSalesData")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(SALES_DATA_FILE))
)

# Remove duplicates
df = df.dropDuplicates()

# Remove null values
df = df.dropna()

# Convert Date column
df = df.withColumn("Date", to_date(col("Date"), "yyyy-MM-dd"))

# Remove invalid values
df = df.filter(col("Inventory Level") >= 0)
df = df.filter(col("Units Sold") >= 0)
df = df.filter(col("Units Ordered") >= 0)
df = df.filter(col("Demand") >= 0)
df = df.filter(col("Price") > 0)

print("=" * 70)
print("CLEAN SALES DATA")
print("=" * 70)

print(f"Total Records : {df.count()}")

df.show(20, False)

spark.stop()