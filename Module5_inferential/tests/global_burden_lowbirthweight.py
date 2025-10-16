import pandas as pd 
import scipy.stats as stats

df = pd.read_csv("Module5_inferential/data/prevalence-global-diseases/IHME_GBD_2023_RISK_EXPOSURE_NEONATAL_PRETERM_AND_LBWSG_24_26_WKS_500_1000_G_Y2025M10D10.CSV")

df['age_group_name'].value_counts()

"""

Research question 1: is there a difference in the mean prevalence of 
low birth weight, between male and females globally? 

"""



### WRONG WAY - because we would be double counting countries with multiple entries (e.g., global includes eastern, western etc...)

sex = df[['sex', 'mean']]

male_values = sex[sex['sex'] == 'Male']['mean']
female_values = sex[sex['sex'] == 'Female']['mean']

## t-test
t_stat, p_value = stats.ttest_ind(male_values, female_values, equal_var=False)


### RIGHT WAY - filter where location is global and age group is age standardized
country_global_age_stnd = df[(df['location_name'] == 'Global') & (df['age_group_name'] == 'Age-standardized')]
# country_global_age_stnd.to_csv("Module5_inferential/tests/global_burden_lowbirthweight_global_age_stnd.csv", index=False)

male_values = country_global_age_stnd[country_global_age_stnd['sex'] == 'Male']['mean']
female_values = country_global_age_stnd[country_global_age_stnd['sex'] == 'Female']['mean']

## t-test
output = stats.ttest_ind(male_values, female_values, equal_var=False)

output1, output2 = stats.ttest_ind(male_values, female_values, equal_var=False)