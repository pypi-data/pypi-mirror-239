from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from tetra_model_zoo.models.mobilenet_v3_small.demo import main as demo_main
from tetra_model_zoo.models.mobilenet_v3_small.model import MODEL_ID, MobileNetV3Small


def test_numerical():
    run_imagenet_classifier_test(MobileNetV3Small.from_pretrained(), MODEL_ID)


def test_trace():
    run_imagenet_classifier_trace_test(MobileNetV3Small.from_pretrained())


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
