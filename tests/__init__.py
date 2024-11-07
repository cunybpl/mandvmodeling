import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES_DIR = os.path.abspath(os.path.join(ROOT_DIR, "tests", "fixtures"))

# Monthly data
GENERATED_DATA_ALL_MODELS_MONTHLY_FILE = os.path.join(
    FIXTURES_DIR, "generated_data_all_models_monthly.json"
)

# Daily data
GENERATED_DATA_ALL_MODELS_DAILY_PRE_FOLDER = os.path.join(FIXTURES_DIR, "daily/pre")
GENERATED_DATA_ALL_MODELS_DAILY_POST_FOLDER = os.path.join(FIXTURES_DIR, "daily/post")
