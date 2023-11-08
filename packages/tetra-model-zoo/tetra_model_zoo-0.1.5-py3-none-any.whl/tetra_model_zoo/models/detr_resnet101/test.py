from tetra_model_zoo.models._shared.detr.app import DETRApp
from tetra_model_zoo.models.detr_resnet101.demo import IMAGE_ADDRESS
from tetra_model_zoo.models.detr_resnet101.demo import main as demo_main
from tetra_model_zoo.models.detr_resnet101.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    DETRResNet101,
)
from tetra_model_zoo.utils.asset_loaders import load_image


def test_task():
    net = DETRResNet101.from_pretrained(DEFAULT_WEIGHTS)
    img = load_image(IMAGE_ADDRESS, MODEL_ID)
    _, _, label, _ = DETRApp(net).predict(img, DEFAULT_WEIGHTS)
    assert set(list(label.numpy())) == {75, 63, 17}


def test_trace():
    net = DETRResNet101.from_pretrained(DEFAULT_WEIGHTS).convert_to_torchscript()
    img = load_image(IMAGE_ADDRESS, MODEL_ID)
    _, _, label, _ = DETRApp(net).predict(img, DEFAULT_WEIGHTS)
    assert set(list(label.numpy())) == {75, 63, 17}


def test_demo():
    demo_main(is_test=True)
