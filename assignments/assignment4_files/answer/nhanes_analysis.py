import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# DATA LOADING AND PREPARATION
# ============================================================================

data_dir = '../data'

# Load and merge all datasets on SEQN (respondent sequence number)
demo = pd.read_sas(f'{data_dir}/DEMO_L.xpt', format='xport')
bp = pd.read_sas(f'{data_dir}/BPXO_L_boodpressure.xpt', format='xport')
paq = pd.read_sas(f'{data_dir}/PAQ_L_physicalactivity.xpt', format='xport')
bmx = pd.read_sas(f'{data_dir}/BMX_L_bodymeasures.xpt', format='xport')

df = demo.merge(bp, on='SEQN', how='left').merge(paq, on='SEQN', how='left').merge(bmx, on='SEQN', how='left')

# Recode variables
# Marital status: 1=Married vs 0=Not Married (widowed, divorced, separated, never married, living with partner)
df['married'] = df['DMDMARTZ'].apply(lambda x: 1 if x == 1.0 else (0 if x in [2.0, 3.0, 4.0, 5.0, 6.0] else np.nan))

# Education: 1=Bachelor's or higher vs 0=Less than bachelor's
df['bachelor_or_higher'] = df['DMDEDUC2'].apply(lambda x: 1 if x == 5.0 else (0 if x in [1.0, 2.0, 3.0, 4.0] else np.nan))

# Sedentary minutes: clean invalid codes (7777=Refused, 9999=Don't know)
df['sedentary_minutes'] = df['PAD680'].replace([7777, 9999], np.nan)

# Weight (using measured weight BMXWT since WHD020 not in dataset)
df['weight'] = df['BMXWT']

# Age groups for Q5
df['age_group'] = pd.cut(df['RIDAGEYR'], bins=[17, 39, 59, 100],
                         labels=['Young Adults (18-39)', 'Middle-Aged (40-59)', 'Older Adults (60+)'])

alpha = 0.05

# ============================================================================
# QUESTION 1: Chi-Square Test - Marital Status vs Education Level
# ============================================================================

q1_data = df[['married', 'bachelor_or_higher']].dropna()
contingency_table = pd.crosstab(q1_data['married'], q1_data['bachelor_or_higher'])
chi2, p_value_q1, dof, expected = stats.chi2_contingency(contingency_table)


# ============================================================================
# QUESTION 2: Independent t-Test - Sedentary Behavior by Marital Status
# ============================================================================

q2_data = df[['married', 'sedentary_minutes']].dropna()
married_sed = q2_data[q2_data['married'] == 1]['sedentary_minutes']
not_married_sed = q2_data[q2_data['married'] == 0]['sedentary_minutes']

# Use Welch's t-test (unequal variances)
t_stat, p_value_q2 = stats.ttest_ind(married_sed, not_married_sed, equal_var=False)
mean_diff = married_sed.mean() - not_married_sed.mean()

# Cohen's d effect size
pooled_std = np.sqrt(((len(married_sed)-1)*married_sed.std()**2 +
                      (len(not_married_sed)-1)*not_married_sed.std()**2) /
                     (len(married_sed) + len(not_married_sed) - 2))
cohens_d = mean_diff / pooled_std


# ============================================================================
# QUESTION 3: Multiple Regression - Age & Marital Status on Systolic BP
# ============================================================================

q3_data = df[['RIDAGEYR', 'married', 'BPXOSY3']].dropna()
q3_data.columns = ['age', 'married', 'systolic_bp']

X = sm.add_constant(q3_data[['age', 'married']])
model = sm.OLS(q3_data['systolic_bp'], X).fit()

# ============================================================================
# QUESTION 4: Correlation - Weight vs Sedentary Behavior
# ============================================================================

q4_data = df[['weight', 'sedentary_minutes']].dropna()
pearson_r, p_value_q4 = stats.pearsonr(q4_data['weight'], q4_data['sedentary_minutes'])

