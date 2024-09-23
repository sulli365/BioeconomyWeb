
# starting with code from - https://www.youtube.com/watch?v=H8Ypb8Ei9YA

# import csv

# filename = "C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/2024-07-28 companies and locations.csv"
# records = []


# with open(filename, 'r') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         records.append(row)

# instantly getting an error where it cant read bytes...will need to figure this out later

# Now convert string lat/lon coordinates to float


import os # cwd = os.getcwd()
import streamlit as st # pip install streamlit
import pandas as pd
import folium
import numpy as np
from streamlit_folium import st_folium
from folium.plugins import FastMarkerCluster


APP_TITLE = "Bioeconomy Web"
# APP_SUB_TITLE = "Caveat emptor"


def display_sidebar_filters(info_df):
    """
    Takes in a dataframe that contains the full list of companies and associated info.

    Uses this info to display options for searching for a company (search bar) and filtering the
    markers visible on the map by keywords (validated list of Keywords).

    Outputs could be company names or keywords that are then passed to the display_map function to
    control what markers are visible on the map.

    Default return for each should be None for the case where no specific filtering is done.
    """
    search_choice = ''
    # pausing on searchbar atm, would need if statement later
    # searchbar = st.
    

    multi_options = list(info_df['Keywords'].unique())
    multi_options.sort()
    multi_choices = st.multiselect("Filter visible companies by keyword:", options=multi_options)

    return search_choice, multi_choices # returns STRING, LIST




def display_map(info_df, search_choice, multi_choices):
    """
    Receives the full company info df but also args that allow the markers display to be a filtered subset of the full list.
    Need to figure out exactly what args this function needs...

    Output should be an interactive streamlit_folium map.
    """
    
    # NEED CODE HERE THAT FILTERS INPUT DF TO ISOLATE RECORDS SO THEY CAN BE TURNED INTO MARKERS
    # ALSO NEED TO INHERIT HOW TO FILTER THE DF BASED ON INPUT FROM SELECTOR AND/OR SEARCH BAR
    
    map = folium.Map(location=[39.8283,-98.5795], zoom_start=1, tiles='CartoDB positron') #scrollWheelZoom=False,

    for record in records: # NEED TO DEFINE RECORDS - SHOULD BE SUBSET OF FULL DF
        coords = (record[1],record[2])
        folium.Marker(coords, popup=record[0]).add_to(map)

    st_map = st_folium(map, use_container_width=True, height=450)

    # code to extract out Name of last-clicked feature on map
    # need to modify this code to use company name to disply dataframe of company info
    company_name = ''
    if st_map['last_active_drawing']:
        company_name = st_map['last_active_drawing']['properties']['name']
    return company_name




def display_company_details(info_df, company_name):
    """
    Receives a company name (either via hovering or clicking mouse), display info on popup and click.

    Both functions need to result in a dataframe or table appear below the map with the appropriate information.
    """
    # Need to inherit user interaction (click/hover) somehow
    # Think this will actually be a click-only thing, hover gets dealt with
    # in display-map function when defining marker characteristics



    # example: df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]
    if company_name
    click_df = info_df['Name' == str(company_name)]

    # need code to drop lat/lon, etc, will wait until final csv shape is known


    #returns a pandas dataframe object
    return click_df


def main():

    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    # st.caption(APP_SUB_TITLE)

    # LOAD DATA

    # comp_loc_df = pd.read_csv(
    #     filepath_or_buffer="C:/Users/sfsul/Coding Files/Supplementary Files/BioeconomyWebSupp/2024-07-28 companies and locations.csv",
    #     header=0
    # )

    # records = []
    
    # def convert_unknown(name, lat_val, lon_val):
    
    #     if lat_val == "Unknown":
    #         return [name, 0,0]
    #     else:
    #         return [name, float(lat_val),float(lon_val)]


    # records = [convert_unknown(x,y,z) for x,y,z in zip(comp_loc_df['Name'],comp_loc_df['Latitude'],comp_loc_df['Longitude']
    # )]

    # DISPLAY FILTERS AND MAP

    map = folium.Map(location=[39.8283,-98.5795], zoom_start=1, tiles='CartoDB positron') #scrollWheelZoom=False,

    for record in records: # THIS WILL NEED TO BE MODIFIED
        coords = (record[1],record[2])
        folium.Marker(coords, popup=record[0]).add_to(map)

    st_map = st_folium(map, use_container_width=True, height=450)

    # And below should be a table with more information about the selected company

    search_choice, multi_choices = display_sidebar_filters(info_df)
    company_name = display_map(info_df, search_choice, multi_choices)
    company_info_df = display_company_details(info_df, company_name)

    # DISPLAY METRICS
    st.subheader(f'{company_name} Facts')
    if company_name != '':
        st.dataframe(data = company_info_df)

    # display a dataframe for the selected company























if __name__ == "__main__":
    main()


















#################################################################################################
# inserting a container at the top to hold a bunch of filters/buttons
# May also want to do this with a sidebar (st.sidebar.write...)

# c_filters = st.container()


# now inserting two columns, on the left will be the map and on the right will be the table display filtering the data

# left_col, right_col = st.columns(2)

# left_col.write("Map Overlay")
# right_col.write("Details")

# with left_col:
#     map = folium.Map(location=[39.8283,-98.5795], zoom_start=1, tiles='CartoDB positron') #scrollWheelZoom=False,

#     st_map = st_folium(map, use_container_width=True, height=450)



#############################

# import folium # pip install folium
# from folium.plugins import FastMarkerCluster # clusters points that are in very similar locations, may not be necessary

# map = folium.Map(location=[39.8283,-98.5795], zoom_start=2, scrollWheelZoom=False, tiles='CartoDB positron') # Centers map, coords are for center of US


# for record in records:
#     coords = (record['Latitude'],record['Longitude']) # will eventually be (latitude, longitude)
#     folium.Marker(coords, popup=record['Name']).add_to(map)

# # opportunity to use FastMarkerCluster

# map = folium.Map(location=[39.8283,-98.5795], zoom_start=2) # Centers map, coords are for center of US
# latitudes = [a['Latitude'] for a in records]
# longitudes = [a['Longitude'] for a in records]

# FastMarkerCluster(data=list(zip(latitudes, longitudes))).add_to(map)



##############################################################################################


# import os # cwd = os.getcwd()
# import streamlit as st # pip install streamlit
# import pandas as pd
# import folium
# from streamlit_folium import st_folium


# def display_map(df, year, quarter):
#     df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]

#     map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')
    
#     choropleth = folium.Choropleth(
#         geo_data='data/us-state-boundaries.geojson',
#         data=df,
#         columns=('State Name', 'State Total Reports Quarter'),
#         key_on='feature.properties.name',
#         line_opacity=0.8,
#         highlight=True
#     )
#     choropleth.geojson.add_to(map)

#     df_indexed = df.set_index('State Name')
#     for feature in choropleth.geojson.data['features']:
#         state_name = feature['properties']['name']
#         feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'State Pop'][0]) if state_name in list(df_indexed.index) else ''
#         feature['properties']['per_100k'] = 'Reports/100K Population: ' + str(round(df_indexed.loc[state_name, 'Reports per 100K-F&O together'][0])) if state_name in list(df_indexed.index) else ''

#     choropleth.geojson.add_child(
#         folium.features.GeoJsonTooltip(['name', 'population', 'per_100k'], labels=False)
#     )
    
#     st_map = st_folium(map, width=700, height=450)

#     state_name = ''
#     if st_map['last_active_drawing']:
#         state_name = st_map['last_active_drawing']['properties']['name']
#     return state_name








# Reference code from https://github.com/zakariachowdhury/streamlit-map-dashboard/blob/main/streamlit_app.py

# running streamlit files in powershell "strealit run app.py"

# '''
# import streamlit as st
# import pandas as pd
# import folium
# from streamlit_folium import st_folium

# APP_TITLE = 'Fraud and Identity Theft Report'
# APP_SUB_TITLE = 'Source: Federal Trade Commission'

# def display_time_filters(df):
#     year_list = list(df['Year'].unique())
#     year_list.sort()
#     year = st.sidebar.selectbox('Year', year_list, len(year_list)-1)
#     quarter = st.sidebar.radio('Quarter', [1, 2, 3, 4])
#     st.header(f'{year} Q{quarter}')
#     return year, quarter

# def display_state_filter(df, state_name):
#     state_list = [''] + list(df['State Name'].unique())
#     state_list.sort()
#     state_index = state_list.index(state_name) if state_name and state_name in state_list else 0
#     return st.sidebar.selectbox('State', state_list, state_index)

# def display_report_type_filter():
#     return st.sidebar.radio('Report Type', ['Fraud', 'Other'])

# def display_map(df, year, quarter):
#     df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]

#     map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')
    
#     choropleth = folium.Choropleth(
#         geo_data='data/us-state-boundaries.geojson',
#         data=df,
#         columns=('State Name', 'State Total Reports Quarter'),
#         key_on='feature.properties.name',
#         line_opacity=0.8,
#         highlight=True
#     )
#     choropleth.geojson.add_to(map)

#     df_indexed = df.set_index('State Name')
#     for feature in choropleth.geojson.data['features']:
#         state_name = feature['properties']['name']
#         feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'State Pop'][0]) if state_name in list(df_indexed.index) else ''
#         feature['properties']['per_100k'] = 'Reports/100K Population: ' + str(round(df_indexed.loc[state_name, 'Reports per 100K-F&O together'][0])) if state_name in list(df_indexed.index) else ''

#     choropleth.geojson.add_child(
#         folium.features.GeoJsonTooltip(['name', 'population', 'per_100k'], labels=False)
#     )
    
#     st_map = st_folium(map, width=700, height=450)

#     state_name = ''
#     if st_map['last_active_drawing']:
#         state_name = st_map['last_active_drawing']['properties']['name']
#     return state_name

# def display_fraud_facts(df, year, quarter, report_type, state_name, field, title, string_format='${:,}', is_median=False):
#     df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]
#     df = df[df['Report Type'] == report_type]
#     if state_name:
#         df = df[df['State Name'] == state_name]
#     df.drop_duplicates(inplace=True)
#     if is_median:
#         total = df[field].sum() / len(df[field]) if len(df) else 0
#     else:
#         total = df[field].sum()
#     st.metric(title, string_format.format(round(total)))

# def main():
#     st.set_page_config(APP_TITLE)
#     st.title(APP_TITLE)
#     st.caption(APP_SUB_TITLE)

#     #Load Data
#     df_continental = pd.read_csv('data/AxS-Continental_Full Data_data.csv')
#     df_fraud = pd.read_csv('data/AxS-Fraud Box_Full Data_data.csv')
#     df_median = pd.read_csv('data/AxS-Median Box_Full Data_data.csv')
#     df_loss = pd.read_csv('data/AxS-Losses Box_Full Data_data.csv')

#     #Display Filters and Map
#     year, quarter = display_time_filters(df_continental)
#     state_name = display_map(df_continental, year, quarter)
#     state_name = display_state_filter(df_continental, state_name)
#     report_type = display_report_type_filter()

#     #Display Metrics
#     st.subheader(f'{state_name} {report_type} Facts')

#     col1, col2, col3 = st.columns(3)
#     with col1:
#         display_fraud_facts(df_fraud, year, quarter, report_type, state_name, 'State Fraud/Other Count', f'# of {report_type} Reports', string_format='{:,}')
#     with col2:
#         display_fraud_facts(df_median, year, quarter, report_type, state_name, 'Overall Median Losses Qtr', 'Median $ Loss', is_median=True)
#     with col3:
#         display_fraud_facts(df_loss, year, quarter, report_type, state_name, 'Total Losses', 'Total $ Loss')        


# if __name__ == "__main__":
#     main()

# '''