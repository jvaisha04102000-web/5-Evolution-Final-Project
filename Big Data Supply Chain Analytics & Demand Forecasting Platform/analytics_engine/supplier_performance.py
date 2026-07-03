# ==========================================================
# Project : Big Data Supply Chain Analytics
# File    : analytics_engine/supplier_analysis.py
# Status  : FINAL VERSION
# ==========================================================

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round, when

from config.config import SALES_DATA_FILE


def create_spark():
    spark = (
        SparkSession.builder
        .appName("SupplierAnalysis")
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def load_data(spark):
    return (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(SALES_DATA_FILE))
    )


def supplier_metrics(df):

    # Delivery Efficiency proxy (Units Ordered vs Demand)
    df = df.withColumn(
        "Delivery Efficiency",
        round(col("Units Ordered") / (col("Demand") + 1), 2)
    )

    # Cost Pressure Index
    df = df.withColumn(
        "Cost Pressure Index",
        round(col("Price") / (col("Competitor Pricing") + 1), 2)
    )

    # Supplier Performance Category
    df = df.withColumn(
        "Supplier Performance",
        when(col("Delivery Efficiency") >= 1.2, "High")
        .when(col("Delivery Efficiency") >= 0.8, "Medium")
        .otherwise("Low")
    )

    return df


def analyze(df):

    print("=" * 70)
    print("SUPPLIER PERFORMANCE ANALYSIS")
    print("=" * 70)

    df.groupBy("Region", "Supplier Performance").count().show()

    df.select(
        "Region",
        "Delivery Efficiency",
        "Cost Pressure Index",
        "Supplier Performance"
    ).show(10, truncate=False)


def main():

    spark = create_spark()

    df = load_data(spark)

    df = supplier_metrics(df)

    analyze(df)

    spark.stop()


if __name__ == "__main__":
    main()