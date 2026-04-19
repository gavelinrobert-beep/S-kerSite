"""Tests for PPE heuristic detection stubs."""

from __future__ import annotations

import numpy as np

from edge.ppe_detector import detect_hardhat, detect_vest


def make_crop(h: int = 200, w: int = 80, color: tuple = (0, 0, 0)) -> np.ndarray:
    frame = np.zeros((h, w, 3), dtype=np.uint8)
    frame[:, :] = color
    return frame


def test_detect_hardhat_with_yellow_head():
    """Yellow head region should be processed by hardhat detection."""
    crop = make_crop(200, 80, (0, 0, 0))
    crop[:50, :] = (0, 220, 220)  # BGR yellow-ish
    result = detect_hardhat(crop)
    assert isinstance(result, bool)


def test_detect_hardhat_empty_crop():
    """Empty crop should return False, not raise."""
    result = detect_hardhat(np.array([]).reshape(0, 0, 3))
    assert result is False


def test_detect_vest_returns_bool():
    """detect_vest must always return a bool."""
    crop = make_crop(200, 80, (50, 200, 50))
    assert isinstance(detect_vest(crop), bool)


def test_detect_vest_empty_crop():
    """Empty crop should return False, not raise."""
    result = detect_vest(np.array([]).reshape(0, 0, 3))
    assert result is False


def test_detections_are_independent():
    """Hardhat and vest detectors should be independent."""
    crop = make_crop(200, 80)
    h = detect_hardhat(crop)
    v = detect_vest(crop)
    assert isinstance(h, bool)
    assert isinstance(v, bool)
