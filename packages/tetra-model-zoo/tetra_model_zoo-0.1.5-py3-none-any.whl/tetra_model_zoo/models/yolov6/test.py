import numpy as np
import torch

from tetra_model_zoo.models._shared.yolo.utils import detect_postprocess
from tetra_model_zoo.models.yolov6.model import (
    DEFAULT_WEIGHTS,
    MODEL_ASSET_VERSION,
    MODEL_ID,
    WEIGHTS_PATH,
    YoloV6,
    _load_yolov6_source_model_from_weights,
)
from tetra_model_zoo.utils.asset_loaders import (
    download_data,
    get_model_asset_url,
    load_image,
)
from tetra_model_zoo.utils.image_processing import preprocess_PIL_image
from tetra_model_zoo.utils.testing import skip_clone_repo_check

IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "test_images/input_image.jpg"
)


@skip_clone_repo_check
def test_numerical():
    model_path = f"{WEIGHTS_PATH}{DEFAULT_WEIGHTS}"
    downloaded_model_path = download_data(model_path, MODEL_ID)

    # source model
    source_model = _load_yolov6_source_model_from_weights(downloaded_model_path)

    # Tetra model
    tetra_model = YoloV6.from_pretrained()

    with torch.no_grad():
        # source model output
        processed_sample_image = preprocess_PIL_image(
            load_image(IMAGE_ADDRESS, MODEL_ID)
        )
        source_detect_out = source_model(processed_sample_image)
        source_out_postprocessed = detect_postprocess(source_detect_out)

        # Tetra model output
        tetra_out_postprocessed = tetra_model(processed_sample_image)
        for i in range(0, len(source_out_postprocessed)):
            assert np.allclose(source_out_postprocessed[i], tetra_out_postprocessed[i])
