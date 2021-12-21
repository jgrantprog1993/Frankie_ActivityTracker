#################
# Name: Jason Grant
# ID: 12430732
# Description: IOT Assignment 2: Folium, creates html file that includes a MAP Then overlays the JSON coordinates onto the map
#################
import os
import folium 

map = folium.Map(location=[52.162787684017104, -7.001080513000488],zoom_start=15)   ## Creates the starting place of the map and its zoom level.
dogActivityData = os.path.join('map1.geojson')                                      

folium.GeoJson(dogActivityData, name='Test').add_to(map)                            ##Overlays the map with the points

map.save("map.html")                                                                ##saves it as "map.html"