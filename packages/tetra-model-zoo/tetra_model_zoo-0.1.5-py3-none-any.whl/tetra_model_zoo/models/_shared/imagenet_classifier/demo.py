import json
from typing import Type

import torch

from tetra_model_zoo.models._shared.imagenet_classifier.app import ImagenetClassifierApp
from tetra_model_zoo.models._shared.imagenet_classifier.model import (
    MODEL_ID,
    ImagenetClassifier,
)
from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    TEST_IMAGENET_IMAGE,
)
from tetra_model_zoo.utils.args import get_model_cli_parser, model_from_cli_args
from tetra_model_zoo.utils.asset_loaders import download_data, load_image

IMAGENET_LABELS_JSON = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
IMAGENET_LABELS_PATH = download_data(IMAGENET_LABELS_JSON, MODEL_ID)
with open(IMAGENET_LABELS_PATH, "r") as imagenet_file:
    IMAGENET_LABELS = json.load(imagenet_file)


#
# Run Imagenet Classifier end-to-end on a sample image.
# The demo will print the predicted class to terminal.
#
def imagenet_demo(
    model_cls: Type[ImagenetClassifier], model_id: str, is_test: bool = False
):
    # Demo parameters
    parser = get_model_cli_parser(model_cls)
    parser.add_argument(
        "--image",
        type=str,
        default=TEST_IMAGENET_IMAGE,
        help="test image file path or URL",
    )
    args = parser.parse_args([] if is_test else None)

    model = model_from_cli_args(model_cls, args)
    assert isinstance(model, ImagenetClassifier)
    image = load_image(args.image, model_id)
    print("Model Loaded")

    # Run app
    app = ImagenetClassifierApp(model)
    probabilities = app.predict(image)
    predicted_class = torch.argmax(probabilities, dim=0)
    if not is_test:
        print(
            f"Prediction: {IMAGENET_LABELS[int(predicted_class)]}, {probabilities[predicted_class]}"
        )
