"""
SakerSite API — FastAPI application entry point.
"""

from __future__ import annotations

import logging

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings
from api.routers import auth, cameras, compliance, events, health, websocket

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(
        getattr(logging, settings.log_level.upper(), logging.INFO)
    ),
    logger_factory=structlog.PrintLoggerFactory(),
)

app = FastAPI(
    title="SakerSite API",
    description=(
        "Privacy-first AI PPE detection platform for Swedish construction sites. "
        "GDPR/EU-AI-Act compliant."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(cameras.router, prefix="/cameras", tags=["cameras"])
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(compliance.router, prefix="/compliance", tags=["compliance"])
app.include_router(websocket.router, tags=["websocket"])


@app.on_event("startup")
async def startup_event() -> None:
    log = structlog.get_logger()
    log.info("sakersite_api_started", version="0.1.0")
    from api.storage import ensure_bucket
    await ensure_bucket()
    from api.scheduler import start_scheduler
    start_scheduler()
