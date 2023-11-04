from coordinates import Coordinates
import json


def _get_geojson_feature_list(geojson: dict, res: int, isl: int) -> list:
    if geojson['type'] == 'FeatureCollection':
        poly_list = []
        for poly in geojson['features']:
            poly_list += _get_geojson_feature_list(poly, res, isl)
        return poly_list

    elif geojson['type'] == 'Feature':

        if geojson['geometry']['type'] == 'Polygon':
            geojson['geometry']['coordinates'] = [geojson['geometry']['coordinates']]
            geojson['geometry']['type'] = 'MultiPolygon'

        if geojson['geometry']['type'] == 'MultiPolygon':
            new_poly_list = []
            for polygon in geojson['geometry']['coordinates']:
                actual_polygon = polygon[0]
                polygon_fixed = []
                polygon_str = []
                for_deletion = []
                for i in range(0, len(actual_polygon)):
                    coord = actual_polygon[i]
                    coord[0] += 180
                    coord[1] += 90
                    coord[0] = round(coord[0] * res) / res
                    coord[1] = round(coord[1] * res) / res
                    coord[0] = str(coord[0])
                    coord[1] = str(coord[1])
                    str_coord = coord[0] + ',' + coord[1]
                    if str_coord in polygon_str:
                        for_deletion.insert(0, i)
                    else:
                        polygon_str.append(str_coord)
                        polygon_fixed.append(coord)
                for i in for_deletion:
                    del actual_polygon[i]
                new_poly = {'type': 'MultiPolygon', 'coordinates': polygon_fixed, 'properties': geojson['properties']}
                if len(new_poly['coordinates']) > isl:
                    new_poly_list.append(new_poly)
            return new_poly_list

        else:
            return []

    else:
        raise TypeError('Not a valid geojson file')


def from_geojson(file: str, record_id: str, res=5, isl=1, poly_keep=None, zoom=None, translate=None,
                 height=180, width=360, relative_zoom=1.1) -> Coordinates:
    if poly_keep is None:
        poly_keep = []
    with open(file) as geojson_txt:
        geojson = json.load(geojson_txt)
    feature_list = _get_geojson_feature_list(geojson, res, isl)
    coordinates_list = []
    record_list = []
    for poly in feature_list:
        record = poly['properties'][record_id]
        if record in poly_keep or poly_keep == []:
            coordinates_list.append(poly['coordinates'])
            record_list.append(record.replace(' ', ''))
    for i in range(0, len(coordinates_list)):
        coordinates_list[i] = {'Points': coordinates_list[i],
                               'Country': record_list[i]}

    return Coordinates(coordinates_list, record_list, zoom, translate, height, width, relative_zoom)
