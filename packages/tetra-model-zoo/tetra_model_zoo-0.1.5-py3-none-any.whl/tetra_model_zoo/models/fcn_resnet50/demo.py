import argparse

from tetra_model_zoo.models.fcn_resnet50.app import FCN_ResNet50App
from tetra_model_zoo.models.fcn_resnet50.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    FCN_ResNet50,
)
from tetra_model_zoo.models.fcn_resnet50.test import INPUT_IMAGE_ADDRESS
from tetra_model_zoo.utils.asset_loaders import load_image


def main():
    # Demo parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        type=str,
        default=INPUT_IMAGE_ADDRESS,
        help="image file path or URL.",
    )
    parser.add_argument(
        "--weights", type=str, default=DEFAULT_WEIGHTS, help="Model weights"
    )

    args = parser.parse_args()

    # This FCN ResNet 50 demo comes from
    # https://pytorch.org/hub/pytorch_vision_fcn_resnet101/
    # load image and model
    image = load_image(args.image, MODEL_ID)
    input_image = image.convert("RGB")
    app = FCN_ResNet50App(FCN_ResNet50.from_pretrained(args.weights))
    output = app.predict(input_image, False)

    output.show()


if __name__ == "__main__":
    main()
