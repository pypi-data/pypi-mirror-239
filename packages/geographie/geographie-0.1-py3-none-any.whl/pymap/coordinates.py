from __future__ import annotations


class Coordinates(dict):

    def __init__(self, coords, records, zoom=None, translate=None, height: int = 180,
                 width: int = 360, relative_zoom: float = 1.1):
        super().__init__()

        if translate is None:
            translate = [0, 0]

        self['data'] = coords
        self['metadata'] = {'scale': zoom, 'translate': translate, 'height': height, 'width': width}
        if zoom is None:
            self.automatic_zoom_and_translate(relative_zoom)
        self['recordList'] = records

    def record_list_to_csv(self, location='MapData.csv'):
        with open(location, 'w') as file:
            file.write('territory_list\n' + '\n'.join(self['recordList']))

    def merge(self, coords: Coordinates, adjust_zoom=True, relative_zoom=1.1) -> None:
        self['recordList'] = self['recordList'] + coords['recordList']
        self['data'] = self['data'] + coords['data']

        if adjust_zoom:
            self.automatic_zoom_and_translate(relative_zoom)

    def modify_record(self, record: str | int, new: str) -> None:
        if type(record) == str:
            curr = None
            i = 0
            while not curr == record:
                curr = self['recordList'][i]
                i += 1
            self['recordList'][i] = new
            self['data'][i]['Country'] = new

        else:
            self['recordList'][record] = new
            self['data'][record]['Country'] = new

    def automatic_zoom_and_translate(self, relative_zoom=1.1) -> None:
        max_long = float(self['data'][0]['Points'][0][0])
        min_long = max_long
        max_lat = float(self['data'][0]['Points'][0][1])
        min_lat = max_lat
        for shape in self['data']:
            for point in shape['Points']:
                float_long = float(point[0])
                float_lat = float(point[1])
                if float_long > max_long:
                    max_long = float_long
                if float_long < min_long:
                    min_long = float_long
                if float_lat > max_lat:
                    max_lat = float_lat
                if float_lat < min_lat:
                    min_lat = float_lat

        self['metadata']['translate'] = [min_long, min_lat]
        diff_long = max_long - min_long
        diff_lat = max_lat - min_lat
        zoom_long = int(360 / diff_long)
        zoom_lat = int(180 / diff_lat)
        if zoom_long < zoom_lat:
            self['metadata']['scale'] = zoom_long
        else:
            self['metadata']['scale'] = zoom_lat
        self['metadata']['scale'] = int(self['metadata']['scale'] / relative_zoom)
        self['metadata']['translate'][0] -= diff_long * (relative_zoom - 1) / 2
        self['metadata']['translate'][1] -= diff_lat * (relative_zoom - 1) / 2
