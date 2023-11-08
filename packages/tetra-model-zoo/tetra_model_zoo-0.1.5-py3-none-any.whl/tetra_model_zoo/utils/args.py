"""
Utility Functions for parsing input args for export and other customer facing scripts.
"""
from __future__ import annotations

import argparse
import inspect
from typing import Optional, Type

from tetra_model_zoo.utils.zoo_base_class import (
    DEFAULT_EXPORT_DEVICES,
    InputSpec,
    TetraZooModel,
)


def get_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )


def get_model_cli_parser(
    cls: Type[TetraZooModel], parser: argparse.ArgumentParser | None = None
) -> argparse.ArgumentParser:
    """
    Generate the argument parser to create this model from an argparse namespace.
    Default behavior is to assume the CLI args have the same names as from_pretrained method args.
    """
    if not parser:
        parser = get_parser()

    from_pretrained_sig = inspect.signature(cls.from_pretrained)
    for name, param in from_pretrained_sig.parameters.items():
        if name == "cls":
            continue
        parser.add_argument(
            f"--{name}",
            type=type(param.annotation),
            default=param.default,
            help=f"For documentation, see {cls.__name__}::from_pretrained.",
        )
    return parser


def model_from_cli_args(
    model_cls: Type[TetraZooModel], cli_args: argparse.Namespace
) -> TetraZooModel:
    """
    Create this model from an argparse namespace.
    Default behavior is to assume the CLI args have the same names as from_pretrained method args.
    """
    from_pretrained_args = inspect.getfullargspec(model_cls.from_pretrained)
    args_list = []
    for arg_name in from_pretrained_args.args:
        if arg_name == "cls":
            continue
        args_list.append(getattr(cli_args, arg_name))
    return model_cls.from_pretrained(*args_list)


def get_model_input_spec_parser(
    model_cls: Type[TetraZooModel], parser: argparse.ArgumentParser | None = None
) -> argparse.ArgumentParser:
    """
    Generate the argument parser to get this model's input spec from an argparse namespace.
    Default behavior is to assume the CLI args have the same names as get_input_spec method args.
    """
    if not parser:
        parser = get_parser()

    get_input_spec_sig = inspect.signature(model_cls.get_input_spec)
    for name, param in get_input_spec_sig.parameters.items():
        if name == "self":
            continue
        parser.add_argument(
            f"--{name}",
            type=type(param.annotation),
            default=param.default,
            help=f"For documentation, see {model_cls.__name__}::get_input_spec.",
        )
    return parser


def input_spec_from_cli_args(
    model: TetraZooModel, cli_args: argparse.Namespace
) -> InputSpec:
    """
    Create this model's input spec from an argparse namespace.
    Default behavior is to assume the CLI args have the same names as get_input_spec method args.
    """
    get_input_spec_args = inspect.getfullargspec(model.get_input_spec)
    args_list = []
    for arg_name in get_input_spec_args.args:
        if arg_name == "self":
            continue
        args_list.append(getattr(cli_args, arg_name))
    return model.get_input_spec(*args_list)


def base_export_parser(
    include_trace_option: bool = False,
    model_cls: Optional[Type[TetraZooModel]] = None,
    parser: argparse.ArgumentParser | None = None,
) -> argparse.ArgumentParser:
    """
    Base arg parser that specifies input args for an export script.

    Parameters:
        include_trace_options: includes saving trace option if set.

    Returns:
        Arg parser object.
    """
    if not parser:
        parser = get_parser()

    if model_cls:
        parser = get_model_cli_parser(model_cls, parser)
        parser = get_model_input_spec_parser(model_cls, parser)
    parser.add_argument(
        "--devices",
        nargs="+",
        default=[device.name for device in DEFAULT_EXPORT_DEVICES],
        help="Device[s] to export to.",
    )
    if include_trace_option:
        parser.add_argument(
            "--save_trace_and_exit",
            action="store_true",
            help="Write torchscript to current directory and exits.",
        )
    return parser


def quantized_export_parser(
    include_trace_option: bool = False, parser: argparse.ArgumentParser | None = None
) -> argparse.ArgumentParser:
    """
    Same as base_export_parser except defaults to android devices, since
        iOS doesn't support quantized models.

    Parameters:
        include_trace_options: includes saving trace option if set.

    Returns:
        Arg parser object.
    """
    if not parser:
        parser = get_parser()

    parser.add_argument(
        "--quantization_samples_path",
        default=None,
        help="A path to a `.pt` file containing sample input images to use for post-training quantization. "
        "The shape of the tensor should be (N, 3, 224, 224). "
        "If no path is provided, the model is quantized using a default set of images.",
    )
    parser.add_argument(
        "--devices",
        nargs="+",
        default=["Google Pixel 7", "Samsung Galaxy S23 Ultra"],
        help="Device[s] to export to. Quantized models can only be exported to Android devices for now.",
    )
    if include_trace_option:
        parser.add_argument(
            "--save_trace_and_exit",
            action="store_true",
            help="Write torchscript to current directory and exits.",
        )
    return parser


def vision_export_parser(
    default_x: int,
    default_y: int,
    dim_constraint: Optional[str] = None,
    include_trace_option: bool = False,
    parser: argparse.ArgumentParser | None = None,
) -> argparse.ArgumentParser:
    """
    Argument parser for a vision model's export script.
    Takes input image dimensions as args.

    Parameters:
        default_x: Default width in pixels.
        default_y: Default height in pixels.
        dim_constraint: Help message stating any constraints on the input dimensions.
        include_trace_options: includes saving trace option if set.

    Returns:
        Arg parser object.
    """
    if not parser:
        parser = get_parser()

    parser = base_export_parser(
        include_trace_option=include_trace_option, parser=parser
    )
    dim_constraint = dim_constraint or ""
    parser.add_argument(
        "--x",
        type=int,
        default=default_x,
        help=f"Input image width. {dim_constraint}",
    )
    parser.add_argument(
        "--y",
        type=int,
        default=default_y,
        help=f"Input image height. {dim_constraint}",
    )
    parser.add_argument("--b", type=int, default=1, help="Batch size.")
    return parser
