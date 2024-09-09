# Bring in company list with tavily outputs
# Cycle throgh them and exclude any that dont have results (or <4 results)
# For the remaining company/info pairs, strip out the everything but the actual relevant context from the results
# In a loop, pass the company name and context to an LLM with instructions to return a dict or a JSON (probs better option)
##### Name, Location?, Keywords, Description (250 words max?), url link


import pickle
import os
import dotenv
import pandas as pd
import numpy as np
from tavily import TavilyClient
# import openai
from openai import OpenAI
# import pydantic
from pydantic import BaseModel, Field # pip install pydantic
import requests # ?


dotenv.load_dotenv()

# with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/2024-08-03 company_list_tavily_output_dict.pkl", 'rb') as f:
#     company_list_tavily_output_dict_new = pickle.load(f)

# with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/company_list_tavily_output_dict - Copy.pkl", 'rb') as f:
#     company_list_tavily_output_dict_old = pickle.load(f)


# # Combine the two dictionaries

# # For dictionaries x and y, their shallowly-merged dictionary z takes values from y, replacing those from x.
# # z = x | y

# full_tavily_dict = company_list_tavily_output_dict_old | company_list_tavily_output_dict_new

## Now need a function that takes in a Tavily output and returns just the info in each results section

with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/2024-08-18 full_tavily_dict.pkl", 'rb') as f:
    full_tavily_dict = pickle.load(f)


def tavily_strip(company_name, full_tavily_dict):

    tav_dict_iso = full_tavily_dict[company_name]

    result_list = tav_dict_iso['results']

    # prompt_text_final = ""
    prompt_text_list = []

    for source in result_list:

        prompt_text_list.append(source['url'])
        prompt_text_list.append(source['content']) # source['title'] + 
    
    # for item in prompt_text_list:

    prompt_text_final = '\n'.join(prompt_text_list)

    return [company_name, prompt_text_final]

# test2 = tavily_strip(testout)
# print(test2)

## Now need to set up an LLM call

def get_company_profile(name_and_info):
    """
    NOT FINISHED
    Uses OpenAI's API to turn information scraped from the web into a structured output containing useful information that will then be used ot make the Streamlit map.


    Args:
    name_and_info (dict): A dictionary containing company name and its associated Tavily information as a Python list with two elements.

    Returns:
    - Name
    - Keywords
    - URL
    - Description
    """

    # Define a Pydantic class to capture the desired output of the LLM call
    class Profile(BaseModel):
        company_name: str = Field(description = "the name of the company")
        company_purpose_keywords: str = Field(description = "3-4 keywords that describe the industry and/or market served by the company")
        url_link: str = Field(description = "the url for the organization's website")
        company_description: str = Field(description = "a description of between 150 and 300 words of what the organization does and what markets it operates in.")


    client = OpenAI(
      api_key = os.getenv('bioeconomyweb_openai_api_key', 'None')
    )

    # bring i
    company_name = name_and_info[0]
    company_info = name_and_info[1]

    # Construct the prompt for the LLM
    system_prompt = f"You are helpful assistant. Using the provided information delimited by triple quotes, for the company or organization named {company_name}, return the organization's name, 3-4 keywords that describe the industry and/or market served by {company_name}, the url for the organization's website, and a brief description of what the organization does and what markets it operates in. If the answer cannot be found in the information provided, please return a message on why you were unable to do so."

    user_prompt = f"""
        Information: 
        {company_info}
    
    """

    # user_query = "For the company or organization named " + str(company_name) +  ", return the organization's name, 3-4 keywords that describe the industry and/or market served by" + str(company_name) + ", the url for the organization's website, and a brief description of what the organization does and what markets it operates in."

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
	  
    return response.choices[0].message.parsed

# Trying my function returning the entire response from the LLM as the output, need to see what this actually is going to look like

testing1 = tavily_strip("AgBiome", full_tavily_dict)
testing2 = get_company_profile(testing1)
testing2 = testing2.model_dump()
# print(testing2)

## Parsing outcome to extract output info into a dataframe

# Define a pandas df that contains all the appropriate info

LLM_company_info_df = pd.DataFrame(data=None, index=None, columns= ['Name', 'Keywords', 'URL', 'Description'])

# Create a python list of the elements in the LLM output and add them to the new df

LLM_out_list = [testing2['company_name'], testing2['company_purpose_keywords'], testing2['url_link'], testing2['company_description']]

LLM_company_info_df.loc[len(LLM_company_info_df)] = LLM_out_list
# print(LLM_company_info_df)











###### Separator for extra code to refer to

# def get_company_profile(name_and_info):
#     """
#     Uses OpenAI's API to turn information scraped from the web into a structured output containing useful information that will then be used ot make the Streamlit map.


#     Args:
#     name_and_info (dict): A dictionary containing company name and its associated Tavily information.

#     Returns:
#     - Name
#     - Keywords
#     - URL
#     - Description
#     """

#     client = OpenAI(
#       api_key = os.getenv('bioeconomyweb_openai_api_key', 'None')
#     )

#     company_name = name_and_info[0]
#     company_info = name_and_info[1]

#     # Construct the prompt for the LLM
#     system_prompt = "You are an AI critical thinker research assistant. Use the provided information delimited by triple quotes to answer questions. If the answer cannot be found in the articles, please return a message on why you were unable to do so."

#     user_prompt = f"""

#         Information: {company_name}
#         Information: {company_info}
    
#     """

#     user_query = "For the company or organization named " + str(company_name) +  ", return the organization's name, 3-4 keywords that describe the industry and/or market served by" + str(company_name) + ", the url for the organization's website, and a brief description of what the organization does and what markets it operates in."

#     # Construct a Pydantic class for sturcture output

#     class Profile(BaseModel):
#         name: str = Field(description = "the name of the company")
#         keywords: list = Field(description = "3-4 keywords that describe the industry and/or market served by the company")
#         link: str = Field(description = "the url for the organization's website")
#         description: str = Field(description = "a description of between 150 and 300 words of what the organization does and what markets it operates in.")


#     # Call the OpenAI API to get the response - changing to use info from https://platform.openai.com/docs/api-reference/chat/create?lang=python
#     response = client.beta.chat.completions.parse( #client.beta.chat.completions.parse # client.chat.completions.create
#         model= "gpt-4o-mini", # "gpt-4o-2024-08-06" "gpt-4o-mini"
#         # max_tokens=150,
#         messages=[
#               {'role': 'system', 'content': system_prompt},
#               {'role': 'user', 'content': [
#                   {"type": "text", "text": user_prompt},
#                   {"type": "text", 'text': user_query}
#                   ]}
#         ],
#         temperature=0.3,
#         response_format= Profile,
#         # top_p=1
#     )


#     # Extract and format the result - print(completion.choices[0].message)
#     # result = response.choices[0].text.strip()
#     # result = response.choices[0].message.content
	  
#     return response