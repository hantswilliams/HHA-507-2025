import pandas as pd
from sqlalchemy import create_engine
import gc # garbage collector

## load in .sql file as string:
with open('Module2_dbs/patient_query.sql', 'r') as file:
    sql_depression_query = file.read()


db_location = 'patients.db'

engine = create_engine(f'sqlite:///{db_location}')

patients_df = pd.read_csv('assignments/assignment2_files/patients.csv')

patients_df.to_sql('patients_diseases', con=engine, if_exists='replace', index=False)

query_anxiety = "select * from patients_diseases WHERE primary_icd10 = 'F41.9'"

results_df = pd.read_sql_query(query_anxiety, con=engine)
len(results_df)



results_loaded_sql_file1 = pd.read_sql_query(sql_depression_query, con=engine)

len(results_loaded_sql_file1)

