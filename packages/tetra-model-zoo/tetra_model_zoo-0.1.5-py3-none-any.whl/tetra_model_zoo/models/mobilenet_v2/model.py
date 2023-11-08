from __future__ import annotations

from typing import Optional

import torchvision.models as tv_models

from tetra_model_zoo.models._shared.imagenet_classifier.model import ImagenetClassifier

MODEL_ID = __name__.split(".")[-2]
DEFAULT_WEIGHTS = "IMAGENET1K_V2"
DEFAULT_QUANTIZED_WEIGHTS = tv_models.quantization.MobileNet_V2_QuantizedWeights


class MobileNetV2(ImagenetClassifier):
    @classmethod
    def from_pretrained(
        cls,
        weights: Optional[str] = None,
        should_quantize: bool = False,
        quantization_samples_path: Optional[str] = None,
    ) -> ImagenetClassifier:
        if should_quantize:
            net = tv_models.quantization.mobilenet_v2(
                weights=weights or DEFAULT_QUANTIZED_WEIGHTS, quantize=False
            )
        else:
            net = tv_models.mobilenet_v2(weights=weights or DEFAULT_WEIGHTS)
        return cls(net, should_quantize, quantization_samples_path)
