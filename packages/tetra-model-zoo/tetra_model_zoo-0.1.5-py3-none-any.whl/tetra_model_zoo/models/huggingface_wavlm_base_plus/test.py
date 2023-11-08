import numpy as np
import torch
from datasets import load_dataset

from tetra_model_zoo.models.huggingface_wavlm_base_plus.app import (
    HuggingFaceWavLMBasePlusApp,
)
from tetra_model_zoo.models.huggingface_wavlm_base_plus.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    HuggingFaceWavLMBasePlus,
)
from tetra_model_zoo.utils.asset_loaders import download_model_asset
from tetra_model_zoo.utils.testing import skip_clone_repo_check

OUTPUT_TENSOR_1 = download_model_asset(
    MODEL_ID, MODEL_ASSET_VERSION, "wavlm_output_tensor_1.pth"
)
OUTPUT_TENSOR_2 = download_model_asset(
    MODEL_ID, MODEL_ASSET_VERSION, "wavlm_output_tensor_2.pth"
)


@skip_clone_repo_check
def test_app():
    # Load input data
    dataset = load_dataset(
        "hf-internal-testing/librispeech_asr_demo", "clean", split="validation"
    )
    dataset = dataset.sort("id")
    x = dataset[0]["audio"]["array"]
    sampling_rate = dataset.features["audio"].sampling_rate

    # Load expected output data
    first_output_tensor = torch.load(OUTPUT_TENSOR_1)
    output_array1 = first_output_tensor.detach().numpy()
    second_output_tensor = torch.load(OUTPUT_TENSOR_2)
    output_array2 = second_output_tensor.detach().numpy()

    # Load model and run inference
    app = HuggingFaceWavLMBasePlusApp(HuggingFaceWavLMBasePlus.from_pretrained())
    app_output_features = app.predict_features(x, sampling_rate)

    # Compare outputs
    np.testing.assert_allclose(
        np.asarray(app_output_features[0].detach().numpy(), dtype=np.float32),
        np.asarray(output_array1, dtype=np.float32),
        rtol=0.02,
        atol=0.2,
    )

    np.testing.assert_allclose(
        np.asarray(app_output_features[1].detach().numpy(), dtype=np.float32),
        np.asarray(output_array2, dtype=np.float32),
        rtol=0.02,
        atol=0.2,
    )
