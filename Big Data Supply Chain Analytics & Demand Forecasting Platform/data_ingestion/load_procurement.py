# ==========================================================
# Project : Big Data Supply Chain Analytics
# File    : data_ingestion/load_procurement.py
# ==========================================================

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from config.config import SALES_DATA_FILE

spark = (
    SparkSession.builder
    .appName("LoadProcurementData")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(SALES_DATA_FILE))
)

procurement_df = df.select(
    "Date",
    "Store ID",
    "Product ID",
    "Category",
    "Region",
    "Inventory Level",
    "Units Ordered",
    "Price",
    "Competitor Pricing",
    "Demand"
)

print("=" * 70)
print("PROCUREMENT DATA LOADED")
print("=" * 70)
print(f"Rows : {procurement_df.count()}")

procurement_df.show(20, False)

spark.stop()