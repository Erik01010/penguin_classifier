import joblib
import pandas as pd
from train import train_model

from src.penguin_classifier.config import MODEL_PATH, RAW_DATA_PATH
from src.penguin_classifier.dataset import clean_data, load_data


def predict(features: pd.DataFrame) -> list[str]:
    """Predict with trained model."""
    try:
        pipeline = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        print("No joblib file found.")
        pipeline = train_model()

    return pipeline.predict(X=features)


def predict_proba(features: pd.DataFrame) -> pd.DataFrame:
    """Predict probabilities with trained model."""
    try:
        pipeline = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        print("No joblib file found.")
        pipeline = train_model()

    predictions = pipeline.predict_proba(X=features)
    predictions = predictions.round(4)
    return predictions


if __name__ == "__main__":
    df = load_data(RAW_DATA_PATH)
    cleaned_df = clean_data(df)
    preds = predict_proba(features=cleaned_df.loc[1:1, :])
    print(preds)
