"""
class_taxonomy.py — DermaLens 8-Class Unified Taxonomy
========================================================
Single source of truth for all class definitions.
Import this everywhere instead of hardcoding class names.

Canonical location: model/class_taxonomy.py (project root package).

NOTE: Bowen's Disease (SCC in-situ) was excluded from this experiment
because it is absent from all four available datasets (HAM10000, ISIC2019,
PAD-UFES-20, DDI). The model trains on 8 classes. BOD can be added in a
future experiment using images sourced from the ISIC archive.
"""

# ── Class index definitions ───────────────────────────────────────────────
NUM_CLASSES = 8

CLASS_NAMES = [
    "Melanoma",                   # 0 — HIGH risk
    "Basal Cell Carcinoma",       # 1 — HIGH risk
    "Squamous Cell Carcinoma",    # 2 — HIGH risk
    "Actinic Keratosis",          # 3 — MEDIUM risk (pre-cancerous)
    "Melanocytic Nevi",           # 4 — LOW risk (dominant class)
    "Benign Keratosis",           # 5 — LOW risk
    "Dermatofibroma",             # 6 — LOW risk
    "Vascular Lesion",            # 7 — LOW risk
]

CLASS_SHORT = [
    "MEL", "BCC", "SCC", "AK", "NV", "BKL", "DF", "VASC"
]

# Risk tier per class — used for app display and threshold logic
# 0 = Low, 1 = Medium, 2 = High
CLASS_RISK_TIER = [2, 2, 2, 1, 0, 0, 0, 0]

RISK_TIER_NAMES  = ["Low risk", "Medium risk — monitor closely", "High risk — consult a dermatologist"]
RISK_TIER_COLORS = ["#27ae60", "#e67e22", "#e74c3c"]  # for Flutter UI

# Which classes are malignant (for binary fairness eval with DDI)
MALIGNANT_CLASSES = {0, 1, 2, 3}   # indices (MEL, BCC, SCC, AK)
BENIGN_CLASSES    = {4, 5, 6, 7}   # indices (NV, BKL, DF, VASC)

def class_idx_to_risk_tier(class_idx: int) -> int:
    """Returns 0 (low), 1 (medium), or 2 (high)."""
    return CLASS_RISK_TIER[class_idx]

def class_idx_to_binary(class_idx: int) -> int:
    """Returns 1 (malignant) or 0 (benign) — for DDI fairness eval."""
    return 1 if class_idx in MALIGNANT_CLASSES else 0


# ── Per-dataset raw label → class index mappings ──────────────────────────

# HAM10000: 'dx' column values
HAM10000_MAP = {
    "mel":   0,   # Melanoma
    "bcc":   1,   # Basal cell carcinoma
    "akiec": 3,   # Actinic keratosis
    "nv":    4,   # Melanocytic nevi
    "bkl":   5,   # Benign keratosis
    "df":    6,   # Dermatofibroma
    "vasc":  7,   # Vascular lesion
    # No SCC or Bowen's in HAM10000
}

# ISIC 2019: one-hot columns — check which col == 1.0
# Column order checked: MEL, NV, BCC, AK, BKL, SCC, DF, VASC
ISIC2019_MAP = {
    "MEL":  0,   # Melanoma
    "BCC":  1,   # Basal cell carcinoma
    "SCC":  2,   # Squamous cell carcinoma
    "AK":   3,   # Actinic keratosis
    "NV":   4,   # Melanocytic nevi
    "BKL":  5,   # Benign keratosis
    "DF":   6,   # Dermatofibroma
    "VASC": 7,   # Vascular lesion
    # No Bowen's in ISIC2019
}

# PAD-UFES-20: 'diagnostic' column values (uppercase)
PAD_UFES_MAP = {
    "MEL": 0,   # Melanoma
    "BCC": 1,   # Basal cell carcinoma
    "SCC": 2,   # Squamous cell carcinoma
    "ACK": 3,   # Actinic keratosis
    "NEV": 4,   # Melanocytic nevi
    "SEK": 5,   # Seborrhoeic keratosis → Benign keratosis
    # BOD absent from PAD-UFES-20 despite documentation; excluded from 8-class model
    # No DF, VASC in PAD-UFES-20
}

# DDI: no class labels — binary only (malignant=True/False)
# Used only for fairness evaluation, not multi-class training
# Maps to binary via class_idx_to_binary()


# ── Approximate class counts (for weight computation reference) ───────────
APPROX_CLASS_COUNTS = {
    0: 5687,    # Melanoma
    1: 4682,    # BCC
    2: 820,     # SCC
    3: 1924,    # AK
    4: 19824,   # NV (dominant; includes +244 from PAD-UFES-20 NEV)
    5: 3967,    # BKL
    6: 354,     # DF
    7: 395,     # VASC
    # Bowen's Disease excluded — zero samples across all datasets
}

def compute_class_weights_from_counts(counts_dict=None):
    """
    Compute inverse-frequency class weights.
    Returns a tensor of 8 floats, normalised so NV (class 4) = 1.0.

    Args:
        counts_dict: {class_idx: count} — uses APPROX_CLASS_COUNTS if None.
                     Replace with actual counts from your dataset after Cell 4.
    """
    import torch
    counts = counts_dict or APPROX_CLASS_COUNTS
    total  = sum(counts.values())
    # Inverse frequency
    weights = {k: total / (NUM_CLASSES * v) for k, v in counts.items()}
    # Normalise to NV (class 4) = 1.0
    nv_weight = weights[4]
    weights   = {k: v / nv_weight for k, v in weights.items()}
    return torch.tensor([weights[i] for i in range(NUM_CLASSES)], dtype=torch.float32)
