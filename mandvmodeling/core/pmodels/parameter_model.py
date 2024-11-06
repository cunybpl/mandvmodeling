from changepointmodel.core.pmodels.parameter_model import ParameterModelFunction as ChangepointModelParameterModelFunction
from typing import Generic
from changepointmodel.core.pmodels import base as ChangepointModelBase
from typing import Union
from . import base as MandVModelingBase


class MandVParameterModelFunction(ChangepointModelParameterModelFunction, Generic[ChangepointModelBase.ParamaterModelCallableT, ChangepointModelBase.EnergyParameterModelT]):
    """
    A class representing a parameter model function, inheriting from
    ChangepointModelParameterModelFunction.

    Attributes:
    -----------
    name : str
        The name of the parameter model function.
    f : ChangepointModelBase.ParamaterModelCallableT
        A callable function representing the parameter model.
    bounds : Union[ChangepointModelBase.BoundCallable, ChangepointModelBase.Bound]
        The bounds for the parameter model function.
    parameter_model : ChangepointModelBase.EnergyParameterModelT
        The energy parameter model associated with the function.
    coefficients_parser : ChangepointModelBase.ICoefficientParser
        The parser to handle coefficients of the function.
    initital_guesses : Union[base.InitialGuessCallable, base.InitialGuess, None], optional
        Initial guesses for the parameter model function (default is None).

    Methods:
    --------
    initial_guesses -> Union[base.InitialGuessCallable, base.InitialGuess, None]:
        Returns the initial guesses for the parameter model function.
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
        Returns the initial guesses for the parameter model function.

        Returns:
        --------
        Union[MandVModelingBase.InitialGuessCallable, MandVModelingBase.InitialGuess, None]
            The initial guesses for the parameter model, if any.
        """
        return self._initial_guesses
