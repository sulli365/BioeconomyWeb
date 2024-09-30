# Goal of this script is to set up "Current" (2024-09-22) versions of dicts to align with all-in-one pipeline

# - Current_bioeconomy_df - initializing fresh
# 	• Has columns Name, Keywords, Description, Link, Address, PlacesID, Latitude, Longitude
# - Current_web_info_dict - 2024-08-18 full_tavily_dict - Copy.pkl
# - Current_location_info_dict - 2024-07-28 company_loc_only_df.pkl
# 		- Need to quickly convert this to a dict. First column is name, rest is correct (except for column order)
# 		- Has 810 entries - this is probably everything...could match up to existing
# - Current_LLM_parse_dict - synbio_web_companies_and_info_df - Copy.pkl
#   - ALso needs to be converted to a dict



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

# current_bioeconomy_df = pd.read_csv(
#     filepath_or_buffer="C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/current_bioeconomy_df - Copy.csv",
#     header=0,
#     skipinitialspace=True,
#     on_bad_lines='warn',
#     encoding= 'ut'
#     )

# convert columns to lists for company checking

# names = list(current_bioeconomy_df['Name'])
# keywords = list(current_bioeconomy_df['Keywords'])
# descriptions = list(current_bioeconomy_df['Description'])
# links = list(current_bioeconomy_df['Link'])
# addresses = list(current_bioeconomy_df['Address'])
# placesIDs = list(current_bioeconomy_df['PlacesID'])
# latitudes = list(current_bioeconomy_df['Latitude'])
# longitudes = list(current_bioeconomy_df['Longitude'])

# BRING IN WEB_INFO DICT

# with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/2024-08-18 full_tavily_dict - Copy.pkl", 'rb') as f:
#     current_web_info_dict = pickle.load(f)

# dict with 775 keys

# with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/current_web_info_dict.pkl", 'rb') as f:
#     current_web_info_dict = pickle.load(f)



# BRING IN LOCATION_INFO DICT

# with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/2024-07-28 company_loc_only_df - Copy.pkl", 'rb') as f:
#     current_location_info_dict = pickle.load(f)



# pandas dataframe with 810 rows, 5 columns --> great!

# with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/2024-07-28 company_loc_only_df - Copy.pkl", 'rb') as f:
#     current_location_info_dict = pickle.load(f)

# with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/current_location_info_dict.pkl", 'rb') as f:
#     current_location_info_dict = pickle.load(f)

# BRING IN LLM_PARSE DICT

# with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/current_company_LLM_parse_dict.pkl", 'rb') as f:
#     current_company_LLM_parse_dict = pickle.load(f)

# current_company_LLM_parse_dict = pd.compat.pickle_compat.load("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/synbio_web_companies_and_info_df - Copy.pkl")

# current_company_LLM_parse_dict = pd.read_pickle("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/synbio_web_companies_and_info_df - Copy.pkl")
# issues with pickling df...use dict only?
# other solution was to install previous version of pickle...not ideal for me

# pandas dataframe with 568 rows, 4 columns --> great! but needs updating



# NEED TO CONVERT LOCATION INFO STRUCT (DATAFRAME) TO DICT 
# 1ST COLUMN IS NAME, COL2 = PLACESID, COL3 = ADDRESS, COL4 = LAT, COL5 = LON
# WANT TO SWITCH COL2 + COL3

# current_location_info_dict = current_location_info_dict[['Name','Address','PlacesID','Latitude','Longitude']]

# location_info_names = list(current_location_info_dict['Name'])

# location_dict2 = dict(zip(current_location_info_dict['Name'], current_location_info_dict[['Address', 'PlacesID', 'Latitude', 'Longitude']].values.tolist()))

# now this is a Python dict with 774 keys --> there are now fewer keys though...maybe there were duplicates?
# confirmed using len(list(set(location_info_names)))


# NEED TO CONVERT current company LLM parse STRUCT (DATAFRAME) TO DICT 

#  LLM_parse_names = current_company_LLM_parse_dict['Name']

# 568 rows

#  LLM_parse_dict2 = dict(zip(current_company_LLM_parse_dict['Name'], current_company_LLM_parse_dict[['Keywords', 'Description', 'Link']].values.tolist()))

# dict with 553 keys --> again lost some,looking for duplicates --> confirmed...how am i getting so many duplicates?

# Check bioeconomy_df --> still has 810 rows... --> going to work off a freshly initialized df --> csv

# current_bioeconomy_df = pd.DataFrame(
#     data = None,
#     index = None,
#     columns = ['Name','Keywords','Description','Link','Address','PlacesID','Latitude','Longitude']
# )


# # WRITE THE NEW SET OF DICTS TO PKL FILES I GUESS

# with open('C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/current_web_info_dict.pkl', 'wb') as f:
#     pickle.dump(current_web_info_dict, f)

# with open('C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/current_location_info_dict.pkl', 'wb') as f:
#     pickle.dump(location_dict2, f)

# with open('C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/current_company_LLM_parse_dict.pkl', 'wb') as f:
#     pickle.dump(LLM_parse_dict2, f)

# current_bioeconomy_df.to_csv(
#     path_or_buf="C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/current_bioeconomy_df.csv",
#     sep=',',
#     index=False,
#     encoding= 'latin-1'
#     )



###################################################

# with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/current_company_LLM_parse_dict.pkl", 'rb') as f:
#     current_company_LLM_parse_dict = pickle.load(f)

# llm_keys = current_company_LLM_parse_dict.keys()

# no_llm_parse_df = pd.DataFrame(
#     data=None,
#     index=None,
#     columns=['Name']
# )

# new_dict = dict()

# for key in llm_keys:

#     entry = current_company_LLM_parse_dict[key]

#     curr_list = current_company_LLM_parse_dict[key][0]

#     if len(curr_list) < 2:

#         no_llm_parse_df.loc[len(no_llm_parse_df)] = key

#         continue

#     elif type(curr_list) == str:
 
#         newlist = curr_list.split(",")
#         newlist2 = [sol.lstrip() for sol in newlist]
#         newlist3 = [sol.title() for sol in newlist2]

#         new_dict[key] = [newlist3, entry[1], entry[2]]

#     elif type(curr_list) == list:

#         newlist = [words.lstrip() for words in curr_list]
#         newlist2 = [words.title() for words in newlist]

#         new_dict[key] = [newlist2, entry[1], entry[2]]


# with open('C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/test_llm_parse_dict.pkl', 'wb') as f:
#     pickle.dump(new_dict, f)

# no_llm_parse_df.to_csv(
#     path_or_buf="C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/no_llm_parse_df.csv",
#     sep=',',
#     index=False,
#     encoding= 'utf_8_sig' # 'latin-1'
#     )

################################

# with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/test_llm_parse_dict.pkl", 'rb') as f:
#     test_llm_parse_dict = pickle.load(f)


# llm_keys = test_llm_parse_dict.keys()

# for key in llm_keys:

#     curr_list = test_llm_parse_dict[key][0]
#     print(curr_list)


######################################

# with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/current_company_LLM_parse_dict.pkl", 'rb') as f:
#     current_company_LLM_parse_dict = pickle.load(f)

# llm_keys = list(current_company_LLM_parse_dict.keys())

# with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/test_llm_parse_dict.pkl", 'rb') as f:
#     test_llm_parse_dict = pickle.load(f)

# llm_keys2 = list(test_llm_parse_dict.keys())


info_df = pd.read_csv(
        filepath_or_buffer="C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/Current/2024-09-27 current_bioeconomy_df.csv",
        header=0,
        skipinitialspace=True,
        on_bad_lines='warn',
        # dtype= str,
        # converters = {'Keywords' : list, 'Latitude': float, 'Longitude': float},
        encoding= 'utf_8_sig'
    )

# multi_options = list(info_df['Keywords'])

multi_options1 = [wordlist[1:-1].split(', ') for wordlist in info_df['Keywords']]

multi_options2 =[]

for wordlist in multi_options1:
    for entry in wordlist:
        multi_options2.append(entry[1:-1])

# multi_options = [wordlist[1:-1].split(', ') for wordlist in info_df['Keywords']]

# multi_options = [words.split(', ') for words in multi_options]

# multi_options = [words[1:-1] for words in multi_options]


# multi_options = [keywords.split(', ') for keywords in multi_options]

# multi_options = [info_df['Keywords'].apply(lambda x: (x.split(', ') for x in info_df['Keywords']))]

# info_df[info_df['Keywords'].apply(lambda x: any(keyword in x for keyword in multi_choices))]

# multi_options = [word.split(', ') for keyword_lists in info_df['Keywords']]

# multi_options = [word for keywords_list in info_df['Keywords'] for word in keywords_list]