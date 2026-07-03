# ==========================================================
# Project : Big Data Supply Chain Analytics & Demand Forecasting
# File    : data_processing/01_data_cleaning.py
# Status  : FINAL VERSION
# ==========================================================

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    to_date,
    when,
    current_timestamp,
    datediff,
    lit
)

from config.config import (
    SPARK_APP_NAME,
    SALES_DATA_FILE,
    CLEANED_DATA_FILE
)


def create_spark_session():

    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    spark = (
        SparkSession.builder
        .appName(f"{SPARK_APP_NAME}_Cleaning")
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark


def load_dataset(spark):

    return (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(SALES_DATA_FILE))
    )


def clean_dataset(df):

    # -----------------------------
    # Convert Date
    # -----------------------------
    df = df.withColumn(
        "Date",
        to_date(col("Date"), "yyyy-MM-dd")
    )

    # -----------------------------
    # Remove Duplicates
    # -----------------------------
    df = df.dropDuplicates()

    # -----------------------------
    # Remove Null Values
    # -----------------------------
    df = df.dropna()

    # -----------------------------
    # Remove Negative Values
    # -----------------------------
    numeric_columns = [
        "Inventory Level",
        "Units Sold",
        "Units Ordered",
        "Price",
        "Discount",
        "Competitor Pricing",
        "Demand"
    ]

    for column in numeric_columns:

        df = df.filter(col(column) >= 0)

    # -----------------------------
    # Inventory Status
    # -----------------------------
    df = df.withColumn(

        "Inventory Status",

        when(col("Inventory Level") < 100, "Low Stock")
        .when(col("Inventory Level") > 500, "Over Stock")
        .otherwise("Normal")

    )

    # -----------------------------
    # Stock Movement
    # -----------------------------
    df = df.withColumn(

        "Stock Movement",

        col("Units Ordered") - col("Units Sold")

    )

    # -----------------------------
    # Days From Today
    # -----------------------------
    df = df.withColumn(

        "Days Since Sale",

        datediff(current_timestamp(), col("Date"))

    )

    # -----------------------------
    # Processing Timestamp
    # -----------------------------
    df = df.withColumn(

        "Processed Timestamp",

        current_timestamp()

    )

    return df


def save_dataset(df):

    df.coalesce(1) \
        .write \
        .mode("overwrite") \
        .option("header", True) \
        .csv(str(CLEANED_DATA_FILE))

def validate(df):

    print("=" * 70)
    print("CLEANED DATASET SUMMARY")
    print("=" * 70)

    print(f"Rows : {df.count()}")
    print(f"Columns : {len(df.columns)}")

    df.printSchema()

    df.show(10, truncate=False)


def main():

    spark = create_spark_session()

    try:

        df = load_dataset(spark)

        cleaned_df = clean_dataset(df)

        validate(cleaned_df)

        save_dataset(cleaned_df)

        print("\nCleaned dataset saved successfully.")

    except Exception as e:

        print(e)

    finally:

        spark.stop()


if __name__ == "__main__":

    main()