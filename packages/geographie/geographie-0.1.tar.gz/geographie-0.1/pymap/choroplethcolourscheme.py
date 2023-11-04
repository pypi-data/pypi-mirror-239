from colour import Color
from choroplethcolourrange import ChoroplethColourRange


class ChoroplethColourScheme(dict):
    """
    Stores information related to the colour scheme.
    """

    def __init__(self):
        super().__init__()
        self['source'] = 'data'
        self['colours'] = []

    def add_colour(self, colour: Color | ChoroplethColourRange, values: any,
                   values_type: str = 'list', color_id: str = None) -> None:
        """
        Adds a colour and associated values to the colour scheme of the map

        colour: The colour or ange of colours that will be added to the map
        values: List or range of values that would result in said colour(s)
        values_type: Whether a list or range of values was provided
        color_id: A unique identifier for a colour

        Preconditions:

        - not color_id.isdigit()
        - values_type == 'list' or values_type == 'range'
        - values_type == 'list' or (type(values) == list and len(values) == 2)

        >>> my_colour = Color(hex_l='#316293')
        >>> values_list = [31, 62, 93]
        >>> colour_scheme = ChoroplethColourScheme()
        >>> colour_scheme.add_colour(my_colour, values_list, 'list')
        >>> final_colour = colour_scheme['colours'][0]
        >>> final_colour['colour_type']
        'single'
        >>> final_colour['colour']
        '#316293'
        >>> final_colour['values'][1]
        62
        >>> final_colour['id']
        '0'
        """

        colour_dict = {'values_type': values_type}

        if type(colour) == Color:
            colour_dict['colour_type'] = 'single'
            colour_dict['colour'] = colour.get_hex_l()
        elif type(colour) == ChoroplethColourRange:
            colour_dict['colour_type'] = 'range'
            colour_dict['colour'] = colour
        else:
            raise TypeError('Invalid color')

        if type(values) == list:
            colour_dict['values'] = values
        else:
            colour_dict['values'] = [values]

        if color_id is None:
            colour_dict['id'] = str(len(self['colours']))
        else:
            colour_dict['id'] = color_id

        self['colours'].append(colour_dict)

    def remove_colour(self, colour: Color) -> None:
        """
        Removes all instances of a colour on the map based on the colour.
        If no such instances exist, does nothing.

        colour: The colour to remove

        Preconditions:

        >>> my_colour = Color(hex_l='#316293')
        >>> values_list = [31, 62, 93]
        >>> colour_scheme = ChoroplethColourScheme()
        >>> colour_scheme.add_colour(my_colour, values_list, 'list')
        >>> colour_scheme.add_colour(my_colour, values_list, 'list')
        >>> len(colour_scheme['colours'])
        2
        >>> colour_scheme.remove_colour(my_colour)
        >>> len(colour_scheme['colours'])
        0

        """
        i = 0
        for_deletion = []
        for c in self['colours']:
            if c['colour'] == colour.get_hex_l():
                for_deletion.insert(0, i)
            i += 1
        for i in for_deletion:
            del self['colours'][i]

    def remove_colour_by_id(self, colour_id: str) -> None:
        """
        Removes a colour on the map based on the id of the colour.
        If no such id exist, does nothing.

        colour_id: id of the colour to be removed.

        >>> my_colour = Color(hex_l='#316293')
        >>> values_list = [31, 62, 93]
        >>> colour_scheme = ChoroplethColourScheme()
        >>> colour_scheme.add_colour(my_colour, values_list, 'list')
        >>> colour_scheme.add_colour(my_colour, values_list, 'list')
        >>> len(colour_scheme['colours'])
        2
        >>> colour_scheme.remove_colour_by_id("0")
        >>> len(colour_scheme['colours'])
        1
        """
        i = 0
        for_deletion = []
        for c in self['colours']:
            if c['id'] == colour_id:
                for_deletion.insert(0, i)
            i += 1
        for i in for_deletion:
            del self['colours'][i]

    def remove_value(self, value, colour=None, colour_id=None):
        for c in self['colours']:
            if c['values_type'] == 'list':
                if (colour is None and colour_id is None) or c['colour'] == colour.get_hex_l() or c['id'] == colour_id:
                    if value in c['values']:
                        value_index = c['values'].index(value)
                        del c[value_index]
                        break

    def add_values_from_color(self, values, colour):
        for c in self['colours']:
            if c['values_type'] == 'list' and c['colour'] == colour.get_hex_l():
                if type(values) == str:
                    c['values'].append(values)
                else:
                    c['values'] = c['values'] + values
                break
