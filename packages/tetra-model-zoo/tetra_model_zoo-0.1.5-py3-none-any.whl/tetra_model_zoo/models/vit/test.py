from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (  # run_imagenet_classifier_trace_test,
    run_imagenet_classifier_test,
)
from tetra_model_zoo.models.vit.demo import main as demo_main
from tetra_model_zoo.models.vit.model import MODEL_ID, VIT


def test_numerical():
    run_imagenet_classifier_test(VIT.from_pretrained(), MODEL_ID)


# TODO: Fix this export test.
# def test_trace():
#   run_imagenet_classifier_trace_test(VIT.from_pretrained())


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
