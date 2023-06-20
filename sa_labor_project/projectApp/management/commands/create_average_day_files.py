import os
import harp

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        filename_patterns = [
            "./downloads/S5P_OFFL_L2__CO_____20230401*.nc",
            "./data/S5P_OFFL_L2__CO_____20230402*.nc",
            "./data/S5P_OFFL_L2__CO_____20230403*.nc",
            "./data/S5P_OFFL_L2__CO_____20230404*.nc",
            "./data/S5P_OFFL_L2__CO_____20230405*.nc",
            "./data/S5P_OFFL_L2__CO_____20230406*.nc",
            "./data/S5P_OFFL_L2__CO_____20230407*.nc"
        ]

        for filename_pattern in filename_patterns:
            outname = str.split(filename_pattern, "/")[2].removesuffix("*.nc").removeprefix("S5P_OFFL_L2__CO_____")
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

            merged = harp.import_product(filename_pattern, operations, reduce_operations=reduce_operations)
            outpath = os.path.join('.', 'daily_avg', 's5p-CO-L3_avg_' + outname + '.nc')
            if not (os.path.exists(outpath)):
                harp.export_product(merged, outpath)



