import pandas as pd
import pytest
from src.penguin_classifier.dataset import clean_data
from src.penguin_classifier.modeling.predict import (
    predict_single_penguin_proba,
)
from sklearn.pipeline import Pipeline
from src.penguin_classifier.modeling.train import build_pipeline

from dash import html
import dash_bootstrap_components as dbc
from src.penguin_classifier.ui.layout import create_layout


# --- Fixtures ---

@pytest.fixture
def raw_data_sample():
    data = {
        "species": ["Adelie", "Gentoo", "Adelie", pd.NA],
        "island": ["Torgersen", "Biscoe", "Dream", "Torgersen"],
        "bill_length_mm": [39.1, 50.0, pd.NA, 40.0],
        "bill_depth_mm": [18.7, 15.0, 18.0, 19.0],
        "flipper_length_mm": [181.0, 220.0, 190.0, 195.0],
        "body_mass_g": [3750.0, 5000.0, 3800.0, 4000.0],
        "sex": ["male", "female", "male", "female"],
        "year": [2007, 2008, 2009, 2007],
    }
    return pd.DataFrame(data)


@pytest.fixture
def valid_penguin_features():
    data = {
        "island": ["Torgersen"],
        "bill_length_mm": [39.1],
        "bill_depth_mm": [18.7],
        "flipper_length_mm": [181.0],
        "body_mass_g": [3750.0],
        "sex": ["male"],
    }
    return pd.DataFrame(data)


# -- Tests --

def test_clean_data_removes_nans(raw_data_sample):
    cleaned_df = clean_data(raw_data_sample)
    assert len(cleaned_df) == 2, "clean_data should remove rows with NaNs"


def test_clean_data_removes_year_column(raw_data_sample):
    cleaned_df = clean_data(raw_data_sample)
    assert "year" not in cleaned_df.columns, "column 'year' should be removed"


def test_prediction_returns_valid_format(valid_penguin_features):
    species, proba = predict_single_penguin_proba(valid_penguin_features)

    assert isinstance(species, str), "prediction must be a string"
    assert species in ["Adelie", "Chinstrap", "Gentoo"], (
        "invalid penguin species"
    )

    assert isinstance(proba, float), "probability must be a float"
    assert 0 <= proba <= 1.0, "probability must be between 0 and 1"


def test_pipeline_construction():
    """Checks if the training pipeline can be built successfully."""
    pipeline = build_pipeline()
    assert isinstance(pipeline, Pipeline), "build_pipeline should return a sklearn Pipeline"
    # Check if steps exist (preprocessor and classifier)
    step_names = [step[0] for step in pipeline.steps]
    assert "preprocessor" in step_names
    assert "classifier" in step_names



def test_layout_creation():
    """Checks if the layout is created without errors and returns a Container."""
    layout = create_layout()

    # Check if it returns the main wrapper component (Container)
    assert isinstance(layout, dbc.Container), (
        "Layout must be a Bootstrap Container"
    )
