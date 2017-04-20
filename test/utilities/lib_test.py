import datetime as dt

import numpy as np
import numpy.ma as ma
import numpy.testing as npt

from utilities import lib


class Test:
    def test_build_qa_mask(self):
        inputarray = np.array([-3000, 3244, 1000, 2320, 1232, 9093, -3000])
        reliability = np.array([-1, 0, 1, 2, 3, 0, 0])
        correctmask = np.array([1, 0, 1, 1, 1, 0, 1])
        lib.build_qa_mask(inputarray, reliability)
        npt.assert_array_equal(reliability, correctmask)
        assert ma.array(inputarray, mask=reliability).sum() == 12337

    def test_get_filenames_list(self):
        files_from = "../test_data/data_list.txt"
        files = ["A2016177_clipped_mosaic_250m 16 days NDVI.tif",
                 "A2016177_clipped_mosaic_250m 16 days pixel reliability.tif",
                 "A2016193_clipped_mosaic_250m 16 days NDVI.tif",
                 "A2016193_clipped_mosaic_250m 16 days pixel reliability.tif"]
        assert files == lib.get_filenames_list(files_from)

    def test_get_data_and_reliability_lists(self):
        directory_path = "../test_data"
        data_file_regex = "clipped_mosaic.*NDVI"
        reliability_file_regex = "clipped_mosaic.*Quality"
        date_regex = "\d{7}"
        data_files = ["A2016177_clipped_mosaic_250m 16 days NDVI.tif", "A2016193_clipped_mosaic_250m 16 days NDVI.tif"]
        data_files.sort(reverse=True)
        reliability_files = ["A2016177_clipped_mosaic_250m 16 days pixel reliability.tif",
                             "A2016193_clipped_mosaic_250m 16 days pixel reliability.tif"]
        reliability_files.sort(reverse=True)
        assert data_files, reliability_files == lib.get_data_and_reliability_lists(directory_path, data_file_regex,
                                                                               date_regex, reliability_file_regex)

    def test_get_files_in_time_range(self):
        start = dt.datetime.strptime("2016150", lib.YEAR_DAY)
        end = dt.datetime.strptime("2016192", lib.YEAR_DAY)
        files = ["A2016177_clipped_mosaic_250m 16 days NDVI.tif", "A2016193_clipped_mosaic_250m 16 days NDVI.tif",
                 "A2016177_clipped_mosaic_250m 16 days pixel reliability.tif",
                 "A2016193_clipped_mosaic_250m 16 days pixel reliability.tif"]
        date_regex = "\d{7}"
        assert lib.get_files_in_time_range(start,  end, files, date_regex) == [
            "A2016177_clipped_mosaic_250m 16 days NDVI.tif",
            "A2016177_clipped_mosaic_250m 16 days pixel reliability.tif"]

