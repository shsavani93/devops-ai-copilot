from fastapi import APIRouter, status
from app.schemas.log import LogCreate

router = APIRouter(
    prefix="/api/v1",
    tags=["Logs"]
)

@router.post("/logs", status_code=status.HTTP_201_CREATED)
async def create_log(log: LogCreate):
    return {
        "message": "Log received successfully",
        "service": log.service,
        "level": log.level,
        "log_message": log.message
    }