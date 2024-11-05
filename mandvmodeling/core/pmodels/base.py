from _collections_abc import Callable
from typing import Union, Tuple
from changepointmodel.core.nptypes import OneDimNDArray, NByOneNDArray
import numpy as np

InitialGuess = Tuple[float, ...]

InitialGuessCallable = Callable[
    [
        Union[OneDimNDArray[np.float64], NByOneNDArray[np.float64]],
        OneDimNDArray[np.float64],
    ],
    InitialGuess,
]