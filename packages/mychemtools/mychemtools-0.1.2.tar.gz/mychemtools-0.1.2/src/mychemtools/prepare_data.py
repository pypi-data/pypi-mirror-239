import pandas as pd
from datasets import Dataset, DatasetDict

def read_xlsx_drug_data(file_path):

  xls = pd.ExcelFile(file_path, engine="openpyxl")

  dataframes = {}

  for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name, engine="openpyxl")
    dataframes[sheet_name] = df

  return dataframes


def convert_dataframe_to_dataset(dataframes):
  
  dataset_dict = {}

  for split, df in dataframes.items():
    dataset_dict[split] = Dataset.from_pandas(df)

  dataset_dict = DatasetDict(dataset_dict)
  return dataset_dict

#file_path = "~/Downloads/drug_data.xlsx"
#result = read_xlsx_drug_data(file_path)
#dataset = convert_dataframe_to_dataset(result)
#print (dataset)