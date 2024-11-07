from typing import Annotated, Any, Optional
from pydantic import BeforeValidator, PlainSerializer, WithJsonSchema
import pydantic
from changepointmodel.core.nptypes import NByOneNDArray, Ordering
from changepointmodel.core import CurvefitEstimatorDataModel
import numpy as np


def _validate_n_by_one_dim_timestamp(v: Any) -> NByOneNDArray[np.datetime64]:
    """
    Converts the input to a NByOneNDArray[np.datetime64] and raises an AssertionError
    if the shape of the data is anything other than M x 1.

    Args:
      v: Any: The input data

    Returns:
      NByOneNDArray[np.datetime64]: The converted data
    """
    arr = np.array(v, dtype=np.datetime64)

    assert (
        len(arr.shape) == 1
    ), f"Shape of data should be M x 1, got {arr.ndim}-dimensional array."

    return arr


# See this for the PlainSerializer: https://github.com/pydantic/pydantic/issues/7017
# See this for the WithJsonSchema annotation: https://docs.pydantic.dev/latest/concepts/json_schema/#withjsonschema-annotation
# Pydantic does not natively support numpy arrays for JSON schema generation
TimestampArrayField = Annotated[
    NByOneNDArray[np.datetime64],
    BeforeValidator(_validate_n_by_one_dim_timestamp),
    PlainSerializer(lambda x: np.datetime_as_string(x).tolist(), return_type=list),
    WithJsonSchema({"type": "array", "items": {"type": "np.datetime64"}}),
]


class MandVDataModel(CurvefitEstimatorDataModel):
    sensor_reading_timestamps: TimestampArrayField
    order: Optional[Ordering] = None
    """
  An extended version of CurvefitEstimatorDataModel that forces the data to be sorted by X
  """

    @pydantic.model_validator(mode="after")
    def check_sorted(self) -> "MandVDataModel":
        """
        Checks to see if the X values are sorted. If not, sorts them.
        """
        if any(self.X.squeeze() != np.sort(self.X.squeeze())):
            self.X, self.y, self.order = self.sorted_X_y()
            self.sensor_reading_timestamps = self.sensor_reading_timestamps[self.order]
        return self

    @pydantic.model_validator(mode="after")
    def validate_all(self) -> "MandVDataModel":
        """
        Asserts that the length of X, y, and sensor_reading_timestamps are the same
        """
        assert (
            len(self.X) == len(self.y) == len(self.sensor_reading_timestamps)
        ), "X, y, and sensor_reading_timestamps len must be the same"

        if self.sigma is not None and len(self.sigma) != len(self.X):
            raise ValueError("len of sigma must match len X and y")

        if self.order is not None and len(self.order) != len(self.X):
            raise ValueError("len of order must match len X and y")

        return self
