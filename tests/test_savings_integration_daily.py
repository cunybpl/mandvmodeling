import numpy as np
import pytest
from mandvmodeling.core import estimator as MandVModelingEstimator
from mandvmodeling.core.schemas import MandVDataModel
from mandvmodeling.core.pmodels import MandVParameterModelFunction
from mandvmodeling.core.calc.bounds import default_bounds

from changepointmodel.core.pmodels import coeffs_parser as ChangepointModelCoeffsParsers
from changepointmodel.core.calc import models as ChangepointModelModels
from changepointmodel.core.pmodels.parameter_model import (
    ThreeParameterCoolingModel,
    FourParameterModel
)
from changepointmodel.core import savings

def test_savings_integration_with_pre_and_post(
    generated_three_pc_data_daily_pre, generated_three_pc_data_daily_post
):
    Xdata = np.array(generated_three_pc_data_daily_pre["X"])
    ydata = np.array(generated_three_pc_data_daily_pre["y"])
    sensor_reading_timestamps = np.array(generated_three_pc_data_daily_pre["Date"])


    Xdata_post = np.array(generated_three_pc_data_daily_post["X"])
    ydata_post = np.array(generated_three_pc_data_daily_post["y"])
    sensor_reading_timestamps_post = np.array(generated_three_pc_data_daily_post["Date"])

    input_data_model = MandVDataModel(X=Xdata, y=ydata, sensor_reading_timestamps=sensor_reading_timestamps)
    input_data_model_post = MandVDataModel(X=Xdata_post, y=ydata_post,sensor_reading_timestamps=sensor_reading_timestamps_post)

    threepc = MandVParameterModelFunction(
        name="3PC",
        f=ChangepointModelModels.threepc,
        bounds=default_bounds.threepc,
        parameter_model=ThreeParameterCoolingModel(),
        coefficients_parser=ChangepointModelCoeffsParsers.ThreeParameterCoefficientsParser(),
    )
    estimator_pre = MandVModelingEstimator.MandVEnergyChangepointEstimator(model=threepc)
    estimator_post = MandVModelingEstimator.MandVEnergyChangepointEstimator(model=threepc)

    fitted_est_pre = estimator_pre.fit(input_data_model)
    fitted_est_post = estimator_post.fit(input_data_model_post)

    adjusted_saving = savings.AshraeAdjustedSavingsCalculator()
    adj_result = adjusted_saving.save(fitted_est_pre, fitted_est_post)

    norms = np.array([i + 1 for i in Xdata])
    normalized_saving = savings.AshraeNormalizedSavingsCalculator(norms.reshape(-1, 1))
    norm_result = normalized_saving.save(fitted_est_pre, fitted_est_post)
    
    # adujusted savings
    assert adj_result.total_savings
    assert adj_result.average_savings
    assert adj_result.percent_savings
    assert adj_result.percent_savings_uncertainty

    # normalized savings
    assert norm_result.total_savings
    assert norm_result.average_savings
    assert norm_result.percent_savings
    assert norm_result.percent_savings_uncertainty

    # saving check
    assert pytest.approx(adj_result.total_savings, 1e-4) == 55057.57270323712
    assert pytest.approx(norm_result.total_savings, 1e-4) == 55136.79695103428
