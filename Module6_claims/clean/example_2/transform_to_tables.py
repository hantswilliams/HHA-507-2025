import pandas as pd 

## load in .txt file to df: data/examples/STONYBRK_20240531_CODE.txt that is | delimited
df = pd.read_csv('data/examples/STONYBRK_20240531_CODE.txt', sep='|')
df.to_csv('data/examples/STONYBRK_20240531_CODE.csv', index=False)

## load in .txt file to df: data/examples/STONYBRK_20240531_LINE.txt that is | delimited
df = pd.read_csv('data/examples/STONYBRK_20240531_LINE.txt', sep='|')
df.to_csv('data/examples/STONYBRK_20240531_LINE.csv', index=False)

