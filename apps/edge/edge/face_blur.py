"""
Face Blur Module
================
Blurs faces in a video frame BEFORE any data leaves the edge device.

This is a core privacy-by-design requirement:
  - GDPR Art. 25 (Data Protection by Design and by Default)
  - Kamerabevakningslagen (2018:1200) data minimisation principle

The face detection uses OpenCV's Haar Cascade classifier which runs on CPU
with no network calls. For higher accuracy consider replacing with a
lightweight face detector such as YuNet (cv2.FaceDetectorYN) or
MediaPipe Face Detection, both of which also run locally on the edge device.
"""

from __future__ import annotations

import numpy as np
import structlog

log = structlog.get_logger()

_cv2 = None
_face_cascade = None


def _get_cv2():
    global _cv2
    if _cv2 is None:
        import cv2 as cv2_module
        _cv2 = cv2_module
    return _cv2


def _get_face_cascade():
    """Load Haar cascade. Returns None if unavailable (e.g., in CI without model file)."""
    global _face_cascade
    if _face_cascade is None:
        cv2 = _get_cv2()
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        _face_cascade = cv2.CascadeClassifier(cascade_path)
        if _face_cascade.empty():
            log.warning("face_cascade_not_loaded", path=cascade_path)
            return None
    return _face_cascade


def blur_faces(frame: np.ndarray, blur_strength: int = 25) -> np.ndarray:
    """
    Detect and blur all faces in the given frame.

    This function MUST be called before any frame or crop is stored, uploaded,
    or transmitted outside the edge device.

    Args:
        frame: BGR numpy array (H x W x 3).
        blur_strength: Kernel size for Gaussian blur (must be odd). Higher = more blur.

    Returns:
        A new frame with all detected faces blurred. If no faces are detected
        or the cascade is unavailable, returns the original frame unchanged.
    """
    if frame is None or frame.size == 0:
        return frame

    cv2 = _get_cv2()
    cascade = _get_face_cascade()

    if cascade is None:
        log.debug("face_blur_skipped", reason="cascade_unavailable")
        return frame

    blurred_frame = frame.copy()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

    if len(faces) == 0:
        return blurred_frame

    k = blur_strength if blur_strength % 2 == 1 else blur_strength + 1

    for x, y, w, h in faces:
        roi = blurred_frame[y : y + h, x : x + w]
        blurred_roi = cv2.GaussianBlur(roi, (k, k), 0)
        blurred_frame[y : y + h, x : x + w] = blurred_roi

    log.debug("faces_blurred", count=len(faces))
    return blurred_frame


def blur_faces_applied(frame: np.ndarray) -> bool:
    """
    Returns True if the blur_faces function would process this frame
    (i.e., cascade is available). Used in compliance assertions.
    """
    return _get_face_cascade() is not None
