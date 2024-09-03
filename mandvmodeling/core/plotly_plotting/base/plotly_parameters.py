import abc
from typing import Union, Dict, Tuple, List
from changepointmodel.core.nptypes import OneDimNDArray, NByOneNDArray
import dataclasses
import numpy as np

class IPlotlyParameters(abc.ABC):
  """
  This is an abstract base class for defining Plotly parameters.

  Attributes:
      mode (str): The mode of Plotly plot.
      name (str): The name of the Plotly plot.
  """

  mode: str
  name: str

  @abc.abstractmethod
  def to_dict(self) -> Dict[str, Union[OneDimNDArray[np.float64], str]]:
    """
    Abstract method to convert Plotly parameters to a dictionary.

    Returns:
        Dict[str, Union[OneDimNDArray[np.float64], str]]: The dictionary containing Plotly parameters.
    """
    ... #pragma: no cover

@dataclasses.dataclass(kw_only = True)
class PlotlyModelCoordinates:
    """
    Dataclass to store coordinates for Plotly models.

    Attributes:
        FirstCoordinate (Tuple[float, float]): The first coordinate of the model.
        LastCoordinate (Tuple[float, float]): The last coordinate of the model.
        ChangepointCoordinates (List[Tuple[float, float]]): List of coordinates
        representing changepoints in the model.
    """
    FirstCoordinate: Tuple[float, float]
    LastCoordinate:  Tuple[float, float]
    ChangepointCoordinates: List[Tuple[float, float]] = dataclasses.field(default_factory = lambda: [])

@dataclasses.dataclass(kw_only = True)
class PlotlyRawDataCoordinates:
  """
  Dataclass to store raw data coordinates for Plotly.

  Attributes:
      x (NByOneNDArray[np.float64]): N-by-one dimensional array of x-coordinates.
      y (OneDimNDArray[np.float64]): One-dimensional array of y-coordinates.
  """
  x: NByOneNDArray[np.float64]
  y: OneDimNDArray[np.float64]

@dataclasses.dataclass(kw_only = True)
class PlotlyModelParameters(PlotlyModelCoordinates, IPlotlyParameters):
    """
    Dataclass which stores parameters to plot the changepoint model on a Plotly figure layer.

    Inherits from PlotlyModelCoordinates to provide coordinate data
    and implements the IPlotlyParameters interface.

    Attributes:
        mode (str): The mode of the Plotly plot. Default is 'markers + lines'.
        name (str): The name of the Plotly plot. Default is 'Model'.
    """
    mode: str = 'markers + lines'
    name: str = 'Model'

    def to_dict(self) -> Dict[str, Union[OneDimNDArray[np.float64], str]]:
        """
        Convert Plotly model parameters to a dictionary.

        Returns:
            Dict[str, Union[OneDimNDArray[np.float64], str]]: The dictionary containing Plotly model parameters.
        """
        return dict(
            x = np.array([self.FirstCoordinate[0]] + [changepoint[0] for changepoint in self.ChangepointCoordinates] + [self.LastCoordinate[0]]),
            y = np.array([self.FirstCoordinate[1]] + [changepoint[1] for changepoint in self.ChangepointCoordinates] + [self.LastCoordinate[1]]),
            mode = self.mode,
            name = self.name
        )

@dataclasses.dataclass(kw_only = True)
class PlotlyRawDataParameters(PlotlyRawDataCoordinates, IPlotlyParameters):
  """
  Dataclass which stores parameters to plot the raw data on a Plotly figure layer.

  Inherits from PlotlyRawDataCoordinates to provide coordinate data
  and implements the IPlotlyParameters interface.

  Attributes:
      mode (str): The mode of the Plotly plot. Default is 'markers'.
      name (str): The name of the Plotly plot. Default is 'Raw Data'.
  """
  mode: str = 'markers'
  name: str = 'Raw Data'

  def to_dict(self) -> Dict[str, Union[OneDimNDArray[np.float64], str]]:
    """
    Convert Plotly raw data parameters to a dictionary.

    Returns:
        Dict[str, Union[OneDimNDArray[np.float64], str]]: The dictionary containing Plotly raw data parameters.
    """
    return dict(
        x = self.x.squeeze(),
        y = self.y,
        mode = self.mode,
        name = self.name
    )