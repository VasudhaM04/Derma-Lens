"""
Black Top-Hat morphological transform for hair removal.
Input: BGR image (OpenCV format)
Output: hair-removed image
"""

import cv2
import numpy as np


def remove_hair(image: np.ndarray, kernel_size: int = 17) -> np.ndarray:
    if image is None or image.size == 0:
        raise ValueError("Input image is empty.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    _, hair_mask = cv2.threshold(blackhat, 10, 255, cv2.THRESH_BINARY)
    result = cv2.inpaint(image, hair_mask, inpaintRadius=1, flags=cv2.INPAINT_TELEA)
    return result
