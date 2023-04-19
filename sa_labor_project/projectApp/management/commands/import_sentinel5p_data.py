import argparse
import os

import pandas
import xarray as xarray
from django.core.management import BaseCommand
from projectApp.models import *

from sa_labor_project import settings


class Command(BaseCommand):
    help = 'Imports all .nc files to db'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--path', type=str, help='Path to Folder to check for .nc files', )
        parser.add_argument('-d', '--delete', action=argparse.BooleanOptionalAction, help='Delete files after import', )

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        if not path:
            path = settings.IMPORT_PATH
        delete = kwargs['delete']
        for filename in os.listdir(path):
            if not filename.endswith(".nc"):
                continue
            file_path = os.path.join(path, filename)
            print(f'Importing file: {file_path}, {os.stat(file_path).st_size / (1024 * 1024)}MB')
            ds = xarray.open_dataset(file_path, group='PRODUCT')
            time_values = ds['time_utc'].values[0]
            lat_scanlines = ds['latitude'].values[0]
            long_scanlines = ds['longitude'].values[0]
            co_scanlines = ds['carbonmonoxide_total_column'].values[0]

            start_time = time_values[0]
            end_time = time_values[-1]

            min_latitude = min(lat_scanlines.ravel())
            max_latitude = max(lat_scanlines.ravel())

            min_longitude = min(long_scanlines.ravel())
            max_longitude = max(long_scanlines.ravel())
            data_package, created = Sentinel5PData.objects.get_or_create(filename=filename, start_time=start_time,
                                                                         end_time=end_time, min_latitude=min_latitude,
                                                                         max_latitude=max_latitude,
                                                                         min_longitude=min_longitude,
                                                                         max_longitude=max_longitude)
            if data_package.fully_imported:
                print('Already imported')
                continue
            if not data_package.fully_imported and not created:
                print('Remove interrupted import')
                Scanline.objects.filter(sentinel_5p_data=data_package).delete()
            scanline_list = []
            for time in time_values:
                scanline = Scanline(sentinel_5p_data=data_package, time=time)
                scanline_list.append(scanline)
            Scanline.objects.bulk_create(scanline_list)
            co_data_list = []
            for lat_values, long_values, co_values, scanline in zip(lat_scanlines, long_scanlines, co_scanlines,
                                                                scanline_list):
                for lat, long, co in zip(lat_values, long_values, co_values):
                    co_data = CoData(scanline=scanline, latitude=lat, longitude=long, co_value=co)
                    co_data_list.append(co_data)
            CoData.objects.bulk_create(co_data_list)
            data_package.fully_imported = True
            data_package.save()
            if delete:
                print(f'Removing file: {file_path}')
                os.remove(file_path)
