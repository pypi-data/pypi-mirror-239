import numpy as np
import torch
from ultralytics import YOLO as ultralytics_YOLO

from tetra_model_zoo.models.yolov8_det.app import YoloV8DetectionApp
from tetra_model_zoo.models.yolov8_det.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    YoloV8Detector,
    yolov8_detect_postprocess,
)
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image
from tetra_model_zoo.utils.image_processing import preprocess_PIL_image
from tetra_model_zoo.utils.testing import skip_clone_repo_check

IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "test_images/input_image.jpg"
)
OUTPUT_IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "test_images/output_image.png"
)
WEIGHTS = "yolov8n.pt"


@skip_clone_repo_check
def test_numerical():
    """Verify that raw (numeric) outputs of both (Tetra and non-tetra) networks are the same."""
    processed_sample_image = preprocess_PIL_image(load_image(IMAGE_ADDRESS, MODEL_ID))
    source_model = ultralytics_YOLO(WEIGHTS).model
    tetra_model = YoloV8Detector.from_pretrained(WEIGHTS)

    with torch.no_grad():
        # original model output
        source_detect_out, *_ = source_model(processed_sample_image)
        source_out_postprocessed = yolov8_detect_postprocess(source_detect_out)

        # Tetra model output
        tetra_out_postprocessed = tetra_model(processed_sample_image)
        for i in range(0, len(source_out_postprocessed)):
            assert np.allclose(source_out_postprocessed[i], tetra_out_postprocessed[i])


def test_yolov8_det_app():
    image = load_image(IMAGE_ADDRESS, MODEL_ID)
    output_image = load_image(OUTPUT_IMAGE_ADDRESS, MODEL_ID)
    app = YoloV8DetectionApp(YoloV8Detector.from_pretrained(WEIGHTS))
    assert np.allclose(app.predict_boxes_from_image(image)[0], np.asarray(output_image))
