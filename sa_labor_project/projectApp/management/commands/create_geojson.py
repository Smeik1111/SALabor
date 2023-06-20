
class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        filename_tropomi = "./averaged.nc"  # "./daily_avg/s5p-CO-L3_avg_20230401.nc"
        # Deutschland: Breitengrad: 47.5 - 54; Längengrad: 6 - 15
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
        tropomi_CO

        crs = 'epsg:4326'
        tropomi = gpd.GeoDataFrame()
        tropomi['geometry'] = None
        tropomi.crs = crs
        # index for the for loop to go through all TROPOMI pixels
        lat_count = tropomi_CO.latitude_bounds.data.shape[0]
        lon_count = tropomi_CO.longitude_bounds.data.shape[0]
        print(lon_count, lat_count)
        # loop over pixels
        for x in range(lon_count):
            lon_c = tropomi_CO.longitude_bounds.data[x]
            for y in range(lat_count):
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

