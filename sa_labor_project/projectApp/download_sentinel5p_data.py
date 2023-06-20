import os
from sentinelsat import SentinelAPI, geojson_to_wkt, read_geojson

from projectApp.models import Sentinel5PData
from sa_labor_project import settings


def download_sentinel5p_data(download_path: str, force: bool = False, start: str = 'NOW', end: str = 'NOW-30DAYS'):
    if not download_path:
        download_path = settings.IMPORT_PATH
    if not os.path.isdir(download_path):
        os.makedirs(download_path, exist_ok=True)
    for file in os.listdir(download_path):
        if file.endswith('.incomplete'):
            print(f'removing incomplete download {file}')
            os.remove(os.path.join(download_path, file))
    api = SentinelAPI(settings.SENTINEL5P_USERNAME, settings.SENTINEL5P_PASSWORD, settings.SENTINEL5P_URL)
    # Define the area of interest
    # aoi_geojson = settings.GEOJSON_PATH
    # aoi = geojson_to_wkt(read_geojson(aoi_geojson))
    # Search for Sentinel-5P data based on the area of interest and date range
    products = api.query(  # aoi,
        date=(start, end),
        platformname='Sentinel-5 Precursor',
        producttype='L2__CO____',
        processingmodeabbreviation='OFFL' )
    # Check if any products were found
    if len(products) == 0:
        print('No Sentinel-5P data found for the specified area and date range.')
    print(f'found {len(products)} products between {start} and {end}')
    sorted_list = list(products.values())
    sorted_list.sort(key=lambda x: x['endposition'], reverse=True)
    # Download the products
    i = 0
    done_list = os.path.join(settings.DAILY_AVERAGE_PATH, "days_processed.txt")
    if os.path.isfile(done_list):
        with open(done_list, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines[1:]]
    for product in sorted_list:
        i += 1
        filename = product['identifier']
        if force:
            try:
                os.remove(os.path.join(download_path))
            except Exception:
                pass
        elif not force and product['filename'] in os.listdir(download_path):
            print('already downloaded Sentinel-5P data')
            continue
        if os.path.isfile(done_list):
            date = product['filename'].split("_")[9].split("T")[0]
            if date in lines:
                print(f'already downloaded Sentinel-5P data in {date}')
                continue
        print(f'Downloading {i}/{len(products)}')
        api.download(product['uuid'], directory_path=download_path)
    print('all Sentinel-5P data downloaded successfully.')
