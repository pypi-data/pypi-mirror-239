from __future__ import annotations

from tetra_model_zoo.models.efficientnet_b0.model import EfficientNetB0
from tetra_model_zoo.utils.args import (
    base_export_parser,
    input_spec_from_cli_args,
    model_from_cli_args,
)
from tetra_model_zoo.utils.hub import download_hub_models


def main():
    # Export parameters
    parser = base_export_parser(model_cls=EfficientNetB0)
    args = parser.parse_args()

    # Instantiate the model
    model = model_from_cli_args(EfficientNetB0, args)
    input_spec = input_spec_from_cli_args(model, args)

    # Submit the model for conversion & profiling.
    jobs = model.export(input_spec, args.devices)

    # Download the optimized asset
    download_hub_models(jobs)


if __name__ == "__main__":
    main()
