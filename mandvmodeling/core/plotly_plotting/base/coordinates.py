import abc
from changepointmodel.core.nptypes import OneDimNDArray
from typing import Tuple, List, TypeVar
from ..base.plotly_parameters import PlotlyModelCoordinates
import numpy as np

class ICoordinatesParser:
    """
    An abstract base class that defines the interface for generating coordinates.

    Methods:
    --------
    generate_coordinates(
    X: OneDimNDArray[np.float64],
    y: OneDimNDArray[np.float64],
    parsed_coeffs: Tuple[float, ...]) -> PlotlyModelCoordinates
        Generates the coordinates required for a Plotly plot.
    """

    @abc.abstractmethod
    def generate_coordinates(
        self,
        X: OneDimNDArray[np.float64],
        y: OneDimNDArray[np.float64],
        coeffs: Tuple[float, ...],
    ) -> PlotlyModelCoordinates: ...  # pragma: no cover


class BoundCoordinatesParser:
    """
    A parser class to generate boundary coordinates for plotting.

    Methods:
    --------
    _generate_bound_coordinates(
        X: OneDimNDArray[np.float64], pred_y: OneDimNDArray[np.float64]
    ) -> PlotlyModelCoordinates:
        Generate the first and last coordinates based on input arrays.
    """

    def _generate_bound_coordinates(
        self, X: OneDimNDArray[np.float64], pred_y: OneDimNDArray[np.float64]
    ) -> PlotlyModelCoordinates:
        """
        Generate the first and last coordinates for a plot.

        Parameters:
        -----------
        X : OneDimNDArray[np.float64]
            Array of x-axis values.
        pred_y : OneDimNDArray[np.float64]
            Array of predicted y-axis values.

        Returns:
        --------
        PlotlyModelCoordinates
            Dataclass containing the first and last coordinates.
        """
        first_coordinate = (X[0], pred_y[0])
        last_coordinate = (X[-1], pred_y[-1])
        return PlotlyModelCoordinates(
            FirstCoordinate=first_coordinate, LastCoordinate=last_coordinate
        )


class ChangepointCoordinatesParser:
    """
    A parser class to generate coordinates for changepoints.

    Methods:
    --------
    _generate_changepoint_coordinates(
        pred_y: OneDimNDArray[np.float64], changepoints: List[float]
    ) -> List[Tuple[float, float]]:
        Generate coordinates for each changepoint based on the minimum value of
        the predicted y-axis values.
    """

    def _generate_changepoint_coordinates(
        self, pred_y: OneDimNDArray[np.float64], changepoints: List[float]
    ) -> List[Tuple[float, float]]:
        """
        Generate coordinates for changepoints.

        Parameters:
        -----------
        pred_y : OneDimNDArray[np.float64]
            Array of predicted y-axis values.
        changepoints : List[float]
            List of changepoint positions on x-axis.

        Returns:
        --------
        List[Tuple[float, float]]
            List of tuples, each containing a changepoint position and the
            minimum predicted y value.
        """
        return [(changepoint, min(pred_y)) for changepoint in changepoints]


class AbstractCoordinatesGenerator(
    BoundCoordinatesParser, ChangepointCoordinatesParser, ICoordinatesParser
):
    """
    An abstract class that combines functionalities from
    BoundCoordinatesParser, ChangepointCoordinatesParser,
    and ICoordinatesParser to generate different types of coordinates.

    Inherits:
    ---------
    BoundCoordinatesParser:
        Provides methods to generate boundary coordinates.
    ChangepointCoordinatesParser:
        Provides methods to generate coordinates for changepoints.
    ICoordinatesParser:
        Defines the interface for coordinate generation.

    This class is abstract and is intended to be subclassed with an
    implementation of the generate_coordinates method.
    """

    ...  # pragma: no cover
  
class ICoordinatesParser:
    """
    An abstract base class that defines the interface for generating coordinates.

    Methods:
    --------
    generate_coordinates(
    X: OneDimNDArray[np.float64],
    y: OneDimNDArray[np.float64],
    parsed_coeffs: Tuple[float, ...]) -> PlotlyModelCoordinates
        Generates the coordinates required for a Plotly plot.
    """

    @abc.abstractmethod
    def generate_coordinates(
        self,
        X: OneDimNDArray[np.float64],
        y: OneDimNDArray[np.float64],
        coeffs: Tuple[float, ...],
    ) -> PlotlyModelCoordinates: ...  # pragma: no cover


class BoundCoordinatesParser:
    """
    A parser class to generate boundary coordinates for plotting.

    Methods:
    --------
    _generate_bound_coordinates(
        X: OneDimNDArray[np.float64], pred_y: OneDimNDArray[np.float64]
    ) -> PlotlyModelCoordinates:
        Generate the first and last coordinates based on input arrays.
    """

    def _generate_bound_coordinates(
        self, X: OneDimNDArray[np.float64], pred_y: OneDimNDArray[np.float64]
    ) -> PlotlyModelCoordinates:
        """
        Generate the first and last coordinates for a plot.

        Parameters:
        -----------
        X : OneDimNDArray[np.float64]
            Array of x-axis values.
        pred_y : OneDimNDArray[np.float64]
            Array of predicted y-axis values.

        Returns:
        --------
        PlotlyModelCoordinates
            Dataclass containing the first and last coordinates.
        """
        first_coordinate = (X[0], pred_y[0])
        last_coordinate = (X[-1], pred_y[-1])
        return PlotlyModelCoordinates(
            FirstCoordinate=first_coordinate, LastCoordinate=last_coordinate
        )


class ChangepointCoordinatesParser:
    """
    A parser class to generate coordinates for changepoints.

    Methods:
    --------
    _generate_changepoint_coordinates(
        pred_y: OneDimNDArray[np.float64], changepoints: List[float]
    ) -> List[Tuple[float, float]]:
        Generate coordinates for each changepoint based on the minimum value of
        the predicted y-axis values.
    """

    def _generate_changepoint_coordinates(
        self, pred_y: OneDimNDArray[np.float64], changepoints: List[float]
    ) -> List[Tuple[float, float]]:
        """
        Generate coordinates for changepoints.

        Parameters:
        -----------
        pred_y : OneDimNDArray[np.float64]
            Array of predicted y-axis values.
        changepoints : List[float]
            List of changepoint positions on x-axis.

        Returns:
        --------
        List[Tuple[float, float]]
            List of tuples, each containing a changepoint position and the
            minimum predicted y value.
        """
        return [(changepoint, min(pred_y)) for changepoint in changepoints]


class AbstractCoordinatesGenerator(
    BoundCoordinatesParser, ChangepointCoordinatesParser, ICoordinatesParser
):
    """
    An abstract class that combines functionalities from
    BoundCoordinatesParser, ChangepointCoordinatesParser,
    and ICoordinatesParser to generate different types of coordinates.

    Inherits:
    ---------
    BoundCoordinatesParser:
        Provides methods to generate boundary coordinates.
    ChangepointCoordinatesParser:
        Provides methods to generate coordinates for changepoints.
    ICoordinatesParser:
        Defines the interface for coordinate generation.

    This class is abstract and is intended to be subclassed with an
    implementation of the generate_coordinates method.
    """

    ...  # pragma: no cover

PlotlyCoordinatesGeneratorT = TypeVar(
    "PlotlyCoordinatesGeneratorT", bound = AbstractCoordinatesGenerator
)
