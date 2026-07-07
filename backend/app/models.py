"""SQLAlchemy models for the uptime monitor application.

This file defines the `URL` table where monitored URLs are stored.
"""

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class URL(Base):
    """Represents a website to be monitored.

    Columns:
    - `id`: primary key integer
    - `url`: unique URL string
    - `created_at`: timestamp when the row was created
    """

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    checks = relationship(
        "HealthCheck",
        back_populates="url",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:  # pragma: no cover - convenience for debugging
        return f"<URL id={self.id} url={self.url!r}>"


class HealthCheck(Base):
    """Stores a single health check result for a monitored URL."""

    __tablename__ = "health_checks"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"), nullable=False, index=True)
    status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=False)
    is_up = Column(Boolean, nullable=False)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    url = relationship("URL", back_populates="checks")

    def __repr__(self) -> str:
        return (
            f"<HealthCheck id={self.id} url_id={self.url_id} status_code={self.status_code} "
            f"response_time_ms={self.response_time_ms} is_up={self.is_up}>")
