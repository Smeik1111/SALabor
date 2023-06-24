

class Command(BaseCommand):
    help = 'create plots of available sentinel5p Data'

    def handle(self, *args, **kwargs):
        #depricated
        filename = "./data/S5P_OFFL_L2__CO_____20230401T020618_20230401T034748_28314_03_020500_20230402T155156.nc"
        operations = get_import_operations()
        operations = ";".join([
            "CO_column_number_density_validity>50",
            "keep(latitude_bounds,longitude_bounds,CO_column_number_density)",
            "bin_spatial(361, -90, 0.5, 721, -180, 0.5)",
            # "derive(CO_column_number_density [DU])",
            "derive(latitude {latitude})",
            "derive(longitude {longitude})",
        ])

        product = import_product(filename=filename, operations=operations)

        vals = product.CO_column_number_density.data
        units = product.CO_column_number_density.unit
        desc = product.CO_column_number_density.description

        latc = product.latitude.data
        lonc = product.longitude.data
        # print(product)
        # print(product.area)

        colortable = cm.batlow
        # For Dobson Units
        vmin = 0
        vmax = 0.09

        plot_as_scatter(latc=latc, lonc=lonc, vals=vals, vmin=vmin, vmax=vmax, colortable=colortable, desc=desc,
                        units=units)
        # print(product) # time dim in long/ lat



        regridded_product = regrid(filename, operations=operations)
        gridlat = np.append(regridded_product.latitude_bounds.data[:, 0], regridded_product.latitude_bounds.data[-1, 1])
        gridlon = np.append(regridded_product.longitude_bounds.data[:, 0],
                            regridded_product.longitude_bounds.data[-1, 1])

        vals = regridded_product.CO_column_number_density.data
        units = regridded_product.CO_column_number_density.unit
        desc = regridded_product.CO_column_number_density.description

        colortable = cm.batlow
        # For Dobson Units
        vmin = 0
        vmax = 0.09
        print(regridded_product)

        plot_as_pColormesh(gridlat=gridlat, gridlon=gridlon, vals=vals, vmin=vmin, vmax=vmax, colortable=colortable,
                           desc=desc, units=units)


        #merge multple files to one mimage
        filename_patterns = [
            "./data/S5P_OFFL_L2__CO_____20230401*.nc",
            "./data/S5P_OFFL_L2__CO_____20230402*.nc",
            "./data/S5P_OFFL_L2__CO_____20230403*.nc",
            "./data/S5P_OFFL_L2__CO_____20230404*.nc",
            "./data/S5P_OFFL_L2__CO_____20230405*.nc",
            "./data/S5P_OFFL_L2__CO_____20230406*.nc",
            "./data/S5P_OFFL_L2__CO_____20230407*.nc"
        ]

        def merge_daily_data(filename_pattern):


        # print as colormesh
        for filename_pattern in filename_patterns:
            merge_daily_data(filename_pattern)

        avg_filenames = "./daily_avg/s5p-CO-L3_avg_*.nc"

        merged = harp.import_product(filename=avg_filenames, reduce_operations=get_reduce_operations())
        merged.latitude_bounds.data[:, :]
        save_as_nc(merged, "averaged.nc")

        gridlat = np.append(merged.latitude_bounds.data[:, 0], merged.latitude_bounds.data[-1, 1]).flatten()
        gridlon = np.append(merged.longitude_bounds.data[:, 0], merged.longitude_bounds.data[-1, 1]).flatten()
        vals = merged.CO_column_number_density.data
        units = merged.CO_column_number_density.unit
        desc = merged.CO_column_number_density.description

        colortable = cm.devon_r

        vmin = 1
        vmax = 150
        merged.CO_column_number_density.data

        plot_as_pColormesh(gridlat=gridlat, gridlon=gridlon, vals=vals, vmin=vmin, vmax=vmax, colortable=colortable,
                           desc=desc, units=units, save=True, outname="averaged")


def get_regrid_operations():
    operations = ";".join([
        "CO_column_number_density_validity>50",
        "keep(latitude_bounds,longitude_bounds,CO_column_number_density)",
        "bin_spatial(3601, -90, 0.05, 7201, -180, 0.05)",
        #"derive(CO_column_number_density [DU])",
        #"derive(latitude {latitude})",
        #"derive(longitude {longitude})",
        "derive(area {time} [km2])",

    ])
    #"bin_spatial(3601, -90, 0.05, 7201, -180, 0.05)",
    return operations

def get_import_operations():
    operations = ";".join([
        "CO_column_number_density_validity>50",
        "keep(datetime_start,scan_subindex,latitude,longitude,CO_column_number_density)",
        #"derive(CO_column_number_density [DU])",
    ])
    return operations

def get_reduce_operations():
    operations = "squash(time, (latitude, longitude, latitude_bounds, longitude_bounds));bin()"
    return operations

def regrid(filename, operations):
    regridded_product = harp.import_product(filename, operations)
    return regridded_product

def import_product(filename, operations):
    reduced_product = harp.import_product(filename, operations)
    return reduced_product

def save_as_nc(data, filename):
    harp.export_product(data, filename)

