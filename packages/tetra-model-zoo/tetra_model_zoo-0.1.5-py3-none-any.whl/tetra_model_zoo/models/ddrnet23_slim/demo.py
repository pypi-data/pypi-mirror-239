import argparse

from tetra_model_zoo.models.ddrnet23_slim.app import DDRNetApp
from tetra_model_zoo.models.ddrnet23_slim.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    DDRNet,
)
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image

INPUT_IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "test_input_image.png"
)


# Run DDRNet end-to-end on a sample image.
# The demo will display a image with the predicted segmentation map overlaid.
def main(is_test: bool = False):
    # Demo parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--weights",
        type=str,
        default=None,
        help="DDRNet checkpoint `.pt` path on disk.",
    )
    parser.add_argument(
        "--image",
        type=str,
        default=INPUT_IMAGE_ADDRESS,
        help="image file path or URL",
    )
    args = parser.parse_args([] if is_test else None)

    # Load image & model
    model = DDRNet.from_pretrained(args.weights)
    image = load_image(args.image, MODEL_ID)
    print("Model Loaded")

    app = DDRNetApp(model)
    output_img = app.segment_image(image)[0]
    if not is_test:
        output_img.show()


if __name__ == "__main__":
    main()
