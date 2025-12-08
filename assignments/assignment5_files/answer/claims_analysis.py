"""
Healthcare Claims Data Analysis - Stony Brook University Hospital
Analyzes claims data from May 2024 for billing patterns, diagnoses, procedures, and payer relationships.
"""

import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')

# DATA LOADING
data_dir = '../../../Module6_claims/clean/example_2'
df_header = pd.read_csv(f'{data_dir}/STONYBRK_20240531_HEADER.csv')
df_line = pd.read_csv(f'{data_dir}/STONYBRK_20240531_LINE.csv')
df_code = pd.read_csv(f'{data_dir}/STONYBRK_20240531_CODE.csv')
df_header['ServiceFromDate'] = pd.to_datetime(df_header['ServiceFromDate'])
df_header['ServiceToDate'] = pd.to_datetime(df_header['ServiceToDate'])

# PART 1: DATA EXPLORATION
n_claims = df_header['ProspectiveClaimId'].nunique()
date_range = f"{df_header['ServiceFromDate'].min().strftime('%Y-%m-%d')} to {df_header['ServiceFromDate'].max().strftime('%Y-%m-%d')}"
avg_lines_per_claim = df_line.groupby('ProspectiveClaimId').size().mean()
avg_dx_per_claim = df_code.groupby('ProspectiveClaimId').size().mean()

# PART 2: RELATIONAL DATA ANALYSIS
# Q1: Top 5 Billing Providers
top_providers = df_header.groupby(['BillingProviderNPI', 'BillingProvFirstName']).size().reset_index(name='ClaimCount')
top_providers = top_providers.sort_values('ClaimCount', ascending=False).head(5)

# Q2: Payer Mix
payer_counts = df_header['PrimaryPayerName'].value_counts()
payer_pct = (payer_counts / len(df_header) * 100).round(2)
top_payers = pd.DataFrame({'Claims': payer_counts, 'Percentage': payer_pct}).head(5)

# Q3: Top 10 Diagnoses
top_dx = df_code['CodeValue'].value_counts().head(10)

# Q4: Top 10 Procedures
top_hcpcs = df_line.groupby(['HCPCS', 'ClientProcedureName']).size().reset_index(name='Count')
top_hcpcs = top_hcpcs.sort_values('Count', ascending=False).head(10)

# Q5: Place of Service
pos_counts = df_header['PlaceOfService'].value_counts()
pos_pct = (pos_counts / len(df_header) * 100).round(2)
pos_df = pd.DataFrame({'Claims': pos_counts, 'Percentage': pos_pct})

# PART 3: ADVANCED ANALYSIS WITH JOINS
# Q6: Claims with High Service Line Counts
lines_per_claim = df_line.groupby('ProspectiveClaimId').agg(
    LineCount=('LinePos', 'count'),
    TotalCharges=('Charges', 'sum')
).reset_index()
high_lines = lines_per_claim[lines_per_claim['LineCount'] >= 5]
high_lines = high_lines.merge(df_header[['ProspectiveClaimId', 'BillingProvFirstName']], on='ProspectiveClaimId')
high_lines = high_lines.sort_values('LineCount', ascending=False)

# Q7: Diagnosis-Procedure Combinations for CPT 99291
cpt_99291_claims = df_line[df_line['HCPCS'] == '99291']['ProspectiveClaimId'].unique()
dx_for_99291 = df_code[df_code['ProspectiveClaimId'].isin(cpt_99291_claims)]
top_dx_99291 = dx_for_99291['CodeValue'].value_counts().head(10)

# Q8: Charges by Payer
header_line = df_header.merge(df_line, on='ProspectiveClaimId')
charges_by_payer = header_line.groupby('PrimaryPayerName').agg(
    TotalCharges=('Charges', 'sum'),
    AvgCharges=('Charges', 'mean'),
    ClaimCount=('ProspectiveClaimId', 'nunique')
).reset_index()
charges_by_payer = charges_by_payer.sort_values('TotalCharges', ascending=False).head(10)

# PART 4: CREATIVE ANALYSIS (Q9)
# Q9: Provider Complexity Analysis
dx_per_claim = df_code.groupby('ProspectiveClaimId').size().reset_index(name='DxCount')
header_dx = df_header.merge(dx_per_claim, on='ProspectiveClaimId')
provider_complexity = header_dx.groupby(['BillingProviderNPI', 'BillingProvFirstName']).agg(
    AvgDxCount=('DxCount', 'mean'),
    ClaimCount=('ProspectiveClaimId', 'count')
).reset_index()
provider_complexity = provider_complexity[provider_complexity['ClaimCount'] >= 5]
provider_complexity = provider_complexity.sort_values('AvgDxCount', ascending=False)

# VISUALIZATIONS
output_dir = './'

# Figure 1: Top 5 Billing Providers
fig1, ax1 = plt.subplots(figsize=(10, 5))
top_prov = df_header.groupby('BillingProvFirstName').size().sort_values(ascending=False).head(5)
bars = ax1.barh(top_prov.index[::-1], top_prov.values[::-1], color='steelblue', edgecolor='black')
ax1.set_xlabel('Number of Claims', fontsize=12)
ax1.set_title('Q1: Top 5 Billing Providers by Claim Count', fontsize=14, fontweight='bold')
for bar, val in zip(bars, top_prov.values[::-1]):
    ax1.text(val + 1, bar.get_y() + bar.get_height()/2, str(val), va='center', fontsize=10)
plt.tight_layout()
plt.savefig(f'{output_dir}fig1_top_providers.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 2: Payer Mix
fig2, ax2 = plt.subplots(figsize=(10, 5))
payer_top5 = df_header['PrimaryPayerName'].value_counts().head(5)
colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
bars = ax2.barh(payer_top5.index[::-1], payer_top5.values[::-1], color=colors[::-1], edgecolor='black')
ax2.set_xlabel('Number of Claims', fontsize=12)
ax2.set_title('Q2: Top 5 Primary Payers by Claim Volume', fontsize=14, fontweight='bold')
for bar, val in zip(bars, payer_top5.values[::-1]):
    pct = val / len(df_header) * 100
    ax2.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val} ({pct:.1f}%)', va='center', fontsize=10)
plt.tight_layout()
plt.savefig(f'{output_dir}fig2_payer_mix.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 3: Top 10 Diagnosis Codes
fig3, ax3 = plt.subplots(figsize=(10, 6))
top_dx_plot = df_code['CodeValue'].value_counts().head(10)
bars = ax3.barh(top_dx_plot.index[::-1], top_dx_plot.values[::-1], color='coral', edgecolor='black')
ax3.set_xlabel('Frequency', fontsize=12)
ax3.set_title('Q3: Top 10 Diagnosis Codes (ICD-10)', fontsize=14, fontweight='bold')
for bar, val in zip(bars, top_dx_plot.values[::-1]):
    ax3.text(val + 0.5, bar.get_y() + bar.get_height()/2, str(val), va='center', fontsize=10)
plt.tight_layout()
plt.savefig(f'{output_dir}fig3_top_diagnoses.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 4: Top 10 Procedures
fig4, ax4 = plt.subplots(figsize=(10, 6))
top_proc = df_line['HCPCS'].value_counts().head(10)
bars = ax4.barh(top_proc.index[::-1], top_proc.values[::-1], color='mediumseagreen', edgecolor='black')
ax4.set_xlabel('Frequency', fontsize=12)
ax4.set_title('Q4: Top 10 Procedure Codes (HCPCS/CPT)', fontsize=14, fontweight='bold')
for bar, val in zip(bars, top_proc.values[::-1]):
    ax4.text(val + 0.5, bar.get_y() + bar.get_height()/2, str(val), va='center', fontsize=10)
plt.tight_layout()
plt.savefig(f'{output_dir}fig4_top_procedures.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 5: Place of Service
fig5, ax5 = plt.subplots(figsize=(8, 5))
pos_data = df_header['PlaceOfService'].value_counts()
colors_pos = ['#3498db', '#e74c3c', '#2ecc71']
ax5.pie(pos_data, labels=pos_data.index, autopct='%1.1f%%', colors=colors_pos[:len(pos_data)], startangle=90)
ax5.set_title('Q5: Claims by Place of Service', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{output_dir}fig5_place_of_service.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 6: Charges by Payer
fig6, ax6 = plt.subplots(figsize=(12, 6))
header_line_raw = df_header.merge(df_line, on='ProspectiveClaimId')
charges_raw = header_line_raw.groupby('PrimaryPayerName')['Charges'].sum().sort_values(ascending=False).head(10)
ax6.barh(charges_raw.index[::-1], charges_raw.values[::-1], color='darkorange', edgecolor='black')
ax6.set_xlabel('Total Charges ($)', fontsize=12)
ax6.set_title('Q8: Total Charges by Payer (Top 10)', fontsize=14, fontweight='bold')
ax6.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.tight_layout()
plt.savefig(f'{output_dir}fig6_charges_by_payer.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 7: Provider Complexity
fig7, ax7 = plt.subplots(figsize=(10, 6))
prov_complex = header_dx.groupby('BillingProvFirstName').agg(
    AvgDxCount=('DxCount', 'mean'),
    ClaimCount=('ProspectiveClaimId', 'count')
).reset_index()
prov_complex = prov_complex[prov_complex['ClaimCount'] >= 5].sort_values('AvgDxCount', ascending=False)
scatter = ax7.scatter(prov_complex['ClaimCount'], prov_complex['AvgDxCount'],
                      s=100, c=prov_complex['AvgDxCount'], cmap='RdYlGn_r', edgecolor='black', alpha=0.7)
ax7.set_xlabel('Number of Claims', fontsize=12)
ax7.set_ylabel('Average Diagnosis Codes per Claim', fontsize=12)
ax7.set_title('Q9: Provider Complexity (Avg Dx per Claim vs Claim Volume)', fontsize=14, fontweight='bold')
plt.colorbar(scatter, ax=ax7, label='Avg Dx Count')
for _, row in prov_complex.head(3).iterrows():
    ax7.annotate(row['BillingProvFirstName'][:20], (row['ClaimCount'], row['AvgDxCount']),
                 xytext=(5, 5), textcoords='offset points', fontsize=8)
plt.tight_layout()
plt.savefig(f'{output_dir}fig7_provider_complexity.png', dpi=150, bbox_inches='tight')
plt.close()
