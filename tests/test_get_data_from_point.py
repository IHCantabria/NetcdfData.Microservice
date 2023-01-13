# create test for get_data_from_point
from app.api.netcdfs import get_data_from_point
import unittest


class TestNetcdf(unittest.TestCase):
    def setUp(self):
        self.longitude = -8.33
        self.latitude = 43.46
        self.filepath = "tests/data/get_data_from_point_single_file"
        self.start_date = "2023-01-08"
        self.end_date = "2023-01-11"
        self.variable = ["sea_surface_height_above_sea_level", "sea_water_salinity"]

    def test_get_data_from_point_single_file(self):
        filepath = "tests/data/get_data_from_point_single_file"
        ds = get_data_from_point(
            self.longitude, self.latitude, filepath, self.start_date, self.end_date, self.variable
        )
        self.assert_(ds.dims["time"], 95)
        self.assert_(ds["sea_surface_height_above_sea_level"].values[0], -327 * 0.001)
        self.assert_(ds["sea_water_salinity"].values[0], 10701 *0.001 + 20)
        self.assert_(ds["sea_surface_height_above_sea_level"].values[8], -842 * 0.001)
        self.assert_(ds["sea_water_salinity"].values[8], 10653*0.001 + 20)
        self.assert_(ds["sea_surface_height_above_sea_level"].values[94], -1355 * 0.001)
        self.assert_(ds["sea_water_salinity"].values[94], 10521*0.001 + 20)

    def test_get_data_from_point_multiple_files(self):
        filepath = "tests/data/get_data_from_point_multiple_files"
        ds = get_data_from_point(
            self.longitude, self.latitude, filepath, self.start_date, self.end_date, self.variable
        )
        self.assert_(ds.dims["time"], 95)
        self.assert_(ds["sea_surface_height_above_sea_level"].values[0], -327 * 0.001)
        self.assert_(ds["sea_water_salinity"].values[0], 10701 *0.001 + 20)
        self.assert_(ds["sea_surface_height_above_sea_level"].values[8], -842 * 0.001)
        self.assert_(ds["sea_water_salinity"].values[8], 10653*0.001 + 20)
        self.assert_(ds["sea_surface_height_above_sea_level"].values[94], -1355 * 0.001)
        self.assert_(ds["sea_water_salinity"].values[94], 10521*0.001 + 20)
