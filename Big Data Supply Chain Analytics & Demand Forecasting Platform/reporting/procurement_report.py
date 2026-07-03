# ==========================================================
# Project : Big Data Supply Chain Analytics
# File    : reporting/procurement_report.py
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
    col,
    sum,
    avg,
    round,
    when
)

from config.config import SALES_DATA_FILE


spark = (
    SparkSession.builder
    .appName("ProcurementReport")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(SALES_DATA_FILE))
)

report = (
    df.groupBy("Region", "Category")
    .agg(
        sum("Units Ordered").alias("Total Ordered"),
        sum("Units Sold").alias("Total Sold"),
        avg("Inventory Level").alias("Avg Inventory"),
        avg("Price").alias("Avg Price")
    )
)

report = (
    report
    .withColumn(
        "Procurement Efficiency",
        round(col("Total Sold") / col("Total Ordered"), 2)
    )
    .withColumn(
        "Procurement Status",
        when(col("Procurement Efficiency") >= 0.80, "Excellent")
        .when(col("Procurement Efficiency") >= 0.60, "Good")
        .otherwise("Needs Improvement")
    )
)

print("=" * 70)
print("PROCUREMENT REPORT")
print("=" * 70)

report.orderBy("Region", "Category").show(100, False)

spark.stop()