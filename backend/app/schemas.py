from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, HttpUrl, field_serializer


def serialize_utc_datetime(value: datetime) -> str:
    """Return ISO-8601 UTC timestamps with a Z suffix for browser conversion."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


class UrlCreate(BaseModel):
    url: HttpUrl


class HealthCheckRead(BaseModel):
    status_code: Optional[int]
    response_time_ms: int
    is_up: bool
    checked_at: datetime

    model_config = {"from_attributes": True}

    @field_serializer("checked_at")
    def serialize_checked_at(self, value: datetime) -> str:
        return serialize_utc_datetime(value)


class UrlRead(BaseModel):
    id: int
    url: HttpUrl
    created_at: datetime

    model_config = {"from_attributes": True}

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return serialize_utc_datetime(value)


class UrlStatusRead(UrlRead):
    latest_check: Optional[HealthCheckRead]

    model_config = {"from_attributes": True}
