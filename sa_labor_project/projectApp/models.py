from datetime import datetime

from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=20)
    oldest_data = models.DateField(default=datetime.max.date())
    newest_data = models.DateField(default=datetime.min.date())
    lat_min = models.FloatField(null=True)
    lat_max = models.FloatField(null=True)
    lat_count = models.IntegerField(default=0)
    lon_min = models.FloatField(null=True)
    lon_max = models.FloatField(null=True)
    lon_count = models.IntegerField(null=True)


class GeoJSONFile(models.Model):
    country = models.ForeignKey(Country, related_name='country', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    date = models.DateField(default=datetime.max.date())
    file = models.FileField()
    data = models.TextField()
