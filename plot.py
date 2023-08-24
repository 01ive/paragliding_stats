import folium

def plot_track(paraliding_geoms):
    coords = tuple()
    for point in paraliding_geoms:
        coords += (point.x, point.y),

    #Define coordinates of where we want to center our map
    boulder_coords = list(coords[int(len(coords)/2)])

    #Create the map
    my_map = folium.Map(location = boulder_coords, zoom_start = 13)

    folium.PolyLine(coords).add_to(my_map)

    # Start point
    folium.Marker([paraliding_geoms[0].x, paraliding_geoms[0].y], 
                    popup="start", 
                    tooltip=str(paraliding_geoms[0].z),
                    icon=folium.Icon(color="green") ).add_to(my_map)
    # Stop point
    folium.Marker([paraliding_geoms[-1].x, paraliding_geoms[-1].y], 
                    popup="start", 
                    tooltip=str(paraliding_geoms[-1].z), 
                    icon=folium.Icon(color="red") ).add_to(my_map)

    #Display the map
    my_map.show_in_browser()
