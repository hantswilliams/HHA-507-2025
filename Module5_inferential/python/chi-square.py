import pandas as pd 
from scipy.stats import chi2_contingency

df = pd.read_csv('Module5_inferential/data/cms-npi-ordering/OrderReferring_20250929.csv') # noqa

df['HHA'].value_counts()
df['PARTB'].value_counts()

contingency_table = pd.crosstab(df['PARTB'], df['HHA'])
print(contingency_table)

chi2, p, _, _ = chi2_contingency(contingency_table)
print(f"Chi2 value: {chi2}")
print(f"P-value: {p}")