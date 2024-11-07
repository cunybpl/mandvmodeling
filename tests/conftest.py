import pytest
import os
import glob
import json
from . import (
    GENERATED_DATA_ALL_MODELS_DAILY_PRE_FOLDER,
    GENERATED_DATA_ALL_MODELS_DAILY_POST_FOLDER,
)


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
def generated_2p_data_pre(generated_data_all_models_daily_pre):
    return _parse_generated_mode_data(
        generated_data_all_models_daily_pre, "positive_slope_two_p"
    )
