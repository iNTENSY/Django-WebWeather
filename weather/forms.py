from django import forms

from weather.models import Cities


class FindCityForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'type': 'search',
                'class': 'form-control me-2',
                'placeholder': 'Название города...',
                'aria-label': 'Search',
            }
        )
    )

    class Meta:
        model: Cities = Cities
        fields: tuple[str] = ('name',)