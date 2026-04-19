"""Compliance/audit-log endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.auth import require_roles
from api.database import get_db
from api.models import AuditLog, User
from api.schemas import AuditLogResponse

router = APIRouter()


@router.get("/audit-log", response_model=list[AuditLogResponse])
async def get_audit_log(
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles("admin", "safety_manager")),
):
    result = await db.execute(
        select(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()
