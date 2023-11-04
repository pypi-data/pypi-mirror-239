from colour import Color


class ChoroplethColourRange(dict):
    """
    Stores two colours.

    Representation invariants:
    - type(self['start']) == Color
    - type(self['end']) == Color
    """

    def __init__(self, c1: Color, c2: Color):
        super().__init__()
        self['start'] = c1.get_hex_l()
        self['end'] = c2.get_hex_l()
