"""
Chi-Square Test of Independence - Claims Data Example

Research Question:
Is there an association between claim status (Paid/Denied/Pending) and
whether the patient is a Stonybrook patient?

Test Type: Chi-Square Test of Independence
- Variable 1: claim_status (categorical - Paid/Denied/Pending)
- Variable 2: stonybrook_patient (categorical - Stonybrook vs Non-Stonybrook)

Null Hypothesis (H0): There is NO association between claim status and
                      Stonybrook patient status (variables are independent)

When to use Chi-Square Test:
- Testing association between two categorical variables
- Data is in the form of counts/frequencies
- Expected frequency in each cell should be ≥ 5
- Independent observations

Interpreting Results:
- Chi-square statistic: Measures the difference between observed and expected frequencies
- p-value < 0.05: Reject null hypothesis (variables are associated)
- p-value >= 0.05: Fail to reject null hypothesis (variables are independent)
- Cramér's V: Effect size measure (0 = no association, 1 = perfect association)
  - Small effect: 0.1, Medium effect: 0.3, Large effect: 0.5
"""

import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the claims data
df = pd.read_csv('Module5_inferential/data/clinical_combo/claims_data.csv')

# Data preparation
df_clean = df[['claim_status', 'stonybrook_patient']].dropna()

# Create readable patient labels
df_clean['patient_type'] = df_clean['stonybrook_patient'].apply(
    lambda x: 'Stonybrook' if x == 1 else 'Non-Stonybrook'
)



# Display individual variable distributions
print(df_clean['claim_status'].value_counts())
print(df_clean['patient_type'].value_counts())


# Create contingency table
contingency_table = pd.crosstab(
    df_clean['claim_status'],
    df_clean['patient_type'],
    margins=True,
    margins_name='Total'
)
print(contingency_table)


# Create percentage tables
row_percentages = pd.crosstab(
    df_clean['claim_status'],
    df_clean['patient_type'],
    normalize='index'
) * 100
print(row_percentages.round(2))



col_percentages = pd.crosstab(
    df_clean['claim_status'],
    df_clean['patient_type'],
    normalize='columns'
) * 100
print(col_percentages.round(2))


# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Stacked bar chart (counts)
ax1 = axes[0, 0]
contingency_plot = pd.crosstab(
    df_clean['claim_status'],
    df_clean['patient_type']
)
contingency_plot.plot(kind='bar', stacked=True, ax=ax1,
                     color=['#3498db', '#e74c3c'], edgecolor='black')
ax1.set_title('Claim Status Distribution by Patient Type (Counts)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Claim Status', fontsize=12)
ax1.set_ylabel('Number of Claims', fontsize=12)
ax1.legend(title='Patient Type', fontsize=10)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
ax1.grid(True, alpha=0.3, axis='y')

# 2. Grouped bar chart (counts)
ax2 = axes[0, 1]
contingency_plot.plot(kind='bar', ax=ax2,
                     color=['#3498db', '#e74c3c'], edgecolor='black')
ax2.set_title('Claim Status Distribution by Patient Type (Grouped)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Claim Status', fontsize=12)
ax2.set_ylabel('Number of Claims', fontsize=12)
ax2.legend(title='Patient Type', fontsize=10)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
ax2.grid(True, alpha=0.3, axis='y')

# 3. Heatmap of proportions
ax3 = axes[1, 0]
sns.heatmap(col_percentages, annot=True, fmt='.1f', cmap='YlOrRd',
           ax=ax3, cbar_kws={'label': 'Percentage'})
ax3.set_title('Claim Status by Patient Type (Column %)', fontsize=14, fontweight='bold')
ax3.set_xlabel('Patient Type', fontsize=12)
ax3.set_ylabel('Claim Status', fontsize=12)

# 4. Stacked bar chart (percentages)
ax4 = axes[1, 1]
col_percentages.T.plot(kind='bar', stacked=True, ax=ax4,
                      colormap='Set3', edgecolor='black')
ax4.set_title('Claim Status Distribution by Patient Type (%)', fontsize=14, fontweight='bold')
ax4.set_xlabel('Patient Type', fontsize=12)
ax4.set_ylabel('Percentage of Claims', fontsize=12)
ax4.legend(title='Claim Status', fontsize=10, loc='upper right')
ax4.set_xticklabels(ax4.get_xticklabels(), rotation=0)
ax4.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()



# Perform Chi-Square Test
# Remove margins from contingency table for the test
contingency_for_test = pd.crosstab(
    df_clean['claim_status'],
    df_clean['patient_type']
)

chi2, p_value, dof, expected_freq = chi2_contingency(contingency_for_test)


# Chi-square statistic interpretation:
# - Measures how much the observed frequencies differ from expected frequencies
# - Larger values indicate greater deviation from independence (stronger association)
# - The statistic follows a chi-square distribution with degrees of freedom = (rows-1) × (columns-1)
# - Compare to critical value or use p-value to determine statistical significance

print(f"Chi-square statistic (χ²): {chi2:.4f}")
print(f"Degrees of freedom: {dof}")
print(f"p-value: {p_value:.4f}")


# Calculate Cramér's V for effect size
n = contingency_for_test.sum().sum()
min_dim = min(contingency_for_test.shape) - 1
cramers_v = np.sqrt(chi2 / (n * min_dim))
print(f"Cramér's V (effect size): {cramers_v:.4f}")


# Display expected frequencies
expected_df = pd.DataFrame(
    expected_freq,
    index=contingency_for_test.index,
    columns=contingency_for_test.columns
)
print(expected_df.round(2))


# Compare observed vs expected
difference_df = contingency_for_test - expected_df
print(difference_df.round(2))

# Check assumption: all expected frequencies >= 5
min_expected = expected_freq.min()
cells_below_5 = (expected_df < 5).sum().sum()

print(f"Minimum expected frequency: {min_expected:.2f}")
print(f"Number of cells with expected frequency < 5: {cells_below_5}")

if min_expected >= 5:
    print("✓ Assumption met: All expected frequencies ≥ 5")
elif min_expected >= 1 and cells_below_5 <= (0.2 * expected_df.size):
    print("⚠ Warning: Some expected frequencies < 5, but less than 20% of cells")
    print("  Results should be interpreted with caution")
else:
    print("⚠ Warning: Too many cells with expected frequencies < 5")
    print("  Consider Fisher's Exact Test or combining categories")
print()


print(f"Chi-square statistic: {chi2:.4f}")
print(f"p-value: {p_value:.4f}")
print()

if p_value < 0.05:
    print("✓ SIGNIFICANT RESULT (p < 0.05)")
    print("  - We reject the null hypothesis")
    print("  - There IS a statistically significant association between")
    print("    claim status and Stonybrook patient enrollment")
    print()

    # Provide directional interpretation for each status
    print("DETAILED INTERPRETATION:")
    print()

    for status in col_percentages.index:
        stonybrook_pct = col_percentages.loc[status, 'Stonybrook']
        non_stonybrook_pct = col_percentages.loc[status, 'Non-Stonybrook']

        print(f"{status} Claims:")
        print(f"  - Stonybrook patients: {stonybrook_pct:.1f}%")
        print(f"  - Non-Stonybrook patients: {non_stonybrook_pct:.1f}%")

        if stonybrook_pct > non_stonybrook_pct:
            diff = stonybrook_pct - non_stonybrook_pct
            print(f"  → {diff:.1f} percentage points HIGHER for Stonybrook patients")
        elif stonybrook_pct < non_stonybrook_pct:
            diff = non_stonybrook_pct - stonybrook_pct
            print(f"  → {diff:.1f} percentage points LOWER for Stonybrook patients")
        else:
            print(f"  → Similar rates for both groups")
        print()

else:
    print("✗ NOT SIGNIFICANT (p >= 0.05)")
    print("  - We fail to reject the null hypothesis")
    print("  - There is NO statistically significant association between")
    print("    claim status and Stonybrook patient enrollment")
    print("  - The two variables appear to be independent")
    print()

    print("INTERPRETATION:")
    print("  - Claim approval/denial rates are similar for both patient types")
    print("  - Stonybrook enrollment does not appear to affect claim outcomes")
print()

# Effect size interpretation
print("EFFECT SIZE INTERPRETATION:")
print(f"Cramér's V = {cramers_v:.4f}")

if cramers_v < 0.1:
    effect = "negligible"
elif cramers_v < 0.3:
    effect = "small"
elif cramers_v < 0.5:
    effect = "medium"
else:
    effect = "large"

print(f"Effect size: {effect.upper()}")
print()


# Contribution to chi-square
print("(How much each cell contributes to the chi-square statistic)")
print("Values > |2| indicate cells contributing most to any association")
print()

standardized_residuals = (contingency_for_test - expected_df) / np.sqrt(expected_df)
print(standardized_residuals.round(2))

# Identify cells with largest contributions
abs_residuals = standardized_residuals.abs()
max_residual = abs_residuals.max().max()
max_location = abs_residuals.stack().idxmax()

print(f"Largest standardized residual: {max_residual:.2f}")
print(f"Location: {max_location[0]} claims, {max_location[1]} patients")
print()

if max_residual > 2:
    print("→ This cell shows the strongest deviation from expected values")
else:
    print("→ No cells show strong deviations from expected values")
print()



for patient_type in ['Stonybrook', 'Non-Stonybrook']:
    total = contingency_for_test[patient_type].sum()
    paid = contingency_for_test.loc['Paid', patient_type] if 'Paid' in contingency_for_test.index else 0
    denied = contingency_for_test.loc['Denied', patient_type] if 'Denied' in contingency_for_test.index else 0
    pending = contingency_for_test.loc['Pending', patient_type] if 'Pending' in contingency_for_test.index else 0

    paid_rate = (paid / total * 100) if total > 0 else 0
    denied_rate = (denied / total * 100) if total > 0 else 0
    pending_rate = (pending / total * 100) if total > 0 else 0

    print(f"{patient_type} Patients:")
    print(f"  Total claims: {total:,}")
    print(f"  Paid rate: {paid_rate:.1f}%")
    print(f"  Denied rate: {denied_rate:.1f}%")
    print(f"  Pending rate: {pending_rate:.1f}%")
    print()


