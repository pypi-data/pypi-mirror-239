from __future__ import annotations

import torch
import torchvision.models as tv_models

from tetra_model_zoo.utils.input_spec import InputSpec

MODEL_ID = __name__.split(".")[-2]
MODEL_ASSET_VERSION = 1
DEFAULT_WEIGHTS = "COCO_WITH_VOC_LABELS_V1"
NUM_CLASSES = 21


class FCN_ResNet50(torch.nn.Module):
    """Exportable FCNresNet50 image segmentation applications, end-to-end."""

    def __init__(
        self,
        fcn_model: torch.nn.Module,
    ) -> None:
        super().__init__()
        self.model = fcn_model

    @staticmethod
    def from_pretrained(weights: str = DEFAULT_WEIGHTS) -> FCN_ResNet50:
        model = tv_models.segmentation.fcn_resnet50(weights=weights).eval()
        return FCN_ResNet50(model)

    def forward(self, image: torch.Tensor) -> torch.Tensor:
        """
        Run FCN_ResNet50 on `image`, and produce a tensor of classes for segmentation

        Parameters:
            image: Pixel values pre-processed for model consumption.
                   Range: float[0, 1]
                   3-channel Color Space: RGB

        Returns:
            tensor: 1x21xHxW tensor of class logits per pixel
        """
        return self.model(image)

    def get_input_spec(
        self,
        image_size: tuple[int, int] | int = 224,
        batch_size: int = 1,
        num_channels: int = 3,
    ) -> InputSpec:
        # Get the input specification ordered (name -> (shape, type)) pairs for this model.
        #
        # This can be used with the tetra_hub python API to declare
        # the model input specification upon submitting a profile job.
        if isinstance(image_size, int):
            image_size = (image_size, image_size)
        return {"image": ((batch_size, num_channels, *image_size), "float32")}
