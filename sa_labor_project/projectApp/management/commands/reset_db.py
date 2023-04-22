import argparse
import os

from django.core.management import BaseCommand
from sentinelsat import SentinelAPI, geojson_to_wkt, read_geojson

from projectApp.models import Sentinel5PData
from sa_labor_project import settings




class Command(BaseCommand):
    help = 'reset DB'

    def handle(self, *args, **kwargs):
        print('Clearing Database.')
        Sentinel5PData.objects.filter().delete()
        print('Database cleared successfully.')