from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from tetra_model_zoo.models.resnext101.demo import main as demo_main
from tetra_model_zoo.models.resnext101.model import MODEL_ID, ResNeXt101


def test_numerical():
    run_imagenet_classifier_test(
        ResNeXt101.from_pretrained(), MODEL_ID, probability_threshold=0.46
    )


def test_trace():
    run_imagenet_classifier_trace_test(ResNeXt101.from_pretrained())


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
