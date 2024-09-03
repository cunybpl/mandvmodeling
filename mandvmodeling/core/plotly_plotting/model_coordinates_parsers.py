from typing import Tuple
from .base.coordinates import AbstractCoordinatesGenerator
from .base.plotly_parameters import PlotlyModelParameters
from changepointmodel.core.nptypes import OneDimNDArray
import numpy as np

class TwoParameterCoordinatesParser(AbstractCoordinatesGenerator):
    """
    A parser for generating coordinates for two parameter changepoint models.

    This class generates boundary coordinates based on input arrays
    X, pred_y, and a tuple of coefficients.

    Methods
    -------
    generate_coordinates(X, pred_y, coeffs)
        Generates boundary coordinates based on the provided data.
    """

    def generate_coordinates(
        self,
        X: OneDimNDArray[np.float64],
        pred_y: OneDimNDArray[np.float64],
        coeffs: Tuple[float, ...]
    ) -> PlotlyModelParameters:
        """
        Generate coordinates using provided X, pred_y, and coeffs.

        Parameters
        ----------
        X : OneDimNDArray[np.float64]
            The input array representing the x-coordinates.
        pred_y : OneDimNDArray[np.float64]
            The predicted y-coordinates corresponding to X.
        coeffs : Tuple[float, ...]
            A tuple containing required coefficients for coordinate generation.

        Returns
        -------
        PlotlyModelParameters
            An object containing generated plotly coordinates.
        """
        _, _ = coeffs
        return self._generate_bound_coordinates(X, pred_y)


class ThreeParameterCoordinatesParser(AbstractCoordinatesGenerator):
    """
    A parser for generating coordinates for three parameter changepoint models.

    This class generates boundary coordinates based on input arrays
    X, pred_y, and a tuple of coefficients including a changepoint.

    Methods
    -------
    generate_coordinates(X, pred_y, coeffs)
        Generates boundary and changepoint coordinates based on the provided data.
    """
    def generate_coordinates(
        self,
        X: OneDimNDArray[np.float64],
        pred_y: OneDimNDArray[np.float64],
        coeffs: Tuple[float, ...],
    ) -> PlotlyModelParameters:
        """
        Generate coordinates using provided X, pred_y, and coeffs.

        Parameters
        ----------
        X : OneDimNDArray[np.float64]
            The input array representing the x-coordinates.
        pred_y : OneDimNDArray[np.float64]
            The predicted y-coordinates corresponding to X.
        coeffs : Tuple[float, ...]
            A tuple containing required coefficients for coordinate generation,
            including a changepoint value.

        Returns
        -------
        PlotlyModelParameters
            An object containing generated plotly coordinates including the changepoint.
        """
        bound_coordinates = self._generate_bound_coordinates(X, pred_y)
        _, _, changepoint = coeffs
        changepoint_coordinates = self._generate_changepoint_coordinates(
            pred_y, [changepoint]
        )
        return PlotlyModelParameters(
            FirstCoordinate=bound_coordinates.FirstCoordinate,
            LastCoordinate=bound_coordinates.LastCoordinate,
            ChangepointCoordinates=changepoint_coordinates,
        )


class FourParameterCoordinatesParser(AbstractCoordinatesGenerator):
    """
    A parser for generating coordinates for four parameter changepoint models.

    This class generates boundary coordinates based on input arrays
    X, pred_y, and a tuple of coefficients including a changepoint.

    Methods
    -------
    generate_coordinates(X, pred_y, coeffs)
        Generates boundary and changepoint coordinates based on the provided data.
    """

    def generate_coordinates(
        self,
        X: OneDimNDArray[np.float64],
        pred_y: OneDimNDArray[np.float64],
        coeffs: Tuple[float, ...],
    ) -> PlotlyModelParameters:
        """
        Generate coordinates using provided X, pred_y, and coeffs.

        Parameters
        ----------
        X : OneDimNDArray[np.float64]
            The input array representing the x-coordinates.
        pred_y : OneDimNDArray[np.float64]
            The predicted y-coordinates corresponding to X.
        coeffs : Tuple[float, ...]
            A tuple containing required coefficients for coordinate generation,
            including a changepoint value.

        Returns
        -------
        PlotlyModelParameters
            An object containing generated plotly coordinates including the changepoint.
        """
        bound_coordinates = self._generate_bound_coordinates(X, pred_y)
        _, _, _, changepoint = coeffs
        changepoint_coordinates = self._generate_changepoint_coordinates(
            pred_y, [changepoint]
        )
        return PlotlyModelParameters(
            FirstCoordinate=bound_coordinates.FirstCoordinate,
            LastCoordinate=bound_coordinates.LastCoordinate,
            ChangepointCoordinates=changepoint_coordinates,
        )

class FiveParameterCoordinatesParser(AbstractCoordinatesGenerator):
    """
    A parser for generating coordinates for five parameter changepoint models.

    This class generates boundary coordinates based on input arrays
    X, pred_y, and a tuple of coefficients including two changepoint values.

    Methods
    -------
    generate_coordinates(X, pred_y, coeffs)
        Generates boundary and changepoint coordinates based on the provided data.
    """

    def generate_coordinates(
        self,
        X: OneDimNDArray[np.float64],
        pred_y: OneDimNDArray[np.float64],
        coeffs: Tuple[float, ...],
    ) -> PlotlyModelParameters:
        """
        Generate coordinates using provided X, pred_y, and coeffs.

        Parameters
        ----------
        X : OneDimNDArray[np.float64]
            The input array representing the x-coordinates.
        pred_y : OneDimNDArray[np.float64]
            The predicted y-coordinates corresponding to X.
        coeffs : Tuple[float, ...]
            A tuple containing required coefficients for coordinate generation,
            including two changepoint values.

        Returns
        -------
        PlotlyModelParameters
            An object containing generated plotly coordinates including the changepoints.
        """
        bound_coordinates = self._generate_bound_coordinates(X, pred_y)
        _, _, _, left_changepoint, right_changepoint = coeffs
        changepoint_coordinates = self._generate_changepoint_coordinates(
            pred_y, [left_changepoint, right_changepoint]
        )
        return PlotlyModelParameters(
            FirstCoordinate=bound_coordinates.FirstCoordinate,
            LastCoordinate=bound_coordinates.LastCoordinate,
            ChangepointCoordinates=changepoint_coordinates,
        )
