# Simple supervised learning workflow (regression)
# Dataset: Diabetes dataset from scikit-learn
# Task: Predict disease progression one year after baseline
# To install dependencies (in your environment/terminal):
#   pip install scikit-learn xgboost

import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)
from xgboost import XGBRegressor
import pandas as pd
import matplotlib.pyplot as plt


# -------------------------------------------------
# 1. Load the healthcare dataset
# -------------------------------------------------

data = load_diabetes()

##### original dataset: https://www4.stat.ncsu.edu/~boos/var.select/diabetes.html
## https://www4.stat.ncsu.edu/~boos/var.select/diabetes.tab.txt

"""
The features (predictors) are ten baseline variables: age, sex, body mass index (BMI),
average blood pressure (BP), and six blood serum measurements (S1-S6).

The target is a quantitative measure of disease progression one year after baseline.
All features have been mean-centered and scaled by the standard deviation times the
number of samples (i.e., the sum of squares of each column totals 1).
"""

## print preview data by converting to pandas DataFrame (optional)
### sklearn uses numpy arrays by default for data storage
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

#### lets create a visualization of target distribution (optional)
plt.hist(data.target, bins=30, edgecolor='k', alpha=0.7)
plt.title('Distribution of Disease Progression Target')
plt.xlabel('Disease Progression Measure')
plt.ylabel('Number of Patients')
plt.show()

X = data.data           # features (baseline measurements)
y = data.target         # target: disease progression measure (continuous)

feature_names = data.feature_names

print("Step 1: Load data")
print("  Feature matrix shape:", X.shape)
print("  Target vector shape:", y.shape)
print("  Feature names:", list(feature_names))
print("  Target statistics:")
print(f"    Min: {y.min():.1f}, Max: {y.max():.1f}")
print(f"    Mean: {y.mean():.1f}, Std: {y.std():.1f}")

n_total = len(y)
print("  Total number of samples:", n_total)

# -------------------------------------------------
# 2. Split into train / validation / test
# -------------------------------------------------
#
# GOAL: End up with approximately:
#   - 60% of data for TRAINING (model learns here)
#   - 20% for VALIDATION (model selection / hyperparameter tuning)
#   - 20% for TEST (held out until the very end)
#
# We do this in TWO STEPS:
#
#   STEP 2a: First split
#       - Take original data
#       - Set aside 20% as TEST (never touch until the end)
#       - Remaining 80% is TEMP data we will later split into TRAIN and VAL
#
#   STEP 2b: Second split
#       - Take that 80% TEMP (train+val) data
#       - Split it into:
#           75% TRAIN  (of TEMP)
#           25% VAL    (of TEMP)
#       - In terms of the ORIGINAL dataset:
#           TRAIN = 0.8 * 0.75 = 0.60  (60%)
#           VAL   = 0.8 * 0.25 = 0.20  (20%)
#           TEST  = 0.2                (20%)

print("\nStep 2: Split data into train / validation / test sets")

# ---------- STEP 2a: train+val vs test ----------
# Note: We don't use stratify for regression since target is continuous
X_trainval, X_test, y_trainval, y_test = train_test_split(
    X,
    y,
    test_size=0.2,       # 20% reserved as TEST
    random_state=42,
)

n_trainval = len(y_trainval)
n_test = len(y_test)

print("    Train+Val samples:", n_trainval, f"({n_trainval / n_total:.1%}) of total")
print("    Test samples:     ", n_test,      f"({n_test / n_total:.1%}) of total")

# ---------- STEP 2b: train vs validation ----------
# We now split the 80% (trainval) into train and val.
# test_size=0.25 here means:
#   - 25% of 80% = 20% of original -> Validation
#   - 75% of 80% = 60% of original -> Training

X_train, X_val, y_train, y_val = train_test_split(
    X_trainval,
    y_trainval,
    test_size=0.25,      # 25% of TRAIN+VAL becomes VALIDATION
    random_state=42,
)

n_train = len(y_train)
n_val = len(y_val)

print("    Train samples:    ", n_train, f"({n_train / n_total:.1%}) of total")
print("    Validation samples:", n_val,   f"({n_val / n_total:.1%}) of total")


# -------------------------------------------------
# 3. Baseline "non-ML" model: predict the mean
# -------------------------------------------------
#
# WHY?
#   - We want a very simple, "dumb" baseline that does *not* use any features.
#   - This shows how well we would do with almost no intelligence at all.
#
# WHAT IS THE MEAN BASELINE?
#   - Look at the target values in the training set (y_train).
#   - Calculate the mean (average) of these values.
#   - Our "model" will always predict that mean value, no matter what the input is.
#
# EXAMPLE:
#   - Suppose in y_train the mean disease progression is 150.
#   - Baseline model: for every patient, we predict 150.
#   - Any ML model should beat this by learning from the features X.

print("\nStep 3: Baseline model (predict the mean)")

# 3a. Calculate mean of training target values
train_mean = y_train.mean()
print(f"  Mean of y_train: {train_mean:.2f}")

# 3b. Create baseline predictions by filling arrays with the mean
baseline_val_pred = np.full(shape=(len(y_val),), fill_value=train_mean)
baseline_test_pred = np.full(shape=(len(y_test),), fill_value=train_mean)

# 3c. Evaluate baseline on VALIDATION set
print("\n=== Baseline (predict mean) - Validation ===")
baseline_val_mse = mean_squared_error(y_val, baseline_val_pred)
baseline_val_rmse = np.sqrt(baseline_val_mse)
baseline_val_mae = mean_absolute_error(y_val, baseline_val_pred)
baseline_val_r2 = r2_score(y_val, baseline_val_pred)

print(f"  MSE:  {baseline_val_mse:.3f}")
print(f"  RMSE: {baseline_val_rmse:.3f}")
print(f"  MAE:  {baseline_val_mae:.3f}")
print(f"  R2:   {baseline_val_r2:.3f}")

## in the output:
### MSE  = Mean Squared Error = average of (actual - predicted)^2
### RMSE = Root Mean Squared Error = sqrt(MSE), same units as target
### MAE  = Mean Absolute Error = average of |actual - predicted|
### R2   = R-squared = 1 - (SS_res / SS_tot), measures how much variance is explained
###        R2 = 0 means model predicts the mean (baseline), R2 = 1 is perfect

# 3d. Evaluate baseline on TEST set
print("\n=== Baseline (predict mean) - Test ===")
baseline_test_mse = mean_squared_error(y_test, baseline_test_pred)
baseline_test_rmse = np.sqrt(baseline_test_mse)
baseline_test_mae = mean_absolute_error(y_test, baseline_test_pred)
baseline_test_r2 = r2_score(y_test, baseline_test_pred)

print(f"  MSE:  {baseline_test_mse:.3f}")
print(f"  RMSE: {baseline_test_rmse:.3f}")
print(f"  MAE:  {baseline_test_mae:.3f}")
print(f"  R2:   {baseline_test_r2:.3f}")


# -------------------------------------------------
# 4. XGBoost regressor (ML model)
# -------------------------------------------------
#
# Now we build a *real* ML model that uses the features X to try
# to beat the baseline.
#
# In a more advanced setting, we would:
#   - Use the validation set to tune hyperparameters.
#   - Possibly try multiple models (linear regression, random forest, etc.).
# Here we just choose some reasonable hyperparameters to keep it simple.

print("\nStep 4: Train an XGBoost model (a real ML model)")

#### setting up the model with some hyperparameters
xgb_model = XGBRegressor(
    n_estimators=200, # number of trees / boosting rounds
    max_depth=3, # maximum depth of each tree
    learning_rate=0.05, # step size shrinkage to prevent overfitting
    subsample=0.8, # fraction of training samples used for each tree
    colsample_bytree=0.8, # fraction of features used for each tree
    objective="reg:squarederror", # regression with squared error loss
    random_state=42, # for reproducibility
    n_jobs=-1, # use all available CPU cores
)






######### TRAINING SET ########
### This is where we create the model by fitting it to the training data
import time
print("  Fitting XGBoost model on the TRAIN data...")

### THIS IS WHERE IT HAPPENS 
xgb_model.fit(X_train, y_train) ## this is where the model learns from the data



start_time = time.time()
print(f"    Start time: {time.ctime(start_time)}")
xgb_model.fit(X_train, y_train) ## this is where the model learns from the data
end_time = time.time()
print(f"    End time:   {time.ctime(end_time)}")
elapsed_time = end_time - start_time
print(f"    Elapsed time for training: {elapsed_time:.2f} seconds")







######## VALIDATION SET ########
# Predictions on validation set (for model selection / hyperparameter tuning)
xgb_val_pred = xgb_model.predict(X_val)

print("\n=== XGBoost - Validation ===")
xgb_val_mse = mean_squared_error(y_val, xgb_val_pred)
xgb_val_rmse = np.sqrt(xgb_val_mse)
xgb_val_mae = mean_absolute_error(y_val, xgb_val_pred)
xgb_val_r2 = r2_score(y_val, xgb_val_pred)

print(f"  MSE:  {xgb_val_mse:.3f}")
print(f"  RMSE: {xgb_val_rmse:.3f}")
print(f"  MAE:  {xgb_val_mae:.3f}")
print(f"  R2:   {xgb_val_r2:.3f}")

#### create df showing predicted vs actual for first 25 samples in validation set (optional)
df_val_results = pd.DataFrame({
    'Actual': y_val,
    'Predicted': xgb_val_pred
}).head(50)

print("\nFirst 50 predictions on VALIDATION set:")
print(df_val_results)



### lets now say that we want to tune some hyperparameters based on the validation
# performance, we would go back to the model definition above and change some of
# the hyperparameters like n_estimators, max_depth, learning_rate, etc., and
# then retrain the model on the training set and re-evaluate on the validation
# set until we are satisfied with the performance.

xgb_model_2 = XGBRegressor(
    n_estimators=500, # increased number of trees
    max_depth=4, # slightly increased depth
    learning_rate=0.02, # decreased learning rate for more robust learning
    subsample=0.9, # increased subsample ratio
    colsample_bytree=0.9, # increased feature sample ratio
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1,
)

print("\n  Fitting TUNED XGBoost model on the TRAIN data...")
xgb_model_2.fit(X_train, y_train)
xgb_val_pred_2 = xgb_model_2.predict(X_val)

print("\n=== TUNED XGBoost - Validation ===")
xgb_val_mse_2 = mean_squared_error(y_val, xgb_val_pred_2)
xgb_val_rmse_2 = np.sqrt(xgb_val_mse_2)
xgb_val_mae_2 = mean_absolute_error(y_val, xgb_val_pred_2)
xgb_val_r2_2 = r2_score(y_val, xgb_val_pred_2)

print(f"  MSE:  {xgb_val_mse_2:.3f}")
print(f"  RMSE: {xgb_val_rmse_2:.3f}")
print(f"  MAE:  {xgb_val_mae_2:.3f}")
print(f"  R2:   {xgb_val_r2_2:.3f}")

##### compare the two models on validation set
print("\nComparison of original and TUNED XGBoost models on VALIDATION set:")
print(f"  Original XGBoost R2: {xgb_val_r2:.3f}, RMSE: {xgb_val_rmse:.3f}")
print(f"  TUNED XGBoost R2:    {xgb_val_r2_2:.3f}, RMSE: {xgb_val_rmse_2:.3f}")










########### TEST SET ########

# Final evaluation on the held-out test set using the non-tuned model
print("\nFinal evaluation on the TEST set using the non-tuned model:")
xgb_model = xgb_model  # use the non-tuned model for final evaluation
xgb_test_pred = xgb_model.predict(X_test)

print("\n=== XGBoost - Test (Final model performance) ===")
xgb_test_mse = mean_squared_error(y_test, xgb_test_pred)
xgb_test_rmse = np.sqrt(xgb_test_mse)
xgb_test_mae = mean_absolute_error(y_test, xgb_test_pred)
xgb_test_r2 = r2_score(y_test, xgb_test_pred)

print(f"  MSE:  {xgb_test_mse:.3f}")
print(f"  RMSE: {xgb_test_rmse:.3f}")
print(f"  MAE:  {xgb_test_mae:.3f}")
print(f"  R2:   {xgb_test_r2:.3f}")

# Compare to baseline
print("\n=== Final Comparison: Baseline vs XGBoost on TEST ===")
print(f"  Baseline R2: {baseline_test_r2:.3f}, RMSE: {baseline_test_rmse:.3f}")
print(f"  XGBoost R2:  {xgb_test_r2:.3f}, RMSE: {xgb_test_rmse:.3f}")
print(f"  Improvement in R2: {xgb_test_r2 - baseline_test_r2:.3f}")
print(f"  Reduction in RMSE: {baseline_test_rmse - xgb_test_rmse:.3f}")


#### create df table showing predicted vs actual for first 25 samples in test set (optional)
df_results = pd.DataFrame({
    'Actual': y_test,
    'Predicted': xgb_test_pred
}).head(25)

print("\nFirst 25 predictions on TEST set:")
print(df_results)







###### save final model to file (optional) inside of Module9/p0_models/models/regression_diabetes_xgb.model
import joblib
model_filename = 'Module9/p0_models/models/regression_diabetes_xgb.model'
joblib.dump(xgb_model, model_filename)
print(f"\nFinal XGBoost model saved to: {model_filename}")


###### save feature statistics for the Flask app to use for scaling raw inputs
# The diabetes dataset features are already standardized, so we save stats to help
# transform real-world values to the standardized space
from sklearn.preprocessing import StandardScaler

# Fit scaler on training data to capture the standardized data's statistics
scaler = StandardScaler()
scaler.fit(X_train)

# Save scaler and feature names
scaler_filename = 'Module9/p0_models/models/regression_diabetes_scaler.joblib'
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
print(f"Feature scaler and statistics saved to: {scaler_filename}")