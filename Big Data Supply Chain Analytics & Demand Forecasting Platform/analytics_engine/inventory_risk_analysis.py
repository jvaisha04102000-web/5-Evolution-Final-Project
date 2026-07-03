# ==========================================================
# Project : Big Data Supply Chain Analytics
# File    : analytics_engine/inventory_risk_analysis.py
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
        .appName("InventoryRiskAnalysis")
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


def inventory_risk_features(df):

    # Stock Gap (Demand vs Inventory)
    df = df.withColumn(
        "Stock Gap",
        col("Demand") - col("Inventory Level")
    )

    # Inventory Risk Level
    df = df.withColumn(
        "Inventory Risk",
        when(col("Stock Gap") > 200, "CRITICAL")
        .when(col("Stock Gap") > 50, "HIGH")
        .when(col("Stock Gap") > 0, "MEDIUM")
        .otherwise("LOW")
    )

    # Overstock Risk
    df = df.withColumn(
        "Overstock Risk",
        when(col("Inventory Level") > 500, "YES").otherwise("NO")
    )

    # Stock Turnover Proxy
    df = df.withColumn(
        "Turnover Ratio",
        round(col("Units Sold") / (col("Inventory Level") + 1), 2)
    )

    return df


def analyze(df):

    print("=" * 70)
    print("INVENTORY RISK ANALYSIS")
    print("=" * 70)

    df.groupBy("Region", "Inventory Risk").count().show()

    print("\nTop Risk Records:")
    df.select(
        "Store ID",
        "Product ID",
        "Region",
        "Inventory Level",
        "Demand",
        "Stock Gap",
        "Inventory Risk"
    ).show(10, truncate=False)


def main():

    spark = create_spark()

    df = load_data(spark)

    df = inventory_risk_features(df)

    analyze(df)

    spark.stop()


if __name__ == "__main__":
    main()