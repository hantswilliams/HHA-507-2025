# Simple supervised learning workflow (classification) 
# Dataset: Breast cancer (diagnostic) from scikit-learn
# Task: Predict whether a tumor is malignant (0) or benign (1)
# To install dependencies (in your environment/terminal):
#   pip install scikit-learn xgboost

from collections import Counter
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from xgboost import XGBClassifier
import pandas as pd


# -------------------------------------------------
# 1. Load the healthcare dataset
# -------------------------------------------------

data = load_breast_cancer()

##### original dataset: https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic 

"""
The features (predictors) are computed from a digitized image of a fine needle aspirate (FNA) of a breast mass.
They describe characteristics of the cell nuclei present in the image. A few of the images c
an be found at http://www.cs.wisc.edu/~street/images/
The primary outcome to predict is whether the tumor is malignant or benign.  
"""

## print preview data by convert to pandas DataFrame (optional)
### sklearn uses numpy arrays by default for data storage
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

X = data.data           # features (measurements from the tumor), or we would do df.drop(columns=['target'])
y = data.target         # labels: 0 = malignant, 1 = benign; or we would do df['target']

feature_names = data.feature_names
target_names = data.target_names

print("Step 1: Load data")
print("  Feature matrix shape:", X.shape)
print("  Target vector shape:", y.shape)
print("  Classes:", target_names)

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
X_trainval, X_test, y_trainval, y_test = train_test_split(
    X,
    y,
    test_size=0.2,       # 20% reserved as TEST
    stratify=y,
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
    stratify=y_trainval,
    random_state=42,
)

n_train = len(y_train)
n_val = len(y_val)

print("    Train samples:    ", n_train, f"({n_train / n_total:.1%}) of total")
print("    Validation samples:", n_val,   f"({n_val / n_total:.1%}) of total")


# -------------------------------------------------
# 3. Baseline "non-ML" model: most common class
# -------------------------------------------------
#
# WHY?
#   - We want a very simple, "dumb" baseline that does *not* use any features.
#   - This shows how well we would do with almost no intelligence at all.
#
# WHAT IS THE MAJORITY-CLASS BASELINE?
#   - Look at the labels in the training set (y_train).
#   - Count how many examples of each class we have.
#   - Pick the class that appears most often (the majority class).
#   - Our "model" will always predict that one class, no matter what the input is.
#
# EXAMPLE:
#   - Suppose in y_train: 60% are benign, 40% malignant.
#   - Majority class = benign.
#   - Baseline model: for every patient, we predict "benign".
#   - That gives ~60% accuracy without using X at all.

# 3a. Look at class distribution in the training labels
class_counts = Counter(y_train)
print("  Class counts in y_train:", class_counts)
for class_id, count in class_counts.items():
    print(f"    Class {class_id} ({target_names[class_id]}): {count} examples")

# 3b. Find the most common (majority) class
most_common_class = class_counts.most_common(1)[0][0]
print("\n  Most common class in training data:",
      most_common_class,
      f"-> '{target_names[most_common_class]}'")

# 3c. Create baseline predictions by filling arrays with the majority class
baseline_val_pred = np.full(shape=(len(y_val),), fill_value=most_common_class)
baseline_test_pred = np.full(shape=(len(y_test),), fill_value=most_common_class)

# 3d. Evaluate baseline on VALIDATION set
print("\n=== Baseline (most common class) – Validation ===")
print("Accuracy:", round(accuracy_score(y_val, baseline_val_pred), 3))
print("Confusion matrix:\n", confusion_matrix(y_val, baseline_val_pred))
print(
    "Classification report:\n",
    classification_report(
        y_val,
        baseline_val_pred,
        digits=3,
        target_names=target_names,
    ),
)

## in the output:
### precision = TP / (TP + FP) // of all predicted positives, how many were actually positive
### recall    = TP / (TP + FN) // of all actual positives, how many did we correctly predict
### f1-score  = 2 * (precision * recall) / (precision + recall) // harmonic mean of precision and recall
### support   = number of actual occurrences of the class in the specified dataset


# 3e. Evaluate baseline on TEST set
print("\n=== Baseline (most common class) – Test ===")
print("Accuracy:", round(accuracy_score(y_test, baseline_test_pred), 3))
print("Confusion matrix:\n", confusion_matrix(y_test, baseline_test_pred))
print(
    "Classification report:\n",
    classification_report(
        y_test,
        baseline_test_pred,
        digits=3,
        target_names=target_names,
    ),
)

# -------------------------------------------------
# 4. XGBoost classifier (ML model)
# -------------------------------------------------
#
# Now we build a *real* ML model that uses the features X to try
# to beat the baseline.
#
# In a more advanced setting, we would:
#   - Use the validation set to tune hyperparameters.
#   - Possibly try multiple models (logistic regression, random forest, etc.).
# Here we just choose some reasonable hyperparameters to keep it simple.

print("\nStep 4: Train an XGBoost model (a real ML model)")

xgb_model = XGBClassifier(
    n_estimators=200, # number of trees / e.g., boosting rounds which means how many times we build a new tree to correct errors of previous trees
    max_depth=3, # maximum depth of each tree, deeper trees can model more complex relationships but may overfit
    learning_rate=0.05, # used in update to prevent overfitting, smaller values make the model more robust but require more trees
    subsample=0.8, # fraction of training samples used for each tree, helps prevent overfitting, typical values are 0.5-1.0
    colsample_bytree=0.8, # fraction of features used for each tree, helps prevent overfitting, typical values are 0.5-1.0
    objective="binary:logistic", # binary classification with logistic loss
    eval_metric="logloss", # evaluation metric for binary classification, logarithmic loss, we could also usee "error" for classification error rate
    random_state=42, # for reproducibility, allows us to get the same results each time we run the code
    n_jobs=-1, # use all available CPU cores for training to speed up the process; if we set n_jobs=1, it would use only one core
)






######### TRAINING SET ########
### This is where we create the model by fitting it to the training data

print("  Fitting XGBoost model on the TRAIN data...")
xgb_model.fit(X_train, y_train) ## this is where the model learns from the data from the TRAINING SET 








######## VALIDATION SET ########
# Predictions on validation set (for model selection / hyperparameter tuning), now we are brining in the VALIDATION SET, specifically X_val, which are the 
### the new variables/features that the model has not seen before, then we are outputting the predictions into xgb_val_pred
xgb_val_pred = xgb_model.predict(X_val)

print("\n=== XGBoost – Validation ===")
print("Accuracy:", round(accuracy_score(y_val, xgb_val_pred), 3))
print("Confusion matrix:\n", confusion_matrix(y_val, xgb_val_pred))
print(
    "Classification report:\n",
    classification_report(
        y_val,
        xgb_val_pred,
        digits=3,
        target_names=target_names,
    ),
)

### lets now say that we want to tune some hyperparameters based on the validation performance, we would go back to the model definition above and change some of the hyperparameters like n_estimators, max_depth, learning_rate, etc., and 
# then retrain the model on the training set and re-evaluate on the validation set until we are satisfied with the performance.

xgb_model_2 = XGBClassifier(
    n_estimators=500, # increased number of trees
    max_depth=8, # increased depth of each tree
    learning_rate=0.02, # decreased learning rate for more robust learning
    subsample=0.9, # increased subsample ratio
    colsample_bytree=0.9, # increased feature sample ratio
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1,
)

print("  Fitting TUNED XGBoost model on the TRAIN data...")
xgb_model_2.fit(X_train, y_train)
xgb_val_pred_2 = xgb_model_2.predict(X_val)
print("\n=== TUNED XGBoost – Validation ===")
print("Accuracy:", round(accuracy_score(y_val, xgb_val_pred_2), 3))
print("Confusion matrix:\n", confusion_matrix(y_val, xgb_val_pred_2))
print(
    "Classification report:\n",
    classification_report(
        y_val,
        xgb_val_pred_2,
        digits=3,
        target_names=target_names,
    ),
)

##### compare the two models on validation set
print("\nComparison of original and TUNED XGBoost models on VALIDATION set:")
print("Original XGBoost Accuracy:", round(accuracy_score(y_val, xgb_val_pred), 3))
print("TUNED XGBoost Accuracy:   ", round(accuracy_score(y_val, xgb_val_pred_2), 3))










########### TEST SET ########

# Final evaluation on the held-out test set using the TUNED model
print("\nFinal evaluation on the TEST set using the TUNED model:")
xgb_model = xgb_model_2  # use the tuned model for final evaluation
xgb_test_pred = xgb_model.predict(X_test)

print("\n=== XGBoost – Test (Final model performance) ===")
print("Accuracy:", round(accuracy_score(y_test, xgb_test_pred), 3))
print("Confusion matrix:\n", confusion_matrix(y_test, xgb_test_pred))
print(
    "Classification report:\n",
    classification_report(
        y_test,
        xgb_test_pred,
        digits=3,
        target_names=target_names,
    ),
)


### create df table showing predicted vs actual for first 25 samples in test set (optional)
df_results = pd.DataFrame({
    'Actual': y_test,
    'Predicted': xgb_test_pred
}).head(25)

print("\nFirst 25 predictions on TEST set:")
print(df_results)





##### save the trained model to a file for later use (optional) / Module9/p0_models/models/classification_cancer_xgb_model.model
import joblib
model_filename = 'Module9/p0_models/models/classification_cancer_xgb_model.model'
joblib.dump(xgb_model, model_filename)
print(f"\nTrained model saved to: {model_filename}")