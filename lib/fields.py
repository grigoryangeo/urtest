# File encoding: utf-8

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import CheckboxSelectMultiple

class UrtestPasswordField(forms.CharField):
    """
    Локальное поле для ввода пароля

    Ограничивает min/max_length и виджет
    """
    def __init__(self, *args, **kwargs):
        forms.CharField.__init__(self,
                                 min_length=5,
                                 max_length=30,
                                 widget=forms.PasswordInput(render_value=False),
                                 *args, **kwargs)


class UrtestFIOField(forms.RegexField):
    """
    Локальное поле для ФИО

    Ограничивает валидацию и сообщения
    """
    fio_regexp = r'(?u)\w+(-\w+)?'
    generic_error = {"invalid": "Неправильно введены данные"}

    def __init__(self, *args, **kwargs):
        forms.RegexField.__init__(self,
                                  regex=self.fio_regexp,
                                  error_messages=self.generic_error,
                                  *args, **kwargs)


class UrtestTextAreaField(forms.CharField):
    """
    Локальное поле для больших текстов

    Ограничивает max_length и виджет
    """
    def __init__(self, *args, **kwargs):
        forms.CharField.__init__(self,
                                 max_length=300,
                                 widget=forms.Textarea,
                                 *args, **kwargs)
