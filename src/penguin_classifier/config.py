from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJ_ROOT / "src"
DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "data.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "prediction_history.csv"
MODEL_PATH = PROJ_ROOT / "models" / "pipeline.joblib"
REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
METRICS_PATH = REPORTS_DIR / "metrics.json"

# Global constants
RANDOM_SEED = 42
TEST_SPLIT_SIZE = 0.2

# Mapping for csv-saving
CSV_HEADER = [
    "species",
    "island",
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
    "sex",
]

# Features for model training
NUMERICAL_FEATURES = [
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
]

CATEGORICAL_FEATURES = ["island", "sex"]

FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES


# Validation constraints for numerical features
FEATURE_CONSTRAINTS = {
    "bill_length_mm": {"min": 25.0, "max": 65.0, "default": 40.0},
    "bill_depth_mm": {"min": 10.0, "max": 25.0, "default": 20.0},
    "flipper_length_mm": {"min": 150.0, "max": 250.0, "default": 200.0},
    "body_mass_g": {"min": 2000.0, "max": 7500.0, "default": 4000.0},
}


# Mapping for dropdown options
ISLAND_OPTIONS: list[dict] = [
    {
        "label": "Torgersen",
        "value": "Torgersen",
    },
    {
        "label": "Biscoe",
        "value": "Biscoe",
    },
    {
        "label": "Dream",
        "value": "Dream",
    },
]
SEX_OPTIONS: list[dict] = [
    {
        "label": "male",
        "value": "male",
    },
    {
        "label": "female",
        "value": "female",
    },
]

OFFSET = "mb-3"
