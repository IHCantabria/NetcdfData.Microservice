import app.api.netcdfs
import unittest


class TestNetcdf(unittest.TestCase):
    def setUp(self):
        self.longitude = -8.33
        self.latitude = 43.46
        self.filepath = "tests/data/get_data_from_point_single_file"
        self.start_date = "2023-01-08"
        self.end_date = "2023-01-11"

    def test_get_netcdf_from_point(self):
        response = app.api.netcdfs.get_netcdf_from_point(
            self.longitude, self.latitude, self.filepath, self.start_date, self.end_date
        )
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/x-netcdf"
        assert response.headers["Content-Disposition"] == 'attachment; filename="data.nc"'
