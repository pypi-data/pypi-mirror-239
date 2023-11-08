from __future__ import annotations

from tetra_model_zoo.models.detr_resnet50.model import DETRResNet50
from tetra_model_zoo.utils.args import (
    get_model_cli_parser,
    model_from_cli_args,
    vision_export_parser,
)
from tetra_model_zoo.utils.hub import download_hub_models


def main():
    # Export parameters
    parser = get_model_cli_parser(DETRResNet50)
    parser = vision_export_parser(
        default_x=480,
        default_y=480,
        dim_constraint="Must be divisible by 32.",
        parser=parser,
    )
    parser.add_argument("--c", type=int, default=3, help="Number of image channels.")
    args = parser.parse_args()

    # Instantiate the model & a sample input spec.
    detr_model = model_from_cli_args(DETRResNet50, args)
    input_spec = detr_model.get_input_spec((args.x, args.y), args.b, args.c)

    # Export the model.
    jobs = detr_model.export(input_spec, args.devices)

    # Download the optimized assets.
    download_hub_models(jobs)


if __name__ == "__main__":
    main()
