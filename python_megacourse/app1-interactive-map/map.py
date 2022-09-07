from distutils import core
from stringprep import map_table_b2
from webbrowser import MacOSX
import folium

import geopy
import os
import pandas
from geopy.geocoders import ArcGIS

import bs4  # FYI this is BeautifulSoup4 they just fucking shorthanded this shit
nom = ArcGIS()

# --------------- Elevation function -----------------------
def elevation(height: float):
    if 0 <= height < 1500:
        print("I should yield green")
        return folium.Icon(color= "green")
    elif 1500<= height < 3000:
        print("I should yield orange")
        return folium.Icon(color= "orange")
    elif 3000 <= height:
        print("I should yield red")
        return folium.Icon(color= "red")
    else:
        print("I should yield blue")
        return folium.Icon(color = "blue")

def elevation_alt(height: float):
    if 0 <= height < 1500:
        return "green"
    elif 1500<= height < 3000:
        return "orange"
    elif 3000 <= height:
        return "red"
    else:
        return "pink"

# Map(location = [latitude, longitude]) also dont forget latitude ranges from -90 to 90 & longitude ranges from -180 to 180
'''
mapsample = folium.Map(location = [38.58,-99.09], zoom_start = 8, tiles = "Stamen Terrain")
mapsample.save("MapSample1.html")
'''
# ps i made geo coordinates for the other sample map combining this part of the lesson & the geopy.geocoders import ArcGIS portion of the other lesson.

'''
https://www.udemy.com/course/the-python-mega-course/learn/lecture/15946138#overview
In the next lecture, I use this in the code:
tiles = "Mapbox Bright"

Please use this instead:
tiles = "Stamen Terrain"

Mapbox Bright and Stamen Terrain are both types of base maps, but Mapbox Bright doesn't work anymore.
Stamen Terrain works great, and you will see it creates a beautiful terrain map.
'''


# original
'''
mapsample2 = folium.Map(location = [29.96830801012382,-90.11122496338153], zoom_start = 6, tiles = "Stamen Terrain")
mapsample2.add_child(folium.Marker(location = [29.968,-90.11], popup = "Hi, I'm a marker", icon = folium.Icon(color = 'green')))
mapsample2.save("MapSample2.html")
'''
# added this after initial creation of mapsample2. instructor suggested we utilize a feature group to add children instead of what we did normally:
'''
mapsample2 = folium.Map(location = [29.96830801012382,-90.11122496338153], zoom_start = 6, tiles = "Stamen Terrain")

fg = folium.FeatureGroup(name = "My Map")
fg.add_child(folium.Marker(location = [29.968,-90.11], popup = "Hi, I'm a marker", icon = folium.Icon(color = 'green')))
mapsample2.add_child(fg)

mapsample2.save("MapSample2.html")
'''
#--------------------Lesson cont.-----------------------
'''
mapsample3 = folium.Map(location = [29.96830801012382,-90.11122496338153],  tiles = "Stamen Terrain")   # I removed zoom_start = 6

fg = folium.FeatureGroup(name = "My Map")

for coordinates in [[29.968, -90.1122], [29.97, -90.1125]]:
    fg.add_child(folium.Marker(location = coordinates, popup = "Hi, I'm a marker", icon = folium.Icon(color = 'blue')))

mapsample3.add_child(fg)

mapsample3.save("MapSample3.html")
'''

#----------------Volcano coord from .txt---------------------
# instructions on how to perform a google search from python: https://www.geeksforgeeks.org/performing-google-search-using-python-code/

# small note to self, if you try to use a comma to link a str path you saved elsewhere to another str to specify a file, it will fail. you need to use a + instead
# BAD: data = pandas.read_csv(directory, "/Webmap_datasources/Volcanoes.txt") 🚫🚫🚫
# GOOD: data = pandas.read_csv(directory + "/Webmap_datasources/Volcanoes.txt") ✔✔✔
directory_ = os.getcwd()
data = pandas.read_csv(directory_ + "/Webmap_datasources/Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

#html = """<h4>Volcano information:</h4> Height: %s m"""
html = """
<h4>Volcano name: </h4><br>
<a href = https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map_volcanoes = folium.Map(location = (lat[0],lon[0]), tiles = "Stamen Terrain")
fg = folium.FeatureGroup(name = "My Map of Volcanic Activity")
for lt, ln, el, name in zip(lat,lon, elev, name):
    iframe = folium.IFrame(html = html % (name, name, el), width = 200, height=100)
    # https://fontawesome.com/v4/examples/
    # as this site explains you can modify the icons with other "fa-" commands like "fa-spin", "fa-lg", "fa-pull-left fa-border" (yes some commands can be combined)
    # to use font awesome vs default icon... use this format: folium.Marker(location, icon = folium.Icon(color = "green", icon = "hamburger", prefix = 'fa'))
    fg.add_child(folium.CircleMarker(
        location = (lt,ln),
        popup = folium.Popup(iframe),
        fill_color = elevation_alt(el),
        color = "pink",
        fill_opacity = 0.7
    ))  #icon = elevation(el)
    # finally got it working... but i still prefer fa's: "hand-peace-o fa-spin" lol
    
    '''
    fg.add_child(folium.Marker(
        location = (lt,ln),
        popup = folium.Popup(iframe),
        icon = folium.Icon(color = "black", icon_color = "#0CFFD1", icon = "circle-o fa-spin", prefix = 'fa')
        # yes you can even use html color codes for the icon_color, color is restricted however
        #icon = folium.Icon(icon = "hand-peace-o fa-spin", prefix = 'fa') # ps this worked
    ))
    '''

fg.add_child(folium.GeoJson())

map_volcanoes.add_child(fg)
map_volcanoes.save("Map_population_json.html")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ My unguided code attempts ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
#--------------------My abomination # 1-----------------------

mapsampleVal = folium.Map(location = [29.96830801012382,-90.11122496338153],  tiles = "Stamen Terrain")   # I removed zoom_start = 6

fgVal = folium.FeatureGroup(name = "My Map")

for coordinates in [[29.968, -90.1122], [29.97, -90.1125]]:
    result = nom.reverse(f"{coordinates[0]}, {coordinates[1]}")
    fgVal.add_child(folium.Marker(location = coordinates, popup = f"Hi, I'm a marker @ {result}", icon = folium.Icon(color = 'pink')))

mapsampleVal.add_child(fgVal)

mapsampleVal.save("MapValerius1.html")

#--------------------My abomination #2 [Volcano.txt lesson]-----------------------
# YAY I FIGURED OUT A (not THE) SOLUTION MYSELF (and thanks to StackOverflow + Google ahaha...)
# anyway this version of the answer that i devised I converted the data frame columns for LAT and LON into a dict and then back into a separate dataframe
# in reality i should just either make a new DF with the important info alone, or directly pull the data from the original DF. BUT i wanted to learn the process of
# moving the data types around a bit more so i did it like a neanderthal

directory_vol = os.getcwd()
dataVol = pandas.read_csv(directory_vol + "/Webmap_datasources/Volcanoes.txt")
col_names = ["LAT", "LON"] # aka key in a dict
col_values_A = [] # aka value in a dict
col_values_B = [] # aka value in a dict

# https://stackoverflow.com/questions/15125343/how-to-iterate-through-two-pandas-columns
# https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-then-filling-it ✨ NEVER GROW A DATAFRAME, just build the data in a list or dict first. THEN move it to dataframe
for x,y in zip(dataVol["LAT"], dataVol["LON"]):
    col_values_A.append(x)
    col_values_B.append(y)

vital_data = {
    "LAT": col_values_A,
    "LON": col_values_B
}

vital_data_as_df = pandas.DataFrame(vital_data)
print("✨✨ Here is your dataframe! ✨✨\n", vital_data_as_df)


myVolcanoSample1 = folium.Map(location = [29.96830801012382,-90.11122496338153],  tiles = "Stamen Terrain")   # I removed zoom_start = 6

fg = folium.FeatureGroup(name = "My Volcano-Sample#1 Map")

for coordinates in zip(vital_data_as_df["LAT"], vital_data_as_df["LON"]):
    # print("The coordinates:\n", coordinates[0], coordinates[1])           # Worked after i used zip() in the loop for the "LAT" & "LON" columns
    fg.add_child(folium.Marker(location = (coordinates[0],coordinates[1]), popup = f"Volcano Here! {coordinates}", icon = folium.Icon(color = 'red')))

myVolcanoSample1.add_child(fg)

myVolcanoSample1.save("MyVolcanoSampleMap1.html")
'''

# playing with google search from python
# not all of this is helpful, but still... https://www.geeksforgeeks.org/performing-google-search-using-python-code/
'''
from googlesearch import search
for goog in search("chonk trash pandas", num_results = 10):
    print(goog)
'''
# worked

