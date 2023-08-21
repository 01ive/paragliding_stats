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
    my_kml.track.calculate_distances()
    my_kml.track.calculate_elevation()
    my_kml.track.calculate_speeds()
    my_kml.track.calculate_bearing()
    my_kml.track.calculate_finesse()
    
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

    igc.track.calculate_distances()
    igc.track.calculate_elevation()
    igc.track.calculate_speeds()
    igc.track.calculate_bearing()
    igc.track.calculate_finesse()

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
    



    # import pandas as pd

    # data = list()

    # for point in igc.track.paraliding_geoms:
    #     data.append([point.x, point.y, point.z, point.time, point.speed_2d])


    # columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
    # df = pd.DataFrame(data, columns=columns)

    # import mplleaflet   # (https://github.com/jwass/mplleaflet)
    # import matplotlib.pyplot as plt
    # plt.plot(df['Longitude'], df['Latitude'], color='red', marker='o', markersize=3, linewidth=2, alpha=0.4)
    # #mplleaflet.display(fig=ax.figure)  # shows map inline in Jupyter but takes up full width
    # mplleaflet.show(path='mpl.html')  # saves to html file for display below
    # #mplleaflet.display(fig=fig, tiles='esri_aerial')  # shows aerial/satellite photo
    # # (I don't actually find the aerial view very helpful as it's oblique and obscures what's on the track.)