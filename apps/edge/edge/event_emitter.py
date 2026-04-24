"""
Event Emitter
=============
Posts PPE detection events to the SakerSite API.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import httpx
import structlog

from edge.config import settings

log = structlog.get_logger()


async def emit_event(
    camera_id: str,
    event_type: str,
    severity: str,
    detections: list[dict[str, Any]],
    metadata: dict[str, Any] | None = None,
) -> bool:
    """
    POST an event to the API ingest endpoint.

    Args:
        camera_id: ID of the camera that captured the event.
        event_type: Event type string, e.g. "ppe_violation".
        severity: "low", "medium", "high", or "critical".
        detections: List of per-person detection dicts.
        metadata: Optional additional metadata dict.

    Returns:
        True if successfully posted; False on error.
    """
    payload = {
        "camera_id": camera_id,
        "event_type": event_type,
        "severity": severity,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "detections": detections,
        "metadata": metadata or {},
    }

    headers = {
        "X-API-Key": settings.ingest_api_key,
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                settings.ingest_api_url,
                content=json.dumps(payload),
                headers=headers,
            )
            response.raise_for_status()
            log.info(
                "event_emitted",
                camera_id=camera_id,
                event_type=event_type,
                severity=severity,
                status_code=response.status_code,
            )
            return True
    except httpx.HTTPError as exc:
        log.warning("event_emit_failed", error=str(exc), camera_id=camera_id)
        return False
