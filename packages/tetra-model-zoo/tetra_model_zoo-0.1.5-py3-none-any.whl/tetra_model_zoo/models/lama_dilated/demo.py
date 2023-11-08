from tetra_model_zoo.models._shared.repaint.demo import repaint_demo
from tetra_model_zoo.models.lama_dilated.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    LamaDilated,
)
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url

IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "test_images/test_input_image.png"
)
MASK_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "test_images/test_input_mask.png"
)


def main(is_test: bool = False):
    repaint_demo(LamaDilated, MODEL_ID, IMAGE_ADDRESS, MASK_ADDRESS, is_test)


if __name__ == "__main__":
    main()
