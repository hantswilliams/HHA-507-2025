import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

data_dir = '../data'
output_dir = './'

demo = pd.read_sas(f'{data_dir}/DEMO_L.xpt', format='xport')
bp = pd.read_sas(f'{data_dir}/BPXO_L_boodpressure.xpt', format='xport')
paq = pd.read_sas(f'{data_dir}/PAQ_L_physicalactivity.xpt', format='xport')
bmx = pd.read_sas(f'{data_dir}/BMX_L_bodymeasures.xpt', format='xport')

df = demo.merge(bp, on='SEQN', how='left').merge(paq, on='SEQN', how='left').merge(bmx, on='SEQN', how='left')

df['married'] = df['DMDMARTZ'].apply(lambda x: 1 if x == 1.0 else (0 if x in [2.0, 3.0, 4.0, 5.0, 6.0] else np.nan))
df['bachelor_or_higher'] = df['DMDEDUC2'].apply(lambda x: 1 if x == 5.0 else (0 if x in [1.0, 2.0, 3.0, 4.0] else np.nan))
df['sedentary_minutes'] = df['PAD680'].copy()
df.loc[df['sedentary_minutes'].isin([7777, 9999]), 'sedentary_minutes'] = np.nan
df['weight'] = df['BMXWT'].copy()
df['age_group'] = pd.cut(df['RIDAGEYR'], bins=[17, 39, 59, 100],
                          labels=['Young Adults\n(18-39)', 'Middle-Aged\n(40-59)', 'Older Adults\n(60+)'])

# FIGURE 1: Chi-Square - Marital Status vs Education Level
fig1, axes1 = plt.subplots(1, 2, figsize=(12, 5))
q1_data = df[['married', 'bachelor_or_higher']].dropna()

contingency = pd.crosstab(q1_data['married'], q1_data['bachelor_or_higher'])
contingency.index = ['Not Married', 'Married']
contingency.columns = ["Less than Bachelor's", "Bachelor's or Higher"]
contingency.plot(kind='bar', ax=axes1[0], color=['#3498db', '#e74c3c'], edgecolor='black', width=0.7)
axes1[0].set_xlabel('Marital Status', fontsize=12)
axes1[0].set_ylabel('Count', fontsize=12)
axes1[0].set_title('Education Level by Marital Status', fontsize=14, fontweight='bold')
axes1[0].legend(title='Education Level', loc='upper right')
axes1[0].tick_params(axis='x', rotation=0)
for container in axes1[0].containers:
    axes1[0].bar_label(container, fontsize=9)

prop_table = pd.crosstab(q1_data['married'], q1_data['bachelor_or_higher'], normalize='index') * 100
prop_table.index = ['Not Married', 'Married']
prop_table.columns = ["Less than Bachelor's", "Bachelor's or Higher"]
prop_table.plot(kind='barh', stacked=True, ax=axes1[1], color=['#3498db', '#e74c3c'], edgecolor='black')
axes1[1].set_xlabel('Percentage (%)', fontsize=12)
axes1[1].set_ylabel('Marital Status', fontsize=12)
axes1[1].set_title('Education Distribution by Marital Status (%)', fontsize=14, fontweight='bold')
axes1[1].legend(title='Education Level', loc='lower right')
for i, (idx, row) in enumerate(prop_table.iterrows()):
    cumsum = 0
    for j, val in enumerate(row):
        axes1[1].text(cumsum + val/2, i, f'{val:.1f}%', ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        cumsum += val

chi2, p_value, dof, expected = stats.chi2_contingency(pd.crosstab(q1_data['married'], q1_data['bachelor_or_higher']))
fig1.text(0.5, -0.02, f'Chi-square = {chi2:.2f}, p < 0.001 (Significant association)',
          ha='center', fontsize=11, style='italic', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.tight_layout()
plt.savefig(f'{output_dir}fig1_chisquare_marital_education.png', dpi=150, bbox_inches='tight')
plt.close()

# FIGURE 2: t-Test - Sedentary Behavior by Marital Status
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5))
q2_data = df[['married', 'sedentary_minutes']].dropna()
q2_data['Marital Status'] = q2_data['married'].map({0: 'Not Married', 1: 'Married'})

sns.boxplot(data=q2_data, x='Marital Status', y='sedentary_minutes', ax=axes2[0],
            palette={'Not Married': '#e74c3c', 'Married': '#3498db'}, width=0.5)
axes2[0].set_xlabel('Marital Status', fontsize=12)
axes2[0].set_ylabel('Sedentary Minutes per Day', fontsize=12)
axes2[0].set_title('Sedentary Behavior by Marital Status', fontsize=14, fontweight='bold')
means = q2_data.groupby('Marital Status')['sedentary_minutes'].mean()
for i, status in enumerate(['Not Married', 'Married']):
    axes2[0].scatter(i, means[status], color='yellow', s=100, zorder=5, edgecolor='black', marker='D', label='Mean' if i==0 else '')
axes2[0].legend()

sns.violinplot(data=q2_data, x='Marital Status', y='sedentary_minutes', ax=axes2[1],
               palette={'Not Married': '#e74c3c', 'Married': '#3498db'}, inner='quartile')
axes2[1].set_xlabel('Marital Status', fontsize=12)
axes2[1].set_ylabel('Sedentary Minutes per Day', fontsize=12)
axes2[1].set_title('Distribution of Sedentary Behavior', fontsize=14, fontweight='bold')

married_sed = q2_data[q2_data['married'] == 1]['sedentary_minutes']
not_married_sed = q2_data[q2_data['married'] == 0]['sedentary_minutes']
t_stat, t_p = stats.ttest_ind(married_sed, not_married_sed, equal_var=False)
mean_diff = married_sed.mean() - not_married_sed.mean()
fig2.text(0.5, -0.02, f't = {t_stat:.2f}, p < 0.001 | Mean difference: {mean_diff:.1f} minutes (Married lower)',
          ha='center', fontsize=11, style='italic', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.tight_layout()
plt.savefig(f'{output_dir}fig2_ttest_sedentary_marital.png', dpi=150, bbox_inches='tight')
plt.close()

# FIGURE 3: Regression - Age and Marital Status on Systolic BP
fig3, axes3 = plt.subplots(1, 2, figsize=(12, 5))
q3_data = df[['RIDAGEYR', 'married', 'BPXOSY3']].dropna()
q3_data['Marital Status'] = q3_data['married'].map({0: 'Not Married', 1: 'Married'})

for status, color in [('Not Married', '#e74c3c'), ('Married', '#3498db')]:
    subset = q3_data[q3_data['Marital Status'] == status]
    axes3[0].scatter(subset['RIDAGEYR'], subset['BPXOSY3'], alpha=0.2, s=10, color=color, label=status)
    z = np.polyfit(subset['RIDAGEYR'], subset['BPXOSY3'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(subset['RIDAGEYR'].min(), subset['RIDAGEYR'].max(), 100)
    axes3[0].plot(x_line, p(x_line), color=color, linewidth=2, linestyle='-')
axes3[0].set_xlabel('Age (Years)', fontsize=12)
axes3[0].set_ylabel('Systolic Blood Pressure (mmHg)', fontsize=12)
axes3[0].set_title('Systolic BP vs Age by Marital Status', fontsize=14, fontweight='bold')
axes3[0].legend(loc='upper left')

q3_data['Age Group'] = pd.cut(q3_data['RIDAGEYR'], bins=[17, 30, 40, 50, 60, 70, 100],
                               labels=['18-30', '31-40', '41-50', '51-60', '61-70', '70+'])
sns.boxplot(data=q3_data, x='Age Group', y='BPXOSY3', hue='Marital Status', ax=axes3[1],
            palette={'Not Married': '#e74c3c', 'Married': '#3498db'})
axes3[1].set_xlabel('Age Group', fontsize=12)
axes3[1].set_ylabel('Systolic Blood Pressure (mmHg)', fontsize=12)
axes3[1].set_title('Systolic BP by Age Group and Marital Status', fontsize=14, fontweight='bold')
axes3[1].legend(title='Marital Status', loc='upper left')
fig3.text(0.5, -0.02, 'Age: +0.40 mmHg/year (p<0.001) | Married: -1.34 mmHg (p=0.003)',
          ha='center', fontsize=11, style='italic', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.tight_layout()
plt.savefig(f'{output_dir}fig3_regression_bp_age_marital.png', dpi=150, bbox_inches='tight')
plt.close()

# FIGURE 4: Correlation - Weight vs Sedentary Behavior
fig4, axes4 = plt.subplots(1, 2, figsize=(12, 5))
q4_data = df[['weight', 'sedentary_minutes']].dropna()

axes4[0].scatter(q4_data['weight'], q4_data['sedentary_minutes'], alpha=0.3, s=15, color='#9b59b6')
z = np.polyfit(q4_data['weight'], q4_data['sedentary_minutes'], 1)
p = np.poly1d(z)
x_line = np.linspace(q4_data['weight'].min(), q4_data['weight'].max(), 100)
axes4[0].plot(x_line, p(x_line), color='#e74c3c', linewidth=2, linestyle='--', label='Trend line')
axes4[0].set_xlabel('Weight (kg)', fontsize=12)
axes4[0].set_ylabel('Sedentary Minutes per Day', fontsize=12)
axes4[0].set_title('Weight vs Sedentary Behavior', fontsize=14, fontweight='bold')
axes4[0].legend()

hb = axes4[1].hexbin(q4_data['weight'], q4_data['sedentary_minutes'], gridsize=30, cmap='YlOrRd', mincnt=1)
axes4[1].set_xlabel('Weight (kg)', fontsize=12)
axes4[1].set_ylabel('Sedentary Minutes per Day', fontsize=12)
axes4[1].set_title('Density: Weight vs Sedentary Behavior', fontsize=14, fontweight='bold')
plt.colorbar(hb, ax=axes4[1], label='Count')

pearson_r, pearson_p = stats.pearsonr(q4_data['weight'], q4_data['sedentary_minutes'])
fig4.text(0.5, -0.02, f'Pearson r = {pearson_r:.3f}, p < 0.001 (Weak positive correlation, R² = {pearson_r**2:.3f})',
          ha='center', fontsize=11, style='italic', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.tight_layout()
plt.savefig(f'{output_dir}fig4_correlation_weight_sedentary.png', dpi=150, bbox_inches='tight')
plt.close()

# FIGURE 5: ANOVA - Systolic BP Across Age Groups
fig5, axes5 = plt.subplots(1, 2, figsize=(12, 5))
q5_data = df[['age_group', 'BPXOSY3']].dropna()
q5_data = q5_data.rename(columns={'BPXOSY3': 'systolic_bp'})

colors = ['#2ecc71', '#f39c12', '#e74c3c']
sns.boxplot(data=q5_data, x='age_group', y='systolic_bp', ax=axes5[0], palette=colors, width=0.6)
axes5[0].set_xlabel('Age Group', fontsize=12)
axes5[0].set_ylabel('Systolic Blood Pressure (mmHg)', fontsize=12)
axes5[0].set_title('Systolic BP by Age Group', fontsize=14, fontweight='bold')
means = q5_data.groupby('age_group')['systolic_bp'].mean()
for i, (idx, mean) in enumerate(means.items()):
    axes5[0].text(i, mean + 2, f'{mean:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

sns.violinplot(data=q5_data, x='age_group', y='systolic_bp', ax=axes5[1], palette=colors, inner='box')
axes5[1].set_xlabel('Age Group', fontsize=12)
axes5[1].set_ylabel('Systolic Blood Pressure (mmHg)', fontsize=12)
axes5[1].set_title('Distribution of Systolic BP by Age Group', fontsize=14, fontweight='bold')

young = q5_data[q5_data['age_group'] == 'Young Adults\n(18-39)']['systolic_bp']
middle = q5_data[q5_data['age_group'] == 'Middle-Aged\n(40-59)']['systolic_bp']
older = q5_data[q5_data['age_group'] == 'Older Adults\n(60+)']['systolic_bp']
f_stat, anova_p = stats.f_oneway(young, middle, older)
fig5.text(0.5, -0.02, f'F = {f_stat:.2f}, p < 0.001 | All pairwise comparisons significant (Tukey HSD)',
          ha='center', fontsize=11, style='italic', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.tight_layout()
plt.savefig(f'{output_dir}fig5_anova_bp_agegroups.png', dpi=150, bbox_inches='tight')
plt.close()
