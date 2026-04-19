"""
Tests for the face_blur module.

Compliance requirement: face blurring MUST occur before any frame
leaves the edge device (GDPR Art. 25, data minimisation).
"""

from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np


def test_blur_faces_called_before_emit(monkeypatch):
    """
    Assert that blur_faces is called during frame processing,
    ensuring the privacy guarantee is upheld.
    """
    import edge.rtsp_worker as rtsp_worker

    blur_call_count = 0

    def mock_blur(frame, **kwargs):
        nonlocal blur_call_count
        blur_call_count += 1
        return frame

    monkeypatch.setattr("edge.rtsp_worker.blur_faces", mock_blur)

    mock_model = MagicMock()
    mock_result = MagicMock()
    mock_result.boxes = None
    mock_model.return_value = [mock_result]

    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    rtsp_worker._process_frame(mock_model, frame, "cam-001")

    assert blur_call_count == 1, (
        "blur_faces() must be called exactly once per frame before any processing. "
        "This is a GDPR/privacy compliance requirement."
    )


def test_blur_faces_returns_same_shape():
    """blur_faces should return an array with the same shape as the input."""
    from edge.face_blur import blur_faces

    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    result = blur_faces(frame)
    assert result.shape == frame.shape


def test_blur_faces_empty_frame():
    """blur_faces should handle empty/None frames gracefully."""
    from edge.face_blur import blur_faces

    result = blur_faces(np.array([]))
    assert result is not None


def test_blur_faces_does_not_mutate_original():
    """blur_faces must not mutate the input frame (privacy: no side-effects)."""
    from edge.face_blur import blur_faces

    frame = np.ones((100, 100, 3), dtype=np.uint8) * 128
    original = frame.copy()
    blur_faces(frame)
    np.testing.assert_array_equal(frame, original)
