from rest_framework import serializers

from .models import Cities


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model: Cities = Cities
        fields: tuple[str] = ('name', 'total_searches', 'last_search')
