from loguru import logger
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.penguin_classifier.config import (
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES,
)


def build_preprocessor() -> ColumnTransformer:
    """Build a ColumnTransformer preprocessor."""
    numerical_processor = StandardScaler()
    categorial_processor = OneHotEncoder(
        handle_unknown="ignore", sparse_output=False
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_processor, NUMERICAL_FEATURES),
            ("cat", categorial_processor, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )
    logger.success("Preprocessor built.")
    return preprocessor


if __name__ == "__main__":
    pass
