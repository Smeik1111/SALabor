import os

import xarray
from django.core.management import BaseCommand
import harp
import geopandas as gpd
import math
from sa_labor_project import settings
from shapely.geometry import Polygon

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        if not os.path.isdir(settings.COUNTRIES_PATH):
            os.makedirs(settings.COUNTRIES_PATH, exist_ok=True)
        for country_path in os.listdir(settings.GEOJSON_PATH):
            if not country_path.endswith(".geo.json"):
                continue
            country = country_path.removesuffix(".geo.json")
            country_folder_path = os.path.join(settings.COUNTRIES_PATH, country)
            if not os.path.isdir(country_folder_path):
                os.makedirs(country_folder_path, exist_ok=True)
            done_list = os.path.join(country_folder_path, "days_processed.txt")
            if not os.path.isfile(done_list):
                with open(done_list, 'w') as f:
                    f.write("Days which have been processed:")
            for file in os.listdir(settings.DAILY_AVERAGE_PATH):
                if file == "days_processed.txt":
                    continue
                date_str = file.removeprefix("s5p-CO-L3_avg_").removesuffix(".nc")
                with open(done_list, 'r') as f:
                    lines = f.readlines()
                lines = [line.strip() for line in lines[1:]]
                if date_str in lines:
                    continue

                area_of_interest = gpd.read_file(os.path.join(settings.GEOJSON_PATH, country_path))
                xmin, ymin, xmax, ymax = area_of_interest.total_bounds
                operations_trop = ";".join([
                    f"latitude>{ymin}",
                    f"latitude<{ymax}",
                    f"longitude>{xmin}",
                    f"longitude<{xmax}",
                    "keep(latitude_bounds,longitude_bounds,CO_column_number_density)",
                    "derive(CO_column_number_density [DU])",
                ])
                tropomi_CO = harp.import_product(os.path.join(settings.DAILY_AVERAGE_PATH, file), operations=operations_trop)
                tropomi = gpd.GeoDataFrame()
                tropomi['geometry'] = None
                tropomi.crs = 'epsg:4326'
                # index for the for loop to go through all TROPOMI pixels
                lat_count = tropomi_CO.latitude_bounds.data.shape[0]
                lon_count = tropomi_CO.longitude_bounds.data.shape[0]
                #tropomi['date'] = date_str  # none in all features
                for x in range(lon_count):
                    print(f"{x}/{lon_count}")
                    lon_c = tropomi_CO.longitude_bounds.data[x]
                    for y in range(lat_count):
                        #tropomi['date'] = date_str  # in properties but not in last one

                        lat_c = tropomi_CO.latitude_bounds.data[y]
                        coords = [(lon_c[0], lat_c[0]), (lon_c[0], lat_c[1]), (lon_c[1], lat_c[1]), (lon_c[1], lat_c[0]),
                                  (lon_c[0], lat_c[0])]
                        poly = Polygon(coords)
                        id = x * lat_count + (y + 1)
                        tropomi.loc[id, 'pixel_id'] = id
                        tropomi.loc[id, 'geometry'] = poly
                        co_value = tropomi_CO.CO_column_number_density.data[0][y][x]
                        if math.isnan(co_value):
                            co_value = 0.0
                        tropomi.loc[id, 'CO'] = co_value
                        tropomi['date'] = date_str  # in properties
                # TODO: add date Files, possibly over json, than export to file
                tropomi.to_file(os.path.join(country_folder_path, f'{date_str}.geo.json'), driver='GeoJSON')
                with open(done_list, 'a') as f:
                    f.write('\n' + date_str)
                continue


                exit()
                data = xarray.open_dataset(os.path.join(settings.DAILY_AVERAGE_PATH, file))
                area_of_interest = gpd.read_file(os.path.join(settings.GEOJSON_PATH, country_path))
                xmin, ymin, xmax, ymax = area_of_interest.total_bounds
                data_subset = data.sel(lon=slice(xmin, xmax), lat=slice(ymin, ymax))
                print(date_str)
                data_subset.to_netcdf(os.path.join(country_folder_path, f'{date_str}.nc'))

                exit()

                filename_tropomi = os.path.join(file, settings.DAILY_AVERAGE_PATH)
                operations_trop = ";".join([
                    "latitude>47.5",
                    "latitude<54",
                    "longitude>6",
                    "longitude<15",
                    "keep(latitude_bounds,longitude_bounds,CO_column_number_density)",
                    "derive(CO_column_number_density [DU])",
                ])
                reduce_operations = ""  # "bin()"
                tropomi_CO = harp.import_product(filename_tropomi, operations=operations_trop)
                tropomi = gpd.GeoDataFrame()
                tropomi['geometry'] = None
                tropomi['date'] = date
                tropomi.crs = 'epsg:4326'
                # index for the for loop to go through all TROPOMI pixels
                lat_count = tropomi_CO.latitude_bounds.data.shape[0]
                lon_count = tropomi_CO.longitude_bounds.data.shape[0]
                for x in range(lon_count):
                    lon_c = tropomi_CO.longitude_bounds.data[x]
                    # for y in range(lat_count):
                    lat_c = tropomi_CO.latitude_bounds.data[y]  # 47.5 x -15 ;
                    coords = [(lon_c[0], lat_c[0]), (lon_c[0], lat_c[1]), (lon_c[1], lat_c[1]), (lon_c[1], lat_c[0]),
                              (lon_c[0], lat_c[0])]
                    # print(f'lon_c={lon_c}; latc={lat_c}')
                    poly = Polygon(coords)
                    id = x * lat_count + (y + 1)
                    tropomi.loc[id, 'pixel_id'] = id
                    tropomi.loc[id, 'geometry'] = poly
                    co_value = tropomi_CO.CO_column_number_density.data[0][y][x]
                    if np.isnan(co_value):
                        co_value = 0.0
                    tropomi.loc[id, 'CO'] = co_value
