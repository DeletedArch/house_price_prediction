"""
Model Training & Evaluation Pipeline for House Price Prediction
Constructs a Scikit-Learn ColumnTransformer Pipeline and trains a LinearRegression baseline model.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Add local path for data_cleaner import
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from data_cleaner import clean_house_prices_dataset

CSV_PATH = BASE_DIR / "data" / "house_prices.csv"
MODEL_EXPORT_PATH = BASE_DIR / "house_price.pkl"
LOCATIONS_EXPORT_PATH = BASE_DIR / "locations.json"
BACKEND_MODEL_PATH = BASE_DIR.parent / "backend" / "models" / "house_price.pkl"


def build_preprocessor() -> ColumnTransformer:
    """
    Constructs ColumnTransformer preprocessing numerical and categorical features.
    Bundles imputation, scaling, and one-hot encoding inside the pipeline.
    """
    numeric_features = ["carpet_area_sqft", "floor_num", "bathroom", "balcony"]
    categorical_features = [
        "location_grouped",
        "Furnishing",
        "Transaction",
        "Ownership",
        "facing",
    ]

    num_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])

    cat_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, numeric_features),
            ("cat", cat_pipeline, categorical_features),
        ],
        remainder="drop",
    )
    return preprocessor


def build_linear_regression_pipeline(use_log_target: bool = True) -> Pipeline:
    """
    Builds an end-to-end scikit-learn Pipeline with Linear Regression.
    Optionally applies log1p transform on target price to handle heavy skewness.
    """
    preprocessor = build_preprocessor()
    regressor = LinearRegression()

    if use_log_target:
        # Wrap regressor to train on np.log1p(y) and invert with np.expm1
        reg_model = TransformedTargetRegressor(
            regressor=regressor,
            func=np.log1p,
            inverse_func=np.expm1,
        )
    else:
        reg_model = regressor

    full_pipeline = Pipeline([
        ("prep", preprocessor),
        ("reg", reg_model),
    ])
    return full_pipeline


def train_and_evaluate(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[Pipeline, Dict[str, float], pd.DataFrame]:
    """
    Splits data, fits Linear Regression pipeline, and computes test metrics.
    """
    feature_cols = [
        "carpet_area_sqft", "floor_num", "bathroom", "balcony",
        "location_grouped", "Furnishing", "Transaction", "Ownership", "facing"
    ]
    X = df[feature_cols]
    y = df["price_clean"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    print(f"Training samples: {len(X_train):,}, Test samples: {len(X_test):,}")

    # Build and train Linear Regression pipeline
    pipeline = build_linear_regression_pipeline(use_log_target=True)
    pipeline.fit(X_train, y_train)

    # Evaluate on test set
    y_pred = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    metrics = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
    }

    print("\n--- Test Set Evaluation Metrics (Linear Regression Baseline) ---")
    print(f"MAE  : ₹ {mae:,.2f} (₹ {mae/1e5:.2f} Lac)")
    print(f"RMSE : ₹ {rmse:,.2f} (₹ {rmse/1e5:.2f} Lac)")
    print(f"R²   : {r2:.4f}")

    results_df = pd.DataFrame({
        "Actual_Price": y_test,
        "Predicted_Price": y_pred,
        "Error": y_test - y_pred,
    })

    return pipeline, metrics, results_df


def run_training_pipeline():
    print("=" * 65)
    print("  House Price Prediction — Linear Regression Training Pipeline")
    print("=" * 65)

    if not CSV_PATH.exists():
        print(f"❌ Dataset not found at {CSV_PATH}. Running downloader...")
        import subprocess
        subprocess.run([sys.executable, str(BASE_DIR / "download_dataset.py")], check=False)

    df_raw = pd.read_csv(CSV_PATH, low_memory=False)
    print(f"Loaded raw dataset: {len(df_raw):,} rows.")

    df_clean, allowed_locations = clean_house_prices_dataset(df_raw, top_n_locations=50)
    print(f"Cleaned dataset: {len(df_clean):,} rows remaining after outlier filter.")

    pipeline, metrics, _ = train_and_evaluate(df_clean)

    # Export artifacts
    print("\n📦 Exporting Pipeline Artifacts...")
    joblib.dump(pipeline, MODEL_EXPORT_PATH)
    print(f" Saved trained model to: {MODEL_EXPORT_PATH}")

    with open(LOCATIONS_EXPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(allowed_locations, f, indent=2)
    print(f" Saved locations to: {LOCATIONS_EXPORT_PATH}")

    # Also sync to backend
    if BACKEND_MODEL_PATH.parent.exists():
        joblib.dump(pipeline, BACKEND_MODEL_PATH)
        print(f" Synced model to backend: {BACKEND_MODEL_PATH}")

    print("\n✅ Linear Regression pipeline trained and exported successfully.")
    return pipeline, metrics


if __name__ == "__main__":
    run_training_pipeline()
