from typing import Optional

import torch

from tetra_model_zoo.utils.input_spec import InputSpec
from tetra_model_zoo.utils.quantization import (
    QNNPackQuantizationMixin,
    get_image_quantization_samples,
)
from tetra_model_zoo.utils.zoo_base_class import TetraZooModel

MODEL_ASSET_VERSION = 1
MODEL_ID = __name__.split(".")[-2]
IMAGENET_DIM = 224


class ImagenetClassifier(TetraZooModel, QNNPackQuantizationMixin):
    """
    Base class for all Imagenet Classifier models within the model zoo.
    """

    def __init__(
        self,
        net: torch.nn.Module,
        should_quantize: bool = False,
        quantization_samples_path: Optional[str] = None,
    ):
        """
        Basic initializer which takes in a pretrained classifier network.
        Subclasses can choose to implement their own __init__ and forward methods.
        """
        super().__init__()
        self.net = net

        self.is_quantized = should_quantize
        if not (self.is_quantized) and quantization_samples_path is not None:
            raise ValueError(
                "`quantization_samples_path` should only be set if `quantize=True`."
            )

        self.eval()

        if self.is_quantized:
            quantization_samples = get_image_quantization_samples(
                quantization_samples_path
            )
            self.quantize_e2e(quantization_samples)

    def forward(self, image_tensor: torch.Tensor):
        """
        Predict class probabilities for an input `image`.

        Parameters:
            image: A [1, 3, 224, 224] image.
                   Assumes image has been resized and normalized using the
                   standard preprocessing method for PyTorch Imagenet models.

                   Pixel values pre-processed for encoder consumption.
                   Range: float[0, 1]
                   3-channel Color Space: RGB

        Returns:
            A [1, 1000] where each value is the log-likelihood of
            the image belonging to the corresponding Imagenet class.
        """
        return self.net(image_tensor)

    def get_input_spec(
        self,
    ) -> InputSpec:
        """
        Returns the input specification (name -> (shape, type). This can be
        used to submit profiling job on TetraHub.
        """
        return {"image": ((1, 3, IMAGENET_DIM, IMAGENET_DIM), "float32")}

    @classmethod
    def from_pretrained(
        cls,
        weights: Optional[str] = None,
        should_quantize: bool = False,
        quantization_samples_path: Optional[str] = None,
    ) -> "ImagenetClassifier":
        # To be implemented by subclasses
        raise NotImplementedError
