import requests
import folium

response = requests.post('http://ip-api.com/batch',json = [
    {"query":"142.250.182.238"},
    {"query":"190.225.183.7"},
    {"query":"108.159.15.106"},
    {"query":"142.250.77.99"},
    {"query":"23.200.48.132"},
    {"query":"134.178.64.211"},
    {"query":"18.161.111.128"},
    {"query":"13.248.195.120"},
    {"query":"49.44.79.236"},
    {"query":"41.33.95.166"},
    {"query":"52.223.34.187"},
    {"query":"133.237.16.234"},
    {"query":"205.210.17.179"},
    {"query":"3.222.89.33"},
    {"query":"52.223.48.227"},
    {"query":"52.28.232.213"},
    {"query":"77.88.55.50"},
    {"query":"217.20.147.1"},
]).json()

lat = []
lon = []
org = []

for ip in response:
    lat.append(ip['lat'])
    lon.append(ip['lon'])
    org.append(ip['org'])

map = folium.Map(location = [10.7905,78.7047],zoom_start = 6,tiles = "Stamen Terrain")
fg = folium.FeatureGroup(name = "Website Map")
for lt,ln,o in zip(lat,lon,org):
    fg.add_child(folium.Marker(location = [lt,ln],popup = o,icon = folium.Icon(color='red')))
map.add_child(fg)
map.save("Website.html")
