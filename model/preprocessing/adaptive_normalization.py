"""
CLAHE (Contrast Limited Adaptive Histogram Equalization) per-channel.
Skin-tone adaptive preprocessing.
"""

import cv2


def apply_clahe(image, clip_limit=2.0, tile_grid_size=(8, 8)):
    if image is None:
        raise ValueError("Input image is empty.")
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    l_eq = clahe.apply(l)
    merged = cv2.merge((l_eq, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
