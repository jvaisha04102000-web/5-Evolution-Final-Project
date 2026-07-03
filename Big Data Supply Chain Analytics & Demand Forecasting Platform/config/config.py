# ==========================================================
# Project : Big Data Supply Chain Analytics & Demand Forecasting
# File    : config/config.py
# Status  : FINAL VERSION
# ==========================================================

from pathlib import Path

# -----------------------------
# PROJECT ROOT
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# DATA PATHS
# -----------------------------
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "data" / "output"
LOG_DIR = BASE_DIR / "logs"

# -----------------------------
# DATA FILES
# -----------------------------
SALES_DATA_FILE = RAW_DATA_DIR / "sales_data.csv"

# -----------------------------
# OUTPUT FILES
# -----------------------------
CLEANED_DATA_FILE = PROCESSED_DATA_DIR / "cleaned_sales"

SUPPLIER_REPORT = OUTPUT_DIR / "supplier_performance.csv"
INVENTORY_REPORT = OUTPUT_DIR / "inventory_report.csv"
DEMAND_FORECAST_REPORT = OUTPUT_DIR / "demand_forecast.csv"
EXECUTIVE_REPORT = OUTPUT_DIR / "executive_summary.csv"

# -----------------------------
# SPARK CONFIGURATION
# -----------------------------
SPARK_APP_NAME = "BigDataSupplyChainAnalytics"

# -----------------------------
# CREATE REQUIRED DIRECTORIES
# -----------------------------
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)