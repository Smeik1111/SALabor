class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        avg_filenames = "./daily_avg/s5p-CO-L3_avg_*.nc"
        operations = "squash(time, (latitude, longitude, latitude_bounds, longitude_bounds));bin()"
        merged = harp.import_product(filename=avg_filenames, reduce_operations=operations)
        merged.latitude_bounds.data[:, :]
        harp.export_product(merged, "averaged.nc")