"""
Epidemiological Analytics Examples
Simple demonstrations of key epidemiological measures
Study: Association between smoking and lung cancer

See data_dictionary.md for variable descriptions
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate

# Set seaborn style for clean visualizations
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


# ============================================================================
# SECTION 1: Load Data
# ============================================================================
print("\n=== SECTION 1: Loading Data ===\n")

# Load the simulated dataset
df = pd.read_csv('Module4_epidemiological/simulated_data.csv')

print(f"Loaded dataset with {len(df)} records")
print("\nFirst 10 rows:")
print(df.head(10))
print("\nDataFrame info:")
print(df.info())


# ============================================================================
# SECTION 2: Descriptive Statistics using Pandas
# ============================================================================
print("\n\n=== SECTION 2: Descriptive Statistics ===\n")

# Use pandas describe() for numerical columns
print(df['age'].describe())

# Count total people
total_people = len(df)
print(f"\n\nTotal people in study: {total_people}")

# Use value_counts() for categorical data
gender_counts = df['gender'].value_counts()
print(gender_counts)
print(df['gender'].value_counts(normalize=True) * 100)

smoker_counts = df['is_smoker'].value_counts()
print(smoker_counts)
print(df['is_smoker'].value_counts(normalize=True) * 100)

cancer_counts = df['has_cancer'].value_counts()
print(cancer_counts)
print(df['has_cancer'].value_counts(normalize=True) * 100)

# Visualizations

# 1. Age Distribution
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='age', bins=20, kde=True)
plt.title('Age Distribution of Study Population', fontsize=14, fontweight='bold')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('Module4_epidemiological/viz_age_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()
print("✓ Saved: viz_age_distribution.png")

# 2. Gender and Smoking Distribution
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.countplot(data=df, x='gender', ax=axes[0], palette='Set2')
axes[0].set_title('Gender Distribution', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Count')
sns.countplot(data=df, x='is_smoker', ax=axes[1], palette='Set1')
axes[1].set_title('Smoking Status Distribution', fontsize=12, fontweight='bold')
axes[1].set_xticklabels(['Non-Smoker', 'Smoker'])
axes[1].set_ylabel('Count')
plt.tight_layout()
plt.savefig('Module4_epidemiological/viz_demographics.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()
print("✓ Saved: viz_demographics.png")

# 3. Cancer Status by Smoking
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='is_smoker', hue='has_cancer', palette='rocket')
plt.title('Cancer Status by Smoking Behavior', fontsize=14, fontweight='bold')
plt.xlabel('Smoking Status')
plt.ylabel('Count')
plt.legend(title='Has Cancer', labels=['No', 'Yes'])
plt.xticks([0, 1], ['Non-Smoker', 'Smoker'])
plt.tight_layout()
plt.savefig('Module4_epidemiological/viz_smoking_cancer.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()
print("✓ Saved: viz_smoking_cancer.png")

# 4. Age Distribution by Cancer Status
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='has_cancer', y='age', palette='viridis')
plt.title('Age Distribution by Cancer Status', fontsize=14, fontweight='bold')
plt.xlabel('Has Cancer')
plt.ylabel('Age')
plt.xticks([0, 1], ['No', 'Yes'])
plt.tight_layout()
plt.savefig('Module4_epidemiological/viz_age_by_cancer.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()
print("✓ Saved: viz_age_by_cancer.png")

print("\nAll visualizations saved successfully!")


# ============================================================================
# SECTION 3: Summary Tables
# ============================================================================

# Table 1: Smoking vs Cancer (2x2 Contingency Table)
print("TABLE 1: Association Between Smoking Status and Lung Cancer")
print("="*70)
table1 = pd.crosstab(df['is_smoker'], df['has_cancer'], margins=True)
table1.index = ['Non-smoker', 'Smoker', 'Total']
table1.columns = ['No Cancer', 'Cancer', 'Total']
print(tabulate(table1, headers='keys', tablefmt='grid'))

# Table 2: Smoking vs Cancer with Percentages
print("\n\nTABLE 2: Cancer Rates by Smoking Status")
print("="*70)
table2 = df.groupby('is_smoker')['has_cancer'].agg(['count', 'sum', 'mean'])
table2.columns = ['Total', 'Cancer Cases', 'Cancer Rate']
table2.index = ['Non-smoker', 'Smoker']
table2['Cancer Rate (%)'] = (table2['Cancer Rate'] * 100).round(1)
print(tabulate(table2[['Total', 'Cancer Cases', 'Cancer Rate (%)']], headers='keys', tablefmt='grid'))

# Table 3: Age Statistics by Groups
print("\n\nTABLE 3: Age Distribution by Smoking and Cancer Status")
print("="*70)
table3 = df.groupby(['is_smoker', 'has_cancer'])['age'].agg(['count', 'mean', 'std', 'median', 'min', 'max'])
table3.columns = ['N', 'Mean', 'SD', 'Median', 'Min', 'Max']
table3.index = pd.MultiIndex.from_tuples([
    ('Non-smoker', 'No Cancer'), ('Non-smoker', 'Cancer'),
    ('Smoker', 'No Cancer'), ('Smoker', 'Cancer')
])
print(tabulate(table3.round(1), headers='keys', tablefmt='grid'))


# ============================================================================
# SECTION 4: Calculate INCIDENCE
# ============================================================================
print("Incidence = New cases / Population at risk")

# Count using pandas
# NEW cases only (not existing cases)
new_cases = df['is_new_case'].sum()  # sum of True values

# Population at risk (those flagged as at_risk)
population_at_risk = df['at_risk'].sum()

incidence = new_cases / population_at_risk

print(f"\nNew cases: {new_cases}")
print(f"Population at risk: {population_at_risk}")
print(f"Incidence: {incidence:.4f}")
print(f"Incidence as percentage: {incidence * 100:.2f}%")
print(f"\nInterpretation: {incidence * 100:.2f}% of the at-risk population developed NEW lung cancer")



# ============================================================================
# SECTION 5: Calculate PREVALENCE
# ============================================================================
print("\n\n=== SECTION 5: PREVALENCE ===\n")
print("Prevalence = Existing cases / Total population")

existing_cases = df['has_cancer'].sum()
total_population = 50000  # Assuming a larger population beyond our sample

prevalence = existing_cases / total_population

print(f"\nExisting cases: {existing_cases}")
print(f"Total population: {total_population}")
print(f"Prevalence: {prevalence:.4f}")
print(f"Prevalence as percentage: {prevalence * 100:.2f}%")
print(f"\nInterpretation: {prevalence * 100:.2f}% of the population has lung cancer")


# ============================================================================
# SECTION 6: Calculate RELATIVE RISK (RR)
# ============================================================================
print("Relative Risk = (Incidence in exposed) / (Incidence in unexposed)")

# EXPOSED GROUP (Smokers) - using pandas filtering
smokers_df = df[df['is_smoker'] == True]
smokers_with_cancer = smokers_df['has_cancer'].sum()
total_smokers = len(smokers_df)
incidence_smokers = smokers_with_cancer / total_smokers

# UNEXPOSED GROUP (Non-smokers)
nonsmokers_df = df[df['is_smoker'] == False]
nonsmokers_with_cancer = nonsmokers_df['has_cancer'].sum()
total_nonsmokers = len(nonsmokers_df)
incidence_nonsmokers = nonsmokers_with_cancer / total_nonsmokers

# Calculate Relative Risk
relative_risk = incidence_smokers / incidence_nonsmokers

print(f"\nRELATIVE RISK CALCULATION:")
print(f"RR = {incidence_smokers:.4f} / {incidence_nonsmokers:.4f}")
print(f"RR = {relative_risk:.2f}")
print(f"\nInterpretation: Smokers are {relative_risk:.2f} times more likely")
print(f"to develop lung cancer compared to non-smokers")


# ============================================================================
# SECTION 7: Calculate ODDS RATIO (OR)
# ============================================================================

# A = Exposed (smokers) AND has cancer
A = len(df[(df['is_smoker'] == True) & (df['has_cancer'] == True)])

# B = Exposed (smokers) AND does NOT have cancer
B = len(df[(df['is_smoker'] == True) & (df['has_cancer'] == False)])

# C = Unexposed (non-smokers) AND has cancer
C = len(df[(df['is_smoker'] == False) & (df['has_cancer'] == True)])

# D = Unexposed (non-smokers) AND does NOT have cancer
D = len(df[(df['is_smoker'] == False) & (df['has_cancer'] == False)])

# Calculate Odds Ratio
odds_ratio = (A * D) / (B * C)

print(f"\nODDS RATIO CALCULATION:")
print(f"OR = {odds_ratio:.2f}")

print(f"\nINTERPRETATION:")
if odds_ratio > 1:
    print(f"OR = {odds_ratio:.2f} is greater than 1")
    print(f"This means INCREASED odds of cancer with smoking exposure")
    print(f"The odds of cancer are {odds_ratio:.2f} times higher in smokers")
elif odds_ratio < 1:
    print(f"OR = {odds_ratio:.2f} is less than 1")
    print(f"This means DECREASED odds of cancer with smoking exposure")
else:
    print(f"OR = 1.0 means NO association between smoking and cancer")


# ============================================================================
# SECTION 8: Summary Data
# ============================================================================
print(f"Population size: {total_people}")
print(f"Incidence: {incidence * 100:.2f}%")
print(f"Prevalence: {prevalence * 100:.2f}%")
print(f"Relative Risk: {relative_risk:.2f}")
print(f"Odds Ratio: {odds_ratio:.2f}")



