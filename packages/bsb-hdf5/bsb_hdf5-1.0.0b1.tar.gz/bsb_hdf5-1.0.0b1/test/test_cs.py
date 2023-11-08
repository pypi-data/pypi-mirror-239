from bsb.unittest import FixedPosConfigFixture, RandomStorageFixture, NumpyTestCase
from bsb.core import Scaffold
from bsb_hdf5.connectivity_set import LocationOutOfBoundsError
import unittest


class TestConnectivitySet(
    FixedPosConfigFixture,
    RandomStorageFixture,
    NumpyTestCase,
    unittest.TestCase,
    engine_name="hdf5",
):
    def setUp(self):
        super().setUp()
        self.cfg.connectivity.add(
            "all_to_all",
            dict(
                strategy="bsb.connectivity.AllToAll",
                presynaptic=dict(cell_types=["test_cell"]),
                postsynaptic=dict(cell_types=["test_cell"]),
            ),
        )
        self.network = Scaffold(self.cfg, self.storage)
        self.network.compile(clear=True, skip_connectivity=True)

    def test_pre_oob(self):
        f = self.network.connectivity.all_to_all.connect_cells

        def pre_oob_connect(pre_set, post_set, src_locs, dest_locs, tag=None):
            f(pre_set, post_set, src_locs + [100, 0, 0], dest_locs + [100, 0, 0])

        self.network.connectivity.all_to_all.connect_cells = pre_oob_connect
        with self.assertRaises(LocationOutOfBoundsError):
            self.network.compile(append=True, skip_placement=True)
