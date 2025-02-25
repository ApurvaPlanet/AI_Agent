from fastapi import APIRouter
import os

router = APIRouter(prefix="/cleanup", tags=["Cleanup"])

FAISS_INDEX_PATH = "storage/faiss_index.bin"
LLM_MODEL_PATH = "storage/llm_model.pkl"

@router.post("/")
async def cleanup_files():
    try:
        # Remove FAISS Index File
        if os.path.exists(FAISS_INDEX_PATH):
            os.remove(FAISS_INDEX_PATH)

        # Remove LLM Model File
        if os.path.exists(LLM_MODEL_PATH):
            os.remove(LLM_MODEL_PATH)

        return {"message": "All temporary files and stored data cleaned up successfully."}
    
    except Exception as e:
        return {"error": f"Cleanup failed: {str(e)}"}
