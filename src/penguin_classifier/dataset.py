from pathlib import Path

from loguru import logger
from palmerpenguins import load_penguins
import pandas as pd

from penguin_classifier.config import NUMERICAL_FEATURES, RAW_DATA_PATH


def fetch_and_save_raw_data() -> None:
    """Fetches the raw penguins dataset and saves it to RAW_DATA_PATH."""
    if RAW_DATA_PATH.exists():
        logger.info(
            f"Raw data already exists at {RAW_DATA_PATH}, skipping fetch."
        )
        return None

    raw_data = load_penguins()
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    raw_data.to_csv(RAW_DATA_PATH, index=False)
    logger.info(f"Raw data saved to {RAW_DATA_PATH}")
    return None


def load_data(filepath: Path) -> pd.DataFrame:
    """Loads data from a CSV file into a pandas DataFrame."""
    try:
        data = pd.read_csv(filepath)
        logger.info(f"Data loaded from {filepath}")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"No data found at {filepath}") from None


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans the penguins dataset by handling missing values."""
    df = df.dropna(subset=NUMERICAL_FEATURES + ["species"], axis="rows")
    logger.success("Data cleaned.")
    return df.drop(
        columns=["year"],
    )


def split_feature_from_target(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """Splits a dataset into features and target."""
    target = df["species"]
    features = df.drop("species", axis=1)
    logger.success("Data split into features and target.")
    return features, target


if __name__ == "__main__":
    df = load_data(RAW_DATA_PATH)
    cleaned_df = clean_data(df)
    print(cleaned_df.columns)
