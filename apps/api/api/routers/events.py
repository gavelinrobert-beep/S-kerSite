"""Event endpoints including ingest (called by edge worker)."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.auth import get_current_user
from api.config import settings
from api.database import get_db
from api.models import Camera, Event, EventDetection, User
from api.schemas import EventIngest, EventResponse, EventUpdate
from api.websocket import broadcast_event

router = APIRouter()


def _verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key_edge:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")


@router.post("/ingest", status_code=status.HTTP_201_CREATED)
async def ingest_event(
    body: EventIngest,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(_verify_api_key),
):
    """Called by edge worker to record a new PPE event."""
    try:
        cam_uuid = uuid.UUID(body.camera_id)
        result = await db.execute(select(Camera).where(Camera.id == cam_uuid))
    except ValueError:
        result = await db.execute(select(Camera).where(Camera.name == body.camera_id))

    camera = result.scalar_one_or_none()
    if camera is None:
        # Auto-create camera for mock/demo purposes
        camera = Camera(name=body.camera_id, is_active=True)
        db.add(camera)
        await db.flush()

    event = Event(
        camera_id=camera.id,
        event_type=body.event_type,
        severity=body.severity,
        status="new",
        started_at=body.started_at,
        metadata_=body.metadata,
    )
    db.add(event)
    await db.flush()

    for det in body.detections:
        detection = EventDetection(
            event_id=event.id,
            person_id=det.person_id,
            bbox=det.bbox,
            hardhat_detected=det.hardhat_detected,
            vest_detected=det.vest_detected,
            confidence=det.confidence,
        )
        db.add(detection)

    await db.flush()
    await db.refresh(event)

    await broadcast_event(
        {
            "id": str(event.id),
            "camera_id": str(event.camera_id),
            "event_type": event.event_type,
            "severity": event.severity,
            "status": event.status,
            "started_at": event.started_at.isoformat(),
        }
    )

    return {"id": str(event.id), "status": "created"}


@router.get("", response_model=list[EventResponse])
async def list_events(
    camera_id: Optional[uuid.UUID] = Query(None),
    event_type: Optional[str] = Query(None),
    event_status: Optional[str] = Query(None, alias="status"),
    since: Optional[datetime] = Query(None),
    until: Optional[datetime] = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = select(Event).options(selectinload(Event.detections))

    if camera_id:
        query = query.where(Event.camera_id == camera_id)
    if event_type:
        query = query.where(Event.event_type == event_type)
    if event_status:
        query = query.where(Event.status == event_status)
    if since:
        query = query.where(Event.started_at >= since)
    if until:
        query = query.where(Event.started_at <= until)

    query = query.order_by(Event.started_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Event)
        .options(selectinload(Event.detections))
        .where(Event.id == event_id)
    )
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    from api.audit import log_access
    await log_access(
        db,
        user_id=current_user.id,
        action="view_event",
        resource_type="event",
        resource_id=str(event_id),
    )

    return event


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: uuid.UUID,
    body: EventUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Event)
        .options(selectinload(Event.detections))
        .where(Event.id == event_id)
    )
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    valid_statuses = {"new", "acknowledged", "resolved", "false_positive"}
    if body.status and body.status not in valid_statuses:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")

    if body.status:
        event.status = body.status

    await db.flush()
    await db.refresh(event)

    from api.audit import log_access
    await log_access(
        db,
        user_id=current_user.id,
        action="update_event_status",
        resource_type="event",
        resource_id=str(event_id),
        details={"new_status": body.status},
    )

    return event
