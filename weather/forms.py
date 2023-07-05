from django.forms import ModelForm

from weather.models import Cities


class FindCityForm(ModelForm):
    class Meta:
        model: Cities = Cities
        fields: tuple[str] = ('name',)