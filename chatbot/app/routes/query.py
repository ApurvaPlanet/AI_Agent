from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from chatbot.app.services.llm_service import query_llm
from chatbot.app.config import get_department_by_token

router = APIRouter(prefix="/query", tags=["Querying"])


class QueryRequest(BaseModel):
    input_text: str  # User input


@router.post("/")
async def query_api(request: QueryRequest, department: str = Depends(get_department_by_token)):
    response = query_llm(request.input_text, department)
    
    if not response.get("answer"):
        raise HTTPException(status_code=400, detail="No relevant indexed data found.")
    
    return response
