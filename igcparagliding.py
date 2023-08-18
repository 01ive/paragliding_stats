from aerofiles.igc import Reader
from opensoar.competition.soaringspot import get_info_from_comment_lines
import datetime

import geoparagliding


class ParaglidingIGC(Reader):
    def __init__(self, igc_file):
        super().__init__()
        with open(igc_file, 'r') as myfile:
            self._doc = self.read(myfile)
    
    def read_items(self, place_id=None):
        if place_id is not None:
            self._place_id = place_id
        self._items = list(self._places[self._place_id].features())
        print(self._items)

    def read_trace(self):
        date = self._doc['header'][1]['utc_date']
        coords = tuple()
        times = tuple()
        for record in self._doc['fix_records'][1]:
            date_time = datetime.datetime.combine(date, record['time'])
            times += date_time,
            coords += tuple((record['lat'], record['lon'], record['gps_alt'])),
        self._current_line = geoparagliding.ParaglidingLine(coords, times)

if __name__ == "__main__":
    igc_file = "2023-08-13-XSD-UB2F42-01.igc"
    igc = ParaglidingIGC(igc_file)
    igc.read_trace()

    igc._current_line.calculate_distances()
    igc._current_line.calculate_elevation()
    igc._current_line.calculate_speeds()
    igc._current_line.calculate_bearing()

    print("My stats 2:")
    print("Distance 2d: " + str(igc._current_line.distance_total_2d()) + " m")
    print("Distance 3d: " + str(igc._current_line.distance_total_3d()) + " m")
    print("Elevation gain: " + str(igc._current_line.elevation_total()) + " m")
    print("Elevation high: " + str(igc._current_line.high()) + " m")
    print("Max speed 2d: " + str(igc._current_line.max_speed_2d()) + " km/h")
    print("Max speed 3d: " + str(igc._current_line.max_speed_3d()) + " km/h")
    print("Average speed 2d: " + str(igc._current_line.average_speed_2d()) + " km/h")
    print("Average speed 3d: " + str(igc._current_line.average_speed_3d()) + " km/h")
    print("Max vertical speed: " + str(igc._current_line.max_vertical_speed()) + " m/s")
    print("Min vertical speed: " + str(igc._current_line.min_vertical_speed()) + " m/s")
