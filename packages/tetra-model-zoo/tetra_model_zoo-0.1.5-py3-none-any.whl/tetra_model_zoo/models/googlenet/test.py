from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from tetra_model_zoo.models.googlenet.demo import main as demo_main
from tetra_model_zoo.models.googlenet.model import MODEL_ID, GoogLeNet


def test_numerical():
    run_imagenet_classifier_test(GoogLeNet.from_pretrained(), MODEL_ID)


def test_trace():
    run_imagenet_classifier_trace_test(GoogLeNet.from_pretrained())


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
