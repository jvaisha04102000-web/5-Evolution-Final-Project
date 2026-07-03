# ==========================================================
# Project : Big Data Supply Chain Analytics
# File    : reporting/executive_report.py
# ==========================================================

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    sum,
    avg,
    max,
    min,
    round
)

from config.config import SALES_DATA_FILE

spark = (
    SparkSession.builder
    .appName("ExecutiveSummary")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(SALES_DATA_FILE))
)

summary = df.agg(
    sum("Units Sold").alias("Total Units Sold"),
    sum("Units Ordered").alias("Total Units Ordered"),
    avg("Demand").alias("Average Demand"),
    avg("Inventory Level").alias("Average Inventory"),
    avg("Price").alias("Average Price"),
    max("Demand").alias("Maximum Demand"),
    min("Demand").alias("Minimum Demand")
)

summary = (
    summary
    .withColumn("Average Demand", round("Average Demand", 2))
    .withColumn("Average Inventory", round("Average Inventory", 2))
    .withColumn("Average Price", round("Average Price", 2))
)

print("=" * 70)
print("EXECUTIVE SUMMARY REPORT")
print("=" * 70)

summary.show(truncate=False)

print("\nRegion Wise Summary")
df.groupBy("Region").agg(
    sum("Units Sold").alias("Units Sold"),
    sum("Demand").alias("Demand")
).show()

print("\nCategory Wise Summary")
df.groupBy("Category").agg(
    sum("Units Sold").alias("Units Sold"),
    avg("Price").alias("Average Price")
).show()

spark.stop()