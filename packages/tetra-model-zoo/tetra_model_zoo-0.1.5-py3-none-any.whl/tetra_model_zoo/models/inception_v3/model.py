from __future__ import annotations

from typing import Optional

import torchvision.models as tv_models

from tetra_model_zoo.models._shared.imagenet_classifier.model import ImagenetClassifier

MODEL_ID = __name__.split(".")[-2]
DEFAULT_WEIGHTS = "IMAGENET1K_V1"
DEFAULT_QUANTIZED_WEIGHTS = tv_models.quantization.Inception_V3_QuantizedWeights


class InceptionNetV3(ImagenetClassifier):
    @classmethod
    def from_pretrained(
        cls,
        weights: Optional[str] = None,
        should_quantize: bool = False,
        quantization_samples_path: Optional[str] = None,
    ) -> ImagenetClassifier:
        if should_quantize:
            net = tv_models.quantization.inception_v3(
                weights=weights or DEFAULT_QUANTIZED_WEIGHTS, quantize=False
            )
        else:
            net = tv_models.inception_v3(weights=weights or DEFAULT_WEIGHTS)
        return cls(net, should_quantize, quantization_samples_path)
