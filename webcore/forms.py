from django import forms

class BsCharField(forms.CharField):
    """Bootstrap styled CharField"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs.update({'class': 'form-control'})

class BsEmailField(forms.EmailField):
    """Bootstrap styled EmailField"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs.update({'class': 'form-control'})

class BsPasswordField(forms.CharField):
    """Bootstrap styled PasswordField"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = forms.PasswordInput(attrs={'class': 'form-control'})

class BsChoiceField(forms.ChoiceField):
    """Bootstrap styled ChoiceField"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs.update({'class': 'form-control'})

class BsPhoneNumberField(forms.CharField):
    """Bootstrap styled PhoneNumberField"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs.update({'class': 'form-control', 'type': 'tel'})

class FormLink:
    """Class to link forms together"""
    def __init__(self, form_class, link_field, link_value_field):
        self.form_class = form_class
        self.link_field = link_field
        self.link_value_field = link_value_field

class ExtraFormContext:
    """Class to add extra context to forms"""
    def __init__(self, form_class, extra_context=None):
        self.form_class = form_class
        self.extra_context = extra_context or {}
