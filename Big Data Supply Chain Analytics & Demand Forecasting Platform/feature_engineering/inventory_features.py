# ==========================================================
# Project : Big Data Supply Chain Analytics & Demand Forecasting
# File    : feature_engineering/inventory_features.py
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
from pyspark.sql.functions import (
    col,
    when,
    round,
    current_timestamp
)

from config.config import SALES_DATA_FILE

OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "inventory_features"


def create_spark():
    spark = (
        SparkSession.builder
        .appName("InventoryFeatureEngineering")
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


def create_inventory_features(df):

    df = df.withColumn(
        "Inventory Shortage Flag",
        when(col("Inventory Level") < 100, 1).otherwise(0)
    )

    df = df.withColumn(
        "Overstock Flag",
        when(col("Inventory Level") > 500, 1).otherwise(0)
    )

    df = df.withColumn(
        "Inventory Turnover",
        round(
            col("Units Sold") / (col("Inventory Level") + 1),
            2
        )
    )

    df = df.withColumn(
        "Reorder Required",
        when(
            (col("Inventory Level") < 100) &
            (col("Demand") > col("Inventory Level")),
            "YES"
        ).otherwise("NO")
    )

    df = df.withColumn(
        "Warehouse Utilization %",
        round(
            (col("Inventory Level") / 500) * 100,
            2
        )
    )

    df = df.withColumn(
        "Inventory Health",
        when(col("Inventory Level") < 100, "Critical")
        .when(col("Inventory Level") < 250, "Medium")
        .otherwise("Healthy")
    )

    df = df.withColumn(
        "Processing Time",
        current_timestamp()
    )

    return df


def save_data(df):

    (
        df.coalesce(1)
        .write
        .mode("overwrite")
        .option("header", True)
        .csv(str(OUTPUT_PATH))
    )


def main():

    spark = create_spark()

    df = load_data(spark)

    feature_df = create_inventory_features(df)

    print("=" * 70)
    print("INVENTORY FEATURE ENGINEERING")
    print("=" * 70)

    print("Rows :", feature_df.count())
    print("Columns :", len(feature_df.columns))

    feature_df.printSchema()

    feature_df.show(10, truncate=False)

    save_data(feature_df)

    print("\nInventory feature engineering completed successfully.")

    spark.stop()


if __name__ == "__main__":
    main()