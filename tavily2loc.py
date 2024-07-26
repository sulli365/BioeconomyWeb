
'''
Pseudo-code

- Figure out how to API keys to a file that isn't mirrored to Github
- Import company list from existing spreadsheet or dict, going w/spreadsheet for now for simplicity.
- Import Tavily_dict.pkl file containing Tavily outputs that have been gathered so far
- Modify existing Tavily/LLM pipeline to look at existing company list output, and for each company, try to use the Tavily info to assign a location (address/city/state/country) to it.
If unable to find a location, it should return "Location Unknown" so that these companies can be grouped together and plotted somewhere arbitrarily on the map later on.
- Output should be a dataframe with the existing company list that now has a new column wiht locations.
- Using those locations, add a new column to the dataframe where I try out some different code to assign lat/lon values to the locations.
- Final output would be a .csv or .xlsx that has the company info and locations that can then fed be to a streamlit viz function.

Future steps
- Clustering of companies in some way (climate type, etc) --> another column in the spreadsheet

'''

# - Import company list from existing spreadsheet or dict (probably dict)

import pickle
import pandas as pd
import numpy as np

# needed to install pandas dependency 'openpyxl' --> pip install openpyxl

with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/company_list_tavily_output_dict - Copy.pkl", 'rb') as f:
    company_list_tavily_output_dict = pickle.load(f)


synbio_web_companies_and_info_df = pd.read_excel("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/2024-03-17 synbio_web_companies_and_info - Copy.xlsx", sheet_name = "Sheet1")


company_list = synbio_web_companies_and_info_df['Name']#[1:]
print(len(company_list))

####
# Remove duplicates from company_list - dont need to do this atm

# company_list = list(set(company_list))
# print(len(company_list))
####

# Proceeding w/just 50 companies for now for simplicity/time

company_list = company_list[0:49]

# Proceeding w/just 50 companies for now for simplicity/time

company_tavily_dict = dict()
no_tavily = []

# for i in company_list:
# 	print(i)
# 	print(type(i))

for i in company_list:

	# name = company_list[i]
	# print(name)

	try:
		tav_info = company_list_tavily_output_dict[i]['results']

	except KeyError:
		
		no_tavily.append(i)
		pass

	company_tavily_dict[i] = tav_info

comp_list_with_tav = [x for x in company_list if x not in no_tavily]


# Issue was both finding things in the dict and the fact that i 
# is alraeady the name of the element in company_list

# Also, for some reason, lots of these companies in the spreadsheet don't have info in the tavily dict...where is their tavily info?

# Now call LLM w/instructions to return location

# requires pip install openai python-dotenv

import os


######################## after this was chatgpt output wiht mods as noted


from openai import OpenAI
import json

# Set up your OpenAI API key

client = OpenAI(
    api_key = 'XXX'
)


# openai_api_key = ''

def get_company_location(company_info):
    """
    Uses OpenAI's API to determine the location of a company from the provided information.

    Args:
    company_info (dict): A dictionary containing company name and associated information.

    Returns:
    dict: A JSON object with the company name as the key and the location as the value.
    """
    company_name = company_info.get('name')
    company_data = company_info.get('info', '')

    # Construct the prompt for the LLM
    prompt = f"""
    I have information about a company. Please determine the most specific location of the company from the information provided. If the location cannot be confidently determined, return "Location Unknown".

    Company Name: {company_name}
    Information: {company_data}

    The output should be in the format of a JSON object where the company name is the key and the location is the value.
    """

    # Call the OpenAI API to get the response
    response = client.completions.create(
        model= "gpt-4o-mini", # "text-davinci-003" decprecated
        prompt=prompt,
        max_tokens=150,
        temperature=0,
        top_p=1
    )

    # Extract and format the result
    result = response.choices[0].text.strip()

    try:
        # Try to parse the result as JSON
        location_info = json.loads(result)
        # Ensure the result is a dictionary with a single entry
        if isinstance(location_info, dict) and len(location_info) == 1 and company_name in location_info:
            return location_info
    except json.JSONDecodeError:
        pass

    # If parsing fails or the format is incorrect, return "Location Unknown"
    return {company_name: "Location Unknown"}

# Example usage
# company_info = {
#     'name': 'BioTech Innovations',
#     'info': 'BioTech Innovations specializes in advanced bioengineering solutions. Their headquarters are located in Boston, Massachusetts.'
# }

# location = get_company_location(company_info)
# print(json.dumps(location, indent=2))


######################## prior to this was chatgpt output

# Going to test chatGPT code quickly

name_temp = comp_list_with_tav[0]
test_dict = dict(name_temp = company_tavily_dict[comp_list_with_tav[0]])
test = get_company_location(test_dict)


# Next step is to loop through all the companies w/their Tavily info and get the locations out, stored in a new dict

comp_loc_dict = dict()


for i in comp_list_with_tav:
    
    temp_dict = {i: company_tavily_dict[i]}
    
	output = get_company_location(company_info)
    
	comp_loc_dict[i] = output[i]
    






# client = OpenAI(
#     # This is the default and can be omitted
#     api_key=os.environ.get("OPENAI_API_KEY"), #"OPENAI_API_KEY"
# )

# response = client.chat.completions.create(
#   model="gpt-4o-mini",
#   response_format={ "type": "json_object" },
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
#     {"role": "user", "content": "Who won the world series in 2020?"}
#   ]
# )
# print(response.choices[0].message.content)












'''

####################################################################################################################################################

# pip install python-dotenv
import dotenv
dotenv.load_dotenv('/content/gdrive/MyDrive/.env')
tavily_api_key = os.environ.get('TAVILY_API_KEY', 'None')
print(tavily_api_key)
openai_api_key = os.environ.get('OPENAI_API_KEY', 'None_2')
print(openai_api_key)


import pandas as pd
import numpy as np

!pip install tavily-python
from tavily import TavilyClient


# install lanchain
!pip install langchain
!pip install openai

from langchain.adapters.openai import convert_openai_messages
from langchain.chat_models import ChatOpenAI


# from langchain_openai import ChatOpenAI  # deprecated from langchain.chat_models import ChatOpenAI
# from langchain_openai import ChatOpenAI # - not working for some reason, what needs to be installed?

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser, JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field





with open('/content/gdrive/MyDrive/Colab Notebooks/company_list_tavily_output_dict.pkl', 'rb') as f:
  company_list_tavily_output_dict = pickle.load(f)

print(len(company_list_tavily_output_dict))






# Final LLM chain calling -  defining function chunk

# The class `langchain_community.chat_models.openai.ChatOpenAI` was deprecated in langchain-community 0.0.10 and will be removed in 0.2.0. An updated version of the class exists in the langchain-openai package and should be used instead. To use it run `pip install -U langchain-openai` and import as `from langchain_openai import ChatOpenAI`.
#   warn_deprecated(

model = ChatOpenAI(model='gpt-4',openai_api_key=openai_api_key)

def call_json_output_parser(company_name, tavily_content): # function currently gets passed Tavily content, a more elegant solution would be to call Tavily during the function but id like to keep them separate

  prompt = ChatPromptTemplate.from_messages([
      ("system", 'You are an AI critical thinker research assistant. '\
                'You will be provided with a large amount of context about a company taken from multiple different websites on the internet. '\
                'Your sole purpose is to use this context to accurately and succinctly respond to the user\'s query. '\
                'Formatting Instructions: {format_instructions}'
      ),
      ("human", 'Information: {tavily_content}\n\n'\
       'Using the above information, answer the following query: {openai_query} .'
      )
  ])

  openai_query = "For the company or organization named " + str(company_name) +  ", return the organization's name, 3-4 keywords that describe the industry and/or market served by" + str(company_name) + ", the url for the organization's website, and a brief description of what the organization does and what markets it operates in."

  class Person(BaseModel):
    name: str = Field(description = "the name of the company")
    keywords: list = Field(description = "3-4 keywords that describe the industry and/or market served by the company")
    link: str = Field(description = "the url for the organization's website")
    description: str = Field(description = "a description of between roughly 100 and 500 words of what the organization does and what markets it operates in.")


  parser = JsonOutputParser(pydantic_object = Person) # needs to be passed a schema for what the JSON should look like, that gets defined using Pydantic

  chain = prompt | model | parser


  return chain.invoke({
    "tavily_content": tavily_content,
    "openai_query": openai_query,
    "format_instructions": parser.get_format_instructions()

    })



#########################################################################################
# Final LLM chain calling - looping through Tavily dict to call LLM for each comapny + context

# initialize a df to dump everything into

synbio_web_companies_and_info_df = pd.DataFrame(columns=['Name', 'Keywords', 'Description', 'Link'])

# print(llm_output_company_df)

# need a list of companies that have entries in the company_list_tavily_output_dict --> trying 'items' method //taking from index

for k, v in company_list_tavily_output_dict.items():

  company_name = k
  tavily_content = v['results']

  try:

    llm_output_dict = call_json_output_parser(company_name, tavily_content)

    synbio_web_companies_and_info_df.loc[len(synbio_web_companies_and_info_df)] = [llm_output_dict['name'],llm_output_dict['keywords'],llm_output_dict['description'],llm_output_dict['link']]

    with open('/content/gdrive/MyDrive/Colab Notebooks/synbio_web_companies_and_info_df.pkl', 'wb') as f:
      pickle.dump(synbio_web_companies_and_info_df, f)

  except:

    pass

  print(len(synbio_web_companies_and_info_df))



# 3/9/24 first call gets through 43 before failing --> need error handling for when there isn't enough info on an org for the LLM to handle it
# need ot subset the company_list_tavily_output_dict to onlybe running stuff that isnt already in synbio_web_companies_and_info_df



'''