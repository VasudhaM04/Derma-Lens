"""
ITA° (Individual Typology Angle) based skin tone estimation.
Maps continuous ITA score to approximate Fitzpatrick type (I-VI).
"""

import cv2
import numpy as np


def estimate_ita(image: np.ndarray, lesion_mask: np.ndarray) -> float:
    """Estimate ITA using surrounding skin pixels (inverse lesion mask)."""
    if image is None or image.size == 0:
        raise ValueError("Input image is empty.")
    if lesion_mask is None or lesion_mask.size == 0:
        raise ValueError("Lesion mask is empty.")

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB).astype(np.float32)
    skin_mask = (lesion_mask == 0)
    if np.count_nonzero(skin_mask) < 10:
        return 0.0

    l_vals = lab[:, :, 0][skin_mask]
    b_vals = lab[:, :, 2][skin_mask]
    b_vals = np.where(np.abs(b_vals) < 1e-5, 1e-5, b_vals)
    ita = np.degrees(np.arctan((l_vals - 50.0) / b_vals))
    return float(np.nanmean(ita))


def ita_to_fitzpatrick(ita: float) -> int:
    """Returns 0-5 corresponding to Fitzpatrick I-VI."""
    if ita > 55:
        return 0
    if 41 < ita <= 55:
        return 1
    if 28 < ita <= 41:
        return 2
    if 10 < ita <= 28:
        return 3
    if -30 < ita <= 10:
        return 4
    return 5
