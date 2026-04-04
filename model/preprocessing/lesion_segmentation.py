"""
Simple lesion segmentation utilities.
"""

import cv2
import numpy as np


def segment_lesion(image: np.ndarray) -> np.ndarray:
    """Returns a binary lesion mask using Otsu thresholding in Lab L-channel."""
    if image is None or image.size == 0:
        raise ValueError("Input image is empty.")

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel = lab[:, :, 0]
    blur = cv2.GaussianBlur(l_channel, (5, 5), 0)
    _, mask = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    return mask
