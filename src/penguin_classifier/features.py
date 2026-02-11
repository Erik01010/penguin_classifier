"""
Defines the feature engineering and preprocessing pipeline.
Converts raw categorical and numerical data into a format suitable for machine learning.
"""

from loguru import logger
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.penguin_classifier.config import (
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES,
)


def build_preprocessor() -> ColumnTransformer:
    """
    Creates a scikit-learn ColumnTransformer for automated feature scaling and encoding.

    Numerical features are scaled to zero mean and unit variance using StandardScaler.
    Categorical features are transformed into binary vectors using OneHotEncoder.

    Returns:
        ColumnTransformer: A configured preprocessor to be used in a model pipeline.
    """
    numerical_processor = StandardScaler()

    # Encoding categorical strings (e.g., Island names) into numeric format
    categorial_processor = OneHotEncoder(
        handle_unknown="ignore", sparse_output=False
    )

    # Combining both processors into a single transformer object
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_processor, NUMERICAL_FEATURES),
            ("cat", categorial_processor, CATEGORICAL_FEATURES),
        ],
        remainder="drop",  # Ensures only specified features are passed to the model
    )

    logger.success("Preprocessor built.")
    return preprocessor
