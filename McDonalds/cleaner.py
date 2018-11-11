import sqlite3
import pandas as pd


def clean_dataframe(df):

    # drop bad rows
    df = df.dropna(subset=['Item', 'Serving Size', 'Iron % Daily Value'])

    # create weight rows
    # first lstrip and rstrip brakcets
    serving_size = df['Serving Size']
    w1 = serving_size.str.extract('(?P<oz>\d+(?:\.\d)?) (?:fl )?oz(?:cup)?\((?P<grams>\d+) g\)')
    w2 = serving_size.str.extract('(?P<oz>\d+) fl oz(?:cup)?')
    w3 = serving_size.str.extract('\d ?(?:pkg|cookie)\((?P<grams>\d+(?:\.\d)?) g\)')
    w4 = serving_size.str.extract('(?P<oz>\d+(?:\.\d)?) (?:fl ?)?oz(?:cup)?')
    w5 = serving_size.str.extract('(?P<oz>\d+(?:\.\d)?) (?:fl ?)?oz(?:cup)?\((?P<ml>\d+) ml\)')

    w = w1.combine_first(w2).combine_first(w3).combine_first(w4).combine_first(w5)
    df = pd.concat([df, w], axis=1)

    # clean items
    df['Item'] = df['Item'].str.replace(' ', '')
    df['Item'] = df['Item'].str.replace('®', '')
    df['Item'] = df['Item'].str.replace('™', '')
    df['Item'] = df['Item'].str.replace('§', '')
    df['Item'] = df['Item'].str.replace('*', '')


    return df

def clean_all_dataframes():
    final_df = pd.DataFrame()

    csvs = glob.glob("*.csv")
    for csv in csvs:
        df = pd.read_csv(csv)
        df['file'] = csv
        final_df = final_df.append(clean_dataframe(df))

    return final_df


def load(df):
    df['index'] = df['Item'] + df['file']
    with sqlite3.connect('mcdata.db') as conn:
        df.to_sql("mcdonalds_nutrition", conn, index=False, index_label="index", if_exists='replace', chunksize=10000)


