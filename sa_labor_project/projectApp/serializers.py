from rest_framework import serializers
from .models import GeoJSONFile, Country


class GeoJSONFileSerializer(serializers.ModelSerializer):
    # geojson_content = serializers.SerializerMethodField()

    def get_geojson_content(self, instance):
        if instance.file:
            file_path = instance.file.path
            with open(file_path, 'r') as file:
                geojson_string = file.read()
            return geojson_string
        return None

    class Meta:
        model = GeoJSONFile
        # fields = ('date', 'geojson_content')
        fields = ('date', 'data')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name',
                  'oldest_data',
                  'newest_data'
                  )


class CountryBorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('lat_min',
                  'lat_max',
                  'lat_count',
                  'lon_min',
                  'lon_max',
                  'lon_count',
                  )


class AnswerSerializer(serializers.Serializer):
    config = CountryBorderSerializer()
    values = GeoJSONFileSerializer(many=True)
