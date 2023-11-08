from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from typing import Any, List

import torch

import tetra_hub as hub
from tetra_model_zoo.utils.input_spec import InputSpec, make_torch_inputs

DEFAULT_EXPORT_DEVICES = [
    hub.Device("Apple iPhone 14 Pro"),
    hub.Device("Samsung Galaxy S23 Ultra"),
]


class DocstringInheritorMeta(ABCMeta):
    """
    Ensures that all subclasses retain the `forward` function's docstring.
    """

    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        if hasattr(new_class, "forward"):
            parent_method = getattr(bases[0], "forward", None)
            if parent_method and new_class.forward.__doc__ is None:  # type: ignore
                new_class.forward.__doc__ = parent_method.__doc__  # type: ignore
        return new_class


class TetraZooModel(torch.nn.Module, ABC, metaclass=DocstringInheritorMeta):
    @classmethod
    @abstractmethod
    def from_pretrained(cls, *args, **kwargs) -> "TetraZooModel":
        """
        Utility function that helps users get up and running with a default
        pretrained model. While this function may take arguments, all arguments
        should have default values specified, so that all classes can be invoked
        with `cls.from_pretrained()` and always have it return something reasonable.
        """
        pass

    @abstractmethod
    def get_input_spec(self, *args, **kwargs) -> InputSpec:
        """
        Returns a map from `{input_name -> (shape, dtype)}`
        specifying the shape and dtype for each input argument.
        """
        pass

    def convert_to_torchscript(self, input_spec: InputSpec | None = None) -> Any:
        """
        Converts the torch module to a torchscript trace, which
        is the format expected by tetra hub.

        This is a default implementation that may be overriden by a subclass.
        """
        if not input_spec:
            input_spec = self.get_input_spec()

        return torch.jit.trace(self, self.sample_inputs(input_spec))

    def export(
        self,
        input_spec: InputSpec | None = None,
        devices: List[hub.Device] | List[str] = DEFAULT_EXPORT_DEVICES,
        options: str = "",
    ):
        """
        Exports this model for deployment on the provided devices.
        The model will use the provided input specification to define input names and shapes.
        """
        if not input_spec:
            input_spec = self.get_input_spec()
        if not devices:
            raise ValueError("Please specify devices to export for.")
        if isinstance(devices[0], str):
            devices = [hub.Device(x) for x in devices]  # type: ignore

        # Trace the model.
        traced_model = self.convert_to_torchscript(input_spec)

        # Submit the traced models for conversion & profiling.
        return hub.submit_profile_job(
            name=type(self).__name__,
            model=traced_model,
            input_shapes=input_spec,
            device=devices,  # type: ignore
            options=options,
        )

    def sample_inputs(self, input_spec: InputSpec | None = None) -> List[torch.Tensor]:
        """
        Returns a list of sample input tensors to the model.

        This is a default implementation that returns random data based
        on the shapes and dtypes from `get_input_spec`. May be overriden by
        a subclass.
        """
        if not input_spec:
            input_spec = self.get_input_spec()
        return make_torch_inputs(input_spec)
