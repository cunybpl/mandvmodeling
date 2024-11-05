from mandvmodeling.core import schemas
import numpy as np
import pytest
import pydantic

def test_MandVDataModel_handles_timestamp_data():
    xdata = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    ydata = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    timestampdata = np.array([
    "2024-01-15 11:30:00",
    "2024-03-15 11:30:00",
    "2024-06-15 11:30:00",
    "2024-07-15 11:30:00",
    "2024-08-15 11:30:00"
    ])
    schemas.MandVDataModel(X=xdata, y=ydata, sensor_reading_timestamps=timestampdata)

def test_MandVDataModel_timestamps_are_of_type_timestamp():
    xdata = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    ydata = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    timestampdata = np.array([
    "2024-01-15 11:30:00",
    "2024-03-15 11:30:00",
    "2024-06-15 11:30:00",
    "2024-07-15 11:30:00",
    "2024-08-15 11:30:00"
    ])
    test = schemas.MandVDataModel(X=xdata, y=ydata, sensor_reading_timestamps=timestampdata)
    assert isinstance(test.sensor_reading_timestamps[0], np.datetime64)

def test_MandVDataModel_raise_validationerror_on_len_mismatch():
    xdata = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    ydata = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    timestampdata = np.array([
    "2024-01-15 11:30:00",
    "2024-03-15 11:30:00",
    "2024-06-15 11:30:00",
    "2024-07-15 11:30:00"
    ])
    sigma = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

    # check various combos of len mismatch for timestampdata
    with pytest.raises(pydantic.ValidationError):
        schemas.MandVDataModel(X=xdata, y=ydata, sensor_reading_timestamps=timestampdata)
    
    with pytest.raises(pydantic.ValidationError):
        schemas.MandVDataModel(X = xdata, y = ydata, sensor_reading_timestamps=timestampdata, sigma=sigma)
    
    with pytest.raises(pydantic.ValidationError):
        timestampdata = np.array([
        "2024-01-15 11:30:00",
        "2024-03-15 11:30:00",
        "2024-06-15 11:30:00",
        "2024-07-15 11:30:00",
        "2024-08-15 11:30:00"
        ])
        sigma = np.array([1.0, 2.0, 3.0, 4.0])
        schemas.MandVDataModel(X = xdata, y=ydata, sensor_reading_timestamps=timestampdata, sigma=sigma)

    with pytest.raises(pydantic.ValidationError):
        ydata = ([1.0, 2.0, 3.0, 4.0])
        sigma = np.array([1.0, 2.0, 3.0])
        schemas.MandVDataModel(X=xdata, y=ydata, sensor_reading_timestamps=timestampdata)


def test_MandVDataModel_forgot_timestamps():
    # This shows you how to parse through the error: https://docs.pydantic.dev/latest/errors/validation_errors/#arguments_type
    xdata = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    ydata = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    try:
        test = schemas.MandVDataModel(X = xdata, y = ydata)
    except pydantic.ValidationError as e:
        assert e.errors()[0]["type"] == "missing"

def test_MandVDataModel_returns_sorted_X_y_timestamps():
    xdata = np.array([3.0, 5.0, 1.0, 2.0, 4.0])
    ydata = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    timestamp_data =  np.array([
        "2024-01-15 11:30:00",
        "2024-03-15 11:30:00",
        "2024-06-15 11:30:00",
        "2024-07-15 11:30:00",
        "2024-08-15 11:30:00"
        ])
    
    test = schemas.MandVDataModel(
        X=xdata,
        y=ydata,
        sensor_reading_timestamps=timestamp_data
    )

    assert [list(x) for x in test.X] == [[1.0], [2.0], [3.0], [4.0], [5.0]]
    assert list(test.y) == [3.0, 4.0, 1.0, 5.0, 2.0]
    assert [str(x) for x in test.sensor_reading_timestamps] == [
        '2024-06-15T11:30:00', 
        '2024-07-15T11:30:00', 
        '2024-01-15T11:30:00', 
        '2024-08-15T11:30:00',
        '2024-03-15T11:30:00'
        ]