from fastkml import kml
import pygeoif
from geopy.distance import great_circle
import math

kml_file = "2023-08-13-XSD-UB2F42-01.kml"

GPS_PERIOD = 1

def ms_to_kmh(ms):
    return ms*3600/1000

def max(a, b):
    if a >= b:
        return a
    else:
        return b

def min(a, b):
    if a <= b:
        return a
    else:
        return b

if __name__ == "__main__":

    with open(kml_file, 'rt', encoding="utf-8") as myfile:
        doc=myfile.read()

    my_kml = kml.KML()

    my_kml.from_string(doc)

    places = list(my_kml.features())

    for place in places:
        print(place.name)

    items = list(place.features())

    for item in items:
        print(item.name)
        print(item.timeStamp)
        if isinstance(item.geometry, pygeoif.geometry.Point):
            pass
        if isinstance(item.geometry, pygeoif.geometry.LineString):
            full_distance_2d = 0
            full_distance_3d = 0
            elevation_loss = 0
            elevation_gain = 0
            max_speed_2d = 0
            max_speed_3d = 0
            max_vert_speed = 0
            min_vert_speed = 0

            line = item.geometry
            for i, point in enumerate(line.geoms):
                if i == len(line.geoms)-1:
                    break
                # distance
                next_point = line.geoms[i+1]
                p1 = (point.x, point.y)
                p2 = (next_point.x, next_point.y)
                distance_2d = great_circle(p1, p2).m
                full_distance_2d += distance_2d
                distance_3d = math.sqrt(distance_2d**2 + (point.z - next_point.z)**2)
                full_distance_3d += distance_3d
                # elevation
                delta_elevation = point.z - next_point.z
                if delta_elevation < 0:
                    elevation_gain += abs(delta_elevation)
                elif delta_elevation > 0:
                    elevation_loss += delta_elevation
                # speed
                max_speed_2d = max(max_speed_2d, ms_to_kmh(distance_2d / GPS_PERIOD))
                max_speed_3d = max(max_speed_3d, ms_to_kmh(distance_3d / GPS_PERIOD))
                max_vert_speed = max(max_vert_speed, delta_elevation)
                min_vert_speed = min(min_vert_speed, delta_elevation)

    print("My stats:")
    print("Distance 2d: " + str(full_distance_2d) + "m")
    print("Distance 3d: " + str(full_distance_3d) + "m")
    print("Elevation gain: " + str(elevation_gain) + "m")
    print("Elevation loss: " + str(elevation_loss) + "m")
    print("Max speed 2d: " + str(max_speed_2d) + " km/h")
    print("Max speed 3d: " + str(max_speed_3d) + " km/h")
    print("Max vertical speed: " + str(max_vert_speed) + " m/s")
    print("Min vertical speed: " + str(min_vert_speed) + " m/s")
