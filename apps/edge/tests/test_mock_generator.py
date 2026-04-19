"""Tests for the mock event generator."""

from __future__ import annotations

import asyncio
import importlib
from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_mock_loop_emits_events():
    """Mock loop should call emit_event at least once."""
    emit_calls = []

    async def fake_emit(**kwargs):
        emit_calls.append(kwargs)
        return True

    mock_gen = importlib.import_module("edge.mock_generator")

    with patch.object(mock_gen, "emit_event", new=fake_emit):
        with patch("edge.mock_generator.settings") as mock_settings:
            mock_settings.mock_interval_seconds = 0.01
            mock_settings.default_camera_id = "cam-001"

            try:
                await asyncio.wait_for(mock_gen.run_mock_loop(), timeout=0.15)
            except asyncio.TimeoutError:
                pass

    assert len(emit_calls) >= 1, "Mock loop must emit at least one event"
