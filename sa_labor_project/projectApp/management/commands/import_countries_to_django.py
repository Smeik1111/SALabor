import argparse
import os
from datetime import datetime

import pandas
import xarray as xarray
from django.core.management import BaseCommand
from projectApp.models import *

from sa_labor_project import settings
from projectApp.models import Country, GeoJSONFile


class Command(BaseCommand):
    help = 'Imports all refs to countrie files to db'

    def handle(self, *args, **kwargs):
        path = settings.COUNTRIES_PATH
        for dir in os.listdir(path):
            country, _ = Country.objects.get_or_create(name=dir)
            dir_path = os.path.join(path, dir)
            if not os.path.isdir(dir_path):
                continue
            for file in os.listdir(dir_path):
                if not file.endswith(".geo.json"):
                    continue
                file_path = os.path.join(dir_path, file)
                date_str = file.removesuffix(".geo.json")
                date = datetime.strptime(date_str, '%Y%m%d').date()
                if country.oldest_data > date:
                    country.oldest_data = date
                    country.save()
                if country.newest_data < date:
                    country.newest_data = date
                    country.save()
                GeoJSONFile.objects.update_or_create(country=country, name=file, date=date, file=file_path)
