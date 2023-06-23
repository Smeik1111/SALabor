from rest_framework import serializers
from .models import Scanline, CoValue, Sentinel5PData, GeoJSONFile, Country


class CoValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoValue
        fields = ["latitude", "longitude", "co_value"]


class ScanlineSerializer(serializers.ModelSerializer):
    co_values = CoValueSerializer(many=True, read_only=True)

    class Meta:
        model = Scanline
        fields = ["sentinel_5p_data", "time", 'co_values']


class Sentinel5PDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentinel5PData
        fields = ["filename", "start_time", "end_time", "min_latitude", "max_latitude", "min_longitude",
                  "max_longitude", "fully_imported"]


class GeoJSONFileSerializer(serializers.ModelSerializer):
    geojson_content = serializers.SerializerMethodField()

    def get_geojson_content(self, instance):
        if instance.file:
            file_path = instance.file.path
            with open(file_path, 'r') as file:
                geojson_string = file.read()
            return geojson_string
        return None

    class Meta:
        model = GeoJSONFile
        fields = ('date', 'geojson_content')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'oldest_data', 'newest_data')
