import app.api.netcdfs

longitude = -8.33
latitude = 43.46
filepath = "tests/data/get_data_from_point_single_file"
start_date = "2023-01-08"
end_date = "2023-01-11"

def test_get_netcdf_from_point():
    response = app.api.netcdfs.get_netcdf_from_point(
        longitude, latitude, filepath, start_date, end_date
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/x-netcdf"
    assert response.headers["Content-Disposition"] == 'attachment; filename="data.nc"'
