import pickle
import os
import dotenv
import pandas as pd
import numpy as np

from tavily import TavilyClient # pip install tavily-python

from google.maps import places_v1
import json

from openai import OpenAI
from pydantic import BaseModel, Field # pip install pydantic
import requests # necessary?

dotenv.load_dotenv()


# BRING IN EXISTING BIOECONOMY CSV AS DATAFRAME

current_bioeconomy_df = pd.read_csv(
    filepath_or_buffer="C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/current_bioeconomy_df - Copy.csv",
    header=0,
    skipinitialspace=True,
    on_bad_lines='warn',
    encoding= 'latin-1'
    )

# convert columns to lists for company checking

names = list(current_bioeconomy_df['Name'])
# keywords = list(current_bioeconomy_df['Keywords'])
# descriptions = list(current_bioeconomy_df['Description'])
# links = list(current_bioeconomy_df['Link'])
# addresses = list(current_bioeconomy_df['Address'])
# placesIDs = list(current_bioeconomy_df['PlacesID'])
# latitudes = list(current_bioeconomy_df['Latitude'])
# longitudes = list(current_bioeconomy_df['Longitude'])

# BRING IN WEB_INFO DICT

with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/current_web_info_dict - Copy.pkl", 'rb') as f:
    current_web_info_dict = pickle.load(f)

# BRING IN LOCATION_INFO DICT

with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/current_location_info_dict - Copy.pkl", 'rb') as f:
    current_location_info_dict = pickle.load(f)

# BRING IN LLM_PARSE DICT

with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/current_company_LLM_parse_dict - Copy.pkl", 'rb') as f:
    current_company_LLM_parse_dict = pickle.load(f)