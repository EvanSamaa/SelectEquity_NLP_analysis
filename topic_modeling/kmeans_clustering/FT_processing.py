import pandas as pd


df = pd.read_csv('FT_all_between_5and6.csv', index_col=["date"], usecols=["date", "title"])

# remove nan
df = df.dropna()

# remove rows that are semantically invalid
df = df[~df.title.str.contains("FT|Letter|Monday, |Tuesday, |Wednesday, |Thursday, |Friday, |Cartoon, |Further reading")]

df.to_csv('FT_all_between_5and6_title.csv')