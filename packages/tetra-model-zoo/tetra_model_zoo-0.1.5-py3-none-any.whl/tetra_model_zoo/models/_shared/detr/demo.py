from typing import Type

from PIL import Image

from tetra_model_zoo.models._shared.detr.app import DETRApp
from tetra_model_zoo.utils.args import get_model_cli_parser, model_from_cli_args
from tetra_model_zoo.utils.asset_loaders import load_image
from tetra_model_zoo.utils.zoo_base_class import TetraZooModel


# Run DETR app end-to-end on a sample image.
# The demo will display the predicted mask in a window.
def detr_demo(
    model: Type[TetraZooModel],
    model_id: str,
    default_weights: str,
    default_image: str,
    is_test: bool = False,
):
    # Demo parameters
    parser = get_model_cli_parser(model)
    parser.add_argument(
        "--image",
        type=str,
        default=default_image,
        help="test image file path or URL",
    )
    args = parser.parse_args([] if is_test else None)

    # Load image & model
    detr = model_from_cli_args(model, args)

    # Run app to scores, labels and boxes
    img = load_image(args.image, model_id)
    app = DETRApp(detr)
    pred_images = app.predict(img, default_weights)

    # Show the predicted boxes, scores and class names on the image.
    if not is_test:
        Image.fromarray(pred_images[0]).show()
