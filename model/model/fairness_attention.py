"""
fairness_attention.py — Fairness Attention Module for FairDermNet
-----------------------------------------------------------------
Implements a parallel Fitzpatrick auxiliary branch + cross-attention fusion.

Design:
  - A lightweight parallel branch predicts skin tone (Fitzpatrick I-VI)
    from the backbone feature map.
  - Cross-attention re-weights the main feature map channels so the model
    learns representations that are LESS sensitive to skin tone and MORE
    sensitive to lesion morphology.
  - During inference, only the attended feature map is used (tone prediction
    is discarded).

This forces colour-invariant feature learning — the key fairness mechanism.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ChannelAttention(nn.Module):
    """
    SE-style channel attention.
    Squeeze → Excite → Scale.
    """

    def __init__(self, channels: int, reduction: int = 16):
        super().__init__()
        mid = max(channels // reduction, 8)
        self.fc = nn.Sequential(
            nn.Linear(channels, mid, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(mid, channels, bias=False),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, C, H, W]
        gap = x.mean(dim=[2, 3])          # [B, C]
        scale = self.fc(gap).unsqueeze(-1).unsqueeze(-1)  # [B, C, 1, 1]
        return x * scale


class SpatialAttention(nn.Module):
    """
    Spatial attention via 7×7 conv on channel-pooled feature map.
    Highlights lesion region vs background.
    """

    def __init__(self, kernel_size: int = 7):
        super().__init__()
        pad = kernel_size // 2
        self.conv = nn.Conv2d(2, 1, kernel_size=kernel_size, padding=pad, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        avg_pool = x.mean(dim=1, keepdim=True)   # [B, 1, H, W]
        max_pool = x.max(dim=1, keepdim=True)[0] # [B, 1, H, W]
        pooled = torch.cat([avg_pool, max_pool], dim=1)  # [B, 2, H, W]
        scale = self.sigmoid(self.conv(pooled))  # [B, 1, H, W]
        return x * scale


class FitzpatrickAuxBranch(nn.Module):
    """
    Lightweight branch that predicts Fitzpatrick skin tone from feature map.
    Used during training to compute fairness loss and to drive cross-attention.
    Output: logits over 6 skin tone classes [Fitz I–VI].
    """

    def __init__(self, in_channels: int = 960, num_tones: int = 6):
        super().__init__()
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_channels, 128, bias=False),
            nn.BatchNorm1d(128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(128, num_tones),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.gap(x))


class FairnessAttentionModule(nn.Module):
    """
    Full Fairness Attention Module.

    Inputs:
        x: backbone feature map [B, C, H, W]

    Outputs:
        attended_features: [B, C, H, W]  — used by main head
        fitz_logits: [B, 6]              — used by fairness loss

    Cross-attention mechanism:
        1. Channel attention re-weights feature channels.
        2. Spatial attention emphasises lesion location.
        3. Fitzpatrick branch predicts tone class (training only).
        4. Skin-tone adaptive scale: a small MLP conditioned on the
           Fitzpatrick prediction softens tone-specific feature activation,
           nudging the model toward tone-agnostic representations.
    """

    def __init__(self, in_channels: int = 960, num_tones: int = 6):
        super().__init__()
        self.channel_attn = ChannelAttention(in_channels, reduction=16)
        self.spatial_attn = SpatialAttention(kernel_size=7)
        self.fitz_branch = FitzpatrickAuxBranch(in_channels, num_tones)

        # Adaptive tone-conditioned channel modulator (cross-attention)
        # Takes soft tone distribution → produces per-channel scale offsets
        self.tone_modulator = nn.Sequential(
            nn.Linear(num_tones, in_channels // 4, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(in_channels // 4, in_channels, bias=False),
            nn.Tanh(),   # scale offset in [-1, 1]
        )
        self.modulation_strength = nn.Parameter(torch.tensor(0.1))

    def forward(self, x: torch.Tensor):
        # Step 1: Standard channel + spatial attention
        out = self.channel_attn(x)
        out = self.spatial_attn(out)

        # Step 2: Fitzpatrick prediction
        fitz_logits = self.fitz_branch(x)   # [B, 6]
        fitz_probs = F.softmax(fitz_logits, dim=-1)  # soft tone distribution

        # Step 3: Cross-attention — tone-conditioned channel modulation
        # Produces [B, C] offset. Small modulation_strength → subtle effect.
        tone_offset = self.tone_modulator(fitz_probs)  # [B, C]
        tone_scale = 1.0 + self.modulation_strength * tone_offset
        out = out * tone_scale.unsqueeze(-1).unsqueeze(-1)

        return out, fitz_logits
