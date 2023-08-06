from django import forms
from .data import UN_RECOGNIZED_COUNTRIES, get_countries_sorted_lazy, get_countries_sorted


class CountryFormField(forms.TypedChoiceField):
    """A form field that allows users to choose their country. By default, it lists all countries recognized by the UN,
    but using the ``countries`` attribute you can specify your own set of allowed countries. Use ``exclude`` to exclude
    specific countries.
    """

    def __init__(self, countries=UN_RECOGNIZED_COUNTRIES, exclude=(), *args, **kwargs):
        # Maintain the empty choice if available
        if kwargs['choices'] and kwargs['choices'][0][0] == '':
            kwargs['choices'] = [kwargs['choices'][0]] + get_countries_sorted(countries, exclude)
        else:
            kwargs['choices'] = get_countries_sorted_lazy(countries, exclude)

        super(CountryFormField, self).__init__(*args, **kwargs)
