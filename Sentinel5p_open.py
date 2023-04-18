import numpy as np
import xarray as xr
import netCDF4 as net
import matplotlib.pyplot as plt
import os
import geopandas as gpd
import pandas as pd


directory = "/home/xy/uniSo2023/SALabor/"
download_path = os.path.join(directory, 'downloads/')

for filename in os.listdir(download_path):
    if filename.endswith(".nc"):
        file_path = os.path.join(download_path, filename)
        print("Opening file:", file_path)
        ds = xr.open_dataset(file_path, group='PRODUCT')
        time = ds['time_utc'].values.ravel()
        data = ds['carbonmonoxide_total_column']
        lat = ds['latitude'].values.ravel()
        long = ds['longitude'].values.ravel()
        co = ds['carbonmonoxide_total_column'].values.ravel()
        df = pd.DataFrame({'time': time, 'latitude': lat, 'longitude': long, 'carbonmonoxide': co})
        filtered_df = df[df['carbonmonoxide'].notnull()]
        filtered_df.to_csv(file_path.replace('.nc','.csv'), index=False)
        #os.remove(file_path)
exit(0)
#nc = net.Dataset(file_path)


# Print information about the NetCDF file
#print(ds)
#print(ds.variables)

# Extract the data variable
data = ds['carbonmonoxide_total_column']

#lat = ds['carbonmonoxide_total_column'].latitude.values[0][0][0]
#long = ds['carbonmonoxide_total_column'].longitude.values[0][0][0]
#co = ds['carbonmonoxide_total_column'].data[0][0][0]

exit(0)


print('show plot')
# initialize an axis
fig, ax = plt.subplots(figsize=(8,6))# plot map on axis
countries = gpd.read_file(
               gpd.datasets.get_path("naturalearth_lowres"))
print('countries loaded')
countries[countries["name"] == "Germany"].plot(color="lightgrey",ax=ax)
print('countries drawn')
ds.plot.contourf(x='longitude', y='latitude',
        z='data',
        ax=ax)# add grid
print('data drawn')
ax.grid(b=True, alpha=0.5)
plt.show()
print('done')
quit(1)

# Plot the data on a map
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)
# Plot the data as a filled contour
levels = np.arange(data.min(), data.max(), (data.max()-data.min())/10)
#print(data[0][0])
#print(ds['carbonmonoxide_total_column'].latitude[0][0].values)

im = ax.contourf(ds.latitude[0], ds.longitude[0], data[0], levels=levels)
#im = ax.scatter(long, lat, c=co)
cb = plt.colorbar(im, ax=ax, orientation='vertical')
cb.ax.set_ylabel('Units')


# Add a title and show the plot
plt.title('NetCDF Data')
plt.show()
nc.close()
