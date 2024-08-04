import pickle
import json
import dotenv # pip install python-dotenv
import os
dotenv.load_dotenv()  #(dotenv_path='/.venv/.env')

import pandas as pd
import numpy as np
from google.maps import places_v1


raw_company_list_path = "C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/2024-07-28 raw company list utf8.csv"

raw_company_list_df = pd.read_csv(
    filepath_or_buffer=raw_company_list_path,
    header=0,
    skipinitialspace=True,
    on_bad_lines='warn',
    encoding= 'latin-1'
    )

# Getting an error that utf8 can't decode a byte in position 396 - invalid start byte...not even sure how to fix this...
# Moved forward by re-saving the csv as UTF8 csv in excel, now it works

# One example is Latin-1 (also called ISO-8859-1), which is technically the default for the Hypertext Transfer Protocol (HTTP), per RFC 2616. Windows has its own Latin-1 variant called cp1252.


# Need to convert df column to a subscriptable list

raw_company_list = raw_company_list_df['Company'].tolist()

places_api_key = os.getenv('bioeconomyweb_google_api_key', 'None') 

# SearchTextRequest
def sample_search_text(company_name):
      
    # Create a client
    client = places_v1.PlacesClient(
        client_options={"api_key": places_api_key}
    )

    company_loc_query = company_name # may need to spruce this up a bit later to help restrict area or type

    # Initialize request argument(s)
    request = places_v1.SearchTextRequest(
        text_query=company_loc_query
    )

    fieldMask = "places.id,places.formattedAddress,places.location" #places.location.latitude,places.location.longitude"        # "*" - returns all fields

    # Make the request
    response = client.search_text(
        request=request,
        metadata=[("x-goog-fieldmask",fieldMask)]
        )

    # Handle the response
    return response


company_loc_only_df = pd.DataFrame(columns=['Name','PlacesID','Address','Latitude','Longitude'])

for i in raw_company_list:

    print(i)

    places_api_out = sample_search_text(i)


    if places_api_out.places == []:

        places_out_list = [

        i,
        "Unknown", 
        "Unknown", 
        "Unknown",
        "Unknown"

        ]

    else:

        places_out_list = [

            i,
            places_api_out.places[0].id, 
            places_api_out.places[0].formatted_address, 
            places_api_out.places[0].location.latitude,
            places_api_out.places[0].location.longitude

        ]

    company_loc_only_df.loc[len(company_loc_only_df)] = places_out_list


# now write the output df to a .csv

company_loc_only_df.to_csv(
    path_or_buf="C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/2024-07-28 companies and locations.csv",
    sep=',',
    index=False
    )


with open('C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/company_loc_only_df.pkl', 'wb') as f:
    pickle.dump(company_loc_only_df, f)







'''
Future steps:
- DataFrame.to_csv()

'''
