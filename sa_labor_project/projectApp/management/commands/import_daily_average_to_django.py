import argparse
import os
from datetime import datetime
import geopandas as gpd
import harp
import pandas
import xarray as xarray
from django.core.management import BaseCommand
from projectApp.models import *

from sa_labor_project import settings
from projectApp.models import Country, GeoJSONFile


class Command(BaseCommand):
    help = 'Imports all refs to countrie files to db'

    def handle(self, *args, **kwargs):
        if not os.path.isdir(settings.COUNTRIES_PATH):
            os.makedirs(settings.COUNTRIES_PATH, exist_ok=True)
        for country_path in os.listdir(settings.GEOJSON_PATH):
            if not country_path.endswith(".geo.json"):
                continue
            country_name = country_path.removesuffix(".geo.json")
            country, _ = Country.objects.get_or_create(name=country_name)
            for file in os.listdir(settings.DAILY_AVERAGE_PATH):
                if file == "days_processed.txt":
                    continue
                date_str = file.removeprefix("s5p-CO-L3_avg_").removesuffix(".nc")
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
                tropomi_CO = harp.import_product(os.path.join(settings.DAILY_AVERAGE_PATH, file),
                                                 operations=operations_trop)
                date = datetime.strptime(date_str, '%Y%m%d').date()
                if country.oldest_data > date:
                    country.oldest_data = date
                    country.save()
                if country.newest_data < date:
                    country.newest_data = date
                    country.save()
                if country.lat_min is None or country.lat_max is None or country.lon_min is None \
                        or country.lon_max is None or country.lat_count is None or country.lon_count is None:
                    country.lat_min = tropomi_CO.latitude_bounds.data[0][0]
                    country.lat_max = tropomi_CO.latitude_bounds.data[-1][-1]
                    country.lat_count = tropomi_CO["CO_column_number_density"].data.shape[1]
                    country.lon_min = tropomi_CO.longitude_bounds.data[0][0]
                    country.lon_max = tropomi_CO.longitude_bounds.data[-1][-1]
                    country.lon_count = tropomi_CO["CO_column_number_density"].data.shape[2]
                    country.save()
                data = tropomi_CO["CO_column_number_density"].data.flatten()
                GeoJSONFile.objects.update_or_create(country=country,
                                                     name=file,
                                                     date=date,
                                                     data=data)
