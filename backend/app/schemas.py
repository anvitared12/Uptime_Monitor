from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl


class UrlCreate(BaseModel):
    url: HttpUrl


class HealthCheckRead(BaseModel):
    status_code: Optional[int]
    response_time_ms: int
    is_up: bool
    checked_at: datetime

    model_config = {"from_attributes": True}


class UrlRead(BaseModel):
    id: int
    url: HttpUrl
    created_at: datetime

    model_config = {"from_attributes": True}


class UrlStatusRead(UrlRead):
    latest_check: Optional[HealthCheckRead]

    model_config = {"from_attributes": True}
