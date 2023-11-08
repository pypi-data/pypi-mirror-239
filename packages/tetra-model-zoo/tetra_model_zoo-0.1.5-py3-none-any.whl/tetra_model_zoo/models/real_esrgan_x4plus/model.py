from __future__ import annotations

import torch
import torch.nn.functional as F

from tetra_model_zoo.utils.asset_loaders import SourceAsRoot, download_data
from tetra_model_zoo.utils.input_spec import InputSpec

# The architecture for this RealESRGAN model comes from the original ESRGAN repo
REALESRGAN_SOURCE_REPOSITORY = "https://github.com/xinntao/ESRGAN"
REALESRGAN_SOURCE_REPO_COMMIT = "73e9b634cf987f5996ac2dd33f4050922398a921"
MODEL_ID = __name__.split(".")[-2]
MODEL_ASSET_VERSION = 2
DEFAULT_WEIGHTS = "RealESRGAN_x4plus"
DEFAULT_WEIGHTS_URL = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
PRE_PAD = 10
SCALE = 4


class Real_ESRGAN_x4plus(torch.nn.Module):
    """Exportable RealESRGAN upscaler, end-to-end."""

    def __init__(
        self,
        realesrgan_model: torch.nn.Module,
    ) -> None:
        super().__init__()
        self.model = realesrgan_model

    @staticmethod
    def from_pretrained(
        weight_path: str = DEFAULT_WEIGHTS,
    ) -> Real_ESRGAN_x4plus:
        """Load RealESRGAN from a weightfile created by the source RealESRGAN repository."""

        # Load PyTorch model from disk
        realesrgan_model = _load_realesrgan_source_model_from_weights(weight_path)

        return Real_ESRGAN_x4plus(realesrgan_model)

    def forward(self, image: torch.Tensor) -> torch.Tensor:
        """
        Run RealESRGAN on `image`, and produce an upscaled image

        Parameters:
            image: Pixel values pre-processed for GAN consumption.
                   Range: float[0, 1]
                   3-channel Color Space: RGB

        Returns:
            image: Pixel values
                   Range: float[0, 1]
                   3-channel Color Space: RGB
        """

        img = F.pad(image, (0, PRE_PAD, 0, PRE_PAD), "reflect")

        # upscale
        output = self.model(img)

        # post-process
        _, _, h, w = output.size()
        output = output[:, :, 0 : h - PRE_PAD * SCALE, 0 : w - PRE_PAD * SCALE]
        output_img = output.data.squeeze().float().cpu().clamp_(0, 1)

        return output_img

    def get_input_spec(
        self,
        image_size: tuple[int, int] | int = 320,
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


def _get_weightsfile_from_name(weights_name: str = DEFAULT_WEIGHTS):
    """Convert from names of weights files to the url for the weights file"""
    if weights_name == DEFAULT_WEIGHTS:
        return DEFAULT_WEIGHTS_URL
    return ""


def _load_realesrgan_source_model_from_weights(weights_name: str) -> torch.nn.Module:
    # Load RealESRGAN model from the source repository using the given weights.
    # Returns <source repository>.realesrgan.archs.srvgg_arch
    weights_url = _get_weightsfile_from_name(weights_name)

    with SourceAsRoot(
        REALESRGAN_SOURCE_REPOSITORY, REALESRGAN_SOURCE_REPO_COMMIT, MODEL_ID
    ):
        # download the weights file
        weights_path = download_data(weights_url, MODEL_ID)

        # necessary import. `archs` comes from the realesrgan repo.
        from basicsr.archs.rrdbnet_arch import RRDBNet

        realesrgan_model = RRDBNet(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_block=23,
            num_grow_ch=32,
            scale=SCALE,
        )
        pretrained_dict = torch.load(weights_path, map_location=torch.device("cpu"))

        if "params_ema" in pretrained_dict:
            keyname = "params_ema"
        else:
            keyname = "params"
        realesrgan_model.load_state_dict(pretrained_dict[keyname], strict=True)

        return realesrgan_model
