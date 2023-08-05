"""
This tests whether the SplicingData object was created correctly. No
computation or visualization tests yet.
"""

import pandas.util.testing as pdt

from flotilla.data_model import SplicingData


def test_splicing_init(example_data):
    splicing_data = SplicingData(example_data.splicing)
    pdt.assert_frame_equal(splicing_data.data, example_data.splicing)
