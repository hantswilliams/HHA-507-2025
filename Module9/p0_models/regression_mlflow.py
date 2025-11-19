# Supervised learning workflow with MLflow experiment tracking
# Dataset: Diabetes dataset from scikit-learn
# Task: Predict disease progression one year after baseline
# To install dependencies:
#   pip install scikit-learn xgboost mlflow

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
import mlflow
import mlflow.xgboost
import joblib
import warnings

warnings.filterwarnings('ignore')

# -------------------------------------------------
# MLflow Configuration
# -------------------------------------------------
# Set the tracking URI to your remote MLflow server
mlflow.set_tracking_uri("https://mlflow.hants-williams.com/")

# Set experiment name
EXPERIMENT_NAME = "Diabetes-Regression-Hyperparameter-Tuning"
mlflow.set_experiment(EXPERIMENT_NAME)

print(f"MLflow Tracking URI: {mlflow.get_tracking_uri()}")
print(f"Experiment: {EXPERIMENT_NAME}\n")

# -------------------------------------------------
# 1. Load the healthcare dataset
# -------------------------------------------------
print("="*60)
print("STEP 1: Loading Data")
print("="*60)

data = load_diabetes()

X = data.data
y = data.target
feature_names = data.feature_names

print(f"Feature matrix shape: {X.shape}")
print(f"Target vector shape: {y.shape}")
print(f"Feature names: {list(feature_names)}")
print(f"Target statistics: Min={y.min():.1f}, Max={y.max():.1f}, Mean={y.mean():.1f}, Std={y.std():.1f}")

# -------------------------------------------------
# 2. Split into train / validation / test
# -------------------------------------------------
print("\n" + "="*60)
print("STEP 2: Splitting Data (60% train, 20% val, 20% test)")
print("="*60)

# First split: 80% train+val, 20% test
X_trainval, X_test, y_trainval, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Second split: 60% train, 20% val (from the 80%)
X_train, X_val, y_train, y_val = train_test_split(
    X_trainval, y_trainval, test_size=0.25, random_state=42
)

n_total = len(y)
n_train = len(y_train)
n_val = len(y_val)
n_test = len(y_test)

print(f"Train samples: {n_train} ({n_train/n_total:.1%})")
print(f"Validation samples: {n_val} ({n_val/n_total:.1%})")
print(f"Test samples: {n_test} ({n_test/n_total:.1%})")

# -------------------------------------------------
# 3. Baseline model (predict mean)
# -------------------------------------------------
print("\n" + "="*60)
print("STEP 3: Baseline Model (Predict Mean)")
print("="*60)

train_mean = y_train.mean()
baseline_val_pred = np.full(len(y_val), train_mean)
baseline_test_pred = np.full(len(y_test), train_mean)

# Calculate baseline metrics
baseline_val_metrics = {
    'mse': mean_squared_error(y_val, baseline_val_pred),
    'rmse': np.sqrt(mean_squared_error(y_val, baseline_val_pred)),
    'mae': mean_absolute_error(y_val, baseline_val_pred),
    'r2': r2_score(y_val, baseline_val_pred)
}

baseline_test_metrics = {
    'mse': mean_squared_error(y_test, baseline_test_pred),
    'rmse': np.sqrt(mean_squared_error(y_test, baseline_test_pred)),
    'mae': mean_absolute_error(y_test, baseline_test_pred),
    'r2': r2_score(y_test, baseline_test_pred)
}

print(f"Baseline Validation - RMSE: {baseline_val_metrics['rmse']:.3f}, R²: {baseline_val_metrics['r2']:.3f}")
print(f"Baseline Test - RMSE: {baseline_test_metrics['rmse']:.3f}, R²: {baseline_test_metrics['r2']:.3f}")

# Log baseline to MLflow
with mlflow.start_run(run_name="Baseline_PredictMean"):
    mlflow.log_param("model_type", "baseline_mean")
    mlflow.log_param("description", "Predicts training mean for all samples")
    
    # Log validation metrics
    mlflow.log_metric("val_mse", baseline_val_metrics['mse'])
    mlflow.log_metric("val_rmse", baseline_val_metrics['rmse'])
    mlflow.log_metric("val_mae", baseline_val_metrics['mae'])
    mlflow.log_metric("val_r2", baseline_val_metrics['r2'])
    
    # Log test metrics
    mlflow.log_metric("test_mse", baseline_test_metrics['mse'])
    mlflow.log_metric("test_rmse", baseline_test_metrics['rmse'])
    mlflow.log_metric("test_mae", baseline_test_metrics['mae'])
    mlflow.log_metric("test_r2", baseline_test_metrics['r2'])

# -------------------------------------------------
# 4. Helper function to train and log XGBoost model
# -------------------------------------------------

def train_and_log_xgboost(model_name, model_params, description):
    """
    Train an XGBoost model and log everything to MLflow
    
    Args:
        model_name: Name for the MLflow run
        model_params: Dictionary of XGBoost hyperparameters
        description: Description of the model configuration
    """
    print(f"\n{'='*60}")
    print(f"Training: {model_name}")
    print(f"Description: {description}")
    print(f"{'='*60}")
    
    with mlflow.start_run(run_name=model_name):
        # Log description and parameters
        mlflow.log_param("description", description)
        for param, value in model_params.items():
            mlflow.log_param(param, value)
        
        # Create and train model
        model = XGBRegressor(**model_params)
        model.fit(X_train, y_train)
        
        # Predictions
        train_pred = model.predict(X_train)
        val_pred = model.predict(X_val)
        test_pred = model.predict(X_test)
        
        # Calculate metrics for all sets
        train_metrics = {
            'mse': mean_squared_error(y_train, train_pred),
            'rmse': np.sqrt(mean_squared_error(y_train, train_pred)),
            'mae': mean_absolute_error(y_train, train_pred),
            'r2': r2_score(y_train, train_pred)
        }
        
        val_metrics = {
            'mse': mean_squared_error(y_val, val_pred),
            'rmse': np.sqrt(mean_squared_error(y_val, val_pred)),
            'mae': mean_absolute_error(y_val, val_pred),
            'r2': r2_score(y_val, val_pred)
        }
        
        test_metrics = {
            'mse': mean_squared_error(y_test, test_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, test_pred)),
            'mae': mean_absolute_error(y_test, test_pred),
            'r2': r2_score(y_test, test_pred)
        }
        
        # Log all metrics
        for metric_name, value in train_metrics.items():
            mlflow.log_metric(f"train_{metric_name}", value)
        for metric_name, value in val_metrics.items():
            mlflow.log_metric(f"val_{metric_name}", value)
        for metric_name, value in test_metrics.items():
            mlflow.log_metric(f"test_{metric_name}", value)
        
        # Calculate overfitting indicator
        overfitting_gap = train_metrics['r2'] - val_metrics['r2']
        mlflow.log_metric("overfitting_gap_r2", overfitting_gap)
        
        # Print summary
        print(f"\nResults for {model_name}:")
        print(f"  Train - RMSE: {train_metrics['rmse']:.3f}, R²: {train_metrics['r2']:.3f}")
        print(f"  Val   - RMSE: {val_metrics['rmse']:.3f}, R²: {val_metrics['r2']:.3f}")
        print(f"  Test  - RMSE: {test_metrics['rmse']:.3f}, R²: {test_metrics['r2']:.3f}")
        print(f"  Overfitting Gap (Train R² - Val R²): {overfitting_gap:.3f}")
        
        # Create and save plots locally (MLflow artifact logging may fail on some servers)
        import os
        os.makedirs('Module9/p0_models/mlflow_plots', exist_ok=True)
        
        # Create and log feature importance plot
        feature_importance = model.feature_importances_
        fig, ax = plt.subplots(figsize=(10, 6))
        sorted_idx = np.argsort(feature_importance)
        pos = np.arange(sorted_idx.shape[0]) + 0.5
        ax.barh(pos, feature_importance[sorted_idx], align='center')
        ax.set_yticks(pos)
        ax.set_yticklabels([feature_names[i] for i in sorted_idx])
        ax.set_xlabel('Feature Importance')
        ax.set_title(f'Feature Importance - {model_name}')
        plt.tight_layout()
        
        importance_plot_path = f"Module9/p0_models/mlflow_plots/{model_name}_feature_importance.png"
        plt.savefig(importance_plot_path)
        
        # Try to log to MLflow, but don't fail if artifact storage isn't configured
        try:
            mlflow.log_artifact(importance_plot_path)
        except Exception as e:
            print(f"  ⚠️  Could not log feature importance plot to MLflow: {str(e)[:100]}")
        plt.close()
        
        # Create and log predictions vs actual plot
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Validation predictions
        axes[0].scatter(y_val, val_pred, alpha=0.6, edgecolors='k', linewidth=0.5)
        axes[0].plot([y_val.min(), y_val.max()], [y_val.min(), y_val.max()], 'r--', lw=2)
        axes[0].set_xlabel('Actual Disease Progression')
        axes[0].set_ylabel('Predicted Disease Progression')
        axes[0].set_title(f'Validation Set - {model_name}\nR² = {val_metrics["r2"]:.3f}')
        axes[0].grid(True, alpha=0.3)
        
        # Test predictions
        axes[1].scatter(y_test, test_pred, alpha=0.6, edgecolors='k', linewidth=0.5)
        axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        axes[1].set_xlabel('Actual Disease Progression')
        axes[1].set_ylabel('Predicted Disease Progression')
        axes[1].set_title(f'Test Set - {model_name}\nR² = {test_metrics["r2"]:.3f}')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        predictions_plot_path = f"Module9/p0_models/mlflow_plots/{model_name}_predictions.png"
        plt.savefig(predictions_plot_path)
        
        # Try to log to MLflow, but don't fail if artifact storage isn't configured
        try:
            mlflow.log_artifact(predictions_plot_path)
        except Exception as e:
            print(f"  ⚠️  Could not log predictions plot to MLflow: {str(e)[:100]}")
        plt.close()
        
        # Try to log the model itself
        try:
            mlflow.xgboost.log_model(model, "model")
        except Exception as e:
            print(f"  ⚠️  Could not log model to MLflow: {str(e)[:100]}")
            print(f"  ℹ️  Model will still be saved locally at the end of the script")
        
        print(f"✓ Logged to MLflow: {model_name}")
        
        return model, val_metrics, test_metrics

# -------------------------------------------------
# 5. Train models with different hyperparameters
# -------------------------------------------------

print("\n" + "="*60)
print("STEP 4: Training XGBoost Models with Different Configurations")
print("="*60)

# Model 1: UNDERTUNED (too simple, will likely underfit)
# Very few trees, shallow depth, high learning rate
undertuned_params = {
    'n_estimators': 20,           # Too few trees
    'max_depth': 2,                # Too shallow
    'learning_rate': 0.3,          # Too high learning rate
    'subsample': 0.5,              # Low subsample
    'colsample_bytree': 0.5,       # Low feature sample
    'objective': 'reg:squarederror',
    'random_state': 42,
    'n_jobs': -1
}

model_undertuned, val_metrics_undertuned, test_metrics_undertuned = train_and_log_xgboost(
    model_name="Model_1_Undertuned",
    model_params=undertuned_params,
    description="Undertuned model with too few trees and shallow depth - expects poor performance"
)

# Model 2: BASELINE (reasonable starting point)
baseline_params = {
    'n_estimators': 100,
    'max_depth': 3,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'objective': 'reg:squarederror',
    'random_state': 42,
    'n_jobs': -1
}

model_baseline, val_metrics_baseline, test_metrics_baseline = train_and_log_xgboost(
    model_name="Model_2_Baseline",
    model_params=baseline_params,
    description="Baseline model with standard hyperparameters"
)

# Model 3: WELL-TUNED (carefully tuned for good performance)
welltuned_params = {
    'n_estimators': 300,
    'max_depth': 4,
    'learning_rate': 0.03,
    'subsample': 0.85,
    'colsample_bytree': 0.85,
    'min_child_weight': 3,
    'gamma': 0.1,
    'reg_alpha': 0.1,          # L1 regularization
    'reg_lambda': 1.0,         # L2 regularization
    'objective': 'reg:squarederror',
    'random_state': 42,
    'n_jobs': -1
}

model_welltuned, val_metrics_welltuned, test_metrics_welltuned = train_and_log_xgboost(
    model_name="Model_3_WellTuned",
    model_params=welltuned_params,
    description="Well-tuned model with regularization and optimized hyperparameters"
)

# Model 4: OVERTUNED (too complex, may overfit)
# Too many trees, too deep, very low learning rate
overtuned_params = {
    'n_estimators': 1000,         # Too many trees
    'max_depth': 8,               # Too deep - will overfit
    'learning_rate': 0.01,        # Very low learning rate
    'subsample': 0.95,
    'colsample_bytree': 0.95,
    'min_child_weight': 1,        # Allow smaller leaves
    'gamma': 0,                   # No pruning
    'reg_alpha': 0,               # No L1 regularization
    'reg_lambda': 0,              # No L2 regularization
    'objective': 'reg:squarederror',
    'random_state': 42,
    'n_jobs': -1
}

model_overtuned, val_metrics_overtuned, test_metrics_overtuned = train_and_log_xgboost(
    model_name="Model_4_Overtuned",
    model_params=overtuned_params,
    description="Overtuned model with excessive complexity - expects overfitting"
)

# -------------------------------------------------
# 6. Final Comparison
# -------------------------------------------------

print("\n" + "="*60)
print("FINAL COMPARISON - All Models")
print("="*60)

comparison_data = {
    'Model': ['Baseline (Mean)', 'Undertuned', 'Baseline XGB', 'Well-Tuned', 'Overtuned'],
    'Val_R2': [
        baseline_val_metrics['r2'],
        val_metrics_undertuned['r2'],
        val_metrics_baseline['r2'],
        val_metrics_welltuned['r2'],
        val_metrics_overtuned['r2']
    ],
    'Val_RMSE': [
        baseline_val_metrics['rmse'],
        val_metrics_undertuned['rmse'],
        val_metrics_baseline['rmse'],
        val_metrics_welltuned['rmse'],
        val_metrics_overtuned['rmse']
    ],
    'Test_R2': [
        baseline_test_metrics['r2'],
        test_metrics_undertuned['r2'],
        test_metrics_baseline['r2'],
        test_metrics_welltuned['r2'],
        test_metrics_overtuned['r2']
    ],
    'Test_RMSE': [
        baseline_test_metrics['rmse'],
        test_metrics_undertuned['rmse'],
        test_metrics_baseline['rmse'],
        test_metrics_welltuned['rmse'],
        test_metrics_overtuned['rmse']
    ]
}

df_comparison = pd.DataFrame(comparison_data)
df_comparison = df_comparison.round(3)

print("\n" + df_comparison.to_string(index=False))

# Find best model
best_model_idx = df_comparison['Val_R2'].idxmax()
best_model_name = df_comparison.loc[best_model_idx, 'Model']
print(f"\n🏆 Best model based on Validation R²: {best_model_name}")

# -------------------------------------------------
# 7. Save the best model locally
# -------------------------------------------------

print("\n" + "="*60)
print("STEP 5: Saving Best Model")
print("="*60)

# Use the well-tuned model as our final model
import os
os.makedirs('Module9/p0_models/models', exist_ok=True)

model_filename = 'Module9/p0_models/models/regression_diabetes_xgb_mlflow.model'
joblib.dump(model_welltuned, model_filename)
print(f"✓ Best model saved to: {model_filename}")

# Save scaler and feature information
scaler = StandardScaler()
scaler.fit(X_train)

scaler_filename = 'Module9/p0_models/models/regression_diabetes_scaler_mlflow.joblib'
joblib.dump({
    'scaler': scaler,
    'feature_names': list(feature_names),
    'X_train_stats': {
        'mean': X_train.mean(axis=0).tolist(),
        'std': X_train.std(axis=0).tolist(),
        'min': X_train.min(axis=0).tolist(),
        'max': X_train.max(axis=0).tolist(),
    }
}, scaler_filename)
print(f"✓ Scaler and statistics saved to: {scaler_filename}")

print("\n" + "="*60)
print("EXPERIMENT COMPLETE!")
print("="*60)
print(f"View your experiments at: https://mlflow.hants-williams.com/")
print(f"Experiment name: {EXPERIMENT_NAME}")
print(f"\nNote: Plots and visualizations saved locally in:")
print(f"  Module9/p0_models/mlflow_plots/")
print("="*60)