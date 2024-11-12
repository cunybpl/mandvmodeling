import pytest
import os
import glob
import json
from . import (
    GENERATED_DATA_ALL_MODELS_DAILY_PRE_FOLDER,
    GENERATED_DATA_ALL_MODELS_DAILY_POST_FOLDER,
)
from changepointmodel.core.nptypes import OneDimNDArray
from changepointmodel.core.pmodels import base as ChangepointModelBase
import numpy as np


@pytest.fixture
def generated_data_all_models_daily_pre():
    contents = []
    json_pattern = os.path.join(GENERATED_DATA_ALL_MODELS_DAILY_PRE_FOLDER, "*.json")
    file_list = glob.glob(json_pattern)
    for file_path in file_list:
        model_type_str = os.path.splitext(os.path.basename(file_path))[0]
        with open(file_path, "r") as f:
            contents.append({"model_type": model_type_str} | json.load(f))
    return contents


@pytest.fixture
def generated_data_all_model_daily_post():
    contents = []
    json_pattern = os.path.join(GENERATED_DATA_ALL_MODELS_DAILY_POST_FOLDER, "*.json")
    file_list = glob.glob(json_pattern)
    for file_path in file_list:
        model_type_str = os.path.splitext(os.path.basename(file_path))[0]
        with open(file_path, "r") as f:
            contents.append({"model_type": model_type_str} | json.load(f))
    return contents
    ...


def _parse_generated_mode_data(data, model_type):
    for i in data:
        if i["model_type"] == model_type:
            return i


@pytest.fixture
def generated_2p_data_daily_pre(generated_data_all_models_daily_pre):
    return _parse_generated_mode_data(
        generated_data_all_models_daily_pre, "positive_slope_two_p"
    )


@pytest.fixture
def generated_three_pc_data_daily_pre(generated_data_all_models_daily_pre):
    return _parse_generated_mode_data(generated_data_all_models_daily_pre, "three_pc")


@pytest.fixture
def generated_three_ph_data_daily_pre(generated_data_all_models_daily_pre):
    return _parse_generated_mode_data(generated_data_all_models_daily_pre, "three_ph")


@pytest.fixture
def generated_four_p_data_daily_pre(generated_data_all_models_daily_pre):
    return _parse_generated_mode_data(generated_data_all_models_daily_pre, "four_p")


@pytest.fixture
def generated_five_p_data_daily_pre(generated_data_all_models_daily_pre):
    return _parse_generated_mode_data(generated_data_all_models_daily_pre, "five_p")


@pytest.fixture
def TestLoadInstance():
    class TestLoad(ChangepointModelBase.ILoad):
        def load(
            self,
            X: OneDimNDArray[np.float64],
            pred_y: OneDimNDArray[np.float64],
            coeffs: ChangepointModelBase.EnergyParameterModelCoefficients,
        ) -> ChangepointModelBase.Load:  # pragma: no cover
            pass

    return TestLoad()
