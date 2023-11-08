import numpy as np

from tetra_model_zoo.models._shared.repaint.app import RepaintMaskApp
from tetra_model_zoo.models.aotgan.demo import IMAGE_ADDRESS, MASK_ADDRESS
from tetra_model_zoo.models.aotgan.demo import main as demo_main
from tetra_model_zoo.models.aotgan.model import AOTGAN, MODEL_ASSET_VERSION, MODEL_ID
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image
from tetra_model_zoo.utils.testing import assert_most_close, skip_clone_repo_check

OUTPUT_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "test_images/test_output.png"
)


@skip_clone_repo_check
def test_numerical():
    app = RepaintMaskApp(AOTGAN.from_pretrained())

    img = load_image(IMAGE_ADDRESS, MODEL_ID)
    mask_image = load_image(MASK_ADDRESS, MODEL_ID)

    out_imgs = app.paint_mask_on_image(img, mask_image)
    expected_out = load_image(OUTPUT_ADDRESS, MODEL_ID)
    assert_most_close(
        np.asarray(out_imgs[0], dtype=np.float32),
        np.asarray(expected_out, dtype=np.float32),
        0.005,
        rtol=0.02,
        atol=1.5,
    )


@skip_clone_repo_check
def test_trace():
    net = AOTGAN.from_pretrained()
    input_spec = net.get_input_spec()
    trace = net.convert_to_torchscript(input_spec)

    img = load_image(IMAGE_ADDRESS, MODEL_ID)
    mask_image = load_image(MASK_ADDRESS, MODEL_ID)
    app = RepaintMaskApp(trace)

    out_imgs = app.paint_mask_on_image(img, mask_image)
    expected_out = load_image(OUTPUT_ADDRESS, MODEL_ID)
    assert_most_close(
        np.asarray(out_imgs[0], dtype=np.float32),
        np.asarray(expected_out, dtype=np.float32),
        0.005,
        rtol=0.02,
        atol=1.5,
    )


@skip_clone_repo_check
def test_demo():
    # Run demo and verify it does not crash
    demo_main(is_test=True)
