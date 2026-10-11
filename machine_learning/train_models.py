"""
Machine Learning Training Engine
Trains Random Forest, Decision Tree, and XGBoost models, compares performance metrics, selects best model, and saves binaries.
"""

import os
import sys
import time
import tracemalloc
import logging
import pandas as pd
import numpy as np
import joblib
import yaml
from typing import Dict, Any, Tuple, List

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
from sklearn.model_selection import cross_val_score

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from machine_learning.preprocessor import DataPreprocessor

logger = logging.getLogger("MLTrainer")

class MLTrainer:
    def __init__(self, base_dir: str = "."):
        self.base_dir = os.path.abspath(base_dir)
        self.config_path = os.path.join(self.base_dir, "config", "settings.yaml")
        self.models_dir = os.path.join(self.base_dir, "models")
        os.makedirs(self.models_dir, exist_ok=True)

        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f: self.config = yaml.safe_load(f)
        else:
            self.config = {}

        self.preprocessor = DataPreprocessor(
            test_size=self.config.get("dataset", {}).get("test_size", 0.2),
            random_state=self.config.get("dataset", {}).get("random_state", 42)
        )

    def train_and_evaluate(self, df: pd.DataFrame, exclude_features: List[str] = None) -> Tuple[Dict[str, Dict[str, Any]], str, pd.DataFrame]:
        logger.info("Preprocessing dataset...")
        X_train, X_test, y_train, y_test, feature_names = self.preprocessor.preprocess(df, exclude_features=exclude_features)
        self.preprocessor.save_scaler(os.path.join(self.models_dir, "scaler.pkl"))

        cv = self.preprocessor.get_cv_folds(n_splits=self.config.get("dataset", {}).get("cv_folds", 5))

        rf_cfg = self.config.get("models", {}).get("random_forest", {})
        dt_cfg = self.config.get("models", {}).get("decision_tree", {})
        xgb_cfg = self.config.get("models", {}).get("xgboost", {})

        models = {
            "Random Forest": RandomForestClassifier(
                n_estimators=rf_cfg.get("n_estimators", 100),
                criterion=rf_cfg.get("criterion", "gini"),
                random_state=rf_cfg.get("random_state", 42),
                class_weight=rf_cfg.get("class_weight", "balanced"),
                bootstrap=rf_cfg.get("bootstrap", True)
            ),
            "Decision Tree": DecisionTreeClassifier(
                criterion=dt_cfg.get("criterion", "gini"),
                random_state=dt_cfg.get("random_state", 42),
                class_weight=dt_cfg.get("class_weight", "balanced")
            ),
            "XGBoost": XGBClassifier(
                n_estimators=xgb_cfg.get("n_estimators", 100),
                learning_rate=xgb_cfg.get("learning_rate", 0.1),
                max_depth=xgb_cfg.get("max_depth", 6),
                random_state=xgb_cfg.get("random_state", 42),
                use_label_encoder=False,
                eval_metric="logloss"
            )
        }

        results = {}
        best_score = -1.0
        best_model_name = ""

        for name, model in models.items():
            logger.info(f"Training {name}...")
            tracemalloc.start()
            start_train = time.time()
            model.fit(X_train, y_train)
            train_time = time.time() - start_train

            start_pred = time.time()
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else y_pred
            pred_time = time.time() - start_pred

            current, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="accuracy")

            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, zero_division=0)
            rec = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            roc_auc = roc_auc_score(y_test, y_prob)
            cm = confusion_matrix(y_test, y_pred)
            report = classification_report(y_test, y_pred, output_dict=True)

            results[name] = {
                "model": model,
                "Accuracy": acc,
                "Precision": prec,
                "Recall": rec,
                "F1 Score": f1,
                "ROC-AUC": roc_auc,
                "CV Accuracy Mean": np.mean(cv_scores),
                "CV Accuracy Std": np.std(cv_scores),
                "Confusion Matrix": cm,
                "Classification Report": report,
                "Training Time (s)": train_time,
                "Prediction Time (s)": pred_time,
                "Peak Memory (MB)": peak_mem / (1024 * 1024),
                "y_test": y_test,
                "y_pred": y_pred,
                "y_prob": y_prob
            }

            filename = name.lower().replace(" ", "_") + ".pkl"
            joblib.dump(model, os.path.join(self.models_dir, filename))

            composite_score = f1 + roc_auc
            if composite_score > best_score:
                best_score = composite_score
                best_model_name = name

        logger.info(f"Selected best model architecture: {best_model_name}")
        best_model_obj = results[best_model_name]["model"]
        joblib.dump(best_model_obj, os.path.join(self.models_dir, "best_model.pkl"))

        summary_rows = []
        for name, mres in results.items():
            summary_rows.append({
                "Model": name,
                "Accuracy": mres["Accuracy"],
                "Precision": mres["Precision"],
                "Recall": mres["Recall"],
                "F1 Score": mres["F1 Score"],
                "ROC-AUC": mres["ROC-AUC"],
                "CV Accuracy": f"{mres['CV Accuracy Mean']:.4f} ± {mres['CV Accuracy Std']:.4f}",
                "Training Time (s)": mres["Training Time (s)"],
                "Prediction Time (s)": mres["Prediction Time (s)"],
                "Peak Memory (MB)": mres["Peak Memory (MB)"]
            })
        summary_df = pd.DataFrame(summary_rows)
        summary_df.to_csv(os.path.join(self.base_dir, "machine_learning", "prediction_results.csv"), index=False)

        fi_df = self._extract_feature_importance(best_model_obj, feature_names)
        fi_df.to_csv(os.path.join(self.base_dir, "machine_learning", "feature_importance.csv"), index=False)

        return results, best_model_name, summary_df

    def _extract_feature_importance(self, model: Any, feature_names: List[str]) -> pd.DataFrame:
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
        else:
            importances = np.ones(len(feature_names)) / len(feature_names)

        fi_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": importances
        }).sort_values(by="Importance", ascending=False).reset_index(drop=True)
        return fi_df

if __name__ == "__main__":
    pass
