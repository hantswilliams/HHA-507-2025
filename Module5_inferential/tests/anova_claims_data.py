"""
ANOVA (Analysis of Variance) Test - Claims Data Example

Research Question:
Do mean claim amounts differ significantly across different service types?

Test Type: One-Way ANOVA
- Dependent Variable: claim_amount (continuous)
- Independent Variable: service_type (categorical with multiple groups)

Null Hypothesis (H0): The mean claim amount is the same across all service types

When to use ANOVA:
- Comparing means across 3 or more independent groups (levels)
- Dependent variable is continuous
- Independent variable is categorical
- Assumes normality and homogeneity of variance

Interpreting Results:
- F-statistic: Ratio of between-group variance to within-group variance
- p-value < 0.05: Reject null hypothesis (significant difference exists)
- p-value >= 0.05: Fail to reject null hypothesis (no significant difference)
- Post-hoc tests (Tukey HSD): Identify which specific groups differ from each other
- Eta-squared (η²): Effect size measure (proportion of variance explained)
"""

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the claims data
df = pd.read_csv('Module5_inferential/data/clinical_combo/claims_data.csv')

# Data preparation
df_clean = df[['service_type', 'claim_amount']].dropna()


# Service type distribution
service_counts = df_clean['service_type'].value_counts()
print(service_counts)


# Descriptive statistics by service type
desc_stats = df_clean.groupby('service_type')['claim_amount'].describe()
print(desc_stats.round(2))


# Calculate means
means = df_clean.groupby('service_type')['claim_amount'].mean().sort_values(ascending=False)
for service, mean_amt in means.items():
    count = service_counts[service]
    print(f"{service:20s}: ${mean_amt:>10,.2f}  (n={count:,})")


# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Box plot
ax1 = axes[0, 0]
df_clean.boxplot(column='claim_amount', by='service_type', ax=ax1)
ax1.set_title('Claim Amount Distribution by Service Type', fontsize=14, fontweight='bold')
ax1.set_xlabel('Service Type', fontsize=12)
ax1.set_ylabel('Claim Amount ($)', fontsize=12)
ax1.tick_params(axis='x', rotation=45)
ax1.get_figure().suptitle('')  # Remove default title

# 2. Violin plot
ax2 = axes[0, 1]
sns.violinplot(data=df_clean, x='service_type', y='claim_amount', ax=ax2)
ax2.set_title('Claim Amount Distribution (Violin Plot)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Service Type', fontsize=12)
ax2.set_ylabel('Claim Amount ($)', fontsize=12)
ax2.tick_params(axis='x', rotation=45)

# 3. Bar plot with means and error bars
ax3 = axes[1, 0]
mean_amounts = df_clean.groupby('service_type')['claim_amount'].mean()
sem_amounts = df_clean.groupby('service_type')['claim_amount'].sem()
service_types = mean_amounts.index

bars = ax3.bar(range(len(service_types)), mean_amounts.values,
               yerr=sem_amounts.values, capsize=10, alpha=0.7, edgecolor='black')
ax3.set_xticks(range(len(service_types)))
ax3.set_xticklabels(service_types, rotation=45, ha='right')
ax3.set_ylabel('Mean Claim Amount ($)', fontsize=12)
ax3.set_title('Mean Claim Amount by Service Type (±SEM)', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for i, (bar, mean, sem) in enumerate(zip(bars, mean_amounts.values, sem_amounts.values)):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + sem,
             f'${mean:,.0f}',
             ha='center', va='bottom', fontsize=9, fontweight='bold')

# 4. Strip plot with mean overlay
ax4 = axes[1, 1]
sns.stripplot(data=df_clean, x='service_type', y='claim_amount',
              alpha=0.3, size=3, ax=ax4)
# Overlay means
for i, service in enumerate(service_types):
    mean_val = mean_amounts[service]
    ax4.hlines(mean_val, i-0.4, i+0.4, colors='red', linewidth=3, label='Mean' if i==0 else '')
ax4.set_title('Individual Claims with Mean Values', fontsize=14, fontweight='bold')
ax4.set_xlabel('Service Type', fontsize=12)
ax4.set_ylabel('Claim Amount ($)', fontsize=12)
ax4.tick_params(axis='x', rotation=45)
ax4.legend()

plt.tight_layout()
plt.show()




# Perform One-Way ANOVA
model = ols('claim_amount ~ C(service_type)', data=df_clean).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)


# Extract key statistics
f_statistic = anova_table['F']['C(service_type)']
p_value = anova_table['PR(>F)']['C(service_type)']

# Sum of Squares (SS) calculations for effect size
# sum_sq: The 'sum_sq' column contains the sum of squared deviations from the mean
# ss_between: Between-group variance (variation explained by service_type differences)
# ss_total: Total variance (between-group + within-group variance)

ss_between = anova_table['sum_sq']['C(service_type)']
ss_total = anova_table['sum_sq'].sum()

# Calculate eta-squared (effect size)
eta_squared = ss_between / ss_total

# Interpret effect size
if eta_squared < 0.01:
    effect_size = "small"
elif eta_squared < 0.06:
    effect_size = "medium"
else:
    effect_size = "large"

print(f"Effect size: {effect_size.upper()}")
print(f"  - Service type explains {eta_squared*100:.2f}% of the variance in claim amounts")


if p_value < 0.05:
    print("✓ SIGNIFICANT RESULT (p < 0.05)")
    print("  - We reject the null hypothesis")
    print("  - There IS a statistically significant difference in mean claim amounts")
    print("    across different service types")
    print()

    # Find highest and lowest means
    highest_service = means.index[0]
    lowest_service = means.index[-1]

    print(f"  Highest mean: {highest_service} (${means[highest_service]:,.2f})")
    print(f"  Lowest mean: {lowest_service} (${means[lowest_service]:,.2f})")
    print(f"  Difference: ${means[highest_service] - means[lowest_service]:,.2f}")
else:
    print("✗ NOT SIGNIFICANT (p >= 0.05)")
    print("  - We fail to reject the null hypothesis")
    print("  - There is NO statistically significant difference in mean claim amounts")
    print("    across different service types")
print()

# Post-hoc tests if significant
if p_value < 0.05:
    print("This test identifies which specific service types have different claim amounts")

    tukey = pairwise_tukeyhsd(endog=df_clean['claim_amount'],
                              groups=df_clean['service_type'],
                              alpha=0.05)
    print(tukey)



# Test assumptions

# Levene's test for homogeneity of variance
from scipy.stats import levene

groups = [group['claim_amount'].values for name, group in df_clean.groupby('service_type')]
levene_stat, levene_p = levene(*groups)

print("1. Homogeneity of Variance (Levene's Test):")
print(f"   Test statistic: {levene_stat:.4f}")
print(f"   p-value: {levene_p:.4f}")

if levene_p > 0.05:
    print("   ✓ Variances appear equal across groups (p > 0.05)")
else:
    print("   ⚠ Variances may differ across groups (p < 0.05)")
    print("     Consider using Welch's ANOVA (robust to unequal variances)")
print()

print("2. Normality:")

# Residuals normality
for i, (service, amount) in enumerate(means.items(), 1):
    print(f"{i}. {service}: ${amount:,.2f}")
print("=" * 80)
