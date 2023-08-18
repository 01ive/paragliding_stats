from fastkml import kml
import geoparagliding
import pygeoif

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
                self._current_line = geoparagliding.ParaglidingLine(item.geometry.coords)
                break
        print(self._current_line)
