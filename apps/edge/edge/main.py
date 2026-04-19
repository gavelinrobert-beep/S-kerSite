"""
SakerSite Edge Worker
=====================
RTSP ingest -> YOLO person detection -> PPE heuristic -> face blur -> event POST

Run with --mock to generate synthetic events without a real camera feed.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys

import structlog

from edge.config import settings
from edge.mock_generator import run_mock_loop
from edge.rtsp_worker import run_rtsp_loop


def configure_logging() -> None:
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level.upper(), logging.INFO)
        ),
        logger_factory=structlog.PrintLoggerFactory(),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SakerSite edge PPE detection worker")
    parser.add_argument(
        "--mock",
        action="store_true",
        default=os.getenv("MOCK_MODE", "false").lower() == "true",
        help="Run in mock mode (generate synthetic events, no camera required)",
    )
    parser.add_argument(
        "--rtsp-url",
        default=os.getenv("RTSP_URL"),
        help="RTSP stream URL",
    )
    return parser.parse_args()


async def main() -> None:
    configure_logging()
    log = structlog.get_logger()
    args = parse_args()

    if args.mock:
        log.info("Starting edge worker in MOCK mode")
        await run_mock_loop()
    else:
        if not args.rtsp_url:
            log.error("RTSP_URL not set and --mock not specified. Exiting.")
            sys.exit(1)
        log.info("Starting edge worker", rtsp_url=args.rtsp_url)
        await run_rtsp_loop(args.rtsp_url)


if __name__ == "__main__":
    asyncio.run(main())
