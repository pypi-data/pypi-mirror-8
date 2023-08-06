"""
Tests for general glymur functionality.
"""
# E1101:  assertWarns introduced in python 3.2
# pylint: disable=E1101

# R0904:  Not too many methods in unittest.
# pylint: disable=R0904

# E0611:  unittest.mock is unknown to python2.7/pylint
# pylint: disable=E0611,F0401

import doctest
import os
import re
import shutil
import struct
import sys
import tempfile
import unittest
import uuid
import warnings
from xml.etree import cElementTree as ET

import numpy as np
import pkg_resources

import glymur
from glymur import Jp2k
from glymur.version import openjpeg_version

from .fixtures import HAS_PYTHON_XMP_TOOLKIT
from .fixtures import WARNING_INFRASTRUCTURE_ISSUE, WARNING_INFRASTRUCTURE_MSG

if HAS_PYTHON_XMP_TOOLKIT:
    import libxmp
    from libxmp import XMPMeta

from .fixtures import OPJ_DATA_ROOT, opj_data_file
from . import fixtures

# Doc tests should be run as well.
def load_tests(loader, tests, ignore):
    # W0613:  "loader" and "ignore" are necessary for the protocol
    # They are unused here, however.
    # pylint: disable=W0613

    """Should run doc tests as well"""
    if os.name == "nt":
        # Can't do it on windows, temporary file issue.
        return tests
    if glymur.lib.openjp2.OPENJP2 is not None:
        tests.addTests(doctest.DocTestSuite('glymur.jp2k'))
    return tests


@unittest.skipIf(fixtures.OPENJPEG_NOT_AVAILABLE,
                 fixtures.OPENJPEG_NOT_AVAILABLE_MSG)
class SliceProtocolBase(unittest.TestCase):
    """
    Test slice protocol, i.e. when using [ ] to read image data.
    """
    @classmethod
    def setUpClass(self):

        self.jp2 = Jp2k(glymur.data.nemo())
        self.jp2_data = self.jp2.read()

        self.j2k = Jp2k(glymur.data.goodstuff())
        self.j2k_data = self.j2k.read()


@unittest.skipIf(os.name == "nt", "NamedTemporaryFile issue on windows")
class TestSliceProtocolBaseWrite(SliceProtocolBase):

    def test_write_ellipsis(self):
        expected = self.j2k_data

        with tempfile.NamedTemporaryFile(suffix='.j2k') as tfile:
            j = Jp2k(tfile.name, 'wb')
            j[...] = self.j2k_data
            actual = j.read()

        np.testing.assert_array_equal(actual, expected)

    def test_basic_write(self):
        expected = self.j2k_data

        with tempfile.NamedTemporaryFile(suffix='.j2k') as tfile:
            j = Jp2k(tfile.name, 'wb')
            j[:] = self.j2k_data
            actual = j.read()

        np.testing.assert_array_equal(actual, expected)

    def test_cannot_write_with_non_default_single_slice(self):
        with tempfile.NamedTemporaryFile(suffix='.j2k') as tfile:
            j = Jp2k(tfile.name, 'wb')
            with self.assertRaises(TypeError):
                j[slice(None, 0)] = self.j2k_data
            with self.assertRaises(TypeError):
                j[slice(0, None)] = self.j2k_data
            with self.assertRaises(TypeError):
                j[slice(0, 0, None)] = self.j2k_data
            with self.assertRaises(TypeError):
                j[slice(0, 640)] = self.j2k_data

    def test_cannot_write_a_row(self):
        with tempfile.NamedTemporaryFile(suffix='.j2k') as tfile:
            j = Jp2k(tfile.name, 'wb')
            with self.assertRaises(TypeError):
                j[5] = self.j2k_data

    def test_cannot_write_a_pixel(self):
        with tempfile.NamedTemporaryFile(suffix='.j2k') as tfile:
            j = Jp2k(tfile.name, 'wb')
            with self.assertRaises(TypeError):
                j[25, 35] = self.j2k_data[25, 35]

    def test_cannot_write_a_column(self):
        with tempfile.NamedTemporaryFile(suffix='.j2k') as tfile:
            j = Jp2k(tfile.name, 'wb')
            with self.assertRaises(TypeError):
                j[:, 25, :] = self.j2k_data[:, :25, :]

    def test_cannot_write_a_band(self):
        with tempfile.NamedTemporaryFile(suffix='.j2k') as tfile:
            j = Jp2k(tfile.name, 'wb')
            with self.assertRaises(TypeError):
                j[:, :, 0] = self.j2k_data[:, :, 0]

    def test_cannot_write_a_subarray(self):
        with tempfile.NamedTemporaryFile(suffix='.j2k') as tfile:
            j = Jp2k(tfile.name, 'wb')
            with self.assertRaises(TypeError):
                j[:25, :45, :] = self.j2k_data[:25, :25, :]


class TestSliceProtocolRead(SliceProtocolBase):

    def test_resolution_strides_cannot_differ(self):
        with self.assertRaises(IndexError):
            # Strides in x/y directions cannot differ.
            self.j2k[::2, ::3]

    def test_resolution_strides_cannot_differ(self):
        with self.assertRaises(IndexError):
            # Strides in x/y directions cannot differ.
            self.j2k[::2, ::3]

    def test_resolution_strides_must_be_powers_of_two(self):
        with self.assertRaises(IndexError):
            self.j2k[::3, ::3]

    def test_integer_index_in_3d(self):

        for j in [0, 1, 2]:
            band = self.j2k[:, :, j]
            np.testing.assert_array_equal(self.j2k_data[:, :, j], band)

    def test_slice_in_third_dimension(self):
        actual = self.j2k[:,:,1:3]
        expected = self.j2k_data[:,:,1:3]
        np.testing.assert_array_equal(actual, expected)

    def test_reduce_resolution_and_slice_in_third_dimension(self):
        d = self.j2k[::2, ::2, 1:3]
        all = self.j2k.read(rlevel=1)
        np.testing.assert_array_equal(all[:,:,1:3], d)

    def test_retrieve_single_row(self):
        actual = self.jp2[0]
        expected = self.jp2_data[0]
        np.testing.assert_array_equal(actual, expected)

    def test_retrieve_single_pixel(self):
        actual = self.jp2[0,0]
        expected = self.jp2_data[0, 0]
        np.testing.assert_array_equal(actual, expected)

    def test_retrieve_single_component(self):
        actual = self.jp2[20,20,2]
        expected = self.jp2_data[20, 20, 2]
        np.testing.assert_array_equal(actual, expected)

    def test_full_resolution_slicing_by_quarters_upper_left(self):
        actual = self.jp2[:728, :1296]
        expected = self.jp2_data[:728, :1296]
        np.testing.assert_array_equal(actual, expected)

    def test_full_resolution_slicing_by_quarters_lower_left(self):
        actual = self.jp2[728:, :1296]
        expected = self.jp2_data[728:, :1296]
        np.testing.assert_array_equal(actual, expected)

    def test_full_resolution_slicing_by_quarters_upper_right(self):
        actual = self.jp2[:728, 1296:]
        expected = self.jp2_data[:728, 1296:]
        np.testing.assert_array_equal(actual, expected)

    def test_full_resolution_slicing_by_quarters_lower_right(self):
        actual = self.jp2[728:, 1296:]
        expected = self.jp2_data[728:, 1296:]
        np.testing.assert_array_equal(actual, expected)

    def test_full_resolution_slicing_by_quarters_center(self):
        actual = self.jp2[364:1092, 648:1942]
        expected = self.jp2_data[364:1092, 648:1942]
        np.testing.assert_array_equal(actual, expected)

    def test_full_resolution_slicing_by_halves_left(self):
        actual = self.jp2[:, :1296]
        expected = self.jp2_data[:, :1296]
        np.testing.assert_array_equal(actual, expected)

    def test_full_resolution_slicing_by_right_half(self):
        actual = self.jp2[:, 1296:]
        expected = self.jp2_data[:, 1296:]
        np.testing.assert_array_equal(actual, expected)

    def test_full_resolution_slicing_by_top_half(self):
        actual = self.jp2[:728, :]
        expected = self.jp2_data[:728, :]
        np.testing.assert_array_equal(actual, expected)

    def test_full_resolution_slicing_by_bottom_half(self):
        actual = self.jp2[728:, :]
        expected = self.jp2_data[728:, :]
        np.testing.assert_array_equal(actual, expected)

    def test_region_rlevel1(self):
        actual = self.jp2[0:201:2, 0:201:2]
        expected = self.jp2.read(area=(0, 0, 201, 201), rlevel=1)
        np.testing.assert_array_equal(actual, expected)

    def test_region_rlevel1_slice_start_is_none(self):
        actual = self.jp2[:201:2, :201:2]
        expected = self.jp2.read(area=(0, 0, 201, 201), rlevel=1)
        np.testing.assert_array_equal(actual, expected)

    def test_region_rlevel1_slice_stop_is_none(self):
        actual = self.jp2[201::2, 201::2]
        expected = self.jp2.read(area=(201, 201, 1456, 2592), rlevel=1)
        np.testing.assert_array_equal(actual, expected)

    def test_region_rlevel1(self):
        actual = self.jp2[0:202:2, 0:202:2]
        expected = self.jp2.read(area=(0, 0, 202, 202), rlevel=1)
        np.testing.assert_array_equal(actual, expected)

    def test_ellipsis_full_read(self):
        actual = self.j2k[...]
        expected = self.j2k_data
        np.testing.assert_array_equal(actual, expected)

    def test_ellipsis_band_select(self):
        actual = self.j2k[..., 0]
        expected = self.j2k_data[..., 0]
        np.testing.assert_array_equal(actual, expected)

    def test_ellipsis_row_select(self):
        actual = self.j2k[0, ...]
        expected = self.j2k_data[0, ...]
        np.testing.assert_array_equal(actual, expected)

    def test_two_ellipsis_band_select(self):
        actual = self.j2k[..., ..., 1]
        expected = self.j2k_data[:, :, 1]
        np.testing.assert_array_equal(actual, expected)

    def test_two_ellipsis_row_select(self):
        actual = self.j2k[1, ..., ...]
        expected = self.j2k_data[1, :, :]
        np.testing.assert_array_equal(actual, expected)

    def test_two_ellipsis_and_full_slice(self):
        actual = self.j2k[..., ..., :]
        expected = self.j2k_data[:]
        np.testing.assert_array_equal(actual, expected)

    def test_single_slice(self):
        rows = slice(3, 8)
        actual = self.j2k[rows]
        expected = self.j2k_data[3:8, :,:]
        np.testing.assert_array_equal(actual, expected)

    def test_slice_protocol_2d_reduce_resolution(self):
        d = self.j2k[:]
        self.assertEqual(d.shape, (800, 480, 3))

        d = self.j2k[::1, ::1]
        self.assertEqual(d.shape, (800, 480, 3))

        d = self.j2k[::2, ::2]
        self.assertEqual(d.shape, (400, 240, 3))

        d = self.j2k[::4, ::4]
        self.assertEqual(d.shape, (200, 120, 3))

        d = self.j2k[::8, ::8]
        self.assertEqual(d.shape, (100, 60, 3))

        d = self.j2k[::16, ::16]
        self.assertEqual(d.shape, (50, 30, 3))

        d = self.j2k[::32, ::32]
        self.assertEqual(d.shape, (25, 15, 3))

    def test_region_rlevel5(self):
        actual = self.j2k[5:533:32, 27:423:32]
        expected = self.j2k.read(area=(5, 27, 533, 423), rlevel=5)
        np.testing.assert_array_equal(actual, expected)

@unittest.skipIf(fixtures.OPENJPEG_NOT_AVAILABLE,
                 fixtures.OPENJPEG_NOT_AVAILABLE_MSG)
@unittest.skipIf(OPJ_DATA_ROOT is None,
                 "OPJ_DATA_ROOT environment variable not set")
class TestSliceProtocolOpjData(unittest.TestCase):
    """
    Test slice protocol, i.e. when using [ ] to read image data.
    These correspond to tests for the read method with the area parameter.
    """
    @classmethod
    def setUpClass(self):

        jfile = opj_data_file('input/conformance/p1_04.j2k')
        self.j2k = Jp2k(jfile)
        self.j2k_data = self.j2k.read()
        self.j2k_half_data = self.j2k.read(rlevel=1)
        self.j2k_quarter_data = self.j2k.read(rlevel=2)

    def test_NR_DEC_p1_04_j2k_43_decode(self):
        actual = self.j2k[:1024, :1024]
        expected = self.j2k_data
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_44_decode(self):
        actual = self.j2k[640:768, 512:640]
        expected = self.j2k_data[640:768, 512:640]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_45_decode(self):
        actual = self.j2k[896:1024, 896:1024]
        expected = self.j2k_data[896:1024, 896:1024]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_46_decode(self):
        actual = self.j2k[500:800, 100:300]
        expected = self.j2k_data[500:800, 100:300]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_47_decode(self):
        actual = self.j2k[520:600, 260:360]
        expected = self.j2k_data[520:600, 260:360]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_48_decode(self):
        actual = self.j2k[520:660, 260:360]
        expected = self.j2k_data[520:660, 260:360]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_49_decode(self):
        actual = self.j2k[520:600, 360:400]
        expected = self.j2k_data[520:600, 360:400]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_50_decode(self):
        actual = self.j2k[:1024:4, :1024:4]
        expected = self.j2k_quarter_data[:256, :256]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_51_decode(self):
        actual = self.j2k[640:768:4, 512:640:4]
        expected = self.j2k_quarter_data[160:192, 128:160]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_52_decode(self):
        actual = self.j2k[896:1024:4, 896:1024:4]
        expected = self.j2k_quarter_data[224:352, 224:352]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_53_decode(self):
        actual = self.j2k[500:800:4, 100:300:4]
        expected = self.j2k_quarter_data[125:200, 25:75]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_54_decode(self):
        actual = self.j2k[520:600:4, 260:360:4]
        expected = self.j2k_quarter_data[130:150, 65:90]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_55_decode(self):
        actual = self.j2k[520:660:4, 260:360:4]
        expected = self.j2k_quarter_data[130:165, 65:90]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_04_j2k_56_decode(self):
        actual = self.j2k[520:600:4, 360:400:4]
        expected = self.j2k_quarter_data[130:150, 90:100]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p1_06_j2k_75_decode(self):
        # Image size would be 0 x 0.
        with self.assertRaises((IOError, OSError)):
            self.j2k[9:12:4, 9:12:4]

    def test_NR_DEC_p0_04_j2k_85_decode(self):
        actual = self.j2k[:256, :256]
        expected = self.j2k_data[:256, :256]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_86_decode(self):
        actual = self.j2k[:128, 128:256]
        expected = self.j2k_data[:128, 128:256]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_87_decode(self):
        actual = self.j2k[10:200, 50:120]
        expected = self.j2k_data[10:200, 50:120]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_88_decode(self):
        actual = self.j2k[150:210, 10:190]
        expected = self.j2k_data[150:210, 10:190]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_89_decode(self):
        actual = self.j2k[80:150, 100:200]
        expected = self.j2k_data[80:150, 100:200]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_90_decode(self):
        actual = self.j2k[20:50, 150:200]
        expected = self.j2k_data[20:50, 150:200]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_91_decode(self):
        actual = self.j2k[:256:4, :256:4]
        expected = self.j2k_quarter_data[0:64, 0:64]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_92_decode(self):
        actual = self.j2k[:128:4, 128:256:4]
        expected = self.j2k_quarter_data[:32, 32:64]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_93_decode(self):
        actual = self.j2k[10:200:4, 50:120:4]
        expected = self.j2k_quarter_data[3:50, 13:30]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_94_decode(self):
        actual = self.j2k[150:210:4, 10:190:4]
        expected = self.j2k_quarter_data[38:53, 3:48]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_95_decode(self):
        actual = self.j2k[80:150:4, 100:200:4]
        expected = self.j2k_quarter_data[20:38, 25:50]
        np.testing.assert_array_equal(actual, expected)

    def test_NR_DEC_p0_04_j2k_96_decode(self):
        actual = self.j2k[20:50:4, 150:200:4]
        expected = self.j2k_quarter_data[5:13, 38:50]
        np.testing.assert_array_equal(actual, expected)

@unittest.skipIf(fixtures.OPENJPEG_NOT_AVAILABLE,
                 fixtures.OPENJPEG_NOT_AVAILABLE_MSG)
class TestJp2k(unittest.TestCase):
    """These tests should be run by just about all configuration."""

    def setUp(self):
        self.jp2file = glymur.data.nemo()
        self.j2kfile = glymur.data.goodstuff()
        self.jpxfile = glymur.data.jpxfile()

    def tearDown(self):
        pass


    @unittest.skipIf(os.name == "nt", "Unexplained failure on windows")
    def test_irreversible(self):
        """Irreversible"""
        j = Jp2k(self.jp2file)
        expdata = j.read()
        with tempfile.NamedTemporaryFile(suffix='.j2k') as tfile:
            j2 = Jp2k(tfile.name, 'wb')
            j2.write(expdata, irreversible=True)

            codestream = j2.get_codestream()
            self.assertEqual(codestream.segment[2].spcod[8],
                             glymur.core.WAVELET_XFORM_9X7_IRREVERSIBLE)

            actdata = j2.read()
            self.assertTrue(fixtures.mse(actdata[0], expdata[0]) < 0.38)

    @unittest.skipIf(re.match('0|1.[0-4]', openjpeg_version) is not None,
                     "Not supported with OpenJPEG {0}".format(openjpeg_version))
    @unittest.skipIf(re.match('1.5.(1|2)', openjpeg_version) is not None,
                     "Mysteriously fails in 1.5.1 and 1.5.2")
    def test_no_cxform_pclr_jpx(self):
        """Indices for pclr jpxfile if no color transform"""
        j = Jp2k(self.jpxfile)
        rgb = j.read()
        idx = j.read(ignore_pclr_cmap_cdef=True)
        nr, nc = 1024, 1024
        self.assertEqual(rgb.shape, (nr, nc, 3))
        self.assertEqual(idx.shape, (nr, nc))

        # Should be able to manually reconstruct the RGB image from the palette
        # and indices.
        palette = j.box[2].box[2].palette
        rgb_from_idx = np.zeros(rgb.shape, dtype=np.uint8)
        for r in np.arange(nr):
            for c in np.arange(nc):
                rgb_from_idx[r, c] = palette[idx[r, c]]
        np.testing.assert_array_equal(rgb, rgb_from_idx)

    @unittest.skipIf(os.name == "nt", "Unexplained failure on windows")
    def test_repr(self):
        """Verify that results of __repr__ are eval-able."""
        j = Jp2k(self.j2kfile)
        newjp2 = eval(repr(j))

        self.assertEqual(newjp2.filename, self.j2kfile)
        self.assertEqual(newjp2.mode, 'rb')
        self.assertEqual(len(newjp2.box), 0)

    def test_rlevel_max(self):
        """Verify that rlevel=-1 gets us the lowest resolution image"""
        j = Jp2k(self.j2kfile)
        thumbnail1 = j.read(rlevel=-1)
        thumbnail2 = j.read(rlevel=5)
        np.testing.assert_array_equal(thumbnail1, thumbnail2)
        self.assertEqual(thumbnail1.shape, (25, 15, 3))

    def test_rlevel_too_high(self):
        """Should error out appropriately if reduce level too high"""
        j = Jp2k(self.jp2file)
        with self.assertRaises(IOError):
            j.read(rlevel=6)

    def test_not_jpeg2000(self):
        """Should error out appropriately if not given a JPEG 2000 file."""
        filename = pkg_resources.resource_filename(glymur.__name__, "jp2k.py")
        with self.assertRaises(IOError):
            Jp2k(filename)

    def test_file_not_present(self):
        """Should error out if reading from a file that does not exist"""
        # Verify that we error out appropriately if not given an existing file
        # at all.
        with self.assertRaises(OSError):
            filename = 'this file does not actually exist on the file system.'
            Jp2k(filename)

    def test_jp2_boxes(self):
        """Verify the boxes of a JP2 file.  Basic jp2 test."""
        jp2k = Jp2k(self.jp2file)

        # top-level boxes
        self.assertEqual(len(jp2k.box), 5)

        self.assertEqual(jp2k.box[0].box_id, 'jP  ')
        self.assertEqual(jp2k.box[0].offset, 0)
        self.assertEqual(jp2k.box[0].length, 12)
        self.assertEqual(jp2k.box[0].longname, 'JPEG 2000 Signature')

        self.assertEqual(jp2k.box[1].box_id, 'ftyp')
        self.assertEqual(jp2k.box[1].offset, 12)
        self.assertEqual(jp2k.box[1].length, 20)
        self.assertEqual(jp2k.box[1].longname, 'File Type')

        self.assertEqual(jp2k.box[2].box_id, 'jp2h')
        self.assertEqual(jp2k.box[2].offset, 32)
        self.assertEqual(jp2k.box[2].length, 45)
        self.assertEqual(jp2k.box[2].longname, 'JP2 Header')

        self.assertEqual(jp2k.box[3].box_id, 'uuid')
        self.assertEqual(jp2k.box[3].offset, 77)
        self.assertEqual(jp2k.box[3].length, 3146)

        self.assertEqual(jp2k.box[4].box_id, 'jp2c')
        self.assertEqual(jp2k.box[4].offset, 3223)
        self.assertEqual(jp2k.box[4].length, 1132296)

        # jp2h super box
        self.assertEqual(len(jp2k.box[2].box), 2)

        self.assertEqual(jp2k.box[2].box[0].box_id, 'ihdr')
        self.assertEqual(jp2k.box[2].box[0].offset, 40)
        self.assertEqual(jp2k.box[2].box[0].length, 22)
        self.assertEqual(jp2k.box[2].box[0].longname, 'Image Header')
        self.assertEqual(jp2k.box[2].box[0].height, 1456)
        self.assertEqual(jp2k.box[2].box[0].width, 2592)
        self.assertEqual(jp2k.box[2].box[0].num_components, 3)
        self.assertEqual(jp2k.box[2].box[0].bits_per_component, 8)
        self.assertEqual(jp2k.box[2].box[0].signed, False)
        self.assertEqual(jp2k.box[2].box[0].compression, 7)
        self.assertEqual(jp2k.box[2].box[0].colorspace_unknown, False)
        self.assertEqual(jp2k.box[2].box[0].ip_provided, False)

        self.assertEqual(jp2k.box[2].box[1].box_id, 'colr')
        self.assertEqual(jp2k.box[2].box[1].offset, 62)
        self.assertEqual(jp2k.box[2].box[1].length, 15)
        self.assertEqual(jp2k.box[2].box[1].longname, 'Colour Specification')
        self.assertEqual(jp2k.box[2].box[1].precedence, 0)
        self.assertEqual(jp2k.box[2].box[1].approximation, 0)
        self.assertEqual(jp2k.box[2].box[1].colorspace, glymur.core.SRGB)
        self.assertIsNone(jp2k.box[2].box[1].icc_profile)

    def test_j2k_box(self):
        """A J2K/J2C file must not have any boxes."""
        # Verify that a J2K file has no boxes.
        jp2k = Jp2k(self.j2kfile)
        self.assertEqual(len(jp2k.box), 0)

    @unittest.skipIf(os.name == "nt", "NamedTemporaryFile issue on windows")
    def test_64bit_xl_field(self):
        """XL field should be supported"""
        # Verify that boxes with the XL field are properly read.
        # Don't have such a file on hand, so we create one.  Copy our example
        # file, but making the codestream have a 64-bit XL field.
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            with open(self.jp2file, 'rb') as ifile:
                # Everything up until the jp2c box.
                write_buffer = ifile.read(3223)
                tfile.write(write_buffer)

                # The L field must be 1 in order to signal the presence of the
                # XL field.  The actual length of the jp2c box increased by 8
                # (8 bytes for the XL field).
                length = 1
                typ = b'jp2c'
                xlen = 1133427 + 8
                write_buffer = struct.pack('>I4sQ', int(length), typ, xlen)
                tfile.write(write_buffer)

                # Get the rest of the input file (minus the 8 bytes for L and
                # T.
                ifile.seek(8, 1)
                write_buffer = ifile.read()
                tfile.write(write_buffer)
                tfile.flush()

            jp2k = Jp2k(tfile.name)

            self.assertEqual(jp2k.box[4].box_id, 'jp2c')
            self.assertEqual(jp2k.box[4].offset, 3223)
            self.assertEqual(jp2k.box[4].length, 1133427 + 8)

    @unittest.skipIf(os.name == "nt", "NamedTemporaryFile issue on windows")
    def test_length_field_is_zero(self):
        """L=0 (length field in box header) is allowed"""
        # Verify that boxes with the L field as zero are correctly read.
        # This should only happen in the last box of a JPEG 2000 file.
        # Our example image has its last box at byte 588458.
        baseline_jp2 = Jp2k(self.jp2file)
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            with open(self.jp2file, 'rb') as ifile:
                # Everything up until the jp2c box.
                write_buffer = ifile.read(588458)
                tfile.write(write_buffer)

                length = 0
                typ = b'uuid'
                write_buffer = struct.pack('>I4s', int(length), typ)
                tfile.write(write_buffer)

                # Get the rest of the input file (minus the 8 bytes for L and
                # T.
                ifile.seek(8, 1)
                write_buffer = ifile.read()
                tfile.write(write_buffer)
                tfile.flush()

            new_jp2 = Jp2k(tfile.name)

            # The top level boxes in each file should match.
            for j in range(len(baseline_jp2.box)):
                self.assertEqual(new_jp2.box[j].box_id,
                                 baseline_jp2.box[j].box_id)
                self.assertEqual(new_jp2.box[j].offset,
                                 baseline_jp2.box[j].offset)
                self.assertEqual(new_jp2.box[j].length,
                                 baseline_jp2.box[j].length)

    def test_basic_jp2(self):
        """Just a very basic test that reading a JP2 file does not error out.
        """
        j2k = Jp2k(self.jp2file)
        j2k.read(rlevel=1)

    def test_basic_j2k(self):
        """This test is only useful when openjp2 is not available
        and OPJ_DATA_ROOT is not set.  We need at least one
        working J2K test.
        """
        j2k = Jp2k(self.j2kfile)
        j2k.read()

    def test_empty_box_with_j2k(self):
        """Verify that the list of boxes in a J2C/J2K file is present, but
        empty.
        """
        j = Jp2k(self.j2kfile)
        self.assertEqual(j.box, [])

    @unittest.skipIf(os.name == "nt", "NamedTemporaryFile issue on windows")
    def test_uinf_ulst_url_boxes(self):
        """Verify that we can read UINF, ULST, and URL boxes"""
        # Verify that we can read UINF, ULST, and URL boxes.  I don't have
        # easy access to such a file, and there's no such file in the
        # openjpeg repository, so I'll fake one.
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            with open(self.jp2file, 'rb') as ifile:
                # Everything up until the jp2c box.
                write_buffer = ifile.read(77)
                tfile.write(write_buffer)

                # Write the UINF superbox
                # Length = 50, id is uinf.
                write_buffer = struct.pack('>I4s', int(50), b'uinf')
                tfile.write(write_buffer)

                # Write the ULST box.
                # Length is 26, 1 UUID, hard code that UUID as zeros.
                write_buffer = struct.pack('>I4sHIIII', int(26), b'ulst',
                                           int(1), int(0), int(0), int(0),
                                           int(0))
                tfile.write(write_buffer)

                # Write the URL box.
                # Length is 16, version is one byte, flag is 3 bytes, url
                # is the rest.
                write_buffer = struct.pack('>I4sBBBB',
                                           int(16), b'url ',
                                           int(0), int(0), int(0), int(0))
                tfile.write(write_buffer)
                write_buffer = struct.pack('>ssss', b'a', b'b', b'c', b'd')
                tfile.write(write_buffer)

                # Get the rest of the input file.
                write_buffer = ifile.read()
                tfile.write(write_buffer)
                tfile.flush()

            jp2k = Jp2k(tfile.name)

            self.assertEqual(jp2k.box[3].box_id, 'uinf')
            self.assertEqual(jp2k.box[3].offset, 77)
            self.assertEqual(jp2k.box[3].length, 50)

            self.assertEqual(jp2k.box[3].box[0].box_id, 'ulst')
            self.assertEqual(jp2k.box[3].box[0].offset, 85)
            self.assertEqual(jp2k.box[3].box[0].length, 26)
            ulst = []
            ulst.append(uuid.UUID('00000000-0000-0000-0000-000000000000'))
            self.assertEqual(jp2k.box[3].box[0].ulst, ulst)

            self.assertEqual(jp2k.box[3].box[1].box_id, 'url ')
            self.assertEqual(jp2k.box[3].box[1].offset, 111)
            self.assertEqual(jp2k.box[3].box[1].length, 16)
            self.assertEqual(jp2k.box[3].box[1].version, 0)
            self.assertEqual(jp2k.box[3].box[1].flag, (0, 0, 0))
            self.assertEqual(jp2k.box[3].box[1].url, 'abcd')

    @unittest.skipIf(os.name == "nt", "NamedTemporaryFile issue on windows")
    def test_xml_with_trailing_nulls(self):
        """ElementTree doesn't like trailing null chars after valid XML text"""
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            with open(self.jp2file, 'rb') as ifile:
                # Everything up until the jp2c box.
                write_buffer = ifile.read(77)
                tfile.write(write_buffer)

                # Write the xml box
                # Length = 36, id is 'xml '.
                write_buffer = struct.pack('>I4s', int(36), b'xml ')
                tfile.write(write_buffer)

                write_buffer = '<test>this is a test</test>' + chr(0)
                write_buffer = write_buffer.encode()
                tfile.write(write_buffer)

                # Get the rest of the input file.
                write_buffer = ifile.read()
                tfile.write(write_buffer)
                tfile.flush()

            jp2k = Jp2k(tfile.name)

            self.assertEqual(jp2k.box[3].box_id, 'xml ')
            self.assertEqual(jp2k.box[3].offset, 77)
            self.assertEqual(jp2k.box[3].length, 36)
            self.assertEqual(ET.tostring(jp2k.box[3].xml.getroot()),
                             b'<test>this is a test</test>')

    @unittest.skipIf(not HAS_PYTHON_XMP_TOOLKIT, 
                     "Requires Python XMP Toolkit >= 2.0")
    def test_xmp_attribute(self):
        """Verify the XMP packet in the shipping example file can be read."""
        j = Jp2k(self.jp2file)

        xmp = j.box[3].data
        ns0 = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'
        ns1 = '{http://ns.adobe.com/xap/1.0/}'
        name = '{0}RDF/{0}Description/{1}CreatorTool'.format(ns0, ns1)
        elt = xmp.find(name)
        self.assertEqual(elt.text, 'Google')

        xmp = XMPMeta()
        xmp.parse_from_str(j.box[3].raw_data.decode('utf-8'),
                           xmpmeta_wrap=False)
        creator_tool = xmp.get_property(libxmp.consts.XMP_NS_XMP, 'CreatorTool')
        self.assertEqual(creator_tool, 'Google') 

    @unittest.skipIf(re.match(r'''(1|2.0.0)''',
                              glymur.version.openjpeg_version) is not None,
                     "Not supported until 2.0.1")
    def test_jpx_mult_codestreams_jp2_brand(self):
        """Read JPX codestream when jp2-compatible."""
        # The file in question has multiple codestreams.
        jpx = Jp2k(self.jpxfile)
        data = jpx.read()
        self.assertEqual(data.shape, (1024, 1024, 3))


@unittest.skipIf(re.match('0|1.[0-4]', openjpeg_version) is not None,
                 "Not supported with OpenJPEG {0}".format(openjpeg_version))
@unittest.skipIf(os.name == "nt", "NamedTemporaryFile issue on windows")
class TestJp2k_write(unittest.TestCase):
    """Write tests, can be run by versions 1.5+"""

    def setUp(self):
        self.jp2file = glymur.data.nemo()
        self.j2kfile = glymur.data.goodstuff()

    def tearDown(self):
        pass

    def test_cblkh_different_than_width(self):
        """Verify that we can set a code block size where height does not equal
        width.
        """
        data = np.zeros((128, 128), dtype=np.uint8)
        with tempfile.NamedTemporaryFile(suffix='.j2k') as tfile:
            j = Jp2k(tfile.name, 'wb')

            # The code block dimensions are given as rows x columns.
            j.write(data, cbsize=(16, 32))

            codestream = j.get_codestream()

            # Code block size is reported as XY in the codestream.
            self.assertEqual(tuple(codestream.segment[2].spcod[5:7]), (3, 2))

    def test_too_many_dimensions(self):
        """OpenJP2 only allows 2D or 3D images."""
        with tempfile.NamedTemporaryFile(suffix='.j2k') as tfile:
            j = Jp2k(tfile.name, 'wb')
            with self.assertRaises(IOError):
                data = np.zeros((128, 128, 2, 2), dtype=np.uint8)
                j.write(data)

    def test_2d_rgb(self):
        """RGB must have at least 3 components."""
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            j = Jp2k(tfile.name, 'wb')
            with self.assertRaises(IOError):
                data = np.zeros((128, 128, 2), dtype=np.uint8)
                j.write(data, colorspace='rgb')

    def test_colorspace_with_j2k(self):
        """Specifying a colorspace with J2K does not make sense"""
        with tempfile.NamedTemporaryFile(suffix='.j2k') as tfile:
            j = Jp2k(tfile.name, 'wb')
            with self.assertRaises(IOError):
                data = np.zeros((128, 128, 3), dtype=np.uint8)
                j.write(data, colorspace='rgb')

    def test_specify_rgb(self):
        """specify RGB explicitly"""
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            j = Jp2k(tfile.name, 'wb')
            data = np.zeros((128, 128, 3), dtype=np.uint8)
            j.write(data, colorspace='rgb')
            self.assertEqual(j.box[2].box[1].colorspace, glymur.core.SRGB)

    def test_specify_gray(self):
        """test gray explicitly specified (that's GRAY, not GREY)"""
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            j = Jp2k(tfile.name, 'wb')
            data = np.zeros((128, 128), dtype=np.uint8)
            j.write(data, colorspace='gray')
            self.assertEqual(j.box[2].box[1].colorspace,
                             glymur.core.GREYSCALE)

    def test_specify_grey(self):
        """test grey explicitly specified"""
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            j = Jp2k(tfile.name, 'wb')
            data = np.zeros((128, 128), dtype=np.uint8)
            j.write(data, colorspace='grey')
            self.assertEqual(j.box[2].box[1].colorspace,
                             glymur.core.GREYSCALE)

    def test_grey_with_two_extra_comps(self):
        """should be able to write gray + two extra components"""
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            j = Jp2k(tfile.name, 'wb')
            data = np.zeros((128, 128, 3), dtype=np.uint8)
            j.write(data, colorspace='gray')
            self.assertEqual(j.box[2].box[0].height, 128)
            self.assertEqual(j.box[2].box[0].width, 128)
            self.assertEqual(j.box[2].box[0].num_components, 3)
            self.assertEqual(j.box[2].box[1].colorspace,
                             glymur.core.GREYSCALE)

    def test_specify_ycc(self):
        """Should reject YCC"""
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            j = Jp2k(tfile.name, 'wb')
            with self.assertRaises(IOError):
                data = np.zeros((128, 128, 3), dtype=np.uint8)
                j.write(data, colorspace='ycc')

    def test_write_with_jp2_in_caps(self):
        """should be able to write with JP2 suffix."""
        j2k = Jp2k(self.j2kfile)
        expdata = j2k.read()
        with tempfile.NamedTemporaryFile(suffix='.JP2') as tfile:
            ofile = Jp2k(tfile.name, 'wb')
            ofile.write(expdata)
            actdata = ofile.read()
            np.testing.assert_array_equal(actdata, expdata)

    def test_write_srgb_without_mct(self):
        """should be able to write RGB without specifying mct"""
        j2k = Jp2k(self.j2kfile)
        expdata = j2k.read()
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            ofile = Jp2k(tfile.name, 'wb')
            ofile.write(expdata, mct=False)
            actdata = ofile.read()
            np.testing.assert_array_equal(actdata, expdata)

            codestream = ofile.get_codestream()
            self.assertEqual(codestream.segment[2].spcod[3], 0)  # no mct

    def test_write_grayscale_with_mct(self):
        """MCT usage makes no sense for grayscale images."""
        j2k = Jp2k(self.j2kfile)
        expdata = j2k.read()
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            ofile = Jp2k(tfile.name, 'wb')
            with self.assertRaises(IOError):
                ofile.write(expdata[:, :, 0], mct=True)

    def test_write_cprl(self):
        """Must be able to write a CPRL progression order file"""
        # Issue 17
        j = Jp2k(self.jp2file)
        expdata = j.read(rlevel=1)
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            ofile = Jp2k(tfile.name, 'wb')
            ofile.write(expdata, prog='CPRL')
            actdata = ofile.read()
            np.testing.assert_array_equal(actdata, expdata)

            codestream = ofile.get_codestream()
            self.assertEqual(codestream.segment[2].spcod[0], glymur.core.CPRL)


@unittest.skipIf(fixtures.OPENJPEG_NOT_AVAILABLE,
                 fixtures.OPENJPEG_NOT_AVAILABLE_MSG)
@unittest.skipIf(glymur.version.openjpeg_version_tuple[0] >= 2,
                 "Negative tests only for version 1.x")
class TestJp2k_1_x(unittest.TestCase):
    """Test suite for openjpeg 1.x, not appropriate for 2.x"""

    def setUp(self):
        self.jp2file = glymur.data.nemo()
        self.j2kfile = glymur.data.goodstuff()

    def tearDown(self):
        pass

    def test_tile(self):
        """tile option not allowed for 1.x.
        """
        j2k = Jp2k(self.j2kfile)
        with self.assertRaises(TypeError):
            j2k.read(tile=0)

    def test_layer(self):
        """layer option not allowed for 1.x.
        """
        j2k = Jp2k(self.j2kfile)
        with self.assertRaises(TypeError):
            j2k.read(layer=1)


@unittest.skipIf(re.match(r'''2.0.0''',
                          glymur.version.openjpeg_version) is None,
                 "Tests only to be run on 2.0 official.")
class TestJp2k_2_0_official(unittest.TestCase):
    """Test suite to only be run on v2.0 official."""

    @unittest.skipIf(os.name == "nt", "NamedTemporaryFile issue on windows")
    def test_extra_components_on_v2(self):
        """Can only write 4 components on 2.0+, should error out otherwise."""
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            j = Jp2k(tfile.name, 'wb')
            data = np.zeros((128, 128, 4), dtype=np.uint8)
            with self.assertRaises(IOError):
                j.write(data)


@unittest.skipIf(glymur.version.openjpeg_version_tuple[0] < 2,
                 "Requires as least v2.0")
class TestJp2k_2_0(unittest.TestCase):
    """Test suite requiring at least version 2.0"""

    def setUp(self):
        self.jp2file = glymur.data.nemo()
        self.j2kfile = glymur.data.goodstuff()

    def tearDown(self):
        pass

    def test_bad_area_parameter(self):
        """Should error out appropriately if given a bad area parameter."""
        j = Jp2k(self.jp2file)
        with self.assertRaises(IOError):
            # Start corner must be >= 0
            j.read(area=(-1, -1, 1, 1))
        with self.assertRaises(IOError):
            # End corner must be > 0
            j.read(area=(10, 10, 0, 0))
        with self.assertRaises(IOError):
            # End corner must be >= start corner
            j.read(area=(10, 10, 8, 8))

    @unittest.skipIf(os.name == "nt", "NamedTemporaryFile issue on windows")
    def test_unrecognized_jp2_clrspace(self):
        """We only allow RGB and GRAYSCALE.  Should error out with others"""
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            j = Jp2k(tfile.name, 'wb')
            with self.assertRaises(IOError):
                data = np.zeros((128, 128, 3), dtype=np.uint8)
                j.write(data, colorspace='cmyk')

    @unittest.skipIf(os.name == "nt", "NamedTemporaryFile issue on windows")
    def test_asoc_label_box(self):
        """Test asoc and label box"""
        # Construct a fake file with an asoc and a label box, as
        # OpenJPEG doesn't have such a file.
        data = Jp2k(self.jp2file).read(rlevel=1)
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            j = Jp2k(tfile.name, 'wb')
            j.write(data)

            with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile2:

                # Offset of the codestream is where we start.
                read_buffer = tfile.read(77)
                tfile2.write(read_buffer)

                # read the rest of the file, it's the codestream.
                codestream = tfile.read()

                # Write the asoc superbox.
                # Length = 36, id is 'asoc'.
                write_buffer = struct.pack('>I4s', int(56), b'asoc')
                tfile2.write(write_buffer)

                # Write the contained label box
                write_buffer = struct.pack('>I4s', int(13), b'lbl ')
                tfile2.write(write_buffer)
                tfile2.write('label'.encode())

                # Write the xml box
                # Length = 36, id is 'xml '.
                write_buffer = struct.pack('>I4s', int(35), b'xml ')
                tfile2.write(write_buffer)

                write_buffer = '<test>this is a test</test>'
                write_buffer = write_buffer.encode()
                tfile2.write(write_buffer)

                # Now append the codestream.
                tfile2.write(codestream)
                tfile2.flush()

                jasoc = Jp2k(tfile2.name)
                self.assertEqual(jasoc.box[3].box_id, 'asoc')
                self.assertEqual(jasoc.box[3].box[0].box_id, 'lbl ')
                self.assertEqual(jasoc.box[3].box[0].label, 'label')
                self.assertEqual(jasoc.box[3].box[1].box_id, 'xml ')


@unittest.skipIf(re.match(r'''0|1|2.0.0''',
                          glymur.version.openjpeg_version) is not None,
                 "Not to be run until unless 2.0.1 or higher is present")
class TestJp2k_2_1(unittest.TestCase):
    """Only to be run in 2.0+."""

    def setUp(self):
        self.jp2file = glymur.data.nemo()
        self.j2kfile = glymur.data.goodstuff()

    def tearDown(self):
        pass

    @unittest.skipIf(os.name == "nt", "NamedTemporaryFile issue on windows")
    def test_grey_with_extra_component(self):
        """version 2.0 cannot write gray + extra"""
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            j = Jp2k(tfile.name, 'wb')
            data = np.zeros((128, 128, 2), dtype=np.uint8)
            j.write(data)
            self.assertEqual(j.box[2].box[0].height, 128)
            self.assertEqual(j.box[2].box[0].width, 128)
            self.assertEqual(j.box[2].box[0].num_components, 2)
            self.assertEqual(j.box[2].box[1].colorspace,
                             glymur.core.GREYSCALE)

    @unittest.skipIf(os.name == "nt", "NamedTemporaryFile issue on windows")
    def test_rgb_with_extra_component(self):
        """v2.0+ should be able to write extra components"""
        with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
            j = Jp2k(tfile.name, 'wb')
            data = np.zeros((128, 128, 4), dtype=np.uint8)
            j.write(data)
            self.assertEqual(j.box[2].box[0].height, 128)
            self.assertEqual(j.box[2].box[0].width, 128)
            self.assertEqual(j.box[2].box[0].num_components, 4)
            self.assertEqual(j.box[2].box[1].colorspace, glymur.core.SRGB)

    @unittest.skipIf(WARNING_INFRASTRUCTURE_ISSUE, WARNING_INFRASTRUCTURE_MSG)
    @unittest.skipIf(os.name == "nt", "NamedTemporaryFile issue on windows")
    def test_openjpeg_library_message(self):
        """Verify the error message produced by the openjpeg library"""
        # This will confirm that the error callback mechanism is working.
        with open(self.jp2file, 'rb') as fptr:
            data = fptr.read()
            with tempfile.NamedTemporaryFile(suffix='.jp2') as tfile:
                # Codestream starts at byte 3323. SIZ marker at 3233.
                # COD marker at 3282.  Subsampling at 3276.
                offset = 3223
                tfile.write(data[0:offset+52])

                # Make the DY bytes of the SIZ segment zero.  That means that
                # a subsampling factor is zero, which is illegal.
                tfile.write(b'\x00')
                tfile.write(data[offset+53:offset+55])
                tfile.write(b'\x00')
                tfile.write(data[offset+57:offset+59])
                #tfile.write(data[3184:3186])
                tfile.write(b'\x00')

                tfile.write(data[offset+59:])
                #tfile.write(data[3186:])
                tfile.flush()
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    j = Jp2k(tfile.name)
                regexp = re.compile(r'''OpenJPEG\slibrary\serror:\s+
                                        Invalid\svalues\sfor\scomp\s=\s0\s+
                                        :\sdx=1\sdy=0''', re.VERBOSE)
                if sys.hexversion < 0x03020000:
                    with self.assertRaisesRegexp((IOError, OSError), regexp):
                        j.read(rlevel=1)
                else:
                    with self.assertRaisesRegex((IOError, OSError), regexp):
                        j.read(rlevel=1)

@unittest.skipIf(OPJ_DATA_ROOT is None,
                 "OPJ_DATA_ROOT environment variable not set")
class TestParsing(unittest.TestCase):
    """Tests for verifying how parsing may be altered."""
    def setUp(self):
        self.jp2file = glymur.data.nemo()
        # Reset parseoptions for every test.
        glymur.set_parseoptions(codestream=True)

    def tearDown(self):
        glymur.set_parseoptions(codestream=True)

    @unittest.skipIf(WARNING_INFRASTRUCTURE_ISSUE, WARNING_INFRASTRUCTURE_MSG)
    def test_bad_rsiz(self):
        """Should not warn if RSIZ when parsing is turned off."""
        filename = opj_data_file('input/nonregression/edf_c2_1002767.jp2')
        glymur.set_parseoptions(codestream=False)
        j = Jp2k(filename)

        glymur.set_parseoptions(codestream=True)
        with self.assertWarnsRegex(UserWarning, 'Invalid profile'):
            jp2 = Jp2k(filename)

    #@unittest.skip('trouble is a brewing...')
    def test_main_header(self):
        """Verify that the main header is not loaded when parsing turned off."""
        # The hidden _main_header attribute should show up after accessing it.
        glymur.set_parseoptions(codestream=False)
        jp2 = Jp2k(self.jp2file)
        jp2c = jp2.box[4]
        self.assertIsNone(jp2c._main_header)
        main_header = jp2c.main_header
        self.assertIsNotNone(jp2c._main_header)

@unittest.skipIf(WARNING_INFRASTRUCTURE_ISSUE, WARNING_INFRASTRUCTURE_MSG)
@unittest.skipIf(OPJ_DATA_ROOT is None,
                 "OPJ_DATA_ROOT environment variable not set")
class TestJp2kOpjDataRootWarnings(unittest.TestCase):
    """These tests should be run by just about all configuration."""

    def test_undecodeable_box_id(self):
        """Should warn in case of undecodeable box ID but not error out."""
        filename = opj_data_file('input/nonregression/edf_c2_1013627.jp2')
        with self.assertWarnsRegex(UserWarning, 'Unrecognized box'):
            jp2 = Jp2k(filename)

        # Now make sure we got all of the boxes.  Ignore the last, which was
        # bad.
        box_ids = [box.box_id for box in jp2.box[:-1]]
        self.assertEqual(box_ids, ['jP  ', 'ftyp', 'jp2h', 'jp2c'])

    def test_bad_ftyp_brand(self):
        """Should warn in case of bad ftyp brand."""
        filename = opj_data_file('input/nonregression/edf_c2_1000290.jp2')
        with self.assertWarns(UserWarning):
           jp2 = Jp2k(filename)

    def test_invalid_approximation(self):
        """Should warn in case of invalid approximation."""
        filename = opj_data_file('input/nonregression/edf_c2_1015644.jp2')
        with self.assertWarnsRegex(UserWarning, 'Invalid approximation'):
            jp2 = Jp2k(filename)

    def test_invalid_colorspace(self):
        """
        Should warn in case of invalid colorspace.

        There are multiple warnings, so there's no good way to regex them all.
        """
        filename = opj_data_file('input/nonregression/edf_c2_1103421.jp2')
        with self.assertWarns(UserWarning):
            jp2 = Jp2k(filename)

    def test_stupid_windows_eol_at_end(self):
        """Garbage characters at the end of the file."""
        filename = opj_data_file('input/nonregression/issue211.jp2')
        with self.assertWarns(UserWarning):
            jp2 = Jp2k(filename)


@unittest.skipIf(OPJ_DATA_ROOT is None,
                 "OPJ_DATA_ROOT environment variable not set")
class TestJp2kOpjDataRoot(unittest.TestCase):
    """These tests should be run by just about all configuration."""

    @unittest.skipIf(os.name == "nt", "NamedTemporaryFile issue on windows")
    def test_irreversible(self):
        """Irreversible"""
        filename = opj_data_file('input/nonregression/issue141.rawl')
        expdata = np.fromfile(filename, dtype=np.uint16)
        expdata.resize((2816, 2048))
        with tempfile.NamedTemporaryFile(suffix='.j2k') as tfile:
            j = Jp2k(tfile.name, 'wb')
            j.write(expdata, irreversible=True)

            codestream = j.get_codestream()
            self.assertEqual(codestream.segment[2].spcod[8],
                             glymur.core.WAVELET_XFORM_9X7_IRREVERSIBLE)

            actdata = j.read()
            self.assertTrue(fixtures.mse(actdata, expdata) < 250)

    @unittest.skipIf(WARNING_INFRASTRUCTURE_ISSUE, WARNING_INFRASTRUCTURE_MSG)
    def test_no_cxform_pclr_jp2(self):
        """Indices for pclr jpxfile if no color transform"""
        filename = opj_data_file('input/conformance/file9.jp2')
        with self.assertWarns(UserWarning):
            j = Jp2k(filename)
        rgb = j.read()
        idx = j.read(ignore_pclr_cmap_cdef=True)
        self.assertEqual(rgb.shape, (512, 768, 3))
        self.assertEqual(idx.shape, (512, 768))

        # Should be able to manually reconstruct the RGB image from the palette
        # and indices.
        palette = j.box[2].box[1].palette
        rgb_from_idx = np.zeros(rgb.shape, dtype=np.uint8)
        for r in np.arange(rgb.shape[0]):
            for c in np.arange(rgb.shape[1]):
                rgb_from_idx[r, c] = palette[idx[r, c]]
        np.testing.assert_array_equal(rgb, rgb_from_idx)

    @unittest.skipIf(fixtures.OPENJPEG_NOT_AVAILABLE,
                     fixtures.OPENJPEG_NOT_AVAILABLE_MSG)
    def test_read_differing_subsamples(self):
        """should error out with read used on differently subsampled images"""
        # Verify that we error out appropriately if we use the read method
        # on an image with differing subsamples
        #
        # Issue 86.
        filename = opj_data_file('input/conformance/p0_05.j2k')
        j = Jp2k(filename)
        with self.assertRaises(RuntimeError):
            j.read()
        
    @unittest.skipIf(WARNING_INFRASTRUCTURE_ISSUE, WARNING_INFRASTRUCTURE_MSG)
    def test_no_cxform_cmap(self):
        """Bands as physically ordered, not as physically intended"""
        # This file has the components physically reversed.  The cmap box
        # tells the decoder how to order them, but this flag prevents that.
        filename = opj_data_file('input/conformance/file2.jp2')
        with self.assertWarns(UserWarning):
            # The file has a bad compatibility list entry.  Not important here.
            j = Jp2k(filename)
        ycbcr = j.read()
        crcby = j.read(ignore_pclr_cmap_cdef=True)

        expected = np.zeros(ycbcr.shape, ycbcr.dtype)
        for k in range(crcby.shape[2]):
            expected[:,:,crcby.shape[2] - k - 1] = crcby[:,:,k]

        np.testing.assert_array_equal(ycbcr, expected)



if __name__ == "__main__":
    unittest.main()
