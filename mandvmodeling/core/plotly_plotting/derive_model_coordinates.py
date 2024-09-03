from .base import ICoordinatesParser, PlotlyModelParameters
from changepointmodel.core.nptypes import OneDimNDArray
from typing import Tuple
import numpy as np

class PlotlyParameterModelCoordinates:
    """
    A class used to represent Plotly Parameter Model Coordinates.

    Attributes
    ----------
    name : str
        The name of the plotly parameter model.
    mode : str, optional
        The mode of the plotly parameter model, by default 'markers + lines'.
    _model_coordinates_parser : ICoordinatesParser
        The parser used to generate coordinates from model data.

    Methods
    -------
    parse_model_coordinates(X, pred_y, coeffs=None)
        Parses the model coordinates given the input data and returns Plotly model coordinates.
    """

    def __init__(
            self,
            name: str,
            mode: str = 'markers + lines',
            model_coordinates_parser = ICoordinatesParser
    ):
        """
        Constructs all the necessary attributes for the PlotlyParameterModelCoordinates object.

        Parameters
        ----------
        name : str
            The name of the plotly parameter model.
        mode : str, optional
            The mode of the plotly parameter model, by default 'markers + lines'.
        model_coordinates_parser : ICoordinatesParser
            The parser used to generate coordinates from model data.
        """
        self.name = name
        self.mode = mode
        self._model_coordinates_parser = model_coordinates_parser

    def parse_model_coordinates(
            self,
            X: OneDimNDArray[np.float64],
            pred_y: OneDimNDArray[np.float64],
            coeffs: Tuple[float, ...] = None
    ) -> PlotlyModelParameters:
        """
        Parses the model coordinates given the input data.

        Parameters
        ----------
        X : OneDimNDArray[np.float64]
            The input data for the X coordinates.
        pred_y : OneDimNDArray[np.float64]
            The predicted Y coordinates based on the model.
        coeffs : tuple, optional
            The coefficients used by the model, by default None.

        Returns
        -------
        PlotlyModelCoordinates
            The parsed coordinates for the Plotly model.
        """
        return self._model_coordinates_parser.generate_coordinates(X, pred_y, coeffs)