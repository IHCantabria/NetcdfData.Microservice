#create a netcdf per day from a netcdf with multiple days

from netCDF4 import Dataset
import numpy as np
import os
import datetime
import time
import xarray as xr

def create_netcdf_per_day(filepath, output_path):
    ds = xr.open_dataset(filepath, engine="netcdf4")
    time = ds["time"]
    for i in range(len(time)):
        ds_day = ds.sel(time=time[i])
        ds_day.to_netcdf("{0}/{1}.nc".format(output_path, time[i].values))

if __name__ == "__main__":
    filepath = "tests/data/get_data_from_point_single_file/Ferrol_2023010900.nc"
    output_path = "/mnt/e/tmp"
    create_netcdf_per_day(filepath, output_path)