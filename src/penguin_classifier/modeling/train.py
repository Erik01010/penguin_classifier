import joblib
import json
from loguru import logger
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from penguin_classifier.config import (
    MODEL_PATH,
    RAW_DATA_PATH,
    METRICS_PATH,
)
from src.penguin_classifier.config import RANDOM_SEED, TEST_SPLIT_SIZE
from src.penguin_classifier.dataset import (
    clean_data,
    load_data,
    split_feature_from_target,
)
from src.penguin_classifier.features import build_preprocessor


def build_pipeline() -> Pipeline:
    preprocessor = build_preprocessor()
    classifier = LogisticRegression(random_state=RANDOM_SEED)

    pipeline = Pipeline(
        steps=[("preprocessor", preprocessor), ("classifier", classifier)]
    )
    logger.success("Pipeline built.")
    return pipeline


def train_model():
    df_raw = load_data(filepath=RAW_DATA_PATH)
    df_cleaned = clean_data(df=df_raw)
    X, y = split_feature_from_target(df=df_cleaned)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SPLIT_SIZE, random_state=RANDOM_SEED
    )

    pipeline = build_pipeline()
    pipeline.fit(X=X_train, y=y_train)
    logger.success("Pipeline trained.")

    preds = pipeline.predict(X_test)
    logger.success("Pipeline predicted on test set.")

    report_dict = classification_report(y_true=y_test, y_pred=preds, output_dict=True)
    print(classification_report(y_true=y_test, y_pred=preds))

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_PATH, "w") as f:
        json.dump(report_dict, f)
    logger.success(f"Metrics saved to {METRICS_PATH}")

    joblib.dump(pipeline, MODEL_PATH)


if __name__ == "__main__":
    train_model()
