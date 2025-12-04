from pathlib import Path

from loguru import logger
from palmerpenguins import load_penguins, load_penguins_raw
import pandas as pd
import typer

from penguin_classifier.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    # ----------------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Processing dataset...")
    raw_data = load_penguins()
    raw_data_raw = load_penguins_raw()
    raw_data_path = RAW_DATA_DIR / "data.csv"
    raw_data_path_raw = RAW_DATA_DIR / "data_raw.csv"
    raw_data.to_csv(raw_data_path)
    raw_data_raw.to_csv(raw_data_path_raw)

    logger.success("Writing dataset complete")
    # -----------------------------------------


if __name__ == "__main__":
    app()
