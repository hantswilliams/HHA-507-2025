"""

Research Question:
Does the mean risk score differ significantly across different insurance types?

Test Type: One-Way ANOVA
- Dependent Variable: risk_score (continuous)
- Independent Variable: insurance_type (categorical with 3+ groups)

Null Hypothesis (H0): The mean risk score is the same across all insurance types

"""

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the patient data
df = pd.read_csv('Module5_inferential/data/clinical_combo/patient_data.csv')

# Exploratory Data Analysis
print(f"Total Patients: {len(df)}")
print(df['insurance_type'].value_counts())


# Descriptive statistics by group
print(df.groupby('insurance_type')['risk_score'].describe())


# Visualize the data
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='insurance_type', y='risk_score')
plt.title('Risk Score Distribution by Insurance Type')
plt.xlabel('Insurance Type')
plt.ylabel('Risk Score')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Perform One-Way ANOVA
model = ols('risk_score ~ C(insurance_type)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

# Extract key statistics
f_statistic = anova_table['F']['C(insurance_type)']
p_value = anova_table['PR(>F)']['C(insurance_type)']


print(f"F-statistic: {f_statistic:.4f}")
print(f"p-value: {p_value:.4f}")


if p_value < 0.05:
    print("✓ SIGNIFICANT RESULT (p < 0.05)")
    print("  - We reject the null hypothesis")
    print("  - There IS a statistically significant difference in mean risk scores")
    print("    across different insurance types")
    print("  - At least one insurance type has a significantly different mean risk score")
else:
    print("✗ NOT SIGNIFICANT (p >= 0.05)")
    print("  - We fail to reject the null hypothesis")
    print("  - There is NO statistically significant difference in mean risk scores")
    print("    across different insurance types")
print()

# Post-hoc test (Tukey HSD) to identify which groups differ
if p_value < 0.05:
    print("=" * 80)
    print("POST-HOC TEST (Tukey HSD):")
    print("=" * 80)

    tukey = pairwise_tukeyhsd(endog=df['risk_score'],
                            groups=df['insurance_type'],
                            alpha=0.05)
    print(tukey)
    



# Calculate and display group means
group_means = df.groupby('insurance_type')['risk_score'].mean().sort_values(ascending=False)
for insurance_type, mean_score in group_means.items():
    print(f"{insurance_type:12s}: {mean_score:.2f}")



