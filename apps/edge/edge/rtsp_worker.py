"""
RTSP Worker
===========
Real camera mode: ingests RTSP stream, runs YOLO person detection,
applies PPE heuristics, blurs faces, and emits events.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any

import numpy as np
import structlog

from edge.config import settings
from edge.event_emitter import emit_event
from edge.face_blur import blur_faces
from edge.ppe_detector import detect_hardhat, detect_vest

log = structlog.get_logger()

PERSON_CLASS_ID = 0


async def run_rtsp_loop(rtsp_url: str, camera_id: str | None = None) -> None:
    """
    Main RTSP ingest loop.

    NOTE: Requires ultralytics and opencv-python-headless packages,
    and a GPU or fast CPU for real-time inference.

    Args:
        rtsp_url: Full RTSP URL, e.g. rtsp://user:pass@192.168.1.100:554/stream1
        camera_id: Override camera id; defaults to settings.default_camera_id
    """
    import cv2
    from ultralytics import YOLO

    cam_id = camera_id or settings.default_camera_id

    # TODO: Replace yolov8n.pt with a fine-tuned PPE model once available.
    log.info("loading_yolo_model", model="yolov8n.pt")
    model = YOLO("yolov8n.pt")

    log.info("opening_rtsp_stream", url=rtsp_url)
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        log.error("rtsp_open_failed", url=rtsp_url)
        return

    frame_interval = 1.0  # process 1 frame/second; tune for performance
    last_process_time = 0.0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                log.warning("rtsp_frame_read_failed", url=rtsp_url)
                await asyncio.sleep(1.0)
                continue

            now = time.monotonic()
            if (now - last_process_time) < frame_interval:
                continue
            last_process_time = now

            detections = _process_frame(model, frame, cam_id)

            if detections:
                violations = [
                    d for d in detections
                    if not d["hardhat_detected"] or not d["vest_detected"]
                ]
                if violations:
                    await emit_event(
                        camera_id=cam_id,
                        event_type="ppe_violation",
                        severity=_compute_severity(violations),
                        detections=violations,
                    )

            await asyncio.sleep(0.01)
    finally:
        cap.release()
        log.info("rtsp_stream_closed", url=rtsp_url)


def _process_frame(model: Any, frame: np.ndarray, camera_id: str) -> list[dict[str, Any]]:
    """
    Run YOLO inference on a frame, then apply PPE heuristics to each person.

    Privacy guarantee: blur_faces() is called on the full frame FIRST, before
    any crop is extracted or stored.
    """
    # Step 1: Blur ALL faces before any further processing
    blurred_frame = blur_faces(frame)

    # Step 2: Run YOLO detection (on the blurred frame)
    results = model(blurred_frame, verbose=False)

    detections: list[dict[str, Any]] = []
    for result in results:
        boxes = result.boxes
        if boxes is None:
            continue
        for box in boxes:
            cls_id = int(box.cls[0].item())
            if cls_id != PERSON_CLASS_ID:
                continue

            conf = float(box.conf[0].item())
            x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]

            # Extract person crop from the already-blurred frame
            person_crop = blurred_frame[y1:y2, x1:x2]

            # Step 3: Apply PPE heuristics
            has_hardhat = detect_hardhat(person_crop)
            has_vest = detect_vest(person_crop)

            detections.append({
                "person_id": len(detections),
                "bbox": [x1, y1, x2 - x1, y2 - y1],
                "hardhat_detected": has_hardhat,
                "vest_detected": has_vest,
                "confidence": conf,
            })

    return detections


def _compute_severity(violations: list[dict[str, Any]]) -> str:
    """Compute event severity based on number of violations."""
    n = len(violations)
    if n >= 3:
        return "high"
    if n == 2:
        return "medium"
    return "low"
