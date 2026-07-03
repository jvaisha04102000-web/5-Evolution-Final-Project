# ==========================================================
# Project : Big Data Supply Chain Analytics
# File    : analytics_engine/logistics_analysis.py
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
from pyspark.sql.functions import col, when, round, avg

from config.config import SALES_DATA_FILE


def create_spark():
    spark = (
        SparkSession.builder
        .appName("LogisticsAnalysis")
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


def logistics_metrics(df):

    # Delivery Load Proxy (Units Ordered vs Units Sold)
    df = df.withColumn(
        "Delivery Load",
        col("Units Ordered") - col("Units Sold")
    )

    # Fulfillment Efficiency
    df = df.withColumn(
        "Fulfillment Efficiency",
        round(col("Units Sold") / (col("Units Ordered") + 1), 2)
    )

    # Delay Risk Indicator (based on mismatch)
    df = df.withColumn(
        "Delay Risk",
        when(col("Delivery Load") > 100, "HIGH")
        .when(col("Delivery Load") > 50, "MEDIUM")
        .otherwise("LOW")
    )

    return df


def analyze(df):

    print("=" * 70)
    print("LOGISTICS PERFORMANCE ANALYSIS")
    print("=" * 70)

    df.groupBy("Region", "Delay Risk").count().show()

    print("\nTop Logistics Records:")
    df.select(
        "Store ID",
        "Product ID",
        "Region",
        "Units Ordered",
        "Units Sold",
        "Delivery Load",
        "Fulfillment Efficiency",
        "Delay Risk"
    ).show(10, truncate=False)


def main():

    spark = create_spark()

    df = load_data(spark)

    df = logistics_metrics(df)

    analyze(df)

    spark.stop()


if __name__ == "__main__":
    main()