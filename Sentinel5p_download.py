# Import necessary libraries
import os

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
directory = '/home/xy/uniSo2023/SALabor/'
download_path = os.path.join(directory, 'sa_labor_project/downloads/')
# Set up the API credentials
username = 's5pguest'
password = 's5pguest'
url = 'https://s5phub.copernicus.eu/dhus/'

for file in os.listdir(download_path):
    if file.endswith('.incomplete'):
        print(f'removing incomplete download {file}')
        os.remove(os.path.join(download_path, file))

api = SentinelAPI(username, password, url)
# Define the area of interest
aoi_geojson = '/home/xy/uniSo2023/SALabor/geojson.txt'
aoi = geojson_to_wkt(read_geojson(aoi_geojson))
# Search for Sentinel-5P data based on the area of interest and date range
products = api.query(aoi,
    date=('NOW-31DAYS', 'NOW'),
    platformname='Sentinel-5 Precursor',
    producttype='L2__CO____',)
# Check if any products were found
if len(products) == 0:
    print('No Sentinel-5P data found for the specified area and date range.')
# Download the products
i = len(products)
for product in products.values():
    print(f'{i} left to download')
    i -= 1
    if product['filename'] in os.listdir(download_path):
        print('already downloaded Sentinel-5P data')
        continue
    if f'{product["title"]}.csv' in os.listdir(download_path):
        print('already parsed Sentinel-5P data')
        continue
    # Get the product information
    product_info = api.get_product_odata(product['uuid'])
    # Download the product
    api.download(product['uuid'], directory_path=download_path)
    print('single Sentinel-5P data downloaded successfully.')

print('all Sentinel-5P data downloaded successfully.')