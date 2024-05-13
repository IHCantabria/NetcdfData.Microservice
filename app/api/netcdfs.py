from fastapi import Header, APIRouter
from fastapi.responses import FileResponse
import uuid
from app.processing.netcdfs_processing import get_netcdf_from_point as get_netcdf_point
from app.processing.netcdfs_processing import get_netcdf_from_area as get_netcdf_area
from app.processing.netcdfs_processing import get_netcdf_from_mask as get_netcdf_mask
import json


router = APIRouter()


@router.get("/get_netcdf_from_point")
def get_netcdf_from_point(
    filepath : str, longitude: float, latitude: float, start_date = None, end_date = None 
):
    """_summary_

    Args:
        longitude (float): Longitude of the point
        latitude (float): Latitude of the point
        filepath (str): Filepath or URL of the netcdf file
        start_date (str): Start date of the data
        end_date (str): End date of the data

    Returns:
        _type_: Netcdf file
    """
    ds = get_netcdf_point(longitude, latitude, start_date, end_date, filepath)
    unique_filename = str(uuid.uuid4())
    ds.to_netcdf("/tmp/{0}.nc".format(unique_filename))
    return FileResponse(
        "/tmp/{0}.nc".format(unique_filename),
        media_type="application/x-netcdf",
        filename="data.nc",
    )



@router.get("/get_netcdf_from_area")
def get_netcdf_from_area(
    longitude_min: float, longitude_max : float, latitude_min: float, latitude_max : float, filepath: str, start_date = None, end_date = None
):
    """_summary_

    Args:
        longitude_min (float): Minimum longitude of the area
        longitude_max (float): Maximum longitude of the area
        latitude_min (float): Minimum latitude of the area
        latitude_max (float): Maximum latitude of the area
        filepath (str): Filepath or URL of the netcdf file
        start_date (str): Start date of the data
        end_date (str): End date of the data

    Returns:
        _type_: Netcdf file
    """
    ds = get_netcdf_area(longitude_min, longitude_max, latitude_min, latitude_max, filepath, start_date, end_date)
    unique_filename = str(uuid.uuid4())
    ds.to_netcdf("/tmp/{0}.nc".format(unique_filename))
    return FileResponse(
        "/tmp/{0}.nc".format(unique_filename),
        media_type="application/x-netcdf",
        filename="data.nc",
    )



@router.get("/get_netcdf_from_mask")
def get_netcdf_from_mask(
    filepath_mask : str, filepath_netcdf : str, start_date = None, end_date = None, row = None
):
    """_summary_

    Args:
        filepath_mask (str): Filepath or URL of the mask file
        filepath_netcdf (str): Filepath or URL to the netcdf file
        start_date (str): Start date of the data
        end_date (str): End date of the data
        row (int): Number of first "n" mask rows
    Returns:
        _type_: xarray dataset
    """
    ds = get_netcdf_mask(filepath_mask, filepath_netcdf, start_date, end_date, row)
    unique_filename = str(uuid.uuid4())
    ds.to_netcdf("/tmp/{0}.nc".format(unique_filename))
    return FileResponse(
        "/tmp/{0}.nc".format(unique_filename),
        media_type="application/x-netcdf",
        filename="data.nc",
    )