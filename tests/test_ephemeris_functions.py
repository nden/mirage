"""Unit tests for working with ephemeris files

Authors
-------
    - Bryan Hilbert

Use
---
    Ensure you have pytest installed. Then, simply run pytest in any
    parent directory of mirage/tests/:
    >>> pytest
"""

import datetime
import numpy as np
import os
import pkg_resources

from mirage.seed_image import ephemeris_tools

package_path = pkg_resources.resource_filename('mirage', '')
data_dir = os.path.join( os.path.dirname(__file__), 'test_data/ephemeris/')
CONFIG_DIR = os.path.join(package_path, 'config')


def test_create_interpol_function():
    """Create an interpolation function from an ephemeris table
    """
    ephemeris_file = os.path.join(data_dir, 'horizons_results.txt')
    ephem_table = ephemeris_tools.read_ephemeris_file(ephemeris_file)
    ra_function, dec_function = ephemeris_tools.create_interpol_function(ephem_table)

    check_time = datetime.datetime(2020, 10, 3)
    check_time_calendar = ephemeris_tools.to_timestamp(check_time)
    ra_interp = ra_function([check_time_calendar])
    dec_interp = dec_function([check_time_calendar])

    assert np.isclose(ra_interp[0], 23.74433333333333, atol=1e-9)
    assert np.isclose(dec_interp[0], 6.01483333, atol=1e-9)

def test_read_ephemeris_file():
    """Read in an ephemeris and return interpolation funcations. Development
    was based on an ephemeris file from Hoirzons.
    """
    ephemeris_file = os.path.join(data_dir, 'horizons_results.txt')
    ephem = ephemeris_tools.read_ephemeris_file(ephemeris_file)

    check_time = datetime.datetime(2020, 10, 1)
    match = ephem['Time'] == check_time

    assert np.isclose(ephem[match]['RA'].data[0], 24.299791666666664, atol=1e-9)
    assert np.isclose(ephem[match]['Dec'].data[0], 6.131916666666666, atol=1e-9)
