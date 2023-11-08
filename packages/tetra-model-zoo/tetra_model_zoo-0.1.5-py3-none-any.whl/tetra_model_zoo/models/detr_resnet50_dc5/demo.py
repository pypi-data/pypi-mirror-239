from tetra_model_zoo.models._shared.detr.demo import detr_demo
from tetra_model_zoo.models.detr_resnet50_dc5.model import (
    DEFAULT_WEIGHTS,
    MODEL_ASSET_VERSION,
    MODEL_ID,
    DETRResNet50DC5,
)
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url

IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "detr_test_image.jpg"
)


# Run DETR app end-to-end on a sample image.
# The demo will display the predicted mask in a window.
def main(is_test: bool = False):
    detr_demo(DETRResNet50DC5, MODEL_ID, DEFAULT_WEIGHTS, IMAGE_ADDRESS, is_test)


if __name__ == "__main__":
    main()
