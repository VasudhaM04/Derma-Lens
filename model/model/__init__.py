"""model/__init__.py"""
from .fairdermet import FairDermNet
from .loss_functions import FairnessAwareLoss, compute_class_weights
from .gem_pooling import GeMPooling
from .fairness_attention import FairnessAttentionModule
from .class_taxonomy import (
    CLASS_NAMES, CLASS_SHORT, CLASS_RISK_TIER,
    NUM_CLASSES, MALIGNANT_CLASSES, BENIGN_CLASSES,
    HAM10000_MAP, ISIC2019_MAP, PAD_UFES_MAP,
    compute_class_weights_from_counts,
)

__all__ = [
    "FairDermNet",
    "FairnessAwareLoss",
    "compute_class_weights",
    "GeMPooling",
    "FairnessAttentionModule",
    "CLASS_NAMES",
    "CLASS_SHORT",
    "CLASS_RISK_TIER",
    "NUM_CLASSES",
    "MALIGNANT_CLASSES",
    "BENIGN_CLASSES",
    "HAM10000_MAP",
    "ISIC2019_MAP",
    "PAD_UFES_MAP",
    "compute_class_weights_from_counts",
]
