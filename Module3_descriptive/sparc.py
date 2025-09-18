import pandas as pd 

url = 'https://health.data.ny.gov/resource/46xm-urtu.csv'

sparcs = pd.read_csv(url)
sparcs

sparcs.to_csv('sparc_data.csv', index=False )
sparcs.columns

sparcs['total_charges']
sparcs['total_costs']

## total_charges to numeric, remove , with whitespace
sparcs['total_charges_clean'] = sparcs['total_charges'].str.replace(',', '')
sparcs['total_charges_clean'] = pd.to_numeric(sparcs['total_charges_clean'], errors='coerce')
sparcs['total_charges_clean'].dtype

sparcs['total_costs_clean'] = sparcs['total_costs'].str.replace(',', '')
sparcs['total_costs_clean'] = pd.to_numeric(sparcs['total_costs_clean'], errors='coerce')
sparcs['total_costs_clean'].dtype

sparcs_costs = sparcs[['total_charges_clean', 'total_costs_clean']]
sparcs_costs_descriptives = sparcs_costs.describe()
sparcs_costs_descriptives.to_csv('sparcs_costs_descriptives.csv')

