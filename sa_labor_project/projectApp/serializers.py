from rest_framework import serializers
from .models import Scanline, CoValue, Sentinel5PData


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
        fields = ["filename", "start_time", "end_time", "min_latitude", "max_latitude", "min_longitude", "max_longitude", "fully_imported"]



