"""
IEEE Paper Publication Plot Generator
Exports high-resolution (300 DPI) publication plots: Confusion Matrix, ROC Curve, Precision-Recall Curve, Model Accuracy Comparison, and Feature Importance.
"""

import os
import sys
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, precision_recall_curve, auc
from typing import Dict, Any, List

plt.style.use("seaborn-v0_8-paper" if "seaborn-v0_8-paper" in plt.style.available else "default")
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300
})

logger = logging.getLogger("IEEEPlotGenerator")

class IEEEPlotGenerator:
    def __init__(self, output_dir: str = "graphs"):
        self.output_dir = os.path.abspath(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_all_plots(self, results: Dict[str, Dict[str, Any]], best_model_name: str, fi_df: pd.DataFrame):
        self.plot_confusion_matrix(results[best_model_name]["Confusion Matrix"], best_model_name)
        self.plot_roc_curves(results)
        self.plot_pr_curves(results)
        self.plot_accuracy_comparison(results)
        self.plot_feature_importance(fi_df)

    def plot_confusion_matrix(self, cm: np.ndarray, model_name: str):
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                    xticklabels=["No Violation", "Violation"],
                    yticklabels=["No Violation", "Violation"], ax=ax)
        ax.set_title(f"Confusion Matrix ({model_name})", fontweight="bold")
        ax.set_xlabel("Predicted Label")
        ax.set_ylabel("True Label")
        plt.tight_layout()
        path = os.path.join(self.output_dir, "confusion_matrix.png")
        plt.savefig(path, dpi=300)
        plt.close()
        logger.info(f"Saved {path}")

    def plot_roc_curves(self, results: Dict[str, Dict[str, Any]]):
        fig, ax = plt.subplots(figsize=(6, 5))
        for name, mres in results.items():
            fpr, tpr, _ = roc_curve(mres["y_test"], mres["y_prob"])
            roc_auc = mres["ROC-AUC"]
            ax.plot(fpr, tpr, lw=2, label=f"{name} (AUC = {roc_auc:.3f})")
        ax.plot([0, 1], [0, 1], color="navy", lw=1.5, linestyle="--")
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel("False Positive Rate (FPR)")
        ax.set_ylabel("True Positive Rate (TPR)")
        ax.set_title("Receiver Operating Characteristic (ROC) Curves", fontweight="bold")
        ax.legend(loc="lower right")
        ax.grid(True, linestyle=":", alpha=0.6)
        plt.tight_layout()
        path = os.path.join(self.output_dir, "roc_curve.png")
        plt.savefig(path, dpi=300)
        plt.close()
        logger.info(f"Saved {path}")

    def plot_pr_curves(self, results: Dict[str, Dict[str, Any]]):
        fig, ax = plt.subplots(figsize=(6, 5))
        for name, mres in results.items():
            prec, rec, _ = precision_recall_curve(mres["y_test"], mres["y_prob"])
            pr_auc = auc(rec, prec)
            ax.plot(rec, prec, lw=2, label=f"{name} (AUC = {pr_auc:.3f})")
        ax.set_xlabel("Recall")
        ax.set_ylabel("Precision")
        ax.set_title("Precision-Recall (PR) Curves", fontweight="bold")
        ax.legend(loc="lower left")
        ax.grid(True, linestyle=":", alpha=0.6)
        plt.tight_layout()
        path = os.path.join(self.output_dir, "precision_recall_curve.png")
        plt.savefig(path, dpi=300)
        plt.close()
        logger.info(f"Saved {path}")

    def plot_accuracy_comparison(self, results: Dict[str, Dict[str, Any]]):
        names = list(results.keys())
        accs = [results[n]["Accuracy"] for n in names]
        f1s = [results[n]["F1 Score"] for n in names]
        aucs = [results[n]["ROC-AUC"] for n in names]

        x = np.arange(len(names))
        width = 0.25

        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.bar(x - width, accs, width, label="Accuracy", color="#1f77b4")
        ax.bar(x, f1s, width, label="F1 Score", color="#ff7f0e")
        ax.bar(x + width, aucs, width, label="ROC-AUC", color="#2ca02c")

        ax.set_ylabel("Score")
        ax.set_title("ML Model Performance Metric Comparison", fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(names)
        ax.set_ylim([0.7, 1.05])
        ax.legend(loc="lower right")
        ax.grid(True, axis="y", linestyle=":", alpha=0.6)
        plt.tight_layout()
        path = os.path.join(self.output_dir, "accuracy_comparison.png")
        plt.savefig(path, dpi=300)
        plt.close()
        logger.info(f"Saved {path}")

    def plot_feature_importance(self, fi_df: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(7, 5))
        fi_sorted = fi_df.sort_values(by="Importance", ascending=True)
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(fi_sorted)))
        ax.barh(fi_sorted["Feature"], fi_sorted["Importance"], color=colors)
        ax.set_xlabel("Relative Feature Importance")
        ax.set_title("Random Forest / XGBoost Feature Importance", fontweight="bold")
        ax.grid(True, axis="x", linestyle=":", alpha=0.6)
        plt.tight_layout()
        path = os.path.join(self.output_dir, "feature_importance.png")
        plt.savefig(path, dpi=300)
        plt.close()
        logger.info(f"Saved {path}")

if __name__ == "__main__":
    pass
