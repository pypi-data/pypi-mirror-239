import numpy as np
import torch

from tetra_model_zoo.models._shared.yolo.utils import detect_postprocess
from tetra_model_zoo.models.yolov7.app import YoloV7DetectionApp
from tetra_model_zoo.models.yolov7.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    YoloV7,
    _load_yolov7_source_model_from_weights,
)
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image
from tetra_model_zoo.utils.image_processing import preprocess_PIL_image
from tetra_model_zoo.utils.testing import skip_clone_repo_check

IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "yolov7_demo_640.jpg"
)
OUTPUT_IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "yolov7_demo_640_output.png"
)
WEIGHTS = "yolov7-tiny.pt"


@skip_clone_repo_check
def test_numerical():
    """Verify that raw (numeric) outputs of both (Tetra and non-tetra) networks are the same."""
    processed_sample_image = preprocess_PIL_image(load_image(IMAGE_ADDRESS, MODEL_ID))
    source_model = _load_yolov7_source_model_from_weights(WEIGHTS)
    tetra_model = YoloV7.from_pretrained(WEIGHTS)

    with torch.no_grad():
        # original model output
        source_model.model[-1].training = False
        source_model.model[-1].export = False
        source_detect_out = source_model(processed_sample_image)[0]
        source_out_postprocessed = detect_postprocess(source_detect_out)

        # Tetra model output
        tetra_out_postprocessed = tetra_model(processed_sample_image)
        for i in range(0, len(source_out_postprocessed)):
            assert np.allclose(source_out_postprocessed[i], tetra_out_postprocessed[i])


def test_yolov7_app():
    image = load_image(IMAGE_ADDRESS, MODEL_ID)
    output_image = load_image(OUTPUT_IMAGE_ADDRESS, MODEL_ID).convert("RGB")
    app = YoloV7DetectionApp(YoloV7.from_pretrained(WEIGHTS))
    assert np.allclose(app.predict_boxes_from_image(image)[0], np.asarray(output_image))
