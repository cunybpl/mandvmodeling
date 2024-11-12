"""
Test to see that the init_guessses also work as well.
"""

import numpy as np
from numpy.testing import (
    assert_almost_equal,
    assert_array_equal,
    assert_array_almost_equal,
)
import pytest
from sklearn.exceptions import NotFittedError

from mandvmodeling.core.pmodels import MandVParameterModelFunction
from mandvmodeling.core.estimator import MandVEnergyChangepointEstimator
from mandvmodeling.core.schemas import MandVDataModel

# `cunybpl/changepointmodel` imports
from changepointmodel.core.pmodels import TwoParameterModel
from changepointmodel.core.pmodels.coeffs_parser import TwoParameterCoefficientParser
from changepointmodel.core.calc.models import twop


def test_mandvenergychangepointestimator_fit_calls_mandvcurvefitestimator_fit(mocker):
    bounds = ((0, -np.inf), (np.inf, np.inf))
    mymodel = MandVParameterModelFunction(
        name="2P",
        f=twop,
        bounds=bounds,
        parameter_model=TwoParameterModel(),
        coefficients_parser=TwoParameterCoefficientParser(),
    )

    est = MandVEnergyChangepointEstimator(model=mymodel)
    mock = mocker.spy(est, "fit")

    X = np.linspace(1, 10, 10)
    y = np.linspace(1, 10, 10)
    sensor_reading_timestamps = np.array(
        [
            "2024-10-20",
            "2024-10-21",
            "2024-10-22",
            "2024-10-23",
            "2024-10-24",
            "2024-10-25",
            "2024-10-26",
            "2024-10-27",
            "2024-10-28",
            "2024-10-29",
        ],
        dtype=np.datetime64,
    )

    data_model = MandVDataModel(
        X=X, y=y, sensor_reading_timestamps=sensor_reading_timestamps
    )

    est.fit(data_model=data_model)
    mock.assert_called_once()

    reshaped_X = X.reshape(-1, 1)
    assert_almost_equal(est.predict(reshaped_X), y, decimal=1)


def test_mandvenergychangepointestimator_properties_set_on_fit():
    bounds = ((0, -np.inf), (np.inf, np.inf))
    mymodel = MandVParameterModelFunction(
        name="2P",
        f=twop,
        bounds=bounds,
        parameter_model=TwoParameterModel(),
        coefficients_parser=TwoParameterCoefficientParser(),
    )

    X = np.linspace(1, 10, 10)
    y = np.linspace(1, 10, 10)
    sensor_reading_timestamps = np.array(
        [
            "2024-10-20",
            "2024-10-21",
            "2024-10-22",
            "2024-10-23",
            "2024-10-24",
            "2024-10-25",
            "2024-10-26",
            "2024-10-27",
            "2024-10-28",
            "2024-10-29",
        ],
        dtype=np.datetime64,
    )

    data_model = MandVDataModel(
        X=X, y=y, sensor_reading_timestamps=sensor_reading_timestamps
    )

    est = MandVEnergyChangepointEstimator(mymodel)
    est.fit(data_model)
    reshaped_X = X.reshape(-1, 1)

    assert est.name == "2P"

    assert_array_equal(reshaped_X, est.X)
    assert_array_equal(y, est.y)
    assert_array_equal(sensor_reading_timestamps, est.sensor_reading_timestamps)
    assert_almost_equal((0, 1), est.coeffs, decimal=1)
    assert_array_almost_equal(est.pred_y, y, decimal=1)
    assert est.sigma is None
    assert est.cov.all()
    assert est.absolute_sigma is False


def test_estimator_calculated_getter_methods():
    bounds = ((0, -np.inf), (np.inf, np.inf))
    mymodel = MandVParameterModelFunction(
        name="2P",
        f=twop,
        bounds=bounds,
        parameter_model=TwoParameterModel(),
        coefficients_parser=TwoParameterCoefficientParser(),
    )

    X = np.linspace(1, 10, 10)
    y = np.linspace(1, 10, 10)
    sensor_reading_timestamps = np.array(
        [
            "2024-10-20",
            "2024-10-21",
            "2024-10-22",
            "2024-10-23",
            "2024-10-24",
            "2024-10-25",
            "2024-10-26",
            "2024-10-27",
            "2024-10-28",
            "2024-10-29",
        ],
        dtype=np.datetime64,
    )

    data_model = MandVDataModel(
        X=X, y=y, sensor_reading_timestamps=sensor_reading_timestamps
    )

    est = MandVEnergyChangepointEstimator(mymodel)
    est.fit(data_model)

    assert est.n_params() == 2
    assert round(est.total_pred_y()) == np.sum(y)
    assert est.total_y() == np.sum(y)
    assert est.len_y() == len(y)


def test_unfit_estimator_raises_notfittederror_on_property_access():
    est = MandVEnergyChangepointEstimator()

    with pytest.raises(NotFittedError):
        est.X

    with pytest.raises(NotFittedError):
        est.y

    with pytest.raises(NotFittedError):
        est.pred_y

    with pytest.raises(NotFittedError):
        est.sigma

    with pytest.raises(NotFittedError):
        est.absolute_sigma

    with pytest.raises(NotFittedError):
        est.cov


def test_unfit_estimator_raises_notfitted_error_on_method_calls():
    est = MandVEnergyChangepointEstimator()
    X = 42

    with pytest.raises(NotFittedError):
        est.predict(X)

    with pytest.raises(NotFittedError):
        est.predict(X)

    with pytest.raises(NotFittedError):
        est.adjust(X)


def test_name_accessor_raises_valueerror_if_model_not_set():
    est = MandVEnergyChangepointEstimator()
    with pytest.raises(ValueError):
        est.name


def test_estimator_adjust_calls_predict_with_other_x(mocker):
    bounds = ((0, -np.inf), (np.inf, np.inf))
    mymodel = MandVParameterModelFunction(
        name="2P",
        f=twop,
        bounds=bounds,
        parameter_model=TwoParameterModel(),
        coefficients_parser=TwoParameterCoefficientParser(),
    )

    X1 = np.linspace(1, 10, 10)
    y1 = np.linspace(1, 10, 10)
    sensor_reading_timestamps1 = np.array(
        [
            "2024-10-20",
            "2024-10-21",
            "2024-10-22",
            "2024-10-23",
            "2024-10-24",
            "2024-10-25",
            "2024-10-26",
            "2024-10-27",
            "2024-10-28",
            "2024-10-29",
        ],
        dtype=np.datetime64,
    )

    data_model1 = MandVDataModel(
        X=X1, y=y1, sensor_reading_timestamps=sensor_reading_timestamps1
    )

    X2 = np.linspace(10, 1, 10)
    y2 = np.linspace(10, 1, 10)
    sensor_reading_timestamps2 = np.array(
        [
            "2024-10-29",
            "2024-10-28",
            "2024-10-27",
            "2024-10-26",
            "2024-10-25",
            "2024-10-24",
            "2024-10-23",
            "2024-10-22",
            "2024-10-21",
            "2024-10-20",
        ],
        dtype=np.datetime64,
    )

    data_model2 = MandVDataModel(
        X=X2, y=y2, sensor_reading_timestamps=sensor_reading_timestamps2
    )

    est1 = MandVEnergyChangepointEstimator(mymodel)
    est1.fit(data_model1)

    est2 = MandVEnergyChangepointEstimator(mymodel)
    est2.fit(data_model2)

    mock = mocker.spy(est1, "predict")
    reshaped_X1 = X1.reshape(-1, 1)
    est1.adjust(est2)
    assert_array_equal(mock.call_args_list[0][0][0], reshaped_X1)


def test_estimator_for_methods(mocker):
    bounds = ((0, -np.inf), (np.inf, np.inf))
    mymodel = MandVParameterModelFunction(
        name="2P",
        f=twop,
        bounds=bounds,
        parameter_model=TwoParameterModel(),
        coefficients_parser=TwoParameterCoefficientParser(),
    )

    est = MandVEnergyChangepointEstimator(model=mymodel)
    mock = mocker.spy(est, "fit")

    X = np.linspace(1, 10, 10)
    y = np.linspace(1, 10, 10)
    reshaped_X = X.reshape(-1, 1)
    sensor_reading_timestamps = np.array(
        [
            "2024-10-20",
            "2024-10-21",
            "2024-10-22",
            "2024-10-23",
            "2024-10-24",
            "2024-10-25",
            "2024-10-26",
            "2024-10-27",
            "2024-10-28",
            "2024-10-29",
        ],
        dtype=np.datetime64,
    )

    data_model = MandVDataModel(
        X=X, y=y, sensor_reading_timestamps=sensor_reading_timestamps
    )

    est.fit(data_model)
    mock.assert_called_once()

    assert_almost_equal(est.predict(reshaped_X), y, decimal=1)
    assert_almost_equal(est.r2(), 1, decimal=1)
    assert_almost_equal(est.adjusted_r2(), 1, decimal=1)
    assert_almost_equal(est.rmse(), 2.32678e-05, decimal=1)
    assert_almost_equal(est.cvrmse(), 4.23051e-06, decimal=1)
    assert est.dpop() == (0, 10)
    assert_almost_equal(est.tstat()[1], 349150.818, decimal=1)
    assert est.shape()
    load_ = est.load()
    assert_almost_equal(load_.cooling, 54.999605, decimal=1)
    assert_almost_equal(load_.base, sum(X) - load_.cooling, decimal=1)


def test_estimator_assert_unretrievable_data_model(mocker):
    bounds = ((0, -np.inf), (np.inf, np.inf))
    mymodel = MandVParameterModelFunction(
        name="2P",
        f=twop,
        bounds=bounds,
        parameter_model=TwoParameterModel(),
        coefficients_parser=TwoParameterCoefficientParser(),
    )

    est = MandVEnergyChangepointEstimator(model=mymodel)
    mock = mocker.spy(est, "fit")

    X = np.linspace(1, 10, 10)
    y = np.linspace(1, 10, 10)
    sensor_reading_timestamps = np.array(
        [
            "2024-10-20",
            "2024-10-21",
            "2024-10-22",
            "2024-10-23",
            "2024-10-24",
            "2024-10-25",
            "2024-10-26",
            "2024-10-27",
            "2024-10-28",
            "2024-10-29",
        ],
        dtype=np.datetime64,
    )

    data_model = MandVDataModel(
        X=X, y=y, sensor_reading_timestamps=sensor_reading_timestamps
    )

    est.fit(data_model)
    mock.assert_called_once()

    with pytest.raises(AttributeError):
        est.__data_model

    with pytest.raises(AttributeError):
        est.data_model


def test_estimator_scalar_handling_for_load_and_nac(mocker):
    bounds = ((0, -np.inf), (np.inf, np.inf))
    mymodel = MandVParameterModelFunction(
        name="2P",
        f=twop,
        bounds=bounds,
        parameter_model=TwoParameterModel(),
        coefficients_parser=TwoParameterCoefficientParser(),
    )

    est = MandVEnergyChangepointEstimator(model=mymodel)
    mock = mocker.spy(est, "fit")

    X = np.linspace(1, 10, 10)
    y = np.linspace(1, 10, 10)
    reshaped_X = X.reshape(-1, 1)
    sensor_reading_timestamps = np.array(
        [
            "2024-10-20",
            "2024-10-21",
            "2024-10-22",
            "2024-10-23",
            "2024-10-24",
            "2024-10-25",
            "2024-10-26",
            "2024-10-27",
            "2024-10-28",
            "2024-10-29",
        ],
        dtype=np.datetime64,
    )

    data_model = MandVDataModel(
        X=X, y=y, sensor_reading_timestamps=sensor_reading_timestamps
    )

    est.fit(data_model)
    mock.assert_called_once()

    load_not_scaled = est.load()
    load_scaled = est.load(scalar=30.437)

    assert_almost_equal(load_scaled.base, load_not_scaled.base * 30.437)
    assert_almost_equal(load_scaled.cooling, load_not_scaled.cooling * 30.437)
    assert_almost_equal(load_scaled.heating, load_not_scaled.heating * 30.437)

    nac_not_scaled = est.nac(reshaped_X)
    nac_scaled = est.nac(reshaped_X, scalar=30.437)

    assert_almost_equal(nac_scaled, nac_not_scaled * 30.437)
