from __future__ import annotations

from tetra_model_zoo.models.detr_resnet50_dc5.model import DETRResNet50DC5
from tetra_model_zoo.utils.args import (
    base_export_parser,
    input_spec_from_cli_args,
    model_from_cli_args,
)
from tetra_model_zoo.utils.hub import download_hub_models


def main():
    # Export parameters
    parser = base_export_parser(model_cls=DETRResNet50DC5)
    args = parser.parse_args()

    # Instantiate the model & the input specs.
    model = model_from_cli_args(DETRResNet50DC5, args)
    input_spec = input_spec_from_cli_args(model, args)

    # Submit compilation + profiling jobs to hub
    jobs = model.export(input_spec)

    # Download the optimized assets.
    download_hub_models(jobs)


if __name__ == "__main__":
    main()
