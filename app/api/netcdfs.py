from fastapi import Header, APIRouter
from fastapi.responses import FileResponse
import uuid
from app.processing.netcdfs_processing import get_netcdf_from_point as get_netcdf
import json

env = json.load(open(".env"))
router = APIRouter()


@router.get("/")
def get_netcdf_from_point(
    longitude: float, latitude: float, filepath: str, start_date: str, end_date: str
):
    """_summary_

    Args:
        longitude (float): Longitude of the point
        latitude (float): Latitude of the point
        filepath (str): Filepath of the netcdf file
        start_date (str): Start date of the data
        end_date (str): End date of the data

    Returns:
        _type_: Netcdf file
    """
    ds = get_netcdf(longitude, latitude, filepath, start_date, end_date)
    unique_filename = str(uuid.uuid4())
    ds.to_netcdf("{0}/{1}.nc".format(env["tmp_folder"], unique_filename))
    return FileResponse(
        "{0}/{1}.nc".format(env["tmp_folder"], unique_filename),
        media_type="application/x-netcdf",
        filename="data.nc",
    )
