from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import Config

# Bearer token security
security = HTTPBearer()

def get_user_department(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Returns the department based on the provided bearer token."""
    token = credentials.credentials
    department = Config.get_department_by_token(token)
    
    if department:
        return department
    raise HTTPException(status_code=403, detail="Invalid API token")
