# ==========================================================
# Project : Big Data Supply Chain Analytics & Demand Forecasting
# File    : data_ingestion/load_sales.py
# Status  : FINAL VERSION
# ==========================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
)
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.config import (
    SALES_DATA_FILE,
    SPARK_APP_NAME
)


def create_spark_session():
    spark = (
        SparkSession.builder
        .appName(SPARK_APP_NAME)
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")
    return spark


def get_schema():

    return StructType([

        StructField("Date", StringType(), True),
        StructField("Store ID", StringType(), True),
        StructField("Product ID", StringType(), True),
        StructField("Category", StringType(), True),
        StructField("Region", StringType(), True),

        StructField("Inventory Level", IntegerType(), True),
        StructField("Units Sold", IntegerType(), True),
        StructField("Units Ordered", IntegerType(), True),

        StructField("Price", DoubleType(), True),
        StructField("Discount", IntegerType(), True),

        StructField("Weather Condition", StringType(), True),
        StructField("Promotion", IntegerType(), True),
        StructField("Competitor Pricing", DoubleType(), True),

        StructField("Seasonality", StringType(), True),
        StructField("Epidemic", IntegerType(), True),
        StructField("Demand", IntegerType(), True)

    ])


def load_sales_data(spark):

    df = (
        spark.read
        .option("header", True)
        .schema(get_schema())
        .csv(str(SALES_DATA_FILE))
    )

    return df


def validate_dataset(df):

    print("=" * 70)
    print("SUPPLY CHAIN DATASET VALIDATION")
    print("=" * 70)

    print(f"Rows    : {df.count()}")
    print(f"Columns : {len(df.columns)}")

    print("\nSchema\n")
    df.printSchema()

    print("\nFirst 10 Records\n")
    df.show(10, truncate=False)

    print("\nMissing Values\n")

    df.select([
        col(c).isNull().cast("int").alias(c)
        for c in df.columns
    ]).groupBy().sum().show()


def main():

    spark = create_spark_session()

    try:

        sales_df = load_sales_data(spark)

        validate_dataset(sales_df)

        print("\nDataset Loaded Successfully.")

    except Exception as e:

        print(f"\nERROR : {e}")

    finally:

        spark.stop()


if __name__ == "__main__":
    main()