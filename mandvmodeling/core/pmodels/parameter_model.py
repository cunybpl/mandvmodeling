from changepointmodel.core.pmodels.parameter_model import (
    ParameterModelFunction as ChangepointModelParameterModelFunction,
)
from typing import Generic
from _collections_abc import Callable
from changepointmodel.core.pmodels import base as ChangepointModelBase
from typing import Union
from . import base as MandVModelingBase


def _validate_param(param, param_str: str = None, valid_type = None):
    """
    Validates a parameter to ensure it meets the required type criteria.

    Parameters:
    -----------
    param : Any
        The parameter to validate.
    param_str : str, optional
        A string representation of the parameter name, used in error messages.
    valid_type : type, optional
        The expected type (or superclass) for validation.

    Raises:
    -------
    TypeError
        If the parameter does not inherit the specified type
        or is not a valid callable function.
    """
    if hasattr(param, "__subclasses__"):
        if not issubclass(param, valid_type):
            raise TypeError(
                "Wrong {} class used. {} class should inherit from {}. Incorrect class: {}.".format(
                    param_str, param_str, str(valid_type), str(param)
                )
            )
    elif not isinstance(param, valid_type):
        raise TypeError(
            "{} is not a valid `{}`. Currently of type {}".format(
                param_str, str(valid_type), type(param)
            )
        )


class MandVParameterModelFunction(
    ChangepointModelParameterModelFunction,
    Generic[
        ChangepointModelBase.ParamaterModelCallableT,
        ChangepointModelBase.EnergyParameterModelT,
    ],
):
    """
    This class models a parameter function and derives from
    ChangepointModelParameterModelFunction.

    Attributes:
    -----------
    name : str
        The identifier for the parameter model function.
    f : ChangepointModelBase.ParamaterModelCallableT
        A callable that defines the parameter model.
    bounds : Union[ChangepointModelBase.BoundCallable, ChangepointModelBase.Bound]
        Constraints for the parameter model function.
    parameter_model : ChangepointModelBase.EnergyParameterModelT
        An associated energy parameter model.
    coefficients_parser : ChangepointModelBase.ICoefficientParser
        A component responsible for parsing coefficients.
    initital_guesses : Union[base.InitialGuessCallable, base.InitialGuess, None], optional
        Preliminary assumptions for the parameter model function, defaults to None.

    Methods:
    --------
    initial_guesses -> Union[base.InitialGuessCallable, base.InitialGuess, None]:
        Provides the preliminary assumptions for the parameter model function.
    """

    def __init__(
        self,
        name: str,
        f: ChangepointModelBase.ParamaterModelCallableT,
        bounds: Union[ChangepointModelBase.BoundCallable, ChangepointModelBase.Bound],
        parameter_model: ChangepointModelBase.EnergyParameterModelT,
        coefficients_parser: ChangepointModelBase.ICoefficientParser,
        initital_guesses: Union[
            MandVModelingBase.InitialGuessCallable, MandVModelingBase.InitialGuess
        ] = None,
    ):
        _validate_param(param=f, param_str="f", valid_type=Callable)
        _validate_param(
            param = coefficients_parser,
            param_str = "coefficients_parser",
            valid_type=ChangepointModelBase.ICoefficientParser,
        )
        _validate_param(
            param = parameter_model,
            param_str="parameter_model",
            valid_type=ChangepointModelBase.AbstractEnergyParameterModel,
        )

        super().__init__(
            name=name,
            f=f,
            bounds=bounds,
            parameter_model=parameter_model,
            coefficients_parser=coefficients_parser,
        )
        if initital_guesses:
            self._initial_guesses = initital_guesses
        else:
            self._initial_guesses = None

    @property
    def initial_guesses(
        self,
    ) -> Union[
        MandVModelingBase.InitialGuessCallable, MandVModelingBase.InitialGuess, None
    ]:
        """
        Provides the preliminary assumptions for the parameter model function.

        Returns:
        --------
        Union[MandVModelingBase.InitialGuessCallable, MandVModelingBase.InitialGuess, None]
            The preliminary assumptions for the parameter model, if present.
        """
        return self._initial_guesses
