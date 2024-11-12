from mandvmodeling.core import estimator as MandVModelingEstimator
from mandvmodeling.core import schemas as MandVModelingSchemas
from mandvmodeling.core.pmodels import MandVParameterModelFunction
from mandvmodeling.core.calc.bounds import default_bounds

from changepointmodel.core.pmodels import coeffs_parser as ChangepointModelCoeffsParsers
from changepointmodel.core.calc import models as ChangepointModelModels
from changepointmodel.core.pmodels.parameter_model import (
    TwoParameterModel,
    ThreeParameterCoolingModel,
    ThreeParameterHeatingModel,
    FourParameterModel,
    FiveParameterModel,
)
import numpy as np
from numpy.testing import assert_almost_equal


def test_2p_daily(generated_2p_data_daily_pre, TestLoadInstance):
    Xdata = np.array(generated_2p_data_daily_pre["X"])
    ydata = np.array(generated_2p_data_daily_pre["y"])
    sensor_reading_timestamps_data = np.array(generated_2p_data_daily_pre["Date"])

    parameter_model = MandVParameterModelFunction(
        name="2P",
        f=ChangepointModelModels.twop,
        bounds=default_bounds.twop,
        parameter_model=TwoParameterModel(),
        coefficients_parser=ChangepointModelCoeffsParsers.TwoParameterCoefficientParser(),
    )

    est = MandVModelingEstimator.MandVEnergyChangepointEstimator(model=parameter_model)
    data_model = MandVModelingSchemas.MandVDataModel(
        X=Xdata, y=ydata, sensor_reading_timestamps=sensor_reading_timestamps_data
    )

    est.original_ordering = data_model.order
    est.fit(data_model)

    # coeffs
    exp_yint = 317.1907
    exp_slopes = 10.9663
    assert_almost_equal(exp_yint, est.coeffs[0], decimal=4)
    assert_almost_equal(exp_slopes, est.coeffs[1], decimal=4)

    # print(TestLoadInstance._heating(X = est.X.squeeze(), pred_y = est.pred_y, slope = est.coeffs[1], yint = est.coeffs[0]))
    # print(TestLoadInstance._cooling(X = est.X.squeeze(), pred_y = est.pred_y, slope = est.coeffs[1], yint = est.coeffs[0]))
    # heating = TestLoad()._heating(X = est.X.squeeze(), pred_y = est.pred_y, slope = est.coeffs[1], yint = est.coeffs[0])
    # cooling = TestLoad()._cooling(X = est.X.squeeze(), pred_y = est.pred_y, slope = est.coeffs[1], yint = est.coeffs[0])
    # print(TestLoad()._base(est.total_pred_y(), heating, cooling))
    # assert 1 == 3

    # loads
    loads_ = est.load()
    exp_baseload = 115774.59064052236
    exp_heating = 0
    exp_cooling = 222273.38831987552

    assert_almost_equal(exp_baseload, loads_.base, decimal=4)
    assert_almost_equal(exp_heating, loads_.heating, decimal=4)
    assert_almost_equal(exp_cooling, loads_.cooling, decimal=4)

    # Test ILoad in `changepointmodel.core.pmodels.base`
    ILoad_heating_test = TestLoadInstance._heating(
        X=est.X.squeeze(), pred_y=est.pred_y, slope=est.coeffs[1], yint=est.coeffs[0]
    )
    ILoad_cooling_test = TestLoadInstance._cooling(
        X=est.X.squeeze(), pred_y=est.pred_y, slope=est.coeffs[1], yint=est.coeffs[0]
    )
    ILoad_base_test = TestLoadInstance._base(
        est.total_pred_y(), ILoad_heating_test, ILoad_cooling_test
    )
    assert_almost_equal(
        exp_cooling,
        ILoad_cooling_test,
        decimal=4,
    )
    assert_almost_equal(exp_heating, ILoad_heating_test, decimal=4)
    assert_almost_equal(exp_baseload, ILoad_base_test, decimal=4)

    est.r2()
    est.cvrmse()
    left_tstat, right_tstat = est.tstat()
    assert left_tstat is None
    assert right_tstat  # slope > 0

    # dpop +
    heatnum, coolnum = est.dpop()
    assert coolnum == len(Xdata)
    assert heatnum == 0  # slope > 0 so cooling
    assert est.shape()


def test_3pc_daily(generated_three_pc_data_daily_pre, TestLoadInstance):
    Xdata = np.array(generated_three_pc_data_daily_pre["X"])
    ydata = np.array(generated_three_pc_data_daily_pre["y"])
    sensor_reading_timestamps_data = np.array(generated_three_pc_data_daily_pre["Date"])

    parameter_model = MandVParameterModelFunction(
        name="3PC",
        f=ChangepointModelModels.threepc,
        bounds=default_bounds.threepc,
        parameter_model=ThreeParameterCoolingModel(),
        coefficients_parser=ChangepointModelCoeffsParsers.ThreeParameterCoefficientsParser(),
    )
    est = MandVModelingEstimator.MandVEnergyChangepointEstimator(model=parameter_model)
    data_model = MandVModelingSchemas.MandVDataModel(
        X=Xdata, y=ydata, sensor_reading_timestamps=sensor_reading_timestamps_data
    )

    est.original_ordering = data_model.order
    est.fit(data_model)

    # coeffs
    exp_yint = 751.5908209
    exp_slopes = 11.33953386
    exp_cp = 60.97490617
    assert_almost_equal(exp_yint, est.coeffs[0], decimal=4)
    assert_almost_equal(exp_slopes, est.coeffs[1], decimal=4)
    assert_almost_equal(exp_cp, est.coeffs[2], decimal=4)

    # loads
    loads_ = est.load()

    exp_baseload = 274330.64962937066
    exp_heating = 0
    exp_cooling = 18488.80081507624
    assert_almost_equal(exp_baseload, loads_.base, decimal=4)
    assert_almost_equal(exp_heating, loads_.heating, decimal=4)
    assert_almost_equal(exp_cooling, loads_.cooling, decimal=4)

    # Test ILoad in `changepointmodel.core.pmodels.base`
    ILoad_heating_test = TestLoadInstance._heating(
        X=est.X.squeeze(),
        pred_y=est.pred_y,
        slope=est.coeffs[1],
        yint=est.coeffs[0],
        changepoint=est.coeffs[2],
    )
    ILoad_cooling_test = TestLoadInstance._cooling(
        X=est.X.squeeze(),
        pred_y=est.pred_y,
        slope=est.coeffs[1],
        yint=est.coeffs[0],
        changepoint=est.coeffs[2],
    )
    ILoad_base_test = TestLoadInstance._base(
        est.total_pred_y(), ILoad_heating_test, ILoad_cooling_test
    )
    assert_almost_equal(
        exp_cooling,
        ILoad_cooling_test,
        decimal=4,
    )
    assert_almost_equal(exp_heating, ILoad_heating_test, decimal=4)
    assert_almost_equal(exp_baseload, ILoad_base_test, decimal=4)
    est.r2()
    est.cvrmse()

    # tstat
    left_tstat, right_tstat = est.tstat()
    assert left_tstat is None
    assert right_tstat

    # dpop
    heatnum, coolnum = est.dpop()
    assert coolnum != 0
    assert heatnum == 0

    assert est.shape()


def test_3ph(generated_three_ph_data_daily_pre, TestLoadInstance):
    Xdata = np.array(generated_three_ph_data_daily_pre["X"])
    ydata = np.array(generated_three_ph_data_daily_pre["y"])
    sensor_reading_timestamps_data = np.array(generated_three_ph_data_daily_pre["Date"])

    parameter_model = MandVParameterModelFunction(
        name="3PH",
        f=ChangepointModelModels.threeph,
        bounds=default_bounds.threeph,
        parameter_model=ThreeParameterHeatingModel(),
        coefficients_parser=ChangepointModelCoeffsParsers.ThreeParameterCoefficientsParser(),
    )
    est = MandVModelingEstimator.MandVEnergyChangepointEstimator(model=parameter_model)
    data_model = MandVModelingSchemas.MandVDataModel(
        X=Xdata, y=ydata, sensor_reading_timestamps=sensor_reading_timestamps_data
    )

    est.original_ordering = data_model.order
    est.fit(data_model)

    # coeffs
    exp_yint = 1505.66686014
    exp_slopes = -20.59891671
    exp_cp = 50.931087
    assert_almost_equal(exp_yint, est.coeffs[0], decimal=4)
    assert_almost_equal(exp_slopes, est.coeffs[1], decimal=4)
    assert_almost_equal(exp_cp, est.coeffs[2], decimal=4)

    # loads
    loads_ = est.load()
    exp_baseload = 549568.4039501161
    exp_heating = 36400.73850706202
    exp_cooling = 0
    assert_almost_equal(exp_baseload, loads_.base, decimal=4)
    assert_almost_equal(exp_heating, loads_.heating, decimal=4)
    assert_almost_equal(exp_cooling, loads_.cooling, decimal=4)

    # Test ILoad in `changepointmodel.core.pmodels.base`
    ILoad_heating_test = TestLoadInstance._heating(
        X=est.X.squeeze(),
        pred_y=est.pred_y,
        slope=est.coeffs[1],
        yint=est.coeffs[0],
        changepoint=est.coeffs[2],
    )
    ILoad_cooling_test = TestLoadInstance._cooling(
        X=est.X.squeeze(),
        pred_y=est.pred_y,
        slope=est.coeffs[1],
        yint=est.coeffs[0],
        changepoint=est.coeffs[2],
    )
    ILoad_base_test = TestLoadInstance._base(
        est.total_pred_y(), ILoad_heating_test, ILoad_cooling_test
    )
    assert_almost_equal(
        exp_cooling,
        ILoad_cooling_test,
        decimal=4,
    )
    assert_almost_equal(exp_heating, ILoad_heating_test, decimal=4)
    assert_almost_equal(exp_baseload, ILoad_base_test, decimal=4)

    est.r2()
    est.cvrmse()

    # tstat
    left_tstat, right_tstat = est.tstat()
    assert left_tstat
    assert right_tstat is None

    # dpop
    heatnum, coolnum = est.dpop()
    exp_heatnum = len([i for i in Xdata if i <= exp_cp])
    assert coolnum == 0
    assert heatnum == exp_heatnum

    assert est.shape()


def test_4p(generated_four_p_data_daily_pre, TestLoadInstance):
    Xdata = np.array(generated_four_p_data_daily_pre["X"])
    ydata = np.array(generated_four_p_data_daily_pre["y"])
    sensor_reading_timestamps_data = np.array(generated_four_p_data_daily_pre["Date"])

    parameter_model = MandVParameterModelFunction(
        name="4P",
        f=ChangepointModelModels.fourp,
        bounds=default_bounds.fourp,
        parameter_model=FourParameterModel(),
        coefficients_parser=ChangepointModelCoeffsParsers.FourParameterCoefficientsParser(),
    )
    est = MandVModelingEstimator.MandVEnergyChangepointEstimator(model=parameter_model)
    data_model = MandVModelingSchemas.MandVDataModel(
        X=Xdata, y=ydata, sensor_reading_timestamps=sensor_reading_timestamps_data
    )

    est.original_ordering = data_model.order
    est.fit(data_model)

    # coeffs
    exp_yint = 1506.80068483
    exp_left_slopes = -20.4696408
    exp_right_slopes = 10.31603643
    exp_cp = 50.99586658
    assert_almost_equal(exp_yint, est.coeffs[0], decimal=4)
    assert_almost_equal(exp_left_slopes, est.coeffs[1], decimal=4)
    assert_almost_equal(exp_right_slopes, est.coeffs[2], decimal=4)
    assert_almost_equal(exp_cp, est.coeffs[3], decimal=4)

    # loads
    loads_ = est.load()
    exp_baseload = 549982.2499645344
    exp_heating = 36306.344611125096
    exp_cooling = 35334.97635568402
    assert_almost_equal(exp_baseload, loads_.base, decimal=4)
    assert_almost_equal(exp_heating, loads_.heating, decimal=4)
    assert_almost_equal(exp_cooling, loads_.cooling, decimal=4)

    # Test ILoad in `changepointmodel.core.pmodels.base` The heating would use the first slope, while the cooling uses
    # the 2nd slope.
    ILoad_heating_test = TestLoadInstance._heating(
        X=est.X.squeeze(),
        pred_y=est.pred_y,
        slope=est.coeffs[1],
        yint=est.coeffs[0],
        changepoint=est.coeffs[3],
    )
    ILoad_cooling_test = TestLoadInstance._cooling(
        X=est.X.squeeze(),
        pred_y=est.pred_y,
        slope=est.coeffs[2],
        yint=est.coeffs[0],
        changepoint=est.coeffs[3],
    )
    ILoad_base_test = TestLoadInstance._base(
        est.total_pred_y(), ILoad_heating_test, ILoad_cooling_test
    )
    assert_almost_equal(
        exp_cooling,
        ILoad_cooling_test,
        decimal=4,
    )
    assert_almost_equal(exp_heating, ILoad_heating_test, decimal=4)
    assert_almost_equal(exp_baseload, ILoad_base_test, decimal=4)

    est.r2()
    est.cvrmse()

    # tstat
    left_tstat, right_tstat = est.tstat()
    assert left_tstat
    assert right_tstat

    # dpop
    heatnum, coolnum = est.dpop()
    exp_heat = len([i for i in Xdata if i <= exp_cp])
    exp_cool = len([i for i in Xdata if i > exp_cp])
    assert heatnum == exp_heat
    assert coolnum == exp_cool

    print(est.shape())

    # This assertion shows us that we do get a V-shape, which is
    # what we want, but the absolute value of the left slope
    # is greater than the absolute value of the right slope
    assert est.shape()  # abs(left slope) < abs(right slope)


def test_5p(generated_five_p_data_daily_pre, TestLoadInstance):
    Xdata = np.array(generated_five_p_data_daily_pre["X"])
    ydata = np.array(generated_five_p_data_daily_pre["y"])
    sensor_reading_timestamps_data = np.array(generated_five_p_data_daily_pre["Date"])

    parameter_model = MandVParameterModelFunction(
        name="5P",
        f=ChangepointModelModels.fivep,
        bounds=default_bounds.fivep,
        parameter_model=FiveParameterModel(),
        coefficients_parser=ChangepointModelCoeffsParsers.FiveParameterCoefficientsParser(),
    )
    est = MandVModelingEstimator.MandVEnergyChangepointEstimator(model=parameter_model)
    data_model = MandVModelingSchemas.MandVDataModel(
        X=Xdata, y=ydata, sensor_reading_timestamps=sensor_reading_timestamps_data
    )

    est.original_ordering = data_model.order
    est.fit(data_model)

    # coeffs
    exp_yint = 1525.75358228
    exp_left_slopes = -23.78444068
    exp_right_slopes = 11.11553788
    exp_left_cp = 47.73128359
    exp_right_cp = 63.17090955
    assert_almost_equal(exp_yint, est.coeffs[0], decimal=4)
    assert_almost_equal(exp_left_slopes, est.coeffs[1], decimal=4)
    assert_almost_equal(exp_right_slopes, est.coeffs[2], decimal=4)
    assert_almost_equal(exp_left_cp, est.coeffs[3], decimal=4)
    assert_almost_equal(exp_right_cp, est.coeffs[4], decimal=4)

    # loads
    loads_ = est.load()
    exp_baseload = 556900.0575330999
    exp_heating = 30831.335706931568
    exp_cooling = 14683.883437896407
    assert_almost_equal(exp_baseload, loads_.base, decimal=4)
    assert_almost_equal(exp_heating, loads_.heating, decimal=4)
    assert_almost_equal(exp_cooling, loads_.cooling, decimal=4)

    # Test ILoad in `changepointmodel.core.pmodels.base` The heating would use the first slope, while the cooling uses
    # the 2nd slope.
    ILoad_heating_test = TestLoadInstance._heating(
        X=est.X.squeeze(),
        pred_y=est.pred_y,
        slope=est.coeffs[1],
        yint=est.coeffs[0],
        changepoint=est.coeffs[3],
    )
    ILoad_cooling_test = TestLoadInstance._cooling(
        X=est.X.squeeze(),
        pred_y=est.pred_y,
        slope=est.coeffs[2],
        yint=est.coeffs[0],
        changepoint=est.coeffs[3],
    )
    ILoad_base_test = TestLoadInstance._base(
        est.total_pred_y(), ILoad_heating_test, ILoad_cooling_test
    )
    assert_almost_equal(
        exp_cooling,
        ILoad_cooling_test,
        decimal=4,
    )
    assert_almost_equal(exp_heating, ILoad_heating_test, decimal=4)
    assert_almost_equal(exp_baseload, ILoad_base_test, decimal=4)

    est.r2()
    est.cvrmse()

    # tstat
    left_tstat, right_tstat = est.tstat()
    assert left_tstat
    assert right_tstat

    # dpop
    heatnum, coolnum = est.dpop()
    exp_heat = len([i for i in Xdata if i <= exp_left_cp])
    exp_cool = len([i for i in Xdata if i > exp_right_cp])
    assert heatnum == exp_heat
    assert coolnum == exp_cool

    # This assertion shows us that we do get a U-shape, which is
    # what we want, but the absolute value of the left slope
    # is greater than the absolute value of the right slope
    assert est.shape()  #  left slope < right slope
