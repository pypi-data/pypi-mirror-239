from tetra_model_zoo.models._shared.imagenet_classifier.test_utils import (
    run_imagenet_classifier_test,
    run_imagenet_classifier_trace_test,
)
from tetra_model_zoo.models.inception_v3_quantized.demo import main as demo_main
from tetra_model_zoo.models.inception_v3_quantized.model import (
    MODEL_ID,
    InceptionNetV3Quantized,
)


def test_numerical():
    run_imagenet_classifier_test(
        InceptionNetV3Quantized.from_pretrained(), MODEL_ID, diff_tol=0.01
    )


def test_trace():
    run_imagenet_classifier_trace_test(InceptionNetV3Quantized.from_pretrained())


def test_demo():
    # Verify demo does not crash
    demo_main(is_test=True)
