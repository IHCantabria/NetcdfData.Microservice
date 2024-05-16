import app.api.netcdfs

longitude = -8.33
latitude = 43.46
product_id = 137
start_date = "2023-01-08"
end_date = "2023-01-11"

def test_get_netcdf_from_point_error():
    response = app.api.netcdfs.get_netcdf_from_point(
        product_id, longitude, latitude, start_date, end_date
    )
    assert response.status_code == 404
