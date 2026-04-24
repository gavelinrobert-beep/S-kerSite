"""Tests for authentication endpoints."""

from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import hash_password
from api.models import User


async def create_test_user(db: AsyncSession) -> User:
    user = User(
        email="test@sakersite.se",
        hashed_password=hash_password("testpass123"),
        full_name="Test User",
        role="supervisor",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.mark.asyncio
async def test_login_success(client, db_session):
    await create_test_user(db_session)
    response = await client.post(
        "/auth/login", json={"email": "test@sakersite.se", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client, db_session):
    response = await client.post(
        "/auth/login", json={"email": "test@sakersite.se", "password": "wrong"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client, db_session):
    login_resp = await client.post(
        "/auth/login", json={"email": "test@sakersite.se", "password": "testpass123"}
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    me_resp = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "test@sakersite.se"
