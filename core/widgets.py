from django.forms import Textarea


class EditorTextArea(Textarea):
    def __init__(self, attrs=None):
        # Use slightly better defaults than HTML's 20x2 box
        default_attrs = {'cols': '20', 'class': 'editor'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
