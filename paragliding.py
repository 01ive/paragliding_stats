import datetime

import kmlparagliding
import igcparagliding


kml_file = "2023-08-13-XSD-UB2F42-01.kml"
igc_file = "2023-08-13-XSD-UB2F42-01.igc"


if __name__ == "__main__":
    my_kml = kmlparagliding.ParaglidingKML(kml_file)

    date = datetime.date.fromisoformat(my_kml.items[1].name)
    time = datetime.time.fromisoformat(my_kml.items[0].name[-6:-1])
    date_time = datetime.datetime.combine(date, time)
    gps_period = datetime.timedelta(seconds=int(my_kml.items[2].name[-5]))

    my_kml.track.calculate_time(date_time, gps_period)    
    my_kml.track.calculate_points_parameters()  

    print("KML stats:")
    print("Distance 2d: " + str(my_kml.track.distance_total_2d()) + " m")
    print("Distance 3d: " + str(my_kml.track.distance_total_3d()) + " m")
    print("Elevation gain: " + str(my_kml.track.elevation_total()) + " m")
    print("Elevation high: " + str(my_kml.track.high()) + " m")
    print("Max speed 2d: " + str(my_kml.track.max_speed_2d()) + " km/h")
    print("Max speed 3d: " + str(my_kml.track.max_speed_3d()) + " km/h")
    print("Average speed 2d: " + str(my_kml.track.average_speed_2d()) + " km/h")
    print("Average speed 3d: " + str(my_kml.track.average_speed_3d()) + " km/h")
    print("Max vertical speed: " + str(my_kml.track.max_vertical_speed()) + " m/s")
    print("Min vertical speed: " + str(my_kml.track.min_vertical_speed()) + " m/s")
    print("Average finesse: " + str(my_kml.track.average_finesse()))
        
    igc = igcparagliding.ParaglidingIGC(igc_file)
    igc.read_trace()

    igc.track.calculate_points_parameters()

    print("IGC stats:")
    print("Distance 2d: " + str(igc.track.distance_total_2d()) + " m")
    print("Distance 3d: " + str(igc.track.distance_total_3d()) + " m")
    print("Elevation gain: " + str(igc.track.elevation_total()) + " m")
    print("Elevation high: " + str(igc.track.high()) + " m")
    print("Max speed 2d: " + str(igc.track.max_speed_2d()) + " km/h")
    print("Max speed 3d: " + str(igc.track.max_speed_3d()) + " km/h")
    print("Average speed 2d: " + str(igc.track.average_speed_2d()) + " km/h")
    print("Average speed 3d: " + str(igc.track.average_speed_3d()) + " km/h")
    print("Max vertical speed: " + str(igc.track.max_vertical_speed()) + " m/s")
    print("Min vertical speed: " + str(igc.track.min_vertical_speed()) + " m/s")
    print("Average finesse: " + str(igc.track.average_finesse()))
    



    import pandas as pd

    data = list()

    for point in igc.track.paraliding_geoms:
        data.append([point.x, point.y, point.z, point.time, point.speed_2d])


    columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
    df = pd.DataFrame(data, columns=columns)

    import folium
    from folium.plugins import MarkerCluster
    import pandas as pd

    #Define coordinates of where we want to center our map
    boulder_coords = list(df.iloc[0][0:2])

    #Create the map
    my_map = folium.Map(location = boulder_coords, zoom_start = 13)

    folium.PolyLine(tuple(df[['Longitude', 'Latitude']].itertuples(index=False, name=None))).add_to(my_map)

    # for point in igc.track.paraliding_geoms:
    #     folium.Marker([point.x, point.y], icon=folium.Icon(icon="bus-simple", icon_color="white", prefix='fa'), tooltip=str(point.z)).add_to(my_map)

    igc.track.paraliding_geoms[0].x
    folium.Marker([igc.track.paraliding_geoms[0].x, igc.track.paraliding_geoms[0].y], 
                  popup="start", 
                  tooltip=str(igc.track.paraliding_geoms[0].z),
                  icon=folium.Icon(color="green") ).add_to(my_map)
    folium.Marker([igc.track.paraliding_geoms[-1].x, igc.track.paraliding_geoms[-1].y], 
                  popup="start", 
                  tooltip=str(igc.track.paraliding_geoms[-1].z), 
                  icon=folium.Icon(color="red") ).add_to(my_map)

    #Display the map
    my_map.show_in_browser()
