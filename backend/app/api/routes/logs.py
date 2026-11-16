
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.database import get_db
from app.models.log import ApplicationLog
from app.schemas.log import LogCreate, LogResponse, LogCreateResponse

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/api/v1",
    tags=["Logs"]
)

@router.post(
    "/logs",
    status_code=status.HTTP_201_CREATED,
    response_model=LogCreateResponse
)
def create_log(
    log: LogCreate,
    db: Session = Depends(get_db)
):
    try:
        db_log = ApplicationLog(
            service=log.service,
            level=log.level.value,
            message=log.message,
            timestamp=log.timestamp
        )

        db.add(db_log)
        db.commit()
        db.refresh(db_log)

        return {
            "id": db_log.id,
            "message": "Log stored successfully",
            "service": db_log.service,
            "level": db_log.level,
            "log_message": db_log.message,
            "timestamp": db_log.timestamp
        }

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to store log"
        )

@router.get("/logs", response_model=list[LogResponse])
def get_logs(
    service: str | None = None,
    level: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    statement = select(ApplicationLog)

    if service is not None:
        statement = statement.where(
            ApplicationLog.service == service
        )

    if level is not None:
        statement = statement.where(
            ApplicationLog.level == level.upper()
        )

    statement = statement.order_by(
        ApplicationLog.id.desc()
    ).offset(skip).limit(limit)

    logs = db.scalars(statement).all()

    return logs