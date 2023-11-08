from __future__ import annotations

from tetra_model_zoo.models.aotgan.model import AOTGAN
from tetra_model_zoo.utils.args import (
    base_export_parser,
    input_spec_from_cli_args,
    model_from_cli_args,
)
from tetra_model_zoo.utils.hub import download_hub_models


def main(is_test: bool = False):
    # Export parameters
    parser = base_export_parser(model_cls=AOTGAN)
    args = parser.parse_args([] if is_test else None)

    # Instantiate the model & a sample input.
    model = model_from_cli_args(AOTGAN, args)
    input_spec = input_spec_from_cli_args(model, args)

    # Submit the model for conversion & profiling.
    jobs = model.export(input_spec, args.devices)

    # Download the optimized assets.
    download_hub_models(jobs)


if __name__ == "__main__":
    main()
