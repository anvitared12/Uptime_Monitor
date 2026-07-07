"""Inspect saved health check records in the database.

Run from the backend directory:
    python -m app.inspect_health_checks
"""
from app.database import SessionLocal
from app.models import HealthCheck


def main() -> None:
    db = SessionLocal()
    try:
        checks = db.query(HealthCheck).order_by(HealthCheck.id).all()
        print(f"Found {len(checks)} health checks")
        for check in checks:
            print(
                f"id={check.id}, url_id={check.url_id}, status={check.status_code}, "
                f"response_time_ms={check.response_time_ms}, is_up={check.is_up}, "
                f"checked_at={check.checked_at}"
            )
    finally:
        db.close()


if __name__ == "__main__":
    main()
