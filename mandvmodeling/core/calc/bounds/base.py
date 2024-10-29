from typing import Tuple, Union, Callable
from ...nptypes import OneDimNDArray, NByOneNDArray
from numpy import float64

BoundTuple = Tuple[Tuple[float, ...], Tuple[float, ...]]
TwoParameterBoundary = Tuple[float, float]
ThreeParameterBoundary = Tuple[float, float, float]
FourParameterBoundary = Tuple[float, float, float, float]
FiveParameterBoundary = Tuple[float, float, float, float, float]

OpenBoundCallable = Callable[
    [Union[OneDimNDArray[float64], NByOneNDArray[float64]]], BoundTuple
]
