import argparse

from tetra_model_zoo.models.sinet.app import SINetApp
from tetra_model_zoo.models.sinet.model import DEFAULT_WEIGHTS, MODEL_ID, SINet
from tetra_model_zoo.models.sinet.test import INPUT_IMAGE_ADDRESS
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

    # load image and model
    image = load_image(args.image, MODEL_ID)
    input_image = image.convert("RGB")
    app = SINetApp(SINet.from_pretrained(args.weights))
    output = app.predict(input_image, False, False)
    output.save("sinet_demo_output.png")
    output.show()


if __name__ == "__main__":
    main()
