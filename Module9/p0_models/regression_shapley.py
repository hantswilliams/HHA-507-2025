import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import pandas as pd
import matplotlib.pyplot as plt
import shap


# -------------------------------------------------
# 1. Load the healthcare dataset
# -------------------------------------------------

data = load_diabetes()

df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

X = data.data
y = data.target
feature_names = list(data.feature_names)

n_total = len(y)


# -------------------------------------------------
# 2. Split into train / test
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
)

# -------------------------------------------------
# 3. Train XGBoost model
# -------------------------------------------------

model = XGBRegressor(
    n_estimators=200,
    max_depth=3,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)

# Evaluate on test set
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)


# -------------------------------------------------
# 4. SHAP Explainability
# -------------------------------------------------

"""
SHAP (SHapley Additive exPlanations) uses game theory to explain predictions.

Key concepts:
- SHAP values show how much each feature contributes to pushing the prediction
  away from the base value (average prediction)
- Positive SHAP value = feature pushes prediction higher
- Negative SHAP value = feature pushes prediction lower
- The sum of all SHAP values + base value = the prediction
"""

# TreeExplainer is optimized for tree-based models like XGBoost
explainer = shap.TreeExplainer(model)

# Calculate SHAP values for test set
shap_values = explainer.shap_values(X_test)

# Get expected value (base value / average prediction)
expected_value = explainer.expected_value
print(f"\n  Base value (average prediction): {expected_value:.2f}")


# -------------------------------------------------
# 5. Global Feature Importance (SHAP)
# -------------------------------------------------

# Calculate mean absolute SHAP values for each feature
mean_shap = np.abs(shap_values).mean(axis=0)
feature_importance = pd.DataFrame({
    'feature': feature_names,
    'mean_shap': mean_shap
}).sort_values('mean_shap', ascending=False)

print("\n  Feature Importance (Mean |SHAP|):")
for _, row in feature_importance.iterrows():
    print(f"    {row['feature']:10s}: {row['mean_shap']:.3f}")


# -------------------------------------------------
# 6. SHAP Visualizations
# -------------------------------------------------

# 6a. Summary plot (beeswarm) - shows distribution of SHAP values
print("\n  Creating summary plot (beeswarm)...")
plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values, X_test, feature_names=feature_names, show=False)
plt.title('SHAP Summary Plot - Feature Impact on Predictions')
plt.tight_layout()
plt.show()


# 6b. Bar plot - mean absolute SHAP values
print("  Creating bar plot...")
plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values, X_test, feature_names=feature_names, plot_type="bar", show=False)
plt.title('SHAP Feature Importance (Mean |SHAP|)')
plt.tight_layout()
plt.show()


# -------------------------------------------------
# 7. Individual Prediction Explanations
# -------------------------------------------------
"""
Let's explain predictions for specific patients to understand
why the model made those predictions.
"""

# Select a few test samples to explain
sample_indices = [0, 10, 20]

for idx in sample_indices:
    print(f"\n  --- Patient {idx} ---")

    # Get actual and predicted values
    actual = y_test[idx]
    predicted = y_pred[idx]

    print(f"  Actual:    {actual:.1f}")
    print(f"  Predicted: {predicted:.1f}")

    # Show SHAP contributions for this patient
    shap_contrib = shap_values[idx]

    # Create a DataFrame of contributions
    contrib_df = pd.DataFrame({
        'feature': feature_names,
        'value': X_test[idx],
        'shap': shap_contrib
    }).sort_values('shap', key=abs, ascending=False)

    print(f"\n  Top feature contributions:")
    for _, row in contrib_df.head(5).iterrows():
        direction = "+" if row['shap'] > 0 else ""
        print(f"    {row['feature']:10s} = {row['value']:7.3f} -> {direction}{row['shap']:.2f}")

    # Verify: base + sum(SHAP) = prediction
    total = expected_value + shap_contrib.sum()
    print(f"\n  Verification: {expected_value:.1f} + {shap_contrib.sum():.1f} = {total:.1f}")


# 7a. Waterfall plot for first patient
print("\n  Creating waterfall plot for Patient 0...")
plt.figure(figsize=(10, 6))
shap.plots.waterfall(shap.Explanation(
    values=shap_values[0],
    base_values=expected_value,
    data=X_test[0],
    feature_names=feature_names
), show=False)
plt.title('SHAP Waterfall Plot - Patient 0')
plt.tight_layout()
plt.show()


# -------------------------------------------------
# 8. Dependence Plots
# -------------------------------------------------
"""
Dependence plots show how a feature's value affects the prediction.
They also reveal interactions with other features.
"""

# Get the most important feature
top_feature = feature_importance.iloc[0]['feature']
top_feature_idx = feature_names.index(top_feature)

print(f"\n  Creating dependence plot for '{top_feature}' (most important feature)...")
plt.figure(figsize=(10, 6))
shap.dependence_plot(
    top_feature_idx,
    shap_values,
    X_test,
    feature_names=feature_names,
    show=False
)
plt.title(f'SHAP Dependence Plot - {top_feature}')
plt.tight_layout()
plt.show()


# Create dependence plot for BMI (clinically relevant)
bmi_idx = feature_names.index('bmi')
print("  Creating dependence plot for 'bmi'...")
plt.figure(figsize=(10, 6))
shap.dependence_plot(
    bmi_idx,
    shap_values,
    X_test,
    feature_names=feature_names,
    show=False
)
plt.title('SHAP Dependence Plot - BMI')
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

print("\n  Feature Importance Comparison (Normalized):")
print("  " + "-"*50)
print(f"  {'Feature':10s} | {'XGBoost':>10s} | {'SHAP':>10s}")
print("  " + "-"*50)
for _, row in comparison.iterrows():
    print(f"  {row['feature']:10s} | {row['xgb_normalized']:>10.1%} | {row['shap_normalized']:>10.1%}")


# Visualization: side-by-side comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# XGBoost importance
axes[0].barh(comparison['feature'], comparison['xgb_normalized'], color='steelblue')
axes[0].set_xlabel('Normalized Importance')
axes[0].set_title('XGBoost Feature Importance (Gain)')
axes[0].invert_yaxis()

# SHAP importance
axes[1].barh(comparison['feature'], comparison['shap_normalized'], color='coral')
axes[1].set_xlabel('Normalized Importance')
axes[1].set_title('SHAP Feature Importance')
axes[1].invert_yaxis()

plt.tight_layout()
plt.show()



