"""APScheduler background tasks (retention cleanup)."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from api.config import settings

log = structlog.get_logger()
_scheduler: AsyncIOScheduler | None = None


def start_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        return

    _scheduler = AsyncIOScheduler()
    _scheduler.add_job(
        _run_retention_cleanup,
        trigger="interval",
        hours=24,
        id="retention_cleanup",
        replace_existing=True,
    )
    _scheduler.start()
    log.info("scheduler_started")


async def _run_retention_cleanup() -> None:
    """Delete events (and their S3 clips) older than retention_days."""
    from api.database import AsyncSessionLocal
    from api.models import Event
    from sqlalchemy.future import select

    cutoff = datetime.now(timezone.utc) - timedelta(days=settings.retention_days)
    log.info("retention_cleanup_started", cutoff=cutoff.isoformat())

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Event).where(Event.created_at < cutoff))
        expired_events = result.scalars().all()

        for event in expired_events:
            if event.clip_s3_key:
                await _delete_s3_object(event.clip_s3_key)
            if event.thumbnail_s3_key:
                await _delete_s3_object(event.thumbnail_s3_key)
            await db.delete(event)

        await db.commit()
        log.info("retention_cleanup_done", deleted=len(expired_events))


async def _delete_s3_object(key: str) -> None:
    try:
        from api.storage import _get_s3

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: _get_s3().delete_object(Bucket=settings.s3_bucket, Key=key),
        )
    except Exception as exc:
        log.warning("s3_delete_failed", key=key, error=str(exc))
