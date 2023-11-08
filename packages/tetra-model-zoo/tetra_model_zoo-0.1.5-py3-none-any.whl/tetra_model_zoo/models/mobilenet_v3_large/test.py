from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from tetra_model_zoo.models.mobilenet_v3_large.demo import main as demo_main
from tetra_model_zoo.models.mobilenet_v3_large.model import MODEL_ID, MobileNetV3Large


def test_numerical():
    run_imagenet_classifier_test(MobileNetV3Large.from_pretrained(), MODEL_ID)


def test_trace():
    run_imagenet_classifier_trace_test(MobileNetV3Large.from_pretrained())


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
