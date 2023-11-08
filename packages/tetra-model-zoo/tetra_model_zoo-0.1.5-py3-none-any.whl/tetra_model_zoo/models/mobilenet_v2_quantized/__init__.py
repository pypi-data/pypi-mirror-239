from tetra_model_zoo.models._shared.imagenet_classifier.app import (  # noqa: F401
    ImagenetClassifierApp as App,
)
from tetra_model_zoo.models.mobilenet_v2_quantized.model import (
    MODEL_ID,
    SOURCE_MODEL_ID,
)
from tetra_model_zoo.models.mobilenet_v2_quantized.model import (  # noqa: F401
    MobileNetV2Quantized as Model,
)
from tetra_model_zoo.utils.quantization import QUANTIZED_MODEL_ID_SUFFIX

MODEL_ID = SOURCE_MODEL_ID + QUANTIZED_MODEL_ID_SUFFIX
