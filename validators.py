from enum import Enum
from typing import Optional
from pydantic import BaseModel, validator


class EventType(str, Enum):
    usual = "usual"
    cumulative = "cumulative"


class Grouping(str, Enum):
    weekly = "weekly"
    bi_weekly = "bi-weekly"
    monthly = "monthly"


class EventQueryParams(BaseModel):
    type_: Optional[EventType]
    grouping: Optional[Grouping]

    @validator("type", pre=True, always=True, check_fields=False)
    def validate_type_(cls, value):
        if value not in EventType.__members__:
            raise ValueError(f"type must be one of: {', '.join(Grouping.__members__)}")
        return value

    @validator('grouping', pre=True, always=True, check_fields=False)
    def validate_grouping(cls, value):
        if value not in Grouping.__members__:
            raise ValueError(f"grouping must be one of: {', '.join(Grouping.__members__)}")
        return value
