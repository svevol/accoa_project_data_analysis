import os
import unittest
import scipy.io

from src.data.import_simulations import gather_sim_data, get_met_rxn_names


class TestImportSimulations(unittest.TestCase):

    def setUp(self):
        this_dir, this_filename = os.path.split(__file__)
        self.data_dir = os.path.join(this_dir, '..', '..', 'data', 'raw')
        self.model_name = 'putida_v2_3_all_fixed_flux'
        self.file_in = os.path.join(self.data_dir, f'simulation_{self.model_name}.mat')
        self.mat = scipy.io.loadmat(self.file_in, squeeze_me=False)


    def test_gather_sim_data(self):
        met_names, rxn_names = get_met_rxn_names(self.data_dir, self.model_name)
        time_points_spline = [10 ** -4, 10 ** -3, 10 ** -2, 10 ** -1, 1]  # , 10, 100]
        n_models = 10
        mconc_no_reg, conc_interp_no_reg, flux_interp_no_reg = gather_sim_data(self.mat, met_names, rxn_names,
                                                                               n_models, time_points_spline)
        #self.assertListEqual(TRUE_RXN_LIST, rxn_strings)
