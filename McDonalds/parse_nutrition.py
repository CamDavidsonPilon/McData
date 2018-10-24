# parsepdfs
import camelot
import argparse
import pandas as pd
import glob
import os


COLUMNS = [
    "Item",
    "Serving Size",
    "Calories",
    "Calories From Fat",
    "Total Fat (g)",
    "Total Fat % Daily Value",
    "Saturated Fat (g)",
    "Saturated Fat % Daily Value",
    "Trans Fat (g)",
    "Cholesterol (mg)",
    "Cholesterol % Daily Value",
    "Sodium (mg)",
    "Sodium % Daily Value",
    "Carbohydrates (g)",
    "Carbohydrates % Daily Value",
    "Dietary Fiber (g)",
    "Dietary Fiber % Daily Value",
    "Sugars (g)",
    "Protein (g)",
    "Vitamin A % Daily Value",
    "Vitamin C % Daily Value",
    "Calcium % Daily Value",
    "Iron % Daily Value"
]

def parse_pdf(filename, output):
    print("Start reading %s" % filename)
    tables = camelot.read_pdf(filename, pages='1-end')
    print("Finish reading %s" % filename)

    accumulating_df = pd.DataFrame(columns=COLUMNS)

    for table in tables:

        df = table.df
        # cleaning.
        if df.shape[0] >= 3:
            # this is meaty content and not just header redundancy
            df = df.iloc[3:]
        else:
            continue

        # the last column is sometimes null
        try:
            df.columns = COLUMNS
        except:
            df = df.drop(df.columns[-1], axis=1)
            df.columns = COLUMNS
        accumulating_df = accumulating_df.append(df, ignore_index=True)


    # prune out header rows
    accumulating_df = accumulating_df.dropna(subset=['Serving Size'])
    # remove whitespace and footnote markers
    accumulating_df['Item'] = accumulating_df['Item'].str.strip("+ †®")

    timestamp = os.path.split(filename)[1].strip('.pdf')
    new_filename = output + timestamp + '.csv'
    print("Saving to %s" % new_filename)

    accumulating_df.to_csv(new_filename, index=False)
    return



if __name__ == "__main__":



    parser = argparse.ArgumentParser()
    parser.add_argument('folder')
    parser.add_argument('output_folder')
    parser.add_argument('--from-scratch', action='store_true')

    args = parser.parse_args()

    if args.from_scratch:
        for filename in sorted(glob.glob(args.folder + "*.pdf")):
            parse_pdf(filename, args.output_folder)

    else:
        # TODO
        parse_pdf(filename, args.output_folder)
