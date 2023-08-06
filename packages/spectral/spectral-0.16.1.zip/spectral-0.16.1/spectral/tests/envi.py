#########################################################################
#
#   envi.py - This file is part of the Spectral Python (SPy) package.
#
#   Copyright (C) 2013 Thomas Boggs
#
#   Spectral Python is free software; you can redistribute it and/
#   or modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#
#   Spectral Python is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this software; if not, write to
#
#               Free Software Foundation, Inc.
#               59 Temple Place, Suite 330
#               Boston, MA 02111-1307
#               USA
#
#########################################################################
#
# Send comments to:
# Thomas Boggs, tboggs@users.sourceforge.net
#
# spyfile.py
'''Runs unit tests of functions associated with the ENVI file format.

To run the unit tests, type the following from the system command line:

    # python -m spectral.tests.envi
'''

from __future__ import division, print_function, unicode_literals

import numpy as np
import os
from numpy.testing import assert_almost_equal
from .spytest import SpyTest
from spectral.tests import testdir

class ENVIWriteTest(SpyTest):
    '''Tests that SpyFile memmap interfaces read and write properly.'''
    def __init__(self):
        pass

    def setup(self):
        import os
        if not os.path.isdir(testdir):
            os.makedirs(testdir)
        
    def test_save_image_ndarray(self):
        '''Test saving an ENVI formated image from a numpy.ndarray.'''
        import os
        import spectral
        (R, B, C) = (10, 20, 30)
        (r, b, c) = (3, 8, 23)
        datum = 33
        data = np.zeros((R, B, C), dtype=np.uint16)
        data[r, b, c] = datum
        fname = os.path.join(testdir, 'test_save_image_ndarray.hdr')
        spectral.envi.save_image(fname, data, interleave='bil')
        img = spectral.open_image(fname)
        assert_almost_equal(img[r, b, c], datum)

    def test_save_image_ndarray_no_ext(self):
        '''Test saving an ENVI formated image with no image file extension.'''
        import os
        import spectral
        data = np.arange(1000, dtype=np.int16).reshape(10, 10, 10)
        base = os.path.join(testdir, 'test_save_image_ndarray_noext')
        hdr_file = base + '.hdr'
        spectral.envi.save_image(hdr_file, data, ext='')
        rdata = spectral.open_image(hdr_file).load()
        assert(np.all(data==rdata))

    def test_save_image_ndarray_alt_ext(self):
        '''Test saving an ENVI formated image with alternate extension.'''
        import os
        import spectral
        data = np.arange(1000, dtype=np.int16).reshape(10, 10, 10)
        base = os.path.join(testdir, 'test_save_image_ndarray_alt_ext')
        hdr_file = base + '.hdr'
        ext = '.foo'
        img_file = base + ext
        spectral.envi.save_image(hdr_file, data, ext=ext)
        rdata = spectral.envi.open(hdr_file, img_file).load()
        assert(np.all(data==rdata))

    def test_save_image_spyfile(self):
        '''Test saving an ENVI formatted image from a SpyFile object.'''
        import os
        import spectral
        (r, b, c) = (3, 8, 23)
        fname = os.path.join(testdir, 'test_save_image_spyfile.hdr')
        src = spectral.open_image('92AV3C.lan')
        spectral.envi.save_image(fname, src)
        img = spectral.open_image(fname)
        assert_almost_equal(src[r, b, c], img[r, b, c])

    def test_create_image_metadata(self):
        '''Test calling `envi.create_image` using a metadata dict.'''
        import os
        import spectral
        (R, B, C) = (10, 20, 30)
        (r, b, c) = (3, 8, 23)
        datum = 33
        md = {'lines': R,
              'samples': B,
              'bands': C,
              'data type': 12}
        fname = os.path.join(testdir, 'test_create_image_metadata.hdr')
        img = spectral.envi.create_image(fname, md)
        mm = img.open_memmap(writable=True)
        mm.fill(0)
        mm[r, b, c] = datum
        mm.flush()
        img = spectral.open_image(fname)
        assert_almost_equal(img[r, b, c], datum)

    def test_create_image_keywords(self):
        '''Test calling `envi.create_image` using keyword args.'''
        import os
        import spectral
        (R, B, C) = (10, 20, 30)
        (r, b, c) = (3, 8, 23)
        datum = 33
        fname = os.path.join(testdir, 'test_create_image_keywords.hdr')
        img = spectral.envi.create_image(fname, shape=(R,B,C),
                                         dtype=np.uint16,
                                         offset=120)
        mm = img.open_memmap(writable=True)
        mm.fill(0)
        mm[r, b, c] = datum
        mm.flush()
        img = spectral.open_image(fname)
        assert_almost_equal(img[r, b, c], datum)

    def test_save_invalid_dtype_fails(self):
        '''Should not be able to write unsupported data type to file.''' 
        import spectral as spy
        from spectral.io.envi import EnviDataTypeError
        a = np.random.randint(0, 200, 900).reshape((30, 30)).astype(np.int8)
        fname = os.path.join(testdir, 'test_save_invalid_dtype_fails.hdr')
        try:
            spy.envi.save_image('invalid.hdr', a)
        except EnviDataTypeError as e:
            pass
        else:
            raise Exception('Expected EnviDataTypeError to be raised.')
        
    def test_save_load_classes(self):
        '''Verify that `envi.save_classification` saves data correctly.'''
        import spectral as spy
        fname = os.path.join(testdir, 'test_save_load_classes.hdr')
        gt = spy.open_image('92AV3GT.GIS').read_band(0)
        spy.envi.save_classification(fname, gt, dtype=np.uint8)
        gt2 = spy.open_image(fname).read_band(0)
        assert(np.all(gt == gt2))

def run():
    print('\n' + '-' * 72)
    print('Running ENVI tests.')
    print('-' * 72)
    write_test = ENVIWriteTest()
    write_test.run()

if __name__ == '__main__':
    from spectral.tests.run import parse_args, reset_stats, print_summary
    parse_args()
    reset_stats()
    run()
    print_summary()
