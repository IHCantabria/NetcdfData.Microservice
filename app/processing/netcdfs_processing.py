import os
import xarray as xr
import geopandas
import rioxarray
from shapely.geometry import mapping
import fiona
import requests
import pandas as pd
import numpy as np


def get_filepath_from_indicator_id(indicator_id) :
    request_id = requests.get("https://datahubdes.ihcantabria.com/v1/public/Products").json()
    for i in range(0,468) :
        if request_id[i]["id"] == indicator_id :
            path = request_id[i]["urlBase"] + request_id[i]["urlXmlLatest"]
            data = pd.read_xml(path)
            ncdf_URL = data["urlPath"][1]
            ncdf_URL = "https://ihthreddsdev.ihcantabria.com" + "/thredds/dodsC/" + ncdf_URL
            print(ncdf_URL)
    return ncdf_URL

def get_netcdf_from_point(longitude: float, latitude: float, indicator_id : int, start_date: str, end_date: str):
    """_summary_

    Args:
        longitude (float): Longitude of the point
        latitude (float): Latitude of the point
        indicator_id (int): Indicator of the netcdf file
        start_date (str): Start date of the data
        end_date (str): End date of the data

    Returns:
        _type_: xarray dataset
    """
    
    try : 
        files = os.listdir(indicator_id)
        if len(files) >1:
            ds = xr.open_mfdataset("{0}*.nc".format(indicator_id), concat_dim="time", combine='nested', engine="netcdf4")
        else:
            ds = xr.open_dataset("{0}{1}".format(indicator_id, files[0]), engine="netcdf4")
    except :
        filepath = get_filepath_from_indicator_id(indicator_id)
        ds = xr.open_dataset(filepath)

    try :
        ds = ds.rename({"lat" : "latitude", "lon" : "longitude"})
    except:
        pass
    try :
        ds = ds.sel(time=slice(start_date, end_date))
    except :
        pass
    ds = ds.sel(longitude=longitude, latitude=latitude, method="nearest")
    return ds



def get_netcdf_from_area(longitude_min: float, longitude_max : float, latitude_min: float, latitude_max : float, indicator_id: int, start_date: str, end_date: str):
    """_summary_

    Args:
        longitude_min (float): Minimum longitude of the area
        longitude_max (float): Maximum longitude of the area
        latitude_min (float): Minimum latitude of the area
        latitude_max (float): Maximum latitude of the area
        indicator_id (int): Indicator of the netcdf file
        start_date (str): Start date of the data
        end_date (str): End date of the data

    Returns:
        _type_: xarray dataset
    """
    
    try : 
        files = os.listdir(indicator_id)
        if len(files) >1:
            ds = xr.open_mfdataset("{0}*.nc".format(indicator_id), concat_dim="time", combine='nested', engine="netcdf4")
        else:
            ds = xr.open_dataset("{0}{1}".format(indicator_id, files[0]), engine="netcdf4")
    except :
        filepath = get_filepath_from_indicator_id(indicator_id)
        ds = xr.open_dataset(filepath)
    try :
        ds = ds.rename({"lat" : "latitude", "lon" : "longitude"})
    except:
        pass
    try:
        ds = ds.sel(time=slice(start_date, end_date))
    except:
        pass
    mask_lon = (ds.longitude >= longitude_min) & (ds.longitude <= longitude_max)
    mask_lat = (ds.latitude >= latitude_min) & (ds.latitude <= latitude_max)
    ds = ds.where(mask_lon & mask_lat, drop=True)
    return ds




def get_netcdf_from_mask(filepath_mask : str, indicator_id : int, row_ID = None, start_date = None, end_date = None) :
    """_summary_

    Args:
        filepath_mask (str): Filepath of the mask file
        indicator_id (int): Indicator of the netcdf file
        start_date (str): Start date of the data
        end_date (str): End date of the data
        row_ID (int): ID of the desired mask
    Returns:
        _type_: xarray dataset
    """
    
    try :
        files = os.listdir(indicator_id)
        if len(files) >1:
            ds = xr.open_mfdataset("{0}*.nc".format(indicator_id), concat_dim="time", combine='nested', engine="netcdf4", drop_variables=["DATA_spatially_aggregated", "latitude_bounds", "longitude_bounds", "spatial_aggregation_region_id", "climatology_bounds"])
        else:
            ds = xr.open_dataset("{0}{1}".format(indicator_id, files[0]), engine="netcdf4", drop_variables="DATA_spatially_aggregated")
    except :
        filepath_netcdf = get_filepath_from_indicator_id(indicator_id)
        ds = xr.open_dataset(filepath_netcdf)
    if row_ID != None :
        mask = fiona.open(filepath_mask)
        mask = geopandas.GeoDataFrame.from_features([mask[int(row_ID)]])
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
    mask_lon = (ds.longitude >= float(mask["MIN_X"].iloc[0])) & (ds.longitude <= float(mask["MAX_X"].iloc[0]))
    mask_lat = (ds.latitude > float(mask["MIN_Y"].iloc[0])) & (ds.latitude < float(mask["MAX_Y"].iloc[0]))
    ds = ds.where(mask_lon & mask_lat, drop=True)
    try:
        ds = ds.sel(time=slice(start_date, end_date))
    except:
        pass
    return ds
