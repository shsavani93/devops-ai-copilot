from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class LogLevel([str], Enum):
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