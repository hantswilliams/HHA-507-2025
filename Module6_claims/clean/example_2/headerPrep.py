import pandas as pd 

df = pd.read_csv('data/examples/STONYBRK_20240531_HEADER.csv')

## print the first row of the dataframe with each column on a new line
print(df.iloc[0])

## print each column name
print(df.columns)



df_code = pd.read_csv('data/examples/STONYBRK_20240531_CODE.csv')

## print the first row of the dataframe with each column on a new line
print(df_code.iloc[0])

## print each column name
print(df_code.columns)



### proecdures: data/examples/STONYBRK_20240531_LINE.csv
df_line = pd.read_csv('data/examples/STONYBRK_20240531_LINE.csv')

## print the first row of the dataframe with each column on a new line
print(df_line.iloc[0])

## print each column name
print(df_line.columns)