import pandas as pd


# helper functions - could be moved to utils file
def convert_xlsx_to_csv(path_to_file: str) -> str:
    file = pd.read_excel(path_to_file)
    csv_file_name: str = ''.join(path_to_file.split('.')[:-1]) + '.csv'
    file.to_csv(csv_file_name)
    return csv_file_name
