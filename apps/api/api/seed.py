"""
Database seed script.
Creates:
  - 1 admin user: admin@sakersite.se / changeme
  - 2 demo cameras
  - 5 demo events
"""

from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timedelta, timezone

import structlog

from api.auth import hash_password
from api.database import AsyncSessionLocal, engine
from api.models import Base, Camera, Event, EventDetection, User

log = structlog.get_logger()


async def seed() -> None:
    log.info("seeding_database")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        from sqlalchemy.future import select

        existing = await db.execute(select(User).where(User.email == "admin@sakersite.se"))
        if existing.scalar_one_or_none():
            log.info("database_already_seeded")
            return

        admin = User(
            email="admin@sakersite.se",
            hashed_password=hash_password("changeme"),
            full_name="Admin Sakersite",
            role="admin",
        )
        db.add(admin)

        cam1 = Camera(
            id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
            name="cam-001",
            location="Main Entrance",
            is_active=True,
        )
        cam2 = Camera(
            id=uuid.UUID("00000000-0000-0000-0000-000000000002"),
            name="cam-002",
            location="Scaffold Level 3",
            is_active=True,
        )
        db.add(cam1)
        db.add(cam2)
        await db.flush()

        now = datetime.now(timezone.utc)
        events_data = [
            ("missing_hardhat", "high", cam1.id, now - timedelta(minutes=5)),
            ("missing_vest", "medium", cam2.id, now - timedelta(minutes=12)),
            ("missing_hardhat_and_vest", "high", cam1.id, now - timedelta(hours=1)),
            ("missing_hardhat", "low", cam2.id, now - timedelta(hours=2)),
            ("missing_vest", "medium", cam1.id, now - timedelta(hours=3)),
        ]

        for event_type, severity, camera_id, started_at in events_data:
            event = Event(
                camera_id=camera_id,
                event_type=event_type,
                severity=severity,
                status="new",
                started_at=started_at,
                metadata_={"source": "seed"},
            )
            db.add(event)
            await db.flush()

            det = EventDetection(
                event_id=event.id,
                person_id=0,
                hardhat_detected=("hardhat" not in event_type),
                vest_detected=("vest" not in event_type),
                confidence=0.87,
            )
            db.add(det)

        await db.commit()
        log.info("seeding_complete")


if __name__ == "__main__":
    asyncio.run(seed())
