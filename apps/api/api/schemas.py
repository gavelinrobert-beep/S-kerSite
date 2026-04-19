"""Pydantic v2 request/response schemas."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime


# ---------------------------------------------------------------------------
# Camera
# ---------------------------------------------------------------------------

class CameraCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    location: str | None = None
    rtsp_url: str | None = None
    is_active: bool = True


class CameraUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    rtsp_url: str | None = None
    is_active: bool | None = None


class CameraResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    location: str | None
    rtsp_url: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

class DetectionCreate(BaseModel):
    person_id: int
    bbox: list[int] | None = None
    hardhat_detected: bool
    vest_detected: bool
    confidence: float | None = None


class EventIngest(BaseModel):
    """Posted by edge worker to /events/ingest."""
    camera_id: str
    event_type: str
    severity: str
    started_at: datetime
    detections: list[DetectionCreate] = []
    metadata: dict[str, Any] | None = None


class EventUpdate(BaseModel):
    status: str | None = None


class DetectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    person_id: int
    bbox: list[int] | None
    hardhat_detected: bool
    vest_detected: bool
    confidence: float | None


class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    camera_id: uuid.UUID
    event_type: str
    severity: str
    status: str
    started_at: datetime
    ended_at: datetime | None
    clip_s3_key: str | None
    thumbnail_s3_key: str | None
    metadata_: dict | None = Field(None, alias="metadata")
    created_at: datetime
    detections: list[DetectionResponse] = []


# ---------------------------------------------------------------------------
# Audit log
# ---------------------------------------------------------------------------

class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID | None
    action: str
    resource_type: str
    resource_id: str | None
    ip_address: str | None
    details: dict | None
    created_at: datetime
