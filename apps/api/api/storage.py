"""S3/MinIO storage utilities."""

from __future__ import annotations

import asyncio
import functools
from typing import Any

import boto3
import structlog
from botocore.exceptions import ClientError

from api.config import settings

log = structlog.get_logger()

_s3_client: Any = None


def _get_s3() -> Any:
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint_url,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
        )
    return _s3_client


async def ensure_bucket() -> None:
    """Create the S3 bucket if it doesn't exist."""
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _create_bucket_sync)
    except Exception as exc:
        log.warning("bucket_init_failed", error=str(exc))


def _create_bucket_sync() -> None:
    s3 = _get_s3()
    try:
        s3.head_bucket(Bucket=settings.s3_bucket)
    except ClientError as e:
        error_code = int(e.response["Error"]["Code"])
        if error_code == 404:
            s3.create_bucket(Bucket=settings.s3_bucket)
            log.info("s3_bucket_created", bucket=settings.s3_bucket)


async def generate_presigned_url(s3_key: str, expires_in: int = 3600) -> str | None:
    """Generate a presigned URL for an S3 object."""
    try:
        loop = asyncio.get_event_loop()
        url = await loop.run_in_executor(
            None,
            functools.partial(
                _get_s3().generate_presigned_url,
                "get_object",
                Params={"Bucket": settings.s3_bucket, "Key": s3_key},
                ExpiresIn=expires_in,
            ),
        )
        return url
    except Exception as exc:
        log.warning("presigned_url_failed", error=str(exc), key=s3_key)
        return None
