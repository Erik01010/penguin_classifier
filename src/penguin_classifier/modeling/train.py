import json
import warnings

import joblib
from loguru import logger
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    train_test_split,
)
from sklearn.pipeline import Pipeline

from src.penguin_classifier.config import (
    METRICS_PATH,
    MODEL_PATH,
    RANDOM_SEED,
    RAW_DATA_PATH,
    TEST_SPLIT_SIZE,
)
from src.penguin_classifier.dataset import (
    clean_data,
    load_data,
    split_feature_from_target,
)
from src.penguin_classifier.features import build_preprocessor

warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources")


def build_pipeline() -> Pipeline:
    """Build the base pipeline with preprocessor and classifier."""
    preprocessor = build_preprocessor()
    classifier = LogisticRegression(random_state=RANDOM_SEED, max_iter=1000)

    pipeline = Pipeline(
        steps=[("preprocessor", preprocessor), ("classifier", classifier)]
    )
    logger.success("Base pipeline built.")
    return pipeline


def train_model():
    """Train the pipeline and save it."""
    df_raw = load_data(filepath=RAW_DATA_PATH)
    df_cleaned = clean_data(df=df_raw)
    X, y = split_feature_from_target(df=df_cleaned)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SPLIT_SIZE, random_state=RANDOM_SEED, stratify=y
    )

    pipeline = build_pipeline()

    param_grid = {
        "classifier__C": [0.1, 1.0, 10.0],
        "classifier__solver": ["lbfgs", "newton-cg"],
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)

    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=cv,
        scoring="accuracy",
        n_jobs=-1,
        verbose=1,
    )

    logger.info("Starting Grid Search with Cross Validation...")
    grid_search.fit(X_train, y_train)

    best_pipeline = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_cv_score = grid_search.best_score_

    logger.success(
        f"Best CV Accuracy: {best_cv_score:.2%} with params: {best_params}"
    )

    preds = best_pipeline.predict(X_test)
    logger.success("Pipeline predicted on test set.")

    report_dict = classification_report(
        y_true=y_test, y_pred=preds, output_dict=True
    )

    report_dict["cross_val_accuracy"] = round(best_cv_score, 2)

    print("\n" + classification_report(y_true=y_test, y_pred=preds))

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_PATH, "w") as f:
        json.dump(report_dict, f, indent=4)
    logger.success(f"Metrics saved to {METRICS_PATH}")

    joblib.dump(best_pipeline, MODEL_PATH)
    logger.success(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
