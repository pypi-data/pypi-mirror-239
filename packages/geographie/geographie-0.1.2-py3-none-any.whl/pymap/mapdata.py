class MapData(dict):
    def __init__(self, data: dict[str, list[str | int | float]], tlist='territory_list'):
        super().__init__()
        if type(data) is dict:
            self['data'] = data
            try:
                # Finds which list is the territory list and marks it
                self['territory_list'] = self['data'][tlist]
            except IndexError:
                raise IndexError('Territory list not found in data.')
        else:
            raise TypeError('Data must be a dictionary.')
