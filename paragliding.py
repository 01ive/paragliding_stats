from fastkml import kml
import pygeoif
from geopy.distance import great_circle
import math
import datetime

kml_file = "2023-08-13-XSD-UB2F42-01.kml"

GPS_PERIOD = 1
AVERAGE_NB_SAMPLE = 10

ms_to_kmh = lambda ms : ms*3600/1000
max = lambda a, b : a if a >= b else b
min = lambda a, b : a if a <= b else b


class ParaglidingPoint(pygeoif.geometry.Point):
    def __init__(self, *args):
        super().__init__(*args)
        self.time = 0
        self.distance_2d = 0
        self.distance_3d = 0
        self.elevation = 0
        self.speed_2d = 0
        self.speed_3d = 0
        self.vertical_speed = 0
        self.bearing = 0


class ParaglidingLine(pygeoif.geometry.LineString):
    def __init__(self, coodinates):
        super().__init__(coodinates)
        self.paraliding_geoms = tuple()
        for point in self.geoms:
            self.paraliding_geoms += ParaglidingPoint(point),

    def calculate_distances(self):
        for i in range(len(self.paraliding_geoms)-1):
            point = self.paraliding_geoms[i]
            next_point = self.paraliding_geoms[i+1]
            p1 = (point.x, point.y)
            p2 = (next_point.x, next_point.y)
            next_point.distance_2d = great_circle(p1, p2).m
            next_point.distance_3d = math.sqrt(next_point.distance_2d**2 + (point.z - next_point.z)**2)

    def calculate_elevation(self):
        for i in range(len(self.paraliding_geoms)-1):
            point = self.paraliding_geoms[i]
            next_point = self.paraliding_geoms[i+1]
            next_point.elevation =  next_point.z - point.z
    
    def calculate_speeds(self):
        for i in range(len(self.paraliding_geoms)-1):
            point = self.paraliding_geoms[i]
            next_point = self.paraliding_geoms[i+1]
            next_point.speed_2d = ms_to_kmh(next_point.distance_2d / (next_point.time - point.time).seconds )
            next_point.speed_3d = ms_to_kmh(next_point.distance_3d / (next_point.time - point.time).seconds )
            next_point.vertical_speed = next_point.elevation / (next_point.time - point.time).seconds

    def calculate_time(self, initial_time, delta_samples):
        self.paraliding_geoms[0].time = initial_time
        for i in range(len(self.paraliding_geoms)-1):
            point = self.paraliding_geoms[i]
            next_point = self.paraliding_geoms[i+1]
            next_point.time = point.time + delta_samples

    def calculate_bearing(self):
        for i in range(len(self.paraliding_geoms)-1):
            point = self.paraliding_geoms[i]
            next_point = self.paraliding_geoms[i+1]
            bearing = math.atan2(math.sin(next_point.x - point.x) * math.cos(next_point.y),
                                math.cos(point.y) * math.sin(next_point.y) - 
                                math.sin(point.y) * math.cos(next_point.y) * math.cos(next_point.x - point.x)
                                )
            next_point.bearing = math.degrees(bearing)

    def duration(self):
        first_point = self.paraliding_geoms[0]
        last_point = self.paraliding_geoms[-1]
        return last_point.time - first_point.time
    
    def distance_total_2d(self):
        distance_total = 0
        for point in self.paraliding_geoms:
            distance_total += point.distance_2d
        return distance_total

    def distance_total_3d(self):
        distance_total = 0
        for point in self.paraliding_geoms:
            distance_total += point.distance_3d
        return distance_total

    def high(self):
        first_point = self.paraliding_geoms[0]
        last_point = self.paraliding_geoms[-1]
        return first_point.z - last_point.z
    
    def elevation_total(self):
        elevation_total = 0
        for point in self.paraliding_geoms:
            if point.elevation > 0:
                elevation_total += point.elevation
        return elevation_total

    def max_speed_2d(self):
        max_speed_2d = 0
        for point in self.paraliding_geoms:
            max_speed_2d = max(max_speed_2d, point.speed_2d)
        return max_speed_2d
    
    def max_speed_3d(self):
        max_speed_3d = 0
        for point in self.paraliding_geoms:
            max_speed_3d = max(max_speed_3d, point.speed_3d)
        return max_speed_3d
    
    def max_vertical_speed(self):
        max_vertical_speed = 0
        for point in self.paraliding_geoms:
            max_vertical_speed = max(max_vertical_speed, point.vertical_speed)
        return max_vertical_speed
    
    def min_vertical_speed(self):
        min_vertical_speed = 0
        for point in self.paraliding_geoms:
            min_vertical_speed = min(min_vertical_speed, point.vertical_speed)
        return min_vertical_speed
    
    def average_speed_2d(self):
        average_speed_2d = 0
        for point in self.paraliding_geoms:
            average_speed_2d += point.speed_2d
        average_speed_2d /= len(self.paraliding_geoms)
        return average_speed_2d
    
    def average_speed_3d(self):
        average_speed_3d = 0
        for point in self.paraliding_geoms:
            average_speed_3d += point.speed_3d
        average_speed_3d /= len(self.paraliding_geoms)
        return average_speed_3d


class ParaglidingKML(kml.KML):
    def __init__(self, kml_file):
        super().__init__()
        with open(kml_file, 'rt', encoding="utf-8") as myfile:
            doc = myfile.read()
        self.from_string(doc)
        self._places = list(self.features())
        self._place_id = 0
        self.read_items()
        self.read_trace()

    @property
    def places(self):
        return self._places
    def nb_places(self):
        return len(self._places)
    @property
    def place_id(self):
        return self._place_id
    @place_id.setter
    def place_id(self, id):
        self._places_id = id
    
    @property
    def items(self):
        return self._items
    
    def read_items(self, place_id=None):
        if place_id is not None:
            self._place_id = place_id
        self._items = list(self._places[self._place_id].features())
        print(self._items)

    def read_trace(self):
        for item in self._items:
            if isinstance(item.geometry, pygeoif.geometry.LineString):
                self._current_line = ParaglidingLine(item.geometry.coords)
                break
        print(self._current_line)


if __name__ == "__main__":
    my_kml = ParaglidingKML(kml_file)

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
