# ==========================================================
# Project 2 : Enterprise Customer Data Engineering Platform
# File Name : main.py
# Purpose   : Automated ETL Workflow
# ==========================================================

import subprocess
import sys

print("=" * 60)
print("Enterprise Customer Data Engineering Platform")
print("Automated ETL Workflow Started")
print("=" * 60)


def run_script(script_name):

    print(f"\nRunning : {script_name}")

    result = subprocess.run(
        [sys.executable, script_name]
    )

    if result.returncode == 0:
        print(f"{script_name} Completed Successfully")
    else:
        print(f"{script_name} Failed")
        exit()


run_script("load_data.py")

run_script("data_cleaning.py")

run_script("feature_engineering.py")

run_script("mysql_upload.py")

run_script("summary_report.py")

print("\n" + "=" * 60)
print("PROJECT COMPLETED SUCCESSFULLY")
print("=" * 60)