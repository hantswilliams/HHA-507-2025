# ============================================================================
# IMPORTS AND SETUP
# ============================================================================

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Set random seed for reproducibility
np.random.seed(42)

# Set seaborn style
sns.set_style("whitegrid")
sns.set_palette("husl")

# ============================================================================
# STEP 1: CREATE SAMPLE HEALTHCARE DATA
# ============================================================================

print("Creating synthetic healthcare dataset...")

# Create sample data structure
n = 1000  # Number of patients

# Generate synthetic patient data
data = {
    'patient_id': range(1, n+1),
    'age': np.random.normal(65, 15, n).clip(18, 95).astype(int),
    'gender': np.random.choice(['M', 'F'], n, p=[0.46, 0.54]),
    'length_of_stay': np.random.lognormal(1.2, 0.8, n).clip(1, 30).astype(int),
    'total_charges': np.random.lognormal(9, 1.2, n).clip(1000, 500000),
    'discharge_disposition': np.random.choice(['Home', 'SNF', 'Rehab', 'Transfer', 'Death'], 
                                             n, p=[0.80, 0.10, 0.03, 0.05, 0.02]),
    'primary_diagnosis': np.random.choice(['Heart Disease', 'Pneumonia', 'Diabetes', 'Stroke', 'Cancer'],
                                         n, p=[0.25, 0.20, 0.20, 0.15, 0.20]),
    'readmission_30d': np.random.choice([0, 1], n, p=[0.85, 0.15]),
    'surgery_performed': np.random.choice([0, 1], n, p=[0.70, 0.30]),
    'infection_acquired': np.random.choice([0, 1], n, p=[0.95, 0.05])
}

# Create DataFrame
df = pd.DataFrame(data)

# Introduce some missing values to simulate real data
missing_indices = np.random.choice(df.index, size=int(n*0.05))
df.loc[missing_indices, 'total_charges'] = np.nan
df.loc[missing_indices, 'age'] = 0


print(f"Dataset created with {len(df)} patient records")

# ============================================================================
# STEP 2: DATA CLEANING AND OVERVIEW
# ============================================================================

print("=" * 60)
print("DATA CLEANING AND OVERVIEW")
print("=" * 60)

print(f'this is hants, hants was here + {df.shape}')

# Basic dataset information
print(f"Dataset shape: {df.shape}")
print(f"Each row represents: Individual patient discharge record")

# Column information
print("\nColumn names and data types:")
print(df.dtypes)

# Check for missing values
print("\nMissing values:")
missing_counts = df.isnull().sum()
missing_pct = (missing_counts / len(df)) * 100
missing_summary = pd.DataFrame({
    'Missing_Count': missing_counts,
    'Missing_Percentage': missing_pct
})

# Basic descriptive statistics
print("\nBasic descriptive statistics:")
print(df.describe())
descriptive_describe = df.describe()
descriptive_describe.to_csv('descriptive_describe.csv')

# ============================================================================
# STEP 3: FREQUENCY ANALYSIS
# ============================================================================

print("\n" + "=" * 60)
print("FREQUENCY ANALYSIS")
print("=" * 60)

# 3A. Categorical variable frequency analysis
print("\n1. CATEGORICAL VARIABLES - Frequency Tables")


df['surgery_performed'].value_counts()


# Gender frequency table - demonstrate all frequency types
print("\nGender Distribution:")
gender_freq = df['gender'].value_counts()
gender_rel_freq = df['gender'].value_counts(normalize=True).sort_index()
gender_cum_freq = gender_freq.cumsum()
gender_rel_cum_freq = gender_rel_freq.cumsum()

freq_table = pd.DataFrame({
    'Absolute_Frequency': gender_freq,
    'Relative_Frequency': gender_rel_freq,
    'Cumulative_Frequency': gender_cum_freq,
    'Relative_Cumulative': gender_rel_cum_freq
})
print(freq_table)
freq_table.to_csv('gender_distribution.csv')

# 3B. Cross-tabulation example
print("\n2. CROSS-TABULATION (Pivot Tables)")
crosstab = pd.crosstab(df['gender'], df['surgery_performed'], margins=True)
print("\nGender vs Surgery Performed:")
print(crosstab)

# Proportions in cross-tab
print("\nProportions (row percentages):")
crosstab_prop = pd.crosstab(df['gender'], df['discharge_disposition'], normalize='index')
print(crosstab_prop.round(3))

# 3C. Grouped frequency for continuous variables
print("\n3. GROUPED FREQUENCY - Age Categories")
df['age_group'] = pd.cut(df['age'], bins=[18, 35, 50, 65, 80, 95], 
                        labels=['A', 'B', 'C', 'D', 'E'])
age_group_freq = df['age_group'].value_counts().sort_index(ascending=True)
print(age_group_freq)

# ============================================================================
# STEP 4: RATIOS, PROPORTIONS, AND RATES
# ============================================================================

print("\n" + "=" * 60)
print("RATIOS, PROPORTIONS, AND RATES")
print("=" * 60)

# 4A. Ratios
print("\n1. RATIOS")
female_count = (df['gender'] == 'F').sum()
male_count = (df['gender'] == 'M').sum()

female_to_male_ratio = female_count / male_count
male_to_female_ratio = male_count / female_count

print(f"Female discharges: {female_count}")
print(f"Male discharges: {male_count}")
print(f"Female-to-male ratio: {female_to_male_ratio:.2f}")
print(f"Male-to-female ratio: {male_to_female_ratio:.2f}")
print(f"Interpretation: For every 1 male discharged, {female_to_male_ratio:.2f} females were discharged")

# 4B. Proportions
print("\n2. PROPORTIONS")
total_discharges = len(df)
female_proportion = female_count / total_discharges
male_proportion = male_count / total_discharges

print(f"Proportion of female discharges: {female_proportion:.3f} ({female_proportion*100:.1f}%)")
print(f"Proportion of male discharges: {male_proportion:.3f} ({male_proportion*100:.1f}%)")

# 4C. Rates
print("\n3. RATES")

# Readmission rate
readmissions = df['readmission_30d'].sum()
readmission_rate = (readmissions / total_discharges) * 100
print(f"30-day readmission rate: {readmission_rate:.1f}%")

# Mortality rate
deaths = (df['discharge_disposition'] == 'Death').sum()
mortality_rate = (deaths / total_discharges) * 100
print(f"In-hospital mortality rate: {mortality_rate:.1f}%")

# Surgery rate
surgeries = df['surgery_performed'].sum()
surgery_rate = (surgeries / total_discharges) * 100
print(f"Surgical procedure rate: {surgery_rate:.1f}%")

# Hospital-acquired infection rate
infections = df['infection_acquired'].sum()
infection_rate = (infections / total_discharges) * 100
print(f"Hospital-acquired infection rate: {infection_rate:.1f}%")

# ============================================================================
# STEP 5: CENTRAL TENDENCY AND VARIABILITY
# ============================================================================

print("\n" + "=" * 60)
print("CENTRAL TENDENCY AND VARIABILITY")
print("=" * 60)

# Focus on length of stay as example
los_data = df['length_of_stay'].dropna()

# 5A. Central tendency measures
print("\n1. CENTRAL TENDENCY MEASURES")
mean_los = los_data.mean()
median_los = los_data.median()
mode_los = los_data.mode().iloc[0] if not los_data.mode().empty else "No mode"

print(f"Length of Stay (days):")
print(f"  Mean: {mean_los:.2f}")
print(f"  Median: {median_los:.2f}")
print(f"  Mode: {mode_los}")

# 5B. Variability measures
print("\n2. VARIABILITY MEASURES")
std_los = los_data.std()
var_los = los_data.var()
range_los = los_data.max() - los_data.min()
iqr_los = los_data.quantile(0.75) - los_data.quantile(0.25)

print(f"  Standard Deviation: {std_los:.2f}")
print(f"  Variance: {var_los:.2f}")
print(f"  Range: {range_los:.2f}")
print(f"  Interquartile Range (IQR): {iqr_los:.2f}")

# 5C. Percentiles and quartiles
print("\n3. PERCENTILES AND QUARTILES")
percentiles = [25, 50, 75, 90, 95]
print("Percentiles for Length of Stay:")
for p in percentiles:
    value = los_data.quantile(p/100)
    print(f"  {p}th percentile: {value:.2f} days")

# ============================================================================
# STEP 6: DISTRIBUTION ASSESSMENT (SKEWNESS & KURTOSIS)
# ============================================================================

print("\n" + "=" * 60)
print("DISTRIBUTION ASSESSMENT")
print("=" * 60)

# Analyze multiple continuous variables
continuous_vars = ['age', 'length_of_stay', 'total_charges']

for var in continuous_vars:
    data = df[var].dropna()
    
    print(f"\n{var.upper()} DISTRIBUTION:")
    
    # Skewness
    skewness = stats.skew(data)
    print(f"  Skewness: {skewness:.3f}")
    if abs(skewness) < 0.5:
        skew_interp = "approximately symmetric"
    elif skewness > 0:
        skew_interp = "positively skewed (right tail)"
    else:
        skew_interp = "negatively skewed (left tail)"
    print(f"  Interpretation: {skew_interp}")
    
    # Kurtosis
    kurtosis = stats.kurtosis(data)
    print(f"  Kurtosis: {kurtosis:.3f}")
    if abs(kurtosis) < 0.5:
        kurt_interp = "mesokurtic (normal-like)"
    elif kurtosis > 0:
        kurt_interp = "leptokurtic (peaked, heavy tails)"
    else:
        kurt_interp = "platykurtic (flat, light tails)"
    print(f"  Interpretation: {kurt_interp}")
    
    # Normality test
    test_data = data[:5000] if len(data) > 5000 else data
    shapiro_stat, shapiro_p = stats.shapiro(test_data)
    print(f"  Shapiro-Wilk test p-value: {shapiro_p:.6f}")
    normal_interp = "normally distributed" if shapiro_p > 0.05 else "not normally distributed"
    print(f"  Interpretation: Data is {normal_interp}")

# ============================================================================
# STEP 7: HEALTHCARE-SPECIFIC METRICS
# ============================================================================

print("\n" + "=" * 60)
print("HEALTHCARE-SPECIFIC METRICS")
print("=" * 60)

total_patients = len(df)

# 7A. Occupancy and utilization metrics
print("\n1. OCCUPANCY AND UTILIZATION METRICS")
avg_los = df['length_of_stay'].mean()
print(f"  Average Length of Stay (ALOS): {avg_los:.2f} days")

# Simulated bed occupancy calculation
total_bed_days = df['length_of_stay'].sum()
available_bed_days = 365 * 100  # Assuming 100 beds available 365 days
occupancy_rate = (total_bed_days / available_bed_days) * 100
print(f"  Estimated Bed Occupancy Rate: {occupancy_rate:.1f}%")

# 7B. Admission and discharge patterns
print("\n2. ADMISSION AND DISCHARGE PATTERNS")
discharge_counts = df['discharge_disposition'].value_counts()
discharge_percentages = df['discharge_disposition'].value_counts(normalize=True) * 100

print("  Discharge Disposition Distribution:")
for disp, count in discharge_counts.items():
    pct = discharge_percentages[disp]
    print(f"    {disp}: {count} ({pct:.1f}%)")

# 7C. Quality metrics
print("\n3. QUALITY METRICS")
readmission_rate_calc = (df['readmission_30d'].sum() / total_patients) * 100
mortality_rate_calc = ((df['discharge_disposition'] == 'Death').sum() / total_patients) * 100
infection_rate_calc = (df['infection_acquired'].sum() / total_patients) * 100

print(f"  30-day Readmission Rate: {readmission_rate_calc:.1f}%")
print(f"  In-hospital Mortality Rate: {mortality_rate_calc:.1f}%")
print(f"  Hospital-Acquired Infection Rate: {infection_rate_calc:.1f}%")

# 7D. Case mix analysis
print("\n4. CASE MIX ANALYSIS")
diagnosis_dist = df['primary_diagnosis'].value_counts(normalize=True) * 100
print("  Primary Diagnosis Distribution:")
for diag, pct in diagnosis_dist.items():
    print(f"    {diag}: {pct:.1f}%")

# ============================================================================
# STEP 8: BASIC VISUALIZATIONS
# ============================================================================

print("\n" + "=" * 60)
print("CREATING VISUALIZATIONS")
print("=" * 60)

# Create a comprehensive dashboard using seaborn
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('Healthcare Data Descriptive Analysis Dashboard', fontsize=16)

# 1. Gender distribution
sns.countplot(data=df, x='gender', ax=axes[0,0])
axes[0,0].set_title('Gender Distribution')
axes[0,0].set_ylabel('Count')

# 2. Length of stay distribution
sns.histplot(data=df, x='length_of_stay', bins=20, ax=axes[0,1])
axes[0,1].set_title('Length of Stay Distribution')
axes[0,1].set_xlabel('Days')
axes[0,1].set_ylabel('Frequency')

# 3. Age distribution
sns.histplot(data=df, x='age', bins=20, ax=axes[0,2])
axes[0,2].set_title('Age Distribution')
axes[0,2].set_xlabel('Age (years)')
axes[0,2].set_ylabel('Frequency')

# 4. Discharge disposition
sns.countplot(data=df, x='discharge_disposition', ax=axes[1,0])
axes[1,0].set_title('Discharge Disposition')
axes[1,0].tick_params(axis='x', rotation=45)

# 5. Total charges (log scale due to skewness)
df_log_charges = df['total_charges'].dropna().apply(np.log)
sns.histplot(x=df_log_charges, bins=20, ax=axes[1,1])
axes[1,1].set_title('Total Charges (Log Scale)')
axes[1,1].set_xlabel('Log(Total Charges)')
axes[1,1].set_ylabel('Frequency')

# 6. Box plot for LOS by gender
sns.boxplot(data=df, x='gender', y='length_of_stay', ax=axes[1,2])
axes[1,2].set_title('Length of Stay by Gender')
axes[1,2].set_xlabel('Gender')
axes[1,2].set_ylabel('Length of Stay (days)')

plt.tight_layout()
plt.show()

print("Visualizations created successfully using seaborn!")

# ============================================================================
# SUMMARY AND KEY TAKEAWAYS
# ============================================================================

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE - KEY TAKEAWAYS")
print("=" * 80)

print("\nKey Takeaways for Healthcare Data:")
print("1. Healthcare data is rarely normally distributed")
print("2. Length of stay and costs typically show positive skewness")
print("3. Ratios and proportions provide meaningful clinical insights")
print("4. Quality metrics (readmission, mortality, infection rates) are critical")
print("5. Visual inspection complements statistical measures")

print("\nNext Steps:")
print("- Apply these techniques to your actual dataset")
print("- Consider data transformations for skewed variables")
print("- Implement quality checks and outlier detection")
print("- Create automated reporting dashboards")

print("\nRemember: Always check data quality and distribution before analysis!")