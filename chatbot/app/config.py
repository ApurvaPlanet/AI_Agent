import os

# OpenAI API Key
OPENAI_API_KEY = "sk-tH8op0zQj6TkOBG22N3ei6ysTlUXzMNWLuC9tn2WNQT3BlbkFJNSjcoG8m0iYdjURMHJ_ALZsADc-4ucD6e0JS9piSYA"

# API Keys for access control
API_KEYS = {
    "HR": "hr_secret_key",
    "Finance": "finance_secret_key",
    "IT": "it_secret_key",
    "Admin": "admin_token"
}

# FAISS Index Storage Directory
FAISS_INDEX_PATH = "./faiss_store/index"

# Data Storage Directory
DATA_DIR = "./data"

# API Rate Limits (Optional)
RATE_LIMIT = os.getenv("RATE_LIMIT", "100 requests per minute")


@staticmethod
def get_department_by_token(token: str):
        """Returns department based on token or None if invalid."""
        for department, key in API_KEYS.items():
            if key == token:
                return department
        return None


 # Storage Directories
STORAGE_DIR = "storage"
VECTOR_DB_PATH = os.path.join(STORAGE_DIR, "faiss_index.bin")
LLM_MODEL_PATH = os.path.join(STORAGE_DIR, "llm_model.pkl")
REMOTE_FILE_STORAGE = os.path.join(STORAGE_DIR, "remote_files")

# Ensure directories exist
for directory in [FAISS_INDEX_PATH, DATA_DIR, STORAGE_DIR, REMOTE_FILE_STORAGE]:
 os.makedirs(directory, exist_ok=True)




