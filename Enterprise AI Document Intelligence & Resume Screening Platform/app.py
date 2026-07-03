from flask import Flask, jsonify
from config import Config
from src.logger import logger
import os
import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)


# Ensure folders exist
def create_folders():
    folders = [
        Config.DATA_DIR,
        Config.RAW_DOCS,
        Config.PROCESSED_DOCS,
        Config.EMBEDDINGS_DIR,
        os.path.dirname(Config.LOG_FILE)
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

create_folders()


@app.route("/")
def home():
    logger.info("Home route accessed")
    return jsonify({
        "message": "Enterprise AI Document Intelligence Platform Running",
        "status": "active"
    })


@app.route("/health")
def health():
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    logger.info("Starting Flask server")
    app.run(debug=True)