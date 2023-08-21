import pygeoif
from geopy.distance import great_circle
import math

ms_to_kmh = lambda ms : ms*3600/1000
max = lambda a, b : a if a >= b else b
min = lambda a, b : a if a <= b else b


class ParaglidingPoint(pygeoif.geometry.Point):
    def __init__(self, point, time=0):
        super().__init__(point)
        self.time = time
        self.distance_2d = 0
        self.distance_3d = 0
        self.elevation = 0
        self.speed_2d = 0
        self.speed_3d = 0
        self.vertical_speed = 0
        self.bearing = 0
        self.finesse = 0


class ParaglidingLine(pygeoif.geometry.LineString):
    def __init__(self, coordinates, times=None):
        super().__init__(coordinates)
        self.paraliding_geoms = tuple()
        for i, point in enumerate(self.geoms):
            if times is not None:
                self.paraliding_geoms += ParaglidingPoint(point, times[i]),
            else:
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

    def calculate_finesse(self):
        for i in range(len(self.paraliding_geoms)-1):
            point = self.paraliding_geoms[i]
            next_point = self.paraliding_geoms[i+1]
            if point.z == next_point.z:
                next_point.finesse = 9
            else:
                next_point.finesse = next_point.distance_2d / (point.z - next_point.z)

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
    
    def average_finesse(self):
        average_finesse = 0
        for point in self.paraliding_geoms:
            average_finesse += point.finesse
        average_finesse /= len(self.paraliding_geoms)
        return average_finesse
