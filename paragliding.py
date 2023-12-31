import datetime

import kmlparagliding
import igcparagliding
import plot

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
    
    plot.plot_track(igc.track.paraliding_geoms)

