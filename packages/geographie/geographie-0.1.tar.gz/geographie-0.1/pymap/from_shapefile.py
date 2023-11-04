from coordinates import Coordinates
import shapefile


def from_shapefile(file: str, record_id: int, res: int = 5, isl: int = 1, poly_keep=None, zoom=None, translate=None,
                   height: int = 180, width: int = 360, relative_zoom: int = 1.1,
                   extra_smooth: bool = False) -> Coordinates:
    """
    Returns a Coordinates object from a shapefile and metadata.

    file: Name or url of the shapefile
    record_id: Column of the shape record with the names of the shapes
    res: The resolution of the data
    isl: Minimum number of coordinates per shape
    poly_keep: List of shapes that should be stored in the Coordinates object
    zoom: Metadata, how zoomed in the resulting map should be. If None, zooms to fit the screen
    translate: Metadata, the longitude and latitude of the bottom left corner of the map
    height: Metadata, the height of the map
    width: Metadata, the width of the map
    relative_zoom: Metadata, zoom relative to the zoom to fit screen.
    extra_smooth: Whether the Coordinates object should be made extra smooth.
    """

    shp = shapefile.Reader(file)
    shapes = shp.shapes()

    svg = []
    record_list = []

    i = 0

    for shape in shapes:
        i += 1

        if poly_keep is None or (shp.shapeRecord(i - 1).record[record_id] in poly_keep):

            main = []
            rounded = []

            for point in shape.points:

                data = ','.join(str(x) for x in point)
                long = float(data.split(',')[0])
                lat = float(data.split(',')[1])

                long = long + 180
                lat = lat + 90

                data = str(long) + ',' + str(lat)
                data = data + ' '

                if data in main:
                    main.append(data)
                    point_rounded = [str(round(long * res) / res), str(round(lat * res) / res)]
                    rounded.append(point_rounded)

                    if len(rounded) > isl:
                        svg.append({'Points': rounded,
                                    'Country': shp.shapeRecord(i - 1).
                                   record[record_id].replace(' ', '')})

                    main = []
                    rounded = []
                else:
                    # Round data as before and save the point
                    main.append(data)
                    rounded_data = [str(round(long * res) / res), str(round(lat * res) / res)]
                    if rounded_data not in rounded:
                        if (not extra_smooth) or len(rounded) == 0 or (
                                not rounded[-1][0] == rounded_data[0] and not rounded[-1][1] == rounded_data[1]):
                            rounded.append(rounded_data)
        record_list.append(shp.shapeRecord(i - 1).record[record_id].replace(' ', ''))
    # Create object from the points
    return Coordinates(svg, record_list, zoom, translate, height, width, relative_zoom)
