from django.db import models


class Sentinel5PData(models.Model):
    filename = models.CharField(unique= True, max_length=90)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    min_latitude = models.FloatField(default=float('NaN'))
    min_longitude = models.FloatField(default=float('NaN'))
    max_latitude = models.FloatField(default=float('NaN'))
    max_longitude = models.FloatField(default=float('NaN'))
    fully_imported = models.BooleanField(default=False)


class Scanline(models.Model):
    sentinel_5p_data = models.ForeignKey(Sentinel5PData, on_delete=models.CASCADE)
    time = models.DateTimeField()


class CoData(models.Model):
    scanline = models.ForeignKey(Scanline, on_delete=models.CASCADE)
    latitude = models.FloatField(default=float('NaN'))
    longitude = models.FloatField(default=float('NaN'))
    co_value = models.FloatField(null=True, blank=True)
