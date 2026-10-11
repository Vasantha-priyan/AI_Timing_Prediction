"""
Explainable AI (XAI) Module
Calculates SHAP values, Permutation Importance, and generates human-readable VLSI explanations.
"""

import os
import sys
import logging
import numpy as np
import pandas as pd
import shap
from sklearn.inspection import permutation_importance
from typing import Dict, Any, List, Tuple

logger = logging.getLogger("ExplainableAI")

class ExplainableAI:
    def __init__(self, model: Any, feature_names: List[str]):
        self.model = model
        self.feature_names = feature_names

    def compute_shap_values(self, X_sample: np.ndarray) -> Tuple[Any, shap.Explainer]:
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer(X_sample)
        return shap_values, explainer

    def compute_permutation_importance(self, X_val: np.ndarray, y_val: np.ndarray, n_repeats: int = 10) -> pd.DataFrame:
        result = permutation_importance(self.model, X_val, y_val, n_repeats=n_repeats, random_state=42)
        perm_df = pd.DataFrame({
            "Feature": self.feature_names,
            "Importance_Mean": result.importances_mean,
            "Importance_Std": result.importances_std
        }).sort_values(by="Importance_Mean", ascending=False).reset_index(drop=True)
        return perm_df

    def explain_sample_prediction(self, sample_dict: Dict[str, Any], shap_values_single: np.ndarray) -> List[str]:
        explanations = []
        if hasattr(shap_values_single, "values"):
            vals = shap_values_single.values
        else:
            vals = shap_values_single

        if vals.ndim > 1:
            vals = vals[:, 1] if vals.shape[1] > 1 else vals[:, 0]

        top_indices = np.argsort(np.abs(vals))[::-1]
        explanations.append("Primary Physical Features Driving Prediction:")
        for idx in top_indices[:4]:
            feat = self.feature_names[idx]
            val = sample_dict.get(feat, "N/A")
            shap_impact = vals[idx]
            direction = "increases violation risk" if shap_impact > 0 else "reduces violation risk"
            explanations.append(f" • {feat} = {val}: SHAP impact {shap_impact:+.4f} ({direction})")

        return explanations
