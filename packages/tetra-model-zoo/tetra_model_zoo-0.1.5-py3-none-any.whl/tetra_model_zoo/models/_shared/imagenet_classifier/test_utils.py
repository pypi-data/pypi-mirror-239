import numpy as np
import pytest
import torch

from tetra_model_zoo.models._shared.imagenet_classifier.app import (
    ImagenetClassifierApp,
    preprocess_image,
)
from tetra_model_zoo.models._shared.imagenet_classifier.model import (
    MODEL_ASSET_VERSION,
    ImagenetClassifier,
)
from tetra_model_zoo.utils.asset_loaders import (
    download_model_asset,
    get_model_asset_url,
    load_image,
)
from tetra_model_zoo.utils.testing import assert_most_close

GROUP_NAME = "imagenet_classifier"
TEST_IMAGENET_IMAGE = get_model_asset_url(GROUP_NAME, MODEL_ASSET_VERSION, "dog.jpg")

# Class "Samoyed" from https://gist.github.com/ageitgey/4e1342c10a71981d0b491e1b8227328b
TEST_IMAGENET_CLASS = 258


@pytest.fixture(scope="module")
def imagenet_sample_torch() -> torch.Tensor:
    """
    Returns:

    - Preprocessed (normalized etc) image as torch.Tensor with shape [1, 3, 224, 224]
    """
    img = load_image(TEST_IMAGENET_IMAGE, "imagenet_classifier")
    return preprocess_image(img)


def run_imagenet_classifier_test(
    model: ImagenetClassifier,
    model_name: str,
    asset_version: int = 2,
    probability_threshold: float = 0.7,
    diff_tol: float = 0.0,
    rtol: float = 0.0,
    atol: float = 1e-4,
) -> None:
    """
    Evaluates the classifier on a test image and validates the output.

    Parameters:
        model: The model to evaluate.
        model_name: Identifier used to lookup the expected output file.
        asset_version: Version of the expected output file to lookup.
        probability_threshold: If the predicited probability for the correct class
            is below this threshold, the method throws an error.
        diff_tol: Float in range [0,1] representing the maximum percentage of
            the probabilities that can differ from the ground truth while
            still having the test pass.
        atol: Absolute tolerance allowed for two numbers to be "close".
        rtol: Relative tolerance allowed for two numbers to be "close".
    """

    img = load_image(TEST_IMAGENET_IMAGE, "imagenet_classifier")
    app = ImagenetClassifierApp(model)
    probabilities = app.predict(img)

    expected_out_path = download_model_asset(
        model_name, asset_version, "expected_out.npy"
    )
    expected_out = np.load(expected_out_path)
    assert_most_close(probabilities.numpy(), expected_out, diff_tol, rtol, atol)

    predicted_class = torch.argmax(probabilities, dim=0)
    predicted_probability = probabilities[TEST_IMAGENET_CLASS].item()
    assert (
        predicted_probability > probability_threshold
    ), f"Predicted probability {predicted_probability:.3f} is below the threshold {probability_threshold}."
    assert (
        predicted_class == TEST_IMAGENET_CLASS
    ), f"Model predicted class {predicted_class} when correct class was {TEST_IMAGENET_CLASS}."


def run_imagenet_classifier_trace_test(
    model: ImagenetClassifier,
    diff_tol: float = 0.005,
    rtol: float = 0.0,
    atol: float = 1e-4,
) -> None:
    img = load_image(TEST_IMAGENET_IMAGE, "imagenet_classifier")
    app = ImagenetClassifierApp(model)
    trace_app = ImagenetClassifierApp(model.convert_to_torchscript())
    probabilities = app.predict(img)
    trace_probs = trace_app.predict(img)
    assert_most_close(probabilities.numpy(), trace_probs.numpy(), diff_tol, rtol, atol)
