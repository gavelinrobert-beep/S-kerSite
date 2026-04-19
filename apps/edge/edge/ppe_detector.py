"""
PPE Detection Heuristics
========================
Stub implementations for hardhat and high-vis vest detection.

TODO: Replace these heuristics with a fine-tuned YOLO PPE model.
      Recommended datasets for fine-tuning:
        - SH17: https://github.com/zivicmilos/sh17-ppe-detection
        - CHVG (Construction Hardhat & Vest on GitHub/Roboflow)
        - Roboflow Universe PPE datasets: https://universe.roboflow.com/

      Expected workflow:
        1. Download a PPE-annotated dataset in YOLO format.
        2. Fine-tune yolov8n.pt (or yolov8s.pt) on the dataset.
        3. Export fine-tuned weights as ppe_model.pt.
        4. Replace the heuristic functions below with real model inference.
        5. Map class ids to HARDHAT_CLASS_ID and VEST_CLASS_ID from training labels.
"""

from __future__ import annotations

import numpy as np

HARDHAT_CLASS_ID = 0  # TODO: set to actual class id from PPE model training
VEST_CLASS_ID = 1  # TODO: set to actual class id from PPE model training


def detect_hardhat(person_crop: np.ndarray) -> bool:
    """
    Stub: Returns True if a hardhat is detected on the person crop.

    Uses a colour heuristic on the top-quarter of the crop (hardhats are often
    yellow/orange/white in Swedish construction contexts).
    Replace with PPE model inference — see module docstring.
    """
    # TODO: Replace with PPE model inference
    if person_crop is None or person_crop.size == 0:
        return False

    h = person_crop.shape[0]
    head_region = person_crop[: max(1, h // 4), :]

    hsv = _bgr_to_hsv(head_region)
    yellow_mask = _in_range(hsv, (20, 80, 80), (40, 255, 255))
    orange_mask = _in_range(hsv, (5, 100, 100), (20, 255, 255))
    white_mask = _in_range(hsv, (0, 0, 200), (180, 30, 255))

    bright_pixels = int(yellow_mask.sum() + orange_mask.sum() + white_mask.sum())
    total_pixels = head_region.shape[0] * head_region.shape[1]
    if total_pixels == 0:
        return False

    return (bright_pixels / total_pixels) > 0.15


def detect_vest(person_crop: np.ndarray) -> bool:
    """
    Stub: Returns True if a high-visibility vest is detected on the person crop.

    Uses a colour heuristic on the torso region. Replace with PPE model inference
    — see module docstring.
    """
    # TODO: Replace with PPE model inference
    if person_crop is None or person_crop.size == 0:
        return False

    h = person_crop.shape[0]
    torso = person_crop[h // 4 : (3 * h) // 4, :]

    hsv = _bgr_to_hsv(torso)
    hivis_yellow = _in_range(hsv, (25, 100, 150), (45, 255, 255))
    hivis_orange = _in_range(hsv, (5, 150, 150), (18, 255, 255))

    bright_pixels = int(hivis_yellow.sum() + hivis_orange.sum())
    total_pixels = torso.shape[0] * torso.shape[1]
    if total_pixels == 0:
        return False

    return (bright_pixels / total_pixels) > 0.10


def _bgr_to_hsv(bgr: np.ndarray) -> np.ndarray:
    """Convert BGR uint8 image to HSV. Falls back to zeros if cv2 unavailable."""
    try:
        import cv2
        return cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    except Exception:
        return np.zeros_like(bgr)


def _in_range(
    hsv: np.ndarray,
    lower: tuple[int, int, int],
    upper: tuple[int, int, int],
) -> np.ndarray:
    """Return boolean mask where HSV pixels fall within [lower, upper]."""
    lo = np.array(lower, dtype=np.uint8)
    hi = np.array(upper, dtype=np.uint8)
    return np.all((hsv >= lo) & (hsv <= hi), axis=-1)
