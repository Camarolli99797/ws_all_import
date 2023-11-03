import pandas as pd
import requests
from io import StringIO

# Function to download CSV from a given URL
def download_csv(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text), delimiter='|', quotechar='"', on_bad_lines='skip')
    else:
        print("Failed to download the file. Status Code:", response.status_code)
        return None

# Function to fill empty cells in the DataFrame
def fill_empty_cells(df):
    for column in df.columns:
        df[column] = df[column].fillna(method='ffill')
    print("Empty cells filled successfully!")

# Function to transform the CSV data
def transform_csv(df, output_file):
    try:
        # Print the first few rows of the DataFrame (for debugging)
        print("First few rows of the original DataFrame:")
        print(df.head())

        # Fill empty cells
        fill_empty_cells(df)

        # Adding a new column with a default value
        df['new_column'] = "DEFAULT VALUE"

        # Convert text to uppercase
        for column in df.columns:
            if df[column].dtype == 'object':
                df[column] = df[column].apply(lambda x: str(x).upper())

        # Save the transformed DataFrame to a new CSV file
        df.to_csv(output_file, index=False)
        print("Data transformation successful! Transformed file saved as '{}'".format(output_file))

        # Print the first few rows of the transformed DataFrame (for debugging)
        print("First few rows of the transformed DataFrame:")
        print(df.head())

    except Exception as e:
        print("An error occurred:", str(e))

# Function to remove rows where RECORD_TYPE is not 'MODEL'
def filter_record_type(df):
    return df[df['RECORD_TYPE'] == 'MODEL']

# Function to add a column 'VEZNIK' that copies text from 'SKU' until it reaches '_' or '-'
def add_veznik_column(df):
    df.loc[:, 'VEZNIK'] = df['SKU'].apply(lambda x: str(x).split('_')[0].split('-')[0])
    print("VEZNIK column added successfully!")

# Main execution
if __name__ == "__main__":
    # URL of the CSV file
    url = "https://feed.stockfirmati.com/csv/exportdropclang.csv"

    # Output file names
    output_file = "transformed_file.csv"
    output_file_modified = "transformed_file_modified.csv"

    # Download the CSV file and load it into a DataFrame
    df = download_csv(url)
    if df is not None:
        # Transform the CSV file
        transform_csv(df, output_file)

        # Filter DataFrame to keep only rows where RECORD_TYPE is 'MODEL'
        df_model = filter_record_type(df)

        # Add 'VEZNIK' column
        add_veznik_column(df_model)

        # List of columns to remove
        columns_to_remove = [
            'Titel_ITA', 'Description_ITA',
            'Titel_ES', 'Description_ES',
            'Titel_FR', 'Description_FR',
            'Titel_DE', 'Description_DE',
            'Titel_BG', 'Description_BG',
            'Titel_PL', 'Description_PL',
            'Titel_CZ', 'Description_CZ',
            'Titel_SK', 'Description_SK',
            'Titel_HU', 'Description_HU',
            'Titel_RO', 'Description_RO'
        ]

        # Remove the specified columns
        df_model.drop(columns=columns_to_remove, inplace=True)

        # Save the modified DataFrame to a new CSV file
        try:
            df_model.to_csv(output_file_modified, index=False)
            print("Modified DataFrame saved as '{}'".format(output_file_modified))
        except PermissionError:
            print("Permission denied: Could not save '{}'. Please make sure the file is not open in another program and that you have write permissions to the directory.".format(output_file_modified))
        except Exception as e:
            print("An error occurred while saving the file:", str(e))