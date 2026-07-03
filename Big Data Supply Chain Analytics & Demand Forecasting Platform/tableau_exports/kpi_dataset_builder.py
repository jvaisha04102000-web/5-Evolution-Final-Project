# ==========================================================
# Project : Big Data Supply Chain Analytics
# File    : tableau_exports/kpi_dataset_builder.py
# ==========================================================

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from config.config import SALES_DATA_FILE

spark = (
    SparkSession.builder
    .appName("KPIDatasetBuilder")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(SALES_DATA_FILE))
)

kpi_df = df.select(
    "Date",
    "Region",
    "Category",
    "Units Sold",
    "Units Ordered",
    "Inventory Level",
    "Demand",
    "Price"
)

# Output folder
output_path = PROJECT_ROOT / "data" / "output"
output_path.mkdir(parents=True, exist_ok=True)

# Convert Spark DataFrame -> Pandas
pdf = kpi_df.toPandas()

# Save CSV
output_file = output_path / "tableau_kpi_dataset.csv"
pdf.to_csv(output_file, index=False)

print("=" * 70)
print("TABLEAU KPI DATASET CREATED")
print("=" * 70)
print("Rows :", len(pdf))
print("Saved :", output_file)

print("\nSample Data:")
print(pdf.head(20))

spark.stop()