import os
import xarray as xr
import geopandas
import rioxarray
from shapely.geometry import mapping

def get_netcdf_from_point(longitude: float, latitude: float,  start_date: str, end_date: str, filepath : str):
    """_summary_

    Args:
        longitude (float): Longitude of the point
        latitude (float): Latitude of the point
        filepath (str): Filepath of the local netcdf file
        URL (str) : URL of the netcdf file
        start_date (str): Start date of the data
        end_date (str): End date of the data

    Returns:
        _type_: xarray dataset
    """
    try :
        files = os.listdir(filepath)
        if len(files) >1:
            ds = xr.open_mfdataset("{0}*.nc".format(filepath), concat_dim="time", combine='nested', engine="netcdf4")
        else:
            ds = xr.open_dataset("{0}{1}".format(filepath, files[0]), engine="netcdf4")
    except :
        ds = xr.open_dataset(filepath, engine="netcdf4")
    try :
        ds = ds.rename({"lat" : "latitude", "lon" : "longitude"})
    except:
        pass
    ds = ds.sel(time=slice(start_date, end_date))
    ds = ds.sel(longitude=longitude, latitude=latitude, method="nearest")
    return ds



def get_netcdf_from_area(longitude_min: float, longitude_max : float, latitude_min: float, latitude_max : float, filepath: str, start_date: str, end_date: str):
    """_summary_

    Args:
        longitude_min (float): Minimum longitude of the area
        longitude_max (float): Maximum longitude of the area
        latitude_min (float): Minimum latitude of the area
        latitude_max (float): Maximum latitude of the area
        filepath (str): Filepath of the netcdf file
        start_date (str): Start date of the data
        end_date (str): End date of the data

    Returns:
        _type_: xarray dataset
    """
    try : 
        files = os.listdir(filepath)
        if len(files) >1:
            ds = xr.open_mfdataset("{0}*.nc".format(filepath), concat_dim="time", combine='nested', engine="netcdf4")
        else:
            ds = xr.open_dataset("{0}{1}".format(filepath, files[0]), engine="netcdf4")
    except :
        ds = xr.open_dataset(filepath, engine="netcdf4")
    try :
        ds = ds.rename({"lat" : "latitude", "lon" : "longitude"})
    except:
        pass
    ds = ds.sel(time=slice(start_date, end_date))
    mask_lon = (ds.longitude >= longitude_min) & (ds.longitude <= longitude_max)
    mask_lat = (ds.latitude >= latitude_min) & (ds.latitude <= latitude_max)
    ds = ds.where(mask_lon & mask_lat, drop=True)
    return ds




def get_netcdf_from_mask(filepath_mask : str, filepath_netcdf : str, start_date = None, end_date = None, row = None) :
    """_summary_

    Args:
        filepath_mask (str): Filepath of the mask file
        filepath_netcdf (str): Filepath to the netcdf file
        start_date (str): Start date of the data
        end_date (str): End date of the data
        row (int): Number of first "n" rows
    Returns:
        _type_: xarray dataset
    """
    try :
        files = os.listdir(filepath_netcdf)
        if len(files) >1:
            ds = xr.open_mfdataset("{0}*.nc".format(filepath_netcdf), concat_dim="time", combine='nested', engine="netcdf4")
        else:
            ds = xr.open_dataset("{0}{1}".format(filepath_netcdf, files[0]), engine="netcdf4")
    except :
        ds = xr.open_dataset(filepath_netcdf, engine="netcdf4")
    if row != None :
        mask = geopandas.read_file(filepath_mask, rows=int(row), crs="epsg:4326")
    else :
        mask = geopandas.read_file(filepath_mask, crs="epsg:4326")
    try :
        ds = ds.rename({"lat" : "latitude", "lon" : "longitude"})
    except :
        pass
    print(mask)
    ds.rio.set_spatial_dims(x_dim="longitude", y_dim="latitude", inplace=True)
    ds.rio.write_crs("epsg:4326", inplace=True)
    ds = ds.rio.clip(mask.geometry.apply(mapping), mask.crs, drop=False)
    try:
        ds = ds.sel(time=slice(start_date, end_date))
    except:
        pass
    return ds