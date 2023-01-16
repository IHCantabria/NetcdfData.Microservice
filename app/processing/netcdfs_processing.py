import os
import xarray as xr

def get_netcdf_from_point(longitude: float, latitude: float, filepath: str, start_date: str, end_date: str):
    files = os.listdir(filepath)
    if len(files) >1:
        ds = xr.open_mfdataset("{0}/*.nc".format(filepath), concat_dim="time", combine='nested', engine="netcdf4")
    else:
        ds = xr.open_dataset("{0}/{1}".format(filepath, files[0]), engine="netcdf4")
    ds = ds.sel(time=slice(start_date, end_date))
    ds = ds.sel(longitude=longitude, latitude=latitude, method="nearest")
    return ds