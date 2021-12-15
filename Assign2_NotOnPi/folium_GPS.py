import os
import folium 

map = folium.Map(location=[52.162787684017104, -7.001080513000488],zoom_start=15)
dogActivityData = os.path.join('Test_json_gps.json')

folium.GeoJson(dogActivityData, name='Test').add_to(map)

map.save("index.html")