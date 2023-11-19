# need to run pip install folium to run 
import folium
import json

def render_subway_map(geojson_file):
    #  makes a base map for nyc
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

    # loading subway line data from file
    with open(geojson_file, 'r') as file:
        subway_data = json.load(file)

    # adding subway lines to the map
    for feature in subway_data['features']:
        line_color = 'purple'  
        folium.GeoJson(feature, name=feature['properties']['line'], style_function=lambda x: {'color': line_color}).add_to(m)

    # saves the map to an HTML file
    m.save('subway_map.html')

if __name__ == "__main__":
    geojson_file = 'Design/Functions/Subway Lines.geojson'
    render_subway_map(geojson_file)