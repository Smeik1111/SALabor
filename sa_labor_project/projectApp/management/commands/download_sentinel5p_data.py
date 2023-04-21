import argparse
import os

from django.core.management import BaseCommand
from sentinelsat import SentinelAPI, geojson_to_wkt, read_geojson

from projectApp.models import Sentinel5PData
from sa_labor_project import settings




class Command(BaseCommand):
    help = 'Download last 10 days of Sentinel5P data as .nc for a given timeframe'
    username = 's5pguest'
    password = 's5pguest'
    url = 'https://s5phub.copernicus.eu/dhus/'
    timespan_start = 'NOW-10DAYS'
    timespan_end = 'NOW'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--force', action=argparse.BooleanOptionalAction, help='Dont check for existing data', )
        parser.add_argument('-p', '--path', type=str, help='Path to download folder', )


    def handle(self, *args, **kwargs):
        download_path = kwargs['path']
        if not download_path:
            download_path = settings.IMPORT_PATH

        for file in os.listdir(download_path):
            if file.endswith('.incomplete'):
                print(f'removing incomplete download {file}')
                os.remove(os.path.join(download_path, file))
        api = SentinelAPI(self.username, self.password, self.url)
        # Define the area of interest
        aoi_geojson = settings.GEOJSON_PATH
        aoi = geojson_to_wkt(read_geojson(aoi_geojson))
        # Search for Sentinel-5P data based on the area of interest and date range
        products = api.query(aoi,
                             date=(self.timespan_start, self.timespan_end),
                             platformname='Sentinel-5 Precursor',
                             producttype='L2__CO____', )
        # Check if any products were found
        if len(products) == 0:
            print('No Sentinel-5P data found for the specified area and date range.')
        # Download the products
        i = 0
        for product in products.values():
            i += 1
            filename = product['identifier']
            if kwargs['force']:
                try:
                    os.remove(os.path.join(download_path))
                except Exception:
                    pass
            elif not kwargs['force'] and product['filename'] in os.listdir(download_path):
                print('already downloaded Sentinel-5P data')
                continue
            elif not kwargs['force'] and Sentinel5PData.objects.filter(filename=filename).exists():
                print('already imported Sentinel-5P data')
                continue
            print(f'Donwloading {i}/{len(products)}')
            api.download(product['uuid'], directory_path=download_path)
        print('all Sentinel-5P data downloaded successfully.')