import pytest
from mandvmodeling.core import schemas
from . import GENERATED_DATA_ALL_MODELS_FILE
import json

def _parse_generated_mode_data(data, model_type):
    for i in data:
        if i["model_type"] == model_type:
            return i

@pytest.fixture
def generated_data_all_models():
    with open(GENERATED_DATA_ALL_MODELS_FILE, "r") as f:
        return json.load(f)

@pytest.fixture
def generated_3pc_data(generated_data_all_models):
    return _parse_generated_mode_data(generated_data_all_models, "3PC")
