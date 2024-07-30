# Going to try using a combo of:
# https://developers.google.com/maps/documentation/places/web-service/client-libraries#python
# https://github.com/googleapis/google-cloud-python/tree/main/packages/google-maps-places

# Making sure you install package to venv location:
# py -m venv <your-env>
# .\<your-env>\Scripts\activate
# pip install google-maps-places
# pip install --upgrade google-maps-places - dont think i need this one

# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html

from google.maps import places_v1
import json
import dotenv # pip install python-dotenv
import os
dotenv.load_dotenv()  #(dotenv_path='/.venv/.env')

places_api_key = os.getenv('bioeconomyweb_google_api_key', 'None') # 2nd argument not necessary 

# SearchTextRequest
def sample_search_text():

    
    # Create a client
    # client = places_v1.PlacesClient()
    client = places_v1.PlacesClient(
    client_options={"api_key": places_api_key}
    )

    # Initialize request argument(s)
    request = places_v1.SearchTextRequest(
        # text_query="text_query_value", # original query
        text_query="Ginkgo Bioworks Boston"
    )

    fieldMask = "places.id,places.formattedAddress,places.location" #places.location.latitude,places.location.longitude"        # "*" - returns all fields

    # Make the request
    response = client.search_text(
        request=request,
        metadata=[("x-goog-fieldmask",fieldMask)]
        )

    # Handle the response
    return response


test_goog = sample_search_text()

# I have working code here that pulls out the id, formatted address, and location, need to think about how I want to store these things to associate later...

# Going to parse the output so that it becomes a list: id, formatted address, latitude, longitude

places_out_list = [
    test_goog.places[0].id, 
    test_goog.places[0].formatted_address, 
    test_goog.places[0].location.latitude,
    test_goog.places[0].location.longitude
    ]







'''
Going to push the sample output to further down this page because it is very large.

The big takeaway is that I probably only need the "formatted_address" and maybe the "id" values...

Wait, the output has lat/lon values as well, in the form of a dict:

#   location {
#     latitude: 42.3443804
#     longitude: -71.0279912
#   }

Also seems to have a "website_uri" value that could be useful...

Looks like fieldMask could also be defined as such:

fieldMask = "formattedAddress,displayName"

in which case, I'm going to try changing it from "*" to "places,formattedAddress,location". 
That doesnt work immediately, going to just take the big output and try to filter.

test_goog.places[0].address_components[0].long_text = 8th floor --> works
test_goog.places[0].address_components[1].long_text = 27

test_goog.places[0].name works. ok, we're cooking now

https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places

from the basic test_goog output

I think I would want something along the lines of...

test_goog = sample_search_text()

desired_outputs = [
    test_goog.places[0].id = PlaceID unique identifier
    test_goog.places[0].formatted_address = full address that i want
    test_goog.places[0].location.latitude = float value
    test_goog.places[0].location.longitude = float value
    ]

'''



# Example output of function when querying for "Ginkgo Bioworks" - print(response)

# places {
#   name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0"
#   id: "ChIJ00DqaZ5644kRuYGl-y78Ax0"
#   types: "point_of_interest"
#   types: "establishment"
#   national_phone_number: "(877) 422-5362"
#   international_phone_number: "+1 877-422-5362"
#   formatted_address: "27 Drydock Ave 8th Floor, Boston, MA 02210, USA"
#   address_components {
#     long_text: "8th Floor"
#     short_text: "8th Floor"
#     types: "subpremise"
#     language_code: "en"
#   }
#   address_components {
#     long_text: "27"
#     short_text: "27"
#     types: "street_number"
#     language_code: "en-US"
#   }
#   address_components {
#     long_text: "Drydock Avenue"
#     short_text: "Drydock Ave"
#     types: "route"
#     language_code: "en"
#   }
#   address_components {
#     long_text: "D Street / West Broadway"
#     short_text: "D Street / West Broadway"
#     types: "neighborhood"
#     types: "political"
#     language_code: "en"
#   }
#   address_components {
#     long_text: "Boston"
#     short_text: "Boston"
#     types: "locality"
#     types: "political"
#     language_code: "en"
#   }
#   address_components {
#     long_text: "Suffolk County"
#     short_text: "Suffolk County"
#     types: "administrative_area_level_2"
#     types: "political"
#     language_code: "en"
#   }
#   address_components {
#     long_text: "Massachusetts"
#     short_text: "MA"
#     types: "administrative_area_level_1"
#     types: "political"
#     language_code: "en"
#   }
#   address_components {
#     long_text: "United States"
#     short_text: "US"
#     types: "country"
#     types: "political"
#     language_code: "en"
#   }
#   address_components {
#     long_text: "02210"
#     short_text: "02210"
#     types: "postal_code"
#     language_code: "en-US"
#   }
#   plus_code {
#     global_code: "87JC8XVC+QR"
#     compound_code: "8XVC+QR Boston, MA, USA"
#   }
#   location {
#     latitude: 42.3443804
#     longitude: -71.0279912
#   }
#   viewport {
#     low {
#       latitude: 42.3431585697085
#       longitude: -71.029295680291511
#     }
#     high {
#       latitude: 42.3458565302915
#       longitude: -71.026597719708491
#     }
#   }
#   rating: 4.9
#   google_maps_uri: "https://maps.google.com/?cid=2090791930750665145"
#   website_uri: "http://ginkgobioworks.com/"
#   utc_offset_minutes: -240
#   adr_format_address: "<span class=\"street-address\">27 Drydock Ave 8th Floor</span>, <span class=\"locality\">Boston</span>, <span class=\"region\">MA</span> <span class=\"postal-code\">02210</span>, <span class=\"country-name\">USA</span>"
#   business_status: OPERATIONAL
#   user_rating_count: 28
#   icon_mask_base_uri: "https://maps.gstatic.com/mapfiles/place_api/icons/v2/generic_pinlet"
#   icon_background_color: "#7B9EB0"
#   display_name {
#     text: "Ginkgo Bioworks"
#     language_code: "en"
#   }
#   short_formatted_address: "The Innovation and Design Building, 27 Drydock Ave 8th Floor, Boston"
#   reviews {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/reviews/ChZDSUhNMG9nS0VJQ0FnSUN6MHFmQmZnEAE"
#     relative_publish_time_description: "a month ago"
#     rating: 5
#     text {
#       text: "You know what I feel hurts our stock?  Seeing Che Austin selling 3968 shares every day."
#       language_code: "en"
#     }
#     original_text {
#       text: "You know what I feel hurts our stock?  Seeing Che Austin selling 3968 shares every day."
#       language_code: "en"
#     }
#     author_attribution {
#       display_name: "Hammer44Time"
#       uri: "https://www.google.com/maps/contrib/107396412870297499066/reviews"
#       photo_uri: "https://lh3.googleusercontent.com/a-/ALV-UjVrbVq1t1NDwO9dUHRbTGDnp0Im-H_BPu3lb125hwy-Ez88ZD0c=s128-c0x00000000-cc-rp-mo"
#     }
#     publish_time {
#       seconds: 1717205231
#     }
#   }
#   reviews {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/reviews/ChZDSUhNMG9nS0VJQ0FnSUNkMXBqcUZREAE"
#     relative_publish_time_description: "5 months ago"
#     rating: 5
#     text {
#       text: "Excellent company, and tremendous innovative intellect going out of this place, wow!"
#       language_code: "en"
#     }
#     original_text {
#       text: "Excellent company, and tremendous innovative intellect going out of this place, wow!"
#       language_code: "en"
#     }
#     author_attribution {
#       display_name: "Tyron Pain"
#       uri: "https://www.google.com/maps/contrib/111304747471839616562/reviews"
#       photo_uri: "https://lh3.googleusercontent.com/a-/ALV-UjUnlGWv_dy_JCImxIC-fV9PBx_egOxmPHLydHrOwY6cqnzmn1Av=s128-c0x00000000-cc-rp-mo-ba3"
#     }
#     publish_time {
#       seconds: 1707963460
#     }
#   }
#   reviews {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/reviews/ChdDSUhNMG9nS0VJQ0FnSURodEx2SzFBRRAB"
#     relative_publish_time_description: "a year ago"
#     rating: 5
#     text {
#       text: "Nothing like I have ever seen.....and have seen the best. Investing wasn\'t even a second thought  Very impressive.  Proves we have a better future seeing their research!!! Buy DNA!!!"
#       language_code: "en"
#     }
#     original_text {
#       text: "Nothing like I have ever seen.....and have seen the best. Investing wasn\'t even a second thought  Very impressive.  Proves we have a better future seeing their research!!! Buy DNA!!!"
#       language_code: "en"
#     }
#     author_attribution {
#       display_name: "Becky Lively"
#       uri: "https://www.google.com/maps/contrib/112735217939300484619/reviews"
#       photo_uri: "https://lh3.googleusercontent.com/a-/ALV-UjWfh3SX-MG3jh-hMnBaBNwlfpFd_csN_n0j-VRImtDtJDlhemwS9g=s128-c0x00000000-cc-rp-mo"
#     }
#     publish_time {
#       seconds: 1677775945
#     }
#   }
#   reviews {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/reviews/ChdDSUhNMG9nS0VJQ0FnSURlaFk2MG53RRAB"
#     relative_publish_time_description: "a year ago"
#     rating: 5
#     text {
#       text: "I Love investing in this company. Hoping to one day visit this out of this world awesome company! 😁"
#       language_code: "en"
#     }
#     original_text {
#       text: "I Love investing in this company. Hoping to one day visit this out of this world awesome company! 😁"
#       language_code: "en"
#     }
#     author_attribution {
#       display_name: "Daniel Carrasco"
#       uri: "https://www.google.com/maps/contrib/102853430099360100377/reviews"
#       photo_uri: "https://lh3.googleusercontent.com/a/ACg8ocLkiTCK2j1kv_nmfs2wCusNxMVaSTbrosxIDw-BFAkmdQ5V_Q=s128-c0x00000000-cc-rp-mo-ba2"
#     }
#     publish_time {
#       seconds: 1665778253
#     }
#   }
#   reviews {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/reviews/ChdDSUhNMG9nS0VJQ0FnSUR5ek1tRHBnRRAB"
#     relative_publish_time_description: "3 years ago"
#     rating: 5
#     text {
#       text: "Wish I worked here. Great place; the best people!"
#       language_code: "en"
#     }
#     original_text {
#       text: "Wish I worked here. Great place; the best people!"
#       language_code: "en"
#     }
#     author_attribution {
#       display_name: "Sam Stoney"
#       uri: "https://www.google.com/maps/contrib/103199972406338497238/reviews"
#       photo_uri: "https://lh3.googleusercontent.com/a-/ALV-UjXV1ObqFQe-p6j5ANyh550wsYbXsD2wLmQWWOBta22Co4-P_Sns=s128-c0x00000000-cc-rp-mo"
#     }
#     publish_time {
#       seconds: 1614364915
#     }
#   }
#   photos {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/photos/AelY_Cuiey4CM4JrvIX9eyKrSHqYqYaIk4jipnboFQuURR6EzzTQx1aIw3h-tkj4zMxguGbMRfN4Oe4FB2lwjf9QP1leeUgF-5-HGl0UcaLgWckglTT0HLkOLhdJDfVaUVVJ5y9_O4W0kD9--RLcz81kppCXGBtYJafQNAA7"
#     width_px: 2500
#     height_px: 1667
#     author_attributions {
#       display_name: "Ginkgo Bioworks"
#       uri: "//maps.google.com/maps/contrib/105877492608314770619"
#       photo_uri: "//lh3.googleusercontent.com/a-/ALV-UjVpcS8JC7CFSH46fVaq6ZdA9f6BhyMimNAx4_vjwGbvu0-iIeA=s100-p-k-no-mo"
#     }
#   }
#   photos {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/photos/AelY_Cs01sV7GBk6kPgjQeI9gkMS-Kfeitr7oprolnOpfxQfuJR_xv-a4dUgLPRFdI8mkeBSRUTD5uUlwC7m4NErXmgEsLyLS4g4Le_pRDZyI0ifxcNRHGhf89jF3mAiMFUZa-qNjbnRnhFwzIUhCjlj_ALdqqxneZzvvLCb"
#     width_px: 3024
#     height_px: 4032
#     author_attributions {
#       display_name: "Philippe Prochasson"
#       uri: "//maps.google.com/maps/contrib/111613955991619328538"
#       photo_uri: "//lh3.googleusercontent.com/a-/ALV-UjXLMy9hH8JpmbQj4OxU0u1_zWw33b3QlB0rkE9akDYzO3M5dzw0Nw=s100-p-k-no-mo"
#     }
#   }
#   photos {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/photos/AelY_CvxwQxR8D7n15q1cMnIkuVKyjCV4VizqZ6zS2DX8wQvtAk51HLQytyoQ-YLIzlyxpyjax51vCuMYCLae-93BSOjnwmse1rHxyHqLdqOae2wkVD3QXv7iDuGJRdzIFVqlyLf9m_pWkPQZW4TfWUl5LJncdc0kh8AQlUA"
#     width_px: 3024
#     height_px: 4032
#     author_attributions {
#       display_name: "Philippe Prochasson"
#       uri: "//maps.google.com/maps/contrib/111613955991619328538"
#       photo_uri: "//lh3.googleusercontent.com/a-/ALV-UjXLMy9hH8JpmbQj4OxU0u1_zWw33b3QlB0rkE9akDYzO3M5dzw0Nw=s100-p-k-no-mo"
#     }
#   }
#   photos {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/photos/AelY_CtE0_eX5TyDsr4n_O_CvKpLm5xUpN-2ax0GC8Cxnakf_5I3-ZAw9PCtpQt7Lg9dgwN-wnMlVC8ZwLL4OLdab3Q1MXQ5mK5BMJWrYXRe73amrT_F4LGiVxCQxWj3Dmaj89nXdzDhCcrbK8qRxDAjS0BoxxyYhVmvkoPO"
#     width_px: 3024
#     height_px: 4032
#     author_attributions {
#       display_name: "Philippe Prochasson"
#       uri: "//maps.google.com/maps/contrib/111613955991619328538"
#       photo_uri: "//lh3.googleusercontent.com/a-/ALV-UjXLMy9hH8JpmbQj4OxU0u1_zWw33b3QlB0rkE9akDYzO3M5dzw0Nw=s100-p-k-no-mo"
#     }
#   }
#   photos {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/photos/AelY_Cs5ANg0qY5IkBTyOFUymfMa6QY-dlcXrEK3W4SiJRmwO4IyTSWxFu3vI_TwEvp3nyfIO-tzLvhWx8TfPS6o6uPsCltruWouvl_p0OJGSN7m-y7Gnj6bY5N4ktJS32kFUQzweH9sQI2ZoHQ0nuhHPV0Dh2wf7kyhskTz"
#     width_px: 4032
#     height_px: 3024
#     author_attributions {
#       display_name: "Philippe Prochasson"
#       uri: "//maps.google.com/maps/contrib/111613955991619328538"
#       photo_uri: "//lh3.googleusercontent.com/a-/ALV-UjXLMy9hH8JpmbQj4OxU0u1_zWw33b3QlB0rkE9akDYzO3M5dzw0Nw=s100-p-k-no-mo"
#     }
#   }
#   accessibility_options {
#     wheelchair_accessible_parking: true
#     wheelchair_accessible_entrance: true
#   }
# }
# contextual_contents {
#   reviews {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/reviews/ChZDSUhNMG9nS0VJQ0FnSURlMXF2NVlnEAE"
#     relative_publish_time_description: "a year ago"
#     rating: 5
#     text {
#       text: "Massive technology with top notch employees."
#       language_code: "en"
#     }
#     original_text {
#       text: "Massive technology with top notch employees."
#       language_code: "en"
#     }
#     author_attribution {
#       display_name: "Jeanne Smith"
#       uri: "https://www.google.com/maps/contrib/103857191846400961760/reviews"
#       photo_uri: "https://lh3.googleusercontent.com/a-/ALV-UjXtgZFsEjH1w7_MteORwwNOgtk0RhrH1vs1EXdFl1E58inW5Ox5=s128-c-c0x00000000-cc-rp-mo-ba3-br100"
#     }
#     publish_time {
#       seconds: 1665344330
#     }
#   }
#   photos {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/photos/AelY_Cs573EWQSs7lcHySeyu2FDQu38_4uzOWKZXf4W5OXuBSKiN_qEZhKZDqHMRdBXM5YfQqgo0Qe6_7oJeNUzLyKp172nUSeTexwCrpxSF8ehXD122vygeq4_J-JJ2DrN51Fn-BWVhtox1AFWqf3NdWGRDuDPgdoeaE6MG"
#     width_px: 2500
#     height_px: 1667
#     author_attributions {
#       display_name: "A Google User"
#       uri: "//maps.google.com/maps/contrib/105877492608314770619"
#       photo_uri: "//lh3.googleusercontent.com/a-/ALV-UjVpcS8JC7CFSH46fVaq6ZdA9f6BhyMimNAx4_vjwGbvu0-iIeA=s100-p-k-no-mo"
#     }
#   }
#   photos {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/photos/AelY_CudHuFgvHnvQr0KZ40jMEyt6ipq04yoFwEyqFLcgPi-KrGO7KcYXboMDYyvXUZoubLzHUSUqDHHWM_WXPryMZu00wy0wjpD9QCDQdSVQYXjW6dIpMlyR70k14_Kcb51G_xchvvIpxp7p93wriLOtu6bfKmy41EfOI1F"
#     width_px: 3024
#     height_px: 4032
#     author_attributions {
#       display_name: "Philippe Prochasson"
#       uri: "//maps.google.com/maps/contrib/111613955991619328538"
#       photo_uri: "//lh3.googleusercontent.com/a-/ALV-UjXLMy9hH8JpmbQj4OxU0u1_zWw33b3QlB0rkE9akDYzO3M5dzw0Nw=s100-p-k-no-mo"
#     }
#   }
#   photos {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/photos/AelY_CtQtUUSM5zZXG7LCcZ02MF9vzkkXBgHPpmzdS5485-bcJgZK8scrP963b4LRNWxGtaCcIGrC4qE2OKGMU3-Q8upyaqrXWZAMXQ4ImiQgGghao-8SN0NlmRmWp6faiXUYo6w27LkgYdNaoEHhwhKB6QaCF8cGKB1FE6o"
#     width_px: 3024
#     height_px: 4032
#     author_attributions {
#       display_name: "Philippe Prochasson"
#       uri: "//maps.google.com/maps/contrib/111613955991619328538"
#       photo_uri: "//lh3.googleusercontent.com/a-/ALV-UjXLMy9hH8JpmbQj4OxU0u1_zWw33b3QlB0rkE9akDYzO3M5dzw0Nw=s100-p-k-no-mo"
#     }
#   }
#   photos {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/photos/AelY_CvpQXwxMO7anzan7aHZHx5gU8NtQPZhLV0iKyli6cFklx3eu_OiTAWaGIlXyJmtxsY21iWVINEpMReWYJw84kXT1Lc1sfD9oF2Z97arVTOFNz0KpC5E-P3iAW02LoiKyh1LhUjA2em-NWZqZfiO9iyL85enTnFvzeHM"
#     width_px: 3024
#     height_px: 4032
#     author_attributions {
#       display_name: "Philippe Prochasson"
#       uri: "//maps.google.com/maps/contrib/111613955991619328538"
#       photo_uri: "//lh3.googleusercontent.com/a-/ALV-UjXLMy9hH8JpmbQj4OxU0u1_zWw33b3QlB0rkE9akDYzO3M5dzw0Nw=s100-p-k-no-mo"
#     }
#   }
#   photos {
#     name: "places/ChIJ00DqaZ5644kRuYGl-y78Ax0/photos/AelY_CvvIsil0JGbJNjEvXW_7Hce65tRctAyUd7pP5N0ovkBOemFnkPYuZQCTOD9ZHtcYlBl4goTBhZ0ChvIVAXBqqN6WtSskTrpg7XhQvKEM3-__ml5Pp2NucRROB1vBSjS3qOCRxNctZpYRWlsiW3666PkIQydn6zo0-1Z"
#     width_px: 4032
#     height_px: 3024
#     author_attributions {
#       display_name: "Philippe Prochasson"
#       uri: "//maps.google.com/maps/contrib/111613955991619328538"
#       photo_uri: "//lh3.googleusercontent.com/a-/ALV-UjXLMy9hH8JpmbQj4OxU0u1_zWw33b3QlB0rkE9akDYzO3M5dzw0Nw=s100-p-k-no-mo"
#     }
#   }
# }


# # GetPlaceRequest
# def sample_get_place():
#     # Create a client
#     client = places_v1.PlacesClient()

#     # Initialize request argument(s)
#     request = places_v1.GetPlaceRequest(
#         name="name_value",
#     )

#     # Make the request
#     response = client.get_place(request=request)

#     # Handle the response
#     print(response)




    # I think the following code from https://github.com/googleapis/google-cloud-python/blob/main/packages/google-maps-places/samples/generated_samples/snippet_metadata_google.maps.places.v1.json
    # yields an example output that will show me how to work with the outputs of the API call























###############################################################################################################
# Following code works off of - https://medium.com/@ayendra4/automate-finding-the-location-of-a-business-using-google-maps-api-755a30023c57

# import googlemaps # pip install google maps
# from geopy.geocoders import Nominatim # pip install geopy
# import pandas as pd # pip install pandas

# # Step 3 — Create a Google Maps service client. 

# map_client = googlemaps.Client(API_KEY)

# # Step 4 — Create a Nominatim user agent. 

# '''
# Nominatim utilizes OpenStreetMap data to perform geocoding, enabling the identification of Earth’s 
# locations based on their names and addresses. Furthermore, it can perform the inverse function, 
# providing addresses for any given location anywhere on the planet.
# '''

# geolocator = Nominatim(user_agent="geoapiExercises")

# # Step 5 — Read row by row from the company list .csv file and feed to the Google API and get the search results.

# for index, row in df.iterrows():
#     # skip the first row since its the title row
#     if index==0:
#         continue
#     try:
#         company_name = row["company_name"]
#         response = map_client.places(query=company_name)
#         results = response.get('results')


# # Step 6 — Extract longitude and latitude values from the response.

# lat = results[0]['geometry']['location']['lat']
# lng = results[0]['geometry']['location']['lng']

# # Output shall look like as follows,
# # latitude 28.6542057
# # logitude 77.1286914

# # Step 7 — Get the correspondent location. 

# location = geolocator.reverse(f'{lat}, {lng}')

# # xample output - Bali Nagar, Patel Nagar Tehsil, West Delhi District, Delhi, 110026, India

# country_code = location.raw['address']["country_code"]

# # convert country code to country name

# def get_country(country_code):
#     country = pytz.country_names[country_code]
#     return country

# # Step 8 — Write data to a pandas dataframe.

# results_df = pd.DataFrame(columns=['company_name','country_code','country'])
# results_df.loc[index] = [company_name,country_code, country_name]

# # write dataframe to a .csv file

# results_df.to_csv("client_list.csv", sep='\t', encoding='utf-8')
