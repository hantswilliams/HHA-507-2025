"""
Independent Samples t-Test - Patient Data Example

Research Question:
Is there a significant difference in average risk scores between male and female patients?

Test Type: Independent Samples t-Test (Two-Sample t-Test)
- Dependent Variable: risk_score (continuous)
- Independent Variable: gender (categorical with 2 groups: Male vs Female)

Hypotheses:
- Null Hypothesis (H0): The mean risk score is the same for males and females (μ_male = μ_female)
- Alternative Hypothesis (H1): The mean risk score is different for males and females (μ_male ≠ μ_female)

When to use Independent t-Test:
- Comparing means between TWO independent groups
- Dependent variable is continuous
- Independent variable is categorical with exactly 2 groups
- Assumes normality and independence
- Use Welch's t-test when variances are unequal (more robust)

Interpreting Results:
- t-statistic: Standardized difference between group means
  - Larger absolute value = larger difference between groups
- p-value < 0.05: Reject null hypothesis (significant difference exists)
- p-value >= 0.05: Fail to reject null hypothesis (no significant difference)
- Cohen's d: Effect size measure
  - Small: 0.2, Medium: 0.5, Large: 0.8
- Confidence Interval: Range of plausible values for the true difference
"""

import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the patient data
df = pd.read_csv('Module5_inferential/data/clinical_combo/patient_data.csv')

print("=" * 80)
print("Independent t-Test: Risk Score Differences Between Genders")
print("=" * 80)
print()

# Data preparation
print("Dataset Overview:")
print(f"Total Patients: {len(df)}")
print()

# Check gender distribution
print("Gender Distribution:")
print(df['gender'].value_counts())
print()

# Remove any missing values
df_clean = df[['gender', 'risk_score']].dropna()
print(f"Patients after removing missing values: {len(df_clean)}")
print()

# Split data by gender
male_scores = df_clean[df_clean['gender'] == 'M']['risk_score']
female_scores = df_clean[df_clean['gender'] == 'F']['risk_score']

print("=" * 80)
print("DESCRIPTIVE STATISTICS BY GENDER:")
print("=" * 80)
print()

print("Male Patients:")
print(f"  Sample size (n): {len(male_scores)}")
print(f"  Mean risk score: {male_scores.mean():.4f}")
print(f"  Median risk score: {male_scores.median():.4f}")
print(f"  Std deviation: {male_scores.std():.4f}")
print(f"  Min: {male_scores.min():.2f}, Max: {male_scores.max():.2f}")
print()

print("Female Patients:")
print(f"  Sample size (n): {len(female_scores)}")
print(f"  Mean risk score: {female_scores.mean():.4f}")
print(f"  Median risk score: {female_scores.median():.4f}")
print(f"  Std deviation: {female_scores.std():.4f}")
print(f"  Min: {female_scores.min():.2f}, Max: {female_scores.max():.2f}")
print()

mean_difference = male_scores.mean() - female_scores.mean()
print(f"Difference in means (Male - Female): {mean_difference:.4f}")
print()

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Box plot comparison
ax1 = axes[0, 0]
df_clean.boxplot(column='risk_score', by='gender', ax=ax1)
ax1.set_title('Risk Score Distribution by Gender', fontsize=14, fontweight='bold')
ax1.set_xlabel('Gender', fontsize=12)
ax1.set_ylabel('Risk Score', fontsize=12)
plt.sca(ax1)
plt.xticks([1, 2], ['Female', 'Male'])
ax1.get_figure().suptitle('')  # Remove default title

# 2. Violin plot
ax2 = axes[0, 1]
df_clean_labeled = df_clean.copy()
df_clean_labeled['gender'] = df_clean_labeled['gender'].map({'M': 'Male', 'F': 'Female'})
sns.violinplot(data=df_clean_labeled, x='gender', y='risk_score', ax=ax2)
ax2.set_title('Risk Score Distribution (Violin Plot)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Gender', fontsize=12)
ax2.set_ylabel('Risk Score', fontsize=12)

# 3. Overlapping histograms
ax3 = axes[1, 0]
ax3.hist(male_scores, bins=20, alpha=0.6, label='Male', color='blue', edgecolor='black')
ax3.hist(female_scores, bins=20, alpha=0.6, label='Female', color='red', edgecolor='black')
ax3.axvline(male_scores.mean(), color='blue', linestyle='--', linewidth=2, label=f'Male Mean: {male_scores.mean():.2f}')
ax3.axvline(female_scores.mean(), color='red', linestyle='--', linewidth=2, label=f'Female Mean: {female_scores.mean():.2f}')
ax3.set_xlabel('Risk Score', fontsize=12)
ax3.set_ylabel('Frequency', fontsize=12)
ax3.set_title('Risk Score Distribution by Gender', fontsize=14, fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. Mean comparison with error bars
ax4 = axes[1, 1]
means = [male_scores.mean(), female_scores.mean()]
stds = [male_scores.std(), female_scores.std()]
sems = [male_scores.sem(), female_scores.sem()]  # Standard error of mean
x_pos = [0, 1]
colors = ['blue', 'red']

bars = ax4.bar(x_pos, means, yerr=sems, capsize=10, color=colors, alpha=0.7, edgecolor='black')
ax4.set_ylabel('Mean Risk Score', fontsize=12)
ax4.set_title('Mean Risk Score by Gender (±SEM)', fontsize=14, fontweight='bold')
ax4.set_xticks(x_pos)
ax4.set_xticklabels(['Male', 'Female'])
ax4.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for i, (bar, mean, sem) in enumerate(zip(bars, means, sems)):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + sem,
             f'{mean:.2f}',
             ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('Module5_inferential/tests/ttest_patient_visualization.png', dpi=300)
print("Visualization saved as: ttest_patient_visualization.png")
print()

# Test for normality
print("=" * 80)
print("ASSUMPTION CHECK: NORMALITY")
print("=" * 80)
print()

# Shapiro-Wilk test for normality
male_shapiro_stat, male_shapiro_p = stats.shapiro(male_scores)
female_shapiro_stat, female_shapiro_p = stats.shapiro(female_scores)

print("Shapiro-Wilk Test for Normality:")
print(f"  Male scores: W = {male_shapiro_stat:.4f}, p = {male_shapiro_p:.4f}")
print(f"  Female scores: W = {female_shapiro_stat:.4f}, p = {female_shapiro_p:.4f}")
print()

if male_shapiro_p > 0.05 and female_shapiro_p > 0.05:
    print("✓ Both groups appear normally distributed (p > 0.05)")
    print("  Parametric t-test is appropriate")
else:
    print("⚠ One or both groups may not be normally distributed (p < 0.05)")
    print("  Consider using Mann-Whitney U test (non-parametric alternative)")
    print("  OR proceed with t-test if sample sizes are large (Central Limit Theorem)")
print()

# Test for equal variances
print("=" * 80)
print("ASSUMPTION CHECK: EQUAL VARIANCES")
print("=" * 80)
print()

levene_stat, levene_p = stats.levene(male_scores, female_scores)
print(f"Levene's Test for Equal Variances:")
print(f"  Test statistic: {levene_stat:.4f}")
print(f"  p-value: {levene_p:.4f}")
print()

if levene_p > 0.05:
    print("✓ Variances are approximately equal (p > 0.05)")
    print("  Standard t-test is appropriate")
    equal_var = True
else:
    print("⚠ Variances are significantly different (p < 0.05)")
    print("  Using Welch's t-test (does not assume equal variances)")
    equal_var = False
print()

# Perform Independent t-test
print("=" * 80)
print("INDEPENDENT t-TEST RESULTS:")
print("=" * 80)
print()

# Welch's t-test (more robust, doesn't assume equal variances)
t_statistic, p_value = stats.ttest_ind(male_scores, female_scores, equal_var=equal_var)

# Calculate degrees of freedom
if equal_var:
    df_ttest = len(male_scores) + len(female_scores) - 2
    test_type = "Standard Independent t-test"
else:
    # Welch-Satterthwaite equation for unequal variances
    s1_sq = male_scores.var()
    s2_sq = female_scores.var()
    n1 = len(male_scores)
    n2 = len(female_scores)
    df_ttest = ((s1_sq/n1 + s2_sq/n2)**2) / ((s1_sq/n1)**2/(n1-1) + (s2_sq/n2)**2/(n2-1))
    test_type = "Welch's t-test (unequal variances)"

print(f"Test type: {test_type}")
print(f"t-statistic: {t_statistic:.4f}")
print(f"Degrees of freedom: {df_ttest:.2f}")
print(f"p-value (two-tailed): {p_value:.4f}")
print()

# Calculate confidence interval for the difference
se_diff = np.sqrt(male_scores.var()/len(male_scores) + female_scores.var()/len(female_scores))
ci_95 = stats.t.interval(0.95, df_ttest, loc=mean_difference, scale=se_diff)
print(f"95% Confidence Interval for difference: [{ci_95[0]:.4f}, {ci_95[1]:.4f}]")
print()

# Calculate Cohen's d effect size
pooled_std = np.sqrt(((len(male_scores)-1)*male_scores.var() +
                      (len(female_scores)-1)*female_scores.var()) /
                     (len(male_scores) + len(female_scores) - 2))
cohens_d = mean_difference / pooled_std

print(f"Cohen's d (effect size): {cohens_d:.4f}")
print()

# Interpret effect size
if abs(cohens_d) < 0.2:
    effect_size = "negligible"
elif abs(cohens_d) < 0.5:
    effect_size = "small"
elif abs(cohens_d) < 0.8:
    effect_size = "medium"
else:
    effect_size = "large"

print(f"Effect size interpretation: {effect_size.upper()}")
print()

# Statistical interpretation
print("=" * 80)
print("INTERPRETATION:")
print("=" * 80)
print()

print(f"Mean difference (Male - Female): {mean_difference:.4f}")
print()

if p_value < 0.05:
    print("✓ SIGNIFICANT RESULT (p < 0.05)")
    print("  - We reject the null hypothesis")
    print("  - There IS a statistically significant difference in risk scores")
    print("    between male and female patients")
    print()

    if mean_difference > 0:
        print(f"  → Male patients have HIGHER risk scores on average")
        print(f"    (Male: {male_scores.mean():.2f} vs Female: {female_scores.mean():.2f})")
    else:
        print(f"  → Female patients have HIGHER risk scores on average")
        print(f"    (Female: {female_scores.mean():.2f} vs Male: {male_scores.mean():.2f})")
else:
    print("✗ NOT SIGNIFICANT (p >= 0.05)")
    print("  - We fail to reject the null hypothesis")
    print("  - There is NO statistically significant difference in risk scores")
    print("    between male and female patients")
    print(f"  - Both groups have similar mean risk scores")
    print(f"    (Male: {male_scores.mean():.2f} vs Female: {female_scores.mean():.2f})")
print()

print("=" * 80)
print("PRACTICAL SIGNIFICANCE:")
print("=" * 80)
print()
print(f"Effect Size (Cohen's d = {cohens_d:.4f}):")
print(f"  - This represents a {effect_size.upper()} effect")
print()

if abs(cohens_d) >= 0.5:
    print("  → The difference is meaningful from a practical standpoint")
else:
    print("  → The difference may be small from a practical standpoint")
print()

print("=" * 80)
print("CLINICAL SIGNIFICANCE:")
print("=" * 80)
print("Understanding these differences can help:")
print("- Identify if gender is a risk factor that needs consideration")
print("- Tailor care management programs based on gender-specific risks")
print("- Allocate resources appropriately across patient populations")
print("- Inform risk stratification and predictive modeling")
print()
print("Note: Statistical significance doesn't always mean clinical significance.")
print("Consider the magnitude of the difference and its practical implications.")
print("=" * 80)
