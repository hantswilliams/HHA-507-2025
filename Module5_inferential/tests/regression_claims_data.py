"""
Linear Regression Analysis - Claims Data Example

Research Question:
Can we predict the paid amount of a claim based on the claim amount?

Test Type: Simple Linear Regression
- Dependent Variable (Y): paid_amount (what we're trying to predict)
- Independent Variable (X): claim_amount (what we're using to predict)

Hypothesis:
- Null Hypothesis (H0): There is NO linear relationship between claim amount and paid amount (slope = 0)

When to use Linear Regression:
- Predicting a continuous outcome variable
- Examining the relationship between variables
- Understanding how much Y changes when X changes
- Assumes linear relationship, independence, homoscedasticity, and normality of residuals

Interpreting Results:
- R-squared (R²): Proportion of variance explained (0 to 1, higher is better)
  - 0.01-0.09: Small effect
  - 0.09-0.25: Medium effect
  - 0.25+: Large effect
- Coefficient (slope): Change in Y for each unit change in X
- p-value < 0.05: Significant relationship exists
- Intercept: Value of Y when X = 0
"""

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns

# Load the claims data
df = pd.read_csv('Module5_inferential/data/clinical_combo/claims_data.csv')


# Data cleaning and preparation
print(f"Total Claims: {len(df):,}")

# Remove any missing values for our variables of interest
df_clean = df[['claim_amount', 'paid_amount']].dropna()

# Display basic statistics
print(df_clean.describe().round(2))

# Check for correlation
correlation = df_clean['claim_amount'].corr(df_clean['paid_amount'])
print(f"Pearson Correlation Coefficient: {correlation:.4f}")

# Define variables for regression
X = df_clean['claim_amount']
y = df_clean['paid_amount']

# Add constant to the model (intercept)
X_with_const = sm.add_constant(X)

# Fit the regression model
model = sm.OLS(y, X_with_const).fit()

# Print the full regression summary
print(model.summary())


# Extract key statistics
r_squared = model.rsquared
adj_r_squared = model.rsquared_adj
intercept = model.params['const']
slope = model.params['claim_amount']
p_value = model.pvalues['claim_amount']


print(f"R-squared (R²): {r_squared:.4f}")
print(f"Adjusted R-squared: {adj_r_squared:.4f}")
print(f"Intercept (β₀): ${intercept:,.2f}")
print(f"Slope (β₁): {slope:.4f}")
print(f"p-value for slope: {p_value:.4e}")

print(f"1. Model Fit (R² = {r_squared:.4f}):")
print(f"   - The claim amount explains {r_squared*100:.2f}% of the variation in paid amount")

if r_squared < 0.09:
    print("   - This represents a SMALL effect size")
elif r_squared < 0.25:
    print("   - This represents a MEDIUM effect size")
else:
    print("   - This represents a LARGE effect size")


print(f"Regression Equation:")
print(f"   Predicted Paid Amount = ${intercept:.2f} + {slope:.4f} × Claim Amount")


print(f"3. Slope Interpretation:")
print(f"   - For every $1 increase in claim amount,")
print(f"     the paid amount increases by ${slope:.4f}")
print(f"   - This represents approximately {slope*100:.2f}% of the claim amount")
print()

if p_value < 0.05:
    print("4. Statistical Significance (p < 0.05):")
    print("   ✓ The relationship IS statistically significant")
    print("   - We reject the null hypothesis")
    print("   - Claim amount is a significant predictor of paid amount")
else:
    print("4. Statistical Significance (p >= 0.05):")
    print("   ✗ The relationship is NOT statistically significant")
    print("   - We fail to reject the null hypothesis")
    print("   - Claim amount may not be a reliable predictor")
print()





# Example predictions
example_claims = [1000, 5000, 10000, 20000]
for claim_amt in example_claims:
    predicted_paid = intercept + slope * claim_amt
    print(f"Claim Amount: ${claim_amt:>6,.0f} → Predicted Paid Amount: ${predicted_paid:>8,.2f}")
print()

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Scatter plot with regression line
ax1 = axes[0, 0]
ax1.scatter(df_clean['claim_amount'], df_clean['paid_amount'], alpha=0.5, s=20)
ax1.plot(df_clean['claim_amount'], model.predict(X_with_const),
         color='red', linewidth=2, label='Regression Line')
ax1.set_xlabel('Claim Amount ($)', fontsize=12)
ax1.set_ylabel('Paid Amount ($)', fontsize=12)
ax1.set_title('Linear Regression: Claim Amount vs Paid Amount', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Add R² to plot
textstr = f'R² = {r_squared:.4f}\ny = {intercept:.2f} + {slope:.4f}x'
ax1.text(0.05, 0.95, textstr, transform=ax1.transAxes, fontsize=10,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# 2. Residuals vs Fitted Values (check for homoscedasticity)
ax2 = axes[0, 1]
residuals = model.resid
fitted_values = model.fittedvalues
ax2.scatter(fitted_values, residuals, alpha=0.5, s=20)
ax2.axhline(y=0, color='red', linestyle='--', linewidth=2)
ax2.set_xlabel('Fitted Values ($)', fontsize=12)
ax2.set_ylabel('Residuals ($)', fontsize=12)
ax2.set_title('Residual Plot (Check for Homoscedasticity)', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)

# 3. Q-Q plot (check for normality of residuals)
ax3 = axes[1, 0]
stats.probplot(residuals, dist="norm", plot=ax3)
ax3.set_title('Q-Q Plot (Check for Normality of Residuals)', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3)

# 4. Histogram of residuals
ax4 = axes[1, 1]
ax4.hist(residuals, bins=50, edgecolor='black', alpha=0.7)
ax4.set_xlabel('Residuals ($)', fontsize=12)
ax4.set_ylabel('Frequency', fontsize=12)
ax4.set_title('Distribution of Residuals', fontsize=14, fontweight='bold')
ax4.axvline(x=0, color='red', linestyle='--', linewidth=2)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Model diagnostics
""""
1. Homoscedasticity (Constant Variance):")
2. Normality of Residuals:")
3. Shapiro-Wilk test for normality (on a sample if dataset is large)
"""


sample_residuals = residuals.sample(n=5000, random_state=42) if len(residuals) > 5000 else residuals

shapiro_stat, shapiro_p = stats.shapiro(sample_residuals)
print(f"3. Shapiro-Wilk Test for Normality:")
print(f"   - Test statistic: {shapiro_stat:.4f}")
print(f"   - p-value: {shapiro_p:.4f}")
if shapiro_p > 0.05:
    print("   ✓ Residuals appear normally distributed (p > 0.05)")
else:
    print("   ⚠ Residuals may not be normally distributed (p < 0.05)")
    print("     (Note: With large samples, this test can be overly sensitive)")


print("- Understand payer reimbursement patterns")
print(f"Payment Ratio: On average, ${slope:.4f} is paid per dollar claimed")
print(f"              This represents a {slope*100:.2f}% payment rate")
