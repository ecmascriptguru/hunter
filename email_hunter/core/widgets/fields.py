from crispy_forms.layout import Field


class BasicBootstrapFormField(Field):
    css_class='input form-control'

    def __init__(self, *args, **kwargs):
        css = kwargs.pop('css_class', '')
        self.css_class += css
        super(BasicBootstrapFormField, self).__init__(css_class=self.css_class,
            *args, **kwargs, )