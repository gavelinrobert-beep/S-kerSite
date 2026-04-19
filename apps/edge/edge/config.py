"""Edge worker configuration loaded from environment."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    ingest_api_url: str = os.getenv("INGEST_API_URL", "http://localhost:8000/events/ingest")
    ingest_api_key: str = os.getenv("INGEST_API_KEY", "dev_edge_key")
    rtsp_url: str = os.getenv("RTSP_URL", "")
    mock_mode: bool = os.getenv("MOCK_MODE", "false").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    default_camera_id: str = os.getenv("DEFAULT_CAMERA_ID", "cam-001")
    mock_interval_seconds: float = float(os.getenv("MOCK_INTERVAL_SECONDS", "15"))


settings = Settings()
