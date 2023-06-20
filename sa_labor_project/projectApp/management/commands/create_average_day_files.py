import glob
import os
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import os
import pprint

from django.core.management import BaseCommand
import harp

from sa_labor_project import settings


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        delete = True
        done_list = os.path.join(settings.DAILY_AVERAGE_PATH, "days_processed.txt")
        if not os.path.isfile(done_list):
            with open(done_list, 'w') as f:
                f.write("Days which have been processed:")
        if not os.path.isdir(settings.DAILY_AVERAGE_PATH):
            os.makedirs(settings.DAILY_AVERAGE_PATH, exist_ok=True)

        file_dict = {}
        for file in os.listdir(settings.IMPORT_PATH):
            date_str = file.split("_")[9].split("T")[0]
            file_dict[datetime.strptime(date_str, '%Y%m%d')] = file
        dates_completely_downloaded = []
        with open(done_list, 'r') as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines[1:]]
        for date in file_dict.keys():
            newer = (date + timedelta(days=1))
            older = (date - timedelta(days=1))
            if newer in file_dict.keys() or newer.strftime('%Y%m%d') in lines:
                if older in file_dict.keys() or older.strftime('%Y%m%d') in lines:
                    dates_completely_downloaded.append(date)

        dates_completely_downloaded.sort()
        print(f"{len(dates_completely_downloaded)} Days completely downloaded {dates_completely_downloaded}")

        for date in dates_completely_downloaded:
            print(f"working on {date.strftime('%Y%m%d')}")
            #outname = str.split(filename_pattern, "/")[2].removesuffix("*.nc").removeprefix("S5P_OFFL_L2__CO_____")
            reduce_operations = "squash(time, (latitude, longitude, latitude_bounds, longitude_bounds));bin()"
            operations = ";".join([
                "CO_column_number_density_validity>50",
                "keep(latitude_bounds,longitude_bounds,CO_column_number_density)",
                "bin_spatial(361, -90, 0.5, 721, -180, 0.5)",
                "derive(CO_column_number_density [DU])",
                # "derive(area {time} [km2])",
                "derive(latitude {latitude})",
                "derive(longitude {longitude})",
            ])
            filenames = glob.glob(os.path.join(settings.IMPORT_PATH,f"S5P_OFFL_L2__CO_____{date.strftime('%Y%m%d')}*.nc"))
            merged = harp.import_product(filenames, operations, reduce_operations=reduce_operations)
            outpath = os.path.join(settings.DAILY_AVERAGE_PATH, 's5p-CO-L3_avg_' + date.strftime('%Y%m%d') + '.nc')
            if os.path.exists(outpath):
                os.remove(outpath)
            harp.export_product(merged, outpath)
            with open(done_list, 'a') as f:
                f.write('\n' + date.strftime('%Y%m%d'))
            if delete:
                print(f"deleting all files belonging to {date.strftime('%Y%m%d')}")
                for file in filenames:
                    os.remove(file)



