from __future__ import annotations

import os

import torch

from tetra_model_zoo.utils.asset_loaders import SourceAsRoot, get_model_asset_url
from tetra_model_zoo.utils.input_spec import InputSpec
from tetra_model_zoo.utils.zoo_base_class import TetraZooModel

ESRGAN_SOURCE_REPOSITORY = "https://github.com/xinntao/ESRGAN"
ESRGAN_SOURCE_REPO_COMMIT = "73e9b634cf987f5996ac2dd33f4050922398a921"
MODEL_ID = __name__.split(".")[-2]
MODEL_ASSET_VERSION = 1


class ESRGAN(TetraZooModel):
    """Exportable ESRGAN super resolution applications, end-to-end."""

    def __init__(
        self,
        esrgan_model: torch.nn.Module,
    ) -> None:
        super().__init__()
        self.model = esrgan_model

    @classmethod
    def from_pretrained(cls, weights_path: str | None = None) -> ESRGAN:
        """Load ESRGAN from a weightfile created by the source ESRGAN repository."""

        # Load PyTorch model from disk
        esrgan_model = _load_esrgan_source_model_from_weights(weights_path)

        return cls(esrgan_model)

    def forward(self, image: torch.Tensor) -> torch.Tensor:
        """
        Run ESRGAN on `image`, and produce an upscaled image

        Parameters:
            image: Pixel values pre-processed for encoder consumption.
                   Range: float[0, 1]
                   3-channel Color Space: RGB

        Returns:
            image: Pixel values
                   Range: float[0, 1]
                   3-channel Color Space: RGB
        """
        return self.model(image)

    def get_input_spec(
        self,
        batch_size: int = 1,
        num_channels: int = 3,
        x: int = 224,
        y: int = 224,
    ) -> InputSpec:
        # Get the input specification ordered (name -> (shape, type)) pairs for this model.
        #
        # This can be used with the tetra_hub python API to declare
        # the model input specification upon submitting a profile job.
        return {"image": ((batch_size, num_channels, x, y), "float32")}


def _load_esrgan_source_model_from_weights(
    weights_path: str | None = None,
) -> torch.nn.Module:
    # Load ESRGAN model from the source repository using the given weights.
    weights_url = get_model_asset_url(
        MODEL_ID, MODEL_ASSET_VERSION, "RRDB_ESRGAN_x4.pth"
    )

    with SourceAsRoot(ESRGAN_SOURCE_REPOSITORY, ESRGAN_SOURCE_REPO_COMMIT, MODEL_ID):
        # download the weights file
        import requests

        if not weights_path:
            response = requests.get(weights_url)
            weights_path = os.path.join(os.getcwd(), "RRDB_ESRGAN_x4.pth")
            with open(weights_path, "wb") as file:
                file.write(response.content)

            print(f"Weights file downloaded as {weights_path}")

        # necessary import. `esrgan.RRDBNet_arch` comes from the esrgan repo.
        import RRDBNet_arch as arch

        esrgan_model = arch.RRDBNet(3, 3, 64, 23, gc=32)
        esrgan_model.load_state_dict(
            torch.load(weights_path, map_location=torch.device("cpu")), strict=True
        )
        return esrgan_model
