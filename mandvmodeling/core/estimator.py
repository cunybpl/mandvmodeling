from typing import Any, Optional, Union, Tuple, Dict
from collections.abc import Callable
from changepointmodel.core.nptypes import OneDimNDArray
import numpy.typing as npt
import numpy as np
from changepointmodel.core import (
    EnergyChangepointEstimator as ChangepointModelEnergyChangepointEstimator,
    CurvefitEstimator as ChangepointModelCurvefitEstimator,
)
from mandvmodeling.core.pmodels.parameter_model import MandVParameterModelFunction
from changepointmodel.core.pmodels import (
    ParamaterModelCallableT,
    EnergyParameterModelT,
)
from changepointmodel.core.estimator import check_not_fitted
from .schemas import MandVDataModel
from changepointmodel.core.calc.bounds import BoundTuple, OpenBoundCallable
from mandvmodeling.core.calc.init_guesses import (
    InitialGuessTuple,
    OpenInitialGuessCallable,
)
from sklearn.utils.validation import check_X_y
from scipy import optimize

Bounds = Union[BoundTuple, OpenBoundCallable]
InitialGuesses = Union[InitialGuessTuple, OpenInitialGuessCallable]


def check_data_model(method: Callable[..., Any]) -> Callable[..., Any]:
    """
    Helper decorator to raise a TypeError if the data_model argument is not of type MandVDataModel. This
    ensures that the date is pre-sorted before being fit to the model.

    Args:
      method: Callable[..., Any]: The method to be decorated

    Returns:
      Callable[..., Any]: The decorated method
    """

    def wrapper(self, data_model):
        if not isinstance(data_model, MandVDataModel):
            raise TypeError(
                "data_model is of type {}. Must be of type MandVDataModel".format(
                    type(data_model).__name__
                )
            )
        return method(self, data_model)

    return wrapper


class MandVCurvefitEstimator(ChangepointModelCurvefitEstimator):
    def __init__(
        self,
        model_func: Optional[Callable[..., Any]] = None,
        p0: Optional[Union[InitialGuesses, OpenInitialGuessCallable]] = None,
        bounds: Union[Bounds, OpenBoundCallable, Tuple[float, float], None] = (
            -np.inf,
            np.inf,
        ),
        method: str = "trf",
        jac: Union[
            str, Callable[[npt.NDArray[np.float64], Any], npt.NDArray[np.float64]], None
        ] = None,
        lsq_kwargs: Optional[Dict[Any, Any]] = {},
    ) -> None:
        super().__init__(
            model_func=model_func,
            p0=p0,
            bounds=bounds,
            method=method,
            jac=jac,
            lsq_kwargs=lsq_kwargs,
        )

    def fit(
        self,
        X: npt.NDArray[np.float64],
        y: Optional[npt.NDArray[np.float64]] = None,
        sigma: Optional[npt.NDArray[np.float64]] = None,
        absolute_sigma: bool = False,
    ) -> "MandVCurvefitEstimator":
        """Fit X features to target y.

        Refer to scipy.optimize.curve_fit docs for details on sigma values.

        Args:
            X (np.array): The feature matrix we are using to fit.
            y (np.array): The target array.
            sigma (Optional[np.array], optional): Determines uncertainty in the ydata. Defaults to None.
            absolute_sigma (bool, optional): Uses sigma in an absolute sense and reflects this in the pcov. Defaults to True.
            squeeze_1d: (bool, optional): Squeeze X into a 1 dimensional array for curve fitting. This is useful if you are fitting
                a function with an X array and do not want to squeeze before it enters curve_fit. Defaults to True.

        Returns:
            GeneralizedCurveFitEstimator: self
        """
        # NOTE the user defined function should handle the neccesary array manipulation (squeeze, reshape etc.)
        # pass the sklearn estimator dimensionality check
        X, y = check_X_y(X, y)

        if callable(self.bounds):  # we allow bounds to be a callable
            bounds = self.bounds(X)
        else:
            bounds = self.bounds  # type: ignore

        if callable(self.p0):
            p0 = self.p0(X, y)
        else:
            p0 = self.p0

        self.X_ = X
        self.y_ = y

        popt, pcov = optimize.curve_fit(
            f=self.model_func,
            xdata=X,
            ydata=y,
            p0=p0,
            method=self.method,
            sigma=sigma,
            absolute_sigma=absolute_sigma,
            bounds=bounds,
            jac=self.jac,
            **self.lsq_kwargs,
        )

        self.popt_ = popt
        self.pcov_ = pcov
        self.name_ = self.model_func.__name__  # type: ignore

        return self


class MandVEnergyChangepointEstimator(ChangepointModelEnergyChangepointEstimator):
    """
    A child class which inherits from the EnergyChangepointEstimator parent class. You can access all of the properties
    and scores from the EnergyChangepointEstimator class from the changepointmodel library but this child class
    ensures that the data is sorted beforehand. By default, you must provide a MandVParameterModelFunction instance compared
    to EnergyChangepointEstimator where this is optional.
    """

    def __init__(
        self,
        model=MandVParameterModelFunction[
            ParamaterModelCallableT, EnergyParameterModelT
        ],
    ):
        if model and isinstance(model, MandVParameterModelFunction):
            self._model = model
            super().__init__(model=self._model)
        else:
            raise ValueError(
                "Must set `model` parameter to a `MandVParameterModelFunction` instance."
            )

    @check_data_model
    def fit(
        self,
        data_model: MandVDataModel,
        sigma: Optional[OneDimNDArray[np.float64]] = None,
        absolute_sigma: bool = False,
        **fit_params,
    ):
        """
        This is a wrapped around EnergyChangepointEstimator.fit that forces the data to be sorted by X. Use
        EnergyChangepointEstimator.fit if you don't need to force the data to be sorted by X.
        """
        self.data_model_ = data_model
        self.estimator_ = MandVCurvefitEstimator(
            model_func=self._model.f,
            bounds=self._model.bounds,
            p0=self._model.initial_guesses,
        )
        self.pred_y_ = self.estimator_.fit(
            self.data_model.X, self.data_model.y, sigma, absolute_sigma
        ).predict(self.data_model.X)

        self.X_, self.y_ = (
            self.estimator_.X_,
            self.estimator_.y_,
        )

        self.sigma_ = sigma
        self.absolute_sigma_ = absolute_sigma

        return self

    @property
    @check_not_fitted
    def data_model(self) -> MandVDataModel:
        """
        Returns the MandVDataModel object used to fit the model.
        """
        return self.data_model_
