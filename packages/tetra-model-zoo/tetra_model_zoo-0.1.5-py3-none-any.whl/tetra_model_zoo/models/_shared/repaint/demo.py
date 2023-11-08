import argparse
from typing import Type

from tetra_model_zoo.models._shared.repaint.app import RepaintMaskApp
from tetra_model_zoo.utils.args import get_model_cli_parser, model_from_cli_args
from tetra_model_zoo.utils.asset_loaders import load_image
from tetra_model_zoo.utils.zoo_base_class import TetraZooModel


#
# Run repaint app end-to-end on a sample image.
# The demo will display the predicted image in a window.
#
def repaint_demo(
    model_type: Type[TetraZooModel],
    model_id: str,
    default_image: str,
    default_mask: str,
    is_test: bool = False,
):
    # Demo parameters
    parser = argparse.ArgumentParser()
    parser = get_model_cli_parser(model_type)
    parser.add_argument(
        "--image",
        type=str,
        default=default_image,
        help="test image file path or URL",
    )
    parser.add_argument(
        "--mask",
        type=str,
        default=default_mask,
        help="test mask file path or URL",
    )
    args = parser.parse_args([] if is_test else None)

    # Load image & model
    model = model_from_cli_args(model_type, args)
    image = load_image(args.image, model_id)
    mask = load_image(args.mask, model_id)
    print("Model Loaded")

    # Run app
    app = RepaintMaskApp(model)
    image.show(title="Model Input")
    out = app.paint_mask_on_image(image, mask)[0]

    if not is_test:
        out.show(title="Repainted (Model Output)")
