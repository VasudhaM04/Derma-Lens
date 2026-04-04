"""
GradCAM++ implementation for FairDermNet.
"""

from typing import Dict, Tuple

import cv2
import numpy as np
from pytorch_grad_cam import GradCAMPlusPlus
from pytorch_grad_cam.utils.image import show_cam_on_image


def generate_gradcam(model, input_tensor, target_layer_name="features.16.block.2"):
    """
    Returns:
        heatmap_overlay: np.ndarray [H, W, 3]
        raw_heatmap: np.ndarray [H, W]
    """
    named_modules = dict(model.backbone.named_modules())
    target_layers = [named_modules[target_layer_name]]
    cam = GradCAMPlusPlus(model=model, target_layers=target_layers)
    grayscale_cam = cam(input_tensor=input_tensor)[0]

    img = input_tensor[0].detach().cpu().numpy().transpose(1, 2, 0)
    img = (img - img.min()) / (img.max() - img.min() + 1e-8)
    overlay = show_cam_on_image(img.astype(np.float32), grayscale_cam, use_rgb=True)
    return overlay, grayscale_cam


def abcde_feature_scores(image: np.ndarray, heatmap: np.ndarray) -> Dict[str, float]:
    """
    Heuristic ABCDE score extraction from image + GradCAM heatmap.
    """
    h, w = heatmap.shape
    binary = (heatmap > np.percentile(heatmap, 75)).astype(np.uint8)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return {"A": 0.0, "B": 0.0, "C": 1.0, "D": 0.0, "E": 0.0}

    cnt = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True) + 1e-8
    x, y, bw, bh = cv2.boundingRect(cnt)

    asymmetry = float(abs(bw - bh) / max(bw, bh))
    border_irregularity = float((perimeter ** 2) / (4 * np.pi * area + 1e-8))
    color_var = float(min(6, max(1, np.unique(image.reshape(-1, 3), axis=0).shape[0] // 500)))
    diameter = float(max(bw, bh))
    evolution = 0.0

    return {"A": round(asymmetry * 2, 2), "B": round(border_irregularity, 2), "C": round(color_var, 2), "D": round(diameter, 2), "E": evolution}


compute_abcde_scores = abcde_feature_scores
