# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from shapely.geometry import Point, Polygon
import geopandas as gpd
import pandas as pd
import geopy
import googlemaps
from math import radians, sin, cos, sqrt, atan2

from st_keyup import st_keyup

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def haversine_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in meters
    R = 6371000.0
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Calculate differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # Calculate the distance
    distance = R * c
    
    return distance

def run():
  st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )


  # street = st.sidebar.text_input("Street", "75 Bay Street")
  # city = st.sidebar.text_input("City", "Toronto")
  # province = st.sidebar.text_input("Province", "Ontario")
  # country = st.sidebar.text_input("Country", "Canada")

  # geolocator = Nominatim(user_agent="GTA Lookup")
  # # geocode = RateLimiter(geolocator.geocode, min_delay_seconds=5)
  # location = geolocator.geocode(street+", "+city+", "+province+", "+country)

  # lat = location.latitude
  # lon = location.longitude

  # map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})

  # st.map(map_data)

  api_key = "AIzaSyAOi5CosdhIJItpyKFjD4jzXmV_MWNj-HA"
  gmaps = googlemaps.Client(key=api_key)

  def autocomplete_address(query):
      result = gmaps.places_autocomplete(query, components={'country': "BE"})
      return result

  # df = pd.DataFrame([{"lat": 50.847671, "lon": 4.412759, "radius": 600,"color": (200,150,50,0.3)},  {"lat": 50.727671, "lon": 4.412759, "radius": 50, "color": (255,50,50,1.0)}])
  # st.dataframe(df)
  # st.map(df, size="radius", color="color")
  st.markdown(
      """
      ## Les prochains réseaux de chaleurs Karno proche de chez moi

      **👇 Introduisez votre adresse ci-dessous**
    """
  )

  # address_query = st.text_input("Entrez votre adresse", "")
  address_query = st_keyup("Entrez votre addresse", key="0")


  # Display autocomplete suggestions
  if address_query:
      suggestions = autocomplete_address(address_query)
          
      # Display clickable list of places
      selected_place = st.selectbox("Nous avons trouvé les adresses suivantes:", suggestions, format_func=lambda place: place['description'])

      # Show selected place details
      if selected_place:
          
          # Extract latitude and longitude from the selected place
          location = gmaps.place(selected_place['place_id'])['result']['geometry']['location']
          lat, lon = location['lat'], location['lng']
          
          distance = haversine_distance(lat, lon, 50.847732, 4.414955)
          st.markdown("distance "+ str(int(distance))+"m")
          # Display the map centered around the selected place
          map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})

        # Display the map centered around the selected place
          st.map(map_data, zoom=13, size=30, color=(200,30,30,1.0))





if __name__ == "__main__":
    run()
