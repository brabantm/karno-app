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
import pandas as pd
import googlemaps
from math import radians, sin, cos, sqrt, atan2

from st_keyup import st_keyup
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def haversine_distance(row, lat2, lon2):
    # Radius of the Earth in meters
    R = 6371000.0
    lat1 = row["Lat"]
    lon1 = row["Long"]
    
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
    print(distance)
    return distance

def run():
  st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

  df = pd.read_csv("data.csv", sep=";")


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
          
          match = ""
          match_min_distance = 10000
          df['distance'] = df.apply(haversine_distance, args=(lat, lon), axis=1)
          print(df.sort_values("distance").iloc[0]["Nom"])
          map_data = df.where(df.distance < 150).dropna(how="all")
          # Creating a new row to append
          new_row = {'distance': 0, 'Lat': lat, "Long": lon, 'other_column': 'D'}
          map_data = map_data.rename(columns={"Lat": "lat", "Long": "lon"})
          print(len(map_data))
          # map_data["color"] = list([250,0,0])
          new_df = pd.DataFrame([{"lat": lat, "lon": lon, "color": "rgb(0,250,0)"}])
          # st.dataframe(map_data)
          # map_data = map_data.append(new_row, ignore_index=True)
          # for index,row in df.iterrows():
          #   distance = haversine_distance()
          #   if distance < row["Rayon"]:
          #     if distance < match_min_distance:
          #       match = row["Nom"] if row["Nom"] != match else match
          #       match_min_distance = distance if distance < match_min_distance else match_min_distance

          st.info("Le réseau de chaleur **" + map_data["Nom"][0] + "** passera proche de chez vous. N'hésitez pas à contacter Karno pour toute question.")
            # st.markdown(distance)
          # st.markdown("distance "+ str(int(distance))+"m")
          # Display the map centered around the selected place
          # map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})

        # Display the map centered around the selected place
          st.map(map_data, zoom=13, size=10)





if __name__ == "__main__":
    run()
