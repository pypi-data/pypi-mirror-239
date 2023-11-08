from tetra_model_zoo.models._shared.detr.app import DETRApp
from tetra_model_zoo.models.detr_resnet50.demo import IMAGE_ADDRESS
from tetra_model_zoo.models.detr_resnet50.demo import main as demo_main
from tetra_model_zoo.models.detr_resnet50.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    DETRResNet50,
)
from tetra_model_zoo.utils.args import get_model_cli_parser, model_from_cli_args
from tetra_model_zoo.utils.asset_loaders import load_image

EXPECTED_OUTPUT = {75, 63, 17}


def test_task():
    net = DETRResNet50.from_pretrained()
    img = load_image(IMAGE_ADDRESS, MODEL_ID)
    _, _, label, _ = DETRApp(net).predict(img, DEFAULT_WEIGHTS)
    assert set(list(label.numpy())) == EXPECTED_OUTPUT


def test_cli_from_pretrained():
    args = get_model_cli_parser(DETRResNet50).parse_args([])
    assert model_from_cli_args(DETRResNet50, args) is not None


def test_trace():
    net = DETRResNet50.from_pretrained()
    input_spec = net.get_input_spec()
    trace = net.convert_to_torchscript(input_spec)

    img = load_image(IMAGE_ADDRESS, MODEL_ID)
    _, _, label, _ = DETRApp(trace).predict(img, DEFAULT_WEIGHTS)
    assert set(list(label.numpy())) == EXPECTED_OUTPUT


def test_demo():
    # Run demo and verify it does not crash
    demo_main(is_test=True)
