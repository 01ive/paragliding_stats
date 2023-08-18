import datetime

import kmlparagliding

kml_file = "2023-08-13-XSD-UB2F42-01.kml"


if __name__ == "__main__":
    my_kml = kmlparagliding.ParaglidingKML(kml_file)

    date = datetime.date.fromisoformat(my_kml.items[1].name)
    time = datetime.time.fromisoformat(my_kml.items[0].name[-6:-1])
    date_time = datetime.datetime.combine(date, time)
    gps_period = datetime.timedelta(seconds=int(my_kml.items[2].name[-5]))

    my_kml._current_line.calculate_time(date_time, gps_period)
    my_kml._current_line.calculate_distances()
    my_kml._current_line.calculate_elevation()
    my_kml._current_line.calculate_speeds()
    my_kml._current_line.calculate_bearing()
    
    print("My stats 2:")
    print("Distance 2d: " + str(my_kml._current_line.distance_total_2d()) + " m")
    print("Distance 3d: " + str(my_kml._current_line.distance_total_3d()) + " m")
    print("Elevation gain: " + str(my_kml._current_line.elevation_total()) + " m")
    print("Elevation high: " + str(my_kml._current_line.high()) + " m")
    print("Max speed 2d: " + str(my_kml._current_line.max_speed_2d()) + " km/h")
    print("Max speed 3d: " + str(my_kml._current_line.max_speed_3d()) + " km/h")
    print("Average speed 2d: " + str(my_kml._current_line.average_speed_2d()) + " km/h")
    print("Average speed 3d: " + str(my_kml._current_line.average_speed_3d()) + " km/h")
    print("Max vertical speed: " + str(my_kml._current_line.max_vertical_speed()) + " m/s")
    print("Min vertical speed: " + str(my_kml._current_line.min_vertical_speed()) + " m/s")
        
    pass
