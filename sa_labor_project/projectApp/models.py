from django.db import models


class Sentinel5PData(models.Model):
    uuid = models.CharField(max_length=40)
    filename = models.CharField(max_length=90)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    min_latitude = models.FloatField
    min_longitude = models.FloatField
    max_latitude = models.FloatField
    max_longitude = models.FloatField


class Scanline(models.Model):
    sentinel_5p_data = models.ForeignKey(Sentinel5PData, on_delete=models.CASCADE)
    time = models.DateTimeField()


class CoData(models.Model):
    scanline = models.ForeignKey(Scanline, on_delete=models.CASCADE)
    latitude = models.FloatField
    longitude = models.FloatField
    co_value = models.FloatField
