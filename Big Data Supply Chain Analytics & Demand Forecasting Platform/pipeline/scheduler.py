# ==========================================================
# scheduler.py
# ==========================================================

import schedule
import time
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def run_pipeline():

    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "pipeline/main_pipeline.py")]
    )

schedule.every().day.at("09:00").do(run_pipeline)

print("Scheduler Started...")

while True:

    schedule.run_pending()
    time.sleep(60)