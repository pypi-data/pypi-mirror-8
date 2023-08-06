"""
The tests defined here roughly correspond to what is in the OpenJPEG test
suite.
"""

# Some test names correspond with openjpeg tests.  Long names are ok in this
# case.
# pylint: disable=C0103

# All of these tests correspond to tests in openjpeg, so no docstring is really
# needed.
# pylint: disable=C0111

# This module is very long, cannot be helped.
# pylint: disable=C0302

# unittest fools pylint with "too many public methods"
# pylint: disable=R0904

# Some tests use numpy test infrastructure, which means the tests never
# reference "self", so pylint claims it should be a function.  No, no, no.
# pylint: disable=R0201

# Many tests are pretty long and that can't be helped.
# pylint:  disable=R0915

# asserWarns introduced in python 3.2 (python2.7/pylint issue)
# pylint: disable=E1101

import re
import sys
import unittest

import numpy as np

from glymur import Jp2k
import glymur

from . import fixtures
from .fixtures import OPJ_DATA_ROOT
from .fixtures import WARNING_INFRASTRUCTURE_ISSUE, WARNING_INFRASTRUCTURE_MSG
from .fixtures import mse, peak_tolerance, read_pgx, opj_data_file


@unittest.skipIf(fixtures.OPENJPEG_NOT_AVAILABLE,
                 fixtures.OPENJPEG_NOT_AVAILABLE_MSG)
@unittest.skipIf(OPJ_DATA_ROOT is None,
                 "OPJ_DATA_ROOT environment variable not set")
@unittest.skipIf(re.match(r'''(1|2.0.0)''',
                          glymur.version.openjpeg_version) is not None,
                 "Only supported in 2.0.1 or higher")
class TestSuite2point1(unittest.TestCase):
    """Runs tests introduced in version 2.0+ or that pass only in 2.0+"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skipIf(WARNING_INFRASTRUCTURE_ISSUE, WARNING_INFRASTRUCTURE_MSG)
    def test_NR_DEC_text_GBR_jp2_29_decode(self):
        jfile = opj_data_file('input/nonregression/text_GBR.jp2')
        with self.assertWarns(UserWarning):
            # brand is 'jp2 ', but has any icc profile.
            jp2 = Jp2k(jfile)
        jp2.read()
        self.assertTrue(True)

    def test_NR_DEC_kodak_2layers_lrcp_j2c_31_decode(self):
        jfile = opj_data_file('input/nonregression/kodak_2layers_lrcp.j2c')
        Jp2k(jfile).read()
        self.assertTrue(True)

    def test_NR_DEC_kodak_2layers_lrcp_j2c_32_decode(self):
        jfile = opj_data_file('input/nonregression/kodak_2layers_lrcp.j2c')
        Jp2k(jfile).read(layer=2)
        self.assertTrue(True)

    def test_NR_DEC_issue104_jpxstream_jp2_33_decode(self):
        jfile = opj_data_file('input/nonregression/issue104_jpxstream.jp2')
        Jp2k(jfile).read()
        self.assertTrue(True)

    def test_NR_DEC_mem_b2b86b74_2753_jp2_35_decode(self):
        jfile = opj_data_file('input/nonregression/mem-b2b86b74-2753.jp2')
        Jp2k(jfile).read()
        self.assertTrue(True)

    @unittest.skipIf(WARNING_INFRASTRUCTURE_ISSUE, WARNING_INFRASTRUCTURE_MSG)
    def test_NR_DEC_gdal_fuzzer_unchecked_num_resolutions_jp2_36_decode(self):
        f = 'input/nonregression/gdal_fuzzer_unchecked_numresolutions.jp2'
        jfile = opj_data_file(f)
        with self.assertWarns(UserWarning):
            # Invalid number of resolutions.
            j = Jp2k(jfile)
            with self.assertRaises(IOError):
                j.read()

    @unittest.skipIf(WARNING_INFRASTRUCTURE_ISSUE, WARNING_INFRASTRUCTURE_MSG)
    def test_NR_DEC_gdal_fuzzer_check_number_of_tiles_jp2_38_decode(self):
        relpath = 'input/nonregression/gdal_fuzzer_check_number_of_tiles.jp2'
        jfile = opj_data_file(relpath)
        with self.assertWarns(UserWarning):
            # Invalid number of tiles.
            j = Jp2k(jfile)
            with self.assertRaises(IOError):
                j.read()

    @unittest.skipIf(WARNING_INFRASTRUCTURE_ISSUE, WARNING_INFRASTRUCTURE_MSG)
    def test_NR_DEC_gdal_fuzzer_check_comp_dx_dy_jp2_39_decode(self):
        relpath = 'input/nonregression/gdal_fuzzer_check_comp_dx_dy.jp2'
        jfile = opj_data_file(relpath)
        with self.assertWarns(UserWarning):
            # Invalid subsampling value
            with self.assertRaises(IOError):
                Jp2k(jfile).read()

    def test_NR_DEC_file_409752_jp2_40_decode(self):
        jfile = opj_data_file('input/nonregression/file409752.jp2')
        with self.assertRaises(RuntimeError):
            Jp2k(jfile).read()

    def test_NR_DEC_issue206_image_000_jp2_42_decode(self):
        jfile = opj_data_file('input/nonregression/issue206_image-000.jp2')
        Jp2k(jfile).read()
        self.assertTrue(True)

    def test_NR_DEC_p1_04_j2k_57_decode(self):
        jfile = opj_data_file('input/conformance/p1_04.j2k')
        jp2k = Jp2k(jfile)
        tdata = jp2k.read(tile=63)  # last tile
        odata = jp2k.read()
        np.testing.assert_array_equal(tdata, odata[896:1024, 896:1024])

    def test_NR_DEC_p1_04_j2k_58_decode(self):
        jfile = opj_data_file('input/conformance/p1_04.j2k')
        jp2k = Jp2k(jfile)
        tdata = jp2k.read(tile=63, rlevel=2)  # last tile
        odata = jp2k.read(rlevel=2)
        np.testing.assert_array_equal(tdata, odata[224:256, 224:256])

    def test_NR_DEC_p1_04_j2k_59_decode(self):
        jfile = opj_data_file('input/conformance/p1_04.j2k')
        jp2k = Jp2k(jfile)
        tdata = jp2k.read(tile=12)  # 2nd row, 5th column
        odata = jp2k.read()
        np.testing.assert_array_equal(tdata, odata[128:256, 512:640])

    def test_NR_DEC_p1_04_j2k_60_decode(self):
        jfile = opj_data_file('input/conformance/p1_04.j2k')
        jp2k = Jp2k(jfile)
        tdata = jp2k.read(tile=12, rlevel=1)  # 2nd row, 5th column
        odata = jp2k.read(rlevel=1)
        np.testing.assert_array_equal(tdata, odata[64:128, 256:320])

    @unittest.skipIf(WARNING_INFRASTRUCTURE_ISSUE, WARNING_INFRASTRUCTURE_MSG)
    def test_NR_DEC_jp2_36_decode(self):
        lst = ('input',
               'nonregression',
               'gdal_fuzzer_assert_in_opj_j2k_read_SQcd_SQcc.patch.jp2')
        jfile = opj_data_file('/'.join(lst))
        with self.assertWarns(UserWarning):
            # Invalid component number.
            j = Jp2k(jfile)
            with self.assertRaises(IOError):
                j.read()

@unittest.skipIf(fixtures.OPENJPEG_NOT_AVAILABLE,
                 fixtures.OPENJPEG_NOT_AVAILABLE_MSG)
@unittest.skipIf(OPJ_DATA_ROOT is None,
                 "OPJ_DATA_ROOT environment variable not set")
@unittest.skipIf(re.match(r'''(1|2.0.0)''',
                          glymur.version.openjpeg_version) is not None,
                 "Only supported in 2.0.1 or higher")
class TestReadArea(unittest.TestCase):
    """
    Runs tests introduced in version 2.0+ or that pass only in 2.0+
    
    Specifically for read method with area parameter.
    """
    @classmethod
    def setUpClass(self):

        jfile = opj_data_file('input/conformance/p1_04.j2k')
        self.j2k = Jp2k(jfile)
        self.j2k_data = self.j2k.read()
        self.j2k_half_data = self.j2k.read(rlevel=1)
        self.j2k_quarter_data = self.j2k.read(rlevel=2)

        jfile = opj_data_file('input/conformance/p1_06.j2k')
        self.j2k_p1_06 = Jp2k(jfile)

    def test_NR_DEC_p1_04_j2k_43_decode(self):
        actual = self.j2k.read(area=(0, 0, 1024, 1024))
        expected = self.j2k_data
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_44_decode(self):
        actual = self.j2k.read(area=(640, 512, 768, 640))
        expected = self.j2k_data[640:768, 512:640]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_45_decode(self):
        actual = self.j2k.read(area=(896, 896, 1024, 1024))
        expected = self.j2k_data[896:1024, 896:1024]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_46_decode(self):
        actual = self.j2k.read(area=(500, 100, 800, 300))
        expected = self.j2k_data[500:800, 100:300]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_47_decode(self):
        actual = self.j2k.read(area=(520, 260, 600, 360))
        expected = self.j2k_data[520:600, 260:360]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_48_decode(self):
        actual = self.j2k.read(area=(520, 260, 660, 360))
        expected = self.j2k_data[520:660, 260:360]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_49_decode(self):
        actual = self.j2k.read(area=(520, 360, 600, 400))
        expected = self.j2k_data[520:600, 360:400]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_50_decode(self):
        actual = self.j2k.read(area=(0, 0, 1024, 1024), rlevel=2)
        expected = self.j2k_quarter_data
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_51_decode(self):
        actual = self.j2k.read(area=(640, 512, 768, 640), rlevel=2)
        expected = self.j2k_quarter_data[160:192, 128:160]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_52_decode(self):
        actual = self.j2k.read(area=(896, 896, 1024, 1024), rlevel=2)
        expected = self.j2k_quarter_data[224:352, 224:352]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_53_decode(self):
        actual = self.j2k.read(area=(500, 100, 800, 300), rlevel=2)
        expected = self.j2k_quarter_data[125:200, 25:75]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_54_decode(self):
        actual = self.j2k.read(area=(520, 260, 600, 360), rlevel=2)
        expected = self.j2k_quarter_data[130:150, 65:90]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_55_decode(self):
        actual = self.j2k.read(area=(520, 260, 660, 360), rlevel=2)
        expected = self.j2k_quarter_data[130:165, 65:90]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_56_decode(self):
        actual = self.j2k.read(area=(520, 360, 600, 400), rlevel=2)
        expected = self.j2k_quarter_data[130:150, 90:100]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_06_j2k_70_decode(self):
        actual = self.j2k_p1_06.read(area=(9, 9, 12, 12), rlevel=1)
        self.assertEqual(actual.shape, (1, 1, 3))

    def test_NR_DEC_p1_06_j2k_71_decode(self):
        actual = self.j2k_p1_06.read(area=(10, 4, 12, 10), rlevel=1)
        self.assertEqual(actual.shape, (1, 3, 3))

    def test_NR_DEC_p1_06_j2k_72_decode(self):
        ssdata = self.j2k_p1_06.read(area=(3, 3, 9, 9), rlevel=1)
        self.assertEqual(ssdata.shape, (3, 3, 3))

    def test_NR_DEC_p1_06_j2k_73_decode(self):
        ssdata = self.j2k_p1_06.read(area=(4, 4, 7, 7), rlevel=1)
        self.assertEqual(ssdata.shape, (2, 2, 3))

    def test_NR_DEC_p1_06_j2k_74_decode(self):
        ssdata = self.j2k_p1_06.read(area=(4, 4, 5, 5), rlevel=1)
        self.assertEqual(ssdata.shape, (1, 1, 3))

    def test_NR_DEC_p1_06_j2k_75_decode(self):
        # Image size would be 0 x 0.
        with self.assertRaises((IOError, OSError)):
            self.j2k_p1_06.read(area=(9, 9, 12, 12), rlevel=2)

    def test_NR_DEC_p0_04_j2k_85_decode(self):
        actual = self.j2k.read(area=(0, 0, 256, 256))
        expected = self.j2k_data[:256, :256]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_86_decode(self):
        actual = self.j2k.read(area=(0, 128, 128, 256))
        expected = self.j2k_data[:128, 128:256]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_87_decode(self):
        actual = self.j2k.read(area=(10, 50, 200, 120))
        expected = self.j2k_data[10:200, 50:120]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_88_decode(self):
        actual = self.j2k.read(area=(150, 10, 210, 190))
        expected = self.j2k_data[150:210, 10:190]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_89_decode(self):
        actual = self.j2k.read(area=(80, 100, 150, 200))
        expected = self.j2k_data[80:150, 100:200]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_90_decode(self):
        actual = self.j2k.read(area=(20, 150, 50, 200))
        expected = self.j2k_data[20:50, 150:200]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_91_decode(self):
        actual = self.j2k.read(area=(0, 0, 256, 256), rlevel=2)
        expected = self.j2k_quarter_data[0:64, 0:64]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_92_decode(self):
        actual = self.j2k.read(area=(0, 128, 128, 256), rlevel=2)
        expected = self.j2k_quarter_data[:32, 32:64]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_93_decode(self):
        actual = self.j2k.read(area=(10, 50, 200, 120), rlevel=2)
        expected = self.j2k_quarter_data[3:50, 13:30]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_94_decode(self):
        actual = self.j2k.read(area=(150, 10, 210, 190), rlevel=2)
        expected = self.j2k_quarter_data[38:53, 3:48]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_95_decode(self):
        actual = self.j2k.read(area=(80, 100, 150, 200), rlevel=2)
        expected = self.j2k_quarter_data[20:38, 25:50]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_96_decode(self):
        actual = self.j2k.read(area=(20, 150, 50, 200), rlevel=2)
        expected = self.j2k_quarter_data[5:13, 38:50]
        np.testing.assert_array_equal(actual, expected)
