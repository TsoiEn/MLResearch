import pandas as pd

def load_dataset(file_path):
    """
    Load the dataset from a CSV file into a Pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The loaded dataset.
    """
    return pd.read_csv(file_path)

def save_dataset(dataframe, file_path):
    """
    Save the processed data to a CSV file.

    Parameters:
    dataframe (pd.DataFrame): The DataFrame to save.
    file_path (str): The path to the CSV file.

    Returns:
    None
    """
    dataframe.to_csv(file_path, index=False)