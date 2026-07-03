# ==========================================================
# Project : Big Data Supply Chain Analytics
# File    : analytics_engine/demand_forecasting.py
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
from pyspark.sql.functions import col

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator

from config.config import SALES_DATA_FILE


def create_spark():
    spark = (
        SparkSession.builder
        .appName("DemandForecasting")
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


def prepare_features(df):

    assembler = VectorAssembler(
        inputCols=[
            "Inventory Level",
            "Units Sold",
            "Units Ordered",
            "Price",
            "Discount",
            "Promotion",
            "Competitor Pricing",
            "Epidemic"
        ],
        outputCol="features"
    )

    df = assembler.transform(df)

    return df.select(
        "features",
        col("Demand").alias("label"),
        "Date",
        "Region",
        "Category"
    )


def train_model(df):

    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

    model = LinearRegression(
        featuresCol="features",
        labelCol="label"
    )

    lr_model = model.fit(train_df)

    predictions = lr_model.transform(test_df)

    return predictions


def evaluate(predictions):

    evaluator = RegressionEvaluator(
        labelCol="label",
        predictionCol="prediction",
        metricName="rmse"
    )

    rmse = evaluator.evaluate(predictions)

    print("\n" + "=" * 70)
    print("DEMAND FORECASTING RESULTS")
    print("=" * 70)
    print(f"RMSE : {round(rmse,2)}")

    predictions.select(
        "Date",
        "Region",
        "Category",
        "label",
        "prediction"
    ).show(20, truncate=False)


def main():

    spark = create_spark()

    df = load_data(spark)

    feature_df = prepare_features(df)

    predictions = train_model(feature_df)

    evaluate(predictions)

    spark.stop()


if __name__ == "__main__":
    main()