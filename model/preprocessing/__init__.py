from .adaptive_normalization import apply_clahe
from .augmentation_pipeline import (
    get_train_transforms,
    get_val_transforms,
    get_tta_transforms,
)
from .hair_removal import remove_hair
from .lesion_segmentation import segment_lesion
from .skin_tone_estimation import estimate_ita, ita_to_fitzpatrick


def full_pipeline(image):
    """Basic end-to-end preprocessing composition."""
    lesion_mask = segment_lesion(image)
    no_hair = remove_hair(image)
    normalized = apply_clahe(no_hair)
    ita = estimate_ita(normalized, lesion_mask)
    fitzpatrick_idx = ita_to_fitzpatrick(ita)
    return normalized, lesion_mask, ita, fitzpatrick_idx
