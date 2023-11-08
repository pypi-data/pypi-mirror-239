from __future__ import annotations

from typing import Any, List

import torch

from tetra_model_zoo.models.detr_resnet101.model import DETRResNet101
from tetra_model_zoo.utils.args import (
    base_export_parser,
    input_spec_from_cli_args,
    model_from_cli_args,
)
from tetra_model_zoo.utils.hub import download_hub_models


def trace(model: DETRResNet101, image_shape: List[int], mask_shape: List[int]) -> Any:
    """
    Convert DETRResNet101 to a pytorch trace. Traces can be saved & loaded from disk.
    Returns: Trace Object
    """
    return torch.jit.trace(
        model, [torch.rand((image_shape)), torch.rand((mask_shape))], strict=False
    )


def main():
    # Export parameters
    parser = base_export_parser(model_cls=DETRResNet101)
    args = parser.parse_args()

    # Instantiate the model & the input specs.
    model = model_from_cli_args(DETRResNet101, args)
    input_spec = input_spec_from_cli_args(model, args)

    # Submit compilation + profiling jobs to hub
    jobs = model.export(input_spec)

    # Download the optimized assets.
    download_hub_models(jobs)


if __name__ == "__main__":
    main()
