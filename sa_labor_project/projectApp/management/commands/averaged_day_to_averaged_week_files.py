import os
from datetime import datetime, timedelta

import harp
from django.core.management import BaseCommand

from sa_labor_project import settings


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        DAYS_TO_AVERAGE = 7
        if not os.path.isdir(settings.DAILY_AVERAGE_PATH):
            os.makedirs(settings.DAILY_AVERAGE_PATH, exist_ok=True)
        if not os.path.isdir(settings.WEEKLY_AVERAGE_PATH):
            os.makedirs(settings.WEEKLY_AVERAGE_PATH, exist_ok=True)
        done_list = os.path.join(settings.WEEKLY_AVERAGE_PATH, "days_processed.txt")
        if not os.path.isfile(done_list):
            with open(done_list, 'w') as f:
                f.write("Days which have been processed:")
        with open(done_list, 'r') as f:
            lines = f.readlines()
            dates_already_processed = [line.strip() for line in lines[1:]]
        for file in os.listdir(settings.DAILY_AVERAGE_PATH):
            if file == "days_processed.txt":
                continue
            date_str = file.removeprefix("s5p-CO-L3_avg_").removesuffix(".nc")
            if date_str in dates_already_processed:
                continue
            date = datetime.strptime(date_str, '%Y%m%d').date()
            files_to_average = []
            for x in range(1,DAYS_TO_AVERAGE):
                date_to_check = date - timedelta(days=x)
                filepath_with_offset = os.path.join(settings.DAILY_AVERAGE_PATH, f"s5p-CO-L3_avg_{date_to_check.strftime('%Y%m%d')}.nc")
                if not os.path.isfile(filepath_with_offset):
                    break
                files_to_average.append(filepath_with_offset)
            if len(files_to_average) < DAYS_TO_AVERAGE - 1:
                continue
            operations = "squash(time, (latitude, longitude, latitude_bounds, longitude_bounds));bin()"
            merged = harp.import_product(filename=files_to_average, reduce_operations=operations)
            outpath = os.path.join(settings.WEEKLY_AVERAGE_PATH, f's5p-CO-L4_avg_week_{date.strftime("%Y%m%d")}.nc')
            if os.path.exists(outpath):
                os.remove(outpath)
            harp.export_product(merged, outpath)
            with open(done_list, 'a') as f:
                f.write('\n' + date.strftime('%Y%m%d'))
