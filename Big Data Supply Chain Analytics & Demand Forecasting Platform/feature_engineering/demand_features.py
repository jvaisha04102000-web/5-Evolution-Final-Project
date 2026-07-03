# ==========================================================
# Project : Big Data Supply Chain Analytics
# File    : feature_engineering/demand_features.py
# ==========================================================

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, round

from config.config import SALES_DATA_FILE

spark = (
    SparkSession.builder
    .appName("DemandFeatures")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(SALES_DATA_FILE))
)

df = (
    df
    .withColumn(
        "Demand Ratio",
        when(
            col("Inventory Level") == 0,
            0
        ).otherwise(
            round(col("Demand") / col("Inventory Level"), 2)
        )
    )
    .withColumn(
        "Sales Ratio",
        when(
            col("Units Ordered") == 0,
            0
        ).otherwise(
            round(col("Units Sold") / col("Units Ordered"), 2)
        )
    )
    .withColumn(
        "Demand Level",
        when(col("Demand") >= 200, "HIGH")
        .when(col("Demand") >= 100, "MEDIUM")
        .otherwise("LOW")
    )
)

print("=" * 70)
print("DEMAND FEATURE ENGINEERING")
print("=" * 70)

df.select(
    "Store ID",
    "Product ID",
    "Region",
    "Category",
    "Demand",
    "Inventory Level",
    "Units Ordered",
    "Demand Ratio",
    "Sales Ratio",
    "Demand Level"
).show(20, False)

spark.stop()