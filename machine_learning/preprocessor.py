"""
Data Preprocessing Module
Cleans data, encodes labels, performs 80/20 stratified train/test split, fits standard scaler, and supports dynamic feature exclusion.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler
import joblib
from typing import Tuple, List, Dict, Any

class DataPreprocessor:
    def __init__(self, target_col: str = "TimingViolation", test_size: float = 0.2, random_state: int = 42):
        self.target_col = target_col
        self.test_size = test_size
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.feature_names: List[str] = []

    def preprocess(self, df: pd.DataFrame, exclude_features: List[str] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[str]]:
        """
        Preprocesses dataframe into X_train, X_test, y_train, y_test arrays and feature name list.
        Allows excluding unwanted features dynamically.
        """
        df_clean = df.copy()

        # Always drop non-feature metadata and target-leakage columns if present
        default_drops = ["Design Name", "WNS", "mode", "Mode"]
        for col in default_drops:
            if col in df_clean.columns:
                df_clean = df_clean.drop(columns=[col])

        # Exclude user-specified unwanted features
        if exclude_features:
            for feat in exclude_features:
                if feat in df_clean.columns and feat != self.target_col:
                    df_clean = df_clean.drop(columns=[feat])

        # Target label encoding: YES -> 1, NO -> 0
        if df_clean[self.target_col].dtype == object:
            y = df_clean[self.target_col].map({"YES": 1, "NO": 0}).values
        else:
            y = df_clean[self.target_col].values

        X_df = df_clean.drop(columns=[self.target_col])
        self.feature_names = list(X_df.columns)
        X = X_df.values

        # 80% Train, 20% Test Stratified Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )

        # Scale numerical features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        return X_train_scaled, X_test_scaled, y_train, y_test, self.feature_names

    def get_cv_folds(self, n_splits: int = 5) -> StratifiedKFold:
        return StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=self.random_state)

    def save_scaler(self, filepath: str):
        joblib.dump(self.scaler, filepath)

    def load_scaler(self, filepath: str):
        self.scaler = joblib.load(filepath)
