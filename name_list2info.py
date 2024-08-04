import pickle
import os
import dotenv
import pandas as pd
import numpy as np
from tavily import TavilyClient # pip install tavily-python


dotenv.load_dotenv()

# places_api_key = os.getenv('bioeconomyweb_google_api_key', 'None')


## Bring in current (2024-08-03) company list, going to try bringing it in as 'latin-1' encoding

raw_company_list_df = pd.read_csv(
    filepath_or_buffer="C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/2024-07-28 raw company list.csv",
    header=0,
    skipinitialspace=True,
    on_bad_lines='warn',
    encoding= 'latin-1'
    )

## Bring in existing list of companies and their associated tavily out

with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/company_list_tavily_output_dict - Copy.pkl", 'rb') as f:
    company_list_tavily_output_dict = pickle.load(f)

# with open("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/synbio_web_companies_and_info_df - Copy.pkl", 'rb') as f:
#     synbio_web_companies_and_info_df = pickle.load(f)

## Bring in current version of 'clean and complete' companies with their associated keywords, description, and link

# synbio_web_companies_and_info_df = pd.read_excel("C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/2024-03-17 synbio_web_companies_and_info - Copy.xlsx", sheet_name = "Sheet1")

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





# def get_company_location(company_info):
#     """
#     Uses OpenAI's API to determine the location of a company from the provided information.

#     Args:
#     company_info (dict): A dictionary containing company name and associated information.

#     Returns:
#     The location of the company
#     """
#     client = OpenAI(
#       api_key = os.getenv('bioeconomyweb_openai_api_key', 'None')
#     )

#     company_name = company_info.get('name')
#     company_data = company_info.get('info', '')

#     # Construct the prompt for the LLM
#     system_prompt = "You are a helpful assistant. Use the provided information delimited by triple quotes to answer questions. If the answer cannot be found in the articles, write 'I could not find an answer'."
# 	  # "You are an helpful assistant that helps extract the locations of companies or other organization from a larger amount of information about the company."

#     user_prompt = f"""
	  
# 	  Information: {company_data}
    
#     """

#     # Call the OpenAI API to get the response - changing to use info from https://platform.openai.com/docs/api-reference/chat/create?lang=python
#     response = client.chat.completions.create(
#         model= "gpt-4o-mini", # "text-davinci-003" decprecated
#         # prompt=prompt, # pretty sure code is wrong and i need to use "messages"
#         # max_tokens=150,
#         messages=[
#               {'role': 'system', 'content': system_prompt},
#               {'role': 'user', 'content': [
#                   {"type": "text", "text": user_prompt},
#                   {"type": "text", 'text': f"Please determine the most specific location of the {company_name} from the information provided. If the location cannot be confidently determined, return 'Location Unknown'."}
#                   ]}
#         ],
#         temperature=0.2,
#         # top_p=1
#     )


#     # Extract and format the result - print(completion.choices[0].message)
#     # result = response.choices[0].text.strip()
#     result = response.choices[0].message.content
	  
#     return result














# ##########################################################################################
# # install lanchain
# !pip install langchain
# !pip install openai

# from langchain.adapters.openai import convert_openai_messages
# from langchain.chat_models import ChatOpenAI


# # from langchain_openai import ChatOpenAI  # deprecated from langchain.chat_models import ChatOpenAI
# # from langchain_openai import ChatOpenAI # - not working for some reason, what needs to be installed?

# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser, JsonOutputParser
# from langchain_core.pydantic_v1 import BaseModel, Field


# #########################################################################################


# # Final Company list preparation chunk

# # Taking in the list of companies. Need to prepare Synbio Web 4 import file
# # beforehand by downloading current "Synbio Web" google sheet as an excel file
# happening_in_synbio = pd.read_excel('/content/gdrive/MyDrive/Synbio Web 4 import.xlsx', sheet_name = "Happening in Synbio")
# company_list = happening_in_synbio['Company'][1:]

# print(len(company_list))

# # Now remove duplicates from company_list

# company_list = list(set(company_list))
# print(len(company_list))

# # responses should be 580/570 as of 3/3/24



# #########################################################################################
# with open('/content/gdrive/MyDrive/Colab Notebooks/company_list_tavily_output_dict.pkl', 'rb') as f:
#   company_list_tavily_output_dict = pickle.load(f)

# print(len(company_list_tavily_output_dict))
# #486 3/6/24

# with open('/content/gdrive/MyDrive/Colab Notebooks/Copy2 of company_list_tavily_output_dict.pkl', 'rb') as f:
#   company_list_tavily_output_dict2 = pickle.load(f)

# print(len(company_list_tavily_output_dict2))
# #460 3/6/24

# with open('/content/gdrive/MyDrive/Colab Notebooks/Copy of company_list_tavily_output_dict.pkl', 'rb') as f:
#   company_list_tavily_output_dict3 = pickle.load(f)

# print(len(company_list_tavily_output_dict3))
# #182 3/6/24
# #########################################################################################
# # create a fake dict with all the keys in company_list, then try to figure out what keys are missing

# fake_dict = dict()

# for i in range(len(company_list)):

#   name = company_list[i]

#   fake_dict[str(name)] = 1

# print(fake_dict.keys())
# #########################################################################################
# # create a fake dict with all the keys in company_list, then try to figure out what keys are missing

# fake_dict = dict()

# for i in range(len(company_list)):

#   name = company_list[i]

#   fake_dict[str(name)] = 1

# print(fake_dict.keys())
# #########################################################################################
# # Final Tavily Calling Chunk

# sean_dana_tavily_api_key = ""

# tavily = TavilyClient(api_key=sean_dana_tavily_api_key)

# # company_list_tavily_output_dict = dict() # commenting out because i loaded it via pickle, dont need ot re-initialize

# for i in range(459,(len(company_list)-1)):

#   company_name = company_list[i]

#   tav_query_final = "Describe what the company " + str(company_name) + " does, including its objectives, the industries and markets in which it operates, and any differentiating characteristics relative to other companies in a similar space."

#   company_name_tavily_output = tavily.search(query = tav_query_final, search_depth="advanced", max_results=10)

#   company_list_tavily_output_dict[str(company_name)] = company_name_tavily_output

#   with open('/content/gdrive/MyDrive/Colab Notebooks/company_list_tavily_output_dict.pkl', 'wb') as f:
#     pickle.dump(company_list_tavily_output_dict, f)

#   print(i)
# #finished through 181 (current length is 182)
# # starting up function call again from range 182:len(comp)-1
# # round 3 made it to 459, next run would be range(459,len(comp)-1)

# # The code above keeps the entire Tavily output, need to make sure to only grab the "Results" when calling the LLM chain later
# #########################################################################################
# #tavily calling chunk to get final 84 companies into Tav query struct.

# sean_dana_tavily_api_key = ""

# tavily = TavilyClient(api_key=sean_dana_tavily_api_key)

# # company_list_tavily_output_dict = dict() # commenting out because i loaded it via pickle, dont need ot re-initialize

# for i in range(0, len(no_tav)-1):

#   company_name = no_tav[i]

#   tav_query_final = "Describe what the company " + str(company_name) + " does, including its objectives, the industries and markets in which it operates, and any differentiating characteristics relative to other companies in a similar space."

#   company_name_tavily_output = tavily.search(query = tav_query_final, search_depth="advanced", max_results=10)

#   company_list_tavily_output_dict[str(company_name)] = company_name_tavily_output

#   with open('/content/gdrive/MyDrive/Colab Notebooks/company_list_tavily_output_dict.pkl', 'wb') as f:
#     pickle.dump(company_list_tavily_output_dict, f)

#   print(i)

# # only missing 1 company, gonna let that one go for now...
# print(len(company_list_tavily_output_dict))
# #########################################################################################
# # Final LLM chain calling -  defining function chunk

# # The class `langchain_community.chat_models.openai.ChatOpenAI` was deprecated in langchain-community 0.0.10 and will be removed in 0.2.0. An updated version of the class exists in the langchain-openai package and should be used instead. To use it run `pip install -U langchain-openai` and import as `from langchain_openai import ChatOpenAI`.
# #   warn_deprecated(

# model = ChatOpenAI(model='gpt-4',openai_api_key=openai_api_key)

# def call_json_output_parser(company_name, tavily_content): # function currently gets passed Tavily content, a more elegant solution would be to call Tavily during the function but id like to keep them separate

#   prompt = ChatPromptTemplate.from_messages([
#       ("system", 'You are an AI critical thinker research assistant. '\
#                 'You will be provided with a large amount of context about a company taken from multiple different websites on the internet. '\
#                 'Your sole purpose is to use this context to accurately and succinctly respond to the user\'s query. '\
#                 'Formatting Instructions: {format_instructions}'
#       ),
#       ("human", 'Information: {tavily_content}\n\n'\
#        'Using the above information, answer the following query: {openai_query} .'
#       )
#   ])

#   openai_query = "For the company or organization named " + str(company_name) +  ", return the organization's name, 3-4 keywords that describe the industry and/or market served by" + str(company_name) + ", the url for the organization's website, and a brief description of what the organization does and what markets it operates in."

#   class Person(BaseModel):
#     name: str = Field(description = "the name of the company")
#     keywords: list = Field(description = "3-4 keywords that describe the industry and/or market served by the company")
#     link: str = Field(description = "the url for the organization's website")
#     description: str = Field(description = "a description of between roughly 100 and 500 words of what the organization does and what markets it operates in.")


#   parser = JsonOutputParser(pydantic_object = Person) # needs to be passed a schema for what the JSON should look like, that gets defined using Pydantic

#   chain = prompt | model | parser


#   return chain.invoke({
#     "tavily_content": tavily_content,
#     "openai_query": openai_query,
#     "format_instructions": parser.get_format_instructions()

#     })



# #########################################################################################
# # Final LLM chain calling - looping through Tavily dict to call LLM for each comapny + context

# # initialize a df to dump everything into

# synbio_web_companies_and_info_df = pd.DataFrame(columns=['Name', 'Keywords', 'Description', 'Link'])

# # print(llm_output_company_df)

# # need a list of companies that have entries in the company_list_tavily_output_dict --> trying 'items' method //taking from index

# for k, v in company_list_tavily_output_dict.items():

#   company_name = k
#   tavily_content = v['results']

#   try:

#     llm_output_dict = call_json_output_parser(company_name, tavily_content)

#     synbio_web_companies_and_info_df.loc[len(synbio_web_companies_and_info_df)] = [llm_output_dict['name'],llm_output_dict['keywords'],llm_output_dict['description'],llm_output_dict['link']]

#     with open('/content/gdrive/MyDrive/Colab Notebooks/synbio_web_companies_and_info_df.pkl', 'wb') as f:
#       pickle.dump(synbio_web_companies_and_info_df, f)

#   except:

#     pass

#   print(len(synbio_web_companies_and_info_df))



# # 3/9/24 first call gets through 43 before failing --> need error handling for when there isn't enough info on an org for the LLM to handle it
# # need ot subset the company_list_tavily_output_dict to onlybe running stuff that isnt already in synbio_web_companies_and_info_df


# #########################################################################################
# df_test = list(synbio_web_companies_and_info_df['Name'])

# index_test = list(company_list_tavily_output_dict.keys())

# print(len(df_test)) # 43
# print(len(index_test)) #569

# # now need to get the unique subset of index_test that is not in df_test

# def get_unique_items(list1, list2):
#   """
#   Returns a list of items that are in list1 but not in list2.

#   Args:
#       list1: The first list.
#       list2: The second list.

#   Returns:
#       A list of unique items.
#   """

#   # Convert both lists to sets for faster comparison.
#   set1 = set(list1)
#   set2 = set(list2)

#   # Use the difference operator to get unique items in list1.
#   unique_items = set1.difference(set2)

#   # Convert the set back to a list.
#   return list(unique_items)

# # here list1 is the index_test object, list2 is the df_tset object

# unique_items = get_unique_items(index_test, df_test)

# #length should be 569-43 = 526
# print(len(unique_items))
# print(type(unique_items[1]))

# print(index_test)

# #somehow its 538. not going to try and figure this out



# #########################################################################################
# # This code chunk is going to try and continue filling synbio_web_companies_and_info_df
# # by isolating just the companies that didn't go in the first run

# # companies_left = list()

# # for x in index_test:
# #   if x not in df_test:
# #     companies_left.append(x)

# # print(range(len(unique_items)))

# for i in range(0,(len(unique_items)-1)):

#   company_name = unique_items[i]
#   tavily_content = company_list_tavily_output_dict[str(company_name)]['results']

#   try:

#     llm_output_dict = call_json_output_parser(company_name, tavily_content)

#     synbio_web_companies_and_info_df.loc[len(synbio_web_companies_and_info_df)] = [llm_output_dict['name'],llm_output_dict['keywords'],llm_output_dict['description'],llm_output_dict['link']]

#     with open('/content/gdrive/MyDrive/Colab Notebooks/synbio_web_companies_and_info_df.pkl', 'wb') as f:
#       pickle.dump(synbio_web_companies_and_info_df, f)

#   except:

#     pass

#   print(len(synbio_web_companies_and_info_df))

# #########################################################################################
# company_name1 = "AgBiome"


# # testing to see output of LLM call
# query1 = "Describe what the company " + str(company_name1) + " does, including its objectives, the industries and markets in which it operates, and any differentiating characteristics relative to other companies in a similar space."
# test_tav1 = company_list_tavily_output_dict[str(company_name1)]#['results']
# llm_output1 = call_json_output_parser(company_name1, test_tav1["results"])

# print(type(test_tav1))
# print(len(test_tav1))
# print(test_tav1)

# print(llm_output1) # output is a dict

# #########################################################################################

# # open the LLM output dataframe

# with open('/content/gdrive/MyDrive/Colab Notebooks/synbio_web_companies_and_info_df.pkl', 'rb') as f:
#     synbio_web_companies_and_info_df = pickle.load(f)

# #########################################################################################

# print(type(synbio_web_companies_and_info_df["Keywords"][1]))

# # successfully converts the whole column to a string but this doesnt remove anything, it just becomes a string instead of a series
# # synbio_web_companies_and_info_df["Keywords"] = synbio_web_companies_and_info_df["Keywords"].astype("string")

# # This is a big fail and adds lots of commas when things are already a string, but works well on the freshly loaded dict
# synbio_web_companies_and_info_df["Keywords"] = [','.join(map(str, l)) for l in synbio_web_companies_and_info_df["Keywords"]]

# # now dropping index column
# synbio_web_companies_and_info_df = synbio_web_companies_and_info_df.drop(synbio_web_companies_and_info_df.columns[[0]], axis=1) # axis 0 for rows and 1 for column
# # good to know this code but can't actually do this! Index isnt technically a column (dropping the 0 column doesnt work)


# #########################################################################################
# # Excel writer code - https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html

# synbio_web_companies_and_info_df.to_excel("/content/gdrive/MyDrive/Colab Notebooks/synbio_web_companies_and_info.xlsx")

# #########################################################################################


#########################################################################################


#########################################################################################
