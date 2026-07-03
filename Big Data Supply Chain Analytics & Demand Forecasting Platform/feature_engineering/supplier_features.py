# ==========================================================
# Project : Big Data Supply Chain Analytics
# File    : feature_engineering/supplier_features.py
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
    .appName("SupplierFeatures")
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
        "Delivery Efficiency",
        when(
            col("Units Ordered") == 0,
            0
        ).otherwise(
            round(col("Units Sold") / col("Units Ordered"), 2)
        )
    )
    .withColumn(
        "Cost Pressure Index",
        round(
            col("Competitor Pricing") / col("Price"),
            2
        )
    )
    .withColumn(
        "Supplier Performance",
        when(col("Units Sold") >= col("Units Ordered") * 0.90, "High")
        .when(col("Units Sold") >= col("Units Ordered") * 0.70, "Medium")
        .otherwise("Low")
    )
)

print("=" * 70)
print("SUPPLIER FEATURE ENGINEERING")
print("=" * 70)

df.select(
    "Store ID",
    "Product ID",
    "Region",
    "Units Ordered",
    "Units Sold",
    "Delivery Efficiency",
    "Cost Pressure Index",
    "Supplier Performance"
).show(20, False)

spark.stop()