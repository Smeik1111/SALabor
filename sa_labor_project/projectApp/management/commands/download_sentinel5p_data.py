import argparse
import os

import pandas
import xarray as xarray
from django.core.management import BaseCommand
from sentinelsat import SentinelAPI, geojson_to_wkt, read_geojson

from Sentinel5p_download import password, username, url
from sa_labor_project import settings


class Command(BaseCommand):
    help = 'Download last 10 days of Sentinel5P data as .nc for a given timeframe'
    username = 's5pguest'
    password = 's5pguest'
    url = 'https://s5phub.copernicus.eu/dhus/'
    def add_arguments(self, parser):
        parser.add_argument('-f', '--force', action=argparse.BooleanOptionalAction, help='Override existing data', )
        parser.add_argument('-p', '--path', type=str, help='Path to download folder', )


    def handle(self, *args, **kwargs):
        download_path = kwargs['path']
        if not download_path:
            download_path = settings.IMPORT_PATH

        for file in os.listdir(download_path):
            if file.endswith('.incomplete'):
                print(f'removing incomplete download {file}')
                os.remove(os.path.join(download_path, file))
        api = SentinelAPI(username, password, url)
        # Define the area of interest
        aoi_geojson = settings.GEOJSON_PATH
        aoi = geojson_to_wkt(read_geojson(aoi_geojson))
        # Search for Sentinel-5P data based on the area of interest and date range
        products = api.query(aoi,
                             date=('NOW-10DAYS', 'NOW'),
                             platformname='Sentinel-5 Precursor',
                             producttype='L2__CO____', )
        # Check if any products were found
        if len(products) == 0:
            print('No Sentinel-5P data found for the specified area and date range.')
        # Download the products
        i = 0
        for product in products.values():
            i += 1
            if kwargs['force']:
                os.remove(os.path.join(download_path))
            elif product['filename'] in os.listdir(download_path):
                print('already downloaded Sentinel-5P data')
                continue
            product_info = api.get_product_odata(product['uuid'])
            print(f'Donwloading {i}/{len(products)}')
            api.download(product['uuid'], directory_path=download_path)
        print('all Sentinel-5P data downloaded successfully.')