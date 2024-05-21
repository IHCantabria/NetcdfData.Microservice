from fastapi import Header, APIRouter
from fastapi.responses import FileResponse
import uuid
from app.processing.netcdfs_processing import get_netcdf_from_point as get_netcdf_point
from app.processing.netcdfs_processing import get_netcdf_from_area as get_netcdf_area
from app.processing.netcdfs_processing import get_netcdf_from_mask as get_netcdf_mask
import requests
from requests.models import Response
import os

datahub_url_base = os.getenv("DATAHUB_URL_BASE")


router = APIRouter()


@router.get("/get_netcdf_from_point")
def get_netcdf_from_point(
    product_id : int, longitude: float, latitude: float, start_date = None, end_date = None 
):
    """_summary_

    Args:
        product_id (int): Product id
        longitude (float): Longitude of the point
        latitude (float): Latitude of the point
        start_date (str): Start date of the data
        end_date (str): End date of the data

    Returns:
        _type_: Netcdf file
    """
    product = requests.get("{0}/v1/private/NetcdfMicroservice/Products?id={1}".format(datahub_url_base, product_id)).json()
    path = product[0]["physicalPath"]
    if path != None:
        ds = get_netcdf_point(longitude, latitude, path, start_date, end_date)
        unique_filename = str(uuid.uuid4())
        ds.to_netcdf("/tmp/{0}.nc".format(unique_filename))
        return FileResponse(
            "/tmp/{0}.nc".format(unique_filename),
            media_type="application/x-netcdf",
            filename="data.nc",
        )
    else:
        # return response with error
        response = Response()
        response.status_code = 404
        response._content = b'{"detail":"Product not found"}'
        return response



@router.get("/get_netcdf_from_area")
def get_netcdf_from_area(
    longitude_min: float, longitude_max : float, latitude_min: float, latitude_max : float, product_id : int, start_date = None, end_date = None
):
    """_summary_

    Args:
        longitude_min (float): Minimum longitude of the area
        longitude_max (float): Maximum longitude of the area
        latitude_min (float): Minimum latitude of the area
        latitude_max (float): Maximum latitude of the area
        product_id (int): Product id
        start_date (str): Start date of the data
        end_date (str): End date of the data

    Returns:
        _type_: Netcdf file
    """
    product = requests.get("{0}/v1/private/NetcdfMicroservice/Products?id={1}".format(datahub_url_base, product_id)).json()
    path = product[0]["physicalPath"]
    if path != None:
        ds = get_netcdf_area(longitude_min, longitude_max, latitude_min, latitude_max, path, start_date, end_date)
        unique_filename = str(uuid.uuid4())
        ds.to_netcdf("/tmp/{0}.nc".format(unique_filename))
        return FileResponse(
            "/tmp/{0}.nc".format(unique_filename),
            media_type="application/x-netcdf",
            filename="data.nc",
        )
    else:
        # return response with error
        response = Response()
        response.status_code = 404
        response._content = b'{"detail":"Product not found"}'
        return response


@router.get("/get_netcdf_from_mask")
def get_netcdf_from_mask(
    filepath_mask : str, product_id : int, row_ID = None, start_date = None, end_date = None
):
    """_summary_

    Args:
        filepath_mask (str): Filepath or URL of the mask file
        product_id (int): Product id
        start_date (str): Start date of the data
        end_date (str): End date of the data
        row_ID (int): ID of the desired mask
    Returns:
        _type_: xarray dataset
    """
    product = requests.get("{0}/v1/private/NetcdfMicroservice/Products?id={1}".format(datahub_url_base, product_id)).json()
    path = product[0]["physicalPath"]
    if path != None:
        ds = get_netcdf_mask(filepath_mask, path, row_ID, start_date, end_date)
        unique_filename = str(uuid.uuid4())
        ds.to_netcdf("/tmp/{0}.nc".format(unique_filename))
        return FileResponse(
            "/tmp/{0}.nc".format(unique_filename),
            media_type="application/x-netcdf",
            filename="data.nc",
        )
    else:
        # return response with error
        response = Response()
        response.status_code = 404
        response._content = b'{"detail":"Product not found"}'
        return response