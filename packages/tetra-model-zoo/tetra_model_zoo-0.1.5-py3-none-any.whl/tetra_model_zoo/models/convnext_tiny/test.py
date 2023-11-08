from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from tetra_model_zoo.models.convnext_tiny.demo import main as demo_main
from tetra_model_zoo.models.convnext_tiny.model import MODEL_ID, ConvNextTiny


def test_numerical():
    run_imagenet_classifier_test(ConvNextTiny.from_pretrained(), MODEL_ID)


def test_trace():
    run_imagenet_classifier_trace_test(ConvNextTiny.from_pretrained())


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
