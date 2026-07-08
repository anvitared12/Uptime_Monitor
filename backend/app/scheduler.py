"""Background scheduler that periodically pings registered URLs.

This scheduler uses APScheduler's AsyncIO scheduler to run an async job
at a fixed interval. The job queries the `urls` table and calls the
`ping_url` utility for each entry, logging results.
"""
from __future__ import annotations

import asyncio
import logging
from typing import List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session

from app.checker import ping_url
from app.database import SessionLocal
from app.models import HealthCheck, URL


logger = logging.getLogger(__name__)


def get_db_session() -> Session:
    return SessionLocal()


async def check_all_urls() -> None:
    """Query all registered URLs, ping them, persist results, and log output."""
    db = get_db_session()
    try:
        urls: List[URL] = db.query(URL).all()
        if not urls:
            logger.info("No URLs registered; nothing to check.")
            return

        tasks = [ping_url(u.url, timeout=8.0) for u in urls]
        results = await asyncio.gather(*tasks)
        for url_obj, result in zip(urls, results):
            check = HealthCheck(
                url_id=url_obj.id,
                status_code=result.get("status"),
                response_time_ms=result["response_time_ms"],
                is_up=result["ok"],
            )
            db.add(check)
            logger.info("Persisted health check for %s: %s", url_obj.url, result)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


class Scheduler:
    def __init__(self, interval_seconds: int = 30):
        self._sched = AsyncIOScheduler()
        self._interval = interval_seconds

    def start(self) -> None:
        logger.info("Starting scheduler with interval %s seconds", self._interval)
        # AsyncIOScheduler can run coroutine functions directly on FastAPI's
        # running event loop.
        self._sched.add_job(
            check_all_urls,
            trigger=IntervalTrigger(seconds=self._interval),
            id="check_all_urls",
            replace_existing=True,
            coalesce=True,
            max_instances=1,
            misfire_grace_time=10,
        )
        self._sched.start()

    def shutdown(self) -> None:
        logger.info("Shutting down scheduler")
        self._sched.shutdown(wait=False)


scheduler = Scheduler()
