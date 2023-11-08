from typing import Optional

import torch

from tetra_model_zoo.utils.asset_loaders import download_data

IMAGE_QUANTIZATION_SAMPLES_URL = "https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/quantization/image_quantization_samples.pt"
# To get the model id for a quantized model, append this to the MODEL_ID of the unquantized version
QUANTIZED_MODEL_ID_SUFFIX = "_quantized"


def get_image_quantization_samples(
    quantization_samples_path: Optional[str] = None,
) -> torch.Tensor:
    """
    Loads a tensor of sample input image data from the specified path.
    This data is intended to be used for post-training quantization.

    If no path is provided, the method returns a default tensor containing
    data from images fetched from the Google OpenImages dataset.

    The default tensor has shape (50, 3, 224, 224). Here is the code to produce
    the default tensor:

    ```
    import fiftyone.zoo as foz
    from PIL import Image
    import torch
    from tetra_model_zoo.models._shared.imagenet_classifier.app import preprocess_image

    image_dataset = foz.load_zoo_dataset(
        "open-images-v6",
        split="validation",
        max_samples=50,
        shuffle=True,
    )

    tensors = []
    for sample in image_dataset:
        img = Image.open(sample.filepath)
        tensors.append(preprocess_image(img))

    final_tensor = torch.cat(tensors, dim=0)

    torch.save(final_tensor, "imagenet_quantization_samples.pt")
    ```
    """
    if quantization_samples_path is None:
        quantization_samples_path = download_data(
            IMAGE_QUANTIZATION_SAMPLES_URL, "quantization"
        )
    return torch.load(quantization_samples_path)


class QNNPackQuantizationMixin(torch.nn.Module):
    """
    A Mixin to be added to models to support quantizing them using qnnpack.

    Models which inherit from this Mixin can be quantized using quantize_e2e.

    This class is not intended to be initialized directly, only added as an
    additional superclass (i.e. Mixin) to an existing
    torch.nn.Module subclass definition.
    """

    def prepare_ptq(self) -> None:
        """
        Prepare the model for post-training quantization. This installs "observers"
        into the model that will record min/max of any samples that pass through it.
        """
        engine = "qnnpack"
        torch.backends.quantized.engine = engine  # type: ignore
        self.qconfig = torch.ao.quantization.get_default_qconfig(engine)

        torch.ao.quantization.prepare(self, inplace=True)

    def quantize(self) -> None:
        """
        Finalize the quantized model.
        """
        torch.ao.quantization.convert(self, inplace=True)

    def quantize_e2e(self, quantization_samples: torch.Tensor) -> None:
        """
        Perform end-to-end quantization given a tensor of quantization samples

        Parameters:
            quantization_samples: Tensor of input data used to
                compute quantization ranges.
        """

        # Install observers
        self.prepare_ptq()
        # Perform PTQ with representative samples
        self(quantization_samples)
        # Finalize quantization
        self.quantize()
