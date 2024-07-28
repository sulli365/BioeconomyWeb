import pickle
import json
import dotenv # pip install python-dotenv
import os
dotenv.load_dotenv()  #(dotenv_path='/.venv/.env')

import pandas as pd
import numpy as np


raw_company_list_path = "C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/2024-07-28 raw company list utf8.csv"

raw_company_list = pd.read_csv(filepath_or_buffer=raw_company_list_path, header=0, skipinitialspace=True, on_bad_lines='warn')

# Getting an error that utf8 can't decode a byte in position 396 - invalid start byte...not even sure how to fix this...
# Moved forward by re-saving the csv as UTF8 csv in excel