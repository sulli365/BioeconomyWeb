import pickle
import json
import dotenv # pip install python-dotenv
import os
dotenv.load_dotenv()  #(dotenv_path='/.venv/.env')

import pandas as pd
import numpy as np


raw_company_list_path = "C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/2024-07-28 raw company list.csv"

raw_company_list = pd.read_csv(filepath_or_buffer=raw_company_list_path, sheet_name = "Sheet1")