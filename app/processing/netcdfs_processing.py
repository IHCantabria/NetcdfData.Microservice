import os
import xarray as xr
import geopandas
from shapely.geometry import mapping
import fiona


def get_netcdf_from_point(longitude: float, latitude: float, path : str, start_date: str, end_date: str):
    """_summary_
    Get time series data from a point
    Args:
        longitude (float): Longitude of the point
        latitude (float): Latitude of the point
        path (int): Path of the netcdf files
        start_date (str): Start date of the data
        end_date (str): End date of the data

    Returns:
        _type_: xarray dataset
    """
    
    files = os.listdir(path)
    if len(files) >1:
        ds = xr.open_mfdataset("{0}*.nc".format(path), concat_dim="time", combine='nested', engine="netcdf4")
    else:
        ds = xr.open_dataset("{0}{1}".format(path, files[0]), engine="netcdf4")

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



def get_netcdf_from_area(longitude_min: float, longitude_max : float, latitude_min: float, latitude_max : float, path: str, start_date: str, end_date: str):
    """_summary_
    Get time series data from an area
    Args:
        longitude_min (float): Minimum longitude of the area
        longitude_max (float): Maximum longitude of the area
        latitude_min (float): Minimum latitude of the area
        latitude_max (float): Maximum latitude of the area
        path (int): Path of the netcdf files
        start_date (str): Start date of the data
        end_date (str): End date of the data

    Returns:
        _type_: xarray dataset
    """
    
    files = os.listdir(path)
    if len(files) >1:
        ds = xr.open_mfdataset("{0}*.nc".format(path), concat_dim="time", combine='nested', engine="netcdf4")
    else:
        ds = xr.open_dataset("{0}{1}".format(path, files[0]), engine="netcdf4")
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


def get_netcdf_from_mask(filepath_mask : str, path : str, row_ID = None, start_date = None, end_date = None) :
    """_summary_
    Get time series data from a mask
    Args:
        filepath_mask (str): Filepath of the mask file
        path (int): Path of the netcdf files
        start_date (str): Start date of the data
        end_date (str): End date of the data
        row_ID (int): ID of the desired mask
    Returns:
        _type_: xarray dataset
    """
    
    files = os.listdir(path)
    if len(files) >1:
        ds = xr.open_mfdataset("{0}*.nc".format(path), concat_dim="time", combine='nested', engine="netcdf4", drop_variables=["DATA_spatially_aggregated", "latitude_bounds", "longitude_bounds", "spatial_aggregation_region_id", "climatology_bounds"])
    else:
        ds = xr.open_dataset("{0}{1}".format(path, files[0]), engine="netcdf4", drop_variables="DATA_spatially_aggregated")
    if row_ID != None :
        mask = fiona.open(filepath_mask, crs="epsg:4326")
        mask = geopandas.GeoDataFrame.from_features([mask[int(row_ID)]], crs=mask.crs)
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
