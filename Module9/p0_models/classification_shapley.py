# Supervised learning workflow with SHAP explainability (classification)
# Dataset: Breast cancer (diagnostic) from scikit-learn
# Task: Predict malignant/benign and explain feature importance
# To install dependencies (in your environment/terminal):
#   pip install scikit-learn xgboost shap matplotlib

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from xgboost import XGBClassifier
import pandas as pd
import matplotlib.pyplot as plt
import shap


# -------------------------------------------------
# 1. Load the healthcare dataset
# -------------------------------------------------

data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

X = data.data
y = data.target
feature_names = list(data.feature_names)
target_names = list(data.target_names)  # ['malignant', 'benign']
n_total = len(y)


# -------------------------------------------------
# 2. Split into train / test
# -------------------------------------------------


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42,
)



# -------------------------------------------------
# 3. Train XGBoost model
# -------------------------------------------------


model = XGBClassifier(
    n_estimators=200,
    max_depth=3,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)

# Evaluate on test set
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]  # Probability of benign (class 1)

accuracy = accuracy_score(y_test, y_pred)
print(f"\n  Test Set Accuracy: {accuracy:.3f}")

print("\n  Classification Report:")
print(classification_report(y_test, y_pred, target_names=target_names))

print("  Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(f"    {cm}")


# -------------------------------------------------
# 4. SHAP Explainability
# -------------------------------------------------

"""
SHAP (SHapley Additive exPlanations) uses game theory to explain predictions.

For binary classification:
- SHAP values show how features push the prediction toward one class
- Positive SHAP value = pushes toward class 1 (benign)
- Negative SHAP value = pushes toward class 0 (malignant)
- The sum of SHAP values + base value = log-odds of the prediction
"""

# TreeExplainer is optimized for tree-based models like XGBoost
explainer = shap.TreeExplainer(model)

# Calculate SHAP values for test set
print("  Calculating SHAP values for test set...")
shap_values = explainer.shap_values(X_test)

# Get expected value (base value)
expected_value = explainer.expected_value
print(f"\n  Base value (log-odds): {expected_value:.3f}")

# Convert to probability for interpretation
base_prob = 1 / (1 + np.exp(-expected_value))
print(f"  Base probability (benign): {base_prob:.1%}")


# -------------------------------------------------
# 5. Global Feature Importance (SHAP)
# -------------------------------------------------

# Calculate mean absolute SHAP values for each feature
mean_shap = np.abs(shap_values).mean(axis=0)
feature_importance = pd.DataFrame({
    'feature': feature_names,
    'mean_shap': mean_shap
}).sort_values('mean_shap', ascending=False)

print("\n  Top 10 Features by Importance (Mean |SHAP|):")
for i, (_, row) in enumerate(feature_importance.head(10).iterrows()):
    print(f"    {i+1}. {row['feature']:25s}: {row['mean_shap']:.3f}")


# -------------------------------------------------
# 6. SHAP Visualizations
# -------------------------------------------------

# 6a. Summary plot (beeswarm) - shows distribution of SHAP values
print("\n  Creating summary plot (beeswarm)...")
plt.figure(figsize=(12, 8))
shap.summary_plot(shap_values, X_test, feature_names=feature_names, show=False)
plt.title('SHAP Summary Plot - Feature Impact on Predictions\n(Positive = Benign, Negative = Malignant)')
plt.tight_layout()
plt.show()


# 6b. Bar plot - mean absolute SHAP values
print("  Creating bar plot...")
plt.figure(figsize=(12, 8))
shap.summary_plot(shap_values, X_test, feature_names=feature_names, plot_type="bar", show=False)
plt.title('SHAP Feature Importance (Mean |SHAP|)')
plt.tight_layout()
plt.show()


# -------------------------------------------------
# 7. Individual Prediction Explanations
# -------------------------------------------------

"""
Let's explain predictions for specific patients to understand
why the model classified them as malignant or benign.
"""

# Find one malignant and one benign prediction
malignant_idx = np.where(y_pred == 0)[0][0]
benign_idx = np.where(y_pred == 1)[0][0]
sample_indices = [malignant_idx, benign_idx]

for idx in sample_indices:
    actual_class = target_names[y_test[idx]]
    predicted_class = target_names[y_pred[idx]]
    predicted_prob = y_pred_proba[idx]

    print(f"\n  --- Sample {idx} ---")
    print(f"  Actual:      {actual_class}")
    print(f"  Predicted:   {predicted_class}")
    print(f"  P(benign):   {predicted_prob:.1%}")

    # Show SHAP contributions for this patient
    shap_contrib = shap_values[idx]

    # Create a DataFrame of contributions
    contrib_df = pd.DataFrame({
        'feature': feature_names,
        'value': X_test[idx],
        'shap': shap_contrib
    }).sort_values('shap', key=abs, ascending=False)

    print(f"\n  Top 5 feature contributions:")
    for _, row in contrib_df.head(5).iterrows():
        direction = "+" if row['shap'] > 0 else ""
        impact = "toward benign" if row['shap'] > 0 else "toward malignant"
        print(f"    {row['feature']:25s} = {row['value']:8.3f} -> {direction}{row['shap']:.3f} ({impact})")


# 7a. Waterfall plots for both samples
for idx in sample_indices:
    predicted_class = target_names[y_pred[idx]]
    print(f"\n  Creating waterfall plot for Sample {idx} ({predicted_class})...")
    plt.figure(figsize=(12, 6))
    shap.plots.waterfall(shap.Explanation(
        values=shap_values[idx],
        base_values=expected_value,
        data=X_test[idx],
        feature_names=feature_names
    ), show=False)
    plt.title(f'SHAP Waterfall Plot - Sample {idx} (Predicted: {predicted_class})')
    plt.tight_layout()
    plt.show()


# -------------------------------------------------
# 8. Dependence Plots
# -------------------------------------------------

print("\n" + "="*50)
print("Step 8: Dependence Plots")
print("="*50)

"""
Dependence plots show how a feature's value affects the prediction.
They reveal non-linear relationships and feature interactions.
"""

# Get top 3 most important features
top_features = feature_importance.head(3)['feature'].tolist()

for feature in top_features:
    feature_idx = feature_names.index(feature)
    print(f"\n  Creating dependence plot for '{feature}'...")
    plt.figure(figsize=(10, 6))
    shap.dependence_plot(
        feature_idx,
        shap_values,
        X_test,
        feature_names=feature_names,
        show=False
    )
    plt.title(f'SHAP Dependence Plot - {feature}')
    plt.tight_layout()
    plt.show()


# -------------------------------------------------
# 9. Compare SHAP vs XGBoost Feature Importance
# -------------------------------------------------

# Get XGBoost's built-in feature importance (gain-based)
xgb_importance = model.feature_importances_

# Create comparison table
comparison = pd.DataFrame({
    'feature': feature_names,
    'xgb_importance': xgb_importance,
    'shap_importance': mean_shap
})

# Normalize for comparison
comparison['xgb_normalized'] = comparison['xgb_importance'] / comparison['xgb_importance'].sum()
comparison['shap_normalized'] = comparison['shap_importance'] / comparison['shap_importance'].sum()

comparison = comparison.sort_values('shap_normalized', ascending=False)

print("\n  Top 10 Features - Importance Comparison (Normalized):")
print("  " + "-"*60)
print(f"  {'Feature':25s} | {'XGBoost':>10s} | {'SHAP':>10s}")
print("  " + "-"*60)
for _, row in comparison.head(10).iterrows():
    print(f"  {row['feature']:25s} | {row['xgb_normalized']:>10.1%} | {row['shap_normalized']:>10.1%}")


# Visualization: side-by-side comparison (top 15 features)
top_comparison = comparison.head(15)
fig, axes = plt.subplots(1, 2, figsize=(14, 8))

# XGBoost importance
axes[0].barh(top_comparison['feature'], top_comparison['xgb_normalized'], color='steelblue')
axes[0].set_xlabel('Normalized Importance')
axes[0].set_title('XGBoost Feature Importance (Gain)')
axes[0].invert_yaxis()

# SHAP importance
axes[1].barh(top_comparison['feature'], top_comparison['shap_normalized'], color='coral')
axes[1].set_xlabel('Normalized Importance')
axes[1].set_title('SHAP Feature Importance')
axes[1].invert_yaxis()

plt.tight_layout()
plt.show()


