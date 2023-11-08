from __future__ import annotations

import torchvision.models as tv_models

from tetra_model_zoo.models._shared.imagenet_classifier.model import ImagenetClassifier

MODEL_ID = __name__.split(".")[-2]
DEFAULT_WEIGHTS = "IMAGENET1K_V2"


class ResNeXt101(ImagenetClassifier):
    @classmethod
    def from_pretrained(cls, weights: str = DEFAULT_WEIGHTS) -> ImagenetClassifier:
        net = tv_models.resnext101_32x8d(weights=weights)
        return cls(net)
