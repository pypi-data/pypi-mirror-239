from mapdata import MapData
import csv


def from_csv(location: str, territory_list: int = 0, delimiter=',') -> MapData:
    columns = []
    with open(location) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for line in reader:
            for i in range(0, len(line)):
                try:
                    line[i] = int(line[i])
                except ValueError:
                    pass
                try:
                    columns[i].append(line[i])
                except IndexError:
                    columns.append([])
                    columns[i].append(line[i])
        data = {}
        for column in columns:
            data[column[0]] = column[1:]
        return MapData(data, columns[territory_list][0])
