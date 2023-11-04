class Infobox(dict):
    def __init__(self):
        # Sets style information
        super().__init__()
        self['style'] = {}
        self['style']['border'] = {}
        self['style']['border']['stroke-width'] = 3
        self['style']['border']['color'] = {}
        self['style']['border']['color']['r'] = 0
        self['style']['border']['color']['g'] = 0
        self['style']['border']['color']['b'] = 0
        self['style']['color'] = {}
        self['style']['color']['r'] = 255
        self['style']['color']['g'] = 255
        self['style']['color']['b'] = 255
        self['style']['text'] = []
        self['text'] = []

    # IMPORTANT: Text is based off of text containers that contain some text all formatted the same way.
    # There can be multiple text containers in a line. The text containers can contain text or data.
    def add_text(self, text: str, text_type='text', line=None, text_id=None,
                 font='Calibri', size=15, r=0, g=0, b=0) -> None:

        # Create text
        text_dict = {'type': text_type}
        # Assign unique ID
        if text_id is None:
            # Default ID is just a number, but a string
            text_dict['id'] = str(len(self['text']))
        else:
            # Custom ID
            text_dict['id'] = text_id

        # Decide which line text belongs on
        if line is None:
            if len(self['text']) == 0:
                # Text starts on first line
                text_dict['line'] = 0
            else:
                # Text continues on same line as before
                text_dict['line'] = self['text'][-1]['line']
        else:
            # Decide line manually
            text_dict['line'] = line

        text_dict['text'] = text

        # Create styles
        style_dict = {'font': font, 'size': size, 'r': r, 'g': g, 'b': b}

        # Add to object
        self['style']['text'].append(style_dict)
        self['text'].append(text_dict)

    def remove_text(self, text_id: int | str) -> None:
        if type(text_id) is int:
            del self['style']['text'][text_id]
            del self['text'][text_id]
        else:
            for text in self['text']:
                if text['id'] == text_id:
                    del self['style']['text'][self['text'].index(text)]
                    del self['text'][self['text'].index(text)]
