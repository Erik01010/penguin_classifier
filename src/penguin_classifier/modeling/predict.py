import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from src.penguin_classifier.config import MODEL_PATH


def _load_pipeline(path: str) -> Pipeline:
    """Load trained model pipeline from disk."""
    return joblib.load(path)


def predict_batch_species(
    features: pd.DataFrame, pipeline: Pipeline
) -> list[str]:
    """Predicts the species for multiple observations."""

    return pipeline.predict(X=features)


def predict_single_penguin_proba(
    features: pd.DataFrame, pipeline: Pipeline
) -> tuple[str, float]:
    """Predicts species and confidence for a single penguin observation."""

    predicted_species = pipeline.predict(X=features)[0]

    all_probabilities = pipeline.predict_proba(X=features)
    max_confidence = np.max(all_probabilities).round(4)

    return predicted_species, max_confidence


if __name__ == "__main__":
    from src.penguin_classifier.dataset import (
        RAW_DATA_PATH,
        clean_data,
        load_data,
    )

    df = load_data(RAW_DATA_PATH)
    cleaned_df = clean_data(df)
    pipeline = _load_pipeline(MODEL_PATH)
    species, proba = predict_single_penguin_proba(
        features=cleaned_df.iloc[[0]], pipeline=pipeline
    )
    print(f"Species: {species}, Probability: {proba}")
