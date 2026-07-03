import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    RAW_DOCS = os.path.join(DATA_DIR, "raw_docs")
    PROCESSED_DOCS = os.path.join(DATA_DIR, "processed")
    EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")

    # Vector DB
    FAISS_INDEX_PATH = os.path.join(EMBEDDINGS_DIR, "faiss_index")

    # Logging
    # Logging
    LOG_FILE = os.path.join(BASE_DIR, "logs", "app.log")
    AI_LOG_FILE = os.path.join(BASE_DIR, "logs", "ai_interactions.log")
    ACTIVITY_LOG_FILE = os.path.join(BASE_DIR, "logs", "activity_logs.json")

    # Model settings
    EMBEDDING_MODEL = "text-embedding-3-small"
    CHAT_MODEL = "gpt-4o-mini"