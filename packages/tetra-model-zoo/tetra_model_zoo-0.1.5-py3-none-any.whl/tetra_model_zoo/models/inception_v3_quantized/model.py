from typing import Optional

from tetra_model_zoo.models.inception_v3.model import MODEL_ID as SOURCE_MODEL_ID
from tetra_model_zoo.models.inception_v3.model import ImagenetClassifier, InceptionNetV3
from tetra_model_zoo.utils.quantization import QUANTIZED_MODEL_ID_SUFFIX

MODEL_ID = SOURCE_MODEL_ID + QUANTIZED_MODEL_ID_SUFFIX


class InceptionNetV3Quantized(InceptionNetV3):
    """Copy of InceptionNetV3, with should_quantize defaulting to True."""

    @classmethod
    def from_pretrained(
        cls,
        weights: Optional[str] = None,
        should_quantize: bool = True,
        quantization_samples_path: Optional[str] = None,
    ) -> ImagenetClassifier:
        return InceptionNetV3.from_pretrained(
            weights, should_quantize, quantization_samples_path
        )
