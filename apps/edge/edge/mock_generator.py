"""
Mock Event Generator
====================
Generates synthetic PPE violation events for demo/testing without a real camera.
Sends events to the API at a configurable interval (~15s by default).
"""

from __future__ import annotations

import asyncio
import random
from datetime import datetime, timezone
from typing import Any

import structlog

from edge.config import settings
from edge.event_emitter import emit_event

log = structlog.get_logger()

DEMO_CAMERAS = ["cam-001", "cam-002"]
SEVERITIES = ["low", "medium", "high"]
VIOLATION_TYPES = [
    "missing_hardhat",
    "missing_vest",
    "missing_hardhat_and_vest",
]


def _generate_detection(person_id: int) -> dict[str, Any]:
    """Generate a synthetic per-person detection record."""
    violation = random.choice(VIOLATION_TYPES)
    return {
        "person_id": person_id,
        "bbox": [
            random.randint(0, 600),
            random.randint(0, 400),
            random.randint(50, 200),
            random.randint(100, 300),
        ],
        "hardhat_detected": "hardhat" not in violation,
        "vest_detected": "vest" not in violation,
        "confidence": round(random.uniform(0.65, 0.99), 3),
    }


async def run_mock_loop() -> None:
    """
    Continuously emit synthetic events.

    Each iteration:
      1. Picks a random camera and number of people (1-3).
      2. Randomly generates PPE violation detections.
      3. Posts the event to the API.
      4. Sleeps for mock_interval_seconds.
    """
    log.info(
        "mock_loop_started",
        interval_seconds=settings.mock_interval_seconds,
    )

    while True:
        camera_id = random.choice(DEMO_CAMERAS)
        n_persons = random.randint(1, 3)
        detections = [_generate_detection(i) for i in range(n_persons)]

        severity = random.choice(SEVERITIES)
        event_type = "ppe_violation"

        await emit_event(
            camera_id=camera_id,
            event_type=event_type,
            severity=severity,
            detections=detections,
            metadata={
                "source": "mock",
                "generated_at": datetime.now(timezone.utc).isoformat(),
            },
        )

        await asyncio.sleep(settings.mock_interval_seconds)
