from datetime import datetime

from django.db import models


class Sentinel5PData(models.Model):
    filename = models.CharField(unique= True, max_length=90)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    min_latitude = models.FloatField(default=float('NaN'))
    max_latitude = models.FloatField(default=float('NaN'))
    min_longitude = models.FloatField(default=float('NaN'))
    max_longitude = models.FloatField(default=float('NaN'))
    fully_imported = models.BooleanField(default=False)


class Scanline(models.Model):
    sentinel_5p_data = models.ForeignKey(Sentinel5PData,related_name='scanlines', on_delete=models.CASCADE)
    time = models.DateTimeField()


class CoValue(models.Model):
    scanline = models.ForeignKey(Scanline,related_name='co_values', on_delete=models.CASCADE)
    latitude = models.FloatField(default=float('NaN'))
    longitude = models.FloatField(default=float('NaN'))
    co_value = models.FloatField(null=True, blank=True)

class Country(models.Model):
    name = models.CharField(max_length=20)
    oldest_data = models.DateField(default=datetime.max.date())
    newest_data = models.DateField(default=datetime.min.date())

class GeoJSONFile(models.Model):
    country = models.ForeignKey(Country, related_name='country', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    date = models.DateField(default=datetime.max.date())
    file = models.FileField()



