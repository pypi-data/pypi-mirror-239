from tetra_model_zoo.models._shared.detr.app import DETRApp
from tetra_model_zoo.models.detr_resnet50_dc5.demo import IMAGE_ADDRESS
from tetra_model_zoo.models.detr_resnet50_dc5.demo import main as demo_main
from tetra_model_zoo.models.detr_resnet50_dc5.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    DETRResNet50DC5,
)
from tetra_model_zoo.utils.asset_loaders import load_image


def test_task():
    net = DETRResNet50DC5.from_pretrained(DEFAULT_WEIGHTS)
    img = load_image(IMAGE_ADDRESS, MODEL_ID)
    _, _, label, _ = DETRApp(net).predict(img, DEFAULT_WEIGHTS)
    assert set(list(label.numpy())) == {75, 63, 17}


def test_trace():
    net = DETRResNet50DC5.from_pretrained(DEFAULT_WEIGHTS).convert_to_torchscript()
    img = load_image(IMAGE_ADDRESS, MODEL_ID)
    _, _, label, _ = DETRApp(net).predict(img, DEFAULT_WEIGHTS)
    assert set(list(label.numpy())) == {75, 63, 17}


def test_demo():
    demo_main(is_test=True)
