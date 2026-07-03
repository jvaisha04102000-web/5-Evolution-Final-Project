# ==========================================================
# Project : Big Data Supply Chain Analytics
# File    : pipeline/main_pipeline.py
# ==========================================================

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

scripts = [

    "data_ingestion/load_sales.py",
    "data_ingestion/load_inventory.py",
    "data_ingestion/load_logistics.py",
    "data_ingestion/load_procurement.py",

    "data_processing/data_cleaning.py",
    "data_processing/clean_sales.py",

    "feature_engineering/demand_features.py",
    "feature_engineering/inventory_features.py",
    "feature_engineering/supplier_features.py",

    "tableau_exports/kpi_dataset_builder.py"

]

print("=" * 70)
print("BIG DATA SUPPLY CHAIN PIPELINE")
print("=" * 70)

for script in scripts:

    print(f"\nRunning : {script}")

    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / script)],
        check=False
    )

print("\nPipeline Completed Successfully")