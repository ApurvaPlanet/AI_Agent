from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from chatbot.app.services.llm_service import update_llm_memory
from chatbot.app.config import get_department_by_token

router = APIRouter(prefix="/learn", tags=["Learning"])

class LearnRequest(BaseModel):
    instruction: str  # Correction or new instruction
    answer: str  # Correct answer provided by the user

@router.post("/")
async def learn_api(request: LearnRequest, department: str = Depends(get_department_by_token)):
    try:
        update_llm_memory(request.instruction, request.answer, department)
        return {"message": "Knowledge updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
