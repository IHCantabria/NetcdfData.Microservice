from fastapi import Header, APIRouter
from fastapi.responses import FileResponse
import uuid
from app.processing.netcdfs_processing import get_netcdf_from_point as get_netcdf
import json

env = json.load(open(".env"))
router = APIRouter()

@router.get("/")
def get_netcdf_from_point(longitude: float, latitude: float, filepath: str, start_date: str, end_date: str):
    ds = get_netcdf(longitude, latitude, filepath, start_date, end_date)
    unique_filename = str(uuid.uuid4())
    ds.to_netcdf("{0}/{1}.nc".format(env["tmp_folder"],unique_filename))
    return FileResponse("{0}/{1}.nc".format(env["tmp_folder"],unique_filename), media_type="application/x-netcdf", filename="data.nc")