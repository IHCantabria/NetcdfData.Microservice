# create test for get_data_from_point
from app.processing.netcdfs_processing import get_netcdf_from_point
import pytest

longitude = -8.33
latitude = 43.46
start_date = "2023-01-08"
end_date = "2023-01-11"

def test_get_netcdf_from_point_single_file():
    filepath = "tests/data/get_data_from_point_single_file"
    ds = get_netcdf_from_point(
        longitude, latitude, filepath, start_date, end_date
    )
    assert ds.dims["time"] == 95
    assert ds["sea_surface_height_above_sea_level"].values[0] == pytest.approx(-327 * 0.001)
    assert ds["sea_water_salinity"].values[0] == pytest.approx(10701 * 0.001 + 20)
    assert ds["sea_surface_height_above_sea_level"].values[8] == pytest.approx(-842 * 0.001)
    assert ds["sea_water_salinity"].values[8] == pytest.approx(10653 * 0.001 + 20)
    assert ds["sea_surface_height_above_sea_level"].values[94] == pytest.approx(-1355 * 0.001)
    assert ds["sea_water_salinity"].values[94] == pytest.approx(10521 * 0.001 + 20)

def test_get_netcdf_from_point_multiple_files():
    filepath = "tests/data/get_data_from_point_multiple_files"
    ds = get_netcdf_from_point(
        longitude, latitude, filepath, start_date, end_date
    )
    assert ds.dims["time"] == 95
    assert ds["sea_surface_height_above_sea_level"].values[0] == pytest.approx(-327 * 0.001)
    assert ds["sea_water_salinity"].values[0] == pytest.approx(10701 * 0.001 + 20)
    assert ds["sea_surface_height_above_sea_level"].values[8] == pytest.approx(-842 * 0.001)
    assert ds["sea_water_salinity"].values[8] == pytest.approx(10653 * 0.001 + 20)
    assert ds["sea_surface_height_above_sea_level"].values[94] == pytest.approx(-1355 * 0.001)
    assert ds["sea_water_salinity"].values[94] == pytest.approx(10521 * 0.001 + 20)
