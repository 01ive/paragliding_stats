from fastkml import kml
import pygeoif
from geopy.distance import great_circle
import math

kml_file = "2023-08-13-XSD-UB2F42-01.kml"

GPS_PERIOD = 1
AVERAGE_NB_SAMPLE = 10

ms_to_kmh = lambda ms : ms*3600/1000
max = lambda a, b : a if a >= b else b
min = lambda a, b : a if a <= b else b


class ParaglidingStats:
    def __init__(self):
        self._full_distance_2d = 0
        self._full_distance_3d = 0
        self._elevation_loss = 0
        self._elevation_gain = 0
        self._max_speed_2d = 0
        self._max_speed_3d = 0
        self._max_vert_speed = 0
        self._min_vert_speed = 0
        self._speed_2d = list()
        self._max_average_speed_2d = 0
        self._bearing = 0

    @property
    def full_distance_2d(self):
        return self._full_distance_2d
    @property
    def full_distance_3d(self):
        return self._full_distance_3d
    @property
    def elevation_loss(self):
        return self._elevation_loss
    @property
    def elevation_gain(self):
        return self._elevation_gain
    @property
    def max_speed_2d(self):
        return self._max_speed_2d
    @property
    def max_speed_3d(self):
        return self._max_speed_3d
    @property
    def max_vert_speed(self):
        return self._max_vert_speed
    @property
    def min_vert_speed(self):
        return self._min_vert_speed
    @property
    def max_average_speed_2d(self):
        return self._max_average_speed_2d
    @property
    def bearing(self):
        return self._bearing

    def calculate_distances(self, point_1, point_2):
        p1 = (point_1.x, point_1.y)
        p2 = (point_2.x, point_2.y)
        distance_2d = great_circle(p1, p2).m
        self._full_distance_2d += distance_2d
        distance_3d = math.sqrt(distance_2d**2 + (point_1.z - point_2.z)**2)
        self._full_distance_3d += distance_3d

    def calculate_elevation(self, point_1, point_2):
        delta_elevation = point_1.z - point_2.z
        if delta_elevation < 0:
            self._elevation_gain += abs(delta_elevation)
        elif delta_elevation > 0:
            self._elevation_loss += delta_elevation

    def calculate_speed(self, point_1, point_2):
        p1 = (point_1.x, point_1.y)
        p2 = (point_2.x, point_2.y)
        distance_2d = great_circle(p1, p2).m
        distance_3d = math.sqrt(distance_2d**2 + (point_1.z - point_2.z)**2)
        delta_elevation = point_1.z - point_2.z
        self._speed_2d.append(ms_to_kmh(distance_2d / GPS_PERIOD))
        if len(self._speed_2d) >= AVERAGE_NB_SAMPLE:
            self._speed_2d.pop(0)
        average_speed_2d = 0
        for k in self._speed_2d:
            average_speed_2d += k
        average_speed_2d /= len(self._speed_2d)
        self._max_average_speed_2d = max(self._max_average_speed_2d, average_speed_2d)
        self._max_speed_2d = max(self._max_speed_2d, ms_to_kmh(distance_2d / GPS_PERIOD))
        self._max_speed_3d = max(self._max_speed_3d, ms_to_kmh(distance_3d / GPS_PERIOD))
        self._max_vert_speed = max(self._max_vert_speed, delta_elevation)
        self._min_vert_speed = min(self._min_vert_speed, delta_elevation)

    def calculate_bearing(self, point_1, point_2):
        bearing = math.atan2(math.sin(point_2.x - point_1.x) * math.cos(point_2.y),
                                math.cos(point_1.y) * math.sin(point_2.y) - 
                                math.sin(point_1.y) * math.cos(point_2.y) * math.cos(point_2.x - point_1.x)
                                )
        self._bearing = math.degrees(bearing)


class ParaglidingLine(pygeoif.geometry.LineString):
    def __init__(self, coodinates):
        super().__init__(coodinates)
        self._distance = 0
        self._elevation = 0
        self._speed_2d = 0
        self._speed_3d = 0
        self._vertical_speed = 0
        self._bearing = 0


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
                # self._current_line = item.geometry
                self._current_line = ParaglidingLine(item.geometry.coords)
                break
        print(self._current_line)

    def process_stats(self):
        stats = ParaglidingStats()
        for i, point in enumerate(self._current_line.geoms):
            if i == len(self._current_line.geoms)-1:
                break
            next_point = self._current_line.geoms[i+1]
            # distances
            stats.calculate_distances(point, next_point)
            # elevation
            stats.calculate_elevation(point, next_point)
            # speed
            stats.calculate_speed(point, next_point)
            # bearing
            stats.calculate_bearing(point, next_point)
            
        return stats


if __name__ == "__main__":
    my_kml = ParaglidingKML(kml_file)

    stats = my_kml.process_stats()
    
    print("My stats:")
    print("Distance 2d: " + str(stats.full_distance_2d) + " m")
    print("Distance 3d: " + str(stats.full_distance_3d) + " m")
    print("Elevation gain: " + str(stats.elevation_gain) + " m")
    print("Elevation loss: " + str(stats.elevation_loss) + " m")
    print("Max speed 2d: " + str(stats.max_speed_2d) + " km/h")
    print("Max speed 3d: " + str(stats.max_speed_3d) + " km/h")
    print("Max vertical speed: " + str(stats.max_vert_speed) + " m/s")
    print("Min vertical speed: " + str(stats.min_vert_speed) + " m/s")

    