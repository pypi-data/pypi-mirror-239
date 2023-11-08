from __future__ import annotations

from typing import Any, List

import torch

import tetra_hub as hub
from tetra_model_zoo.models.huggingface_wavlm_base_plus.model import (
    DEFAULT_INPUT_VEC_LENGTH,
    HuggingFaceWavLMBasePlus,
)
from tetra_model_zoo.utils.args import base_export_parser
from tetra_model_zoo.utils.hub import download_hub_models


def trace(model: HuggingFaceWavLMBasePlus, input_shape: List[int] = [1, 320000]) -> Any:
    """
    Convert HuggingFaceWavLMBasePlus to a pytorch trace. Traces can be saved & loaded from disk.
    Returns: Trace Object
    """
    return torch.jit.trace(model, [torch.ones(input_shape)])


def main():
    # Export parameters
    parser = base_export_parser()
    parser.add_argument("--b", type=int, default=1, help="Batch size.")
    parser.add_argument(
        "--x",
        type=int,
        default=DEFAULT_INPUT_VEC_LENGTH,
        help=f"Input audio length. Default is {DEFAULT_INPUT_VEC_LENGTH}",
    )

    args = parser.parse_args()

    # Instantiate the model & a sample input.
    wavlm_model = HuggingFaceWavLMBasePlus.from_pretrained()

    # Trace the model.
    traced_wavlm = trace(wavlm_model, [args.b, args.x])

    # Select the device(s) you'd like to optimize for.
    devices = [hub.Device(x) for x in args.devices]

    # Submit the traced models for conversion & profiling.
    jobs = hub.submit_profile_job(
        name="HuggingFaceWavLMBasePlus",
        model=traced_wavlm,
        input_shapes={"input": ((args.b, args.x), "float32")},
        device=devices,
    )

    # Download the optimized assets!
    download_hub_models(jobs)


if __name__ == "__main__":
    main()
