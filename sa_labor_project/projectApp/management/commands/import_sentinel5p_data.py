import os

import pandas
import xarray as xarray
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Imports all .nc files to db'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--path', type=str, help='Path to Folder to check for .nc files', )
        parser.add_argument('-d', '--delete', type=bool, help='Delete files after import', )

    def handle(self, *args, **kwargs):
        print(os.path)
        path = kwargs['path']
        delete = kwargs['delete']
        for filename in os.listdir(path):
            if not filename.endswith(".nc"):
                continue
            file_path = os.path.join(path, filename)
            print("Opening file:", file_path)
            ds = xarray.open_dataset(file_path, group='PRODUCT')
            time = ds['time_utc'].values.ravel()
            data = ds['carbonmonoxide_total_column']
            lat = ds['latitude'].values.ravel()
            long = ds['longitude'].values.ravel()
            co = ds['carbonmonoxide_total_column'].values.ravel()
            df = pandas.DataFrame({'latitude': lat, 'longitude': long, 'carbonmonoxide': co})
            filtered_df = df[df['carbonmonoxide'].notnull()]
            #filtered_df.to_csv(file_path.replace('.nc', '.csv'), index=False)
            #if delete:
                #os.remove(file_path)
