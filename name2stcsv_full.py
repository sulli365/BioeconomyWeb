'''
This script contains efforts to build a full company processing pipeline - 
takes in a name or a list of names and returns a csv containing all of the relevant info.
The output of the function is a csv that can then be easily imported into Streamlit.

The columns of the final csv will be:
- Name, Keywords, Description, Link, Address, PlacesID, Latitude, Longitude

The script will loop through the company list and, for each company, will check if web_info, 
LLM_parse, and location_info are present in the existing data structures. If not, the pipeline
will call functions to generate that info/data before proceeding to the next step.

ALERT: THIS WILL LIKELY REQUIRE MAKING SURE THAT I HAVE APPROPRIATE OUTPUTS CODED AT EACH STEP
TO IDENTIFY IF SOMETHING SOMEHOW SLIPPED THROUGH...WILL HAVE VALUES RETURN 'empty' SO I CAN CHECK FOR THAT STRING.

To do this, I will have web_info, LLM_parse, and location_info saved as dicts so that I can identify
whether no info is present via KeyErrors.

I will also check the values in the individual csv columns so that even data exists in the relevant
dict for a given company, I can go back later and troubleshoot why it didn't produce the desired output. I will write a separate csv
file that captures wehther the values are 'good' or 'bad'.

Other things to do:
- implement time-stamping for bioeconomy csv to save file

'''

DONT RUN UNTIL IVE MADE SURE THAT CURRENT COMPANY LIST AND NEW COMPANY CAN BE COMPARED AND SO NOTHING
IS OVERWRITTEN UNNECESSARILY

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


# BRING IN THE 'NEW' COMPANY LIST TO BE PROCESSED AS A DATAFRAME, HEADER MUST BE 'NAME'

raw_company_list_df = pd.read_csv(
    filepath_or_buffer="C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/2024-07-28 raw company list.csv",
    header=0,
    skipinitialspace=True,
    on_bad_lines='warn',
    encoding= 'latin-1'
    )

# convert names to list and drop duplicates
raw_company_list = list(raw_company_list_df['Name'].unique())


# BRING IN EXISTING BIOECONOMY CSV AS DATAFRAME

current_bioeconomy_df = pd.read_csv(
    filepath_or_buffer="C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/current_bioeconomy_df - Copy.csv",
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


# BRING IN TROUBLESHOOTING CSV AS DATAFRAME

# current_troubleshooting_df = pd.read_csv(
#     filepath_or_buffer="C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/current_troubleshooting_df - Copy.csv",
#     header=0,
#     skipinitialspace=True,
#     on_bad_lines='warn',
#     encoding= 'latin-1'
#     )


# DEFINE FUNCTIONS FOR GATHERING WEB_INFO, LOCATION_INFO, LLM_PARSE
# NEED TO MAKE IT SO THAT FAILED OUTPUTS RETURN 'empty'

def get_web_info(company_name):

    tavily_api_key = os.getenv('TAVILY_API_KEY_sfs', 'None')
    tavily = TavilyClient(api_key=tavily_api_key)

    tav_query_final = "Describe what " + company_name + " does, including its objectives, location, the industries and markets in which it operates, and any differentiating characteristics relative to other companies in a similar space."

    company_name_tavily_output = tavily.search(
        query = tav_query_final,
        search_depth="advanced",
        max_results=10
        )
    
    return company_name_tavily_output


def get_location_info(company_name):

    places_api_key = os.getenv('bioeconomyweb_google_api_key', 'None')

    # Create a client
    client = places_v1.PlacesClient(
    client_options={"api_key": places_api_key}
    )

    # Initialize request argument(s)
    request = places_v1.SearchTextRequest(
        # text_query="text_query_value", # original query
        text_query=company_name
    )

    fieldMask = "places.id,places.formattedAddress,places.location" #places.location.latitude,places.location.longitude"        # "*" - returns all fields

    # Make the request
    places_api_out = client.search_text(
        request=request,
        metadata=[("x-goog-fieldmask",fieldMask)] # Figuring this out sucked btw, the fact that you need this 'fieldMask' param
        )

    # Going to parse the output so that it becomes a list: formatted address, placesID, latitude, longitude
    
    if places_api_out.places == []:

        places_out_list = [
            "Unknown", 
            "Unknown",
            "Unknown",
            "Unknown"
        ]

    else:

        places_out_list = [
            places_api_out.places[0].formatted_address,
            places_api_out.places[0].id,            
            places_api_out.places[0].location.latitude,
            places_api_out.places[0].location.longitude
        ]

    return places_out_list



def get_LLM_parse(company_name, web_info_dict):
    """
    Uses OpenAI's API to turn information scraped from the web into a structured output containing 
    useful information that will then be used ot make the Streamlit map.


    Args:
    company_name (string) and the full web_info_dict (dict): A dictionary all company names and 
    their associated web information.

    Returns:
    If successful: a list containing company name, keywords, description, and URL.

    If unsuccessful (error message): a list containing 'empty', 'empty', 'empty', 'empty'. Later on I will implement better error messages.
    """
    # Grab web_info for company
    company_web_info = web_info_dict[company_name]
    result_list = company_web_info['results']

    # Generate prompt context by extract most important web info
    prompt_text_list = []

    for source in result_list:

        prompt_text_list.append(source['url'])
        prompt_text_list.append(source['content']) 
    
    company_prompt = '\n'.join(prompt_text_list)


    # Define a Pydantic class to capture the desired output of the LLM call
    class Profile(BaseModel):
        company_name: str = Field(description = "the name of the company")
        company_purpose_keywords: str = Field(description = "3-4 keywords that describe the industry and/or market served by the company")
        url_link: str = Field(description = "the url for the organization's website")
        company_description: str = Field(description = "a description of between 150 and 300 words of what the organization does and what markets it operates in.")

    # Define an LLM model
    client = OpenAI(
      api_key = os.getenv('bioeconomyweb_openai_api_key', 'None')
    )

    # Construct the prompt for the LLM
    system_prompt = f"You are helpful assistant. Using the provided information delimited by triple quotes, for the company or organization named {company_name}, return the organization's name, 3-4 keywords that describe the industry and/or market served by {company_name}, the url for the organization's website, and a brief description of what the organization does and what markets it operates in. If the answer cannot be found in the information provided, please return a message on why you were unable to do so."
    user_prompt = f"""
        Information: 
        {company_prompt}
    
    """

    try:
        # Call the OpenAI API to get the response - changing to use info from https://platform.openai.com/docs/api-reference/chat/create?lang=python
        response = client.beta.chat.completions.parse( #client.beta.chat.completions.parse # client.chat.completions.create
            model= "gpt-4o-mini", # "gpt-4o-2024-08-06" "gpt-4o-mini"
            # max_tokens=150,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
                ],
            #temperature=0.3,
            response_format=Profile,
            # top_p=1
        )
        
        outcome = response.choices[0].message

        if outcome.parsed:
            
            model_out = outcome.parsed.model_dump()
            LLM_out_list = [model_out['company_name'], model_out['company_purpose_keywords'],  model_out['company_description'], model_out['url_link']]

 
        elif outcome.refusal:

            # LLM_out_list = ['refusal','refusal','refusal','refusal']
            LLM_out_list = ['empty','empty','empty','empty']
        
    except Exception as e:

        print(company_name, e)
        # LLM_out_list = ['exception','exception','exception','exception']
        LLM_out_list = ['empty','empty','empty','empty']
    
    finally:

        return LLM_out_list



# LOOP THROUGH NEW_COMPANY LIST. FOR EACH COMPANY, CHECK WHAT DATA ALEADY EXISTS IN BIOECONOMY CSV
# CALL FUNCTIONS TO GET WHAT DATA IS NOT PRESENT

for company in raw_company_list:

    # in_bioeconomy, in_web_info, in_location_info, in_LLM_parse = False, False, False, False

    # check_name, check_keywords, check_description, check_link, check_address, check_placesID, check_latitude, check_longitude = False, False, False, False, False, False, False, False


    # Is the company present in the Bioeconomy csv? What info needs closer inspection?
    if company in names:
        # check_name = True
        index = names.index(company)

        if keywords[index] == 'empty'

    
    # For companies not present, run through the normal pipeline of gathering and parsing info
    else:
        # Check web_info_dict
        try:
            current_web_info_dict[company]
        except KeyError:
            web_info = get_web_info(company)
            current_web_info_dict[company] = web_info


        # Check location_info_dict
        try:
            current_location_info_dict[company]
        except KeyError:
            location_info = get_location_info(company)
            current_location_info_dict[company] = location_info


        # Check LLM_parse_dict
        try:
            current_company_LLM_parse_dict[company]
        except KeyError:
            # What should this return?
            LLM_parse = get_LLM_parse(company, current_location_info_dict)
            current_company_LLM_parse_dict[company] = LLM_parse

        # Assemble the new bioeconomy_df entry and add it to the df
        new_df_entry = [
            LLM_parse[0],
            LLM_parse[1],
            LLM_parse[2],
            LLM_parse[3],
            location_info[0],
            location_info[1],
            location_info[2],
            location_info[3],
        ]

        current_bioeconomy_df.loc[len(current_bioeconomy_df)] = new_df_entry



# STORE UPDATED WEB_INFO, LOCATION_INFO, LLM_PARSE, BIOECONOMY_DF, AND TROUBLESHOOTING_DF --> AS 'CURRENT' VERSION, NO COPY

with open('C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/current_web_info_dict.pkl', 'wb') as f:
    pickle.dump(current_web_info_dict, f)

with open('C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/current_location_info_dict.pkl', 'wb') as f:
    pickle.dump(current_location_info_dict, f)

with open('C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/current_company_LLM_parse_dict.pkl', 'wb') as f:
    pickle.dump(current_company_LLM_parse_dict, f)

current_bioeconomy_df.to_csv(
    path_or_buf="C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/current_bioeconomy_df.csv",
    sep=',',
    index=False
    )

# current_troubleshooting_df.to_csv(
#     path_or_buf="C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/current_troubleshooting_df - Copy.csv",
#     sep=',',
#     index=False
#     )















######################################################

## Now make a list of the set of companies that don't have Tavily data

companies = raw_company_list_df['Company']
no_tav_list = []

for i in companies:
    
    try:

        company_list_tavily_output_dict[i]

    except KeyError:

        no_tav_list.append(i)

## Now going to try to find companies that returned Tavily results that are garbage

have_tav_list = [i for i in companies if i not in no_tav_list]
# print(len(companies))
# print(len(no_tav_list))
# print(len(have_tav_list))

empty_tav_list = []

for i in have_tav_list:

    results = company_list_tavily_output_dict[i]['results']

    if len(results) < 5:
        
        print(results)
        empty_tav_list.append(i)

## 23 companies have 'empty' or short Tav lists, adding them to the Tavily search list
## may want to also drop them from the tavily output dict...or just not add ones that have results length = 0

no_tav_list.append(empty_tav_list)

## Now set up Tavily pipeline with this list

tavily_api_key = os.getenv('TAVILY_API_KEY_sfs', 'None')
tavily = TavilyClient(api_key=tavily_api_key)

tav_out_dict = {}

for i in no_tav_list:

    tav_query_final = "Describe what " + i + " does, including its objectives, location, the industries and markets in which it operates, and any differentiating characteristics relative to other companies in a similar space."

    company_name_tavily_output = tavily.search(
        query = tav_query_final,
        search_depth="advanced",
        max_results=8
        )

    tav_out_dict[i] = company_name_tavily_output

    print(i)

with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/2024-08-03 company_list_tavily_output_dict.pkl", 'wb') as f:
    pickle.dump(tav_out_dict, f)


# GATHER INFO ABOUT THE LOCATION OF THE COMPANY





# GATHER INFO ABOUT THE COMPANY USING TAVILY






# CALL AN LLM TO TURN THE TAVILY INFO INTO THE DESIRED STRUCTURED OUTPUT





# WRITE THE COMLETED DATAFRAME TO A CSV TO BE IMPORTED WITH STREAMLIT



