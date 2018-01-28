# test script
from tabula import read_pdf
from subprocess import CalledProcessError
import pandas as pd
from glob import glob
import click

COLUMNS = [
    "Item",
    "Serving Size",
    "Calories",
    "Calories From Fat",
    "Total Fat (g)",
    "Total Fat % Daily Value**",
    "Saturated Fat (g)",
    "Saturated Fat % Daily Value**",
    "Trans Fat (g)",
    "Cholesterol (mg)",
    "Cholesterol % Daily Value**",
    "Sodium (mg)",
    "Sodium % Daily Value**",
    "Carbohydrates (g)",
    "Carbohydrates % Daily Value**",
    "Dietary Fiber (g)",
    "Dietary Fiber % Daily Value**",
    "Sugars (g)",
    "Protein (g)",
    "Vitamin A",
    "Vitamin C",
    "Calcium",
    "Iron"]


def extract_timestamp(path):
    _, _, timestamp_pdf = path.split("/")
    timestamp_as_string = timestamp_pdf.strip(".pdf")
    return pd.to_datetime(timestamp_as_string)


def extract_data_from_page(path, page):
    df = read_pdf(path, pages=page, lattice=True, guess=False, pandas_options={'skiprows': [0]}, silent=True)
    if df is None:
        return None
    df.columns = COLUMNS
    df['Item'] = df['Item'].str.replace("\r", " ")
    df['Item'] = df['Item'].str.replace('†', "")
    df['Item'] = df['Item'].str.replace('+', "")
    df['Item'] = df['Item'].str.replace('®', "")
    df['Item'] = df['Item'].str.replace('§', "")
    df['Item'] = df['Item'].str.replace('*', "")
    df['Item'] = df['Item'].str.strip()
    df['Serving Size'] = df['Serving Size'].str.replace("\r", " ")
    df['extracted_at'] = extract_timestamp(path)
    to_drop = pd.isnull(df['Calories'])
    df = df.loc[~to_drop]
    return df


def extract_data_from_pdf(path):
    df = pd.DataFrame(columns=COLUMNS)
    page = 1
    while True:
        try:
            print("  page: %d" % page)
            _df = extract_data_from_page(path, page)
        except CalledProcessError:
            break
        if _df is not None:
            df = df.append(_df)
        page += 1
    return df


@click.command()
@click.option('--input-path', help='Directory that contains the PDFs.')
@click.option('--output', help='The name of the csv file to save to.')
def main(input_path, output):
    df = pd.DataFrame(columns=COLUMNS)
    for pdf_count, pdf_path in enumerate(sorted(glob(input_path + "/*.pdf")), start=1):
        print(" PDF: %d" % pdf_count)
        df = df.append(extract_data_from_pdf(pdf_path))
        if pdf_count == 2:
            break
    df.to_csv(output, index=False)
    return

if __name__ == '__main__':
    main()

