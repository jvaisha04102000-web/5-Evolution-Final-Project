import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")

    # Groq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    RAW_DOCS = os.path.join(DATA_DIR, "raw_docs")
    PROCESSED_DOCS = os.path.join(DATA_DIR, "processed")
    EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")

    # Vector DB
    FAISS_INDEX_PATH = os.path.join(EMBEDDINGS_DIR, "faiss_index")

    # Logging
    LOG_FILE = os.path.join(BASE_DIR, "logs", "app.log")
    AI_LOG_FILE = os.path.join(BASE_DIR, "logs", "ai_interactions.log")
    ACTIVITY_LOG_FILE = os.path.join(BASE_DIR, "logs", "activity_logs.json")

    # Models
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    CHAT_MODEL = "llama-3.3-70b-versatile"