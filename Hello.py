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
    return distance

def run():
  st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

  df = pd.read_csv("data.csv", sep=",")

  print(df["Nom"].nunique())

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
          
          
          df['distance'] = df.apply(haversine_distance, args=(lat, lon), axis=1)
          map_data = df[df.distance < 1000]
          
          if map_data["distance"].min() < 50:
            # Le réseau d'énergie thermique $$$ $$$$$ passera à côté de chez vous. Il est très probable que vous puissiez vous connecter. Contactez-nous pour entammer les démarches de connexion au réseau.
            st.success(f"Le réseau d'énergie thermique **{map_data['Nom'].iloc[0]}** passera à côté de chez vous. Il est très probable que vous puissiez vous connecter. [Contactez-nous](https://www.karno.energy/contact/) pour entammer les démarches de connexion au réseau.") #OLD = Le réseau de chaleur **" + map_data["Nom"].iloc[0] + "** passera chez vous. N'hésitez pas à contacter Karno pour toute question.")
          elif map_data["distance"].min() < 500:
            # Le réseau d'énergie thermique $$$ $$$$$ est en cours de développement dans votre quartier. Vous n'êtes pas situé le long du tracé prévu mais n'hésitez à nous contacter pour évaluer la possibilité d'une extension de réseau.
            st.info(f"Le réseau d'énergie thermique **{map_data['Nom'].iloc[0]}** est en cours de développement dans votre quartier. Vous n'êtes pas situé le long du tracé prévu mais n'hésitez à [nous contacter](https://www.karno.energy/contact/) pour évaluer la possibilité d'une extension de réseau.") # OLD=Le réseau de chaleur **" + map_data["Nom"].iloc[0] + "** passera proche de chez vous. N'hésitez pas à contacter Karno pour toute question.")
          elif map_data["distance"].min() < 2000:
            st.info(f"Le réseau d'énergie thermique **{map_data['Nom'].iloc[0]}** est en cours de développement à proximité de chez vous. Il ne passe malheureusement pas encore dans votre quartier. Si vous êtes un grand consommateurs/producteur d'énergie thermique, [contactez-nous](https://www.karno.energy/contact/), on peut envisager une extension du réseau.")
          else: 
            st.info("Aucun réseau d'énergie thermique n'est en cours de développement à proximité de chez vous. Pour vous tenir au courant de nos prochains réseaux, n'hésitez pas à nous suivre sur [Linkedin](https://be.linkedin.com/company/karno-energy). De plus, contactez-nous si vous pensez que votre quartier bénéficierait d'un réseau de chaleur.") # OLD = Aucun réseau de chaleur ne passera proche de chez vous.")

          if len(map_data) > 0:
            st.markdown(''' 
                        #### Légende
                     - votre addresse en :blue[bleu]  
                     - le réseau de chaleur Karno en :red[rouge]''')
          
              # Creating a new row to append
            new_row = {'distance': 0, 'Lat': lat, "Long": lon, 'Rayon': 50}
            map_data = map_data.rename(columns={"Lat": "lat", "Long": "lon"})
            map_data["size"] = 5
            map_data["color"] = [[250,0,0,0.2]] * len(map_data)

            map_data = map_data.reset_index()
            map_data.loc[len(map_data),:] = {"lat": lat, "lon": lon, "Nom": "Test", "distance": 0, "size": 20, 'Rayon': 50, "color": [0,0,250, 0.8]}#{"lat": lat, "lon": lon, "Nom": "Test", "distance": 0,  'Rayon': 50, "size": 10, "color": [0,0,250, 0.8]}

            st.map(map_data[["lat", "color", "lon", "size"]], zoom=13, size="size", color="color")
            
          else:
            st.map(pd.DataFrame([{"lat": lat, "lon": lon, "Nom": "Test", "distance": 0,  'Rayon': 50}]), zoom=13)

          # st.write("")
                      # - :red[le réseau Karno]")




if __name__ == "__main__":
    run()
