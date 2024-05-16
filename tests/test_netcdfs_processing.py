# create test for get_data_from_point
from app.processing.netcdfs_processing import get_netcdf_from_point, get_netcdf_from_area, get_netcdf_from_mask
import pytest
import numpy as np

longitude = -8.33
latitude = 43.46
start_date = "2023-01-08"
end_date = "2023-01-11"

def test_get_netcdf_from_point_single_file():
    path = "tests/data/get_data_from_point_single_file/"
    ds = get_netcdf_from_point(
        longitude, latitude, path, start_date, end_date
    )
    assert ds.dims["time"] == 95
    assert ds["sea_surface_height_above_sea_level"].values[0] == pytest.approx(-327 * 0.001)
    assert ds["sea_water_salinity"].values[0] == pytest.approx(10701 * 0.001 + 20)
    assert ds["sea_surface_height_above_sea_level"].values[8] == pytest.approx(-842 * 0.001)
    assert ds["sea_water_salinity"].values[8] == pytest.approx(10653 * 0.001 + 20)
    assert ds["sea_surface_height_above_sea_level"].values[94] == pytest.approx(-1355 * 0.001)
    assert ds["sea_water_salinity"].values[94] == pytest.approx(10521 * 0.001 + 20)



def test_get_netcdf_from_area():
    path = "tests/data/get_data_from_point_single_file/"
    longitude_min = -8.267496
    longitude_max = -8.258834
    latitude_min = 43.44947052
    latitude_max = 43.46964645
    ds = get_netcdf_from_area(
        longitude_min, longitude_max, latitude_min, latitude_max, path, start_date, end_date
    )
    assert ds.dims["time"] == 95
    assert ds.dims["longitude"] == 11
    assert ds.dims["latitude"] == 33
    assert np.nanmean(ds.variables["sea_surface_height_above_sea_level"]) == pytest.approx(-0.29108825)
    assert np.nanmean(ds.variables["eastward_sea_barotropic_velocity"]) == pytest.approx(0.0016770974)
    assert np.nanmean(ds.variables["eastward_sea_water_velocity"]) == pytest.approx(0.024458151)
    assert np.nanmean(ds.variables["northward_sea_barotropic_velocity"]) == pytest.approx(-0.008823973)
    assert np.nanmean(ds.variables["northward_sea_water_velocity"]) == pytest.approx(-0.0089076795)
    assert np.nanmean(ds.variables["sea_water_potential_temperature"]) == pytest.approx(11.782998)
    assert np.nanmean(ds.variables["sea_water_salinity"]) == pytest.approx(30.22909)

    

def test_get_netcdf_from_mask():
    path = "/home/pablo807/workspace/NetcdfClimatico/PercentilesPorPaises/Data/Ncdf_test_mask/"
    filepath_mask = "/home/pablo807/workspace/NetcdfClimatico/PercentilesPorPaises/Data/MasksCountries/WB_GAD_ADM0.shp"
    row_ID = 61
    start_date = "1950/01/01"
    end_date = "2050/01/01"
    ds = get_netcdf_from_mask(
        filepath_mask, path, row_ID, start_date, end_date
    )
    assert ds.dims["longitude"] == 23
    assert ds.dims["latitude"] == 16
    assert ds.dims["time"] == 1
    assert np.nanmean(ds.variables["climatology_cdsrperiodmean_period"]) == pytest.approx(1.4977748)



