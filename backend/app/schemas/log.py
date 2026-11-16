from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogCreate(BaseModel):
    service: str = Field(min_length=1, max_length=100)
    level: LogLevel
    message: str = Field(min_length=1, max_length=5000)
    timestamp: datetime

class LogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    service: str
    level: str
    message: str
    timestamp: datetime

class LogCreateResponse(BaseModel):
    id: int
    message: str
    service: str
    level: str
    log_message: str
    timestamp: datetime