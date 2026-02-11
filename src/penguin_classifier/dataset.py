from pathlib import Path

from loguru import logger
import pandas as pd

from penguin_classifier.config import (
    CSV_HEADER,
    NUMERICAL_FEATURES,
    PROCESSED_DATA_PATH,
    RAW_DATA_PATH,
)


def fetch_and_save_raw_data() -> None:
    """Fetches the raw penguins dataset and saves it to RAW_DATA_PATH."""
    if RAW_DATA_PATH.exists():
        logger.info(
            f"Raw data already exists at {RAW_DATA_PATH}, skipping fetch."
        )
        return None

    from palmerpenguins import load_penguins

    raw_data = load_penguins()
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    raw_data.to_csv(RAW_DATA_PATH, index=False)
    logger.info(f"Raw data saved to {RAW_DATA_PATH}")
    return None


def load_data(filepath: Path) -> pd.DataFrame:
    """Loads data from a CSV file into a pandas DataFrame."""
    try:
        data = pd.read_csv(filepath)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"No data found at {filepath}") from None


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans the penguins dataset by handling missing values."""
    df = df.dropna(subset=NUMERICAL_FEATURES + ["species"], axis="rows")
    return df.drop(
        columns=["year"],
    )


def split_feature_from_target(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """Splits a dataset into features and target."""
    target = df["species"]
    features = df.drop("species", axis=1)
    logger.success("Data split into features and target.")
    return features, target


def save_prediction(new_data: pd.DataFrame = None):
    """Appends new data to the CSV file."""
    file_exists = Path(PROCESSED_DATA_PATH).exists()

    new_data_ordered = new_data[CSV_HEADER]
    new_data_ordered.to_csv(
        PROCESSED_DATA_PATH, mode="a", header=not file_exists, index=False
    )


def load_combined_data():
    """Loads datasets and concatenates if history is not empty."""
    raw_data = load_data(RAW_DATA_PATH)
    cleaned_data = clean_data(raw_data)
    if not PROCESSED_DATA_PATH.exists():
        return cleaned_data.iloc[::-1]

    prediction_history = load_data(PROCESSED_DATA_PATH)
    if prediction_history.notna().any().any():
        updated_data = pd.concat(
            [cleaned_data, prediction_history], axis="rows"
        )
        return updated_data.iloc[::-1]

    return cleaned_data.iloc[::-1]


if __name__ == "__main__":
    pass
